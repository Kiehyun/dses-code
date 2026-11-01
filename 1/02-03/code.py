# 지구과학 데이터 사이언스 1 | II-03. 지도 그리기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 22.
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 1행 3열 서브플롯 생성
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12.0, 4.0))

# 첫 번째 지도 (해안선만)
plt.sca(ax1)  # 첫 번째 축을 활성화
m1 = Basemap(projection='ortho', lat_0=90, lon_0=127, ax=ax1)
m1.drawcoastlines()  # 해안선 그리기
ax1.set_title('해안선만 표시')

# 두 번째 지도 (해안선 + 위경도선)
plt.sca(ax2)  # 두 번째 축을 활성화
m2 = Basemap(projection='ortho', lat_0=90, lon_0=127, ax=ax2)
m2.drawcoastlines()                         # 해안선 그리기
m2.drawparallels(np.arange(10, 90, 10))     # 위도선 그리기
m2.drawmeridians(np.arange(-180, 180, 10))  # 경도선 그리기
ax2.set_title('해안선 + 위경도선 표시')

# 세 번째 지도 (lat_0=37로 중심 변경)
plt.sca(ax3)  # 세 번째 축을 활성화
m3 = Basemap(projection='ortho', lat_0=37, lon_0=127, ax=ax3)
m3.drawcoastlines()  # 해안선 그리기
ax3.set_title('중심 위도 37도')

plt.tight_layout()  # 레이아웃 조정
du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_03_Drawing_maps_01"))
plt.show()

# %% code 23.
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

fig = plt.figure(figsize=(12, 4))

# 첫 번째 서브플롯 - ETOPO 지형도
ax1 = fig.add_subplot(1, 3, 1)
m1 = Basemap(projection='ortho', resolution='c', lat_0=37, lon_0=127, ax=ax1)
m1.etopo(scale=0.5, alpha=0.7)  # ETOPO 지형 이미지 (수심/고도 표시)

# 두 번째 서브플롯 - NASA 블루마블 이미지
ax2 = fig.add_subplot(1, 3, 2)
m2 = Basemap(projection='ortho', resolution='c', lat_0=37, lon_0=127, ax=ax2)
m2.bluemarble(scale=0.5, alpha=0.7)  # NASA 블루마블 위성 이미지

# 세 번째 서브플롯 - 음영기복도
ax3 = fig.add_subplot(1, 3, 3)
m3 = Basemap(projection='ortho', resolution='c', lat_0=37, lon_0=127, ax=ax3)
m3.shadedrelief(scale=0.5, alpha=0.7)  # 음영기복 이미지 (지형의 입체감 표현)

plt.tight_layout()  # 서브플롯 간격 자동 조정
plt.show()          # 그래프 출력

# %% code 24.
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(5, 5))
m = Basemap(projection='lcc', width=8E6, height=8E6, 
            lat_0=38, lon_0=127,)
m.etopo(scale=0.5, alpha=0.5)

# 경도·위도를 그림 좌표(x, y)로 변환
x, y = m(127.0, 37.2)
plt.plot(x, y, 'ob', markersize=5)
plt.text(x, y, 'Suwon', fontsize=12)

du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_03_Drawing_maps_02"))
plt.show()

# %% code 25.
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# 1행 2열의 그래프 생성
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 4.8))

# 첫 번째 서브플롯 - 등고선이 있는 직교 투영법
plt.sca(ax1)
map1 = Basemap(projection='ortho',lat_0=45,lon_0=-100,resolution='l')
map1.drawcoastlines(linewidth=0.25)                   # 해안선 그리기
map1.drawcountries(linewidth=0.25)                    # 국경선 그리기
map1.fillcontinents(color='coral',lake_color='aqua')  # 대륙을 산호색으로, 호수를 하늘색으로 채우기
map1.drawmapboundary(fill_color='aqua')               # 지도 경계를 하늘색으로 채우기
map1.drawmeridians(np.arange(0,360,30))               # 경선 그리기 (30도 간격)
map1.drawparallels(np.arange(-90,90,30))              # 위선 그리기 (30도 간격)

