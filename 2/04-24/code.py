# 지구과학 데이터 사이언스 2 | IV-04. 태풍의 진로와 세기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅳ-69.
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

URL = "https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/Besttracks/bst_all.zip"
zip_file = Path(proj_dir) / "bst_all.zip"
txt_file = Path(proj_dir) / "bst_all.txt"
if not txt_file.exists():
    du.download(URL, zip_file)
    with zipfile.ZipFile(zip_file) as z:
        z.extract("bst_all.txt", proj_dir)
du.preview_text(txt_file, n=6)

# %% code Ⅳ-70.
rows = []
for line in open(txt_file, encoding="ascii", errors="ignore"):
    if line.startswith("66666"):
        intl = line[6:10].strip()          # 국제 번호(yynn), 열대 폭풍이 되지 못한 것은 0000
        name = line[30:50].strip()
        sid = f"{intl}_{name}" if intl != "0000" else None
        continue
    if sid is None:
        continue
    yy = int(line[0:2])
    year = 1900 + yy if yy >= 51 else 2000 + yy
    time = pd.Timestamp(year=year, month=int(line[2:4]), day=int(line[4:6]),
                        hour=int(line[6:8]))
    wind = line[33:36].strip()
    rows.append({
        "sid": sid, "name": name, "time": time,
        "grade": int(line[13]),
        "lat": int(line[15:18]) / 10, "lon": int(line[19:23]) / 10,
        "pres": int(line[24:28]),
        "wind_kt": int(wind) if wind and int(wind) > 0 else np.nan,
    })

bt = pd.DataFrame(rows)
bt["wind_ms"] = bt["wind_kt"] * 0.514          # kt → m/s
bt["year"] = bt["time"].dt.year
print(f"관측 기록 {len(bt):,}줄, 태풍 {bt['sid'].nunique():,}개 ({bt['year'].min()}~{bt['year'].max()})")
bt.head()

# %% code Ⅳ-71.
this_year = pd.Timestamp.now().year
count = bt.groupby("year")["sid"].nunique()
count = count[count.index < this_year]

fig, ax = plt.subplots(figsize=(8.4, 3.0))
ax.bar(count.index, count.values, color="lightsteelblue",
       label="해마다 발생 수")
ax.plot(count.index, count.rolling(10, center=True).mean(), color="navy",
        lw=2, label="10년 이동평균")
ax.axhline(count.mean(), color="gray", ls="--", lw=1)
ax.set_xlabel("연도")
ax.set_ylabel("태풍 수 (개)")
ax.set_title(f"북서태평양 태풍 발생 수 (평균 {count.mean():.1f}개/년)")
ax.legend()
ax.grid(axis="y", alpha=0.3)
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_01"))
plt.show()

# %% code Ⅳ-72.
ts = bt[bt["grade"].isin([3, 4, 5, 9])]
genesis = ts.sort_values("time").groupby("sid").first()

fig = plt.figure(figsize=(7.5, 2.9))
ax = fig.add_subplot(1, 2, 1,
                     projection=ccrs.PlateCarree(central_longitude=150))
ax.set_extent([100, 190, -5, 45], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND, facecolor="lightgray")
ax.coastlines(linewidth=0.5)
sc = ax.scatter(genesis["lon"], genesis["lat"], c=genesis["time"].dt.month, cmap="twilight", vmin=1, vmax=12,
                s=6, transform=ccrs.PlateCarree())
plt.colorbar(sc, ax=ax, shrink=0.8, label="발생한 달")
gl = ax.gridlines(draw_labels=True, linewidth=0.3)
gl.top_labels = gl.right_labels = False
ax.set_title("태풍 발생 위치 (1951~)")

ax2 = fig.add_subplot(1, 2, 2)
ax2.hist(genesis["lat"], bins=np.arange(0, 41, 2), orientation="horizontal",
         color="teal")
