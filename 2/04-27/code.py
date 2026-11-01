# 지구과학 데이터 사이언스 2 | IV-07. MODIS 에어로졸 광학 두께(AOD) 지도 그리기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 488.
from mpl_toolkits.basemap import Basemap
from pyhdf.SD import SD, SDC

# %% code 489.
# 구글 드라이브에 공유한 MODIS 에어로졸 파일 내려받기
modis_url = (
    "https://docs.google.com/uc?export=download&id=1_uveudlJRIk8hMisC0TJf7ngmMy6uh8G")
du.download(modis_url, proj_dir / "MOD04_L2.A2023103.0135.061.2023134174649.hdf")

# %% code 490.
from pyhdf.SD import SD, SDC

# 파일명 변수 설정
base_dr = str(proj_dir) + "/"
filename = "MOD04_L2.A2023103.0135.061.2023134174649.hdf"

# hdf 파일 읽기
hdf = SD("{}{}".format(base_dr, filename), SDC.READ)
print("hdf: {}".format(hdf))

# %% code 491.
dir(hdf)

# %% code 492.
hdf.datasets()

# %% code 493.
DATAFIELD_NAME = "Optical_Depth_Land_And_Ocean"
hdf_raw = hdf.select(DATAFIELD_NAME)
print("hdf_raw: {}".format(hdf_raw))

# %% code 494.
dir(hdf_raw)

# %% code 495.
hdf_raw[:,:]

# %% code 496.
import numpy as np
hdf_array = np.array(hdf_raw[:,:])
print("np.shape(hdf_array): {}".format(np.shape(hdf_array)))
print("hdf_array:\n {}".format(hdf_array))

# %% code 497.
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

# %% code 498.
for i in longitude[:10] :
    print("longitude: {}".format(i))

# %% code 499.
for i in latitude[:10] :
    print("latitude: {}".format(i))

# %% code 500.
#hdf_raw.getcompress()
#hdf_raw.getdatastrs()
#hdf_raw.getfillvalue()
#hdf_raw.getrange()

# %% code 501.
print("np.shape(hdf_array): {}".format(np.shape(hdf_array)))
print("np.shape(latitude): {}".format(np.shape(latitude)))
print("np.shape(longitude): {}".format(np.shape(longitude)))

# %% code 502.
print("hdf_array: {}".format(hdf_array))
print("np.shape(hdf_array): {}".format(np.shape(hdf_array)))
print("type(hdf_array): {}".format(type(hdf_array)))
print("hdf_array.dtype: {}".format(hdf_array.dtype))

# %% code 503.
print("hdf_raw.attributes(): {}".format(hdf_raw.attributes()))
print("hdf_raw.dimensions(): {}".format(hdf_raw.dimensions()))
print("hdf_raw.getfillvalue(): {}".format(hdf_raw.getfillvalue()))

# %% code 504.
print("hdf_array.dtype : {}".format(hdf_array.dtype))
print("latitude.dtype : {}".format(latitude.dtype))
print("longitude.dtype : {}".format(longitude.dtype))

# %% code 505.
hdf_array = hdf_array.astype(dtype=np.float64)
print("type(hdf_array): {}".format(type(hdf_array)))

hdf_array[hdf_array == hdf_raw.attributes()['_FillValue']] = np.nan
print("hdf_array: {}".format(hdf_array))

# %% code 506.
#hdf_array1 = hdf_array.astype(dtype=np.float64)
#print("type(hdf_array1): {}".format(type(hdf_array1)))

#hdf_array1[hdf_array1 == hdf_raw.attributes()['_FillValue']] = np.nan
#print("hdf_array1: {}".format(hdf_array1))

# %% code 507.
#hdf_array = hdf_array.astype(dtype=np.float64)
#for x in range(0, hdf_array.shape[0]):
# for y in range(0, hdf_array.shape[1]):
# if hdf_array[x, y] == hdf_raw.attributes()['_FillValue']:
# hdf_array[x, y] = np.nan

#print("hdf_array: {}".format(hdf_array))

# %% code 508.
hdf_array[hdf_array < hdf_raw.attributes()['valid_range'][0]] = np.nan
hdf_array[hdf_array > hdf_raw.attributes()['valid_range'][1]] = np.nan
print("hdf_array: {}".format(hdf_array))

# %% code 509.
#for x in range(0, hdf_array.shape[0]):
# for y in range(0, hdf_array.shape[1]):
# if hdf_array[x, y] == hdf_raw.attributes()['_FillValue'] \
# or hdf_array[x, y] < hdf_raw.attributes()['valid_range'][0]\
# or hdf_array[x, y] > hdf_raw.attributes()['valid_range'][1]:
# hdf_array[x, y] = np.nan
#print("hdf_array: {}".format(hdf_array))

# %% code 510.
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

# %% code 511.
attrs = hdf_raw.attributes()
print("hdf_raw.attributes()['scale_factor']: {}".format(attrs['scale_factor']))
print("hdf_raw.attributes()['add_offset']: {}".format(attrs['add_offset']))