# 등고선 데이터 생성
nlats = 73; nlons = 145; delta = 2.*np.pi/(nlons-1)
lats = (0.5*np.pi-delta*np.indices((nlats,nlons))[0,:,:])  # 위도 배열
lons = (delta*np.indices((nlats,nlons))[1,:,:])       # 경도 배열
wave = 0.75*(np.sin(2.*lats)**8*np.cos(4.*lons))      # 파형 데이터
mean = 0.5*np.cos(2.*lats)*((np.sin(2.*lats))**2 + 2.)  # 평균 데이터
x1, y1 = map1(lons*180./np.pi, lats*180./np.pi)       # 좌표 변환
cs = map1.contour(x1,y1,wave+mean,15,linewidths=1.5)  # 등고선 그리기
ax1.set_title('대륙 배경 위의 등고선')

# 두 번째 서브플롯 - 밀러 투영법과 주야 구분
plt.sca(ax2)
map2 = Basemap(projection='mill',lon_0=180)
map2.drawcoastlines()                                 # 해안선 그리기
map2.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])  # 위선과 라벨
map2.drawmeridians(np.arange(map2.lonmin,map2.lonmax+30,60),labels=[0,0,0,1])  # 경선과 라벨
map2.drawmapboundary(fill_color='aqua')               # 지도 경계 하늘색으로 채우기
map2.fillcontinents(color='coral',lake_color='aqua')  # 대륙을 산호색으로, 호수를 하늘색으로 채우기

# 밤 그림자 추가 (현재 시간 기준)
date = datetime.utcnow()    # 현재 UTC 시간
CS = map2.nightshade(date)  # 밤 지역에 그림자 효과
ax2.set_title('%s (UTC) 주야 구분 지도' % date.strftime("%d %b %Y %H:%M:%S"))

# 레이아웃 조정 및 표시
plt.tight_layout()  # 자동 레이아웃 조정
plt.show()          # 그래프 출력

# %% code 26.
from itertools import chain

def draw_map(m, scale=0.2):   # 함수 정의하기
 # 음영 기복도 그리기
    m.shadedrelief(scale=scale)
    
 # 위도와 경도는 딕셔너리로 반환된다
    lats = m.drawparallels(np.linspace(-90, 90, 13))
    lons = m.drawmeridians(np.linspace(-180, 180, 13))

 # 키에는 plt.Line2D 객체가 들어 있다
    lat_lines = chain(*(tup[1][0] for tup in lats.items()))
    lon_lines = chain(*(tup[1][0] for tup in lons.items()))
    all_lines = chain(lat_lines, lon_lines)
    
 # 이 선들을 돌면서 원하는 스타일을 지정한다
    for line in all_lines:
        line.set(linestyle='-', alpha=0.3, color='w')

# %% code 27.
fig, ax = plt.subplots(1, 3, figsize=(10, 5))

for i, res in enumerate(['l', 'i', 'h']):
 # 심사 투영법(gnomonic)으로 지도 생성
 # lat_0, lon_0: 지도 중심 좌표 (서울 근처)
 # width, height: 지도 크기 (미터 단위)
 # resolution: 해안선 해상도 (l=낮음, i=중간, h=높음)
    m = Basemap(projection='gnom', lat_0=37, lon_0=126.5,
                width=100000, height=150000, resolution=res, ax=ax[i])
    
 # 대륙 채우기 (연한 주황색), 호수 색상 (연한 파란색)
    m.fillcontinents(color="#FFDDCC", lake_color='#DDEEFF')
    
 # 지도 경계 채우기 (바다 색상을 연한 파란색으로)
    m.drawmapboundary(fill_color="#DDEEFF")
    
 # 해안선 그리기
    m.drawcoastlines()
    
 # 각 서브플롯의 제목 설정
    ax[i].set_title("해상도='{0}'".format(res));

# %% code 28.
plt.figure(figsize=(8, 6))

loglat = [90, 0, 180, 62]
clog = (loglat[2]+loglat[0])/2
clat = (loglat[3]+loglat[1])/2

m = Basemap(llcrnrlon = loglat[0], llcrnrlat = loglat[1],
            urcrnrlon = loglat[2], urcrnrlat = loglat[3],
            resolution = res, projection = 'aea', 
            lon_0 = clog, lat_0 = clat)
            
