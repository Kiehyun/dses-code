# 지구과학 데이터 사이언스 2 | IV-09. 수괴와 T-S도
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 509.
from pathlib import Path
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import gsw

SERVER = "https://www.ncei.noaa.gov/data/oceans/woa/WOA23/DATA"
PATHS = {
    "t": "temperature/netcdf/decav/1.00/woa23_decav_t00_01.nc",
    "s": "salinity/netcdf/decav/1.00/woa23_decav_s00_01.nc",
    "o": "oxygen/netcdf/all/1.00/woa23_all_o00_01.nc",
}
VARS = {"t": "t_an", "s": "s_an", "o": "o_an"}

def open_woa(key):
    """WOA23 파일(약 80 MB)을 처음 한 번 내려받아 두고 열기"""
    local = Path(proj_dir) / Path(PATHS[key]).name
    if not local.exists():
        du.download(f"{SERVER}/{PATHS[key]}", local)
    return xr.open_dataset(local, decode_times=False)

def get_section(lon):
    """경도 lon(°E, 서경은 음수)의 남북 단면(수온 · 염분 · 용존 산소) 받기"""
    nc_file = Path(proj_dir) / f"woa23_section_{lon:+.1f}.nc"
    if nc_file.exists():
        return xr.open_dataset(nc_file)
    data = {}
    for key in PATHS:
        ds = open_woa(key)
        da = ds[VARS[key]].isel(time=0).sel(lon=lon, method="nearest")
        data[key] = da.drop_vars("time").load()
    sec = xr.Dataset(data)
    sec.to_netcdf(nc_file)
    return sec

atl = get_section(-25.5)   # 대서양 25.5°W
print(atl)

# %% code 510.
panels = [
    ("t", "수온 (°C)", "RdYlBu_r", np.arange(-2, 29, 1), [0, 2, 4, 10]),
    ("s", "실용염분", "viridis", np.arange(33.8, 37.01, 0.1),
     [34.3, 34.7, 34.9, 35.5]),
    ("o", "용존 산소 (µmol/kg)", "YlGnBu", np.arange(140, 361, 10),
     [200, 250, 280]),
]

fig, axes = plt.subplots(3, 1, figsize=(7.5, 5.4), sharex=True)
for ax, (key, label, cmap, levels, lines) in zip(axes, panels):
    da = atl[key]
    cf = ax.contourf(da.lat, da.depth, da, levels=levels, cmap=cmap,
                     extend="both")
    cs = ax.contour(da.lat, da.depth, da, levels=lines, colors="k",
                    linewidths=0.7)
    ax.clabel(cs, fmt="%g", fontsize=8)
    ax.set_ylim(5500, 0)
    ax.set_ylabel("깊이 (m)")
    ax.set_title(f"대서양 25.5°W 단면 — {label}")
    fig.colorbar(cf, ax=ax, pad=0.01)
axes[-1].set_xlim(-70, 65)
axes[-1].set_xlabel("위도 (°N, 남위는 음수)")
plt.tight_layout()
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_01"))
plt.show()

# %% code 511.
def add_density(sec, lon):
    depth2d, lat2d = np.meshgrid(sec.depth.values, sec.lat.values,
                                 indexing="ij")
    p = gsw.p_from_z(-depth2d, lat2d)           # 깊이(m) → 압력(dbar)
    SA = gsw.SA_from_SP(sec["s"].values, p, lon, lat2d)  # 절대 염분 (g/kg)
    CT = gsw.CT_from_t(SA, sec["t"].values, p)  # 보존 수온 (°C)
    sec["sigma0"] = (("depth", "lat"), gsw.sigma0(SA, CT))  # 포텐셜 밀도 - 1000
    sec["theta"] = (("depth", "lat"), gsw.pt_from_CT(SA, CT))  # 포텐셜 수온
    return sec

atl = add_density(atl, -25.5)
print(f"σθ 범위: {float(atl.sigma0.min()):.2f} ~ {float(atl.sigma0.max()):.2f}")

# %% code 512.
fig, ax = plt.subplots(figsize=(7.5, 3.4))
cf = ax.contourf(atl.lat, atl.depth, atl["s"],
                 levels=np.arange(33.8, 37.01, 0.1), cmap="viridis",
                 extend="both")
