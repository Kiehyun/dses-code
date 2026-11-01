# 지구과학 데이터 사이언스 2 | IV-06. 기후변화의 원인 가르기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 479.
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

# 화산 에어로졸(GloSSAC) 파일 주소는 길어서 따로 적음
GLOSSAC_URL = (
    "https://data.giss.nasa.gov/modelforce/strataer/data/tau_reff_GloSSAC.v2.24.nc")
URLS = {
    "gistemp.csv": "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv",
    "co2_mm_mlo.csv": "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.csv",
    "nina34.anom.data": "https://psl.noaa.gov/data/correlation/nina34.anom.data",
    "glossac.nc": GLOSSAC_URL,
    "sunspot.csv": "https://www.sidc.be/SILSO/INFO/snmtotcsv.php",
}
F = {name: Path(proj_dir) / name for name in URLS}
for name, url in URLS.items():
    if not F[name].exists():
        du.download(url, F[name])
print("내려받기 끝:", ", ".join(URLS))

# %% code 480.
# 1) 기온 편차
g = pd.read_csv(F["gistemp.csv"], skiprows=1, na_values="***")
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
          "Oct", "Nov", "Dec"]
g = g.melt(id_vars="Year", value_vars=months, var_name="m", value_name="temp")
month_no = (g["m"].map(months.index) + 1).astype(str)          # "Jan" → "1"
g["date"] = pd.to_datetime(g["Year"].astype(str) + "-" + month_no + "-01")
temp = g.set_index("date")["temp"].sort_index().astype(float)

# 2) CO2 (계절 변동 제거값)
c = pd.read_csv(F["co2_mm_mlo.csv"], comment="#")
c["date"] = pd.to_datetime(dict(year=c["year"], month=c["month"], day=1))
co2 = c.set_index("date")["deseasonalized"]

# 3) ENSO 지수(니뇨 3.4 편차)
rows = []
for line in open(F["nina34.anom.data"]):
    p = line.split()
    if len(p) == 13 and p[0].isdigit():
        for m, v in enumerate(p[1:], start=1):
            rows.append((pd.Timestamp(int(p[0]), m, 1), float(v)))
enso = pd.Series(dict(rows)).replace(-99.99, np.nan)

# 4) 화산 에어로졸 — 위도 가중 전 지구 평균
ds = xr.open_dataset(F["glossac.nc"], decode_times=False)
wgt = np.cos(np.deg2rad(ds["lat"]))
tau = (ds["tau"] * wgt).sum("lat") / wgt.sum()
tau_dates = pd.to_datetime("1850-01-01") + pd.to_timedelta(ds["month"].values,
                                                           unit="D")
volc = pd.Series(tau.values, index=tau_dates.to_period("M").to_timestamp())

# 5) 흑점 수
s = pd.read_csv(F["sunspot.csv"], sep=";", header=None)
s["date"] = pd.to_datetime(dict(year=s[0], month=s[1], day=1))
sun = s.set_index("date")[3].replace(-1, np.nan)

for name, x in [("기온", temp), ("CO2", co2), ("ENSO", enso), ("화산", volc),
                ("흑점", sun)]:
    x = x.dropna()
    print(f"{name:5s} {x.index[0]:%Y-%m} ~ {x.index[-1]:%Y-%m}  ({len(x):,}개월)")

# %% code 481.
df = pd.concat({"temp": temp, "co2": co2, "enso": enso, "volc": volc, "sun": sun},
               axis=1)
df = df.loc["1979-01-01":].dropna()
df["co2_forcing"] = 5.35 * np.log(df["co2"] / 278.0)
print(f"분석 기간: {df.index[0]:%Y-%m} ~ {df.index[-1]:%Y-%m} ({len(df)}개월)")

panels = [("temp", "기온 편차 (°C)", "crimson"), ("co2", "CO₂ (ppm)", "black"),
          ("enso", "니뇨 3.4 편차 (°C)", "teal"), ("volc",
                                                  "화산 에어로졸\n광학 두께",
                                                  "saddlebrown"),
          ("sun", "흑점 수", "orange")]
fig, axes = plt.subplots(5, 1, figsize=(7.5, 5.8), sharex=True)
for ax, (col, label, color) in zip(axes, panels):
    ax.plot(df.index, df[col], color=color, lw=1)
    ax.set_ylabel(label)
    ax.grid(alpha=0.3)
axes[3].set_ylim(top=df["volc"].max() * 1.3)
for year, name in [(1982, "엘치촌"), (1991, "피나투보")]:
    axes[3].annotate(name,
                     (pd.Timestamp(year, 6, 1), df["volc"].loc[str(year + 1)].max()),
                     fontsize=9)
axes[0].set_title("기온과 네 가지 요인 (1979~)")
plt.tight_layout()
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_01"))
plt.show()

