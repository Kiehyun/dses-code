# 지구과학 데이터 사이언스 2 | III-03. 우주론
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 76.
import numpy as np
import pandas as pd
import astropy.units as u
from astropy.cosmology import Planck18

z_list = np.array([0, 0.5, 1, 2, 5, 10, 1100])
table = pd.DataFrame({
    "z": z_list,
    "척도인자 a": Planck18.scale_factor(z_list),
    "우주 나이 (Gyr)": Planck18.age(z_list).to(u.Gyr).value,
    "H(z) (km/s/Mpc)": Planck18.H(z_list).value,
})
display(table.round({"척도인자 a": 4, "우주 나이 (Gyr)": 4,
                     "H(z) (km/s/Mpc)": 1}))

# %% code 77.
import astropy.constants as const

H0 = Planck18.H0
rho_c = (3 * H0**2 / (8 * np.pi * const.G)).to(u.kg / u.m**3)
print(f"직접 계산한 임계 밀도 : {rho_c:.3e}")
print(f"astropy 값            : {Planck18.critical_density0.to(u.kg / u.m**3):.3e}")
print(f"양성자로 치면 1 m³마다 약 {(rho_c / const.m_p).to(u.m**-3).value:.1f}개")

# %% code 78.
from astropy.cosmology import LambdaCDM

curvature = pd.DataFrame([
    {"모형": "가속 팽창 평탄 우주", "Omega_m": 0.3, "Omega_Lambda": 0.7},
    {"모형": "물질만 있는 열린 우주", "Omega_m": 0.3, "Omega_Lambda": 0.0},
    {"모형": "물질만 있는 평탄 우주", "Omega_m": 1.0, "Omega_Lambda": 0.0},
    {"모형": "물질만 있는 닫힌 우주", "Omega_m": 6.0, "Omega_Lambda": 0.0},
])
curvature["Omega_k (식)"] = 1 - curvature["Omega_m"] - curvature["Omega_Lambda"]
curvature["Omega_k (astropy)"] = [
    LambdaCDM(H0=70, Om0=om, Ode0=ol).Ok0
    for om, ol in zip(curvature["Omega_m"], curvature["Omega_Lambda"])
]
curvature["곡률"] = curvature["Omega_k (식)"].map(
    lambda ok: "평탄" if abs(ok) < 1e-12 else ("열린" if ok > 0 else "닫힌"))
display(curvature)

# %% code 79.
import matplotlib.pyplot as plt
from astropy.cosmology import FlatLambdaCDM

Hubble_const = 67.8 * u.km / u.s / u.Mpc   # 허블 상수
Omega_m = 0.3                               # 물질 밀도 계수(보통 물질 + 암흑 물질)
Omega_Lambda = 0.7                          # 암흑 에너지 밀도 계수

cosmo_flat = FlatLambdaCDM(H0=Hubble_const, Om0=Omega_m, Tcmb0=2.725,
                           Neff=3.046)
cosmo_lambda = LambdaCDM(H0=Hubble_const, Om0=Omega_m, Ode0=Omega_Lambda,
                         Tcmb0=2.725, Neff=3.046)

