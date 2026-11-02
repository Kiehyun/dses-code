# 지구과학 데이터 사이언스 2 | IV-03. 종관일기도 그리기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅳ-60.
import warnings
warnings.filterwarnings("ignore")           # 데이터 서버가 보내는 참고용 경고 숨기기

from datetime import datetime, timedelta
from siphon.catalog import TDSCatalog

# 사례 시각(세계시 UTC) — 2021년 1월 한파
valid_time = datetime(2021, 1, 7, 12)

# NCAR RDA의 GFS 0.25도 과거 데이터(d084001) 날짜별 카탈로그
RDA_URL = ("https://thredds.rda.ucar.edu/thredds/catalog/files/g/d084001/"
           f"{valid_time:%Y}/{valid_time:%Y%m%d}/catalog.xml")
file_name = f"gfs.0p25.{valid_time:%Y%m%d%H}.f000.grib2"   # f000 = 분석장

catalog = TDSCatalog(RDA_URL)
ncss = catalog.datasets[file_name].subset()  # 잘라 받기(NCSS) 기능 사용 준비

print("데이터 파일 :", file_name)
print("제공 변수 :", len(ncss.variables), "개")
print("사용 시각 :", valid_time, "UTC  =", valid_time + timedelta(hours=9), "KST")

# %% code Ⅳ-61.
import numpy as np

# 관심 영역(동아시아)과 연직면
NORTH, SOUTH, EAST, WEST = 55, 20, 150, 100
LEVEL_850 = 85000  # Pa 단위(850 hPa)
LEVEL_500 = 50000  # 500 hPa

def fetch(variable, level=None):
    """GFS 분석장에서 필요한 영역·변수만 잘라 받는다."""
    query = ncss.query()
    query.lonlat_box(north=NORTH, south=SOUTH, east=EAST, west=WEST)
    query.time(valid_time)
    query.accept("netcdf")                  # 이 서버는 NetCDF-3 형식으로 보냄
    query.variables(variable)
    if level is not None:
        query.vertical_level(level)
    return ncss.get_data(query)

def to_array(dataset, name):
    """결측이 표시된 배열을 계산하기 쉬운 실수 배열로 바꾼다."""
    values = np.squeeze(dataset.variables[name][:])
    return np.ma.filled(values, np.nan).astype(float)

data_mslp = fetch("Pressure_reduced_to_MSL_msl")      # 해면기압
data_t850 = fetch("Temperature_isobaric", LEVEL_850)  # 850 hPa 기온
data_z500 = fetch("Geopotential_height_isobaric", LEVEL_500)  # 500 hPa 고도
data_zsfc = fetch("Geopotential_height_surface")      # 지형 높이

lat = to_array(data_mslp, "latitude")
lon = to_array(data_mslp, "longitude")
print(f"격자 크기 : 위도 {lat.size}개 x 경도 {lon.size}개")

# %% code Ⅳ-62.
from metpy.units import units
import metpy.calc as mpcalc

mslp = to_array(data_mslp, "Pressure_reduced_to_MSL_msl") / 100.0   # Pa -> hPa
t850 = to_array(data_t850, "Temperature_isobaric") - 273.15         # K -> 섭씨
z500 = to_array(data_z500, "Geopotential_height_isobaric")          # m
zsfc = to_array(data_zsfc, "Geopotential_height_surface")           # 지형 높이 m

# 지형이 1000 m 이상인 곳은 850 hPa 면이 땅속에 있거나 지면에 붙어 있어 비워 둠
HIGH_TERRAIN = 1000
t850 = np.where(zsfc < HIGH_TERRAIN, t850, np.nan)

# 격자 잡음을 줄여 등압선이 매끄럽게 그려지도록 완만하게 다듬기
mslp_smooth = mpcalc.smooth_gaussian(mslp * units.hPa, 3).magnitude
z500_smooth = mpcalc.smooth_gaussian(z500 * units.m, 3).magnitude

