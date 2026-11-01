# 지구과학 데이터 사이언스 2 | V-04. 방사성 동위원소 연대측정 기초
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 565.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from io import StringIO
import requests

DATA_DIR = proj_dir
DATA_DIR.mkdir(exist_ok=True)

# 대표적인 방사성 연대측정 계의 반감기
half_lives = pd.DataFrame([
    {"system": "C-14", "half_life_year": 5730,
     "typical_use": "유기물, 고고학적 시료"},
    {"system": "K-40 (전체, Ar 분기 약 10.6%)", "half_life_year": 1.269e9,
     "typical_use": "화산암, 화성암 (K-Ar, Ar-Ar)"},
    {"system": "U-238 to Pb-206", "half_life_year": 4.468e9,
     "typical_use": "지르콘, 오래된 암석"},
    {"system": "U-235 to Pb-207", "half_life_year": 7.04e8,
     "typical_use": "지르콘, 오래된 암석"},
])
half_lives

# %% code 566.
fig, ax = plt.subplots(figsize=(8.5, 4.4))

for row in half_lives.itertuples(index=False):
    # 각 동위원소마다 5번의 반감기가 지나는 구간까지 계산
    t = np.linspace(0, row.half_life_year * 5, 300)
    remaining = 0.5 ** (t / row.half_life_year)
    ax.plot(t / row.half_life_year, remaining, label=row.system)

ax.set_title("반감기 단위로 본 방사성 붕괴 곡선")
ax.set_xlabel("경과 시간 / 반감기")
ax.set_ylabel("남은 모원소 비율")
ax.grid(alpha=0.3)
ax.legend()
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_01"))
plt.show()

# %% code 567.
def age_from_remaining_fraction(remaining_fraction, half_life_year):
    """남은 모원소 비율과 반감기로 연대를 계산"""
    remaining_fraction = np.asarray(remaining_fraction, dtype=float)
    return -np.log2(remaining_fraction) * half_life_year

# 예: U-238 → Pb-206 계
remaining = np.array([0.95, 0.90, 0.75, 0.60, 0.50])
u238_half_life = 4.468e9
ages = age_from_remaining_fraction(remaining, u238_half_life)

pd.DataFrame({
    "remaining_fraction": remaining,
    "age_year": ages,
    "age_Ma": ages / 1e6,
})

# %% code 568.
# 40K 붕괴 상수 (Min et al., 2000), 단위 1/년
lambda_e = 0.580e-10     # 40K → 40Ar (전자포획)
lambda_beta = 4.883e-10  # 40K → 40Ca (베타 붕괴)
lambda_total = lambda_e + lambda_beta
print(f"전체 붕괴 상수: {lambda_total:.3e} /년, "
      f"반감기: {np.log(2) / lambda_total / 1e9:.3f} Ga")
print(f"Ar 분기 비율 lambda_e / lambda: {lambda_e / lambda_total:.4f}")

# 비교용: 옛 표준값 (Steiger & Jäger, 1977)
lambda_e_sj, lambda_beta_sj = 0.581e-10, 4.962e-10

def age_k_ar(ar_k_ratio, lam_e=lambda_e, lam_b=lambda_beta):
    """방사성 40Ar*/40K 비율로 K-Ar 연대(년)를 계산"""
    ar_k_ratio = np.asarray(ar_k_ratio, dtype=float)
    lam = lam_e + lam_b
    return np.log(1 + lam / lam_e * ar_k_ratio) / lam

ar_k = np.array([0.0001, 0.001, 0.01, 0.05, 0.1])
age_min = age_k_ar(ar_k)
age_sj = age_k_ar(ar_k, lambda_e_sj, lambda_beta_sj)
# 분기 비율을 무시한 잘못된 계산: N0 = K + Ar
age_wrong = age_from_remaining_fraction(1 / (1 + ar_k), np.log(2) / lambda_total)

pd.DataFrame({
    "Ar40_K40_ratio": ar_k,
    "age_Ma": age_min / 1e6,
    "age_Ma_SJ1977": age_sj / 1e6,
    "diff_percent": (age_sj / age_min - 1) * 100,
    "age_Ma_no_branching": age_wrong / 1e6,
}).round({"age_Ma": 2, "age_Ma_SJ1977": 2, "diff_percent": 2, "age_Ma_no_branching": 2})

# %% code 569.
measurement_error = np.linspace(-0.03, 0.03, 61)
rows = []