cs = ax.contour(atl.lat, atl.depth, atl["sigma0"],
                levels=[26.8, 27.2, 27.5, 27.7, 27.8, 27.85, 27.9],
                colors="w", linewidths=0.8)
ax.clabel(cs, fmt="%.2f", fontsize=8)
ax.set_ylim(5500, 0)
ax.set_xlim(-70, 65)
ax.set_xlabel("위도 (°N)")
ax.set_ylabel("깊이 (m)")
ax.set_title("대서양 25.5°W — 염분(색)과 포텐셜 밀도 σθ(흰 선)")
fig.colorbar(cf, ax=ax, pad=0.01, label="실용염분")
plt.tight_layout()
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_02"))
plt.show()

# %% code 513.
S = atl["s"].values.ravel()
TH = atl["theta"].values.ravel()
D = np.broadcast_to(atl.depth.values[:, None], atl["s"].shape).ravel()
ok = np.isfinite(S) & np.isfinite(TH)

# 등밀도선(포텐셜 밀도) 격자
s_grid, t_grid = np.meshgrid(np.linspace(33.6, 37.2, 200),
                             np.linspace(-2.5, 28, 200))
sig_grid = gsw.sigma0(s_grid, t_grid)   # 표층 근사(SA≈SP, CT≈θ)로 그린 등밀도선

fig, ax = plt.subplots(figsize=(8.6, 4.6))
cs = ax.contour(s_grid, t_grid, sig_grid, levels=np.arange(23, 28.6, 0.5),
                colors="gray", linewidths=0.6)
ax.clabel(cs, fmt="%.1f", fontsize=8)
sc = ax.scatter(S[ok], TH[ok], c=D[ok], s=4, cmap="viridis_r", vmin=0,
                vmax=5000)
fig.colorbar(sc, ax=ax, label="깊이 (m)")

# 수괴별 조건(교육용 근사)에 맞는 점들의 평균 위치에 이름표 달기
LAT = np.broadcast_to(atl.lat.values[None, :], atl["s"].shape).ravel()
masks = {
    "남극 저층수\n(AABW)": ((TH < 1.0) & (D >= 3000), (0.55, -1.2)),
    "북대서양 심층수\n(NADW)": ((TH >= 1.5) & (TH <= 4.0) & (S >= 34.88) & (D >= 1200),
                                (0.55, -0.3)),
    "남극 중층수\n(AAIW)": ((S <= 34.45) & (D >= 400) & (D <= 1500),
                            (-0.25, 3.5)),
    "지중해 유출수\n(MOW)": ((S >= 35.3) & (D >= 800) & (D <= 1300)
                             & (LAT >= 25) & (LAT <= 45), (0.6, -1.5)),
}
for name, (m, (dx, dy)) in masks.items():
    s0, t0 = np.nanmean(S[m]), np.nanmean(TH[m])
    ax.annotate(name, (s0, t0), xytext=(s0 + dx, t0 + dy), fontsize=9, ha="center",
                arrowprops=dict(arrowstyle="->", color="crimson"),
                bbox=dict(boxstyle="round", fc="w", ec="crimson", alpha=0.9))
ax.set_xlim(33.8, 37.0)
ax.set_ylim(-2, 28)
ax.set_xlabel("실용염분")
ax.set_ylabel("포텐셜 수온 θ (°C)")
ax.set_title("대서양 25.5°W 단면의 T-S도 (회색 선: σθ)")
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_03"))
plt.show()

# %% code 514.
from matplotlib.colors import ListedColormap

th, s = atl["theta"].values, atl["s"].values
depth2d = np.broadcast_to(atl.depth.values[:, None], th.shape)
wm = np.full(th.shape, np.nan)
wm[(th < 1.0) & (depth2d >= 3000)] = 1                                    # AABW
wm[(th >= 1.5) & (th <= 4.0) & (s >= 34.88) & (depth2d >= 1200)] = 2      # NADW
wm[(s <= 34.45) & (depth2d >= 400) & (depth2d <= 1500)] = 3               # AAIW

cmap = ListedColormap(["#3b4cc0", "#e7a33e", "#5bb15b"])
fig, ax = plt.subplots(figsize=(7.5, 3.4))
ax.pcolormesh(atl.lat, atl.depth, wm, cmap=cmap, vmin=0.5, vmax=3.5,
              shading="nearest")
