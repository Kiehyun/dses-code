# 지구과학 데이터 사이언스 2 | III-02. 허블-르메트르 법칙
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 67.
# NED-D 거리 목록(2020년 4월 판)을 프로젝트 폴더에 내려받기(이미 있으면 건너뜀)
fname = "NED30.5.1-D-17.1.2-20200415.csv"
url = "https://ned.ipac.caltech.edu/Archive/Distances/" + fname
du.download(url, proj_dir / fname)

# 폴더 안의 CSV 파일 목록 만들기
fpaths = sorted(proj_dir.glob("*.csv"))
for p in fpaths:
    print(f"{p.name}  ({p.stat().st_size / 1e6:.1f} MB)")

# %% code 68.
# 파일 앞 16줄만 읽어 머리말과 첫 데이터 줄 확인
with open(fpaths[0], encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i >= 16:
            break
        print(line.rstrip()[:150])

# %% code 69.
import numpy as np
import pandas as pd

# 머리말 13줄을 건너뛰고, 첫 열(제외 코드)을 인덱스로 사용
df = pd.read_csv(fpaths[0], skiprows=13, header=None, index_col=0,
                 low_memory=False)
df.index.name = "Exclusion Code"
df.columns = ["D", "G", "Galaxy ID", "m-M", "err", "D (Mpc)", "Method", "REFCODE",
              "SN ID", "redshift (z)", "Hubble const.", "Adopted LMC modulus",
              "Date (Yr. - 1980)", "Note"]

# 숫자 열을 숫자로 변환(숫자가 아닌 칸은 NaN)
for col in ["m-M", "err", "D (Mpc)", "redshift (z)", "Hubble const."]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print(f"측정값(행) {len(df):,}개, 천체 {df['Galaxy ID'].nunique():,}개")
display(df[["Galaxy ID", "m-M", "err", "D (Mpc)", "Method"]].head(8))

# %% code 70.
print(f"거리 측정 방법: {df['Method'].nunique()}가지")
method_table = pd.DataFrame({
    "측정값 수": df["Method"].value_counts(),
    "적색편이가 있는 수": df.groupby("Method")["redshift (z)"].count(),
}).fillna(0).astype(int)

print("\n[측정값이 많은 방법 10개]")
display(method_table.sort_values("측정값 수", ascending=False).head(10))
print("[적색편이가 함께 적힌 방법 6개]")
display(method_table.sort_values("적색편이가 있는 수", ascending=False).head(6))

# %% code 71.
c = 299792.458  # 빛의 속력(km/s)

z = df["redshift (z)"]
df["v_approx"] = c * z                                     # 비상대론 근사 v = cz
df["v_rel"] = c * ((1 + z)**2 - 1) / ((1 + z)**2 + 1)      # 상대론적 도플러 관계

has_z = df.dropna(subset=["redshift (z)"])
print(f"적색편이가 있는 측정값: {len(has_z):,}개, z 범위 {z.min():.5f} ~ {z.max():.3f}")
display(has_z[["Galaxy ID", "redshift (z)", "v_approx", "v_rel", "D (Mpc)"]].head(5)
        .round({"v_approx": 1, "v_rel": 1}))

print(" z      cz (km/s)   상대론 (km/s)   차이")
for z0 in [0.01, 0.05, 0.1, 0.5, 1.0, 2.0]:
    v_a = c * z0
    v_r = c * ((1 + z0)**2 - 1) / ((1 + z0)**2 + 1)
    print(f"{z0:4.2f}  {v_a:10,.0f}  {v_r:12,.0f}   {100 * (v_a - v_r) / v_r:5.1f}%")

# %% code 72.
import matplotlib.pyplot as plt

def fit_through_origin(x, y):
    # 원점을 지나는 직선 y = slope * x를 최소제곱으로 맞춤
    # 돌려주는 값: 기울기, 기울기의 표준오차(통계 오차만), 원점 기준 R²
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    slope = np.sum(x * y) / np.sum(x**2)
    resid = y - slope * x
    se = np.sqrt(np.sum(resid**2) / (len(x) - 1) / np.sum(x**2))
    r2 = 1 - np.sum(resid**2) / np.sum(y**2)
    return slope, se, r2

d_all = df["D (Mpc)"]
v_all = df["v_approx"]
mask_pos = d_all.notna() & v_all.notna() & (d_all > 0) & (v_all > 0)
mask_local = mask_pos & (d_all < 100) & (v_all < 10000)
mask_out = mask_pos & ~mask_local

H0_local, se_local, r2_local = fit_through_origin(d_all[mask_local],
                                                  v_all[mask_local])
r_local = np.corrcoef(d_all[mask_local], v_all[mask_local])[0, 1]

fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.2))

