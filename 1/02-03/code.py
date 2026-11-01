# 지구과학 데이터 사이언스 1 | II-03. 지도 그리기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 22.
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12.0, 4.0))

plt.sca(ax1)  # 현재 축으로 지정
m1 = Basemap(projection='ortho', lat_0=90, lon_0=127, ax=ax1)  # 정사 도법, 북극 중심
m1.drawcoastlines()
ax1.set_title('해안선만 표시')

plt.sca(ax2)
m2 = Basemap(projection='ortho', lat_0=90, lon_0=127, ax=ax2)
m2.drawcoastlines()
m2.drawparallels(np.arange(10, 90, 10))     # 위도선 10° 간격
m2.drawmeridians(np.arange(-180, 180, 10))  # 경도선 10° 간격
ax2.set_title('해안선 + 위경도선 표시')

plt.sca(ax3)
m3 = Basemap(projection='ortho', lat_0=37, lon_0=127, ax=ax3)
m3.drawcoastlines()
ax3.set_title('중심 위도 37도')

plt.tight_layout()
du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_03_Drawing_maps_01"))
plt.show()

# %% code 23.
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

fig = plt.figure(figsize=(12, 4))

# ETOPO 지형도(고도 · 수심)
ax1 = fig.add_subplot(1, 3, 1)
m1 = Basemap(projection='ortho', resolution='c', lat_0=37, lon_0=127, ax=ax1)
m1.etopo(scale=0.5, alpha=0.7)

# NASA 블루마블 위성 영상
ax2 = fig.add_subplot(1, 3, 2)
m2 = Basemap(projection='ortho', resolution='c', lat_0=37, lon_0=127, ax=ax2)
m2.bluemarble(scale=0.5, alpha=0.7)

# 음영기복도
ax3 = fig.add_subplot(1, 3, 3)
m3 = Basemap(projection='ortho', resolution='c', lat_0=37, lon_0=127, ax=ax3)
m3.shadedrelief(scale=0.5, alpha=0.7)

plt.tight_layout()
plt.show()

# %% code 24.
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(5, 5))
m = Basemap(projection='lcc', width=8E6, height=8E6,  # 람베르트 정각원추 도법, 8000 km 범위
            lat_0=38, lon_0=127,)
m.etopo(scale=0.5, alpha=0.5)

# 경도 · 위도를 그림 좌표(x, y)로 변환
x, y = m(127.0, 37.2)  # 수원
plt.plot(x, y, 'ob', markersize=5)
plt.text(x, y, 'Suwon', fontsize=12)

du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_03_Drawing_maps_02"))
plt.show()

# %% code 25.
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 4.8))

# 1) 정사 도법 + 등고선
plt.sca(ax1)
map1 = Basemap(projection='ortho',lat_0=45,lon_0=-100,resolution='l')
map1.drawcoastlines(linewidth=0.25)
map1.drawcountries(linewidth=0.25)
map1.fillcontinents(color='coral',lake_color='aqua')
map1.drawmapboundary(fill_color='aqua')  # 바다 색
map1.drawmeridians(np.arange(0,360,30))
map1.drawparallels(np.arange(-90,90,30))

# 등고선용 가상 자료(위도 · 경도 격자, 라디안)
nlats = 73; nlons = 145; delta = 2.*np.pi/(nlons-1)
lats = (0.5*np.pi-delta*np.indices((nlats,nlons))[0,:,:])
lons = (delta*np.indices((nlats,nlons))[1,:,:])
wave = 0.75*(np.sin(2.*lats)**8*np.cos(4.*lons))
mean = 0.5*np.cos(2.*lats)*((np.sin(2.*lats))**2 + 2.)
x1, y1 = map1(lons*180./np.pi, lats*180./np.pi)       # 라디안 → 도 → 지도 좌표
cs = map1.contour(x1,y1,wave+mean,15,linewidths=1.5)  # 등고선 15개
ax1.set_title('대륙 배경 위의 등고선')

# 2) 밀러 도법 + 낮밤 경계
plt.sca(ax2)
map2 = Basemap(projection='mill',lon_0=180)
map2.drawcoastlines()
map2.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])  # 왼쪽에 위도 표시
map2.drawmeridians(np.arange(map2.lonmin,map2.lonmax+30,60),labels=[0,0,0,1])  # 아래쪽에 경도 표시
map2.drawmapboundary(fill_color='aqua')
map2.fillcontinents(color='coral',lake_color='aqua')

