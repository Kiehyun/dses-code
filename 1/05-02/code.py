# 지구과학 데이터 사이언스 1 | V-02. 세계의 지진대
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 14.
proj_dir = du.make_project_dir(du.current_notebook_name() or "05_02_Visualizing_Global_Seismic_Belts")

# %% code 15.
import requests

# 분석에 사용할 USGS GeoJSON 파일을 확인합니다.
# 폴더에 JSON 파일이 없으면 공개 USGS feed에서 직접 다운로드합니다.
proj_dir.mkdir(parents=True, exist_ok=True)

usgs_feeds = {
    "01_usgs_all_month.geojson": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson",
    "02_usgs_4.5_month.geojson": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_month.geojson",
}

for filename, url in usgs_feeds.items():
    outpath = proj_dir / filename
    if not outpath.exists():
        print(f"다운로드 중: {url}")
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        outpath.write_text(response.text, encoding="utf-8")
        print(f"저장 완료: {outpath}")

fpaths = sorted(proj_dir.glob("*.geojson")) + sorted(proj_dir.glob("*.json"))
# 같은 파일이 두 번 잡히지 않도록 중복을 제거합니다.
fpaths = list(dict.fromkeys(fpaths))

if len(fpaths) == 0:
    raise FileNotFoundError(f"{proj_dir} 폴더에서 JSON/GeoJSON 파일을 찾지 못했습니다.")

print(f"fpaths: {fpaths}")
print(f"len(fpaths): {len(fpaths)}")

# %% code 16.
du.preview_text(fpaths[0], n=10)

# %% code 17.
import pandas as pd
import json

