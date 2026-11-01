# 지구과학 데이터 사이언스 2 | II-02. 곡선 맞춤과 모형 평가
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 25.
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(1)

TRUE_SLOPE, TRUE_INTERCEPT = 2.5, 1.0        # 참값(실제로는 모르는 값)
x = np.linspace(0, 10, 25)
y = TRUE_SLOPE * x + TRUE_INTERCEPT + rng.normal(0, 1.5, x.size)

print("데이터 점 개수:", x.size)
print("x 범위 :", x.min(), "~", x.max())
print("y 범위 :", round(y.min(), 2), "~", round(y.max(), 2))

# %% code 26.
slope, intercept = np.polyfit(x, y, 1)  # 1차 = 직선 맞춤
y_fit = slope * x + intercept           # 맞춘 직선의 예측값
residual = y - y_fit                    # 잔차 = 실제값 - 예측값

print(f"맞춘 기울기 : {slope:.3f}  (참값 {TRUE_SLOPE})")
print(f"맞춘 절편   : {intercept:.3f}  (참값 {TRUE_INTERCEPT})")
print(f"잔차 제곱합 : {np.sum(residual**2):.2f}")
print(f"잔차 평균   : {residual.mean():.3e}  (최소제곱이면 거의 0)")

# %% code 27.
fig, axes = plt.subplots(2, 1, figsize=(8.5, 5.5), sharex=True,
                         gridspec_kw={"height_ratios": [2, 1]})

axes[0].scatter(x, y, color="steelblue", label="관측값")
axes[0].plot(x, y_fit, "r-", lw=2,
             label=f"맞춘 직선 y={slope:.2f}x+{intercept:.2f}")
axes[0].vlines(x, y_fit, y, color="gray", lw=0.8)   # 잔차를 선으로 표시
axes[0].set_ylabel("y")
axes[0].set_title("최소제곱 직선 맞춤과 잔차")
axes[0].legend()

axes[1].axhline(0, color="red", lw=1)
axes[1].scatter(x, residual, color="darkorange")
axes[1].set_xlabel("x")
axes[1].set_ylabel("잔차")
axes[1].grid(alpha=0.3)

du.save_figure(fig, os.path.join(proj_dir, "linear_fit"))
plt.show()

# %% code 28.
from scipy.optimize import curve_fit

def decay(t, amplitude, tau, offset):
    """지수 감소 모형: 바닥값 위의 몫이 시간상수 tau마다 1/e(약 0.37)배로 줄어듦"""
    return amplitude * np.exp(-t / tau) + offset


t = np.linspace(0, 20, 40)
true_params = (100.0, 5.0, 10.0)                       # 진폭, 시간상수, 바닥값
signal = decay(t, *true_params) + rng.normal(0, 3.0, t.size)

params, covariance = curve_fit(decay, t, signal, p0=(80, 3, 5))
errors = np.sqrt(np.diag(covariance))                  # 대각성분의 제곱근 = 표준오차

for name, fit, err, true in zip(["진폭", "시간상수", "바닥값"],
                                params, errors, true_params):
    pad = " " * (10 - 2 * len(name))                    # 한글 한 글자는 두 칸 너비
    print(f"{name}{pad}: {fit:7.2f} +/- {err:5.2f}   (참값 {true})")

# %% code 29.
fig, ax = plt.subplots(figsize=(8.5, 4.2))
ax.scatter(t, signal, s=25, color="steelblue", label="관측값")
t_smooth = np.linspace(t.min(), t.max(), 300)
ax.plot(t_smooth, decay(t_smooth, *params), "r-", lw=2, label="맞춘 곡선")
ax.set_xlabel("시간")
ax.set_ylabel("신호 세기")
ax.set_title(f"지수 감소 모형 맞춤 (시간상수 {params[1]:.2f})")
ax.legend()
ax.grid(alpha=0.3)
du.save_figure(fig, os.path.join(proj_dir, "curve_fit"))
plt.show()

# %% code 30.
def r_squared(observed, predicted):
    """결정계수: 1에 가까울수록 모형이 데이터의 변동을 잘 설명한 것."""
    ss_residual = np.sum((observed - predicted) ** 2)
    ss_total = np.sum((observed - observed.mean()) ** 2)
    return 1 - ss_residual / ss_total


print("직선 맞춤 R^2      :", round(r_squared(y, y_fit), 4))
print("지수 모형 R^2      :", round(r_squared(signal, decay(t, *params)), 4))

print("\n다항식 차수별 R^2 (같은 데이터)")
for degree in (1, 3, 7, 15):
    coefficients = np.polyfit(x, y, degree)
    print(f"  {degree:2d}차 : {r_squared(y, np.polyval(coefficients, x)):.4f}")

# %% code 31.
x_dense = np.linspace(x.min() - 0.5, x.max() + 0.5, 400)   # 데이터 범위보다 조금 넓게

fig, ax = plt.subplots(figsize=(8.5, 4.4))
ax.scatter(x, y, color="steelblue", zorder=3, label="관측값")
for degree, style in zip((1, 15), ("r-", "g--")):
    coefficients = np.polyfit(x, y, degree)
    ax.plot(x_dense, np.polyval(coefficients, x_dense), style, lw=1.8,
            label=f"{degree}차 다항식")
ax.set_ylim(y.min() - 5, y.max() + 5)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("차수를 올리면 잘 맞는 것처럼 보이지만")
ax.legend()
ax.grid(alpha=0.3)
du.save_figure(fig, os.path.join(proj_dir, "overfitting"))
plt.show()
