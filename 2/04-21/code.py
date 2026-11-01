# 지구과학 데이터 사이언스 2 | IV-01. 지구과학 데이터 형식
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 392.
# 파일 ID와 저장 경로를 리스트로 정의
files = [
    ("1E5TZgqXhh73i0VZLcY-xh7CNR3OJgB8K", "sst.wkmean.1990-present.nc"),
    ("1gxp1wK1JBhD215gQgVHPauTJnrfKv9Zi", "lsmask.nc"),
    ("1txeMeu4dVESAQj0AcKdOBAtduH3MaiX3", "T2008168030500.L2_LAC_SST.x.zip"),
    ("1vf01dzj_qkeY4PG_5VXRCxO-RhkBvYfH", "T2008170025000.L2_LAC_SST.x.zip")
]

# for 루프를 사용하여 파일 다운로드
for file_id, output_path in files:
    du.download(f"https://docs.google.com/uc?export=download&id={file_id}",
                PROJ / output_path)

# %% code 393.
fpaths = du.list_files(PROJ, pattern="*.*")

# %% code 394.
import shutil

for fpath in fpaths:
    if fpath.suffix == ".zip":
        print(fpath, "is unpacked to", str(PROJ))
        shutil.unpack_archive(str(fpath), str(PROJ))

fpaths = du.list_files(PROJ, "nc")

# %% code 395.
from netCDF4 import Dataset
import numpy as np

# 육지·바다 구분 마스크
file_path = str(PROJ / "lsmask.nc")  # NetCDF 파일 경로
nc_file = Dataset(file_path, 'r') 
nc_file.variables

# %% code 396.
from netCDF4 import Dataset
import numpy as np

# 육지·바다 구분 마스크
file_path = str(PROJ / "lsmask.nc")  # NetCDF 파일 경로
with Dataset(file_path, 'r') as nc_file:
    mask = nc_file.variables['mask'][:]  # 'mask' 변수 읽기
    mask = mask[0, :, :]                 # 첫 번째 시간 단계 선택
    mask = mask.astype(float)
    mask[mask == 0] = np.nan  # 육지 부분을 np.nan으로 변환

print("Mask data loaded and processed.")

# %% code 397.
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# NetCDF 파일 경로
file_path = str(PROJ / "sst.wkmean.1990-present.nc")  # SST 데이터 파일 경로
mask_path = str(PROJ / "lsmask.nc")  # Land-sea mask 파일 경로

# 변수명 확인
with Dataset(file_path, 'r') as sst_file:
    print("SST file variables:", list(sst_file.variables.keys()))

# %% code 398.
# 변수명에 따라 수정 (예: 'longitude', 'latitude' 등)
with Dataset(file_path, 'r') as sst_file, Dataset(mask_path, 'r') as mask_file:
 # 변수명 자동 탐색
    varnames = list(sst_file.variables.keys())
    if 'lon' in varnames:
        lon = sst_file.variables['lon'][:]
    elif 'longitude' in varnames:
        lon = sst_file.variables['longitude'][:]
    else:
        raise KeyError(f"Longitude variable not found in {file_path}")

    if 'lat' in varnames:
        lat = sst_file.variables['lat'][:]
    elif 'latitude' in varnames:
        lat = sst_file.variables['latitude'][:]
    else:
        raise KeyError(f"Latitude variable not found in {file_path}")

 # SST 변수명도 자동 탐색
    if 'sst' in varnames:
        sst = sst_file.variables['sst'][:]
    else:
        raise KeyError(f"SST variable not found in {file_path}")

    mask = mask_file.variables['mask'][0, :, :]
    print("sst.shape:", sst.shape)
    print("lon.shape:", lon.shape)
    print("lat.shape:", lat.shape)

# 데이터 전처리
sst = np.mean(sst, axis=0)  # 시간 평균 (scale_factor 는 netCDF4 가 이미 적용해 °C 단위)
mask = mask.astype(float)
mask[mask == 0] = np.nan  # 육지 부분을 NaN으로 설정
sst *= mask               # 육지 부분 제거
sst_c = np.ma.filled(sst, np.nan)
print(f"평균 SST 범위: {np.nanmin(sst_c):.1f} ~ {np.nanmax(sst_c):.1f} °C")

# 사용자 정의 컬러맵
levs = np.arange(-2, 35, 1)  # 온도 범위
jet = ["#000080", "blue", "#007FFF", "cyan", "#7FFF7F", "yellow", "#FF7F00",
       "red", "#7F0000"]
cm = LinearSegmentedColormap.from_list('custom_jet', jet, N=len(levs))