print(f"해면기압   : {mslp.min():7.1f} ~ {mslp.max():7.1f} hPa")
print(f"850 hPa 기온: {np.nanmin(t850):7.1f} ~ {np.nanmax(t850):7.1f} °C  (지형 {HIGH_TERRAIN} m 미만)")
print(f"500 hPa 고도: {z500.min():7.0f} ~ {z500.max():7.0f} m")

# 서울(37.57°N, 126.97°E)에서 가장 가까운 격자의 850 hPa 기온
iy, ix = np.abs(lat - 37.57).argmin(), np.abs(lon - 126.97).argmin()
print(f"서울 상공 850 hPa 기온: {t850[iy, ix]:.1f} °C")

# %% code Ⅳ-63.
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

PROJ = ccrs.LambertConformal(central_longitude=127.5, central_latitude=38)
EXTENT = [105, 145, 22, 52]        # 지도에 실제로 보일 범위(경도, 위도)

def make_map(ax):
    """해안선과 국경을 그려 일기도 바탕을 만든다."""
    ax.set_extent(EXTENT, crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE.with_scale("50m"), linewidth=0.6)
    ax.add_feature(cfeature.BORDERS.with_scale("50m"), linewidth=0.4,
                   edgecolor="gray")
    gl = ax.gridlines(draw_labels=True, x_inline=False, y_inline=False,
                      linewidth=0.3, color="gray", alpha=0.5, linestyle=":")
    gl.top_labels = gl.right_labels = False
    gl.xlabel_style = gl.ylabel_style = {"size": 8}
    return ax

print("지도 바탕 함수 준비 완료")

# %% code Ⅳ-64.
fig = plt.figure(figsize=(5.6, 4.9))
ax = make_map(plt.axes(projection=PROJ))

# 850 hPa 기온을 색으로 표시
shade = ax.contourf(lon, lat, t850, levels=np.arange(-30, 41, 2),
                    cmap="RdYlBu_r", extend="both",
                    transform=ccrs.PlateCarree())

# 해면기압 등압선(4 hPa 간격)
isobars = ax.contour(lon, lat, mslp_smooth, levels=np.arange(940, 1061, 4),
                     colors="black", linewidths=1.0,
                     transform=ccrs.PlateCarree())
ax.clabel(isobars, fmt="%d", fontsize=7, inline=True)

cb = plt.colorbar(shade, ax=ax, orientation="horizontal", pad=0.12, aspect=35,
                  shrink=0.9)
cb.set_label("850 hPa 기온 (°C)", fontsize=9)
cb.ax.tick_params(labelsize=8)
ax.set_title(f"지상일기도  해면기압(hPa) + 850 hPa 기온\n"
             f"GFS 분석장 {valid_time:%Y-%m-%d %H}UTC", fontsize=10)

du.save_figure(fig, os.path.join(proj_dir, "surface_chart"))
plt.show()

# %% code Ⅳ-65.
from scipy.ndimage import maximum_filter, minimum_filter

def find_extrema(field, lon, lat, kind="min", size=25, count=4,
                 terrain=None, max_height=HIGH_TERRAIN):
    """기압장에서 고기압(max) 또는 저기압(min) 중심 위치를 찾는다."""
    filtered = (maximum_filter(field, size) if kind == "max"
                else minimum_filter(field, size))
    is_ext = field == filtered  # 창 안에서 극값인 지점
    margin = size // 2          # 경계에서 창 절반 이내는 제외
    is_ext[:margin, :] = is_ext[-margin:, :] = False
    is_ext[:, :margin] = is_ext[:, -margin:] = False
    if terrain is not None:                           # 높은 고원 위의 점 제외
        is_ext &= terrain < max_height
    rows, cols = np.where(is_ext)
    values = field[rows, cols]
    order = np.argsort(values)[::-1] if kind == "max" else np.argsort(values)
    picked = order[:count]
    return lon[cols[picked]], lat[rows[picked]], values[picked]