ax = axes[0]
ax.scatter(d_all[mask_local], v_all[mask_local], s=10, alpha=0.4, facecolors="none",
           edgecolors="tab:blue", linewidths=0.4, label="간단한 범위의 표본")
x_line = np.linspace(0, 100, 100)
ax.plot(x_line, H0_local * x_line, color="tab:red", lw=2,
        label=f"맞춘 직선: $H_0$ = {H0_local:.1f} km/s/Mpc")
ax.set(xlim=(0, 105), ylim=(0, 10500), xlabel="거리 (Mpc)",
       ylabel="후퇴속도 $cz$ (km/s)", title="(a) 간단한 범위 필터")
ax.text(0.03, 0.97,
        f"$H_0$ = {H0_local:.1f} km/s/Mpc\nr = {r_local:.3f}\n$R^2$ = {r2_local:.3f}\nN = {mask_local.sum():,}",
        transform=ax.transAxes, va="top", fontsize=10,
        bbox=dict(boxstyle="round", fc="white", ec="0.3", alpha=0.9))
ax.legend(loc="lower right")
ax.grid(alpha=0.3)

ax = axes[1]
ax.scatter(d_all[mask_local], v_all[mask_local], s=6, alpha=0.3, color="tab:blue",
           edgecolors="none", label="범위 안")
ax.scatter(d_all[mask_out], v_all[mask_out], s=6, alpha=0.3, color="tab:orange",
           edgecolors="none", label="범위 밖")
ax.set(xscale="log", yscale="log", xlabel="거리 (Mpc)",
       ylabel="후퇴속도 $cz$ (km/s)",
       title="(b) 양수인 모든 행(로그-로그 축)")
ax.text(0.03, 0.97,
        f"양수인 행 = {mask_pos.sum():,}\n범위 밖 = {mask_out.sum():,}\n"
        f"최대 D = {d_all[mask_pos].max():,.0f} Mpc\n최대 v = {v_all[mask_pos].max():,.0f} km/s",
        transform=ax.transAxes, va="top", fontsize=10,
        bbox=dict(boxstyle="round", fc="white", ec="0.3", alpha=0.9))
ax.legend(loc="lower right")
ax.grid(alpha=0.3, which="both")

plt.tight_layout()
du.save_figure(fig, proj_dir / "hubble_first_look")
plt.show()

print(f"간단한 범위로 고른 표본: H0 = {H0_local:.1f} ± {se_local:.1f} km/s/Mpc (N = {mask_local.sum():,})")
print("\n속도가 가장 큰 측정값:")
display(df[mask_pos][["Galaxy ID", "D (Mpc)", "redshift (z)", "v_approx", "err", "Method"]]
        .sort_values("v_approx", ascending=False).head(8).round({"v_approx": 0}))

# %% code 73.
trusted_methods = ["SNIa", "SNIa SDSS", "SNII optical"]

sel = df.dropna(subset=["Galaxy ID", "D (Mpc)", "redshift (z)", "err",
                        "Method"]).copy()
sel["no_exclusion"] = sel.index.isna()          # 제외 코드가 비어 있으면 True

mask_reliable = (sel["no_exclusion"]
                 & (sel["err"] <= 0.30)
                 & sel["Method"].isin(trusted_methods))
mask_range = (sel["D (Mpc)"].between(5, 200)
              & sel["redshift (z)"].between(0.0017, 0.05))
rows = sel[mask_reliable & mask_range].copy()

# 한 은하의 여러 측정은 중앙값 하나로 묶기
gal = (rows.groupby("Galaxy ID")
           .agg(D=("D (Mpc)", "median"), z=("redshift (z)", "median"),
                v_approx=("v_approx", "median"), v_rel=("v_rel", "median"),
                err=("err", "median"), n_meas=("D (Mpc)", "size"))
           .reset_index())

print(f"전체 측정값                    : {len(df):,}")
print(f"거리·적색편이가 모두 있는 측정값: {len(sel):,}")
print(f"신뢰도·범위 기준을 통과한 측정값: {len(rows):,}")
print(f"최종 표본(은하 수)             : {len(gal):,}")
print("\n통과한 측정값의 방법별 수:")
print(rows["Method"].value_counts().to_string())

H0_fit, H0_se, r2_fit = fit_through_origin(gal["D"], gal["v_approx"])
r_fit = np.corrcoef(gal["D"], gal["v_approx"])[0, 1]
print(f"\n믿을 만한 표본의 허블 상수: H0 = {H0_fit:.1f} ± {H0_se:.1f} km/s/Mpc (통계 오차만)")

