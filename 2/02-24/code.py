# 지구과학 데이터 사이언스 2 | II-04. 기체 분자 운동과 맥스웰-볼츠만 분포
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 40.
import numpy as np
import matplotlib.pyplot as plt
from scipy import constants

plt.rcParams.update({"axes.titlesize": 13, "axes.labelsize": 11,
                     "xtick.labelsize": 9, "ytick.labelsize": 9,
                     "legend.fontsize": 9})

k_B = constants.k            # 볼츠만 상수 (J/K)
amu = constants.atomic_mass  # 원자 질량 단위 (kg)

def mb_speed_3d(v, m, T):
    """3차원 맥스웰-볼츠만 속력 분포 f(v) (단위: s/m)"""
    a = m / (2 * k_B * T)
    return 4 * np.pi * (a / np.pi) ** 1.5 * v**2 * np.exp(-a * v**2)

def mb_speed_2d(v, m, T):
    """2차원 맥스웰-볼츠만 속력 분포 f(v) (단위: s/m)"""
    return m * v / (k_B * T) * np.exp(-m * v**2 / (2 * k_B * T))

def char_speeds_3d(m, T):
    """3차원 최빈 속력, 평균 속력, 제곱평균제곱근 속력 (m/s)"""
    v_p = np.sqrt(2 * k_B * T / m)
    v_mean = np.sqrt(8 * k_B * T / (np.pi * m))
    v_rms = np.sqrt(3 * k_B * T / m)
    return v_p, v_mean, v_rms

m_N2 = 28.014 * amu             # 질소 분자 하나의 질량
v = np.linspace(0, 3000, 1201)  # 속력 격자 (m/s)
dv = v[1] - v[0]

print(f"질소 분자 하나의 질량: {m_N2:.3e} kg")
for T in (300, 1000):
    v_p, v_mean, v_rms = char_speeds_3d(m_N2, T)
    area = mb_speed_3d(v, m_N2, T).sum() * dv  # 넓이(확률의 합) 확인
    print(f"T = {T:4d} K : v_p = {v_p:5.0f}, <v> = {v_mean:5.0f}, "
          f"v_rms = {v_rms:5.0f} m/s,  넓이 = {area:.4f}")

# %% code 41.
fig, ax = plt.subplots(figsize=(8.8, 4))
for T, color in zip((100, 300, 600, 1000),
                    ("tab:blue", "tab:green", "tab:orange", "tab:red")):
    ax.plot(v, mb_speed_3d(v, m_N2, T) * 1000, color=color, lw=2,
            label=f"{T} K")

# 300 K 곡선 위에 세 대표 속력 표시
for vv, ls, name in zip(char_speeds_3d(m_N2, 300), (":", "--", "-."),
                        ("$v_p$", r"$\langle v \rangle$", "$v_{rms}$")):
    ax.axvline(vv, color="tab:green", ls=ls, lw=1, label=f"{name} (300 K)")

ax.set_xlabel("속력 (m/s)")
ax.set_ylabel("확률 밀도 (1/(km/s))")
ax.set_title("온도에 따른 질소 분자의 속력 분포")
ax.legend(ncol=2)
ax.grid(alpha=0.3)
du.save_figure(fig, os.path.join(proj_dir, "mb_temperature"))
plt.show()

# %% code 42.
gases = {"H$_2$": 2.016, "He": 4.003, "H$_2$O": 18.015,
         "N$_2$": 28.014, "O$_2$": 31.998, "CO$_2$": 44.009}
T = 300
v_wide = np.linspace(0, 4000, 1601)

fig, ax = plt.subplots(figsize=(8.8, 4))
for name, M in gases.items():
    ax.plot(v_wide, mb_speed_3d(v_wide, M * amu, T) * 1000, lw=2, label=name)
ax.set_xlabel("속력 (m/s)")
ax.set_ylabel("확률 밀도 (1/(km/s))")
ax.set_title("300 K에서 기체별 분자 속력 분포")
ax.legend()
ax.grid(alpha=0.3)
du.save_figure(fig, os.path.join(proj_dir, "mb_molecules"))
plt.show()

print(f"기체   분자량 {'v_p':>7s} {'<v>':>7s} {'v_rms':>7s}  (m/s, 300 K)")
for name, M in gases.items():
    label = name.replace("$_2$", "2").replace("$", "")
    v_p, v_mean, v_rms = char_speeds_3d(M * amu, T)
    print(f"{label:6s} {M:6.1f} {v_p:7.0f} {v_mean:7.0f} {v_rms:7.0f}")