date = datetime.utcnow()    # 현재 UTC 시각
CS = map2.nightshade(date)  # 밤 지역에 그림자
ax2.set_title('%s (UTC) 주야 구분 지도' % date.strftime("%d %b %Y %H:%M:%S"))

plt.tight_layout()
plt.show()

# %% code 26.
from itertools import chain

def draw_map(m, scale=0.2):
    m.shadedrelief(scale=scale)
    
    # 위도와 경도는 딕셔너리로 반환된다
    lats = m.drawparallels(np.linspace(-90, 90, 13))
    lons = m.drawmeridians(np.linspace(-180, 180, 13))

    # 딕셔너리 값에 plt.Line2D 객체가 들어 있다
    lat_lines = chain(*(tup[1][0] for tup in lats.items()))
    lon_lines = chain(*(tup[1][0] for tup in lons.items()))
    all_lines = chain(lat_lines, lon_lines)
    
    # 이 선들을 돌면서 원하는 스타일을 지정한다
    for line in all_lines:
        line.set(linestyle='-', alpha=0.3, color='w')

# %% code 27.
fig, ax = plt.subplots(1, 3, figsize=(10, 5))

for i, res in enumerate(['l', 'i', 'h']):  # 해안선 해상도: 낮음 · 중간 · 높음
    # 심사 도법(gnomonic), 서울 부근 중심, 폭 · 높이 단위 m
    m = Basemap(projection='gnom', lat_0=37, lon_0=126.5,
                width=100000, height=150000, resolution=res, ax=ax[i])
    
    m.fillcontinents(color="#FFDDCC", lake_color='#DDEEFF')
    
    m.drawmapboundary(fill_color="#DDEEFF")  # 바다 색
    
    m.drawcoastlines()
    
    ax[i].set_title("해상도='{0}'".format(res));

# %% code 28.
plt.figure(figsize=(8, 6))

loglat = [90, 0, 180, 62]  # 왼쪽 아래 경도 · 위도, 오른쪽 위 경도 · 위도
clog = (loglat[2]+loglat[0])/2
clat = (loglat[3]+loglat[1])/2

m = Basemap(llcrnrlon = loglat[0], llcrnrlat = loglat[1],
            urcrnrlon = loglat[2], urcrnrlat = loglat[3],
            resolution = res, projection = 'aea',  # res는 앞 셀의 'h', aea: 앨버스 정적원추 도법
            lon_0 = clog, lat_0 = clat)
            
m.drawcoastlines(linewidth = 0.25)
m.drawcountries()
m.fillcontinents()

m.drawparallels(np.arange(-90, 90, 10), labels=[1, 1, 0, 0])
m.drawmeridians(np.arange(-180, 181, 20), labels=[0, 0, 1, 0])
m.drawmeridians(np.arange(-180, 181, 10), labels=[0, 0, 0, 1])
plt.title("Weather map\n", fontsize=20)
plt.savefig(f'{proj_dir}/Weather_map.pdf')
plt.show()   

# %% code 29.
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature

fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8), subplot_kw={'projection': ccrs.PlateCarree()})  # 정거 원통 도법

ax1 = axes[0]
ax1.coastlines(resolution='110m')
ax1.set_title('Simple World Map')

ax2 = axes[1]
ax2.coastlines(resolution='110m')
ax2.add_feature(cfeature.LAND)
ax2.add_feature(cfeature.OCEAN)
ax2.gridlines()
ax2.set_title('Detailed World Map')

plt.tight_layout()
du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_03_Drawing_maps_03"))
plt.show()

# %% code 30.
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import cartopy.feature as cfeature

fig = plt.figure(figsize=(12.0, 4.8))

# 1) 세계 지도(경도 180° 중심)
ax1 = plt.subplot(1, 2, 1, projection=ccrs.PlateCarree(central_longitude=180))

ax1.coastlines(resolution='110m')

ax1.add_feature(cfeature.LAND)
ax1.add_feature(cfeature.OCEAN)

ax1.gridlines()

ax1.set_title('World', fontsize=18)

# 경위도 눈금과 표기 형식
ax1.set_xticks([0, 60, 120, 180, 240, 300, 360], crs=ccrs.PlateCarree())
ax1.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax1.xaxis.set_major_formatter(lon_formatter)
ax1.yaxis.set_major_formatter(lat_formatter)

# 2) 호주 지도
ax2 = plt.subplot(1, 2, 2, projection=ccrs.PlateCarree())