z = 10**np.arange(3, -2, -0.01)             # z = 1000 ~ 0.01

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.1), sharey=True)
for ax, cosmo, title, label in [
        (axs[0], cosmo_flat, "FlatLambdaCDM", rf"$\Omega_m = {Omega_m}$"),
        (axs[1], cosmo_lambda, "LambdaCDM", rf"$\Omega_m = {Omega_m},~\Omega_\Lambda = {Omega_Lambda}$")]:
    ax.plot(cosmo.age(z), cosmo.scale_factor(z), label=label)
    ax.set(xlabel="우주의 나이 (Gyr)", title=title)
    ax.text(0.96, 0.04, f"$H_0$ = {Hubble_const.value} km/s/Mpc\n지금 나이 = {cosmo.age(0):.2f}",
            ha="right", va="bottom", fontsize=10, transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.5", fc="wheat", alpha=0.5))
    ax.grid(True)
    ax.legend(loc="upper left")
axs[0].set_ylabel("척도인자 $a$")
plt.tight_layout()
du.save_figure(fig, proj_dir / "flat_vs_lambdacdm")
plt.show()
print(f"FlatLambdaCDM의 Ode0 = {cosmo_flat.Ode0:.5f}, LambdaCDM의 Ok0 = {cosmo_lambda.Ok0:.5f}")

# %% code 80.
from astropy.cosmology import WMAP9

for name, cosmo in [("WMAP9", WMAP9), ("Planck18", Planck18)]:
    hubble_len = cosmo.hubble_distance
    print(f"[{name}]")
    print(f"  허블 상수 H0      : {cosmo.H0:.2f}")
    print(f"  우주의 나이       : {cosmo.age(0):.3f}")
    print(f"  허블 시간 1/H0    : {cosmo.hubble_time.to(u.Gyr):.3f}")
    print(f"  허블 길이 c/H0    : {hubble_len:.1f} = {hubble_len.to(u.lyr).value / 1e9:.2f} Gly")

# %% code 81.
cosmo = LambdaCDM(H0=Hubble_const, Om0=Omega_m, Ode0=Omega_Lambda,
                  Tcmb0=2.725, Neff=3.046)
age = cosmo.age(z)
scale = cosmo.scale_factor(z)

t_hubble = cosmo.hubble_time.to(u.Gyr)      # 허블 시간 = 등속 팽창 우주의 나이
age_now = cosmo.age(0).to(u.Gyr)            # ΛCDM 우주의 나이

t_const = np.linspace(0, t_hubble.value, 100)
a_const = t_const / t_hubble.value          # 등속 팽창: a = t / t_H

fig, ax = plt.subplots(figsize=(7.5, 4.4))
ax.plot(t_const, a_const, label="등속 팽창(텅 빈) 우주: $a = t/t_H$")
ax.plot(age, scale,
        label=rf"$\Lambda$CDM ($\Omega_m = {Omega_m},~\Omega_\Lambda = {Omega_Lambda}$)")
ax.axvline(t_hubble.value, color="r", ls="--",
           label=f"허블 시간 ({t_hubble:.2f})")
ax.axvline(age_now.value, color="g", ls="--",
           label=f"우주의 나이 ({age_now:.2f})")
ax.set(xlabel="빅뱅 뒤로 흐른 시간 (Gyr)", ylabel="척도인자 $a$",
       title="시간에 따른 척도인자", xlim=(0, t_hubble.value * 1.2), ylim=(0, 1.1))
ax.grid(True)
ax.legend(loc="upper left")
plt.tight_layout()
du.save_figure(fig, proj_dir / "hubble_time_vs_age")
plt.show()
print(f"허블 시간 {t_hubble:.2f}, ΛCDM 우주의 나이 {age_now:.2f}, 차이 {t_hubble - age_now:.2f}")

# %% code 82.
fig, ax = plt.subplots(figsize=(7.5, 4.4))
ax.plot(t_const - t_hubble.value, a_const, label="등속 팽창(텅 빈) 우주")
ax.plot((age - age_now).value, scale,
        label=rf"$\Lambda$CDM ($\Omega_m = {Omega_m},~\Omega_\Lambda = {Omega_Lambda}$)")
ax.axvline(-t_hubble.value, color="tab:blue", ls="--")
ax.text(-t_hubble.value - 0.2, 0.45, "허블 시간", rotation=90, va="bottom", ha="right",
        color="tab:blue")
ax.axvline(-age_now.value, color="tab:orange", ls="--")
ax.text(-age_now.value + 0.2, 0.45, "우주의 나이", rotation=90, ha="left",
        va="bottom", color="tab:orange")
ax.axvline(0, color="g", ls="--")
ax.text(-0.2, 0.2, "현재", rotation=90, va="bottom", ha="right", color="g")
ax.set(xlabel=r"현재로부터의 시간 (Gyr)  (과거 $\leftarrow$ 0)", ylabel="척도인자 $a$",
       title="현재를 0으로 둔 척도인자", xlim=(-t_hubble.value - 1.5, 1), ylim=(0, 1.1))
ax.grid(True)
ax.legend(loc="upper left")
plt.tight_layout()
du.save_figure(fig, proj_dir / "hubble_time_vs_age_centered")
plt.show()

# %% code 83.
z_t = np.concatenate([np.logspace(4, -3, 400), -np.linspace(0.001, 0.09, 40)])  # 과거 → 미래
t_now = cosmo.age(0).to(u.Gyr).value
t = cosmo.age(z_t).to(u.Gyr).value - t_now                       # 현재로부터의 시간

D_horizon = ((cosmo.comoving_distance(1e5) - cosmo.comoving_distance(z_t)) / (1 + z_t)).to(u.Gpc)
D_hubble = (const.c / cosmo.H(z_t)).to(u.Gpc)                    # 그 시각의 허블 길이
D_coast = (const.c * (t + t_now) * u.Gyr).to(u.Gpc)              # 등속 팽창 우주의 c·t

fig, ax = plt.subplots(figsize=(7.5, 4.5))
ax.plot(t, D_horizon, color="tab:green",
        label=r"우주의 지평선 ($\Lambda$CDM, 고유 거리)")
ax.plot(t, D_hubble, color="tab:blue",
        label=r"허블 길이 $c/H(t)$ ($\Lambda$CDM)")
ax.plot(t, D_coast, "--", color="tab:gray", label=r"등속 팽창 우주: $c\,t$")
ax.axvline(0, color="k", ls=":")
ax.set(xlabel="현재로부터의 시간 (Gyr)", ylabel="거리 (Gpc)",
       title="허블 길이와 관측 가능한 우주의 크기")
ax.grid(True, alpha=0.5)
ax.legend(loc="upper left")
plt.tight_layout()
du.save_figure(fig, proj_dir / "horizon_and_hubble_length")
plt.show()

gly = lambda d: d.to(u.lyr).value / 1e9
D_h0 = (const.c / cosmo.H0).to(u.Gpc)
D_p0 = cosmo.comoving_distance(1e5).to(u.Gpc)
print(f"지금의 허블 길이      : {D_h0:.2f} = {gly(D_h0):.1f} Gly")
print(f"지금의 우주의 지평선  : {D_p0:.2f} = {gly(D_p0):.1f} Gly")
print(f"빛의 속력 × 우주 나이 : {gly(const.c * cosmo.age(0)):.1f} Gly")

# %% code 84.
H0_values = [67.4, 73.0] * u.km / u.s / u.Mpc

fig, axs = plt.subplots(1, 2, figsize=(7.5, 2.8), sharey=True)
for H0_i in H0_values:
    cosmo_i = LambdaCDM(H0=H0_i, Om0=Omega_m, Ode0=Omega_Lambda, Tcmb0=2.725,
                        Neff=3.046)
    age_i = cosmo_i.age(z)
    a_i = cosmo_i.scale_factor(z)
    label = f"$H_0$ = {H0_i.value} km/s/Mpc"
    axs[0].plot(age_i, a_i, label=label)
    axs[1].plot(age_i - cosmo_i.age(0), a_i, label=label)
    print(f"H0 = {H0_i.value}: 허블 시간 {cosmo_i.hubble_time.to(u.Gyr):.2f}, 우주의 나이 {cosmo_i.age(0):.2f}")

axs[0].set(xlabel="빅뱅 뒤로 흐른 시간 (Gyr)", ylabel="척도인자 $a$",
           title="빅뱅부터 잰 시간")
axs[1].set(xlabel="현재로부터의 시간 (Gyr)", title="현재를 0으로 둔 시간")
for ax in axs:
    ax.grid(True)
    ax.legend(loc="upper left")
plt.tight_layout()
du.save_figure(fig, proj_dir / "hubble_tension_scale_factor")
plt.show()

# %% code 85.
fname = "SCPUnion2.1_mu_vs_z.txt"
sn_path = du.download("https://supernova.lbl.gov/union/figures/" + fname,
                      proj_dir / fname)

with open(sn_path, encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i >= 7:
            break
        print(line.rstrip())

sn = pd.read_csv(sn_path, sep="\t", comment="#", header=None,
                 names=["name", "z", "mu", "mu_err", "p_lowmass"])
print(f"\n초신성 {len(sn)}개, 적색편이 {sn['z'].min():.3f} ~ {sn['z'].max():.3f}, "
      f"거리지수 {sn['mu'].min():.2f} ~ {sn['mu'].max():.2f}")
display(sn.head())

# %% code 86.
checks = {
    "값이 모두 있음": sn[["name", "z", "mu", "mu_err"]].notna().all(axis=1),
    "물리적으로 가능한 값": (sn["z"] > 0) & (sn["mu"] > 0) & (sn["mu_err"] > 0),
    "0.01 <= z <= 1.4": sn["z"].between(0.01, 1.4),
    "오차 <= 0.40등급": sn["mu_err"] <= 0.40,
    "이름이 겹치지 않음": ~sn["name"].duplicated(keep=False),
}
summary = pd.DataFrame({"통과": [int(m.sum()) for m in checks.values()],
                        "걸림": [int((~m).sum()) for m in checks.values()]},
                       index=list(checks.keys()))
display(summary)

ok = np.logical_and.reduce(list(checks.values()))
sn_ok = sn[ok].copy()
print(f"점검 전 {len(sn)}개 → 점검 후 {len(sn_ok)}개 ({len(sn_ok) / len(sn):.1%})")
print(f"점검 후 평균 거리지수 오차: {sn_ok['mu_err'].mean():.3f}등급")

# %% code 87.
import matplotlib.ticker as mticker

H0_union = 70 * u.km / u.s / u.Mpc
models = [
    {"label": "가속 팽창 평탄 우주", "Om0": 0.3, "Ode0": 0.7, "ls": "-",
     "color": "tab:blue"},
    {"label": "물질만 있는 열린 우주", "Om0": 0.3, "Ode0": 0.0,
     "ls": "--", "color": "tab:orange"},
    {"label": "물질만 있는 평탄 우주", "Om0": 1.0, "Ode0": 0.0, "ls": ":",
     "color": "tab:green"},
]
ref = LambdaCDM(H0=H0_union, Om0=0.3, Ode0=0.0, Tcmb0=2.725, Neff=3.046)   # 잔차의 기준: 물질만 있는 열린 우주

def plot_sn_models(data, xscale="linear", fig_name=None):
    z_grid = np.geomspace(0.01, 1.45, 200)
    resid = data["mu"].to_numpy() - ref.distmod(data["z"].to_numpy()).value

    fig, axs = plt.subplots(2, 1, figsize=(7.5, 6.4), sharex=True,
                            gridspec_kw={"height_ratios": [2, 1]})
    axs[0].errorbar(data["z"], data["mu"], yerr=data["mu_err"], fmt="o", ms=2, color="0.25",
                    ecolor="0.75", capsize=0, alpha=0.6, label="Union2.1 Ia형 초신성")
    axs[1].errorbar(data["z"], resid, yerr=data["mu_err"], fmt="o", ms=2, color="0.25",
                    ecolor="0.75", capsize=0, alpha=0.6, label="Union2.1 Ia형 초신성")
    for m in models:
        cosmo_m = LambdaCDM(H0=H0_union, Om0=m["Om0"], Ode0=m["Ode0"],
                            Tcmb0=2.725, Neff=3.046)
        mu_m = cosmo_m.distmod(z_grid).value
        label = rf'{m["label"]} ($\Omega_m={m["Om0"]},~\Omega_\Lambda={m["Ode0"]}$)'
        axs[0].plot(z_grid, mu_m, ls=m["ls"], color=m["color"], lw=1.8,
                    label=label)
        axs[1].plot(z_grid, mu_m - ref.distmod(z_grid).value, ls=m["ls"],
                    color=m["color"], lw=1.8)

    # 적색편이 구간별 잔차의 가중 평균(가중치 = 1/오차²)
    edges = np.geomspace(0.01, 1.4, 9) if xscale == "log" else np.linspace(0.01,
                                                                           1.4,
                                                                           9)
    idx = np.digitize(data["z"], edges)
    w = 1 / data["mu_err"].to_numpy()**2
    zc, rc, ec = [], [], []
    for k in range(1, len(edges)):
        s = idx == k
        if s.sum() >= 5:
            zc.append(np.average(data["z"][s], weights=w[s]))
            rc.append(np.average(resid[s], weights=w[s]))
            ec.append(1 / np.sqrt(w[s].sum()))
    axs[1].errorbar(zc, rc, yerr=ec, fmt="s", color="crimson", ms=6, capsize=3,
                    label="구간 가중 평균", zorder=5)

    axs[0].set(ylabel="거리지수 $\\mu = m - M$",
               title="Ia형 초신성과 세 팽창 모형")
    axs[1].set(xlabel="적색편이 $z$",
               ylabel=r"$\Delta\mu$ (물질만 있는 열린 우주 기준)", ylim=(-1.0, 1.0))
    axs[1].axhline(0, color="k", lw=0.8)
    for ax in axs:
        ax.set_xscale(xscale)
        if xscale == "log":   # 눈금을 0.01, 0.1, 1처럼 소수로 표기(지수 표기의 빼기 기호 글꼴 문제 방지)
            ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,
                                                               _: f"{x:g}"))
            ax.xaxis.set_minor_formatter(mticker.NullFormatter())
        ax.grid(True, alpha=0.4)
        ax.legend(loc="upper left" if ax is axs[0] else "lower left",
                  fontsize=9)
    plt.tight_layout()
    if fig_name:
        du.save_figure(fig, proj_dir / fig_name)
    plt.show()
    return pd.DataFrame({"z": zc, "평균 잔차": rc, "오차": ec})

