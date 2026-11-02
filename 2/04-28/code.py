# 지구과학 데이터 사이언스 2 | IV-08. 우리 바다의 수온
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 502.
# 필요한 라이브러리 불러오기
import io
from zipfile import ZipFile

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

%matplotlib inline

# 해역마다 쓸 색 정해 두기
COLOR = {"동해": "#2b6cb0", "남해": "#38a169", "서해": "#e2553d"}

# %% code 503.
# 데이터를 저장할 폴더를 만들고 압축 파일 내려받기
proj_dir = du.make_project_dir(du.current_notebook_name())

url = "https://www.nifs.go.kr/risa/cmmn/pastRisaInfoDown/total_2025.zip"
zip_path = os.path.join(proj_dir, "total_2025.zip")

if not os.path.exists(zip_path):                     # 이미 받아 두었으면 다시 받지 않음
    print("내려받는 중입니다 …")
    urllib.request.urlretrieve(url, zip_path)

print(f"파일 크기: {os.path.getsize(zip_path) / 1e6:.1f} MB")

# 바깥 압축 풀기(해역별 압축 파일 세 개가 나옴)
with ZipFile(zip_path) as z:
    print("안에 들어 있는 파일:", z.namelist())
    z.extractall(proj_dir)

# %% code 504.
SEA = {"es_2025": "동해", "ss_2025": "남해", "ys_2025": "서해"}   # 파일 이름 : 해역 이름
USE = ["관측소", "관측일시", "표층수온(℃)", "표층수심(m)", "저층수온(℃)",
       "저층수심(m)"]

frames = []
for key, sea in SEA.items():
    # 바깥 압축을 푼 total_2025 폴더 안의 해역별 압축 파일
    inner_zip = os.path.join(proj_dir, "total_2025", f"{key}.zip")
    with ZipFile(inner_zip) as z:                       # 안쪽 압축은 풀지 않고 바로 읽기
        for name in sorted(n for n in z.namelist() if n.endswith(".csv")):
            data = pd.read_csv(io.BytesIO(z.read(name)), encoding="cp949",
                               usecols=USE)
            data["해역"] = sea
            frames.append(data)

df = pd.concat(frames, ignore_index=True)               # 36개 표를 세로로 이어 붙이기

# 열 이름을 짧게 바꾸고 날짜와 지점 이름 정리
df = df.rename(columns={"표층수온(℃)": "표층수온", "저층수온(℃)": "저층수온",
                        "표층수심(m)": "표층수심", "저층수심(m)": "저층수심"})
df["관측일시"] = pd.to_datetime(df["관측일시"])
# 「강릉(bgna3)」에서 괄호 안 관측소 코드를 떼어 지점 이름만 남김
df["지점"] = df["관측소"].str.replace(r"\(.*\)$", "", regex=True).str.strip()

print(f"데이터 크기 : {df.shape[0]:,} 행 × {df.shape[1]} 열")
print(f"기간      : {df['관측일시'].min()} ~ {df['관측일시'].max()}")
df.head()

# %% code 505.
print("해역별 관측 지점 수")
print(df.groupby("해역")["지점"].nunique().to_string())

print("\n해역별 데이터 수")
print(df.groupby("해역").size().to_string())

print("\n비어 있는 값의 비율 (%)")
print((df[["표층수온", "저층수온"]].isna().mean() * 100).round(1).to_string())

print("\n관측 수심의 중앙값 (m)")
print(df.groupby("해역")[["표층수심", "저층수심"]].median().to_string())

# %% code 506.
# 하루 단위로 묶어 해역별 평균 수온 구하기
daily = (df.set_index("관측일시")
           .groupby("해역")["표층수온"]
           .resample("D").mean()
           .reset_index())

fig, ax = plt.subplots(figsize=(7.5, 3.5))
for sea in ["동해", "남해", "서해"]:
    one = daily[daily["해역"] == sea]
    ax.plot(one["관측일시"], one["표층수온"], color=COLOR[sea], linewidth=1.8,
            label=sea)

ax.set_title("2025년 우리나라 연안 표층 수온 (해역 평균)", fontsize=12,
             fontweight="bold")