ax.contour(atl.lat, atl.depth, atl["sigma0"], levels=[27.2, 27.7, 27.85],
           colors="k", linewidths=0.5)
for name, (x, y), c in [("남극 저층수", (-40, 4800), "#3b4cc0"),
                        ("북대서양 심층수", (20, 2600), "#e7a33e"),
                        ("남극 중층수", (-30, 900), "#5bb15b")]:
    ax.text(x, y, name, color="w", fontsize=11, weight="bold", ha="center",
            bbox=dict(fc=c, ec="none", alpha=0.9))
ax.set_ylim(5500, 0)
ax.set_xlim(-70, 65)
ax.set_xlabel("위도 (°N)")
ax.set_ylabel("깊이 (m)")
ax.set_title("대서양 25.5°W — 수온 · 염분 기준으로 나눈 수괴")
plt.tight_layout()
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_04"))
plt.show()

# %% code 515.
pac = get_section(-165.5)   # 태평양 165.5°W

layer = slice(2500, 4000)
o_atl = atl["o"].sel(depth=layer).mean("depth")
o_pac = pac["o"].sel(depth=layer).mean("depth")

fig, ax = plt.subplots(figsize=(8.3, 3.3))
ax.plot(o_atl.lat, o_atl, color="tab:blue", label="대서양 25.5°W")
ax.plot(o_pac.lat, o_pac, color="tab:red", label="태평양 165.5°W")
ax.set_xlim(-70, 65)
ax.set_xlabel("위도 (°N)")
ax.set_ylabel("용존 산소 (µmol/kg)")
ax.set_title("수심 2,500~4,000 m 평균 용존 산소")
ax.grid(alpha=0.3)
ax.legend()
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_05"))
plt.show()

print(f"대서양 평균: {float(o_atl.mean()):.0f} µmol/kg, "
      f"태평양 평균: {float(o_pac.mean()):.0f} µmol/kg")

# %% code 516.
import cartopy.crs as ccrs
import cartopy.feature as cfeature

sfc_file = Path(proj_dir) / "woa23_surface_ts.nc"
if sfc_file.exists():
    sfc = xr.open_dataset(sfc_file)
else:
    sfc = xr.Dataset({k: open_woa(k)[VARS[k]].isel(time=0, depth=0)
                         .drop_vars(["time", "depth"]).load()
                      for k in ("t", "s")})
    sfc.to_netcdf(sfc_file)

from cartopy.util import add_cyclic_point

lon2d, lat2d = np.meshgrid(sfc.lon, sfc.lat)
SA0 = gsw.SA_from_SP(sfc["s"].values, 0, lon2d, lat2d)
sig0 = gsw.sigma0(SA0, gsw.CT_from_t(SA0, sfc["t"].values, 0))

sig0c, lonc = add_cyclic_point(sig0, coord=sfc.lon.values)   # 날짜 변경선의 이음매 없애기

fig = plt.figure(figsize=(7.5, 3.7))
ax = plt.axes(projection=ccrs.Robinson(central_longitude=-30))
cf = ax.contourf(lonc, sfc.lat, sig0c, levels=np.arange(22, 28.21, 0.2), cmap="cividis",
                 extend="both", transform=ccrs.PlateCarree())
cs = ax.contour(lonc, sfc.lat, sig0c, levels=[27.6], colors="red",
                linewidths=1.2, transform=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND, facecolor="lightgray", zorder=2)
ax.coastlines(linewidth=0.5, zorder=3)
ax.set_global()
cb = fig.colorbar(cf, ax=ax, orientation="horizontal", pad=0.04, shrink=0.7)
cb.set_label("해수면 포텐셜 밀도 σθ", fontsize=9)
cb.ax.tick_params(labelsize=8)
ax.set_title("연평균 해수면 밀도 — 빨간 선: σθ = 27.6", fontsize=10)

# 고위도 해역별 해수면 σθ 최댓값
bands = {"남극 주변(65°S 남쪽)": (-80, -65), "북대서양 고위도(60~80°N)": (60, 80),
         "북태평양 고위도(45~60°N)": (45, 60)}
for name, (la0, la1) in bands.items():
    band = (sfc.lat.values >= la0) & (sfc.lat.values <= la1)
    print(f"{name}: σθ 최댓값 {np.nanmax(sig0[band, :]):.2f}")
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_06"))
plt.show()
