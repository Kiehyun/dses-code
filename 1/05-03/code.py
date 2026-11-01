# 지구과학 데이터 사이언스 1 | V-03. 지진파 데이터로 진앙 찾기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 27.
from pathlib import Path
from datetime import datetime
from urllib.parse import urlencode
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd
import requests

EVENT_ID = "73990216"
EVENT_URL = "https://service.ncedc.org/fdsnws/event/1/query"
STATION_URL = "https://service.ncedc.org/fdsnws/station/1/query"

params = {
    "format": "xml",
    "eventid": EVENT_ID,
    "includearrivals": "true",
}

response = requests.get(EVENT_URL, params=params, timeout=60)
response.raise_for_status()
xml_text = response.text

event_file = Path(proj_dir) / f"ncedc_event_{EVENT_ID}_arrivals.xml"
event_file.write_text(xml_text, encoding="utf-8")

print(response.url)
print(f"저장 위치: {event_file}")
print(f"파일 크기: {event_file.stat().st_size:,} bytes")

# %% code 28.
def tag_name(element):
    return element.tag.split("}")[-1]

def first_child(element, name):
    for child in list(element):
        if tag_name(child) == name:
            return child
    return None

def child_text(element, path):
    current = element
    for name in path:
        current = first_child(current, name)
        if current is None:
            return None
    return current.text

def parse_time(value):
    return pd.to_datetime(value, utc=True)

root = ET.fromstring(xml_text)
event = next(elem for elem in root.iter() if tag_name(elem) == "event")
origin = next(elem for elem in event.iter() if tag_name(elem) == "origin")

origin_info = {
    "event_id": EVENT_ID,
    "origin_time": parse_time(child_text(origin, ["time", "value"])),
    "latitude": float(child_text(origin, ["latitude", "value"])),
    "longitude": float(child_text(origin, ["longitude", "value"])),
    "depth_km": float(child_text(origin, ["depth", "value"])) / 1000,
}

origin_info

# %% code 29.
pick_rows = []

for pick in [elem for elem in event.iter() if tag_name(elem) == "pick"]:
    waveform = first_child(pick, "waveformID")
    if waveform is None:
        continue

    pick_rows.append({
        "pick_id": pick.attrib.get("publicID"),
        "phase": child_text(pick, ["phaseHint"]),
        "pick_time": parse_time(child_text(pick, ["time", "value"])),
        "network": waveform.attrib.get("networkCode"),
        "station": waveform.attrib.get("stationCode"),
        "channel": waveform.attrib.get("channelCode"),
        "location": waveform.attrib.get("locationCode"),
    })

picks = pd.DataFrame(pick_rows)
print(picks)

# %% code 30.
picks["phase"].value_counts(dropna=False)

# %% code 31.
phase_table = (
    picks[picks["phase"].isin(["P", "S"])]
    .sort_values("pick_time")
    .groupby(["network", "station", "phase"], as_index=False)
    .first()
    .pivot(index=["network", "station"], columns="phase", values="pick_time")
    .dropna(subset=["P", "S"])
    .reset_index()
)

phase_table["s_minus_p_sec"] = (phase_table["S"] - phase_table["P"]).dt.total_seconds()
phase_table = phase_table[(phase_table["s_minus_p_sec"] > 0) & (phase_table["s_minus_p_sec"] < 120)]
phase_table = phase_table.sort_values("s_minus_p_sec").reset_index(drop=True)

print(phase_table)