ax2.add_feature(cfeature.LAND)
ax2.add_feature(cfeature.OCEAN)

ax2.gridlines(draw_labels=True)  # 위경도 표기

ax2.set_extent([60, 180, -50, 60], ccrs.PlateCarree())  # [서쪽 경도, 동쪽 경도, 남쪽 위도, 북쪽 위도]

ax2.stock_img()  # 지형 배경 이미지

ax2.coastlines(resolution='110m')

ax2.add_feature(cfeature.BORDERS, linestyle=':')
ax2.add_feature(cfeature.LAKES, alpha=0.9)
ax2.add_feature(cfeature.RIVERS)

ax2.set_title('Australia', fontsize=18)

plt.tight_layout()

du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_03_Drawing_maps_04"))
plt.show()

# %% code 31.
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeature

fig = plt.figure(figsize=[12, 6])

ax1 = fig.add_subplot(1, 2, 1, projection=ccrs.SouthPolarStereo())  # 남극 중심 평사 도법
ax2 = fig.add_subplot(1, 2, 2, projection=ccrs.SouthPolarStereo(),
                        sharex=ax1, sharey=ax1)
fig.subplots_adjust(bottom=0.05, top=0.95, left=0.04, right=0.95, wspace=0.02)

ax1.set_extent([-180, 180, -90, -60], ccrs.PlateCarree())  # 남위 60° 이남

ax1.add_feature(cfeature.LAND)
ax1.add_feature(cfeature.OCEAN)

ax1.gridlines(draw_labels = True)
ax2.gridlines(draw_labels = True)

ax2.add_feature(cfeature.LAND)
ax2.add_feature(cfeature.OCEAN)

# 축 좌표(0~1)로 원을 만들어 지도 경계로 사용: 확대 · 이동해도 원형 유지
theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)

ax2.set_boundary(circle, transform=ax2.transAxes)

du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_03_Drawing_maps_05"))
plt.show()

# %% code 32.
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10, 10))

ax = plt.axes(projection=ccrs.PlateCarree())

ax.add_feature(cfeature.LAND)
# ax.add_feature(cfeature.OCEAN)

ax.gridlines(draw_labels = True)

ax.set_extent([111, 145, 25, 50], ccrs.PlateCarree())  # 경도 111~145°, 위도 25~50°

ax.coastlines(resolution='50m')  # 1:5천만 축척 해안선

plt.title('Map of the Korea', fontsize=18)

du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_03_Drawing_maps_06"))
plt.show()

# %% code 33.
import folium
from IPython.display import display

basic_map = folium.Map(location=[37.5665, 126.9780], zoom_start=12)  # 서울 중심, [위도, 경도] 순서

display(basic_map)

# %% code 34.
import folium

seoul_coords = [37.5665, 126.9780]  # 서울(위도, 경도)

basic_map = folium.Map(location=seoul_coords, zoom_start=12)  # 확대 수준 12

