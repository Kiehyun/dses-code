# 지구과학 데이터 사이언스 2 | II-03. 시계열에서 주기 찾기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 32.
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(2)

YEARS = 10
PER_YEAR = 12                                  # 한 달에 한 번 관측
time = np.arange(YEARS * PER_YEAR) / PER_YEAR  # 단위: 년

trend = 2.0 * time                         # 해마다 2씩 증가
seasonal = 5.0 * np.sin(2 * np.pi * time)  # 1년 주기, 진폭 5
noise = rng.normal(0, 1.0, time.size)      # 잡음
series = 350 + trend + seasonal + noise    # 셋을 겹친 관측값

print(f"데이터 길이 : {series.size}개 ({YEARS}년 치, 월 1회)")
print(f"값의 범위 : {series.min():.1f} ~ {series.max():.1f}")

# %% code 33.
fig, ax = plt.subplots(figsize=(8.5, 3.8))
ax.plot(time, series, "o-", ms=3, lw=0.8, color="steelblue", label="관측값")
ax.plot(time, 350 + trend, "r--", lw=2, label="숨어 있는 추세")
ax.set_xlabel("시간 (년)")
ax.set_ylabel("농도 (임의 단위)")
ax.set_title("추세 + 계절 변동 + 잡음이 겹친 시계열")
ax.legend()
ax.grid(alpha=0.3)
du.save_figure(fig, os.path.join(proj_dir, "timeseries"))
plt.show()

# %% code 34.
def moving_average(values, window):
    """가장자리를 잘라내지 않고 같은 길이로 돌려주는 이동평균."""
    kernel = np.ones(window) / window
    padded = np.pad(values, (window // 2, window - 1 - window // 2),
                    mode="edge")
    return np.convolve(padded, kernel, mode="valid")


fig, ax = plt.subplots(figsize=(8.5, 3.8))
ax.plot(time, series, color="lightgray", lw=1, label="원시 데이터")
for window, color in zip((3, 12, 36), ("orange", "red", "green")):
    ax.plot(time, moving_average(series, window), color=color, lw=1.8,
            label=f"{window}개월 이동평균")
ax.set_xlabel("시간 (년)")
ax.set_ylabel("농도 (임의 단위)")
ax.set_title("창 크기에 따라 달라지는 이동평균")
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
du.save_figure(fig, os.path.join(proj_dir, "moving_average"))
plt.show()

# %% code 35.
trend_estimated = moving_average(series, 12)  # 12개월 평균 = 추세 추정
detrended = series - trend_estimated          # 추세를 뺀 나머지

print(f"원시 데이터 표준편차 : {series.std():.2f}")
print(f"추세 제거 후 표준편차: {detrended.std():.2f}")
print(f"넣어 둔 계절 진폭    : 5.0  ->  추정 진폭 약 {detrended.std()*np.sqrt(2):.2f}")

# %% code 36.
values = detrended - detrended.mean()             # 평균도 0으로 맞춘다
n = values.size
dt = 1 / PER_YEAR                                 # 표본 간격(년)

spectrum = np.fft.rfft(values)     # 실수 데이터용 푸리에 변환
freqs = np.fft.rfftfreq(n, d=dt)   # 진동수 (1/년)
power = np.abs(spectrum) ** 2 / n  # 진동수별 세기

peak = np.argmax(power[1:]) + 1                   # 0번(평균) 제외하고 최대
print(f"가장 강한 진동수 : {freqs[peak]:.3f}회/년")
print(f"그에 해당하는 주기: {1/freqs[peak]:.2f} 년")

# %% code 37.
fig, ax = plt.subplots(figsize=(8.5, 4))
ax.plot(freqs[1:], power[1:], color="steelblue")
ax.axvline(1.0, color="red", ls="--", lw=1, label="1년 주기(넣어 둔 값)")
ax.plot(freqs[peak], power[peak], "ro", ms=8, label="찾아낸 봉우리")
ax.set_xlabel("진동수 (회/년)")
ax.set_ylabel("세기")
ax.set_title("주기도 — 데이터에 숨은 주기 찾기")
ax.legend()
ax.grid(alpha=0.3)
du.save_figure(fig, os.path.join(proj_dir, "periodogram"))
plt.show()

# %% code 38.
nyquist = 1 / (2 * dt)
print(f"표본 간격 : {dt*12:.0f}개월")
print(f"나이키스트 진동수 : {nyquist:.1f}회/년  (최소 {1/nyquist*12:.0f}개월 주기까지)")

# 되말림 확인
alias_freq = abs(8 - round(8 / (2*nyquist)) * 2 * nyquist)
print(f"\n실제 진동수 8회/년 -> 관측에서는 {alias_freq:.1f}회/년처럼 보인다")
