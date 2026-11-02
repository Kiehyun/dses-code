# 지구과학 데이터 사이언스 2 | V-03. 화석 산출과 지질 시대
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 530.
from pathlib import Path
from io import StringIO
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

DATA_DIR = proj_dir
DATA_DIR.mkdir(exist_ok=True)

params = {
    "base_name": "Trilobita",
    "show": "coords,phylo,strat,lith",
    "occs_created_before": "2026-10-26",  # 이 날짜 전에 등록된 기록만(결과 재현용)
    "limit": "all",  # 숫자를 주면 등록 순서 앞쪽 기록만 받음
}
url = "https://paleobiodb.org/data1.2/occs/list.csv"

# PBDB API에서 CSV 문자열 내려받기
response = requests.get(url, params=params, timeout=180)
response.raise_for_status()

csv_file = DATA_DIR / "pbdb_trilobita_occurrences.csv"
csv_file.write_bytes(response.content)   # 받은 그대로 저장(윈도우 줄바꿈 중복 방지)

# 내려받은 CSV를 DataFrame으로 읽기
fossils = pd.read_csv(StringIO(response.text), low_memory=False)

print(response.url)
print(f"데이터 개수: {len(fossils):,}")
print(f"저장 위치: {csv_file}")
fossils.head()

# %% code 531.
use_cols = ["accepted_name", "accepted_rank", "early_interval",
            "late_interval", "max_ma", "min_ma", "lng", "lat", "phylum",
            "class", "order", "family", "genus", "lithology1"]
fossils[use_cols].head(10)

# %% code 532.
# 분석을 위해 숫자형 열과 대표 연대 정리
fossils["max_ma"] = pd.to_numeric(fossils["max_ma"], errors="coerce")
fossils["min_ma"] = pd.to_numeric(fossils["min_ma"], errors="coerce")
fossils["mid_ma"] = (fossils["max_ma"] + fossils["min_ma"]) / 2

# 좌표가 있는 데이터만 지도 분석에 사용
fossils_geo = fossils.dropna(subset=["lng", "lat"]).copy()
print(f"좌표가 있는 데이터: {len(fossils_geo):,}")

# %% code 533.
# 국제 연대층서표(ICS v2026/06)의 고생대 기 경계 (Ma)
period_edges = [251.902, 298.9, 358.86, 419.62, 443.1, 486.85, 538.8]
period_names = ["페름기", "석탄기", "데본기", "실루리아기", "오르도비스기", "캄브리아기"]

fossils["period"] = pd.cut(fossils["mid_ma"], bins=period_edges,
                           labels=period_names, right=False)
period_counts = (
    fossils["period"]
    .value_counts()
    .reindex(period_names[::-1])  # 오래된 기부터
    .rename_axis("period")
    .reset_index(name="count")
)
print(f"전체 기록 수: {len(fossils):,}")
print(period_counts.to_string(index=False))

fig, ax = plt.subplots(figsize=(7.7, 4.2))
sns.barplot(data=period_counts, x="count", y="period", ax=ax,
            color="lightseagreen")
ax.set_title("고생대 기별 삼엽충 화석 산출 기록 수")
ax.set_xlabel("산출 기록 수")
ax.set_ylabel("지질 시대(기)")
ax.grid(axis="x", alpha=0.3)
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_01"))
plt.show()

# %% code 534.
fig, ax = plt.subplots(figsize=(8.4, 3.8))
ax.hist(fossils["mid_ma"].dropna(), bins=40, color="slateblue", alpha=0.8)
ax.axvline(251.9, color="red", ls="--", lw=1, label="페름기 말 대멸종 (251.9 Ma)")
ax.invert_xaxis()  # 오래된 시기를 왼쪽에
ax.set_title("삼엽충 화석 산출 기록의 연대 분포")
ax.set_xlabel("연대 (Ma, 백만 년 전)")
ax.set_ylabel("산출 기록 수")
ax.legend()
ax.grid(alpha=0.3)
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_02"))
plt.show()

# %% code 535.
import folium

# 너무 많은 점을 모두 표시하면 지도가 느려질 수 있어 일부만 사용
map_data = fossils_geo.sample(min(800, len(fossils_geo)), random_state=42)

m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")
for row in map_data.itertuples(index=False):
    popup = f"{row.accepted_name}<br>{row.early_interval}<br>{row.max_ma}-{row.min_ma} Ma"
    folium.CircleMarker(
        [row.lat, row.lng], radius=3, color="darkred", fill=True,
        fill_opacity=0.6, popup=popup,
    ).add_to(m)

map_file = DATA_DIR / "pbdb_trilobita_map.html"
m.save(map_file)
print(f"지도 저장 위치: {map_file}")
