# 지구과학 데이터 사이언스 1 | II-04. 단진자 운동
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅱ-39.
import numpy as np
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

length = 1  # 진자 길이

x = 1/np.sqrt(2)  # 45° 기울어진 추의 위치
y = -1/np.sqrt(2)

# 왼쪽 그림
ax1.grid(True, linestyle='--')
ax1.set_aspect('equal')
ax1.set(xlim=[-length-0.5, length+0.5], ylim=[-length-0.5, length-0.5])
line1, = ax1.plot([], [], color='b', linewidth=2)
obj1, = ax1.plot([], [], 'bo')
line1.set_data([0, x], [0, y])
obj1.set_data([x], [y])
ax1.set_title('첫 번째 그림')

# 오른쪽 그림
ax2.set(xlim=[-length-0.5, length+0.5], ylim=[-length-0.5, length-0.5])
ax2.set_aspect('equal')
line2, = ax2.plot([], [], color='b', linewidth=2)
center, = ax2.plot(0, 0, 'ko', markersize=5)
obj2, = ax2.plot([], [], 'ro', markersize=18)
line2.set_data([0, x], [0, y])
obj2.set_data([x], [y])
ax2.set_title('두 번째 그림')

plt.tight_layout()
du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_04_Simple_pendulum_motion_01"))
plt.show()

# %% code Ⅱ-40.
fig, ax = plt.subplots(figsize=(8,8))

# 단진자 추의 (x, y) 좌표
length = 1 
angle = 45  # 도(°)
x = length*np.sin(np.radians(angle))
y = -length*np.cos(np.radians(angle))

ax.set(xlim=[-length-0.5, length+0.5], ylim=[-length-0.5, length-0.5])
ax.set_aspect('equal', adjustable='box')
ax.grid(True, linestyle='--')

ax.set_xticks(np.arange(-1.5, 2.0, 0.5))
ax.set_yticks(np.arange(-1.5, 1.0, 0.5))

line, = ax.plot([], [], color='b', linewidth=2)
center, = ax.plot(0, 0, 'ko', markersize=5)
obj, = ax.plot([], [], 'ro', markersize=18)

time_text = ax.text(-length-0.2, -length-0.2, '')  # 시간 표시 자리(애니메이션에서 사용)
line.set_data([0, x], [0, y])
obj.set_data([x], [y])

du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_04_Simple_pendulum_motion_02"))
plt.show()

# %% code Ⅱ-41.
import numpy as np
from scipy.integrate import odeint

def odefun(Z, t, k):
    """
    단진자의 운동방정식을 정의하는 함수
    Z[0]: 각도(θ)
    Z[1]: 각속도(dθ/dt)
    k: g/L (중력가속도/진자길이)
    """
    dZdt = np.zeros(2)
    dZdt[0] = Z[1]               # dθ/dt = 각속도
    dZdt[1] = -k * np.sin(Z[0])  # d²θ/dt² = -(g/L)sin(θ)
    return dZdt

init_angle = 45    # 도
length = 1.0       # m
k = 9.81 / length  # g/L

t = np.linspace(0, 10, 100)                   # 0 ~ 10 s, 100개 시점
Z0 = np.array([init_angle * np.pi / 180, 0])  # 초기 조건 [각도(라디안), 각속도]

Z = odeint(odefun, Z0, t, args=(k,))  # 미분방정식 수치 적분

print(f"해의 개수: {len(Z)}")
print(f"각도 변화 (처음 12개): {Z[:12, 0] * 180 / np.pi}")  # 라디안 → 도
print(f"각속도 변화 (처음 12개): {Z[:12, 1]}")

# %% code Ⅱ-42.
fig, ax = plt.subplots(figsize=(8,8))

# 단진자 추의 (x, y) 좌표
length = 1  # 진자 길이
angle = 45  # 도
x = length*np.sin(np.radians(angle))
y = -length*np.cos(np.radians(angle))  # 음수: 고정점 아래쪽

ax.set(xlim=[-length-0.5, length+0.5], ylim=[-length-0.5, length-0.5])
ax.set_aspect('equal', adjustable='box')
ax.grid(True, linestyle='--')

ax.set_xticks(np.arange(-1.5, 2.0, 0.5))
ax.set_yticks(np.arange(-1.5, 1.0, 0.5))