# %% code 399.
# 시각화
fig, ax = plt.subplots(figsize=(7.5, 3.8))
contour = ax.contourf(lon, lat, sst, levels=levs, cmap=cm, extend='both')
cbar = plt.colorbar(contour, ax=ax, orientation='vertical', fraction=0.02,
                    pad=0.04)
cbar.set_label('Sea Surface Temperature (°C)', fontsize=11)

ax.set_xticks(np.arange(0, 361, 60))
ax.set_xticklabels(['0°', '60°E', '120°E', '180°', '120°W', '60°W', '0°'])
ax.set_yticks(np.arange(-90, 91, 30))
ax.set_yticklabels(['90°S', '60°S', '30°S', '0°', '30°N', '60°N', '90°N'])
ax.set_title('NOAA OISST Sea Surface Temperature', fontsize=12)
ax.set_xlabel('Longitude', fontsize=11)
ax.set_ylabel('Latitude', fontsize=11)

plt.tight_layout()
plt.show()

# %% code 400.
from netCDF4 import Dataset

sst_l2 = PROJ / "T2008168030500.L2_LAC_SST.x.nc"   # 위성 해수면 온도(MODIS L2) 파일
nc = Dataset(sst_l2)

print("전역 속성 개수 :", len(nc.ncattrs()))
for key in ["title", "platform", "instrument", "processing_level",
            "time_coverage_start", "time_coverage_end", "spatialResolution"]:
    print(f"  {key:20s}: {nc.getncattr(key)}")
print("그룹 :", list(nc.groups))

# %% code 401.
for dim in nc.dimensions.values():
    print(dim)

# %% code 402.
print("nc.groups", nc.groups)
print("nc.groups['geophysical_data']", nc.groups['geophysical_data'])

# %% code 403.
print("nc.groups['geophysical_data']['sst']",
      nc.groups['geophysical_data']['sst'])
print("nc.groups['geophysical_data']['sst'].dimensions",
      nc.groups['geophysical_data']['sst'].dimensions)

# %% code 404.
print("nc.groups['navigation_data']", nc.groups['navigation_data'])
print("nc.groups['navigation_data']['latitude']",
      nc.groups['navigation_data']['latitude'])

# %% code 405.
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

latitude = nc.groups['navigation_data']['latitude'][:]
longitude = nc.groups['navigation_data']['longitude'][:]
sst = nc.groups['geophysical_data']['sst'][:]
qual = nc.groups['geophysical_data']['qual_sst'][:]   # 품질 플래그 (0 최상, 클수록 나쁨)
sst = np.ma.masked_where(qual > 1, sst)               # 품질 0·1 화소만 남김
print(f"품질 0·1 화소 수: {sst.count():,} / {sst.size:,}")

# %% code 406.
# 원소를 모두 찍으면 수천 줄이 나오므로 모양과 일부만 확인
import numpy as _np
_a = _np.asarray(latitude)
print(f"latitude: shape={_a.shape}, "
      f"min={_np.nanmin(_a):.4f}, max={_np.nanmax(_a):.4f}")
print("앞 5개 :", _np.ravel(_a)[:5])
print("뒤 5개 :", _np.ravel(_a)[-5:])
_o = _np.asarray(longitude)
print(f"longitude: shape={_o.shape}, "
      f"min={_np.nanmin(_o):.4f}, max={_np.nanmax(_o):.4f}")

# %% code 407.
print("latitude.dtype : {}".format(latitude.dtype))
print("longitude.dtype : {}".format(longitude.dtype))
print("sst.dtype : {}".format(sst.dtype))

# %% code 408.
DATAFIELD_NAME = "SST"

import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(8.4, 4.2))
#plt.title("Histogram")
plt.title("Histogram of {0}: {1}\n mean : {2:.02f}, max: {3:.02f}, min: {4:.02f}\n\
            longitude : {5:.02f}~{6:.02f}, latitude: {7:.02f}~{8:.02f}".format(DATAFIELD_NAME, sst_l2.name, 
            sst.mean(), sst.max(), sst.min(),
            np.nanmin(longitude), np.nanmax(longitude),
            np.nanmin(latitude), np.nanmax(latitude)), fontsize=11)

plt.hist(sst.compressed(), bins=40)   # 결측을 뺀 1차원 값
plt.grid(True)

plt.savefig(f"{PROJ}/{sst_l2.stem}_hist.pdf", bbox_inches='tight')
print(f"savefig: {PROJ}/{sst_l2.stem}_hist.pdf")
plt.show()   

