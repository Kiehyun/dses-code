# 지구과학 데이터 사이언스 1 | V-01. 세계의 화산대
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 1.
from pathlib import Path

fname = "List_of_Volcanoes_of_the_World_for_VAAC_Use.xls"
fid = "1dmJpAd1RI6LCaoV_iRR72HMeVP8vDoV-"

du.download(f"https://docs.google.com/uc?export=download&id={fid}", Path(proj_dir) / fname)

# %% code 2.
fpaths = du.list_files(proj_dir, "xls")

# %% code 3.
n_lines = 10  # 출력할 줄 수

print(f"파일 내용 출력 (처음 {n_lines}줄):")
print("="*40)

# 순수 파이썬으로 구현 (운영체제 무관)
try:
    with open(fpaths[0], encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= n_lines:
                break
            print(f"{i+1:3d}: {line.rstrip()}")
except UnicodeDecodeError:
 # UTF-8로 읽기 실패시 다른 인코딩 시도
    try:
        with open(fpaths[0], encoding='cp949') as f:
            for i, line in enumerate(f):
                if i >= n_lines:
                    break
                print(f"{i+1:3d}: {line.rstrip()}")
    except Exception as e2:
        print(f"파일 읽기 실패 (UTF-8, CP949 모두 실패): {e2}")
except Exception as e:
    print(f"파일 읽기 실패: {e}")

print("="*60)

# %% code 4.
import pandas as pd
import lxml.etree as ET

# XML 파싱
tree = ET.parse(fpaths[0])  # fpaths[0]은 XML 파일 경로입니다.
ns = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"}

# Row 추출
rows = tree.xpath("//ss:Row", namespaces=ns)

# Row별 Cell의 Data 추출
data = []
for row in rows:
    row_data = [cell.text for cell in row.xpath(".//ss:Cell/ss:Data", namespaces=ns)]
    data.append(row_data)

# DataFrame 생성
df_vol = pd.DataFrame(data)

# 두 번째 Row를 컬럼명으로 지정하고, 메타 데이터와 헤더 Row 제거
df_vol.columns = df_vol.iloc[1]
df_vol = df_vol.drop([0, 1]).reset_index(drop=True)

# 자료형 변환 시도 (예: 숫자형으로 변환 가능한 경우 변환)
for col in df_vol.columns:
    df_vol[col] = pd.to_numeric(df_vol[col], errors='coerce').fillna(df_vol[col])

# 데이터 확인
print("df_vol :", df_vol)

# %% code 5.
df_vol.columns

# %% code 6.
df_vol['Latitude'] = df_vol['LatitudeDecimal']
df_vol['Longitude'] = df_vol['LongitudeDecimal']
print(df_vol[['Latitude', 'Longitude']])

# %% code 7.
import matplotlib.pyplot as plt
import numpy as np

# 화산 위치 산점도
plt.scatter(df_vol['Longitude'], df_vol['Latitude'], 
            c='red', s=15, alpha=0.6, marker='^', 
            edgecolors='darkred', linewidth=0.3)

# 지도 설정
plt.xlim(-180, 180)  # 경도 범위 설정 (-180도 ~ 180도)
plt.ylim(-90, 90)    # 위도 범위 설정 (-90도 ~ 90도)
plt.xlabel('경도', fontsize=12)
plt.ylabel('위도', fontsize=12)
plt.title('전 세계 화산 분포', fontsize=16, fontweight='bold')
plt.grid(True, alpha=0.3)  # 격자 표시

# 기준선 추가 (적도와 본초자오선)
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)  # 적도 (위도 0도)
plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)  # 본초자오선 (경도 0도)

plt.tight_layout()  # 레이아웃 자동 조정
du.save_figure(plt.gcf(), os.path.join(proj_dir, "05_01_Plotting_ring_of_fire_01"))
plt.show()

# %% code 8.
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

# 데이터 확인
print("데이터 샘플:")
print(f"\n총 화산 개수: {len(df_vol)}")

# 그래프 크기 설정
plt.figure(figsize=(12.0, 8.0))

# 원통형 투영법으로 세계지도 생성
m = Basemap(projection='cyl', resolution='c',
            llcrnrlat=-90, urcrnrlat=90,    # 위도 범위: -90도 ~ 90도
            llcrnrlon=-180, urcrnrlon=180)  # 경도 범위: -180도 ~ 180도