# %% code 512.
fill_value = hdf_raw.attributes()['_FillValue']
scale_factor = hdf_raw.attributes()['scale_factor']
offset = hdf_raw.attributes()['add_offset']
hdf_value = hdf_array * scale_factor + offset
hdf_value = np.array(hdf_value)
print("hdf_value: {}".format(hdf_value))

# %% code 513.
print("np.shape(hdf_value): {}".format(np.shape(hdf_value)))
print("np.shape(latitude): {}".format(np.shape(latitude)))
print("np.shape(longitude): {}".format(np.shape(longitude)))

print("hdf_value.dtype : {}".format(hdf_value.dtype))
print("latitude.dtype : {}".format(latitude.dtype))
print("longitude.dtype : {}".format(longitude.dtype))

# %% code 514.
import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(8.2, 4.3))

# 히스토그램 그리기(NaN을 뺀 유효한 값만 1차원으로)
valid = hdf_value[~np.isnan(hdf_value)]
plt.hist(valid, bins=50)

# 제목, 축 이름 지정
plt.title("Histogram of {0} \n {1}".format(DATAFIELD_NAME, filename), fontsize=12)
plt.xlabel("AOD at 0.55 µm", fontsize=11)
plt.ylabel("Count", fontsize=11)
plt.tick_params(labelsize=9)