# %% code 409.
Llon, Rlon, Slat, Nlat = 100, 150, 10, 60

import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

plt.figure(figsize=(4.4, 4.4))

# 원통 도법 지도
m = Basemap(projection='cyl', resolution='l', \
            llcrnrlat = Slat, urcrnrlat = Nlat, \
            llcrnrlon = Llon, urcrnrlon = Rlon)

m.drawcoastlines(linewidth=0.25)
m.drawcountries(linewidth=0.25)
m.fillcontinents()
m.drawmapboundary()

m.drawparallels(np.arange(-90., 90., 10.), labels=[1, 0, 0, 0], color='white', fontsize=8)
m.drawmeridians(np.arange(-180., 181., 15.), labels=[0, 0, 0, 1],
                color='white', fontsize=8)

x, y = m(longitude, latitude) # 투영 지도로 변환

plt.title('SST product using MODIS', fontsize=10) 
      
plt.show()

# %% code 410.
DATAFIELD_NAME = "SST"

print("="*80)
print("Plotting data on the map")

Llon, Rlon, Slat, Nlat = 100, 150, 10, 60

import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import warnings

plt.figure(figsize=(4.4, 4.2))

# 원통 도법 지도
m = Basemap(projection='cyl', resolution='l', \
            llcrnrlat = Slat, urcrnrlat = Nlat, \
            llcrnrlon = Llon, urcrnrlon = Rlon)

m.drawcoastlines(linewidth=0.25, color='white')
m.drawcountries(linewidth=0.25, color='white')
m.fillcontinents(color='black', lake_color='black')
m.drawmapboundary(fill_color='black')

m.drawparallels(np.arange(-90., 90., 10.), labels=[1, 0, 0, 0], color='white', fontsize=8)
m.drawmeridians(np.arange(-180., 181., 15.), labels=[0, 0, 0, 1],
                color='white', fontsize=8)

x, y = m(longitude, latitude) # 투영 지도로 변환
# L2 위경도는 화소마다 조금씩 휘어 있어(단조 증가가 아님) pcolormesh가 칸 경계를
# 어림한다는 UserWarning이 나온다. 그림에는 문제가 없으므로 이 경고만 끈다.
with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    m.pcolormesh(x, y, sst, vmin=14, vmax=24, cmap='RdYlBu_r', shading='auto')
m.colorbar(fraction=0.0455, pad=0.044, ticks=np.arange(14, 24.1, 2)).ax.tick_params(labelsize=8)

plt.title('SST product using MODIS', fontsize=10) 

x1, y1 = m(100, 7.5)
plt.text(x1, y1, 'Maximum value: {0:.1f}\nMean value: {1:.1f}\nMin value: {2:.1f}\n'\
            .format(sst.max(), sst.mean(), sst.min()), 
            horizontalalignment='left',
            verticalalignment='top', 
            fontsize=7, style='italic', wrap=True)

x2, y2 = m(149.5, 7.5)
plt.text(x2, y2, "{}\nMODIS SST product from Ocean Color Web\n".format(sst_l2.stem), 
            horizontalalignment='right',
            verticalalignment='top', 
            fontsize=7, style='italic', wrap=True)         

plt.savefig(f"{PROJ}/{sst_l2.stem}_{DATAFIELD_NAME}.pdf", bbox_inches='tight')
print(f"savefig: {PROJ}/{sst_l2.stem}_{DATAFIELD_NAME}.pdf")
plt.show()

# %% code 411.
Llon, Rlon, Slat, Nlat = 100, 150, 10, 60     # 지도 영역(경도 · 위도)
RES = 24                                      # 4 km 격자: 1도에 24칸

i0, i1 = int((90 - Nlat) * RES), int((90 - Slat) * RES)   # 위도 칸(북 → 남)
j0, j1 = int((Llon + 180) * RES), int((Rlon + 180) * RES) # 경도 칸(서 → 동)

fname = "AQUA_MODIS.20190801_20190831.L3m.MO.CHL.chlor_a.4km.nc"
url = ("https://oceandata.sci.gsfc.nasa.gov/opendap/MODISA/L3SMI/2019/0801/"
       f"{fname}.nc4?chlor_a[{i0}:1:{i1}][{j0}:1:{j1}],"
       f"lat[{i0}:1:{i1}],lon[{j0}:1:{j1}]")
print("요청 주소 :", url)

hdf_path = proj_dir / "AQUA_MODIS.201908.L3m.MO.chlor_a.4km_EastAsia.nc4"
du.download(url, hdf_path)