binned = plot_sn_models(sn_ok, xscale="linear", fig_name="sn_models_linear")
display(binned.round(3))

# %% code 88.
binned_log = plot_sn_models(sn_ok, xscale="log", fig_name="sn_models_log")
display(binned_log.round(3))

# %% code 89.
import warnings

scale_models = [
    ("물질만 있는 닫힌 우주", 6.0, 0.0),
    ("물질만 있는 평탄 우주", 1.0, 0.0),
    ("물질만 있는 열린 우주", 0.3, 0.0),
    ("텅 빈 우주(등속 팽창)", 0.0, 0.0),
    ("가속 팽창 평탄 우주",   0.3, 0.7),
]
line_styles = ["-", "--", "-.", ":", (0, (3, 1, 1, 1))]
a_grid = np.linspace(0.01, 4, 600)
z_grid = 1 / a_grid - 1

rows = []
fig, ax = plt.subplots(figsize=(7.5, 3.8))
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    for (label, om, ol), ls in zip(scale_models, line_styles):
        cosmo_m = LambdaCDM(H0=Hubble_const, Om0=om, Ode0=ol, Tcmb0=2.725,
                            Neff=3.046)
        t_m = cosmo_m.age(z_grid).to(u.Gyr).value
        age_m = cosmo_m.age(0).to(u.Gyr).value
        ax.plot(t_m - age_m, a_grid, ls=ls, lw=1.8,
                label=rf"{label} ($\Omega_m = {om},~\Omega_\Lambda = {ol}$)")
        rows.append({"모형": label, "Omega_m": om, "Omega_Lambda": ol,
                     "Omega_k": round(1 - om - ol, 3), "나이 (Gyr)": round(age_m, 2)})

ax.axvline(0, color="tab:red", ls="--")
ax.text(1, 0.15, "현재", color="tab:red", fontsize=12)
ax.set(xlabel="현재로부터의 시간 (Gyr)", ylabel="척도인자 $a$",
       title="여러 우주 모형의 척도인자 시간 변화", xlim=(-18, 50), ylim=(0, 4))
ax.grid(True)
ax.legend(loc="upper left")
plt.tight_layout()
du.save_figure(fig, proj_dir / "scale_factor_models")
plt.show()
display(pd.DataFrame(rows))
