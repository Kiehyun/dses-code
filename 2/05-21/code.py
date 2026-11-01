# 지구과학 데이터 사이언스 2 | V-01. 암석 데이터 분류하기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 517.
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

DATA_DIR = proj_dir
DATA_DIR.mkdir(exist_ok=True)

url = "https://macrostrat.org/api/v2/defs/lithologies?format=json"

# 공개 API에서 암상 정의 데이터 내려받기
response = requests.get(url, timeout=60)
response.raise_for_status()
data = response.json()

# API 응답의 success.data 부분이 실제 표 데이터
rocks = pd.DataFrame(data["success"]["data"])

# 나중에 인터넷 없이도 다시 볼 수 있도록 CSV로 저장
csv_file = DATA_DIR / "macrostrat_lithologies.csv"
rocks.to_csv(csv_file, index=False, encoding="utf-8-sig")

print(response.url)
print(f"데이터 개수: {len(rocks):,}")
print(f"저장 위치: {csv_file}")
rocks.head()

# %% code 518.
# 분석에 사용할 핵심 열만 먼저 확인
cols = ["lith_id", "name", "class", "type", "group", "color", "t_units"]
rocks[cols].head(15)

# %% code 519.
# 빈칸은 결측값이라기보다 상위 그룹이 지정되지 않은 경우가 많음
rocks["group"] = rocks["group"].replace("", "not specified")
rocks["class"] = rocks["class"].replace("", "not specified")

class_counts = rocks["class"].value_counts().rename_axis("class").reset_index(name="count")
class_counts

# %% code 520.
fig, ax = plt.subplots(figsize=(7.7, 4.2))
sns.barplot(data=class_counts, x="count", y="class", hue="class", legend=False,
            ax=ax, palette="Set2")
ax.set_title("Macrostrat 암상 정의의 대분류")
ax.set_xlabel("암상 이름 개수")
ax.set_ylabel("암석 대분류")
ax.grid(axis="x", alpha=0.3)
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_01"))
plt.show()

# %% code 521.
def simple_rock_classifier(name):
    """암석 이름에 들어 있는 단어로 대략적인 암석 분류를 반환"""
    text = str(name).lower()

    # 화성암에서 자주 보이는 이름
    igneous_words = ["basalt", "granite", "andesite", "rhyolite", "dacite",
                     "gabbro", "diorite", "tuff"]
    # 퇴적암에서 자주 보이는 이름
    sedimentary_words = ["sand", "shale", "limestone", "dolomite", "mud",
                         "silt", "conglomerate", "coal"]
    # 변성암에서 자주 보이는 이름
    metamorphic_words = ["gneiss", "schist", "slate", "marble", "quartzite",
                         "amphibolite"]

    if any(word in text for word in igneous_words):
        return "igneous"
    if any(word in text for word in sedimentary_words):
        return "sedimentary"
    if any(word in text for word in metamorphic_words):
        return "metamorphic"
    return "unknown"

rocks["rule_class"] = rocks["name"].apply(simple_rock_classifier)
rocks[["name", "class", "rule_class"]].head(20)

# %% code 522.
# 규칙 기반 분류가 Macrostrat의 class와 얼마나 비슷한지 비교
comparison = pd.crosstab(rocks["class"], rocks["rule_class"])

# 대각선(실제 분류 = 규칙 분류) 개수로 정확도 계산
n_correct = (rocks["class"] == rocks["rule_class"]).sum()
n_unknown = (rocks["rule_class"] == "unknown").sum()
print(f"규칙이 맞힌 개수: {n_correct}/{len(rocks)} ({n_correct / len(rocks):.0%})")
print(f"unknown 개수: {n_unknown}")
comparison