m.drawcoastlines(linewidth = 0.25)
m.drawcountries()
m.fillcontinents()

m.drawparallels(np.arange(-90, 90, 10),
                labels=[1, 1, 0, 0])
m.drawmeridians(np.arange(-180, 181, 20),
                labels=[0, 0, 1, 0])
m.drawmeridians(np.arange(-180, 181, 10),
                labels=[0, 0, 0, 1])
plt.title("Weather map\n", fontsize=20)
plt.savefig(f'{proj_dir}/Weather_map.pdf')
plt.show()   

# %% code 29.
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature

# 1행 2열 서브플롯 생성
fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8), subplot_kw={'projection': ccrs.PlateCarree()})

# 첫 번째 서브플롯 (왼쪽)
ax1 = axes[0]
ax1.coastlines(resolution='110m')
ax1.set_title('Simple World Map')

# 두 번째 서브플롯 (오른쪽)
ax2 = axes[1]
ax2.coastlines(resolution='110m')
ax2.add_feature(cfeature.LAND)
ax2.add_feature(cfeature.OCEAN)
ax2.gridlines()
ax2.set_title('Detailed World Map')

# 레이아웃 조정
plt.tight_layout()
du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_03_Drawing_maps_03"))
plt.show()

# %% code 30.
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import cartopy.feature as cfeature

# 그림 크기 설정 (1행 2열로 배치)
fig = plt.figure(figsize=(12.0, 4.8))

# 첫 번째 subplot - 세계 지도
ax1 = plt.subplot(1, 2, 1, projection=ccrs.PlateCarree(central_longitude=180))

# 해안선 그리기
ax1.coastlines(resolution='110m')

#육지 바다 표시하기
ax1.add_feature(cfeature.LAND)
ax1.add_feature(cfeature.OCEAN)

# 위선, 경선 그리기
ax1.gridlines()

#그림 제목 설정
ax1.set_title('World', fontsize=18)

# 위도 경도 tick 설정
ax1.set_xticks([0, 60, 120, 180, 240, 300, 360], crs=ccrs.PlateCarree())
ax1.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax1.xaxis.set_major_formatter(lon_formatter)
ax1.yaxis.set_major_formatter(lat_formatter)

# 두 번째 subplot - 호주 지도
ax2 = plt.subplot(1, 2, 2, projection=ccrs.PlateCarree())

#육지 바다 표시하기
ax2.add_feature(cfeature.LAND)
ax2.add_feature(cfeature.OCEAN)

# 위선, 경선 그리기 (축 레이블 넣기)
ax2.gridlines(draw_labels=True)

# 지도 영역 설정하기
ax2.set_extent([60, 180, -50, 60], ccrs.PlateCarree())

# 지형 배경에 넣기
ax2.stock_img()

# 해안선 그리기
ax2.coastlines(resolution='110m')

# 국경, 호수, 강 넣기
ax2.add_feature(cfeature.BORDERS, linestyle=':')
ax2.add_feature(cfeature.LAKES, alpha=0.9)
ax2.add_feature(cfeature.RIVERS)

#그림 제목 설정
ax2.set_title('Australia', fontsize=18)

# 레이아웃 조정
plt.tight_layout()

du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_03_Drawing_maps_04"))
plt.show()

# %% code 31.
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 그림 크기 설정
fig = plt.figure(figsize=[12, 6])

# 서브플롯 생성
ax1 = fig.add_subplot(1, 2, 1, projection=ccrs.SouthPolarStereo())
ax2 = fig.add_subplot(1, 2, 2, projection=ccrs.SouthPolarStereo(),
                        sharex=ax1, sharey=ax1)
# 서브플롯 간격 조정
fig.subplots_adjust(bottom=0.05, top=0.95,
                    left=0.04, right=0.95, wspace=0.02)

# 지도 영역 설정하기
ax1.set_extent([-180, 180, -90, -60], ccrs.PlateCarree())

# 육지 바다 표시하기
ax1.add_feature(cfeature.LAND)
ax1.add_feature(cfeature.OCEAN)

# 위선, 경선 그리기 (축 레이블 넣기)
ax1.gridlines(draw_labels = True)
ax2.gridlines(draw_labels = True)