ax2.set_ylabel("발생 위도 (°N)")
ax2.set_xlabel("태풍 수")
ax2.set_title("발생 위도 분포")
ax2.grid(alpha=0.3)
plt.tight_layout()
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_02"))
plt.show()

print(f"위도 5° 미만에서 발생한 태풍: {(genesis['lat'] < 5).mean() * 100:.1f}%")

# %% code Ⅳ-73.
recent = bt[bt["year"] >= 2000]
gen_month = genesis["time"].dt.month

fig, axes = plt.subplots(1, 4, figsize=(7.5, 2.3),
                         subplot_kw={"projection": ccrs.PlateCarree()})
for ax, month in zip(axes, [7, 8, 9, 10]):
    ax.set_extent([105, 160, 5, 50], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, facecolor="lightgray")
    ax.coastlines(linewidth=0.4)
    sids = gen_month[gen_month == month].index
    for sid, g in recent[recent["sid"].isin(sids)].groupby("sid"):
        ax.plot(g["lon"], g["lat"], lw=0.6, alpha=0.5, color="crimson",
                transform=ccrs.PlateCarree())
    ax.plot(127.0, 37.5, "k*", ms=10, transform=ccrs.PlateCarree())   # 서울
    ax.set_title(f"{month}월에 발생한 태풍\n({len(set(sids) & set(recent['sid']))}개)", fontsize=10)
plt.tight_layout()
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_03"))
plt.show()

# %% code Ⅳ-74.
GRADE = {2: "열대 저압부", 3: "열대 폭풍", 4: "강한 열대 폭풍", 5: "태풍(TY)",
         6: "온대 저기압"}
h = bt[bt["sid"] == "2211_HINNAMNOR"].copy()
h["kst"] = h["time"] + pd.Timedelta("9h")