line, = ax.plot([], [], color='b', linewidth=2)  # 진자 줄
center, = ax.plot(0, 0, 'ko', markersize=5)      # 고정점
obj, = ax.plot([], [], 'ro', markersize=18)      # 추

time_text = ax.text(-length-0.2, -length-0.2, '')
line.set_data([0, x], [0, y])
obj.set_data([x], [y])

plt.show()

# 처음 12개 시점의 추 좌표
x_values = []
y_values = []

for j in Z[:12] :
    theta = j[0]  # 각도(라디안)
    x_values.append(length*np.sin(theta))
    y_values.append(-length*np.cos(theta))
print("x_values :", x_values)
print("y_values :", y_values)

# %% code Ⅱ-43.
import matplotlib.pyplot as plt
import numpy as np

frames = range(1, 13)

fig, axes = plt.subplots(3, 4, figsize=(12, 9))
fig.suptitle('프레임별 추의 좌표', fontsize=16, fontweight='bold')

for i, (frame, x, y) in enumerate(zip(frames, x_values, y_values)):
    row = i // 4
    col = i % 4
    ax = axes[row, col]
    
    # 고정점(원점)에서 추까지 화살표
    ax.arrow(0, 0, x, y, head_width=0.05, head_length=0.05, fc='red', ec='red', linewidth=2)
    ax.plot(x, y, 'ro', markersize=8)
    
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 0.3)
    ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax.set_aspect('equal')
    
    ax.set_title(f'프레임 {frame}', fontweight='bold')
    
    # 그림 아래에 좌표값 표시
    ax.text(0, -1.6, f'x = {x:.3f}, y = {y:.3f}', 
            ha='center', va='top', fontsize=10, 
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7))

plt.tight_layout()
plt.subplots_adjust(top=0.93, bottom=0.1)
du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_04_Simple_pendulum_motion_03"))
plt.show()

# %% code Ⅱ-44.
length = 1
init_angle = 30
k = 9.81/length

tf, dt = 10, 0.05  # 끝 시각 · 시간 간격(s)
t = np.arange(0, tf+dt, dt)

Z0 = np.array([init_angle * np.pi / 180, 0])  # 초기 각도 30°로 다시 정함
Z = odeint(odefun, Z0, t, args=(k,))

fig, ax = plt.subplots(figsize=(8,8))

# 초기 각도의 추 위치
theta_initial = init_angle * np.pi / 180
x = length * np.sin(theta_initial)
y = -length * np.cos(theta_initial)

ax.set(xlim=[-length-0.5, length+0.5], ylim=[-length-0.5, length-0.5])
ax.set_aspect('equal', adjustable='box')

# 축 숨기기
ax.set_xticks([])
ax.set_yticks([])
ax.axis('off')

center, = ax.plot(0, 0, 'ko', markersize=5)
line, = ax.plot([], [], color='b', linewidth=2)
obj, = ax.plot([], [], 'ro', markersize=18)
time_text = ax.text(-length-0.2, -length-0.2, '')  # 시각 표시(애니메이션에서 사용)

line.set_data([0, x], [0, y])
obj.set_data([x], [y])

du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_04_Simple_pendulum_motion_04"))
plt.show()

# %% code Ⅱ-45.
def animate(i):
    """애니메이션의 각 프레임을 업데이트하는 함수"""
    theta = Z[i, 0]  # i번째 시각의 각도
    x = length*np.sin(theta)
    y = -length*np.cos(theta)
    line.set_data([0, x], [0, y])
    obj.set_data([x], [y])
    time_text.set_text('시각 = {:.1f} s'.format(t[i]))
    return line, obj, time_text  # 다시 그릴 객체(blit=True)

from matplotlib.animation import FuncAnimation
ani = FuncAnimation(fig, animate, frames=len(Z), 
                    interval=int(dt*1000), blit=True)
# interval: 프레임 간격(ms), blit: 바뀐 부분만 다시 그리기

import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['animation.embed_limit'] = 50  # MB(기본값 약 20 MB)
matplotlib.rcParams['animation.writer'] = 'ffmpeg'

print(f"애니메이션 임베드 제한 설정값: {matplotlib.rcParams['animation.embed_limit']} MB")