# 주석(annotate) 지정
plt.annotate("mean : {0:.02f}, max: {1:.02f}, min: {2:.02f}".\
            format(np.nanmean(hdf_value), np.nanmax(hdf_value),
                   np.nanmin(hdf_value)),
        xy=(1, 1), xytext=(-12, -12), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points')

plt.annotate("longitude : {0:.01f} ~ {1:.01f}, latitude : {2:.01f} ~ {3:.01f}".\
            format(np.nanmin(longitude), np.nanmax(longitude),
                   np.nanmin(latitude), np.nanmax(latitude)),
        xy=(1, 0.94), xytext=(-12, -12), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points')

print("유효한 AOD 칸: {} / {} ({:.1f}%)".format(valid.size, hdf_value.size,
                                          100 * valid.size / hdf_value.size))
plt.grid(True)
plt.show()

# %% code 515.
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

plt.figure()

#####
# 지도
m = Basemap(projection='cyl')

# 대륙 채우기
m.fillcontinents()

plt.show()

# %% code 516.
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

plt.figure()

#####
# 지도
m = Basemap(projection='mbtfpq',
            lon_0 = 0)

# 대륙 채우기
m.fillcontinents()

plt.show()

# %% code 517.
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

plt.figure()

#####
# 지도
m = Basemap(projection='sinu', 
            lon_0 = 180)

# 대륙 채우기
m.fillcontinents()

plt.show()

# %% code 518.
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

plt.figure(figsize=(6.4, 4.2))

#####
# 지도
m = Basemap(projection = 'lcc',
            lat_1=20.,lat_2=40.,
            lon_0=120.,
            llcrnrlon=100.,llcrnrlat=10.,
            urcrnrlon=180.,urcrnrlat=50.)

# 대륙 채우기
m.fillcontinents()

plt.show()

# %% code 519.
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

plt.figure(figsize=(6.4, 4.2))

#####
# 지도
m = Basemap(projection='laea', 
            lat_ts=37,
            lat_0 = 37, 
            lon_0 = 127,\
            width=1.5e7, height=1.5e7)

# 대륙 채우기
m.fillcontinents()

plt.show()

# %% code 520.
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

# %% code 521.
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

plt.figure(figsize=(4.6, 4.2))

#####
# 지도
m = Basemap(projection='laea', resolution='l', \
            lat_ts=37,
            lat_0 = 37, lon_0 = 127,\
            width=1.5e7, height=1.5e7)

# 해안선 · 국경 그리기, 대륙 채우기
m.drawcoastlines(linewidth=0.25)
m.drawcountries(linewidth=0.25)
m.fillcontinents()

m.drawparallels(np.arange(-90., 90.1, 45.), labels=[1, 0, 1, 0], fontsize=8)
m.drawmeridians(np.arange(-180., 180.1, 45.), labels=[0, 1, 0, 1], fontsize=8)

plt.show()

# %% code 522.
print("np.nanmin(longitude):{}".format(np.nanmin(longitude)))
print("np.nanmax(longitude):{}".format(np.nanmax(longitude))) 
print("np.nanmin(latitude):{}".format(np.nanmin(latitude)))
print("np.nanmax(latitude):{}".format(np.nanmax(latitude)))

# %% code 523.
longitude360 = longitude + 180
latitude180 = latitude + 90

long_center = ((np.nanmax(longitude360) + np.nanmin(longitude360)) / 2) - 180
lat_center = ((np.nanmax(latitude180) + np.nanmin(latitude180)) / 2) - 90

print("long_center:{}".format(long_center))
print("lat_center:{}".format(lat_center))

# %% code 524.
longitude360 = longitude + 180
latitude180 = latitude + 90

Wlon = np.nanmin(longitude360) - 180
Elon = np.nanmax(longitude360) - 180

Slat = np.nanmin(latitude180) - 90
Nlat = np.nanmax(latitude180) - 90

Clon = ((np.nanmax(longitude360) + np.nanmin(longitude360)) / 2) - 180
Clat = ((np.nanmax(latitude180) + np.nanmin(latitude180)) / 2) - 90

print("Wlon: {}".format(Wlon))
print("Elon: {}".format(Elon))
print("Slat: {}".format(Slat))
print("Nlat: {}".format(Nlat))
print("Clon: {}".format(Clon))
print("Clat: {}".format(Clat))

# %% code 525.
def findRangeOfMap(longitude, latitude, idl) :
 ## idl: 날짜 변경선(IDL) 포함 여부
 ## 0(날짜 변경선 포함), 1(날짜 변경선 포함 안 함)
 ## 입력: 위도와 경도의 numpy.array
 ## 출력: 경도와 위도의 동서남북 경계와 중심 좌표(float)
    idl = idl
    longitude360 = longitude + 180
    latitude180 = latitude + 90

    Slat = np.nanmin(latitude180) - 90
    Nlat = np.nanmax(latitude180) - 90
    Clon = ((np.nanmax(longitude360) + np.nanmin(longitude360)) / 2) - 180
    Clat = ((np.nanmax(latitude180) + np.nanmin(latitude180)) / 2) - 90
    if idl == 0 :
        Wlon = np.nanmax(longitude360) - 180
        Elon = np.nanmin(longitude360) - 180
    else : 
        Wlon = np.nanmin(longitude360) - 180
        Elon = np.nanmax(longitude360) - 180
        
    return Wlon, Elon, Slat, Nlat, Clon, Clat   

Wlon, Elon, Slat, Nlat, Clon, Clat = findRangeOfMap(longitude, latitude, 1)

print("Wlon: {}".format(Wlon))
print("Elon: {}".format(Elon))
print("Slat: {}".format(Slat))
print("Nlat: {}".format(Nlat)) 
print("Clon: {}".format(Clon))
print("Clat: {}".format(Clat))

# %% code 526.
Wlon, Elon, Slat, Nlat, Clon, Clat = findRangeOfMap(longitude, latitude, 0)

print("Wlon: {}".format(Wlon))
print("Elon: {}".format(Elon))
print("Slat: {}".format(Slat))
print("Nlat: {}".format(Nlat)) 
print("Clon: {}".format(Clon))
print("Clat: {}".format(Clat))

# 뒤의 지도에서는 이 장면에 맞는 경계(idl=1)를 다시 사용
Wlon, Elon, Slat, Nlat, Clon, Clat = findRangeOfMap(longitude, latitude, 1)

# %% code 527.
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

# %% code 528.
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

plt.show()

# %% code 529.
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
plt.annotate("mean : {0:.02f}, max: {1:.02f}, min: {2:.02f}".\
            format(np.nanmean(hdf_value), np.nanmax(hdf_value),
                   np.nanmin(hdf_value)),
        xy=(0, 0), xytext=(12, -30), va='top',
        xycoords='axes fraction', textcoords='offset points')

plt.annotate("longitude : {0:.01f} ~ {1:.01f}, latitude : {2:.01f} ~ {3:.01f}".\
            format(Wlon, Elon, Slat, Nlat),
        xy=(0, 0), xytext=(12, -44), va='top',
        xycoords='axes fraction', textcoords='offset points')

plt.annotate("filename:{}".format(filename),
        xy=(1, 0), xytext=(12, -58), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points')

plt.show()

# %% code 530.
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

plt.figure(figsize=(4.9, 3.9))

# 지도 표시 범위 찾기
Wlon, Elon, Slat, Nlat, Clon, Clat = findRangeOfMap(longitude, latitude, 1)

#####
# 지도
m = Basemap(projection='laea', 
            lat_ts = Clat,
            lat_0 = Clat, 
            lon_0 = Clon,\
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
plt.annotate("mean : {0:.02f}, max: {1:.02f}, min: {2:.02f}".\
            format(np.nanmean(hdf_value), np.nanmax(hdf_value),
                   np.nanmin(hdf_value)),
        xy=(0, 0), xytext=(12, -22), va='top',
        xycoords='axes fraction', textcoords='offset points', fontsize=8)

plt.annotate("longitude : {0:.01f} ~ {1:.01f}, latitude : {2:.01f} ~ {3:.01f}".\
            format(Wlon, Elon, Slat, Nlat),
        xy=(0, 0), xytext=(12, -33), va='top',
        xycoords='axes fraction', textcoords='offset points', fontsize=8)

plt.annotate("filename:{}".format(filename),
        xy=(1, 0), xytext=(12, -44), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points', fontsize=8)

plt.show()
