# 지구과학 데이터 사이언스 1 | III-05. 태양계 시뮬레이션
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 55.
from astropy.time import Time

specific_time = Time("2017-01-01")

# NASA JPL Horizons 천체력 서비스
from astroquery.jplhorizons import Horizons

# 수성의 위치 · 속도 벡터
obj1 = Horizons(id = '199',                # 199 = 수성
                location="@sun",          # 태양 중심 기준
                epochs=specific_time.jd   # 줄리안 데이
                ).vectors()

print("type(obj1): ", type(obj1))

print("obj1: ",obj1)

# %% code 56.
import numpy as np
from astropy.time import Time, TimeDelta

specific_time_str = "2017-01-01"
print("type(specific_time_str):", type(specific_time_str))
print("specific_time_str", specific_time_str)

specific_time = Time(specific_time_str)

print("specific_time:", specific_time)
print("type(specific_time): ", type(specific_time))

# 줄리안 데이로 Time 객체 만들기
specific_time_jd = Time(specific_time.jd, format="jd")
print("type(specific_time.jd):", type(specific_time.jd))
print("specific_time.jd: ", specific_time.jd)
print("specific_time_jd.iso: {}".format(specific_time_jd.iso))

# 시뮬레이션 기간
start_time_text = "2017-01-01"
end_time_text = "2017-02-01"

dt = 1  # 시간 간격(일)

def astropyTime_range(start, end, delta):
    """
    시작 시간부터 종료 시간까지 일정한 간격으로 시간을 생성하는 제너레이터 함수
    
    Parameters:
    start: 시작 시간 (astropy Time 객체)
    end: 종료 시간 (astropy Time 객체)
    delta: 시간 간격 (TimeDelta 객체)
    """
    current = start
    while current < end:
        yield current
        current += delta

# 1일 간격 시각 목록(ISO 문자열)
dts = [dt.iso for dt in 
       astropyTime_range(Time(start_time_text), Time(end_time_text), 
       TimeDelta(dt, format='jd'))]

print("len(dts) :", len(dts))
print("dts :", dts)

# %% code 57.
import matplotlib.pyplot as plt

fig = plt.figure(figsize=[4, 4])

# 축이 그림 전체를 채우게, 범위 ±1.8 AU
ax = plt.axes([0., 0., 1., 1.], xlim=(-1.8, 1.8), ylim=(-1.8, 1.8))

# 원이 찌그러지지 않도록
ax.set_aspect('equal')

ax.set_xlabel('x')
ax.set_ylabel('y')

ax.grid(True)

# 태양(원점)
plot = ax.scatter(0, 0,
                  color = "red",
                  s = 28**2,          # 점 크기는 지름의 제곱
                  edgecolors = None,
                  zorder = 10)        # 다른 것보다 앞에 그리기

# %% code 58.
import matplotlib.pyplot as plt

# 검은 배경
plt.style.use('dark_background')

# 축이 그림 전체를 채우게, 범위 ±1.8 AU
ax = plt.axes([0., 0., 1., 1.], xlim=(-1.8, 1.8), ylim=(-1.8, 1.8))

# 원이 찌그러지지 않도록
ax.set_aspect('equal')

ax.set_xlabel('x')
ax.set_ylabel('y')

ax.grid(False)

ax.axis('off')

# 태양(원점)
plot = ax.scatter(0, 0,
                  color = "red",
                  s = 28**2,          # 점 크기는 지름의 제곱
                  edgecolors = None,
                  zorder = 10)

# %% code 59.
from astropy.time import Time
specific_time = Time("2017-01-01")

from astroquery.jplhorizons import Horizons
# 수성의 위치 · 속도 벡터
obj1 = Horizons(id = '199', location="@sun", epochs=specific_time.jd).vectors()

print("type(obj1): ", type(obj1))
print("obj1: ", obj1)

# 위치(AU)
print("obj1['x']: ", obj1['x'])
print("obj1['y']: ", obj1['y'])
print("obj1['z']: ", obj1['z'])

# 속도(AU/day)
print("obj1['vx']: ", obj1['vx'])
print("obj1['vy']: ", obj1['vy'])
print("obj1['vz']: ", obj1['vz'])