# 육지 바다 표시하기
ax2.add_feature(cfeature.LAND)
ax2.add_feature(cfeature.OCEAN)

# 축 좌표계에서 원을 계산하여 지도의 경계로 사용
# 팬/줌을 얼마나 해도 경계는 항상 원형으로 유지됨
theta = np.linspace(0, 2*np.pi, 100)                 # 0부터 2π까지 100개의 점
center, radius = [0.5, 0.5], 0.5                     # 중심점과 반지름 설정
verts = np.vstack([np.sin(theta), np.cos(theta)]).T  # 원의 꼭짓점 좌표 생성
circle = mpath.Path(verts * radius + center)         # 원형 경로 생성

# 두 번째 축에 원형 경계 설정
ax2.set_boundary(circle, transform=ax2.transAxes)

du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_03_Drawing_maps_05"))
plt.show()

# %% code 32.
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

# 그림 크기 설정
fig = plt.figure(figsize=(10, 10))

ax = plt.axes(projection=ccrs.PlateCarree())

#육지 바다 표시하기
ax.add_feature(cfeature.LAND)
#ax.add_feature(cfeature.OCEAN)

# 위선, 경선 그리기
ax.gridlines(draw_labels = True)

# 지도 영역 설정
#####
ax.set_extent([111, 145, 50, 25], ccrs.PlateCarree())

# 해안선 그리기
ax.coastlines(resolution='50m')

#그림 제목 설정
plt.title('Map of the Korea', fontsize=18)

du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_03_Drawing_maps_06"))
plt.show()

# %% code 33.
import folium
from IPython.display import display

# 서울의 좌표(위도: 37.5665, 경도: 126.9780)를 중심으로 하는 기본 지도 생성
basic_map = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# Jupyter 노트북에서 지도를 화면에 표시
display(basic_map)

# %% code 34.
import folium

# 서울의 위도, 경도 좌표 설정
seoul_coords = [37.5665, 126.9780]

# 서울을 중심으로 한 기본 지도 생성 (확대 레벨 12)
basic_map = folium.Map(location=seoul_coords, zoom_start=12)

# 서울 위치에 마커 추가
folium.Marker(
        seoul_coords,        # 마커를 표시할 좌표
        popup='서울특별시',       # 마커 클릭 시 나타나는 팝업 텍스트
        tooltip='대한민국의 수도',  # 마커에 마우스를 올렸을 때 나타나는 툴팁
        icon=folium.Icon(color='red', icon='info-sign')  # 빨간색 정보 아이콘
    ).add_to(basic_map)                        # 생성한 지도에 마커 추가

# 지도를 HTML 파일로 저장하고 화면에 표시
basic_map.save(Path(proj_dir)/'basic_map_of_Seoul.html')  # HTML 파일로 저장
display(basic_map)  # 지도를 화면에 출력

# %% code 35.
def safe_tile_loader():
    """안전한 타일 로딩"""
    location = [37.5665, 126.9780]  # 서울시청 좌표
    
 # 안정적인 타일 서비스들
    safe_tiles = {
        'OpenStreetMap': 'OpenStreetMap',
        'CartoDB_Positron': 'CartoDB positron',
        'CartoDB_DarkMatter': 'CartoDB dark_matter'
    }
    
    maps = {}
    
    for name, tile in safe_tiles.items():
        try:
 # 타일로 지도 생성
            if tile:
                m = folium.Map(location=location, zoom_start=12, tiles=tile)
            else:
                m = folium.Map(location=location, zoom_start=12)
            
 # 마커 추가
            folium.Marker(
                location,
                popup=f'{name} 지도',
                icon=folium.Icon(color='red')
            ).add_to(m)
            
            maps[name] = m
            print(f"✓ {name} 지도 생성 완료")
            
        except Exception as e:
            print(f"✗ {name} 실패: {e}")
    
    return maps

def check_internet_connection():
    """인터넷 연결 확인"""
    import urllib.request
    
    try:
        urllib.request.urlopen('http://www.google.com', timeout=5)
        return True
    except:
        return False