fig = plt.figure(figsize=(6.0, 4.8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([118, 156, 15, 50], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND, facecolor="lightgray")
ax.coastlines(linewidth=0.5)
ax.plot(h["lon"], h["lat"], color="k", lw=0.8, transform=ccrs.PlateCarree())
sc = ax.scatter(h["lon"], h["lat"], c=h["pres"], cmap="magma", s=25, zorder=3,
                transform=ccrs.PlateCarree())
cb = plt.colorbar(sc, ax=ax, shrink=0.8)
cb.set_label("중심 기압 (hPa)", fontsize=9)
cb.ax.tick_params(labelsize=8)
# 일생의 주요 순간 네 곳에만 이름표를 단다
events = {
    "발생(열대 폭풍)": h[h["grade"] >= 3].index[0],
    "최성기(최저 기압)": h["pres"].idxmin(),
    "상륙 직전": h[h["kst"] <= "2022-09-06 04:50"].index[-1],
    "온대 저기압으로 변질": h[h["grade"] == 6].index[0],
}
offsets = [(-96, 20), (-96, -4), (8, -14), (8, 0)]
for (label, i), off in zip(events.items(), offsets):
    r = h.loc[i]
    ax.annotate(f"{label}\n{r.kst:%m/%d %H시} · {r.pres} hPa", (r.lon, r.lat), xytext=off,
                textcoords="offset points", fontsize=7, arrowprops=dict(arrowstyle="-",
                                                                        lw=0.6),
                bbox=dict(boxstyle="round", fc="w", alpha=0.85), transform=ccrs.PlateCarree())
gl = ax.gridlines(draw_labels=True, linewidth=0.3)
gl.top_labels = gl.right_labels = False
gl.xlabel_style = gl.ylabel_style = {"size": 8}
ax.set_title("태풍 힌남노(2022)의 진로와 중심 기압", fontsize=10)
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_04"))
plt.show()

# %% code Ⅳ-75.
landfall = pd.Timestamp("2022-09-06 04:50")

fig, ax = plt.subplots(2, 1, figsize=(7.5, 4.1), sharex=True)
ax[0].plot(h["kst"], h["pres"], "o-", color="purple", ms=3)
ax[0].set_ylabel("중심 기압 (hPa)")
ax[0].invert_yaxis()
ax[1].plot(h["kst"], h["wind_ms"], "o-", color="darkorange", ms=3)
ax[1].axhline(17, color="gray", ls=":", lw=1)
ax[1].text(h["kst"].iloc[-1], 18, "17 m/s (태풍 기준)", fontsize=9, ha="right",
           color="gray")
ax[1].set_ylabel("최대 풍속 (m/s)")
for a in ax:
    a.axvline(landfall, color="crimson", ls="--")
    a.grid(alpha=0.3)
ax[0].set_title("힌남노의 중심 기압과 최대 풍속 (빨간 선: 거제 상륙)")
fig.autofmt_xdate()
plt.tight_layout()
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_05"))
plt.show()

print(f"가장 낮은 중심 기압: {h['pres'].min()} hPa ({h.loc[h['pres'].idxmin(), 'kst']:%m월 %d일 %H시})")
print(f"가장 센 최대 풍속: {h['wind_ms'].max():.0f} m/s")

# 급격한 발달: 열대 폭풍이 된 때부터 최저 기압까지
ts0, pmin = h[h["grade"] >= 3].iloc[0], h.loc[h["pres"].idxmin()]
hours = (pmin["kst"] - ts0["kst"]).total_seconds() / 3600
print(f"열대 폭풍이 된 때({ts0['kst']:%m월 %d일 %H시}, {ts0['pres']} hPa)부터 "
      f"{hours:.0f}시간 동안 {ts0['pres'] - pmin['pres']} hPa 떨어짐")

# 다시 발달: 9월 2~5일 사이 가장 약할 때와 그 뒤 가장 강할 때
mid = h[(h["kst"] >= "2022-09-02") & (h["kst"] < "2022-09-06")]
weak = mid.loc[mid["pres"].idxmax()]
strong = mid[mid["kst"] > weak["kst"]].loc[lambda d: d["pres"].idxmin()]
print(f"다시 발달: {weak['kst']:%m월 %d일 %H시} {weak['pres']} hPa → "
      f"{strong['kst']:%m월 %d일 %H시} {strong['pres']} hPa")

# %% code Ⅳ-76.
sel = bt[(bt["year"] >= 1977) & bt["grade"].isin([3, 4, 5])].copy()
bins = np.arange(5, 47, 2)
sel["lat_bin"] = pd.cut(sel["lat"], bins)
groups = [g["pres"].values for _, g in sel.groupby("lat_bin", observed=False)]

fig, ax = plt.subplots(figsize=(8.3, 3.2))
ax.boxplot(groups, positions=bins[:-1] + 1, widths=1.4, showfliers=False)
ax.set_xticks(bins[:-1] + 1)
ax.set_xticklabels([f"{b + 1}" for b in bins[:-1]], fontsize=9)
ax.invert_yaxis()
ax.set_xlabel("위도 (°N, 구간 가운데 값)")
ax.set_ylabel("중심 기압 (hPa)")
ax.set_title("위도별 태풍 중심 기압 분포 (1977~, 위쪽일수록 강함)")
ax.grid(alpha=0.3)
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_06"))
plt.show()

# %% code Ⅳ-77.
# 힌남노의 이동 속도: 거제 상륙(6일 04:50 KST) 직전 6시간
# 9월 5일 12시~18시(UTC) = 5일 21시~6일 3시(KST) 사이 이동 거리 / 시간
a, b = h.set_index("time").loc["2022-09-05 12:00"], h.set_index("time").loc["2022-09-05 18:00"]
dy = (b["lat"] - a["lat"]) * 111e3
dx = (b["lon"] - a["lon"]) * 111e3 * np.cos(np.deg2rad((a["lat"] + b["lat"]) / 2))
move_u, move_v = dx / 6 / 3600, dy / 6 / 3600
print(f"이동 속도: {np.hypot(move_u, move_v):.1f} m/s, 방향: 북쪽에서 시계 방향 {np.rad2deg(np.arctan2(move_u, move_v)):.0f}°")

VMAX, RMAX = 35.0, 50e3                 # 최대 회전 풍속(m/s), 최대 풍속 반경(m) — 모형 값
x = np.linspace(-300e3, 300e3, 121)
X, Y = np.meshgrid(x, x)
R = np.hypot(X, Y) + 1
vt = np.where(R < RMAX, VMAX * R / RMAX, VMAX * RMAX / R)  # 회전 풍속
u_rot, v_rot = -vt * Y / R, vt * X / R  # 시계 반대 방향
U, V = u_rot + move_u, v_rot + move_v
speed = np.hypot(U, V)

fig, ax = plt.subplots(figsize=(5.6, 4.6))
cf = ax.contourf(X / 1e3, Y / 1e3, speed, levels=np.arange(0, 56, 5),
                 cmap="YlOrRd")
step = 10
ax.quiver(X[::step, ::step] / 1e3, Y[::step, ::step] / 1e3, U[::step, ::step],
          V[::step, ::step], scale=600)
ax.annotate("", xy=(move_u * 4, move_v * 4), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", lw=3, color="blue"))
ax.text(150, -250, "위험 반원\n(오른쪽)", fontsize=9, ha="center",
        color="darkred", weight="bold")
ax.text(-150, -250, "가항 반원\n(왼쪽)", fontsize=9, ha="center",
        color="navy", weight="bold")
cb = plt.colorbar(cf)
cb.set_label("풍속 (m/s)", fontsize=9)
cb.ax.tick_params(labelsize=8)
ax.set_xlabel("동서 거리 (km)", fontsize=9)
ax.set_ylabel("남북 거리 (km)", fontsize=9)
ax.tick_params(labelsize=8)
ax.set_aspect("equal")
ax.set_title("움직이는 태풍 모형의 바람 (파란 화살표: 이동 방향)", fontsize=10)
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_07"))
plt.show()

# %% code Ⅳ-78.
cols = ["date", "hour", "temp", "dwpt", "rhum", "prcp", "snow", "wdir",
        "wspd", "wpgt", "pres", "tsun", "coco"]
st_file = Path(proj_dir) / "meteostat_47153.csv.gz"
if not st_file.exists():
    du.download("https://bulk.meteostat.net/v2/hourly/47153.csv.gz", st_file)
obs = pd.read_csv(st_file, names=cols)
obs["kst"] = pd.to_datetime(obs["date"]) + pd.to_timedelta(obs["hour"],
                                                           unit="h") + pd.Timedelta("9h")
w = obs[(obs["kst"] >= "2022-09-05 09:00") & (obs["kst"] <= "2022-09-06 18:00")].set_index("kst")

fig, ax = plt.subplots(4, 1, figsize=(7.5, 5.4), sharex=True)
ax[0].plot(w.index, w["pres"], color="purple"); ax[0].set_ylabel("기압 (hPa)")
ax[1].plot(w.index, w["wspd"] / 3.6, color="darkorange"); ax[1].set_ylabel("풍속 (m/s)")
ax[2].scatter(w.index, w["wdir"], c="teal", s=12); ax[2].set_ylabel("풍향 (°)")
ax[2].set_yticks([0, 90, 180, 270, 360]); ax[2].set_yticklabels(["북", "동",
                                                                 "남", "서",
                                                                 "북"])
ax[3].bar(w.index, w["prcp"].fillna(0), width=0.035, color="royalblue"); ax[3].set_ylabel("강수량 (mm)")
t_min = w["pres"].idxmin()
for a in ax:
    a.axvline(t_min, color="crimson", ls="--")
    a.grid(alpha=0.3)
ax[0].set_title(f"힌남노가 지날 때 김해의 기록 (빨간 선: 기압 최저 {w['pres'].min():.0f} hPa, {t_min:%d일 %H시})")
fig.autofmt_xdate()
plt.tight_layout()
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_08"))
plt.show()