ax.set_xlabel("날짜")
ax.set_ylabel("표층 수온 (°C)")
ax.legend(fontsize=10)
ax.grid(True, linestyle=":", alpha=0.5)

plt.tight_layout()
plt.show()

# %% code 507.
df["월"] = df["관측일시"].dt.month

# 행은 월, 열은 해역인 표 만들기
monthly = df.pivot_table(index="월", columns="해역", values="표층수온",
                         aggfunc="mean")
yearly_range = (monthly.max() - monthly.min()).reindex(["동해", "남해", "서해"])

fig, axes = plt.subplots(1, 2, figsize=(7.5, 2.9))

for sea in ["동해", "남해", "서해"]:
    axes[0].plot(monthly.index, monthly[sea], marker="o", color=COLOR[sea],
                 linewidth=2, label=sea)
axes[0].set_title("해역별 월평균 표층 수온", fontsize=12, fontweight="bold")
axes[0].set_xlabel("월")
axes[0].set_ylabel("수온 (°C)")
axes[0].set_xticks(range(1, 13))
axes[0].legend()
axes[0].grid(True, linestyle=":", alpha=0.5)

axes[1].bar(yearly_range.index, yearly_range.values,
            color=[COLOR[s] for s in yearly_range.index], alpha=0.85, edgecolor="black")
for i, v in enumerate(yearly_range.values):
    axes[1].text(i, v + 0.3, f"{v:.1f} °C", ha="center", fontsize=10,
                 fontweight="bold")
axes[1].set_title("해역별 수온 연교차", fontsize=12, fontweight="bold")
axes[1].set_ylabel("연교차 (°C)")
axes[1].set_ylim(0, yearly_range.max() * 1.15)
axes[1].grid(axis="y", linestyle=":", alpha=0.5)

plt.tight_layout()
plt.show()

print(monthly.round(1).to_string())

# %% code 508.
# 표층과 저층이 모두 기록된 데이터만 고르기
both = df.dropna(subset=["표층수온", "저층수온"]).copy()
both["수온차"] = both["표층수온"] - both["저층수온"]

# 동해 삼척 지점만 골라 하루 평균으로 정리
samcheok = (both[(both["해역"] == "동해") & (both["지점"] == "삼척")]
            .set_index("관측일시").sort_index()
            .resample("D")[["표층수온", "저층수온", "수온차"]].mean())

fig, axes = plt.subplots(2, 1, figsize=(7.5, 4.6), sharex=True)

axes[0].plot(samcheok.index, samcheok["표층수온"], color="#e2553d",
             linewidth=1.6, label="표층 (5 m)")
axes[0].plot(samcheok.index, samcheok["저층수온"], color="#2b6cb0",
             linewidth=1.6, label="저층 (25 m)")
axes[0].fill_between(samcheok.index, samcheok["저층수온"], samcheok["표층수온"],
                     where=samcheok["표층수온"] >= samcheok["저층수온"],
                     color="#f6ad55", alpha=0.4)
axes[0].set_title("동해 삼척 — 표층과 저층의 수온 (2025년)", fontsize=12,
                  fontweight="bold")
axes[0].set_ylabel("수온 (°C)")
axes[0].legend(fontsize=10)

axes[1].plot(samcheok.index, samcheok["수온차"], color="#6b46c1",
             linewidth=1.6)
axes[1].axhline(0, color="black", linewidth=0.8)
axes[1].set_title("표층 − 저층 수온차", fontsize=12, fontweight="bold")
axes[1].set_xlabel("날짜")
axes[1].set_ylabel("수온차 (°C)")

for ax in axes:
    ax.grid(True, linestyle=":", alpha=0.5)

plt.tight_layout()
plt.show()

print("월별 표층 − 저층 수온차 (°C)")
print(samcheok["수온차"].groupby(samcheok.index.month).mean().round(1).to_string())

# %% code 509.
df["날짜"] = df["관측일시"].dt.normalize()

# 정시·30분 관측만 사용 (불규칙 시각은 표본이 한두 개뿐이라 제외)
reg = df[df["관측일시"].dt.minute.isin([0, 30])].copy()
reg["시각"] = reg["관측일시"].dt.hour + reg["관측일시"].dt.minute / 60
print(f"불규칙 시각 데이터 {len(df) - len(reg):,}개 제외, "
      f"시각 칸 {reg['시각'].nunique()}개")