# %% code 43.
rng = np.random.default_rng(42)       # 난수 씨앗 고정

m_Ar = 39.948 * amu   # 아르곤 원자 질량 (kg)
radius = 0.17e-9      # 원자 반지름 (m)
N = 900               # 원자 수
L = 75e-9             # 상자 한 변 (m)
T0 = 300.0            # 온도 (K)
v0 = np.sqrt(2 * k_B * T0 / m_Ar)   # 모든 원자의 처음 속력 (m/s)

# 격자점에 놓고 조금씩 흔들기 (처음부터 겹치지 않게)
n_side = int(np.ceil(np.sqrt(N)))
spacing = L / n_side
grid = (np.arange(n_side) + 0.5) * spacing
gx, gy = np.meshgrid(grid, grid)
pos0 = np.column_stack([gx.ravel(), gy.ravel()])[:N]
pos0 = pos0 + rng.uniform(-0.3, 0.3, size=pos0.shape) * spacing

# 같은 속력, 무작위 방향
theta = rng.uniform(0, 2 * np.pi, N)
vel0 = v0 * np.column_stack([np.cos(theta), np.sin(theta)])

# 밀도와 충돌 빈도 어림 (2차원)
n2d = N / L**2
fill = N * np.pi * radius**2 / L**2
mfp = 1 / (2 * np.sqrt(2) * n2d * 2 * radius)        # 평균 자유 거리
v_mean_2d = np.sqrt(np.pi * k_B * T0 / (2 * m_Ar))  # 2차원 평균 속력
print(f"처음 속력 v0       : {v0:.1f} m/s (모든 원자 같음)")
print(f"원반이 차지한 넓이 : {fill * 100:.2f}%")
print(f"평균 원자 간격     : {np.sqrt(1 / n2d) * 1e9:.2f} nm")
print(f"평균 자유 거리     : {mfp * 1e9:.1f} nm")
print(f"평균 충돌 시간     : {mfp / v_mean_2d * 1e12:.1f} ps")

# 비교: 해수면 공기 (3차원)
P_air, T_air, d_air = 101325.0, 288.15, 0.37e-9
n_air = P_air / (k_B * T_air)
mfp_air = 1 / (np.sqrt(2) * np.pi * d_air**2 * n_air)
print(f"\n[해수면 공기] 수 밀도 {n_air:.2e} /m^3, "
      f"평균 분자 간격 {n_air ** (-1 / 3) * 1e9:.1f} nm, "
      f"평균 자유 거리 {mfp_air * 1e9:.0f} nm")

# %% code 44.
from scipy.spatial import cKDTree

def step(pos, vel, dt):
    """원자를 dt 동안 움직이고 벽 · 원자 충돌을 처리 (pos, vel을 제자리에서 바꿈)"""
    pos += vel * dt                                   # 1) 이동

    wall_impulse = 0.0                                # 2) 벽 충돌
    for axis in range(2):
        hit = ((pos[:, axis] < radius) & (vel[:, axis] < 0)) | \
              ((pos[:, axis] > L - radius) & (vel[:, axis] > 0))
        wall_impulse += 2 * m_Ar * np.abs(vel[hit, axis]).sum()
        vel[hit, axis] *= -1

    n_coll = 0                                        # 3) 원자끼리 충돌
    pairs = cKDTree(pos).query_pairs(2 * radius, output_type="ndarray")
    for i, j in pairs:
        dr = pos[j] - pos[i]
        dv = vel[j] - vel[i]
        approach = dv @ dr
        if approach < 0:                              # 다가가는 쌍만
            change = approach / (dr @ dr) * dr
            vel[i] += change
            vel[j] -= change
            n_coll += 1
    return wall_impulse, n_coll

# %% code 45.
import time

dt = 0.05e-12        # 시간 간격 (s)
n_steps = 12000      # 600 ps
t_eq = 200e-12       # 이 시각 뒤를 평형 구간으로 봄
snap_times_ps = (0, 10, 40, 200)

pos, vel = pos0.copy(), vel0.copy()
history = {"t": [0.0], "E": [0.5 * m_Ar * (vel**2).sum()],
           "v2": [(vel**2).sum(1).mean()], "v4": [((vel**2).sum(1)**2).mean()]}
snapshots = {0: np.linalg.norm(vel, axis=1)}
eq_speed, eq_vx = [], []
impulse_eq, n_coll_total = 0.0, 0