# %% code 32.
def download_station_metadata(network, station, event_time):
    params = {
        "format": "text",
        "net": network,
        "sta": station,
        "level": "station",
        "startbefore": event_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "endafter": event_time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    response = requests.get(STATION_URL, params=params, timeout=30)
    response.raise_for_status()

    lines = [line for line in response.text.splitlines() if line and not line.startswith("#")]
    if not lines:
        return None

    values = lines[0].split("|")
    return {
        "network": values[0],
        "station": values[1],
        "station_latitude": float(values[2]),
        "station_longitude": float(values[3]),
        "elevation_m": float(values[4]),
        "site_name": values[5],
    }

station_rows = []

for row in phase_table[["network", "station"]].drop_duplicates().itertuples(index=False):
    metadata = download_station_metadata(row.network, row.station, origin_info["origin_time"])
    if metadata is not None:
        station_rows.append(metadata)

stations = pd.DataFrame(station_rows)

print(stations)

# %% code 33.
data = phase_table.merge(stations, on=["network", "station"], how="inner")

# 단순한 지각 평균 속도 가정
vp = 6.0  # km/s
vs = 3.5  # km/s

data["estimated_distance_km"] = data["s_minus_p_sec"] / (1 / vs - 1 / vp)
data = data.sort_values("estimated_distance_km").reset_index(drop=True)

print(data[["network", "station", "P", "S", "s_minus_p_sec", "estimated_distance_km", "station_latitude", "station_longitude"]])

# %% code 34.
def haversine_km(lat1, lon1, lat2, lon2):
    radius = 6371.0
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * radius * np.arcsin(np.sqrt(a))

# 가까운 관측소 위주로 사용하면 단순 속도 가정의 영향이 줄어듭니다.
used = data.head(12).copy()

lat_grid = np.linspace(used["station_latitude"].min() - 0.8, used["station_latitude"].max() + 0.8, 160)
lon_grid = np.linspace(used["station_longitude"].min() - 0.8, used["station_longitude"].max() + 0.8, 160)
lon_mesh, lat_mesh = np.meshgrid(lon_grid, lat_grid)

misfit = np.zeros_like(lat_mesh, dtype=float)

for _, row in used.iterrows():
    model_distance = haversine_km(lat_mesh, lon_mesh, row["station_latitude"], row["station_longitude"])
    misfit += (model_distance - row["estimated_distance_km"]) ** 2

misfit = np.sqrt(misfit / len(used))
best_index = np.unravel_index(np.argmin(misfit), misfit.shape)
estimated_lat = lat_mesh[best_index]
estimated_lon = lon_mesh[best_index]
best_misfit = misfit[best_index]

print(f"추정 진앙: lat={estimated_lat:.4f}, lon={estimated_lon:.4f}")
print(f"발표 진앙: lat={origin_info['latitude']:.4f}, lon={origin_info['longitude']:.4f}")
print(f"평균 거리 잔차(RMS): {best_misfit:.1f} km")
print(f"실제 진앙과의 거리 차이: {haversine_km(estimated_lat, estimated_lon, origin_info['latitude'], origin_info['longitude']):.1f} km")

# %% code 35.
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'   # macOS: 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# 관측소와 발표 진앙 사이의 실제 거리(앞 셀의 haversine_km 사용)
data["true_distance_km"] = haversine_km(data["station_latitude"], data["station_longitude"],
                                        origin_info["latitude"], origin_info["longitude"])

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(data["s_minus_p_sec"], data["true_distance_km"], s=70, color="tab:blue",
           label="실제 거리(haversine)")
ax.plot(data["s_minus_p_sec"], data["estimated_distance_km"], color="tab:red",
        label="추정 거리(S-P 시간 차이 × 8.4)")
for _, row in data.head(12).iterrows():
    ax.text(row["s_minus_p_sec"] + 0.05, row["true_distance_km"], row["station"], fontsize=9)
ax.set_xlabel("S-P 시간 차이 (초)")
ax.set_ylabel("관측소–진앙 거리 (km)")
ax.set_title("S-P 시간 차이와 관측소–진앙 거리")
ax.legend()
ax.grid(alpha=0.3)
du.save_figure(plt.gcf(), os.path.join(proj_dir, "05_03_Finding_epicenter_with_P_and_S_waves_01"))
plt.show()

# %% code 36.
import folium

center_lat = np.mean([estimated_lat, origin_info["latitude"]])
center_lon = np.mean([estimated_lon, origin_info["longitude"]])

m = folium.Map(location=[center_lat, center_lon], zoom_start=7, tiles="CartoDB positron")

folium.Marker(
    [origin_info["latitude"], origin_info["longitude"]],
    popup="발표 진앙",
    icon=folium.Icon(color="red", icon="star"),
).add_to(m)

folium.Marker(
    [estimated_lat, estimated_lon],
    popup="S-P 자료로 추정한 진앙",
    icon=folium.Icon(color="blue", icon="info-sign"),
).add_to(m)

for _, row in used.iterrows():
    folium.CircleMarker(
        [row["station_latitude"], row["station_longitude"]],
        radius=5,
        color="black",
        fill=True,
        fill_color="white",
        popup=f"{row['network']}.{row['station']} / S-P={row['s_minus_p_sec']:.2f}s",
    ).add_to(m)
    folium.Circle(
        [row["station_latitude"], row["station_longitude"]],
        radius=row["estimated_distance_km"] * 1000,
        color="steelblue",
        weight=1,
        fill=False,
        opacity=0.35,
    ).add_to(m)

map_file = Path(proj_dir) / "estimated_epicenter_map.html"
m.save(map_file)
print(f"지도 저장 위치: {map_file}")
m