# %% code 482.
def design(lags):
    l1, l2, l3 = lags
    X = pd.DataFrame({
        "상수": 1.0,
        "CO2": df["co2_forcing"],
        "ENSO": enso.shift(l1).reindex(df.index),
        "화산": volc.shift(l2).reindex(df.index),
        "태양": sun.shift(l3).reindex(df.index),
    })
    ok = X.notna().all(axis=1) & df["temp"].notna()
    return X[ok], df["temp"][ok]


def fit(lags):
    X, y = design(lags)
    coef, *_ = np.linalg.lstsq(X.values, y.values, rcond=None)
    resid = y.values - X.values @ coef
    return coef, X, y, (resid ** 2).mean()


best = min(((l1, l2, l3) for l1 in range(7) for l2 in range(13) for l3 in range(4)),
           key=lambda lags: fit(lags)[3])
coef, X, y, mse = fit(best)
yhat = X.values @ coef
r2 = 1 - ((y - yhat) ** 2).sum() / ((y - y.mean()) ** 2).sum()

# 계수의 표준오차 (보통 최소제곱 공식)
resid = y.values - yhat
n, k = X.shape
s2 = (resid ** 2).sum() / (n - k)
se = np.sqrt(np.diag(s2 * np.linalg.inv(X.values.T @ X.values)))

# 잔차의 자기상관(r1)을 고려해 표준오차를 키운 값 (유효 표본 수 보정)
r1 = np.corrcoef(resid[:-1], resid[1:])[0, 1]
se_adj = se * np.sqrt((1 + r1) / (1 - r1))

print(f"가장 잘 맞는 지연: ENSO {best[0]}개월, 화산 {best[1]}개월, 태양 {best[2]}개월")
print(f"결정계수 R² = {r2:.3f},  잔차의 이웃 달 상관 r1 = {r1:.2f}")
print("           계수     표준오차   보정 표준오차")
for name, b, e1, e2 in zip(X.columns, coef, se, se_adj):
    print(f"  {name:4s} {b:+9.4f}   {e1:8.4f}   {e2:8.4f}")
print(f"CO2 계수 × 3.7 = {coef[1] * 3.7:.2f} ± {2 * se_adj[1] * 3.7:.2f} °C "
      "(보정 표준오차 2배 범위)")

# %% code 483.
contrib = pd.DataFrame({name: X[name] * b for name,
                        b in zip(X.columns, coef) if name != "상수"})
contrib = contrib - contrib.mean()
colors = {"CO2": "black", "ENSO": "teal", "화산": "saddlebrown",
          "태양": "orange"}

fig, ax = plt.subplots(2, 1, figsize=(7.5, 5.0), sharex=True)
ax[0].plot(y.index, y, color="lightcoral", lw=1, label="관측")
ax[0].plot(y.index, yhat, color="k", lw=1.2, label=f"모형 (R² = {r2:.2f})")
ax[0].set_ylabel("기온 편차 (°C)")
ax[0].legend()
for name in contrib:
    ax[1].plot(contrib.index, contrib[name], color=colors[name], lw=1.2,
               label=name)
ax[1].set_ylabel("요인별 기여 (°C)")
ax[1].legend(ncol=4)
for a in ax:
    a.grid(alpha=0.3)
ax[0].set_title("관측 기온과 회귀 모형, 요인별 기여")
plt.tight_layout()
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_02"))
plt.show()

# %% code 484.
years = (y.index.year + (y.index.month - 0.5) / 12).values
trend = {"관측 기온": np.polyfit(years, y.values, 1)[0] * 10}
for name in contrib:
    trend[name] = np.polyfit(years, contrib[name].values, 1)[0] * 10
trend = pd.Series(trend)

fig, ax = plt.subplots(figsize=(8.3, 3.6))
bar_colors = ["crimson"] + [colors[n] for n in contrib]
ax.bar(trend.index, trend.values, color=bar_colors)
for i, v in enumerate(trend.values):
    ax.text(i, v + (0.004 if v >= 0 else -0.004), f"{v:+.3f}", ha="center",
            va="bottom" if v >= 0 else "top", fontsize=10)
ax.set_ylim(min(trend.min() * 2.5, -0.03), trend.max() * 1.15)
ax.axhline(0, color="k", lw=0.8)
ax.set_ylabel("추세 (°C/10년)")
ax.set_title(f"{y.index[0]:%Y}~{y.index[-1]:%Y}년 기온 추세와 요인별 기여")
ax.grid(axis="y", alpha=0.3)
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_03"))
plt.show()
print(trend.round(3))

# %% code 485.
# CO2 강제력 대신 시간(연도)을 넣은 모형 — 지연은 앞에서 고른 best 그대로
X_t, y_t = design(best)
X_t = X_t.rename(columns={"CO2": "시간"})
X_t["시간"] = X_t.index.year + (X_t.index.month - 0.5) / 12   # 소수 연도
coef_t, *_ = np.linalg.lstsq(X_t.values, y_t.values, rcond=None)
yhat_t = X_t.values @ coef_t
r2_t = 1 - ((y_t - yhat_t) ** 2).sum() / ((y_t - y_t.mean()) ** 2).sum()

