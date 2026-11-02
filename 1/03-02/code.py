# 지구과학 데이터 사이언스 1 | III-02. 행성의 물리량 계산
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 23.
import re
import time
from functools import lru_cache
from io import StringIO

import numpy as np
import pandas as pd
import requests

# 위키백과 API 정책: 연락처가 담긴 사용자 에이전트를 쓴다
headers = {"User-Agent": "DSES-book/1.0 (https://github.com/Kiehyun/dses-code)"}

# 각주/특수 공백을 제거해 비교 가능한 문자열로 정리
def clean_text(text):
    s = re.sub(r"\[[^\]]*\]", "", str(text))
    s = s.replace("\xa0", " ").replace("−", "-").replace("–", "-")
    return " ".join(s.split())

# 텍스트에서 첫 번째 수치를 추출(과학 표기 포함)
def first_float(text):
    s = clean_text(text).replace(",", "")
    m = re.search(r"([-+]?\d*\.?\d+)\s*[x×*]\s*10(?:\^|\s*)\s*([-+]?\d+)", s, flags=re.I)
    if m:
        return float(m.group(1)) * (10 ** int(m.group(2)))
    m = re.search(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", s)
    return float(m.group()) if m else np.nan

def second_float(text):
    s = clean_text(text).replace(",", "")
    nums = re.findall(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", s)
    return float(nums[1]) if len(nums) >= 2 else np.nan

# 1/298 형태의 편평도 표기도 수치로 변환
def parse_flattening(text):
    s = clean_text(text)
    reciprocal = re.search(r"1\s*/\s*(\d+(?:\.\d+)?)", s)
    if reciprocal:
        return 1.0 / float(reciprocal.group(1))
    return first_float(s)

# 정보상자의 알베도 칸에는 본드(Bond) · 기하(geometric) 알베도가 함께 적혀 있음
# → 'Bond' 앞의 수치만 골라냄(복사 평형 계산에는 본드 알베도를 씀)
def bond_albedo(text):
    m = re.search(r"(\d*\.\d+)\s*\(?\s*bond", clean_text(text), flags=re.I)
    return float(m.group(1)) if m else np.nan

def get_row_key(df, prefix):
    return next(i for i in df.index if clean_text(i).startswith(prefix))

# 행성 문서는 한 번만 받아 둔다 — 같은 문서를 거듭 요청하면 API가 429(요청 과다)로 막는다
@lru_cache(maxsize=None)
def get_page_html(page):
    for wait in (0, 5, 15, 30):
        time.sleep(wait)
        r = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={"action": "parse", "page": page, "prop": "text", "format": "json", "redirects": 1},
            headers=headers, timeout=20,
        )
        if r.status_code != 429:
            break
    r.raise_for_status()
    return r.json()["parse"]["text"]["*"]

# 행성 개별 문서의 infobox에서 원하는 항목 값을 읽음
def get_infobox_value(page, aliases):
    info = pd.read_html(StringIO(get_page_html(page)))[0].fillna("")
    kcol = info.columns[0]
    for _, row in info.iterrows():
        key = clean_text(row[kcol]).lower()
        if any(alias in key for alias in aliases):
            return clean_text(" ".join(str(x) for x in row.tolist()[1:]))
    return ""

# JSON 데이터 1: 태양계 비교표를 주는 MediaWiki API
js = requests.get(
    "https://en.wikipedia.org/w/api.php",
    params={
        "action": "parse",
        "page": "List_of_gravitationally_rounded_objects_of_the_Solar_System",
        "prop": "text",
        "format": "json",
        "redirects": 1,
    },
    headers=headers,
    timeout=20,
).json()
wiki_table = pd.read_html(StringIO(js["parse"]["text"]["*"]))[2]

# 8개 행성 열만 선택
planet_cols = [
    c
    for c in wiki_table.columns
    if any(
        p in str(c)
        for p in ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
    )
]

w = wiki_table[["Unnamed: 0", "Unnamed: 1"] + planet_cols].copy()
w.columns = [
    "field", "unit", "Mercury", "Venus",
    "Earth", "Mars",  "Jupiter", "Saturn", "Uranus",
    "Neptune", ]
# 항목명(field)을 인덱스로 바꿔 이후 조회를 단순화
w = w.dropna(subset=["field"]).set_index("field")

# JSON 데이터 2: 행성별 정보상자 API(편평도, 반사율)
planet_pages = {
    "Mercury": "Mercury_(planet)",
    "Venus": "Venus", "Earth": "Earth", "Mars": "Mars", 
    "Jupiter": "Jupiter", "Saturn": "Saturn", "Uranus": "Uranus",
    "Neptune": "Neptune",
}

ko_name = {
    "Mercury": "수성", "Venus": "금성",
    "Earth": "지구", "Mars": "화성",
    "Jupiter": "목성", "Saturn": "토성",
    "Uranus": "천왕성",
    "Neptune": "해왕성",
}

planet_order = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

# 비교표에서 필요한 행 이름(키) 미리 찾기
distance_key = get_row_key(w, "Mean distance from the Sun")
inclination_key = get_row_key(w, "Inclination")
eccentricity_key = get_row_key(w, "Eccentricity")
rotation_key = get_row_key(w, "Rotation period")
moons_key = get_row_key(w, "Number of known moons")
axial_tilt_key = get_row_key(w, "Axial tilt")
atmosphere_key = get_row_key(w, "Atmospheric composition")
rings_key = get_row_key(w, "Rings?")
radius_key = get_row_key(w, "Equatorial radius")
mass_key = get_row_key(w, "Mass")

# 수집한 원본 데이터 확인
preview_keys = [
    radius_key, mass_key, distance_key, inclination_key, eccentricity_key,
    rotation_key, moons_key,
]

print("행성 순서:", planet_order)
print("\n비교표 추출값 미리보기:")
display(w.loc[preview_keys, planet_order])

# %% code 24.
import pandas as pd

# 행성별 레코드 만들기
rows = []
for en in planet_order:
    flattening_text = get_infobox_value(planet_pages[en], ["flattening"])
    albedo_text = get_infobox_value(planet_pages[en], ["albedo"])

    ring_text = clean_text(w.loc[rings_key, en]).lower()
    has_ring = "Yes" if ring_text.startswith("yes") else "No"

    rows.append(
        {
            "행성": ko_name[en],
            "영어이름": en,
            "적도반지름(km)": first_float(w.loc[radius_key, en]),
            "편평도": parse_flattening(flattening_text),
            "질량(kg)": first_float(w.loc[mass_key, en]),
            "장반경(AU)": second_float(w.loc[distance_key, en]),
            "본드 알베도": bond_albedo(albedo_text),
            "태양 적도에 대한 경사각(도)": first_float(w.loc[inclination_key, en]),
            "궤도 이심률": first_float(w.loc[eccentricity_key, en]),
            "자전 주기(days)": first_float(w.loc[rotation_key, en]),
            "확인된 위성 수": int(first_float(w.loc[moons_key, en])),
            "축 경사각(도)": first_float(w.loc[axial_tilt_key, en]),
            "고리": has_ring,
            "대기": clean_text(w.loc[atmosphere_key, en]),
        }
    )

columns = [
    "행성", "영어이름", "적도반지름(km)", "편평도", "질량(kg)", "장반경(AU)",
    "본드 알베도", "태양 적도에 대한 경사각(도)", "궤도 이심률", "자전 주기(days)",
    "확인된 위성 수", "축 경사각(도)", "고리", "대기",
]

df = pd.DataFrame(rows, columns=columns)

df.to_csv("planet_attributes.csv", index=False)

df = df.set_index("행성")
display(df)

# %% code 25.
print("df.index: {}".format(df.index))
print("df.columns: {}".format(df.columns))

print("type(df.loc['수성', '질량(kg)']): ", type(df.loc['수성', '질량(kg)']))
print("df.loc['수성', '질량(kg)']: ", df.loc['수성', '질량(kg)'])

# %% code 26.
df['상대 질량'] = df["질량(kg)"]/df.loc["지구", "질량(kg)"]
df['적도 반지름(상댓값)'] = df["적도반지름(km)"]/df.loc["지구", "적도반지름(km)"]
df['부피(상댓값)'] = df['적도 반지름(상댓값)']**3
print("df['부피(상댓값)']:\n", df['부피(상댓값)'])
# print("df:\n", df)

# %% code 27.
import astropy.units as u
import astropy.constants as const
import numpy as np

# 공전주기 계산(케플러 제3법칙)
df['공전주기(년)'] = (2 * np.pi * ((df["장반경(AU)"].values * u.AU)**3 / const.GM_sun)**0.5).to(u.year).value

# 평균반지름 계산(편평도 고려): 부피가 같은 구의 반지름
df['평균반지름(km)'] = df["적도반지름(km)"] * (1 - df["편평도"])**(1/3)

# 평균 밀도 계산(평균반지름 사용)
df['평균 밀도 (g cm^-3)'] = (3 * (df["질량(kg)"].values * u.kg) / (4 * np.pi * (df["평균반지름(km)"].values * u.km)**3)).to(u.g / u.cm**3).value

# 적도에서의 인력 가속도(만유인력만, 자전에 따른 원심 효과는 넣지 않음)
df['적도 인력 가속도(m s^-2)'] = (const.G * (df["질량(kg)"].values * u.kg) / (df["적도반지름(km)"].values * u.km)**2).to(u.m / u.s**2).value

print("df[['공전주기(년)', '평균반지름(km)', '평균 밀도 (g cm^-3)', '적도 인력 가속도(m s^-2)']]:\n", df[['공전주기(년)', '평균반지름(km)', '평균 밀도 (g cm^-3)', '적도 인력 가속도(m s^-2)']] )

# %% code 28.
# 지구의 태양상수
solar_constant0 = const.L_sun / (4 * np.pi * const.au**2)
print(f"Solar constant (Earth): {solar_constant0.value:.2f} {solar_constant0.unit}")

df["태양상수(W m^-2)"] = const.L_sun / (4 * np.pi * (df["장반경(AU)"] *u.au.to(u.m))**2)
df["태양상수(W m^-2)"]

# %% code 29.
df["입사량(W)"] = ((1 - df["본드 알베도"]) * np.pi * (df["평균반지름(km)"] * u.km.to(u.m))**2 * df["태양상수(W m^-2)"]).values
# 복사평형온도 계산
df["복사평형온도(K)"] = ((((1 - df["본드 알베도"]) * (df["태양상수(W m^-2)"]) * u.W/u.m**2) / (4 * const.sigma_sb))**(1/4))
print("df[['입사량(W)', '복사평형온도(K)']]:\n", df[['입사량(W)', '복사평형온도(K)']] )

# %% code 30.
df.to_csv('result_of_calculations.csv')
print("계산 결과가 'result_of_calculations.csv' 파일로 저장되었습니다.")