fig, ax = plt.subplots(figsize=(8.6, 4.4))
for true_remaining, color in [(0.75, "tab:blue"), (0.25, "darkorange"), (0.05, "tab:red")]:
    measured_remaining = true_remaining + measurement_error
    # 연대를 반감기 단위로 (반감기 = 1)
    age_hl = age_from_remaining_fraction(measured_remaining, 1.0)
    ax.plot(measured_remaining, age_hl, color=color)
    ax.axvline(true_remaining, color=color, ls="--", lw=1,
               label=f"참값 {true_remaining}")
    rows.append({"true_remaining": true_remaining,
                 "age_true_hl": age_from_remaining_fraction(true_remaining, 1.0),
                 "age_min_hl": age_hl.min(), "age_max_hl": age_hl.max(),
                 "spread_hl": age_hl.max() - age_hl.min()})

ax.set_title("모원소 비율 측정 오차(±0.03)와 계산 연대")
ax.set_xlabel("측정된 남은 모원소 비율")
ax.set_ylabel("계산 연대 (반감기 단위)")
ax.grid(alpha=0.3)
ax.legend()
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_02"))
plt.show()

pd.DataFrame(rows).round(3)

# %% code 570.
url = "https://data.goettingen-research-online.de/api/access/datafile/40582"
raw_file = DATA_DIR / "Ball_2022_intraplate_volcanics.csv"
if not raw_file.exists():  # 이미 받아 둔 파일은 다시 받지 않음
    response = requests.get(url, timeout=180)
    response.raise_for_status()
    raw_file.write_bytes(response.content)  # 받은 바이트 그대로 저장

# 맨 위 세 줄(이용 허락 · 인용 문구)은 건너뜀
ball = pd.read_csv(raw_file, skiprows=3, encoding="latin-1", low_memory=False)
kor = ball[ball["Region"] == "Korea"].copy()

province_ko = {
    "Jeju Island": "제주도", "Jeju Island / Ilchulbong": "제주도",
    "Udo": "우도(제주)", "Ulleung": "울릉도", "Baengnyeong": "백령도",
    "Chongok": "한탄강 일대", "Chatan": "한탄강 일대", "Jeongok Basalt": "한탄강 일대",
    "Gyeonggi": "경기 지역",
}
kor["region"] = kor["Province"].map(province_ko)
kor["Uncertainty"] = pd.to_numeric(kor["Uncertainty"], errors="coerce")
kor["is_radiometric"] = kor["Method"].isin(["Ar-Ar", "K-Ar"])

print(f"전체 시료 수: {len(ball):,}")
print(f"우리나라 시료 수: {len(kor):,}")
pd.crosstab(kor["region"], kor["Method"], margins=True, margins_name="합계")

# %% code 571.
fig, ax = plt.subplots(figsize=(8.5, 4.2))
bins = np.arange(0, 7.0, 0.25)
ax.hist([kor.loc[kor["is_radiometric"], "Age"], kor.loc[~kor["is_radiometric"], "Age"]],
        bins=bins, stacked=True, color=["crimson", "lightgray"],
        label=["방사성 연대(Ar-Ar, K-Ar)", "층서 연대(지층 연대를 붙임)"])
ax.set_title("우리나라 신생대 화산암 시료의 연대 분포")
ax.set_xlabel("연대 (Ma)")
ax.set_ylabel("시료 수")
ax.legend()
ax.grid(alpha=0.3)
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_03"))
plt.show()

# %% code 572.
# 지역 · 방법 · 연대 · 오차가 같은 시료를 한 묶음으로
age_groups = (kor.groupby(["region", "Method", "Age", "Uncertainty"])
              .size().reset_index(name="n_samples")
              .sort_values("Age").reset_index(drop=True))

fig, ax = plt.subplots(figsize=(6.8, 4.2))
for is_radio, color in [(False, "gray"), (True, "crimson")]:
    part = age_groups[age_groups["Method"].isin(["Ar-Ar", "K-Ar"]) == is_radio]
    ax.errorbar(part["Age"], part.index, xerr=part["Uncertainty"], fmt="o",
                color=color, capsize=3,
                label="방사성 연대" if is_radio else "층서 연대")
ax.set_yticks(age_groups.index)
ax.set_yticklabels(age_groups["region"] + " (" + age_groups["Method"] + ", "
                   + age_groups["n_samples"].astype(str) + "개)", fontsize=9)
ax.set_title("연대값과 오차 (같은 값끼리 묶음)")
ax.set_xlabel("연대 (Ma)")
ax.grid(alpha=0.3)
ax.legend(loc="lower right")
du.save_figure(plt.gcf(), os.path.join(str(proj_dir), f"{proj_dir.name}_04"))
plt.show()

age_groups