r_ct = np.corrcoef(X["CO2"], X_t["시간"])[0, 1]          # CO2 강제력과 시간의 상관
r_pred = np.corrcoef(yhat, yhat_t)[0, 1]                   # 두 모형 예측값의 상관

print(f"CO2 강제력과 시간의 상관 r = {r_ct:.4f}")
print(f"CO2 모형  R² = {r2:.3f}   CO2 항의 추세 기여 {trend['CO2']:+.3f} °C/10년")
print(f"시간 모형 R² = {r2_t:.3f}   시간 계수          {coef_t[1] * 10:+.3f} °C/10년")
print(f"두 모형 예측값의 상관 r = {r_pred:.4f}")

# %% code 486.
sun_trend = np.polyfit(years, X["태양"].values, 1)[0] * 10
co2_change = df["co2"].iloc[-12:].mean() - df["co2"].iloc[:12].mean()
peak_enso = df["enso"].idxmax()
cards = pd.DataFrame([
    ("E1", "관측 기온 추세", f"{trend['관측 기온']:+.3f} °C/10년"),
    ("E2", "CO₂ 항의 추세 기여", f"{trend['CO2']:+.3f} °C/10년"),
    ("E3", "태양 항의 추세 기여", f"{trend['태양']:+.3f} °C/10년"),
    ("E4", "흑점 수 자체의 추세", f"{sun_trend:+.1f} 개/10년"),
    ("E5", "ENSO 항의 추세 기여", f"{trend['ENSO']:+.3f} °C/10년"),
    ("E6", "가장 강한 엘니뇨 시기",
     f"{peak_enso:%Y년 %m월} (니뇨 3.4 {df['enso'].max():+.1f} °C)"),
    ("E7", "화산 항의 추세 기여", f"{trend['화산']:+.3f} °C/10년"),
    ("E8", "CO₂ 농도 증가(첫 해 → 마지막 해)", f"{co2_change:+.0f} ppm"),
    ("E9", "모형의 설명력", f"R² = {r2:.2f}"),
], columns=["번호", "증거", "값"])
cards

# %% code 487.
pre = temp.loc["1880":"1900"].mean()   # 산업화 이전 기준(GISTEMP는 1880년부터)
offset = -pre                          # 1951~1980년 기준 → 산업화 이전 기준
base = (coef[0] + coef[2] * df["enso"].mean()
        + coef[3] * volc.loc["1979":].mean() + coef[4] * sun.loc["1979":].mean())

last_year = df.index[-1].year
c_now = df["co2"].iloc[-12:].mean()
fy = np.arange(last_year, 2061)


def scenario(stop_year):
    if stop_year is None:                   # 지금처럼: 해마다 2.5 ppm
        rate = np.full(len(fy), 2.5)
    else:                                   # stop_year까지 증가 폭을 0으로 줄임
        rate = 2.5 * np.clip((stop_year - fy) / (stop_year - last_year), 0, 1)
    return c_now + np.concatenate([[0], np.cumsum(rate[1:])])


scen = {"지금처럼": scenario(None),
        "점진 안정(2050)": scenario(2050),
        "빠른 안정(2040)": scenario(2040)}

fig, ax = plt.subplots(1, 2, figsize=(7.5, 2.9))
t_ok = temp.dropna()
full = t_ok.groupby(t_ok.index.year).count() == 12   # 열두 달이 다 있는 해만
annual = (temp.groupby(temp.index.year).mean() + offset)[full].loc[1950:]
annual.index = pd.to_datetime(annual.index.astype(str))
ax[1].plot(annual.index.year, annual.values, color="gray",
           label="관측(연평균)")
for (name, cc), color in zip(scen.items(),
                             ["crimson", "darkorange", "seagreen"]):
    ax[0].plot(fy, cc, color=color, label=name)
    t_proj = base + coef[1] * 5.35 * np.log(cc / 278.0) + offset
    ax[1].plot(fy, t_proj, color=color, lw=2,
               label=f"{name}: 2060년 {t_proj[-1]:.2f} °C")
for lv in (1.5, 2.0):
    ax[1].axhline(lv, color="k", ls=":", lw=1)
    ax[1].text(1951, lv + 0.03, f"{lv} °C", fontsize=9)
ax[0].set_ylabel("CO₂ (ppm)")
ax[0].set_title("CO₂ 농도 시나리오")
ax[1].set_ylabel("산업화 이전 대비 기온 (°C)")
ax[1].set_title("단순 모형으로 어림한 전 지구 기온")
ax[1].set_ylim(bottom=-0.7)                    # 아래쪽 범례 자리
for a in ax:
    a.grid(alpha=0.3)
    a.legend(fontsize=8, loc="lower right" if a is ax[1] else "best")
plt.tight_layout()
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_04"))
plt.show()