start = time.perf_counter()
for s in range(1, n_steps + 1):
    impulse, n_coll = step(pos, vel, dt)
    n_coll_total += n_coll
    t = s * dt
    if t > t_eq:
        impulse_eq += impulse
    if s % 10 == 0:                                   # 0.5 ps마다 기록
        v2 = (vel**2).sum(1)
        history["t"].append(t)
        history["E"].append(0.5 * m_Ar * v2.sum())
        history["v2"].append(v2.mean())
        history["v4"].append((v2**2).mean())
    t_ps = round(t * 1e12, 6)
    if t_ps in snap_times_ps:
        snapshots[int(t_ps)] = np.linalg.norm(vel, axis=1)
    if t > t_eq and s % 40 == 0:                      # 2 ps마다 평형 데이터
        eq_speed.append(np.linalg.norm(vel, axis=1))
        eq_vx.append(vel[:, 0].copy())

history = {key: np.array(val) for key, val in history.items()}
eq_speed, eq_vx = np.concatenate(eq_speed), np.concatenate(eq_vx)
print(f"계산 시간 {time.perf_counter() - start:.1f} 초, "
      f"충돌 {n_coll_total}번 (원자 하나당 평균 {2 * n_coll_total / N:.1f}번)")
print(f"평형 데이터: 속력 표본 {eq_speed.size}개")

# %% code 46.
speed_end = np.linalg.norm(vel, axis=1)
fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.6), constrained_layout=True)
for ax, p, s_, title in zip(axes, (pos0, pos), (np.linalg.norm(vel0, axis=1), speed_end),
                            ("처음 (t = 0 ps)", "마지막 (t = 600 ps)")):
    sc = ax.scatter(p[:, 0] * 1e9, p[:, 1] * 1e9, c=s_, s=4, cmap="plasma",
                    vmin=0, vmax=900)
    ax.set_xlim(0, L * 1e9)
    ax.set_ylim(0, L * 1e9)
    ax.set_aspect("equal")
    ax.set_xlabel("x (nm)")
    ax.set_title(title)
axes[0].set_ylabel("y (nm)")
fig.colorbar(sc, ax=axes, shrink=0.85, label="속력 (m/s)")
du.save_figure(fig, os.path.join(proj_dir, "box_snapshots"))
plt.show()

# %% code 47.
v_grid = np.linspace(0, 1000, 401)
f2_theory = mb_speed_2d(v_grid, m_Ar, T0)
bins = np.linspace(0, 1000, 41)

fig, axes = plt.subplots(2, 2, figsize=(7.5, 5.2), sharex=True, sharey=True,
                         constrained_layout=True)
for ax, t_ps in zip(axes.ravel(), snap_times_ps):
    ax.hist(snapshots[t_ps], bins=bins, density=True, color="tab:blue",
            alpha=0.6, label="시뮬레이션")
    ax.plot(v_grid, f2_theory, "r-", lw=2, label="이론 (300 K)")
    ax.set_title(f"t = {t_ps} ps", fontsize=12)
    ax.set_ylim(0, 0.006)
    ax.grid(alpha=0.3)
for ax in axes[1]:
    ax.set_xlabel("속력 (m/s)")
for ax in axes[:, 0]:
    ax.set_ylabel("확률 밀도 (s/m)")
axes[0, 0].legend(loc="upper right")
du.save_figure(fig, os.path.join(proj_dir, "speed_hist_evolution"))
plt.show()

for t_ps in snap_times_ps:
    sp = snapshots[t_ps]
    print(f"t = {t_ps:3d} ps : 평균 {sp.mean():5.1f} m/s, 표준편차 {sp.std():5.1f} m/s")

# %% code 48.
sigma = np.sqrt(k_B * T0 / m_Ar)                     # 성분별 표준편차
vx_grid = np.linspace(-1000, 1000, 401)
gauss = np.exp(-vx_grid**2 / (2 * sigma**2)) / (np.sqrt(2 * np.pi) * sigma)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.2), constrained_layout=True)
ax1.hist(eq_speed, bins=bins, density=True, color="tab:blue", alpha=0.6,
         label="시뮬레이션")
ax1.plot(v_grid, f2_theory, "r-", lw=2, label="2차원 이론")
ax1.set_xlabel("속력 v (m/s)")
ax1.set_ylabel("확률 밀도 (s/m)")
ax1.set_title("속력")
ax1.legend()
ax1.grid(alpha=0.3)

ax2.hist(eq_vx, bins=np.linspace(-1000, 1000, 41), density=True,
         color="tab:green", alpha=0.6, label="시뮬레이션")
