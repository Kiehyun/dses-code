# 지구과학 데이터 사이언스 2 | IV-07. MODIS 에어로졸 광학 두께(AOD) 지도 그리기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅳ-97.
from mpl_toolkits.basemap import Basemap
from pyhdf.SD import SD, SDC

# %% code Ⅳ-98.
# 구글 드라이브에 공유한 MODIS 에어로졸 파일 내려받기
modis_url = (
    "https://docs.google.com/uc?export=download&id=1x5NgxKJR7w2dmS3NsC3nd8r0-CdG7XDA")
du.download(modis_url, proj_dir / "MOD04_L2.A2023103.0135.061.2023134174649.hdf")

# %% code Ⅳ-99.
from pyhdf.SD import SD, SDC

# 파일명 변수 설정
base_dr = str(proj_dir) + "/"
filename = "MOD04_L2.A2023103.0135.061.2023134174649.hdf"

# hdf 파일 읽기
hdf = SD("{}{}".format(base_dr, filename), SDC.READ)
print("hdf: {}".format(hdf))

# %% code Ⅳ-100.
print([name for name in dir(hdf) if not name.startswith("_")])

# %% code Ⅳ-101.
hdf.datasets()

# %% code Ⅳ-102.
DATAFIELD_NAME = "Optical_Depth_Land_And_Ocean"
hdf_raw = hdf.select(DATAFIELD_NAME)
print("hdf_raw: {}".format(hdf_raw))

# %% code Ⅳ-103.
hdf_raw[:,:]

# %% code Ⅳ-104.
import numpy as np
hdf_array = np.array(hdf_raw[:,:])
print("np.shape(hdf_array): {}".format(np.shape(hdf_array)))
print("hdf_array:\n {}".format(hdf_array))

# %% code Ⅳ-105.
import numpy as np

# 위도값
lat_raw = hdf.select('Latitude')
latitude = np.array(lat_raw[:,:])
print("np.shape(latitude): {}".format(np.shape(latitude)))
print("latitude: {}".format(latitude))

# 경도값
lon_raw = hdf.select('Longitude')
longitude = np.array(lon_raw[:,:])
print("np.shape(longitude): {}".format(np.shape(longitude)))
print("longitude: {}".format(longitude))

# %% code Ⅳ-106.
for i in longitude[:10] :
    print("longitude: {}".format(i))

# %% code Ⅳ-107.
for i in latitude[:10] :
    print("latitude: {}".format(i))

# %% code Ⅳ-108.
print("np.shape(hdf_array): {}".format(np.shape(hdf_array)))
print("np.shape(latitude): {}".format(np.shape(latitude)))
print("np.shape(longitude): {}".format(np.shape(longitude)))

# %% code Ⅳ-109.
print("hdf_array: {}".format(hdf_array))
print("np.shape(hdf_array): {}".format(np.shape(hdf_array)))
print("type(hdf_array): {}".format(type(hdf_array)))
print("hdf_array.dtype: {}".format(hdf_array.dtype))

# %% code Ⅳ-110.
print("hdf_raw.attributes(): {}".format(hdf_raw.attributes()))
print("hdf_raw.dimensions(): {}".format(hdf_raw.dimensions()))
print("hdf_raw.getfillvalue(): {}".format(hdf_raw.getfillvalue()))

# %% code Ⅳ-111.
print("hdf_array.dtype : {}".format(hdf_array.dtype))
print("latitude.dtype : {}".format(latitude.dtype))
print("longitude.dtype : {}".format(longitude.dtype))

# %% code Ⅳ-112.
hdf_array = hdf_array.astype(dtype=np.float64)
print("type(hdf_array): {}".format(type(hdf_array)))

hdf_array[hdf_array == hdf_raw.attributes()['_FillValue']] = np.nan
print("hdf_array: {}".format(hdf_array))

# %% code Ⅳ-113.
hdf_array[hdf_array < hdf_raw.attributes()['valid_range'][0]] = np.nan
hdf_array[hdf_array > hdf_raw.attributes()['valid_range'][1]] = np.nan
print("hdf_array: {}".format(hdf_array))