def earthquake_json_to_dataframe(json_path):
    """USGS GeoJSON 또는 일반 JSON 지진 자료를 DataFrame으로 변환합니다."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # USGS GeoJSON feed는 features 리스트 안에 properties와 geometry를 저장합니다.
    if isinstance(data, dict) and "features" in data:
        rows = []
        for feature in data["features"]:
            props = feature.get("properties", {}) or {}
            coords = (feature.get("geometry", {}) or {}).get("coordinates", [None, None, None])
            row = dict(props)
            row["longitude"] = coords[0] if len(coords) > 0 else None
            row["latitude"] = coords[1] if len(coords) > 1 else None
            row["depth"] = coords[2] if len(coords) > 2 else None
            rows.append(row)
        df_out = pd.DataFrame(rows)
    elif isinstance(data, dict) and "items" in data:
        df_out = pd.DataFrame(data["items"])
    elif isinstance(data, dict) and "earthquakes" in data:
        df_out = pd.DataFrame(data["earthquakes"])
    elif isinstance(data, list):
        df_out = pd.DataFrame(data)
    else:
        df_out = pd.DataFrame(data)

    # 뒤쪽 시각화 셀에서 magnitude와 mag를 모두 쓸 수 있도록 열 이름을 맞춥니다.
    if "mag" in df_out.columns and "magnitude" not in df_out.columns:
        df_out["magnitude"] = df_out["mag"]
    if "magnitude" in df_out.columns and "mag" not in df_out.columns:
        df_out["mag"] = df_out["magnitude"]

    # 시간은 USGS에서 밀리초 단위 Unix time으로 제공되므로 사람이 읽는 시간도 추가합니다.
    if "time" in df_out.columns:
        df_out["time_utc"] = pd.to_datetime(df_out["time"], unit="ms", utc=True, errors="coerce")

    return df_out, data

# 첫 번째 JSON/GeoJSON 파일을 표로 변환합니다.
df, data = earthquake_json_to_dataframe(fpaths[0])

print(f"파일명: {fpaths[0].name}")

# %% code 18.
# 앞 셀에서 만든 DataFrame을 확인합니다.
# USGS GeoJSON의 properties와 geometry에서 위도, 경도, 깊이, 규모를 추출했습니다.
print(f"파일명: {fpaths[0].name}")
print(f"데이터프레임 크기: {df.shape}")
print(f"컬럼: {df.columns.tolist()}")
print(f"자료형:\n{df.dtypes}")
display(df.head(3))

# %% code 19.
import hashlib
from pathlib import Path

def _file_hash(path, chunk_size=1024 * 1024):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def save_csv_if_changed(df_obj, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_suffix(output_path.suffix + '.part')
    df_obj.to_csv(temp_path, index=False, encoding='utf-8-sig')
    if output_path.exists() and _file_hash(output_path) == _file_hash(temp_path):
        temp_path.unlink(missing_ok=True)
        print(f"Skip (same file): {output_path}")
        return
    temp_path.replace(output_path)
    print(f"Saved: {output_path}")

save_csv_if_changed(df, proj_dir/"noaa_earthquakes.csv")

# %% code 20.
# 두 번째 분석 단계에서도 같은 폴더의 JSON/GeoJSON 파일 목록을 다시 확인합니다.
fpaths = sorted((proj_dir).glob("*.geojson")) + sorted((proj_dir).glob("*.json"))
fpaths = list(dict.fromkeys(fpaths))

if len(fpaths) < 2:
    raise FileNotFoundError("비교할 두 번째 JSON/GeoJSON 파일이 없습니다. 앞의 다운로드 셀을 먼저 실행해 주세요.")

print(f"fpaths: {fpaths}")
print(f"len(fpaths): {len(fpaths)}")

# %% code 21.
import json

# 두 번째 JSON/GeoJSON 파일을 읽고 구조를 확인합니다.
print(f"파일명: {fpaths[1].name}")
print(f"파일 크기: {fpaths[1].stat().st_size / 1024:.2f} KB")
print(f"전체 경로: {fpaths[1]}")

df1, data = earthquake_json_to_dataframe(fpaths[1])

print("\n=== 데이터 구조 ===")
print(f"자료형: {type(data)}")

if isinstance(data, dict):
    print(f"최상위 키: {list(data.keys())}")
    for key in list(data.keys())[:3]:
        value = data[key]
        if isinstance(value, (list, dict)):
            print(f"  {key}: {type(value).__name__} (길이: {len(value)})")
        else:
            print(f"  {key}: {type(value).__name__}")
elif isinstance(data, list):
    print(f"리스트 길이: {len(data)}")

print("\n=== DataFrame 확인 ===")
print(f"데이터프레임 크기: {df1.shape}")
print(f"컬럼: {df1.columns.tolist()}")
display(df1.head(3))

# %% code 22.
# 앞 셀에서 만든 두 번째 DataFrame을 확인합니다.
# df1은 규모 4.5 이상 지진 자료를 같은 형식으로 정리한 표입니다.
print(f"파일명: {fpaths[1].name}")
print(f"데이터프레임 크기: {df1.shape}")
print(f"컬럼: {df1.columns.tolist()}")
display(df1.head(3))

# %% code 23.
import folium
from folium import plugins
import numpy as np

# 데이터 정제: 위도, 경도가 있는 데이터만 추출
df_clean = df[df['mag'] >= 2.5].dropna(subset=['longitude', 'latitude'])

print(f"위치 정보가 있는 지진: {len(df_clean)} / {len(df)}")

# 지도 중심 계산
center_lat = df_clean['latitude'].mean()
center_lon = df_clean['longitude'].mean()

# 지도 생성
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=3,
    tiles='OpenStreetMap'
)

# 지진 데이터 포인트 추가
for idx, row in df_clean.iterrows():
 # 규모에 따라 마커 크기 결정
    magnitude = row.get('magnitude', 0) or 0
    radius = max(2, magnitude * 2)

 # 규모에 따라 색상 결정
    if magnitude >= 7:
        color = 'red'
    elif magnitude >= 6:
        color = 'orange'
    elif magnitude >= 5:
        color = 'yellow'
    else:
        color = 'green'

 # 팝업 정보
    popup_text = f"""
    <b>지진</b><br>
    위도: {row.get('latitude', 'N/A'):.2f}<br>
    경도: {row.get('longitude', 'N/A'):.2f}<br>
    규모: {magnitude}<br>
    깊이: {row.get('depth', 'N/A')} km<br>
    위치: {row.get('locationName', 'N/A')}<br>
    연도: {row.get('year', 'N/A')}
    """

    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=radius,
        popup=folium.Popup(popup_text, max_width=300),
        color=color,
        fill=True,
        fillColor=color,
        fillOpacity=0.7,
        weight=1
    ).add_to(m)

# 지도 저장 및 표시
map_path = proj_dir / "earthquake_map.html"
m.save(str(map_path))
print(f"\n지도 저장 완료: {map_path}")
print(f"지도에 표시된 지진 수: {len(df_clean)}")
m

# %% code 24.
import folium
import numpy as np

# 데이터 정제: 위도, 경도가 있는 데이터만 추출
df1_clean = df1.dropna(subset=['longitude', 'latitude'])

print(f"위치 정보가 있는 지진: {len(df1_clean)} / {len(df1)}")

# 지도 중심 계산
center_lat = df1_clean['latitude'].mean()
center_lon = df1_clean['longitude'].mean()

# 지도 생성
m1 = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=2,
    tiles='OpenStreetMap'
)

# 지진 데이터 포인트 추가
for idx, row in df1_clean.iterrows():
 # 규모에 따라 마커 크기 결정
    magnitude = row.get('magnitude', 0) or 0
    radius = max(2, magnitude * 2)

 # 규모에 따라 색상 결정
    if magnitude >= 7:
        color = 'red'
    elif magnitude >= 6:
        color = 'orange'
    elif magnitude >= 5:
        color = 'yellow'
    elif magnitude >= 4:
        color = 'lightblue'
    else:
        color = 'green'

 # 팝업 정보
    place = row.get('place', 'N/A')
    time_val = row.get('time', 'N/A')

    popup_text = f"""
    <b>지진 정보</b><br>
    규모: {magnitude}<br>
    위도: {row.get('latitude', 'N/A'):.2f}<br>
    경도: {row.get('longitude', 'N/A'):.2f}<br>
    깊이: {row.get('depth', 'N/A')} km<br>
    위치: {place}<br>
    시간: {time_val}
    """

    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=radius,
        popup=folium.Popup(popup_text, max_width=300),
        color=color,
        fill=True,
        fillColor=color,
        fillOpacity=0.7,
        weight=1
    ).add_to(m1)

# 지도 저장 및 표시
map_path1 = proj_dir / "usgs_earthquake_map.html"
m1.save(str(map_path1))
print(f"\n지도 저장 완료: {map_path1}")
print(f"지도에 표시된 지진 수: {len(df1_clean)}")
m1

# %% code 25.
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

# 데이터 정제: 위도, 경도가 있는 데이터만 추출
df1_clean = df1.dropna(subset=['longitude', 'latitude', 'mag'])

# Matplotlib 그림 설정
plt.figure(figsize=(12.0, 8.0))

# Basemap 생성
# projection: 지도를 투영하는 방식 (e.g., 'merc' for Mercator)
# llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon: 지도의 경계 (latitude, longitude)
# resolution: 해상도 ('l'ow, 'i'ntermediate, 'h'igh, 'f'ull)
m = Basemap(projection='merc',
            llcrnrlat=-80, urcrnrlat=80,
            llcrnrlon=-180, urcrnrlon=180,
            lat_ts=20, resolution='l')

# 해안선, 국가 경계선, 위도/경도선 그리기
m.drawcoastlines()
m.drawcountries()
m.drawparallels(np.arange(-90, 91, 30), labels=[1,0,0,0]) # 위도선
m.drawmeridians(np.arange(-180, 181, 60), labels=[0,0,0,1]) # 경도선

# 지진 데이터 포인트 변환 및 플로팅
x, y = m(df1_clean['longitude'].values, df1_clean['latitude'].values)

# 규모에 따라 마커 크기 및 색상 설정
# 'mag' (magnitude) 컬럼 사용. USGS 데이터에는 'mag'가 있음.
# 여기서는 USGS 데이터를 사용하므로 'mag'를 사용.
# 규모가 클수록 마커 크기를 크게, 색상을 붉게

# 매핑 함수 정의
def get_marker_size(magnitude):
    return max(8, (magnitude - 4) * 2 * 8)  # 최소 크기 8, 규모 1당 16씩 증가

def get_marker_color(magnitude):
    if magnitude >= 7: return 'red'
    elif magnitude >= 6: return 'orange'
    elif magnitude >= 5: return 'yellow'
    elif magnitude >= 4: return 'blue'
    else: return 'green'

sizes = df1_clean['mag'].apply(get_marker_size)
colors = df1_clean['mag'].apply(get_marker_color)

m.scatter(x, y, s=sizes, c=colors, alpha=0.7, edgecolor='none', zorder=5)

# 범례 추가 (선택 사항, scatter plot에서는 복잡할 수 있음)
# 간단한 범례를 위해 몇몇 대표 규모를 예시로 표시할 수 있습니다.
for mag_val, color_val in zip([3, 5, 7], ['green', 'yellow', 'red']):
    plt.scatter([], [], c=color_val, alpha=0.7, s=get_marker_size(mag_val), label=f'Magnitude >= {mag_val}')
plt.legend(scatterpoints=1, frameon=False, labelspacing=1, title='Earthquake Magnitude')

plt.title('Global Earthquakes (USGS Data) - Basemap')
du.save_figure(plt.gcf(), os.path.join(proj_dir, "05_02_Visualizing_global_seismic_belts_01"))
plt.show()

print(f"지도에 표시된 지진 수: {len(df1_clean)}")

# %% code 26.
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# 데이터 정제: 위도, 경도, 규모가 있는 데이터만 추출
df1_clean = df1.dropna(subset=['longitude', 'latitude', 'mag'])

# 1. Matplotlib figure와 Cartopy axes 생성
plt.figure(figsize=(12.0, 8.0))
ax = plt.axes(projection=ccrs.PlateCarree())

# 2. 지리적 특성 추가
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)

# 격자선 및 라벨 추가
gridlines = ax.gridlines(draw_labels=True, linestyle='--', color='gray')
gridlines.xlabels_top = False
gridlines.ylabels_right = False

# 3. 마커 크기·색상: 앞 셀의 함수와 결과를 그대로 사용

# 4. 지진 데이터 플로팅
# transform=ccrs.PlateCarree()는 데이터가 Plate Carree 좌표계(위도, 경도)임을 Cartopy에 알립니다.
ax.scatter(
    df1_clean['longitude'],
    df1_clean['latitude'],
    s=sizes,
    c=colors,
    alpha=0.7,
    edgecolor='black',
    linewidth=0.5,
    transform=ccrs.PlateCarree(),
    zorder=5 # 다른 feature 위에 표시
)

# 5. 지도 제목 설정
ax.set_title('Global Earthquakes (USGS Data) - Cartopy')

# 6. 범례 추가
# 더미 플롯을 사용하여 범례를 만듭니다.
legend_elements = []
for mag_val, color_val in zip([3, 4, 5, 6, 7], ['green', 'blue', 'yellow', 'orange', 'red']):
    legend_elements.append(plt.scatter(
        [], [],
        c=color_val,
        s=get_marker_size(mag_val),
        label=f'Magnitude >= {mag_val}',
        alpha=0.7,
        edgecolor='black',
        linewidth=0.5
    ))

ax.legend(handles=legend_elements, title='Earthquake Magnitude', loc='lower left', bbox_to_anchor=(0.02, 0.05))

# 7. 플롯 표시
du.save_figure(plt.gcf(), os.path.join(proj_dir, "05_02_Visualizing_global_seismic_belts_02"))
plt.show()

# 8. 확인 메시지 출력
print(f"지도에 표시된 지진 수: {len(df1_clean)}")