# %% code 60.
from astropy.time import Time
specific_time = Time("2017-01-01")

import matplotlib.pyplot as plt
plt.style.use('dark_background')
ax = plt.axes([0., 0., 1., 1.], xlim=(-1.8, 1.8), ylim=(-1.8, 1.8))

ax.set_aspect('equal')
ax.grid(False)
ax.axis('off')

# 태양(원점)
plot = ax.scatter(0, 0, color="red", s=28**2, edgecolors=None, zorder=10)

# 왼쪽 위에 날짜
ax.text(.03, .94,                          # 축 좌표(0~1) 기준 위치
        '날짜: {}'.format(specific_time.iso[:10]),
        color='w',
        transform=ax.transAxes,
        fontsize='x-large')

# 수성 · 금성 · 지구 · 화성
from astroquery.jplhorizons import Horizons
ids = ['199', '299', '399', '499']             # Horizons ID(행성 본체)
sizes = [0.38, 0.95, 1., 0.53]                 # 상대 크기(지구 = 1)
names = ['수성', '금성', '지구', '화성']
for i in range(4):
    obj = Horizons(id = ids[i],
                   location = "@sun",
                   epochs = specific_time.jd).vectors()

    plot = ax.scatter(obj["x"], obj["y"], s = (10 * sizes[i])**2,
                      edgecolors = None, zorder = 10)

    # 행성 위에 이름
    ax.text(obj["x"], obj["y"]+0.1, names[i], zorder=1000, ha='center',
            fontsize='large')

# %% code 61.
from astropy.time import Time
specific_time = Time("2017-01-01")

import matplotlib.pyplot as plt
plt.style.use('dark_background')

ax = plt.axes([0., 0., 1., 1.], xlim=(-1.8, 1.8), ylim=(-1.8, 1.8))
ax.set_aspect('equal')
ax.grid(False)
ax.axis('off')

# 태양(원점)
sun = ax.scatter(0, 0, color="red", s=28**2, edgecolors=None, zorder=10)

ax.text(.03, .94, '날짜: {}'.format(specific_time.iso[:10]), color='w',
        transform=ax.transAxes, fontsize='x-large')

from astroquery.jplhorizons import Horizons
# 지구(id='399')의 위치 · 속도 벡터
obj = Horizons(id='399', location="@sun", epochs=specific_time.jd).vectors()

plot = ax.scatter(obj["x"], obj["y"], s=10**2, edgecolors=None, zorder=10)

ax.text(obj["x"], obj["y"]+0.1, "지구", zorder=1000, ha='center', fontsize='large')

print([obj[xi] for xi in ['x', 'y', 'z']])

import numpy as np
# 위치 벡터 r(AU)
r = np.array([np.double(obj[xi]) for xi in ['x', 'y', 'z']], dtype=np.float64)
r

# %% code 62.
import numpy as np
from astropy.time import Time, TimeDelta

start_time_text = "2017-01-01"
end_time_text = "2020-01-01"

dt = 1  # 시간 간격(일)

# 1일 간격 시각 목록(astropyTime_range는 앞에서 정의함)
dts = [t.iso for t in
       astropyTime_range(Time(start_time_text), Time(end_time_text),
       TimeDelta(dt, format='jd'))]

# 지구의 처음 위치 · 속도
from astroquery.jplhorizons import Horizons
obj = Horizons(id='399', location="@sun", epochs=Time(start_time_text).jd).vectors()