# %% code Ⅳ-114.
print("lon_raw.attributes(): {}".format(lon_raw.attributes()))
print("lon_raw.attributes()['valid_range']: {}".format(lon_raw.attributes()['valid_range']))

longitude[longitude < lon_raw.attributes()['valid_range'][0]] = np.nan
longitude[longitude > lon_raw.attributes()['valid_range'][1]] = np.nan
print("longitude: {}".format(longitude))

print("lat_raw.attributes(): {}".format(lat_raw.attributes()))
print("lat_raw.attributes()['valid_range']: {}".format(lat_raw.attributes()['valid_range']))

latitude[latitude < lat_raw.attributes()['valid_range'][0]] = np.nan
latitude[latitude > lat_raw.attributes()['valid_range'][1]] = np.nan
print("latitude: {}".format(latitude))

# %% code Ⅳ-115.
attrs = hdf_raw.attributes()
print("hdf_raw.attributes()['scale_factor']: {}".format(attrs['scale_factor']))
print("hdf_raw.attributes()['add_offset']: {}".format(attrs['add_offset']))

# %% code Ⅳ-116.
fill_value = hdf_raw.attributes()['_FillValue']
scale_factor = hdf_raw.attributes()['scale_factor']
offset = hdf_raw.attributes()['add_offset']
hdf_value = hdf_array * scale_factor + offset
hdf_value = np.array(hdf_value)
print("hdf_value: {}".format(hdf_value))

# %% code Ⅳ-117.
print("np.shape(hdf_value): {}".format(np.shape(hdf_value)))
print("np.shape(latitude): {}".format(np.shape(latitude)))
print("np.shape(longitude): {}".format(np.shape(longitude)))

print("hdf_value.dtype : {}".format(hdf_value.dtype))
print("latitude.dtype : {}".format(latitude.dtype))
print("longitude.dtype : {}".format(longitude.dtype))

# %% code Ⅳ-118.
import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(8.2, 4.3))

# 히스토그램 그리기(NaN을 뺀 유효한 값만 1차원으로)
valid = hdf_value[~np.isnan(hdf_value)]
plt.hist(valid, bins=50)

# 제목, 축 이름 지정
plt.title("AOD 히스토그램 — {0}\n{1}".format(DATAFIELD_NAME, filename), fontsize=12)
plt.xlabel("AOD (파장 0.55 µm)", fontsize=11)
plt.ylabel("칸 수", fontsize=11)
plt.tick_params(labelsize=9)