def create_offline_map():
    """오프라인용 기본 지도"""
    location = [37.5665, 126.9780]
    
 # 외부 타일 없는 기본 지도
    m = folium.Map(
        location=location,
        zoom_start=12
    )
    
 # 서울시청 마커
    folium.Marker(
        location,
        popup='서울시청',
        tooltip='Seoul City Hall'
    ).add_to(m)
    
 # 1km 반경 원
    folium.Circle(
        location,
        radius=1000,
        popup='1km 반경',
        color='blue',
        fill=True,
        fillOpacity=0.2
    ).add_to(m)
    
    return m

# 실행
print("인터넷 연결 확인 중...")
if check_internet_connection():
    print("✓ 인터넷 연결됨")
    maps = safe_tile_loader()  # 온라인 지도들 생성
else:
    print("✗ 인터넷 연결 없음 - 오프라인 지도 생성")
    maps = {'Offline': create_offline_map()}  # 오프라인 지도 생성

# 지도들 표시
for name, map_obj in maps.items():
    print(f"\n{name} 지도:")
    display(map_obj)

# %% code 36.
def create_marker_showcase():
    """다양한 마커 스타일을 보여주는 지도"""
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)
    
 # 한국의 주요 관광지 데이터
    tourist_spots = [
        {'name': '경복궁', 'coords': [37.5796, 126.9770], 'color': 'red', 'icon': 'home'},
        {'name': '남산타워', 'coords': [37.5512, 126.9882], 'color': 'blue', 'icon': 'tower'},
        {'name': '한강공원', 'coords': [37.5172, 126.9073], 'color': 'green', 'icon': 'leaf'},
        {'name': '동대문', 'coords': [37.5665, 127.0092], 'color': 'purple', 'icon': 'shopping-cart'},
        {'name': '홍대', 'coords': [37.5563, 126.9236], 'color': 'orange', 'icon': 'music'}
    ]
    
    for spot in tourist_spots:
 # HTML 팝업 내용 생성
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="color: {spot['color']};">{spot['name']}</h4>
            <p><b>위치:</b> {spot['coords'][0]:.4f}, {spot['coords'][1]:.4f}</p>
            <p><b>설명:</b> 서울의 주요 관광명소</p>
        </div>
        """
        
        folium.Marker(
            spot['coords'],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"클릭하면 {spot['name']} 정보를 볼 수 있습니다",
            icon=folium.Icon(color=spot['color'], icon=spot['icon'])
        ).add_to(m)
        
 # 원형 마커도 추가
        folium.CircleMarker(
            spot['coords'],
            radius=15,
            popup=spot['name'],
            color=spot['color'],
            fill=True,
            opacity=0.3
        ).add_to(m)
    
    return m

# 마커 쇼케이스 지도 생성
marker_map = create_marker_showcase()
marker_map.save(Path(proj_dir)/'marker_showcase_map.html')
display(marker_map)

# %% code 37.
import numpy as np

def create_heatmap():
    """히트맵을 생성하는 함수"""
 # 서울 지역의 가상 데이터 생성
    np.random.seed(42)
    
 # 서울 주변 좌표 생성
    n_points = 1000
    lat_center, lon_center = 37.5665, 126.9780
    
 # 정규분포를 따르는 랜덤 좌표 생성
    lats = np.random.normal(lat_center, 0.1, n_points)
    lons = np.random.normal(lon_center, 0.1, n_points)
    
 # 가중치 (인구밀도나 상점 수 등을 시뮬레이션)
    weights = np.random.exponential(2, n_points)
    
 # 히트맵 데이터 준비
    heat_data = [[lat, lon, weight] for lat, lon, weight in zip(lats, lons, weights)]
    
 # 기본 지도 생성
    m = folium.Map(location=[lat_center, lon_center], zoom_start=11)
    
 # 히트맵 레이어 추가
    from folium.plugins import HeatMap
    HeatMap(
        heat_data,
        min_opacity=0.2,
        max_zoom=18,
        radius=15,
        blur=10,
        gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}
    ).add_to(m)
    
    return m

# 히트맵 생성
heatmap = create_heatmap()
heatmap.save(Path(proj_dir)/'heatmap.html')
print("히트맵이 생성되었습니다.")

# 히트맵 표시
display(heatmap)

# %% code 38.
import pandas as pd
def create_choropleth_map():
    """한국 시도별 인구 데이터를 표시하는 코로플레스 지도"""
    
 # 한국 시도별 가상 인구 데이터
    population_data = {
        '서울특별시': 9720846,
        '경기도': 13427014,
        '인천광역시': 2955024,
        '강원도': 1536270,
        '충청북도': 1612801,
        '충청남도': 2118183,
        '대전광역시': 1475221,
        '세종특별자치시': 340575,
        '전라북도': 1792476,
        '전라남도': 1838353,
        '광주광역시': 1441970,
        '경상북도': 2675564,
        '경상남도': 3364660,
        '대구광역시': 2410700,
        '울산광역시': 1124459,
        '부산광역시': 3413841,
        '제주특별자치도': 672948
    }
    
 # 데이터프레임으로 변환
    df = pd.DataFrame(list(population_data.items()), columns=['지역', '인구수'])
    
 # 한국 지도 중심 좌표
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)
    
 # 간단한 원형 마커로 인구 비례 표시 (GeoJSON이 없는 경우의 대안)
 # 실제로는 한국 행정구역 GeoJSON 파일이 필요합니다
    
 # 시도별 대략적 중심 좌표 (임의 설정)
    region_coords = {
        '서울특별시': [37.5665, 126.9780],
        '경기도': [37.4138, 127.5183],
        '인천광역시': [37.4563, 126.7052],
        '강원도': [37.8228, 128.1555],
        '충청북도': [36.6357, 127.4917],
        '충청남도': [36.5184, 126.8000],
        '대전광역시': [36.3504, 127.3845],
        '세종특별자치시': [36.4800, 127.2890],
        '전라북도': [35.7175, 127.1530],
        '전라남도': [34.8679, 126.9910],
        '광주광역시': [35.1595, 126.8526],
        '경상북도': [36.4919, 128.8889],
        '경상남도': [35.4606, 128.2132],
        '대구광역시': [35.8714, 128.6014],
        '울산광역시': [35.5384, 129.3114],
        '부산광역시': [35.1796, 129.0756],
        '제주특별자치도': [33.4996, 126.5312]
    }
    
 # 인구수에 비례하는 크기와 색상으로 원형 마커 생성
    max_pop = max(population_data.values())
    min_pop = min(population_data.values())
    
    for region, population in population_data.items():
        if region in region_coords:
            coords = region_coords[region]
            
 # 인구수에 비례한 반지름 (10-50 사이)
            radius = 10 + (population - min_pop) / (max_pop - min_pop) * 40
            
 # 인구수에 따른 색상 결정
            if population > 8000000:
                color = 'darkred'
            elif population > 4000000:
                color = 'red'
            elif population > 2000000:
                color = 'orange'
            elif population > 1000000:
                color = 'yellow'
            else:
                color = 'lightgreen'
            
            popup_text = f"""
            <div style="font-family: Arial;">
                <h4>{region}</h4>
                <p><b>인구수:</b> {population:,}명</p>
                <p><b>비율:</b> {population/sum(population_data.values())*100:.1f}%</p>
            </div>
            """
            
            folium.CircleMarker(
                coords,
                radius=radius,
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=f'{region}: {population:,}명',
                color='black',
                weight=1,
                fill=True,
                fillColor=color,
                fillOpacity=0.7
            ).add_to(m)
    
 # 범례 추가 (HTML로 구현)
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 150px; height: 120px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <p><b>인구수 범례</b></p>
    <p><i class="fa fa-circle" style="color:darkred"></i> 800만명 이상</p>
    <p><i class="fa fa-circle" style="color:red"></i> 400-800만명</p>
    <p><i class="fa fa-circle" style="color:orange"></i> 200-400만명</p>
    <p><i class="fa fa-circle" style="color:yellow"></i> 100-200만명</p>
    <p><i class="fa fa-circle" style="color:lightgreen"></i> 100만명 미만</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m

# 코로플레스 지도 생성
choropleth_map = create_choropleth_map()
choropleth_map.save(Path(proj_dir)/'choropleth_map.html')
print("코로플레스 지도가 생성되었습니다.")
# 코로플레스 지도 표시
display(choropleth_map) 