r = np.array([np.double(obj[xi]) for xi in ['x', 'y', 'z']], dtype=np.float64)    # AU
v = np.array([np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.float64)  # AU/day
print("r: {}, v: {}".format(r, v))

xs, ys = [], []
rs, vs, accs = [], [], []
i = 0
# 오일러-크로머 방법으로 궤도 계산
while i < (len(dts)) :
    r = r + v * dt                                   # 위치 갱신: r ← r + v·dt
    acc = -2.959e-4 * r / np.sum(r**2)**(3./2)  # 새 위치의 가속도(태양 GM = 2.959e-4 AU³/day²)
    v = v + acc * dt                                 # 속도 갱신: v ← v + a·dt
    rs.append(r)
    vs.append(v)
    accs.append(acc)
    xs.append(r[0])
    ys.append(r[1])
    i += 1

print("len(xs): {}".format(len(xs)))
print("len(ys): {}".format(len(ys)))
print("len(rs): {}".format(len(rs)))

print("len(vs): {}".format(len(vs)))

print("len(accs): {}".format(len(accs)))

print("rs[5][:2]: {}".format(rs[5][:2]))
print("rs[4]: {}".format(rs[4]))
print("rs[5]: {}".format(rs[5]))

# %% code 63.
import matplotlib.pyplot as plt

# 궤도(rs, xs, ys)와 날짜 목록(dts)은 앞에서 계산한 것을 그대로 씀
plt.style.use('dark_background')
fig = plt.figure(figsize=[6, 6])
ax = plt.axes([0., 0., 1., 1.], xlim=(-1.8, 1.8), ylim=(-1.8, 1.8))
ax.set_aspect('equal')
ax.axis('off')
sun = ax.scatter(0, 0, color="red", s=28**2, edgecolors=None, zorder=10)

# 지구의 처음 위치(앞에서 Horizons로 받은 obj)
ax.text(obj["x"], obj["y"]+0.1,
        "지구", zorder=1000, ha='center', fontsize='large')
plot = ax.scatter(obj["x"], obj["y"], s=10**2, edgecolors=None, zorder=10)
line, = ax.plot([], [], linewidth=1.4)
timestamp = ax.text(.03, .94, '날짜: ', color='w', transform=ax.transAxes, fontsize='x-large')

# %% code 64.
def animate(i):
    plot.set_offsets(rs[i][:2])
    line.set_xdata(xs[:i])
    line.set_ydata(ys[:i])
    timestamp.set_text('날짜: ' + dts[i][:10])
    return plot, line, timestamp

from matplotlib.animation import FuncAnimation
ani = FuncAnimation(fig, animate, frames=len(dts), blit=True)

# %% code 65.
import matplotlib
from IPython.display import HTML

# 애니메이션 설정(이 장의 모든 애니메이션에 씀)
matplotlib.rcParams['animation.embed_limit'] = 100     # 용량 한도 100 MB(기본 약 20 MB)
matplotlib.rcParams['animation.html'] = 'jshtml'       # 노트북에 넣는 형식
matplotlib.rcParams['animation.writer'] = 'ffmpeg'     # MP4 저장(ffmpeg 실행 파일 필요)

print(f"애니메이션 용량 한도: {matplotlib.rcParams['animation.embed_limit']} MB")
print(f"애니메이션 HTML 형식: {matplotlib.rcParams['animation.html']}")

HTML(ani.to_jshtml())

# %% code 66.
# MP4 동영상으로 넣기(ffmpeg 실행 파일 필요)
HTML(ani.to_html5_video())

# %% code 67.
import numpy as np
import matplotlib.pyplot as plt
from astropy.time import Time
from astroquery.jplhorizons import Horizons

sim_start_date = "2018-01-01"
sim_duration = 2 * 365            # 2년(일) = 애니메이션 프레임 수
GM_sun = 2.959e-4                 # 태양 GM(AU³/day²)

class Object:                     # 천체 하나(태양, 행성)
    def __init__(self, name, rad, color, r, v, ax):
        self.name = name
        self.r    = np.array(r, dtype=np.float64)  # 처음 위치(AU)
        self.v    = np.array(v, dtype=np.float64)  # 처음 속도(AU/day)
        self.path = None                           # 미리 계산한 날짜별 위치
        self.is3d = (ax.name == '3d')              # 3D 축이면 3D로 그림
        if self.is3d:
            self.plot = ax.scatter(r[0], r[1], r[2], color=color, s=rad**2, edgecolors=None, zorder=10)
            self.line, = ax.plot([], [], [], color=color, linewidth=1.4)
        else:
            self.plot = ax.scatter(r[0], r[1], color=color, s=rad**2, edgecolors=None, zorder=10)
            self.line, = ax.plot([], [], color=color, linewidth=1.4)

class SolarSystem:                # 태양계 전체
    def __init__(self, thesun, ax):
        self.thesun = thesun
        self.planets = []
        self.time = None          # 시작 시각(줄리안 데이)
        text = ax.text2D if thesun.is3d else ax.text
        self.timestamp = text(.03, .94, '날짜: ', color='w', transform=ax.transAxes, fontsize='x-large')

    def add_planet(self, planet):
        self.planets.append(planet)

    def run(self, n_days, dt=1.0):    # 궤도를 미리 계산(오일러-크로머 방법)
        self.times = self.time + dt * np.arange(1, n_days + 1)
        self.timestamp.set_text('날짜: ' + Time(self.time, format='jd').iso[:10])  # 시작 날짜
        for p in self.planets:
            r, v = p.r.copy(), p.v.copy()
            p.path = np.zeros((n_days, 3))
            for k in range(n_days):
                r = r + v * dt                                # 위치 갱신: r ← r + v·dt
                acc = -GM_sun * r / np.sum(r**2)**(3./2)      # 새 위치의 태양 중력 가속도
                v = v + acc * dt                              # 속도 갱신: v ← v + a·dt
                p.path[k] = r

    def draw(self, i):            # i번째 날의 모습만 그림(계산하지 않음)
        artists = []
        for p in self.planets:
            x, y, z = p.path[:i+1].T                          # 처음부터 i번째 날까지의 궤적
            if p.is3d:
                p.plot._offsets3d = ([x[-1]], [y[-1]], [z[-1]])  # 3D 점 위치(내부 속성 사용)
                p.line.set_data_3d(x, y, z)
            else:
                p.plot.set_offsets([x[-1], y[-1]])
                p.line.set_data(x, y)
            artists += [p.plot, p.line]
        self.timestamp.set_text('날짜: ' + Time(self.times[i], format='jd').iso[:10])
        # blit용으로 바뀐 객체 반환
        return artists + [self.timestamp]

fig = plt.figure(facecolor='black')
plt.style.use('dark_background')

ax = plt.axes([0., 0., 1., 1.], xlim=(-1.8, 1.8), ylim=(-1.8, 1.8))
ax.set_aspect('equal')
ax.axis('off')

# 태양을 원점에 둔 태양계
ss = SolarSystem(Object("태양", 28, 'red', [0, 0, 0], [0, 0, 0], ax), ax)
ss.time = Time(sim_start_date).jd

ids = ['199', '299', '399', '499']               # Horizons ID: 수성 · 금성 · 지구 · 화성
colors = ['gray', 'orange', 'blue', 'chocolate']
sizes = [0.38, 0.95, 1., 0.53]                    # 상대 크기(지구 = 1)
names = ['수성', '금성', '지구', '화성']
texty = [.47, .73, 1, 1.5]                        # 이름 표시 y 위치

# 수성~화성 추가
for i, nasaid in enumerate(ids):
    obj = Horizons(id=nasaid, location="@sun", epochs=ss.time).vectors()

    ss.add_planet(Object(names[i],
                         20 * sizes[i],
                         colors[i],
                         [np.double(obj[xi]) for xi in ['x', 'y', 'z']],
                         [np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']],
                         ax))

    # 아래쪽에 이름
    ax.text(0, - (texty[i] + 0.1), names[i], color=colors[i],
            zorder=1000, ha='center', fontsize='large')

ss.run(sim_duration)  # 2년 치 궤도를 미리 계산
plt.show()

# %% code 68.
# 프레임 i: 미리 계산한 궤도에서 i번째 날을 그림
def animate(i):
    return ss.draw(i)

import matplotlib.animation as animation

ani = animation.FuncAnimation(fig,
                              animate,
                              repeat=False,
                              frames=sim_duration,  # 프레임 수 = 시뮬레이션 일수
                              blit=True,
                              interval=20)          # ms

# %% code 69.
# 애니메이션 설정은 앞에서 정한 것을 그대로 씀
HTML(ani.to_jshtml())

# %% code 70.
# MP4 동영상으로 넣기(ffmpeg 실행 파일 필요)
HTML(ani.to_html5_video())

# %% code 71.
fname = 'Solar_System_2D_Animation_Class_Based'

try:
    # MP4 저장(ffmpeg 필요)
    ani.save(f'{proj_dir}/{fname}.mp4', fps=60, dpi=150, writer='ffmpeg')
    print(f"동영상이 저장되었습니다: {proj_dir}/{fname}.mp4")
except Exception as e:
    print(f"MP4 저장 중 오류 발생: {e}")
    
    # 안 되면 GIF
    try:
        ani.save(f'{proj_dir}/{fname}.gif', fps=30, dpi=100, writer='pillow')
        print(f"GIF 파일이 저장되었습니다: {proj_dir}/{fname}.gif")
    except Exception as e2:
        print(f"GIF 저장 중 오류 발생: {e2}")
        
        # 그래도 안 되면 HTML
        try:
            with open(f'{proj_dir}/{fname}.html', 'w') as f:
                f.write(ani.to_jshtml())
            print(f"HTML 파일이 저장되었습니다: {proj_dir}/{fname}.html")
        except Exception as e3:
            print(f"HTML 저장 중 오류 발생: {e3}")

# %% code 72.
import numpy as np
import matplotlib.pyplot as plt
from astropy.time import Time
from astroquery.jplhorizons import Horizons

# 앞에서 만든 Object · SolarSystem 클래스와 sim_start_date, sim_duration,
# ids, colors, sizes, names, texty를 그대로 씀(축이 3D이면 3D로 그림)
plt.style.use('dark_background')
fig = plt.figure(figsize=(12, 10), facecolor='black')

ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.grid(False)

# 범위(AU)
ax.set_xlim3d([-1.8, 1.8])
ax.set_ylim3d([-1.8, 1.8])
ax.set_zlim3d([-1.0, 1.0])

ax.set_xlabel('X (AU)', color='white')
ax.set_ylabel('Y (AU)', color='white')
ax.set_zlabel('Z (AU)', color='white')
ax.set_title('태양계 (3D)', color='white', fontsize=16)

# 태양을 원점에 둔 태양계
ss = SolarSystem(Object("태양", 28, 'red', [0, 0, 0], [0, 0, 0], ax), ax)
ss.time = Time(sim_start_date).jd

# 수성~화성 추가
for i, nasaid in enumerate(ids):
    obj = Horizons(id=nasaid, location="@sun", epochs=ss.time).vectors()
    ss.add_planet(Object(names[i],
                         20 * sizes[i],
                         colors[i],
                         [np.double(obj[xi]) for xi in ['x', 'y', 'z']],
                         [np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']],
                         ax))
    ax.text(0, -(texty[i] + 0.1), 0, names[i], color=colors[i],
            zorder=1000, ha='center', fontsize='large')

ss.run(sim_duration)  # 2년 치 궤도를 미리 계산
plt.tight_layout()
plt.show()

# %% code 73.
# 프레임 i: 미리 계산한 궤도에서 i번째 날을 그림
def animate(i):
    return ss.draw(i)

from matplotlib.animation import FuncAnimation

ani = FuncAnimation(fig, animate,
                    frames=sim_duration,  # 프레임 수 = 시뮬레이션 일수(2년)
                    blit=True)

# %% code 74.
# 애니메이션 설정은 앞에서 정한 것을 그대로 씀
HTML(ani.to_jshtml())

# %% code 75.
# MP4 동영상으로 넣기(ffmpeg 실행 파일 필요)
HTML(ani.to_html5_video())

# %% code 76.
fname = 'Solar_System_3D_Animation_Class_Based'

ani.save(f'{proj_dir}/{fname}.mp4', fps=60, dpi=150,
         writer='ffmpeg')  # ffmpeg 필요
print(f"동영상이 저장되었습니다: {proj_dir}/{fname}.mp4")

# %% code 77.
ani.save(f'{proj_dir}/{fname}.gif',
            fps=30,           # MP4보다 낮춰 용량 줄이기
            dpi=100,
            writer='pillow')
print(f"GIF 파일이 저장되었습니다: {proj_dir}/{fname}.gif")
