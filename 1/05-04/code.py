# 지구과학 데이터 사이언스 1 | V-04. 지질도 작성 및 이해
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 34.
from pathlib import Path
from urllib.parse import urlencode
import json

import geopandas as gpd
import numpy as np
import pandas as pd
import requests

MACROSTRAT_URL = "https://macrostrat.org/api/v2/geologic_units/map"  # 지질도 API

# 지질 단위를 조회할 지점(위도 · 경도, °)
places = pd.DataFrame([
    {"name": "서울", "lat": 37.5665, "lng": 126.9780},
    {"name": "대전", "lat": 36.3504, "lng": 127.3845},
    {"name": "부산", "lat": 35.1796, "lng": 129.0756},
    {"name": "광주", "lat": 35.1595, "lng": 126.8526},
    {"name": "강릉", "lat": 37.7519, "lng": 128.8761},
    {"name": "제주", "lat": 33.4996, "lng": 126.5312},
])

# 지도 중심: 지점들의 평균 위치
map_center = {
    "name": "대한민국",
    "lat": places["lat"].mean(),
    "lng": places["lng"].mean(),
}

features_by_map_id = {}  # map_id → 지질 단위(중복 제거)
refs = {}                # source_id → 출처 문헌
download_log = []

# 지점마다 그 위치의 지질 단위 조회
for row in places.itertuples(index=False):
    params = {"lat": row.lat, "lng": row.lng, "format": "geojson"}
    response = requests.get(MACROSTRAT_URL, params=params, timeout=60)
    response.raise_for_status()
    geojson_data = response.json()

    for feature in geojson_data["success"]["data"].get("features", []):
        map_id = feature.get("properties", {}).get("map_id")
        features_by_map_id[map_id] = feature

    refs.update(geojson_data["success"].get("refs", {}))
    download_log.append({
        "name": row.name,
        "url": response.url,
        "feature_count": len(geojson_data["success"]["data"].get("features", [])),
    })

# 하나의 GeoJSON으로 모아 저장
feature_collection = {
    "type": "FeatureCollection",
    "features": list(features_by_map_id.values()),
}

geojson_file = Path(proj_dir) / "macrostrat_geologic_units_korea.geojson"
geojson_file.write_text(json.dumps(feature_collection), encoding="utf-8")

download_log = pd.DataFrame(download_log)

print(f"중복 제거 후 지질 단위 수: {len(feature_collection['features'])}")
print(f"파일 크기: {geojson_file.stat().st_size:,} bytes")
print(download_log)

# %% code 35.
clean_geojson_file = Path(proj_dir) / "macrostrat_geologic_units_clean.geojson"
clean_geojson_file.write_text(
    json.dumps(feature_collection), encoding="utf-8",
)

gdf = gpd.read_file(clean_geojson_file)
gdf = gdf.set_crs("EPSG:4326", allow_override=True)  # WGS84 경위도

print(gdf.shape)
gdf.head()

# lith: 암상, best_int_name: 대표 시대
# t_ · b_int_name: 가장 젊은 · 오래된 시대
# t_ · b_age: 연대(Ma, 백만 년 전)
columns_to_show = [
    "map_id", "source_id", "name", "lith", "t_int_name", "b_int_name",
    "best_int_name", "t_age", "b_age", "color"
]

print(gdf[columns_to_show].head(10))

# %% code 36.
# 대표 시대별 다각형 수
age_summary = (
    gdf.groupby("best_int_name", dropna=False)
    .size()
    .sort_values(ascending=False)
    .rename("polygon_count")
    .reset_index()
)

# 암상별 다각형 수
lith_summary = (
    gdf.groupby("lith", dropna=False)
    .size()
    .sort_values(ascending=False)
    .rename("polygon_count")
    .reset_index()
)

print(age_summary)
print(lith_summary)

# %% code 37.
import matplotlib.pyplot as plt

plot_gdf = gdf.copy()
plot_gdf["plot_color"] = plot_gdf["color"].fillna("#cccccc")  # 색 없으면 회색

fig, ax = plt.subplots(figsize=(8, 9))
plot_gdf.plot(ax=ax, color=plot_gdf["plot_color"], edgecolor="black", linewidth=0.4, alpha=0.85)

# 조회 지점과 이름
ax.scatter(places["lng"], places["lat"], color="red", marker="*", s=120, label="예시 지점", zorder=5)
for row in places.itertuples(index=False):
    ax.text(row.lng + 0.08, row.lat, row.name, fontsize=10, zorder=6)

ax.set_title("Macrostrat 자료로 그린 대한민국 주변 지질 단위")
ax.set_xlabel("경도")
ax.set_ylabel("위도")
ax.legend(loc="upper right")
ax.set_aspect("equal")  # 경도 · 위도 1° 길이를 같게
du.save_figure(plt.gcf(), os.path.join(proj_dir, "05_04_Geologic_map_basics_01"))
plt.show()

# %% code 38.
import matplotlib.pyplot as plt

# 대표 시대와 색의 짝(중복 제거)
legend_df = (
    plot_gdf[["best_int_name", "plot_color"]]
    .dropna()
    .drop_duplicates()
    .sort_values("best_int_name")
)

fig, ax = plt.subplots(figsize=(6, max(2, len(legend_df) * 0.35)))
ax.axis("off")

# 시대마다 색 상자 + 이름
for i, row in enumerate(legend_df.itertuples(index=False)):
    ax.add_patch(plt.Rectangle((0, i), 0.5, 0.25, color=row.plot_color, ec="black", lw=0.4))
    ax.text(0.65, i + 0.12, row.best_int_name, va="center", fontsize=10)

ax.set_xlim(0, 3)
ax.set_ylim(-0.2, len(legend_df))
ax.invert_yaxis()  # 위에서 아래로 나열
ax.set_title("지질 시대 범례", loc="left")
du.save_figure(plt.gcf(), os.path.join(proj_dir, "05_04_Geologic_map_basics_02"))
plt.show()

# %% code 39.
import folium

m = folium.Map(location=[map_center["lat"], map_center["lng"]], zoom_start=6, tiles="CartoDB positron")

# 마우스를 올리면 보일 속성과 한글 이름
tooltip = folium.GeoJsonTooltip(
    fields=["name", "lith", "best_int_name", "t_int_name", "b_int_name"],
    aliases=["이름", "암상", "대표 시대", "상한 시대", "하한 시대"],
    localize=True,
)

# 지질 단위 다각형(Macrostrat 지정 색으로 채움)
folium.GeoJson(
    feature_collection,
    name="Macrostrat geologic units",
    style_function=lambda feature: {
        "fillColor": feature["properties"].get("color") or "#cccccc",
        "color": "#333333",
        "weight": 0.5,
        "fillOpacity": 0.65,
    },
    tooltip=tooltip,
).add_to(m)

# 조회 지점 마커
for row in places.itertuples(index=False):
    folium.Marker([row.lat, row.lng], popup=row.name).add_to(m)

folium.LayerControl().add_to(m)

map_file = Path(proj_dir) / "macrostrat_geologic_map_korea.html"
m.save(map_file)
print(f"지도 저장 위치: {map_file}")
m

# %% code 40.
# 자료 출처(source_id)별 다각형 수와 문헌
source_summary = (
    gdf.groupby("source_id")
    .size()
    .sort_values(ascending=False)
    .rename("polygon_count")
    .reset_index()
)

source_summary["reference"] = source_summary["source_id"].astype(str).map(refs)
print(source_summary)