folium.Marker(
        seoul_coords,
        popup='서울특별시',       # 클릭하면 보이는 글
        tooltip='대한민국의 수도',  # 마우스를 올리면 보이는 글
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(basic_map)

basic_map.save(Path(proj_dir)/'basic_map_of_Seoul.html')  # HTML 파일로 저장
display(basic_map)

# %% code 35.
def safe_tile_loader():
    """안전한 타일 로딩"""
    location = [37.5665, 126.9780]  # 서울시청 좌표
    
    # 배경 지도 타일 서비스
    safe_tiles = {
        'OpenStreetMap': 'OpenStreetMap',
        'CartoDB_Positron': 'CartoDB positron',
        'CartoDB_DarkMatter': 'CartoDB dark_matter'
    }
    
    maps = {}
    
    for name, tile in safe_tiles.items():
        try:
            if tile:
                m = folium.Map(location=location, zoom_start=12, tiles=tile)
            else:
                m = folium.Map(location=location, zoom_start=12)
            
            folium.Marker(
                location, popup=f'{name} 지도', icon=folium.Icon(color='red')
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
    
    m = folium.Map(location=location, zoom_start=12)
    
    folium.Marker(
        location, popup='서울시청', tooltip='Seoul City Hall'
    ).add_to(m)
    
    folium.Circle(
        location,
        radius=1000,  # m
        popup='1km 반경',
        color='blue',
        fill=True,
        fillOpacity=0.2
    ).add_to(m)
    
    return m

print("인터넷 연결 확인 중...")
if check_internet_connection():
    print("✓ 인터넷 연결됨")
    maps = safe_tile_loader()
else:
    print("✗ 인터넷 연결 없음 - 오프라인 지도 생성")
    maps = {'Offline': create_offline_map()}

for name, map_obj in maps.items():
    print(f"\n{name} 지도:")
    display(map_obj)

# %% code 36.
def create_marker_showcase():
    """다양한 마커 스타일을 보여주는 지도"""
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)
    
    # 서울의 주요 관광지(위도, 경도)
    tourist_spots = [
        {'name': '경복궁', 'coords': [37.5796, 126.9770], 'color': 'red', 'icon': 'home'},
        {'name': '남산타워', 'coords': [37.5512, 126.9882], 'color': 'blue', 'icon': 'tower'},
        {'name': '한강공원', 'coords': [37.5172, 126.9073], 'color': 'green', 'icon': 'leaf'},
        {'name': '동대문', 'coords': [37.5665, 127.0092], 'color': 'purple', 'icon': 'shopping-cart'},
        {'name': '홍대', 'coords': [37.5563, 126.9236], 'color': 'orange', 'icon': 'music'}
    ]
    
    for spot in tourist_spots:
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="color: {spot['color']};">{spot['name']}</h4>
            <p><b>위치:</b> {spot['coords'][0]:.4f}, {spot['coords'][1]:.4f}</p>
            <p><b>설명:</b> 서울의 주요 관광명소</p>
        </div>
        """
        
        folium.Marker(
            spot['coords'], popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"클릭하면 {spot['name']} 정보를 볼 수 있습니다",
            icon=folium.Icon(color=spot['color'], icon=spot['icon'])
        ).add_to(m)
        
        folium.CircleMarker(
            spot['coords'], radius=15, popup=spot['name'],
            color=spot['color'], fill=True, opacity=0.3
        ).add_to(m)
    
    return m

marker_map = create_marker_showcase()
marker_map.save(Path(proj_dir)/'marker_showcase_map.html')
display(marker_map)

# %% code 37.
import numpy as np

def create_heatmap():
    """히트맵을 생성하는 함수"""
    # 서울 주변 가상 자료
    np.random.seed(42)  # 난수 고정
    
    n_points = 1000
    lat_center, lon_center = 37.5665, 126.9780  # 서울
    
    # 중심에서 표준편차 0.1°로 흩어진 좌표
    lats = np.random.normal(lat_center, 0.1, n_points)
    lons = np.random.normal(lon_center, 0.1, n_points)
    
    weights = np.random.exponential(2, n_points)  # 가중치(인구밀도 등을 흉내)
    
    heat_data = [[lat, lon, weight] for lat, lon, weight in zip(lats, lons, weights)]
    
    m = folium.Map(location=[lat_center, lon_center], zoom_start=11)
    
    from folium.plugins import HeatMap
    HeatMap(
        heat_data, min_opacity=0.2, max_zoom=18, radius=15, blur=10,
        gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}
    ).add_to(m)
    
    return m

heatmap = create_heatmap()
heatmap.save(Path(proj_dir)/'heatmap.html')
print("히트맵이 생성되었습니다.")

display(heatmap)

# %% code 38.
import pandas as pd
def create_choropleth_map():
    """한국 시도별 인구 데이터를 표시하는 코로플레스 지도"""
    
    # 시도별 인구(가상 자료)
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
    
    df = pd.DataFrame(list(population_data.items()), columns=['지역', '인구수'])
    
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)  # 남한 중심(위도, 경도)
    
    # 행정구역 GeoJSON 파일 대신 원 크기로 인구를 나타냄
    
    # 시도별 대략적 중심 좌표(위도, 경도)
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
    
    max_pop = max(population_data.values())
    min_pop = min(population_data.values())
    
    for region, population in population_data.items():
        if region in region_coords:
            coords = region_coords[region]
            
            # 반지름: 인구에 비례해 10 ~ 50
            radius = 10 + (population - min_pop) / (max_pop - min_pop) * 40
            
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
                coords, radius=radius,
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=f'{region}: {population:,}명', color='black',
                weight=1, fill=True, fillColor=color, fillOpacity=0.7
            ).add_to(m)
    
    # 범례(HTML)
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

choropleth_map = create_choropleth_map()
choropleth_map.save(Path(proj_dir)/'choropleth_map.html')
print("코로플레스 지도가 생성되었습니다.")
display(choropleth_map) 
