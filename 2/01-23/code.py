# 지구과학 데이터 사이언스 2 | I-03. AI 코딩 도우미로 데이터 분석하기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 12.
import numpy as np
import pandas as pd

rng = np.random.default_rng(0)                       # 같은 난수가 나오도록 씨앗 고정
days = pd.date_range("2025-01-01", "2025-12-31", freq="D")
doy = days.dayofyear.to_numpy()

season = -np.cos(2 * np.pi * (doy - 15) / 365)       # 1월 중순 -1, 7월 중순 +1
tmean = 12.5 + 14.5 * season                         # 일평균기온의 계절 변화(°C)
drange = 8.5 + 1.5 * np.cos(4 * np.pi * (doy - 105) / 365)  # 일교차(반년 주기: 4·10월 최대, 1·7월 최소)

df = pd.DataFrame({
    "tmax": tmean + drange / 2 + rng.normal(0, 2.0, len(days)),
    "tmin": tmean - drange / 2 + rng.normal(0, 2.0, len(days)),
}, index=days)
df.head()

# %% code 13.
import matplotlib.pyplot as plt

ai = df.copy()
ai["month"] = ai.index.month.astype(str) + "월"           # 1월, 2월, … 을 글자로 만든다
ai["range"] = ai["tmax"] - ai["tmin"]
monthly = ai.groupby("month")[["tmax", "tmin", "range"]].mean()

fig, ax = plt.subplots(figsize=(8.5, 4))
monthly.plot(ax=ax, marker="o")
ax.set_xlabel("월")
ax.set_ylabel("기온 (°C)")
ax.set_title("AI가 처음 그린 그래프")
plt.show()
print(list(monthly.index))

# %% code 14.
expected = [f"{m}월" for m in range(1, 13)]
print("월 순서가 1월~12월인가? ", list(monthly.index) == expected)

july_direct = df.loc[df.index.month == 7, "tmax"].mean()     # 다른 방법으로 다시 계산
print("7월 평균 최고기온이 같은가?",
      np.isclose(july_direct, monthly.loc["7월", "tmax"]))

# %% code 15.
import os

fixed = (df.assign(range=df["tmax"] - df["tmin"])
         .groupby(df.index.month)[["tmax", "tmin", "range"]].mean())

fig, ax = plt.subplots(figsize=(8.5, 4))
ax.plot(fixed.index, fixed["tmax"], marker="o", label="평균 최고기온")
ax.plot(fixed.index, fixed["tmin"], marker="o", label="평균 최저기온")
ax.plot(fixed.index, fixed["range"], marker="s", label="평균 일교차")
ax.set_xticks(range(1, 13))
ax.set_xticklabels([f"{m}월" for m in range(1, 13)])
ax.set_ylabel("기온 (°C)")
ax.set_title("고친 그래프 — 월별 기온과 일교차")
ax.grid(True, alpha=0.4)
ax.legend()
du.save_figure(fig, os.path.join(str(proj_dir), f"{proj_dir.name}_01"))
plt.show()

print("월 순서가 1~12인가?", list(fixed.index) == list(range(1, 13)))
