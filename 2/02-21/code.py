# 지구과학 데이터 사이언스 2 | II-01. 측정과 오차 다루기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 19.
import numpy as np

rng = np.random.default_rng(0)          # 결과를 재현할 수 있게 씨앗 고정

TRUE_PERIOD = 2.000  # 참값(초) — 실제 실험에서는 알 수 없다
SIGMA = 0.05         # 한 번 잴 때의 우연오차 크기(초)

measurements = rng.normal(TRUE_PERIOD, SIGMA, size=20)   # 20번 측정
print("측정값 (앞 5개):", np.round(measurements[:5], 3))
print(f"측정 횟수 : {measurements.size}회")

# %% code 20.
mean = measurements.mean()              # 평균
std = measurements.std(ddof=1)          # 표준편차(표본)
sem = std / np.sqrt(measurements.size)  # 표준오차

print(f"평균     : {mean:.4f} 초")
print(f"표준편차 : {std:.4f} 초   (측정 하나의 흩어짐)")
print(f"표준오차 : {sem:.4f} 초   (평균의 오차)")
print(f"결과     : {mean:.3f} +/- {sem:.3f} 초")
print(f"참값과의 차이: {abs(mean - TRUE_PERIOD):.4f} 초")

# %% code 21.
import matplotlib.pyplot as plt

counts = np.arange(2, 201)                          # 측정 횟수 2회부터 200회까지
big_sample = rng.normal(TRUE_PERIOD, SIGMA, size=counts.max())
running_sem = [big_sample[:n].std(ddof=1) / np.sqrt(n) for n in counts]

fig, ax = plt.subplots(figsize=(8.4, 4.2))
ax.plot(counts, running_sem, label="표본으로 추정한 표준오차")
ax.plot(counts, SIGMA / np.sqrt(counts), "--",
        label=r"이론값 $\sigma/\sqrt{N}$")
ax.set_xlabel("측정 횟수 N")
ax.set_ylabel("평균의 표준오차 (초)")
ax.set_title("측정을 늘릴수록 평균은 얼마나 정확해지는가")
ax.legend()
ax.grid(alpha=0.3)
du.save_figure(fig, os.path.join(proj_dir, "standard_error"))
plt.show()

# %% code 22.
L, L_err = 1.000, 0.002  # 진자 길이 (m)
T, T_err = 2.000, 0.011  # 주기 (초)

g = 4 * np.pi**2 * L / T**2        # 중력가속도

rel_L = L_err / L
rel_T = T_err / T
rel_g = np.sqrt(rel_L**2 + (2 * rel_T)**2)
g_err = g * rel_g

print(f"길이 상대오차 : {rel_L*100:.2f}%")
print(f"주기 상대오차 : {rel_T*100:.2f}%  (제곱이라 {2*rel_T*100:.2f}%로 반영)")
print(f"g = {g:.2f} +/- {g_err:.2f} m/s^2  (상대오차 {rel_g*100:.2f}%)")

# %% code 23.
N = 100_000
L_samples = rng.normal(L, L_err, N)                  # 길이를 N번 뽑고
T_samples = rng.normal(T, T_err, N)                  # 주기도 N번 뽑아
g_samples = 4 * np.pi**2 * L_samples / T_samples**2  # 그때마다 g 계산

print(f"공식으로 구한 오차    : {g_err:.4f} m/s^2")
print(f"모의실험으로 구한 오차: {g_samples.std(ddof=1):.4f} m/s^2")

fig, ax = plt.subplots(figsize=(8.4, 4.2))
ax.hist(g_samples, bins=80, color="steelblue", alpha=0.8)
ax.axvline(g, color="red", lw=2, label=f"공식값 {g:.3f}")
ax.axvline(g - g_err, color="red", ls="--", lw=1)
ax.axvline(g + g_err, color="red", ls="--", lw=1, label="공식 오차 범위")
ax.set_xlabel("중력가속도 (m/s$^2$)")
ax.set_ylabel("빈도")
ax.set_title("오차 전파 공식과 모의실험 비교")
ax.legend()
du.save_figure(fig, os.path.join(proj_dir, "error_propagation"))
plt.show()

# %% code 24.
def format_result(value, error, sig=1):
    """측정값과 오차를 자릿수를 맞춰 보기 좋게 적는다."""
    if error <= 0:
        return f"{value:g}"
    # 오차의 첫 유효숫자가 있는 자릿수를 찾는다
    exponent = int(np.floor(np.log10(abs(error))))
    digits = -(exponent - (sig - 1))
    error_r = round(error, digits)
    # 반올림으로 자리가 올라가면(예: 0.0098 -> 0.010) 자릿수를 다시 계산
    exponent = int(np.floor(np.log10(abs(error_r))))
    digits = -(exponent - (sig - 1))
    error_r = round(error_r, digits)
    value_r = round(value, digits)
    if digits <= 0:
        return f"{value_r:.0f} +/- {error_r:.0f}"
    return f"{value_r:.{digits}f} +/- {error_r:.{digits}f}"

print("g       :", format_result(g, g_err))
print("주기    :", format_result(mean, sem))
print("예시 1  :", format_result(1234.5678, 12.3))
print("예시 2  :", format_result(0.0043219, 0.00007))