fig, ax = plt.subplots(figsize=(7.5, 4.4))
ax.scatter(d_all[mask_pos], v_all[mask_pos], s=6, alpha=0.08, color="lightsteelblue",
           edgecolors="none", label="양수인 모든 데이터")
ax.scatter(gal["D"], gal["v_approx"], s=14, alpha=0.65, color="tab:blue",
           edgecolors="none", label="믿을 만한 표본(은하당 점 하나)")
x_line = np.linspace(0, 210, 100)
ax.plot(x_line, H0_fit * x_line, color="crimson", lw=2,
        label=f"맞춘 직선: $H_0$ = {H0_fit:.1f} ± {H0_se:.1f} km/s/Mpc")
ax.set(xlim=(0, 210), ylim=(0, 16000), xlabel="거리 (Mpc)",
       ylabel="후퇴속도 $cz$ (km/s)", title="믿을 만한 표본의 허블 도표")
ax.text(0.97, 0.04, f"은하 N = {len(gal):,}개\nr = {r_fit:.3f}\n$R^2$ = {r2_fit:.3f}",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=10,
        bbox=dict(boxstyle="round", fc="white", alpha=0.85))
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
plt.tight_layout()
du.save_figure(fig, proj_dir / "hubble_reliable_sample")
plt.show()

display(gal.sort_values("n_meas", ascending=False).head(8)
        .round({"v_approx": 0, "v_rel": 0}))

# %% code 74.
rows["assumed_H0"] = rows["Hubble const."].round(0)
print("가정한 H0   은하 수   맞춘 기울기 (km/s/Mpc)")
for assumed, group in rows.dropna(subset=["assumed_H0"]).groupby("assumed_H0"):
    per_gal = group.groupby("Galaxy ID")[["D (Mpc)", "v_approx"]].median()
    if len(per_gal) < 30:
        continue
    slope, se, _ = fit_through_origin(per_gal["D (Mpc)"], per_gal["v_approx"])
    print(f"{assumed:8.0f}   {len(per_gal):6d}   {slope:6.1f} ± {se:.1f}")

# %% code 75.
fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.2), sharey=True)
results = {}
for ax, col, title in zip(axes, ["v_approx", "v_rel"],
                          ["(a) 비상대론 근사: $v = cz$",
                           "(b) 상대론적 도플러 관계"]):
    H0_i, se_i, r2_i = fit_through_origin(gal["D"], gal[col])
    r_i = np.corrcoef(gal["D"], gal[col])[0, 1]
    results[col] = (H0_i, se_i)
    ax.scatter(gal["D"], gal[col], s=14, alpha=0.6, color="tab:blue", edgecolors="none",
               label="믿을 만한 표본")
    ax.plot(x_line, H0_i * x_line, color="crimson", lw=2,
            label=f"맞춘 직선: $H_0$ = {H0_i:.1f} km/s/Mpc")
    ax.text(0.03, 0.97, f"$H_0$ = {H0_i:.1f} ± {se_i:.1f} km/s/Mpc\nr = {r_i:.3f}\n"
            f"$R^2$ = {r2_i:.3f}\nN = {len(gal):,}",
            transform=ax.transAxes, va="top", fontsize=10,
            bbox=dict(boxstyle="round", fc="white", ec="0.3", alpha=0.9))
    ax.set(xlim=(0, 210), ylim=(0, 16000), xlabel="거리 (Mpc)", title=title)
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)
axes[0].set_ylabel("후퇴속도 (km/s)")
plt.tight_layout()
du.save_figure(fig, proj_dir / "hubble_nonrel_vs_rel")
plt.show()

H0_a, H0_r = results["v_approx"][0], results["v_rel"][0]
print(f"비상대론 근사: {H0_a:.1f} km/s/Mpc, 상대론적 관계: {H0_r:.1f} km/s/Mpc, "
      f"차이 {100 * (H0_a - H0_r) / H0_r:.1f}%")

# %% code 76.
from astropy.cosmology import Planck18

print(f"이 장, 간단한 범위로 고른 표본 : {H0_local:6.2f} ± {se_local:.2f} km/s/Mpc")
print(f"이 장, 믿을 만한 표본(v = cz)  : {H0_fit:6.2f} ± {H0_se:.2f} km/s/Mpc")
print(f"astropy Planck18 모형          : {Planck18.H0.value:6.2f} km/s/Mpc")
print(f"SH0ES (Riess 외, 2022)         : {73.04:6.2f} ± 1.04 km/s/Mpc")