low_lon, low_lat, low_val = find_extrema(mslp_smooth, lon, lat, "min", terrain=zsfc)
high_lon, high_lat, high_val = find_extrema(mslp_smooth, lon, lat, "max", terrain=zsfc)

print("저기압 중심 (경도, 위도, hPa)")
for x, y, v in zip(low_lon, low_lat, low_val):
    print(f"  L  {x:6.1f}E {y:5.1f}N  {v:7.1f}")
print("고기압 중심 (경도, 위도, hPa)")
for x, y, v in zip(high_lon, high_lat, high_val):
    print(f"  H  {x:6.1f}E {y:5.1f}N  {v:7.1f}")

# %% code Ⅳ-66.
fig = plt.figure(figsize=(5.6, 4.9))
ax = make_map(plt.axes(projection=PROJ))

isobars = ax.contour(lon, lat, mslp_smooth, levels=np.arange(940, 1061, 4),
                     colors="black", linewidths=1.0,
                     transform=ccrs.PlateCarree())
ax.clabel(isobars, fmt="%d", fontsize=7)

# 저기압은 파란 L, 고기압은 빨간 H로 표시
for x, y in zip(low_lon, low_lat):
    ax.text(x, y, "L", color="blue", fontsize=11, fontweight="bold",
            ha="center", va="center", transform=ccrs.PlateCarree())
for x, y in zip(high_lon, high_lat):
    ax.text(x, y, "H", color="red", fontsize=11, fontweight="bold",
            ha="center", va="center", transform=ccrs.PlateCarree())

ax.set_title(f"기압계 배치  {valid_time:%Y-%m-%d %H}UTC", fontsize=10)
du.save_figure(fig, os.path.join(proj_dir, "pressure_systems"))
plt.show()

# %% code Ⅳ-67.
fig = plt.figure(figsize=(5.6, 4.9))
ax = make_map(plt.axes(projection=PROJ))

heights = ax.contour(lon, lat, z500_smooth, levels=np.arange(4800, 6061, 60),
                     colors="darkblue", linewidths=1.0,
                     transform=ccrs.PlateCarree())
ax.clabel(heights, fmt="%d", fontsize=7)

ax.set_title(f"500 hPa 상층일기도  등고선 간격 60 m\n"
             f"GFS 분석장 {valid_time:%Y-%m-%d %H}UTC", fontsize=10)
du.save_figure(fig, os.path.join(proj_dir, "upper_chart"))
plt.show()

# %% code Ⅳ-68.
fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.3),
                         subplot_kw={"projection": PROJ})

# 왼쪽: 지상일기도
make_map(axes[0])
cs = axes[0].contour(lon, lat, mslp_smooth, levels=np.arange(940, 1061, 4),
                     colors="black", linewidths=0.9,
                     transform=ccrs.PlateCarree())
axes[0].clabel(cs, fmt="%d", fontsize=7)
for x, y in zip(low_lon, low_lat):
    axes[0].text(x, y, "L", color="blue", fontsize=11, fontweight="bold",
                 ha="center", va="center", transform=ccrs.PlateCarree())
axes[0].set_title("지상 (해면기압)", fontsize=10)

# 오른쪽: 상층일기도
make_map(axes[1])
cs2 = axes[1].contour(lon, lat, z500_smooth, levels=np.arange(4800, 6061, 60),
                      colors="darkblue", linewidths=0.9,
                      transform=ccrs.PlateCarree())
axes[1].clabel(cs2, fmt="%d", fontsize=7)
axes[1].set_title("500 hPa (등고선)", fontsize=10)

fig.suptitle(f"지상과 상층 비교  {valid_time:%Y-%m-%d %H}UTC", fontsize=11)
du.save_figure(fig, os.path.join(proj_dir, "surface_vs_upper"))
plt.show()