from IPython.display import HTML
# 1) JavaScript 애니메이션: 가볍고 대화형
matplotlib.rcParams['animation.html'] = 'jshtml'
print(f"애니메이션 HTML 형식: {matplotlib.rcParams['animation.html']}")
HTML(ani.to_jshtml())

# 2) HTML5 비디오: 안정적이지만 파일이 큼
# matplotlib.rcParams['animation.html'] = 'html5'
# print(f"애니메이션 HTML 형식: {matplotlib.rcParams['animation.html']}")
# HTML(ani.to_html5_video())

# %% code Ⅱ-46.
class Pendulum(object):
    def __init__(self, length=1, init_angle=30, tf=10, dt=0.05):
        self.length = length
        self.init_angle = init_angle*np.pi/180  # 도 → 라디안
        self.dt = dt
        self.t = np.arange(0, tf+dt, dt)
 
        Z0 = np.array([self.init_angle, 0])
 
        self.Z = odeint(self.odefun, Z0, self.t, args=(9.81/length,))  # [각도, 각속도] 시계열
 
    def odefun(self, Z, t, k):
        dZdt = np.zeros(2)
        dZdt[0] = Z[1]
        dZdt[1] = -k * np.sin(Z[0])
        return dZdt

fig, ax = plt.subplots(figsize=(8,8)) 
pend = Pendulum()
length = pend.length
 
ax.set(xlim=[-length-0.5, length+0.5], ylim=[-length-0.5, length-0.5])
ax.set_aspect('equal', adjustable='box')

# 축 숨기기
ax.set_xticks([])
ax.set_yticks([])
ax.axis('off')
 
center, = ax.plot(0, 0, 'ko', markersize=5)
line, = ax.plot([], [], color='b', linewidth=2)
obj, = ax.plot([], [], 'ro', markersize=18)
time_text = ax.text(-length-0.2, -length-0.2, '')

x = length*np.sin(pend.init_angle)   # 초기 각도의 추 위치
y = -length*np.cos(pend.init_angle)
line.set_data([0, x], [0, y])
obj.set_data([x], [y])

plt.tight_layout()
du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_04_Simple_pendulum_motion_05"))
plt.show()

# %% code Ⅱ-47.
def animate(i):
    theta = pend.Z[i, 0]
    x = length*np.sin(theta)
    y = -length*np.cos(theta)
    line.set_data([0, x], [0, y])
    obj.set_data([x], [y])
    time_text.set_text('시각 = {:.1f} s'.format(pend.t[i]))
    return line, obj, time_text
  
from matplotlib.animation import FuncAnimation
ani = FuncAnimation(fig, animate, frames=len(pend.Z), 
                    interval=int(pend.dt*1000), blit=True)

import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['animation.embed_limit'] = 50  # MB(기본값 약 20 MB)
matplotlib.rcParams['animation.writer'] = 'ffmpeg'

print(f"애니메이션 임베드 제한 설정값: {matplotlib.rcParams['animation.embed_limit']} MB")

from IPython.display import HTML
# 1) JavaScript 애니메이션: 가볍고 대화형
matplotlib.rcParams['animation.html'] = 'jshtml'
print(f"애니메이션 HTML 형식: {matplotlib.rcParams['animation.html']}")
HTML(ani.to_jshtml())

# 2) HTML5 비디오: 안정적이지만 파일이 큼
# matplotlib.rcParams['animation.html'] = 'html5'
# print(f"애니메이션 HTML 형식: {matplotlib.rcParams['animation.html']}")
# HTML(ani.to_html5_video())

# %% code Ⅱ-48.
# 애니메이션 저장
fname = 'Simple_pendulum'

import shutil
from pathlib import Path

output_path = Path(proj_dir) / f"{fname}.mp4"
output_path.parent.mkdir(parents=True, exist_ok=True)

if shutil.which('ffmpeg') is None:
    print('ffmpeg가 설치되어 있지 않아 MP4 저장을 건너뜁니다.')
else:
    ani.save(str(output_path), fps=int(round(1/pend.dt)), dpi=150)  # dt = 0.05 s → 초당 20프레임(실제 속도)
    print(f"애니메이션 저장: {output_path}")
