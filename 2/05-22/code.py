# 지구과학 데이터 사이언스 2 | V-02. 마그마 조성과 화성암 분류
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅴ-7.
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

DATA_DIR = proj_dir
DATA_DIR.mkdir(exist_ok=True)

# GEOROC Compilation: Intraplate Volcanic Rocks (V13, 2026-09)
# 가운데 동아시아 신생대 화산암 파일
files = {  # 부분 이름: (내려받을 주소, 저장할 파일 이름)
    "part1": (
        "https://data.goettingen-research-online.de/api/access/datafile/218829",
        "GEOROC_CENTRAL_ASIAN_FOLDBELT_CENOZOIC_QUATERNARY_part1.csv"),
    "part2": (
        "https://data.goettingen-research-online.de/api/access/datafile/218822",
        "GEOROC_CENTRAL_ASIAN_FOLDBELT_CENOZOIC_QUATERNARY_part2.csv"),
}

tables = []
for part, (file_url, file_name) in files.items():
    raw_file = DATA_DIR / file_name
    if not raw_file.exists():  # 이미 받아 둔 파일은 다시 받지 않음
        response = requests.get(file_url, timeout=180)
        response.raise_for_status()
        raw_file.write_bytes(response.content)  # 받은 바이트 그대로 저장
    tables.append(pd.read_csv(raw_file, encoding="cp1252", low_memory=False))
    print(f"{part}: {raw_file}")

georoc = pd.concat(tables, ignore_index=True)

# 위치가 '한반도(KOREAN PENINSULA)'로 분류된 시료만
is_korea = georoc["LOCATION"].str.contains("KOREAN PENINSULA - CENOZOIC", regex=False,
                                           na=False)
geo = georoc[is_korea].copy()

print(f"전체 행 수(두 파일): {len(georoc):,}")
print(f"우리나라 시료 수: {len(geo):,}")
geo[["LOCATION", "ROCK NAME", "ROCK TYPE", "MATERIAL", "SIO2(WT%)", "NA2O(WT%)",
     "K2O(WT%)"]].head()

# %% code Ⅴ-8.
# 화산암(VOL)의 전암(WR) 분석만
geo = geo[(geo["ROCK TYPE"] == "VOL")
          & geo["MATERIAL"].str.startswith("WR", na=False)].copy()

oxide_cols = {"SIO2(WT%)": "SiO2", "TIO2(WT%)": "TiO2", "AL2O3(WT%)": "Al2O3",
              "FEOT(WT%)": "FeOT", "FEO(WT%)": "FeO", "FE2O3(WT%)": "Fe2O3",
              "MNO(WT%)": "MnO", "MGO(WT%)": "MgO", "CAO(WT%)": "CaO",
              "NA2O(WT%)": "Na2O", "K2O(WT%)": "K2O", "P2O5(WT%)": "P2O5"}
geo = geo.rename(columns=oxide_cols)
for col in oxide_cols.values():
    geo[col] = pd.to_numeric(geo[col], errors="coerce")

# 전체 철을 FeO로 환산(FeOT가 없을 때 FeO + 0.8998 × Fe2O3)
fe_calc = geo["FeO"].fillna(0) + 0.8998 * geo["Fe2O3"].fillna(0)
geo["FeOT"] = geo["FeOT"].fillna(fe_calc.where(fe_calc > 0))

major = ["SiO2", "TiO2", "Al2O3", "FeOT", "MnO", "MgO", "CaO", "Na2O", "K2O", "P2O5"]
geo = geo.dropna(subset=["SiO2", "Al2O3", "FeOT", "MgO", "CaO", "Na2O", "K2O"])
geo["oxide_total"] = geo[major].sum(axis=1)

# 합이 94~102%인 분석만 남기고 휘발성분을 뺀 합 100%로 다시 맞춤
n_before = len(geo)
geo = geo[geo["oxide_total"].between(94, 102)].copy()
for col in major:
    geo[col] = geo[col] / geo["oxide_total"] * 100

def region_of(location):
    """GEOROC 위치 문자열에서 지역 이름 정하기"""
    if "JEJU" in location:
        return "제주도"
    if "ULLEUNG" in location:
        return "울릉도"
    if "DOKDO" in location or "DOK ISLAND" in location:
        return "독도"
    if "CHANGBAISHAN" in location or "PAEKTU" in location:
        return "백두산"
    return "기타 한반도"

geo["region"] = geo["LOCATION"].apply(region_of)
geo["total_alkali"] = geo["Na2O"] + geo["K2O"]
tas = geo

region_order = ["제주도", "울릉도", "독도", "백두산", "기타 한반도"]
print(f"화산암 전암 분석(합 확인 전): {n_before:,}")
print(f"합 94~102%를 만족해 분석에 쓰는 시료: {len(tas):,}")
print(tas["region"].value_counts().reindex(region_order).to_string())

# %% code Ⅴ-9.
def silica_group(sio2):
    """SiO2 함량(wt.%)에 따른 전통적 화성암 조성 구분"""
    if sio2 < 45:
        return "초고철질"
    if sio2 < 52:
        return "고철질"
    if sio2 < 63:
        return "중성"
    return "규장질"

group_order = ["초고철질", "고철질", "중성", "규장질"]
tas["silica_group"] = tas["SiO2"].apply(silica_group)
pd.crosstab(tas["region"], tas["silica_group"], margins=True, margins_name="합계") \
    .reindex(index=region_order + ["합계"], columns=group_order + ["합계"])