ax2.plot(vx_grid, gauss, "r-", lw=2, label="정규 분포")
ax2.set_xlabel("속도 성분 $v_x$ (m/s)")
ax2.set_title("x 방향 속도")
ax2.legend()
ax2.grid(alpha=0.3)
du.save_figure(fig, os.path.join(proj_dir, "speed_equilibrium"))
plt.show()

v_p2 = np.sqrt(k_B * T0 / m_Ar)
v_mean2 = np.sqrt(np.pi * k_B * T0 / (2 * m_Ar))
v_rms2 = np.sqrt(2 * k_B * T0 / m_Ar)
counts, edges = np.histogram(eq_speed, bins=bins)
v_mode_sim = 0.5 * (edges[counts.argmax()] + edges[counts.argmax() + 1])

def lab(s, n=14):                                    # 한글은 두 칸 너비로 세어 맞춤
    return s + " " * (n - sum(2 if ord(ch) > 0x1100 else 1 for ch in s))

print(lab("") + "시뮬레이션" + " " * 6 + "이론")
print(f"{lab('최빈 속력')}{v_mode_sim:10.0f}{v_p2:10.0f}  m/s (막대 폭 25 m/s)")
print(f"{lab('평균 속력')}{eq_speed.mean():10.1f}{v_mean2:10.1f}  m/s")
print(f"{lab('rms 속력')}{np.sqrt((eq_speed**2).mean()):10.1f}{v_rms2:10.1f}  m/s")
print(f"{lab('v_x 표준편차')}{eq_vx.std():10.1f}{sigma:10.1f}  m/s")

# %% code 49.
t_ps = history["t"] * 1e12
E_rel = (history["E"] - history["E"][0]) / history["E"][0]
shape = history["v4"] / history["v2"]**2
tau = mfp / v_mean_2d * 1e12                          # 평균 충돌 시간 (ps)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.2), constrained_layout=True)
ax1.plot(t_ps, E_rel / 1e-16, color="tab:purple")
ax1.set_ylim(-5, 5)
ax1.set_xlabel("시간 (ps)")
ax1.set_ylabel(r"에너지 상대 변화 ($\times 10^{-16}$)")
ax1.set_title("운동 에너지 합")
ax1.grid(alpha=0.3)

ax2.plot(t_ps, shape, color="tab:blue", lw=1)
ax2.axhline(2, color="r", ls="--", label="2차원 이론값 2")
ax2.axvline(tau, color="gray", ls=":", label=f"평균 충돌 시간 {tau:.0f} ps")
ax2.set_xlabel("시간 (ps)")
ax2.set_ylabel(r"$\langle v^4\rangle / \langle v^2\rangle^2$")
ax2.set_title("분포 모양의 변화")
ax2.legend(loc="lower right")
ax2.grid(alpha=0.3)
du.save_figure(fig, os.path.join(proj_dir, "energy_and_shape"))
plt.show()

print(f"에너지 상대 변화의 최댓값: {np.abs(E_rel).max():.1e}")
for t_check in (10, 40, 100):
    print(f"t = {t_check:3d} ps의 모양 비율: {shape[np.searchsorted(t_ps, t_check)]:.2f}")
print(f"평형 구간 평균 모양 비율 : {shape[t_ps > 200].mean():.3f}")

# %% code 50.
duration = n_steps * dt - t_eq
P_sim = impulse_eq / (duration * 4 * L)               # 측정한 압력 (N/m)
T_sim = history["E"][-1] / (N * k_B)                  # 2차원: E/N = k_B T
P_ideal = N * k_B * T_sim / L**2                      # 이상기체 식

print(f"운동 에너지로 구한 온도 : {T_sim:.2f} K")
print(f"벽 충돌로 잰 압력      : {P_sim:.3e} N/m")
print(f"이상기체 식 N k_B T / A : {P_ideal:.3e} N/m")
print(f"비율 (측정 / 이상기체)  : {P_sim / P_ideal:.3f}")

# %% code 51.
from scipy.special import erfcx

G = constants.G
bodies = {  # 이름: (질량 kg, 반지름 m, 대기 맨 위층 대표 온도 K)
    "지구": (5.972e24, 6.371e6, 1000),
    "달":   (7.342e22, 1.737e6, 390),
    "화성": (6.417e23, 3.390e6, 250),
}
species = {"H": 1.008, "He": 4.003, "N2": 28.014, "CO2": 44.009}