# 지도 기본 요소 그리기
m.drawcoastlines(linewidth=0.5)            # 해안선 그리기
m.drawcountries(linewidth=0.5)             # 국경선 그리기
m.drawmapboundary(fill_color='lightblue')  # 지도 경계 및 바다 색상
m.fillcontinents(color='lightgray', lake_color='lightblue')  # 대륙과 호수 색상

# 경위도 격자선 그리기
m.drawparallels(np.arange(-90, 91, 30), labels=[1,0,0,0], fontsize=8)  # 위도선 (30도 간격)
m.drawmeridians(np.arange(-180, 181, 60), labels=[0,0,0,1], fontsize=8) # 경도선 (60도 간격)

# 화산 위치를 지도 좌표계로 변환
x, y = m(df_vol['Longitude'].values, df_vol['Latitude'].values)

# 화산 위치 표시
m.scatter(x, y, c='red', s=20, alpha=0.7, marker='^', 
            edgecolors='darkred', linewidth=0.5, label='화산')

# 그래프 제목 및 범례 설정
plt.title('전 세계 화산 분포도', fontsize=16, fontweight='bold')
plt.legend(loc='lower left')
plt.tight_layout()
du.save_figure(plt.gcf(), os.path.join(proj_dir, "05_01_Plotting_ring_of_fire_02"))
plt.show()

# %% code 9.
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

plt.figure(figsize=(12.0, 6.4))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_global()
ax.coastlines()
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
ax.add_feature(cfeature.BORDERS, linestyle=':')
plt.scatter(df_vol['Longitude'], df_vol['Latitude'], 
            c='red', s=15, alpha=0.6, marker='^', 
            edgecolors='darkred', linewidth=0.3, 
            transform=ccrs.PlateCarree(), label='Volcano')
plt.title('World Volcanoes Distribution (Cartopy)', fontsize=16, fontweight='bold')
plt.legend(loc='lower left')
du.save_figure(plt.gcf(), os.path.join(proj_dir, "05_01_Plotting_ring_of_fire_03"))
plt.show()

# %% code 10.
import folium
from folium.plugins import MarkerCluster
import pandas as pd

# 지도 중심 좌표 (예: 서울 근처)
m = folium.Map(location=[37.5, 127], zoom_start=2, tiles='cartodbpositron')
marker_cluster = MarkerCluster().add_to(m)
for idx, row in df_vol.iterrows():
    lat = row['Latitude']
    lon = row['Longitude']
    name = row['VolcanoName'] if 'VolcanoName' in df_vol.columns else ''
 # NaN 값이 있으면 건너뜀
    if pd.isna(lat) or pd.isna(lon):
        continue
    folium.Marker([lat, lon], popup=name, icon=folium.Icon(color='red', icon='fire')).add_to(marker_cluster)
m.save('world_volcanoes_folium.html')
display(m)

# %% code 11.
import plotly.graph_objects as go
import plotly.express as px

fig = go.Figure()

# 화산 위치 추가
fig.add_trace(go.Scattergeo(
            lon=df_vol['Longitude'],  # 경도 데이터
            lat=df_vol['Latitude'],   # 위도 데이터
            mode='markers',           # 마커 모드로 설정
            marker=dict(
                size=8,                              # 마커 크기
                color='red',                         # 마커 색상 (빨간색)
                symbol='triangle-up',                # 마커 모양 (위쪽 삼각형)
                line=dict(width=1, color='darkred')  # 마커 테두리 설정
            ),
 # 화산 이름이 있으면 텍스트로 표시
            text=df_vol['VolcanoName'] if 'VolcanoName' in df_vol.columns else None,
 # 마우스 호버 시 표시할 정보 템플릿
            hovertemplate='<b>%{text}</b><br>' +
                            'Latitude: %{lat}<br>' +
                            'Longitude: %{lon}<br>' +
                            '<extra></extra>',
            name='Volcanoes'  # 범례에 표시될 이름
        ))

# 지도 레이아웃 설정
fig.update_layout(
        title='World Volcanoes Distribution',  # 지도 제목
        geo=dict(
            showland=True,                        # 육지 표시
            landcolor='rgb(243, 243, 243)',       # 육지 색상 (연한 회색)
            coastlinecolor='rgb(204, 204, 204)',  # 해안선 색상 (회색)
            showocean=True,                       # 바다 표시
            oceancolor='rgb(230, 245, 255)',      # 바다 색상 (연한 파란색)
            projection_type='natural earth'       # 지도 투영법 (자연적 지구 투영)
        ),
        width=800,  # 지도 너비
        height=450  # 지도 높이
    )

fig.show()  # 지도 출력
