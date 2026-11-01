# 지구과학 데이터 사이언스 1 | V-01. 세계의 화산대
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 1.
from pathlib import Path

# 세계 화산 목록(VAAC용) 엑셀 파일, 구글 드라이브 파일 ID
fname = "List_of_Volcanoes_of_the_World_for_VAAC_Use.xls"
fid = "1dmJpAd1RI6LCaoV_iRR72HMeVP8vDoV-"

du.download(f"https://docs.google.com/uc?export=download&id={fid}", Path(proj_dir) / fname)

# %% code 2.
fpaths = du.list_files(proj_dir, "xls")

# %% code 3.
n_lines = 10  # 출력할 줄 수

print(f"파일 내용 출력 (처음 {n_lines}줄):")
print("="*40)

# UTF-8로 읽고, 안 되면 CP949로 다시 시도
try:
    with open(fpaths[0], encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= n_lines:
                break
            print(f"{i+1:3d}: {line.rstrip()}")
except UnicodeDecodeError:
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

# 1) 엑셀 2003 XML(SpreadsheetML) 파일 파싱
tree = ET.parse(fpaths[0])
ns = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"}  # 엑셀 XML 이름공간

# 2) 행(Row)마다 셀 값 추출
rows = tree.xpath("//ss:Row", namespaces=ns)

data = []
for row in rows:
    row_data = [cell.text for cell in row.xpath(".//ss:Cell/ss:Data", namespaces=ns)]
    data.append(row_data)

# 3) DataFrame으로 변환
df_vol = pd.DataFrame(data)

# 둘째 행을 열 이름으로, 앞 두 행(메타 정보 · 머리글)은 제거
df_vol.columns = df_vol.iloc[1]
df_vol = df_vol.drop([0, 1]).reset_index(drop=True)

# 4) 숫자로 바꿀 수 있는 열은 숫자형으로
for col in df_vol.columns:
    df_vol[col] = pd.to_numeric(df_vol[col], errors='coerce').fillna(df_vol[col])

print("df_vol :", df_vol)

# %% code 5.
df_vol.columns

# %% code 6.
# 십진 도(°) 단위 위도 · 경도를 짧은 열 이름으로
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

# 축 범위 · 기준선
plt.xlim(-180, 180)  # 경도(°)
plt.ylim(-90, 90)    # 위도(°)
plt.xlabel('경도', fontsize=12)
plt.ylabel('위도', fontsize=12)
plt.title('전 세계 화산 분포', fontsize=16, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)  # 적도(위도 0°)
plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)  # 본초자오선(경도 0°)

plt.tight_layout()
du.save_figure(plt.gcf(), os.path.join(proj_dir, "05_01_Plotting_ring_of_fire_01"))
plt.show()

# %% code 8.
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

print("데이터 샘플:")
print(f"\n총 화산 개수: {len(df_vol)}")

plt.figure(figsize=(12.0, 8.0))

# 원통 도법(cyl) 세계 지도
m = Basemap(projection='cyl', resolution='c',
            llcrnrlat=-90, urcrnrlat=90,    # 왼쪽 아래 · 오른쪽 위 모서리의 위도
            llcrnrlon=-180, urcrnrlon=180)  # 같은 모서리의 경도

# 지도 기본 요소 그리기
m.drawcoastlines(linewidth=0.5)
m.drawcountries(linewidth=0.5)
m.drawmapboundary(fill_color='lightblue')  # 바다 색
m.fillcontinents(color='lightgray', lake_color='lightblue')

m.drawparallels(np.arange(-90, 91, 30), labels=[1,0,0,0], fontsize=8)  # 30° 간격, 왼쪽 눈금
m.drawmeridians(np.arange(-180, 181, 60), labels=[0,0,0,1], fontsize=8)  # 60° 간격, 아래 눈금

# 경위도 → 지도 좌표
x, y = m(df_vol['Longitude'].values, df_vol['Latitude'].values)

m.scatter(x, y, c='red', s=20, alpha=0.7, marker='^', 
            edgecolors='darkred', linewidth=0.5, label='화산')

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
ax = plt.axes(projection=ccrs.PlateCarree())  # 정거 원통 도법
ax.set_global()                               # 지구 전체
ax.coastlines()
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
ax.add_feature(cfeature.BORDERS, linestyle=':')
plt.scatter(df_vol['Longitude'], df_vol['Latitude'], 
            c='red', s=15, alpha=0.6, marker='^', 
            edgecolors='darkred', linewidth=0.3, 
            transform=ccrs.PlateCarree(), label='Volcano')  # 자료 좌표: 경위도
plt.title('World Volcanoes Distribution (Cartopy)', fontsize=16, fontweight='bold')
plt.legend(loc='lower left')
du.save_figure(plt.gcf(), os.path.join(proj_dir, "05_01_Plotting_ring_of_fire_03"))
plt.show()

# %% code 10.
import folium
from folium.plugins import MarkerCluster
import pandas as pd

# 지도 중심: 서울 부근(위도 37.5°, 경도 127°)
m = folium.Map(location=[37.5, 127], zoom_start=2, tiles='cartodbpositron')
marker_cluster = MarkerCluster().add_to(m)  # 가까운 마커끼리 묶어 표시
for idx, row in df_vol.iterrows():
    lat = row['Latitude']
    lon = row['Longitude']
    name = row['VolcanoName'] if 'VolcanoName' in df_vol.columns else ''
    # 위경도가 없는 화산은 건너뜀
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
            lon=df_vol['Longitude'],
            lat=df_vol['Latitude'],
            mode='markers',
            marker=dict(
                size=8,
                color='red',
                symbol='triangle-up',
                line=dict(width=1, color='darkred')
            ),
            # 화산 이름(없으면 생략)
            text=df_vol['VolcanoName'] if 'VolcanoName' in df_vol.columns else None,
            # 마우스를 올렸을 때 보일 정보
            hovertemplate='<b>%{text}</b><br>' +
                            'Latitude: %{lat}<br>' +
                            'Longitude: %{lon}<br>' +
                            '<extra></extra>',
            name='Volcanoes'
        ))

# 지도 레이아웃 설정
fig.update_layout(
        title='World Volcanoes Distribution',
        geo=dict(
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
            showocean=True,
            oceancolor='rgb(230, 245, 255)',
            projection_type='natural earth'  # 지도 도법
        ),
        width=800,  # 그림 크기(픽셀)
        height=450
    )

fig.show()