# %% code Ⅴ-10.
from matplotlib.patches import Polygon
from matplotlib.path import Path as MplPath

# Le Bas 등(1986) TAS 분류 영역의 꼭짓점 (SiO2, Na2O+K2O)
# pyrolite(TAS config_lemaitre)에서 옮김
tas_fields = {
    "피크로현무암": [(41, 0), (41, 3), (45, 3), (45, 0)],
    "현무암": [(45, 0), (45, 5), (52, 5), (52, 0)],
    "현무암질 안산암": [(52, 0), (52, 5), (57, 5.9), (57, 0)],
    "안산암": [(57, 0), (57, 5.9), (63, 7), (63, 0)],
    "데이사이트": [(63, 0), (63, 7), (69, 8), (77.3, 0)],
    "유문암": [(69, 8), (69, 13), (85.9, 6.8), (87.5, 4.7), (77.3, 0)],
    "조면현무암": [(45, 5), (49.4, 7.3), (52, 5)],
    "현무암질 조면안산암": [(49.4, 7.3), (53, 9.3), (57, 5.9), (52, 5)],
    "조면안산암": [(53, 9.3), (57.6, 11.7), (61, 8.6), (63, 7), (57, 5.9)],
    "조면암·조면데이사이트": [(57.6, 11.7), (61, 13.5), (63, 16.2), (69, 13), (69, 8),
                      (63, 7), (61, 8.6)],
    "테프라이트·베이사나이트": [(41, 3), (41, 7), (45, 9.4), (49.4, 7.3), (45, 5), (45, 3)],
    "포노테프라이트": [(45, 9.4), (48.4, 11.5), (53, 9.3), (49.4, 7.3)],
    "테프리포놀라이트": [(48.4, 11.5), (52.5, 14), (57.6, 11.7), (53, 9.3)],
    "포놀라이트": [(52.5, 14), (52.5, 18), (57, 18), (63, 16.2), (61, 13.5), (57.6, 11.7)],
    "포이다이트": [(35, 9), (37, 14), (52.5, 18), (52.5, 14), (48.4, 11.5), (45, 9.4),
              (41, 7), (41, 3), (37, 3)],
}
# 영역 이름을 적을 위치
label_xy = {
    "피크로현무암": (43, 1.3), "현무암": (48.5, 2.5), "현무암질 안산암": (54.5, 2.5),
    "안산암": (60, 3.0), "데이사이트": (66.5, 3.5), "유문암": (74.5, 8.5),
    "조면현무암": (49, 5.8), "현무암질 조면안산암": (53, 7.4), "조면안산암": (57.8, 9.0),
    "조면암·조면데이사이트": (64.6, 14.2), "테프라이트·베이사나이트": (43.5, 6.0),
    "포노테프라이트": (49, 9.4), "테프리포놀라이트": (53, 11.6), "포놀라이트": (57.5, 14.8),
    "포이다이트": (42, 10.5),
}

fig, ax = plt.subplots(figsize=(8.5, 6.8))
sns.scatterplot(data=tas, x="SiO2", y="total_alkali", hue="region",
                hue_order=region_order, s=14, alpha=0.7, edgecolor="none", ax=ax)

# 경계선과 영역 이름은 점 위에 겹쳐 그림
for name, verts in tas_fields.items():
    ax.add_patch(Polygon(verts, closed=True, fill=False, edgecolor="gray", lw=0.8,
                         zorder=4))
    x, y = label_xy[name]
    ax.text(x, y, name.replace(" ", "\n").replace("·", "·\n"), ha="center",
            va="center", fontsize=8, color="black", zorder=5,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75))

ax.set_xlim(40, 78)
ax.set_ylim(0, 16)
ax.set_title("우리나라 신생대 화산암의 TAS 도표 (Le Bas 등, 1986 경계)")
ax.set_xlabel("SiO2 (wt.%, 휘발성분 제외 100% 환산)")
ax.set_ylabel("Na2O + K2O (wt.%)")
ax.legend(title="지역", loc="upper left", fontsize=9)
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_01"))
plt.show()

# 각 시료가 들어가는 TAS 영역 판정
points = tas[["SiO2", "total_alkali"]].to_numpy()
tas["tas_name"] = "분류 밖"
for name, verts in tas_fields.items():
    inside = MplPath(verts).contains_points(points) & (tas["tas_name"] == "분류 밖")
    tas.loc[inside, "tas_name"] = name

tas_counts = pd.crosstab(tas["tas_name"], tas["region"]).reindex(columns=region_order)
tas_counts["합계"] = tas_counts.sum(axis=1)
tas_counts.sort_values("합계", ascending=False)

# %% code Ⅴ-11.
fig, ax = plt.subplots(figsize=(7.8, 4))
sns.boxplot(data=tas, x="SiO2", y="region", order=region_order, ax=ax,
            color="lightsteelblue")
for x in [45, 52, 63]:
    ax.axvline(x, color="gray", lw=0.8, ls="--", alpha=0.7)
ax.set_title("지역별 SiO2 함량 분포")
ax.set_xlabel("SiO2 (wt.%)")
ax.set_ylabel("지역")
ax.grid(axis="x", alpha=0.3)
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_02"))
plt.show()

summary = tas.groupby("region").agg(
    n=("SiO2", "size"),
    SiO2_median=("SiO2", "median"), SiO2_min=("SiO2", "min"), SiO2_max=("SiO2", "max"),
    alkali_median=("total_alkali", "median"),
).reindex(region_order).round(1)
summary