def log10_escape_fraction(v_esc, m, T):
    """속력이 v_esc보다 큰 분자 비율의 상용로그 (3차원 맥스웰-볼츠만)"""
    x = v_esc / np.sqrt(2 * k_B * T / m)
    return -x**2 * np.log10(np.e) + np.log10(erfcx(x) + 2 * x / np.sqrt(np.pi))

v_esc_of = {}
for body, (M, R, T_top) in bodies.items():
    v_esc = np.sqrt(2 * G * M / R)
    v_esc_of[body] = v_esc
    print(f"[{body}] 탈출 속도 {v_esc / 1000:.2f} km/s, 온도 {T_top} K")
    for sp, Mw in species.items():
        m = Mw * amu
        v_mean = np.sqrt(8 * k_B * T_top / (np.pi * m))
        ratio = v_esc / v_mean
        verdict = "남음" if ratio > 6 else "빠져나감"
        print(f"   {sp:4s} 평균 속력 {v_mean / 1000:5.2f} km/s, "
              f"v_esc/<v> = {ratio:5.1f}, "
              f"log10 F = {log10_escape_fraction(v_esc, m, T_top):7.1f}  -> {verdict}")

# %% code 52.
from matplotlib.ticker import FuncFormatter, LogLocator, NullLocator

v_km = np.linspace(0.01, 16, 800)                    # km/s
T_exo = bodies["지구"][2]

fig, ax = plt.subplots(figsize=(8.6, 4.2))
for sp, color in zip(("H", "He", "N2"), ("tab:red", "tab:orange", "tab:blue")):
    f = mb_speed_3d(v_km * 1000, species[sp] * amu, T_exo) * 1000  # 1/(km/s)
    label = "N$_2$" if sp == "N2" else sp
    ax.semilogy(v_km, f, color=color, lw=2, label=label)
for body, ls in zip(("달", "화성", "지구"), (":", "-.", "--")):
    ax.axvline(v_esc_of[body] / 1000, color="k", ls=ls, lw=1.2,
               label=f"{body} 탈출 속도")
ax.set_ylim(1e-12, 1e5)
ax.yaxis.set_major_locator(LogLocator(base=10, numticks=10))
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"$10^{{{np.log10(y):.0f}}}$"))
ax.yaxis.set_minor_locator(NullLocator())
ax.set_xlabel("속력 (km/s)")
ax.set_ylabel("확률 밀도 (1/(km/s))")
ax.set_title(f"{T_exo} K에서 기체별 속력 분포와 탈출 속도")
ax.legend(ncol=2, loc="upper right")
ax.grid(alpha=0.3, which="both")
du.save_figure(fig, os.path.join(proj_dir, "escape_tail"))
plt.show()

# %% code 53.
MAKE_ANIMATION = False   # True로 바꾸면 애니메이션 생성

if MAKE_ANIMATION:
    from matplotlib import animation
    from IPython.display import HTML, display

    pos_a, vel_a = pos0.copy(), vel0.copy()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.4), constrained_layout=True)
    dots = ax1.scatter(pos_a[:, 0] * 1e9, pos_a[:, 1] * 1e9, s=4,
                       c=np.linalg.norm(vel_a, axis=1), cmap="plasma", vmin=0, vmax=900)
    ax1.set_xlim(0, L * 1e9)
    ax1.set_ylim(0, L * 1e9)
    ax1.set_aspect("equal")
    ax1.set_xlabel("x (nm)")
    ax1.set_ylabel("y (nm)")
    ax2.plot(v_grid, f2_theory, "r-", lw=2)
    _, _, bars = ax2.hist(np.linalg.norm(vel_a, axis=1), bins=bins, density=True,
                          color="tab:blue", alpha=0.6)
    ax2.set_ylim(0, 0.006)
    ax2.set_xlabel("속력 (m/s)")
    title = ax2.set_title("t = 0 ps")

    def update(frame):
        for _ in range(10):                          # 10단계 = 0.5 ps
            step(pos_a, vel_a, dt)
        speed = np.linalg.norm(vel_a, axis=1)
        dots.set_offsets(pos_a * 1e9)
        dots.set_array(speed)
        heights, _ = np.histogram(speed, bins=bins, density=True)
        for bar, h in zip(bars, heights):
            bar.set_height(h)
        title.set_text(f"t = {(frame + 1) * 0.5:.1f} ps")
        return [dots, title, *bars]

    ani = animation.FuncAnimation(fig, update, frames=200, interval=50)
    plt.close(fig)
    display(HTML(ani.to_jshtml()))
else:
    print("애니메이션을 보려면 MAKE_ANIMATION = True로 바꾸어 실행 (책에는 싣지 않음)")