# %% code 412.
signature = hdf_path.read_bytes()[:8]
print("파일 크기 :", f"{hdf_path.stat().st_size / 1e6:.2f} MB")
print("서명      :", signature)
print("HDF5 인가 :", signature == b"\x89HDF\r\n\x1a\n")

# %% code 413.
import h5py

hdf = h5py.File(hdf_path, "r")
print("맨 위 항목 :", list(hdf.keys()))

def show(name, obj):
    """그룹과 데이터셋의 이름 · 모양 · 자료형을 출력"""
    if isinstance(obj, h5py.Dataset):
        print(f"  데이터셋 {name:10s} shape={obj.shape}  dtype={obj.dtype}")
    else:
        print(f"  그룹     {name}")

hdf.visititems(show)

# %% code 414.
import numpy as np

def attr(dset, key):
    """HDF5 속성 값을 파이썬 값으로 변환(바이트 → 문자열, 길이 1 배열 → 숫자)"""
    v = dset.attrs[key]
    if isinstance(v, bytes):
        return v.decode()
    if isinstance(v, np.ndarray) and v.size == 1:
        return v.item()
    return v

chl_ds = hdf["chlor_a"]
for key in ["long_name", "units", "_FillValue", "valid_min", "valid_max"]:
    print(f"{key:12s}: {attr(chl_ds, key)}")

# %% code 415.
chl = chl_ds[:].astype(float)
lat = hdf["lat"][:]
lon = hdf["lon"][:]

bad = ((chl == attr(chl_ds, "_FillValue"))
       | (chl < attr(chl_ds, "valid_min"))
       | (chl > attr(chl_ds, "valid_max")))
chl[bad] = np.nan
longitude, latitude = np.meshgrid(lon, lat)

print("배열 모양     :", chl.shape)
print("위도 범위     :", lat.min().round(2), "~", lat.max().round(2))
print("경도 범위     :", lon.min().round(2), "~", lon.max().round(2))
print("유효한 칸 비율:", f"{np.isfinite(chl).mean() * 100:.1f} %")
print(f"최솟값 · 중앙값 · 최댓값: {np.nanmin(chl):.3f} · {np.nanmedian(chl):.3f} · {np.nanmax(chl):.1f} mg/m³")

# %% code 416.
import matplotlib.pyplot as plt
plt.rcParams["axes.unicode_minus"] = False   # 로그 눈금의 마이너스(−)를 하이픈으로 표시

valid = chl[np.isfinite(chl)]
bins = np.logspace(-2, 2, 61)                 # 0.01 ~ 100 mg/m³, 로그 간격

fig, ax = plt.subplots(figsize=(8.2, 4.0))
ax.hist(valid, bins=bins, color="tab:green", alpha=0.8)
ax.set_xscale("log")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))   # 0.01, 0.1, 1 … 로 표시
ax.axvline(np.median(valid), color="k", ls="--",
           label=f"중앙값 {np.median(valid):.2f} mg/m³")
ax.set_xlabel("엽록소 농도 (mg/m³)")
ax.set_ylabel("칸 수")
ax.set_title("MODIS Aqua 엽록소 농도 분포 (2019년 8월)")
ax.legend()
plt.savefig(proj_dir / "chlor_a_hist.png", dpi=150, bbox_inches="tight")
plt.show()

# %% code 417.
from matplotlib.colors import LogNorm
from mpl_toolkits.basemap import Basemap

plt.figure(figsize=(4.8, 4.4))
m = Basemap(projection="cyl", resolution="l",
            llcrnrlat=Slat, urcrnrlat=Nlat, llcrnrlon=Llon, urcrnrlon=Rlon)
m.drawcoastlines(linewidth=0.3)
m.fillcontinents(color="lightgray", lake_color="white")
m.drawparallels(np.arange(-90., 90., 10.), labels=[1, 0, 0, 0], linewidth=0.3, fontsize=8)
m.drawmeridians(np.arange(-180., 181., 15.), labels=[0, 0, 0, 1], linewidth=0.3, fontsize=8)

x, y = m(longitude, latitude)
pm = m.pcolormesh(x, y, chl, norm=LogNorm(vmin=0.05, vmax=20),
                  cmap="viridis", shading="auto")
cb = m.colorbar(pm, location="right", pad="3%")
cb.set_label("엽록소 농도 (mg/m³)", fontsize=9)
cb.ax.tick_params(labelsize=8)
cb.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))
plt.title("MODIS Aqua 엽록소 농도 (2019년 8월 평균)", fontsize=10)
plt.savefig(proj_dir / "chlor_a_map.png", dpi=150, bbox_inches="tight")
plt.show()
hdf.close()