# 지점·날짜별 평균을 뺀 '그날 평균으로부터의 차이'
reg["일평균"] = reg.groupby(["지점", "날짜"])["표층수온"].transform("mean")
reg["편차"] = reg["표층수온"] - reg["일평균"]

SEASONS = {"겨울 (1~2월)": [1, 2], "여름 (7~8월)": [7, 8]}

fig, axes = plt.subplots(1, 2, figsize=(7.5, 2.7))
for ax, (label, months) in zip(axes, SEASONS.items()):
    sub = reg[reg["월"].isin(months)]
    for sea in ["동해", "남해", "서해"]:
        curve = sub[sub["해역"] == sea].groupby("시각")["편차"].mean()
        ax.plot(curve.index, curve.values, color=COLOR[sea], linewidth=2,
                label=sea)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title(f"{label} 하루 중 수온 변화", fontsize=12, fontweight="bold")
    ax.set_xlabel("시각 (시)")
    ax.set_ylabel("그날 평균과의 차 (°C)")
    ax.set_xticks(range(0, 25, 3))
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(fontsize=10)

plt.tight_layout()
plt.show()

for label, months in SEASONS.items():
    sub = reg[reg["월"].isin(months)]
    curve = sub.groupby(["해역", "시각"])["편차"].mean()
    # 시각 칸 하나에 들어간 가장 적은 표본 수
    n_min = sub.groupby(["해역", "시각"]).size().min()
    print(f"{label} (시각 칸 최소 표본 {n_min:,}개)")
    for sea in ["동해", "남해", "서해"]:
        c = curve[sea]
        print(f"  {sea} : 변화 폭 {c.max() - c.min():.2f} °C, "
              f"가장 높은 시각 {c.idxmax():4.1f}시, 가장 낮은 시각 {c.idxmin():4.1f}시")

# %% code 510.
import matplotlib.dates as mdates

THRESHOLD = 28.0     # 고수온 주의보 기준 (°C)

# 지점별·날짜별 최고 수온
daily_max = df.groupby(["해역", "지점", "날짜"])["표층수온"].max().reset_index()
hot = daily_max[daily_max["표층수온"] >= THRESHOLD]

hot_by_day = hot.groupby(["해역", "날짜"]).size().reset_index(name="지점수")
hot_by_station = hot.groupby(["해역", "지점"]).size().sort_values(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(7.5, 2.7))

for sea in ["동해", "남해", "서해"]:
    one = hot_by_day[hot_by_day["해역"] == sea]
    axes[0].plot(one["날짜"], one["지점수"], marker="o", markersize=3,
                 color=COLOR[sea], linewidth=1.4, label=sea)
axes[0].set_title(f"하루 최고 수온이 {THRESHOLD:.0f} °C 이상인 지점 수",
                  fontsize=12, fontweight="bold")
axes[0].set_xlabel("날짜 (월/일)")
axes[0].xaxis.set_major_locator(mdates.MonthLocator())
axes[0].xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
axes[0].set_ylabel("지점 수")
axes[0].legend()
axes[0].grid(True, linestyle=":", alpha=0.5)

top10 = hot_by_station.head(10)[::-1]
labels = [f"{name} ({sea})" for sea, name in top10.index]
axes[1].barh(labels, top10.values,
             color=[COLOR[sea] for sea, name in top10.index], alpha=0.85, edgecolor="black")
axes[1].set_title(f"{THRESHOLD:.0f} °C 이상을 기록한 날이 많은 지점",
                  fontsize=12, fontweight="bold")
axes[1].set_xlabel("일수")
axes[1].grid(axis="x", linestyle=":", alpha=0.5)

plt.tight_layout()
plt.show()

print(f"{THRESHOLD:.0f} °C 이상을 기록한 (지점, 날짜)의 수 : {len(hot):,}")
print(hot["해역"].value_counts().to_string())
print("\n연중 가장 높았던 수온")
top3 = df.nlargest(3, "표층수온")[["해역", "지점", "관측일시", "표층수온"]]
print(top3.to_string(index=False))
