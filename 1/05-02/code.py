# 지구과학 데이터 사이언스 1 | V-02. 세계의 지진대
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 12.
# USGS 지진 목록(GeoJSON): 최근 30일 전체, 규모 4.5 이상
usgs_feeds = {
    "01_usgs_all_month.geojson": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson",
    "02_usgs_4.5_month.geojson": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_month.geojson",
}

for filename, url in usgs_feeds.items():
    du.download(url, proj_dir / filename)

fpaths = sorted(proj_dir.glob("*.geojson")) + sorted(proj_dir.glob("*.json"))
# 중복 경로 제거
fpaths = list(dict.fromkeys(fpaths))

if len(fpaths) == 0:
    raise FileNotFoundError(f"{proj_dir} 폴더에서 JSON/GeoJSON 파일을 찾지 못했습니다.")

print(f"fpaths: {fpaths}")
print(f"len(fpaths): {len(fpaths)}")

# %% code 13.
du.preview_text(fpaths[0], n=10);

# %% code 14.
import pandas as pd
import json

def earthquake_json_to_dataframe(json_path):
    """USGS GeoJSON 또는 일반 JSON 지진 자료를 DataFrame으로 변환합니다."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # USGS GeoJSON: 지진(feature)마다 properties(속성)와 geometry(좌표)
    if isinstance(data, dict) and "features" in data:
        rows = []
        for feature in data["features"]:
            props = feature.get("properties", {}) or {}
            # coordinates: [경도, 위도, 깊이(km)]
            coords = (feature.get("geometry", {}) or {}).get("coordinates", [None, None, None])
            row = dict(props)
            row["longitude"] = coords[0] if len(coords) > 0 else None
            row["latitude"] = coords[1] if len(coords) > 1 else None
            row["depth"] = coords[2] if len(coords) > 2 else None  # km
            rows.append(row)
        df_out = pd.DataFrame(rows)
    # 그 밖의 JSON 형식
    elif isinstance(data, dict) and "items" in data:
        df_out = pd.DataFrame(data["items"])
    elif isinstance(data, dict) and "earthquakes" in data:
        df_out = pd.DataFrame(data["earthquakes"])
    elif isinstance(data, list):
        df_out = pd.DataFrame(data)
    else:
        df_out = pd.DataFrame(data)

    # 규모 열을 mag · magnitude 두 이름으로 모두 쓸 수 있게
    if "mag" in df_out.columns and "magnitude" not in df_out.columns:
        df_out["magnitude"] = df_out["mag"]
    if "magnitude" in df_out.columns and "mag" not in df_out.columns:
        df_out["mag"] = df_out["magnitude"]

    # time: 1970-01-01부터의 밀리초(Unix 시간) → UTC 날짜 · 시각
    if "time" in df_out.columns:
        df_out["time_utc"] = pd.to_datetime(df_out["time"], unit="ms", utc=True, errors="coerce")

    return df_out, data

# 첫 파일(최근 30일 전체 지진)을 표로
df, data = earthquake_json_to_dataframe(fpaths[0])

print(f"파일명: {fpaths[0].name}")

# %% code 15.
# 위도 · 경도 · 깊이(km) · 규모(mag) 열이 들어 있는지 확인
print(f"파일명: {fpaths[0].name}")
print(f"데이터프레임 크기: {df.shape}")
print(f"컬럼: {df.columns.tolist()}")
print(f"자료형:\n{df.dtypes}")
display(df.head(3))

# %% code 16.
import hashlib
from pathlib import Path

# 파일 내용의 SHA-256 해시(같은 파일인지 비교용)
def _file_hash(path, chunk_size=1024 * 1024):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

# 내용이 바뀌었을 때만 CSV 저장: 임시 파일에 쓰고 비교한 뒤 교체
def save_csv_if_changed(df_obj, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_suffix(output_path.suffix + '.part')
    df_obj.to_csv(temp_path, index=False, encoding='utf-8-sig')  # 엑셀 한글 깨짐 방지
    if output_path.exists() and _file_hash(output_path) == _file_hash(temp_path):
        temp_path.unlink(missing_ok=True)
        print(f"내용이 같아 저장하지 않음: {output_path}")
        return
    temp_path.replace(output_path)
    print(f"저장 완료: {output_path}")

save_csv_if_changed(df, proj_dir/"usgs_all_month.csv")

# %% code 17.
# 폴더의 GeoJSON 파일 목록 다시 확인(두 번째 파일을 쓸 차례)
fpaths = sorted((proj_dir).glob("*.geojson")) + sorted((proj_dir).glob("*.json"))
fpaths = list(dict.fromkeys(fpaths))

if len(fpaths) < 2:
    raise FileNotFoundError("비교할 두 번째 JSON/GeoJSON 파일이 없습니다. 앞의 다운로드 셀을 먼저 실행해 주세요.")

print(f"fpaths: {fpaths}")
print(f"len(fpaths): {len(fpaths)}")

# %% code 18.
import json

# 두 번째 파일(규모 4.5 이상) 읽기 · 구조 확인
print(f"파일명: {fpaths[1].name}")
print(f"파일 크기: {fpaths[1].stat().st_size / 1024:.2f} KB")
print(f"전체 경로: {fpaths[1]}")

df1, data = earthquake_json_to_dataframe(fpaths[1])

print("\n=== 데이터 구조 ===")
print(f"자료형: {type(data)}")

if isinstance(data, dict):
    print(f"최상위 키: {list(data.keys())}")
    for key in list(data.keys())[:3]:  # 앞의 키 3개만
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

# %% code 19.
# df1: 규모 4.5 이상 지진(df와 같은 열 구성)
print(f"파일명: {fpaths[1].name}")
print(f"데이터프레임 크기: {df1.shape}")
print(f"컬럼: {df1.columns.tolist()}")
display(df1.head(3))

# %% code 20.
import folium
from folium import plugins
import numpy as np

# 1) 규모 2.5 이상이고 위경도가 있는 지진만
df_clean = df[df['mag'] >= 2.5].dropna(subset=['longitude', 'latitude'])

print(f"위치 정보가 있는 지진: {len(df_clean)} / {len(df)}")

# 2) 지진 위치의 평균을 지도 중심으로
center_lat = df_clean['latitude'].mean()
center_lon = df_clean['longitude'].mean()

m = folium.Map(
    location=[center_lat, center_lon], zoom_start=3, tiles='OpenStreetMap'
)

# 3) 지진마다 원 마커 추가
for idx, row in df_clean.iterrows():
    # 규모가 클수록 큰 원(반지름 최소 2)
    magnitude = row.get('magnitude', 0) or 0
    radius = max(2, magnitude * 2)

    # 규모별 색
    if magnitude >= 7:
        color = 'red'
    elif magnitude >= 6:
        color = 'orange'
    elif magnitude >= 5:
        color = 'yellow'
    else:
        color = 'green'

    # 클릭하면 보일 정보(HTML)
    popup_text = f"""
    <b>지진</b><br>
    위도: {row.get('latitude', 'N/A'):.2f}<br>
    경도: {row.get('longitude', 'N/A'):.2f}<br>
    규모: {magnitude}<br>
    깊이: {row.get('depth', 'N/A')} km<br>
    위치: {row.get('place', 'N/A')}<br>
    시각: {row['time_utc']:%Y-%m-%d %H:%M} UTC
    """

    folium.CircleMarker(
        location=[row['latitude'], row['longitude']], radius=radius,
        popup=folium.Popup(popup_text, max_width=300), color=color, fill=True,
        fillColor=color, fillOpacity=0.7, weight=1
    ).add_to(m)

# 4) 지도 저장 · 표시
map_path = proj_dir / "earthquake_map.html"
m.save(str(map_path))
print(f"\n지도 저장 완료: {map_path}")
print(f"지도에 표시된 지진 수: {len(df_clean)}")
m

# %% code 21.
import folium
import numpy as np

# 1) 위경도가 있는 지진만(df1: 규모 4.5 이상)
df1_clean = df1.dropna(subset=['longitude', 'latitude'])

print(f"위치 정보가 있는 지진: {len(df1_clean)} / {len(df1)}")

# 2) 지진 위치의 평균을 지도 중심으로
center_lat = df1_clean['latitude'].mean()
center_lon = df1_clean['longitude'].mean()

m1 = folium.Map(
    location=[center_lat, center_lon], zoom_start=2, tiles='OpenStreetMap'
)

# 3) 지진마다 원 마커 추가
for idx, row in df1_clean.iterrows():
    # 규모가 클수록 큰 원(반지름 최소 2)
    magnitude = row.get('magnitude', 0) or 0
    radius = max(2, magnitude * 2)

    # 규모별 색
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

    # 클릭하면 보일 정보(HTML)
    place = row.get('place', 'N/A')
    time_val = f"{row['time_utc']:%Y-%m-%d %H:%M} UTC"  # 밀리초 숫자 대신 날짜 · 시각

    popup_text = f"""
    <b>지진 정보</b><br>
    규모: {magnitude}<br>
    위도: {row.get('latitude', 'N/A'):.2f}<br>
    경도: {row.get('longitude', 'N/A'):.2f}<br>
    깊이: {row.get('depth', 'N/A')} km<br>
    위치: {place}<br>
    시각: {time_val}
    """

    folium.CircleMarker(
        location=[row['latitude'], row['longitude']], radius=radius,
        popup=folium.Popup(popup_text, max_width=300), color=color, fill=True,
        fillColor=color, fillOpacity=0.7, weight=1
    ).add_to(m1)

# 4) 지도 저장 · 표시
map_path1 = proj_dir / "usgs_earthquake_map.html"
m1.save(str(map_path1))
print(f"\n지도 저장 완료: {map_path1}")
print(f"지도에 표시된 지진 수: {len(df1_clean)}")
m1

# %% code 22.
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

# 1) 위경도 · 규모가 있는 지진만
df1_clean = df1.dropna(subset=['longitude', 'latitude', 'mag'])

plt.figure(figsize=(12.0, 8.0))

# 2) 메르카토르 도법(극 쪽은 끝없이 늘어나 위도 ±80°까지)
m = Basemap(projection='merc',
            llcrnrlat=-80, urcrnrlat=80,
            llcrnrlon=-180, urcrnrlon=180,
            lat_ts=20, resolution='l')  # 축척 기준 위도, 낮은 해상도

m.drawcoastlines()
m.drawcountries()
m.drawparallels(np.arange(-90, 91, 30), labels=[1,0,0,0])  # 왼쪽에 위도 눈금
m.drawmeridians(np.arange(-180, 181, 60), labels=[0,0,0,1])  # 아래쪽에 경도 눈금

# 3) 경위도 → 지도 좌표
x, y = m(df1_clean['longitude'].values, df1_clean['latitude'].values)

# 4) 규모(mag)가 클수록 크고 붉은 마커
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

# 5) 범례: 빈 산점도로 대표 규모만 표시
for mag_val, color_val in zip([3, 5, 7], ['green', 'yellow', 'red']):
    plt.scatter([], [], c=color_val, alpha=0.7, s=get_marker_size(mag_val), label=f'규모 {mag_val} 이상')
plt.legend(scatterpoints=1, frameon=False, labelspacing=1, title='규모')

plt.title('전 세계 지진 분포 (USGS 데이터, Basemap)')
du.save_figure(plt.gcf(), os.path.join(proj_dir, "05_02_Visualizing_global_seismic_belts_01"))
plt.show()

print(f"지도에 표시된 지진 수: {len(df1_clean)}")

# %% code 23.
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# 위경도 · 규모가 있는 지진만
df1_clean = df1.dropna(subset=['longitude', 'latitude', 'mag'])

# 1) 정거 원통 도법(PlateCarree) 지도
plt.figure(figsize=(12.0, 8.0))
ax = plt.axes(projection=ccrs.PlateCarree())

# 2) 지리 요소 · 격자선
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)

gridlines = ax.gridlines(draw_labels=True, linestyle='--', color='gray')
gridlines.top_labels = False    # 위쪽 경도 눈금 숨김
gridlines.right_labels = False  # 오른쪽 위도 눈금 숨김

# 3) 마커 크기 · 색: 앞 셀의 sizes, colors 사용

# 4) 지진 표시
ax.scatter(
    df1_clean['longitude'],
    df1_clean['latitude'],
    s=sizes,
    c=colors,
    alpha=0.7,
    edgecolor='black',
    linewidth=0.5,
    transform=ccrs.PlateCarree(),  # 자료가 경위도 좌표임을 알림
    zorder=5                       # 지도 요소 위에
)

ax.set_title('전 세계 지진 분포 (USGS 데이터, Cartopy)')

# 5) 범례: 빈 산점도로 대표 규모 표시
legend_elements = []
for mag_val, color_val in zip([3, 4, 5, 6, 7], ['green', 'blue', 'yellow', 'orange', 'red']):
    legend_elements.append(plt.scatter(
        [], [],
        c=color_val,
        s=get_marker_size(mag_val),
        label=f'규모 {mag_val} 이상',
        alpha=0.7,
        edgecolor='black',
        linewidth=0.5
    ))

ax.legend(handles=legend_elements, title='규모', loc='lower left', bbox_to_anchor=(0.02, 0.05))

du.save_figure(plt.gcf(), os.path.join(proj_dir, "05_02_Visualizing_global_seismic_belts_02"))
plt.show()

print(f"지도에 표시된 지진 수: {len(df1_clean)}")