# 주석(annotate) 지정
plt.annotate("평균 : {0:.02f}, 최댓값 : {1:.02f}, 최솟값 : {2:.02f}".\
            format(np.nanmean(hdf_value), np.nanmax(hdf_value),
                   np.nanmin(hdf_value)),
        xy=(1, 1), xytext=(-12, -12), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points')

plt.annotate("경도 : {0:.01f} ~ {1:.01f}, 위도 : {2:.01f} ~ {3:.01f}".\
            format(np.nanmin(longitude), np.nanmax(longitude),
                   np.nanmin(latitude), np.nanmax(latitude)),
        xy=(1, 0.94), xytext=(-12, -12), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points')

print("유효한 AOD 칸: {} / {} ({:.1f}%)".format(valid.size, hdf_value.size,
                                          100 * valid.size / hdf_value.size))
plt.grid(True)
plt.show()

# %% code Ⅳ-119.
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

plt.figure(figsize=(7.5, 5))

# 원통 도법 지도
m = Basemap(projection='cyl')

# 해안선 · 국경 그리기, 대륙 채우기
m.drawcoastlines(linewidth=0.25)
m.drawcountries(linewidth=0.25)
m.fillcontinents()

m.drawparallels(np.arange(-90., 90.1, 30.), labels=[1, 1, 1, 1], fontsize=9)
m.drawmeridians(np.arange(-180., 180.1, 30.), labels=[1, 1, 1, 1], fontsize=9)

plt.show()

# %% code Ⅳ-120.
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

plt.figure(figsize=(4.6, 4.2))

#####
# 지도
m = Basemap(projection='laea', resolution='l', lat_ts=37,
            lat_0 = 37, lon_0 = 127, width=1.5e7, height=1.5e7)

# 해안선 · 국경 그리기, 대륙 채우기
m.drawcoastlines(linewidth=0.25)
m.drawcountries(linewidth=0.25)
m.fillcontinents()

m.drawparallels(np.arange(-90., 90.1, 45.), labels=[1, 0, 1, 0], fontsize=8)
m.drawmeridians(np.arange(-180., 180.1, 45.), labels=[0, 1, 0, 1], fontsize=8)

plt.show()

# %% code Ⅳ-121.
print("np.nanmin(longitude):{}".format(np.nanmin(longitude)))
print("np.nanmax(longitude):{}".format(np.nanmax(longitude))) 
print("np.nanmin(latitude):{}".format(np.nanmin(latitude)))
print("np.nanmax(latitude):{}".format(np.nanmax(latitude)))

# %% code Ⅳ-122.
Wlon, Elon = np.nanmin(longitude), np.nanmax(longitude)  # 서 · 동 경계
Slat, Nlat = np.nanmin(latitude), np.nanmax(latitude)  # 남 · 북 경계
Clon, Clat = (Wlon + Elon) / 2, (Slat + Nlat) / 2  # 중심 좌표

print(f"서 {Wlon:.2f}°, 동 {Elon:.2f}°, 남 {Slat:.2f}°, 북 {Nlat:.2f}°")
print(f"중심 ({Clon:.2f}°E, {Clat:.2f}°N)")

# %% code Ⅳ-123.
def findRangeOfMap(longitude, latitude, idl=False):
    """경위도 배열로 지도의 서 · 동 · 남 · 북 경계와 중심 좌표를 구한다.

    idl=True 이면 날짜 변경선을 지나는 장면으로 보고 경도를 0~360°로 바꾸어 계산한다.
    """
    lon = longitude % 360 if idl else longitude
    Wlon, Elon = np.nanmin(lon), np.nanmax(lon)
    Clon = (Wlon + Elon) / 2
    if idl:                                   # 다시 -180~180° 범위로
        Wlon, Elon, Clon = [(v + 180) % 360 - 180 for v in (Wlon, Elon, Clon)]
    Slat, Nlat = np.nanmin(latitude), np.nanmax(latitude)
    Clat = (Slat + Nlat) / 2
    return Wlon, Elon, Slat, Nlat, Clon, Clat

Wlon, Elon, Slat, Nlat, Clon, Clat = findRangeOfMap(longitude, latitude)
print(f"서 {Wlon:.2f}°, 동 {Elon:.2f}°, 남 {Slat:.2f}°, 북 {Nlat:.2f}°")
print(f"중심 ({Clon:.2f}°E, {Clat:.2f}°N)")

# %% code Ⅳ-124.
lon_idl = np.array([[170.0, 175.0, -175.0, -170.0]])       # 날짜 변경선을 지나는 가상 장면
lat_idl = np.array([[30.0, 31.0, 32.0, 33.0]])

for idl in (False, True):
    W, E, S, N, Cx, Cy = findRangeOfMap(lon_idl, lat_idl, idl)
    print(f"idl={idl!s:5}: 서 {W:7.1f}°, 동 {E:7.1f}°, 중심 경도 {Cx:7.1f}°")

# %% code Ⅳ-125.
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

plt.figure(figsize=(8.2, 5))

# 원통 도법 지도
m = Basemap(projection='cyl')

# 해안선 · 국경 그리기, 대륙 채우기
m.drawcoastlines(linewidth=0.25)
m.drawcountries(linewidth=0.25)
m.fillcontinents()

m.drawparallels(np.arange(-90., 90.1, 30.), labels=[1, 0, 0, 0], fontsize=9)
m.drawmeridians(np.arange(-180., 180.1, 30.), labels=[1, 1, 1, 1], fontsize=9)

# 제목 지정
plt.title('MODIS {} \n'.format(DATAFIELD_NAME), fontsize=12)      

# 지도 위에 데이터 표시
x, y = m(longitude, latitude) # 투영 지도로 변환
m.pcolormesh(x, y, hdf_value)

plt.show()

# %% code Ⅳ-126.
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

plt.figure(figsize=(8.2, 5))

# 원통 도법 지도
m = Basemap(projection='cyl')

# 해안선 · 국경 그리기, 대륙 채우기
m.drawcoastlines(linewidth=0.25)
m.drawcountries(linewidth=0.25)
m.fillcontinents()

m.drawparallels(np.arange(-90., 90.1, 30.), labels=[1, 0, 0, 0], fontsize=9)
m.drawmeridians(np.arange(-180., 180.1, 30.), labels=[1, 1, 1, 1], fontsize=9)

# 제목 지정
plt.title('MODIS {} \n'.format(DATAFIELD_NAME), fontsize=12)      

# 지도 위에 데이터 표시
x, y = m(longitude, latitude) # 투영 지도로 변환
m.pcolormesh(x, y, hdf_value)

# 컬러바 추가
m.colorbar()

# 주석(annotate) 지정
plt.annotate("평균 : {0:.02f}, 최댓값 : {1:.02f}, 최솟값 : {2:.02f}".\
            format(np.nanmean(hdf_value), np.nanmax(hdf_value),
                   np.nanmin(hdf_value)),
        xy=(0, 0), xytext=(12, -30), va='top',
        xycoords='axes fraction', textcoords='offset points')

plt.annotate("경도 : {0:.01f} ~ {1:.01f}, 위도 : {2:.01f} ~ {3:.01f}".\
            format(Wlon, Elon, Slat, Nlat),
        xy=(0, 0), xytext=(12, -44), va='top',
        xycoords='axes fraction', textcoords='offset points')

plt.annotate("파일 : {}".format(filename),
        xy=(1, 0), xytext=(12, -58), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points')

plt.show()

# %% code Ⅳ-127.
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

plt.figure(figsize=(4.9, 3.9))

# 지도 표시 범위 찾기
Wlon, Elon, Slat, Nlat, Clon, Clat = findRangeOfMap(longitude, latitude)

#####
# 지도
m = Basemap(projection='laea', lat_ts = Clat, lat_0 = Clat, lon_0 = Clon,\
            width=4e6, height=4e6, resolution='i')

# 해안선 · 국경 그리기, 대륙 채우기
m.drawcoastlines(linewidth=0.25)
m.drawcountries(linewidth=0.25)
m.fillcontinents()

m.drawparallels(np.arange(-90., 90.1, 10.), labels=[1, 0, 1, 0], fontsize=8)
m.drawmeridians(np.arange(-180., 180.1, 10.), labels=[0, 0, 1, 1], fontsize=8)

# 제목 지정
plt.title('MODIS {} \n'.format(DATAFIELD_NAME), fontsize=10)      

# 지도 위에 데이터 표시
x, y = m(longitude, latitude)
m.pcolormesh(x, y, hdf_value)
m.colorbar().ax.tick_params(labelsize=8)

# 주석(annotate) 지정
plt.annotate("평균 : {0:.02f}, 최댓값 : {1:.02f}, 최솟값 : {2:.02f}".\
            format(np.nanmean(hdf_value), np.nanmax(hdf_value),
                   np.nanmin(hdf_value)),
        xy=(0, 0), xytext=(12, -22), va='top',
        xycoords='axes fraction', textcoords='offset points', fontsize=8)

plt.annotate("경도 : {0:.01f} ~ {1:.01f}, 위도 : {2:.01f} ~ {3:.01f}".\
            format(Wlon, Elon, Slat, Nlat),
        xy=(0, 0), xytext=(12, -33), va='top',
        xycoords='axes fraction', textcoords='offset points', fontsize=8)

plt.annotate("파일 : {}".format(filename),
        xy=(1, 0), xytext=(12, -44), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points', fontsize=8)

plt.show()
