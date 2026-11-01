# 지구과학 데이터 사이언스 1 | III-05. 태양계 시뮬레이션
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 53.
from astropy.time import Time

specific_time = Time("2017-01-01")

# NASA JPL Horizons 천체력 서비스
from astroquery.jplhorizons import Horizons

# 수성의 위치 · 속도 벡터
obj1 = Horizons(id = 1,                    # 1 = 수성
                location="@sun",          # 태양 중심 기준
                epochs=specific_time.jd,  # 줄리안 데이
                id_type='majorbody').vectors()

print("type(obj1): ", type(obj1))

print("obj1: ",obj1)

# %% code 54.
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

# %% code 55.
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

# %% code 56.
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

# %% code 57.
from astropy.time import Time
specific_time = Time("2017-01-01")

from astroquery.jplhorizons import Horizons
# 수성의 위치 · 속도 벡터
obj1 = Horizons(id = 1, location="@sun", epochs=specific_time.jd,
                id_type='majorbody').vectors()

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

# %% code 58.
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
        'Date: {}'.format(specific_time),
        color='w',
        transform=ax.transAxes,
        fontsize='x-large')

# 수성 · 금성 · 지구 · 화성
from astroquery.jplhorizons import Horizons
sizes = [0.38, 0.95, 1., 0.53]                 # 상대 크기(지구 = 1)
names = ['Mercury', 'Venus', 'Earth', 'Mars']
for i in range(4):
    obj = Horizons(id = i+1,               # 1 수성, 2 금성, 3 지구, 4 화성
                   location = "@sun",
                   epochs = specific_time.jd,
                   id_type = 'majorbody').vectors()

    plot = ax.scatter(obj["x"], obj["y"], s = (10 * sizes[i])**2,
                      edgecolors = None, zorder = 10)
    
    # 행성 위에 이름
    ax.text(obj["x"], obj["y"]+0.1, names[i], zorder=1000, ha='center',
            fontsize='large')

# %% code 59.
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

ax.text(.03, .94, 'Date: {}'.format(specific_time), color='w', 
        transform=ax.transAxes, fontsize='x-large')

from astroquery.jplhorizons import Horizons
# 지구(id=3)의 위치 · 속도 벡터
obj = Horizons(id=3, location="@sun", epochs=specific_time.jd,
               id_type='id').vectors()

plot = ax.scatter(obj["x"], obj["y"], s=10**2, edgecolors=None, zorder=10)

ax.text(obj["x"], obj["y"]+0.1, "Earth", zorder=1000, ha='center', fontsize='large')

# 시각 다시 정의(중복이지만 명확성을 위해)
from astropy.time import Time
specific_time = Time("2017-01-01")

from astroquery.jplhorizons import Horizons
obj = Horizons(id=3, location="@sun", epochs=specific_time.jd, id_type='id').vectors()

print([obj[xi] for xi in ['x', 'y', 'z']])

import numpy as np
# 위치 벡터 r(AU)
r = np.array([np.double(obj[xi]) for xi in ['x', 'y', 'z']], dtype=np.float64)
r

# %% code 60.
import numpy as np
from astropy.time import Time, TimeDelta

start_time_text = "2017-01-01"
end_time_text = "2020-01-01"

dt = 1

def astropyTime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta

dts = [dt.iso for dt in 
       astropyTime_range(Time(start_time_text), Time(end_time_text), 
       TimeDelta(dt, format='jd'))]

# 지구의 처음 위치 · 속도
from astroquery.jplhorizons import Horizons
obj = Horizons(id=3, location="@sun", epochs=Time(start_time_text).jd, id_type='id').vectors()

r = np.array([np.double(obj[xi]) for xi in ['x', 'y', 'z']], dtype=np.float64)
v = np.array([np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.float64)
print("r: {}, v: {}".format(r, v))

xs, ys = [], []
rs, vs, accs = [], [], []
i = 0
while i < (len(dts)) :    
    r = r + v * dt
    acc = -2.959e-4 * r / np.sum(r**2)**(3./2)  # 태양 GM = 2.959e-4 AU³/day²
    v = v + acc * dt
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

# %% code 61.
import numpy as np
from astropy.time import Time, TimeDelta

# 시뮬레이션 기간
start_time_text = "2017-01-01"
end_time_text = "2020-01-01"

dt = 1  # 시간 간격(일)

def astropyTime_range(start, end, delta):
    """
    주어진 시작 시간부터 종료 시간까지 일정한 간격으로 시간을 생성하는 제너레이터 함수
    
    Parameters:
    start: 시작 시간 (astropy Time 객체)
    end: 종료 시간 (astropy Time 객체)  
    delta: 시간 간격 (TimeDelta 객체)
    """
    current = start
    while current < end:
        yield current
        current += delta

# 1일 간격 시각 목록
dts = [dt.iso for dt in 
       astropyTime_range(Time(start_time_text), Time(end_time_text), 
       TimeDelta(dt, format='jd'))]

plt.style.use('dark_background')
fig = plt.figure(figsize=[6, 6])
ax = plt.axes([0., 0., 1., 1.], xlim=(-1.8, 1.8), ylim=(-1.8, 1.8))
ax.set_aspect('equal')
ax.axis('off')
sun = ax.scatter(0, 0, color="red", s=28**2, edgecolors=None, zorder=10)

# 지구의 처음 위치 · 속도(Horizons)
from astroquery.jplhorizons import Horizons
obj = Horizons(id=3, location="@sun", epochs=Time(start_time_text).jd,
               id_type='id').vectors()

ax.text(obj["x"], obj["y"]+0.1,
        "Earth", zorder=1000, ha='center', fontsize='large')
plot = ax.scatter(obj["x"], obj["y"], s=10**2, edgecolors=None, zorder=10)
line, = ax.plot([], [], linewidth=1.4)
timestamp = ax.text(.03, .94, 'Date: ', color='w', transform=ax.transAxes, fontsize='x-large')

# 처음 위치(AU)
r = np.array([np.double(obj[xi]) for xi in ['x', 'y', 'z']], dtype=np.float64)
# 처음 속도(AU/day)
v = np.array([np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.float64)
print("r: {}, v: {}".format(r, v))

xs, ys = [], []
rs, vs, accs = [], [], []

i = 0

# 오일러 방법으로 궤도 계산
while i < (len(dts)):    
    # 위치 갱신: r ← r + v·dt
    r = r + v * dt
    
    # 태양 중력 가속도: a = -GM·r/|r|³
    acc = -2.959e-4 * r / np.sum(r**2)**(3./2)  # 태양 GM = 2.959e-4 AU³/day²
    
    # 속도 갱신: v ← v + a·dt
    v = v + acc * dt
    
    rs.append(r)
    vs.append(v)
    accs.append(acc)
    xs.append(r[0])
    ys.append(r[1])
    
    i += 1

print("len(xs): {}".format(len(xs)))
print("xs: {}".format(xs))
print("len(ys): {}".format(len(ys)))
print("ys: {}".format(ys))

print("len(rs): {}".format(len(rs)))
print("rs: {}".format(rs))

print("len(vs): {}".format(len(vs)))
print("vs: {}".format(vs))

print("len(accs): {}".format(len(accs)))
print("accs: {}".format(accs))

# 특정 시점 확인(검증용)
print("rs[5][:2]: {}".format(rs[5][:2]))
print("rs[4]: {}".format(rs[4]))
print("rs[5]: {}".format(rs[5]))

# %% code 62.
def animate(i):
    plot.set_offsets(rs[i][:2])
    line.set_xdata(xs[:i])
    line.set_ydata(ys[:i])
    timestamp.set_text('Date: ' + Time(dts[i]).iso)
    return plot, line, timestamp

from matplotlib.animation import FuncAnimation
ani = FuncAnimation(fig, animate, frames=len(dts), blit=True)

# %% code 63.
import matplotlib
import matplotlib.pyplot as plt

# 애니메이션 용량 한도 50 MB로(기본 약 20 MB)
matplotlib.rcParams['animation.embed_limit'] = 50

matplotlib.rcParams['animation.html'] = 'jshtml'
matplotlib.rcParams['animation.writer'] = 'ffmpeg'  # ffmpeg이 있을 때

print(f"Animation embed limit set to: {matplotlib.rcParams['animation.embed_limit']} MB")
print(f"Animation HTML format: {matplotlib.rcParams['animation.html']}")

from IPython.display import HTML
HTML(ani.to_jshtml())

# %% code 64.
import matplotlib
matplotlib.rcParams['animation.html'] = 'html5'
print(f"Animation HTML format: {matplotlib.rcParams['animation.html']}")
HTML(ani.to_html5_video())

# %% code 65.
import numpy as np
import matplotlib.pyplot as plt
from astropy.time import Time
from astroquery.jplhorizons import Horizons

sim_start_date = "2018-01-01"
sim_duration = 2 * 365            # 2년(일)
m_earth = 5.9722e24 / 1.98847e30  # 지구 질량(태양 질량 단위)
m_moon = 7.3477e22 / 1.98847e30   # 달 질량(태양 질량 단위)

class Object:                     # 천체 하나(태양, 행성)
    def __init__(self, name, rad, color, r, v):
        self.name = name
        self.r    = np.array(r, dtype=np.float64)  # 위치(AU)
        self.v    = np.array(v, dtype=np.float64)  # 속도(AU/day)
        self.xs = []                               # 궤적 기록
        self.ys = []
        # 현재 위치 점
        self.plot = ax.scatter(r[0], r[1], color=color, s=rad**2, edgecolors=None, zorder=10)
        # 궤도 선
        self.line, = ax.plot([], [], color=color, linewidth=1.4)

class SolarSystem:                # 태양계 전체
    def __init__(self, thesun):
        self.thesun = thesun
        self.planets = []
        self.time = None      # 줄리안 데이
        self.timestamp = ax.text(.03, .94, 'Date: ', color='w', transform=ax.transAxes, fontsize='x-large')
    
    def add_planet(self, planet):
        self.planets.append(planet)
    
    def evolve(self):             # 하루씩 궤도 계산
        dt = 1.0
        self.time += dt
        plots = []
        lines = []
        
        for p in self.planets:
            # 위치 갱신: r ← r + v·dt
            p.r += p.v * dt
            # 태양 중력 가속도(GM = 2.959e-4 AU³/day²)
            acc = -2.959e-4 * p.r / np.sum(p.r**2)**(3./2)
            # 속도 갱신: v ← v + a·dt
            p.v += acc * dt
            p.xs.append(p.r[0])
            p.ys.append(p.r[1])
            p.plot.set_offsets(p.r[:2])
            p.line.set_xdata(p.xs)
            p.line.set_ydata(p.ys)
            plots.append(p.plot)
            lines.append(p.line)
        
        self.timestamp.set_text('Date: ' + Time(self.time, format='jd').iso)
        # blit용으로 바뀐 객체 반환
        return plots + lines + [self.timestamp]

fig = plt.figure(facecolor='black')
plt.style.use('dark_background')

ax = plt.axes([0., 0., 1., 1.], xlim=(-1.8, 1.8), ylim=(-1.8, 1.8))
ax.set_aspect('equal')
ax.axis('off')

# 태양을 원점에 둔 태양계
ss = SolarSystem(Object("Sun", 28, 'red', [0, 0, 0], [0, 0, 0]))
ss.time = Time(sim_start_date).jd

colors = ['gray', 'orange', 'blue', 'chocolate']
sizes = [0.38, 0.95, 1., 0.53]                    # 상대 크기(지구 = 1)
names = ['Mercury', 'Venus', 'Earth', 'Mars']
texty = [.47, .73, 1, 1.5]                        # 이름 표시 y 위치

# 수성~화성 추가
for i, nasaid in enumerate([1, 2, 3, 4]):  # Horizons ID: 1 수성, 2 금성, 3 지구, 4 화성
    obj = Horizons(id=nasaid, location="@sun", epochs=ss.time, id_type='id').vectors()
    
    ss.add_planet(Object(nasaid,
                         20 * sizes[i],
                         colors[i],
                         [np.double(obj[xi]) for xi in ['x', 'y', 'z']], 
                         [np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']]))
    
    # 아래쪽에 이름
    ax.text(0, - (texty[i] + 0.1), names[i], color=colors[i], 
            zorder=1000, ha='center', fontsize='large')

plt.show()

# %% code 66.
# 프레임마다 하루씩 진행
def animate(i):
    return ss.evolve()
    
import matplotlib.animation as animation

ani = animation.FuncAnimation(fig,
                              animate,
                              repeat=False,
                              frames=sim_duration,  # 프레임 수 = 시뮬레이션 일수
                              blit=True,
                              interval=20)          # ms

# %% code 67.
import matplotlib
import matplotlib.pyplot as plt

# 애니메이션 용량 한도 50 MB로(기본 약 20 MB)
matplotlib.rcParams['animation.embed_limit'] = 50

matplotlib.rcParams['animation.html'] = 'jshtml'
matplotlib.rcParams['animation.writer'] = 'ffmpeg'  # ffmpeg이 있을 때

print(f"Animation embed limit set to: {matplotlib.rcParams['animation.embed_limit']} MB")
print(f"Animation HTML format: {matplotlib.rcParams['animation.html']}")

from IPython.display import HTML
HTML(ani.to_jshtml())

# %% code 68.
import matplotlib
matplotlib.rcParams['animation.html'] = 'html5'
print(f"Animation HTML format: {matplotlib.rcParams['animation.html']}")
HTML(ani.to_html5_video())

# %% code 69.
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

# %% code 70.
import numpy as np
import matplotlib.pyplot as plt
from astropy.time import Time
from astroquery.jplhorizons import Horizons
import mpl_toolkits.mplot3d.axes3d as p3

sim_start_date = "2018-01-01"
sim_duration = 2 * 365
m_earth = 5.9722e24 / 1.98847e30
m_moon = 7.3477e22 / 1.98847e30

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
ax.set_title('The Solar System (3D)', color='white', fontsize=16)

specific_time = Time(sim_start_date)

class Object:
    def __init__(self, name, rad, color, r, v):
        self.name = name
        self.r = np.array(r, dtype=np.float64)
        self.v = np.array(v, dtype=np.float64)
        self.xs = []
        self.ys = []
        self.zs = []
        self.plot = ax.scatter(r[0], r[1], r[2], color=color, s=rad**2, 
                               edgecolors=None, zorder=10)
        self.line, = ax.plot([], [], [], color=color, linewidth=1.4)

class SolarSystem:
    def __init__(self, thesun):
        self.thesun = thesun
        self.planets = []
        self.time = None
        self.timestamp = ax.text2D(.03, .94, 'Date: ', color='white', 
                                   transform=ax.transAxes, fontsize='x-large')
    
    def add_planet(self, planet):
        self.planets.append(planet)
    
    def evolve(self):
        dt = 1.0
        self.time += dt
        plots = []
        lines = []
        
        for p in self.planets:
            # 위치 갱신(오일러 방법, 앞과 같음)
            p.r += p.v * dt
            # 태양 중력 가속도(AU/day²)
            acc = -2.959e-4 * p.r / np.sum(p.r**2)**(3./2)
            # 속도 갱신
            p.v += acc * dt
            p.xs.append(p.r[0])
            p.ys.append(p.r[1])
            p.zs.append(p.r[2])
            # 3D 점 위치 갱신(내부 속성 사용)
            p.plot._offsets3d = ([p.r[0]], [p.r[1]], [p.r[2]])
            p.line.set_data_3d(p.xs, p.ys, p.zs)
            plots.append(p.plot)
            lines.append(p.line)
        
        self.timestamp.set_text('Date: ' + Time(self.time, format='jd').iso)
        return plots + lines + [self.timestamp]

# 태양(원점)
sun = ax.scatter(0, 0, 0, color="red", s=28**2, edgecolors=None, zorder=10)

ax.text2D(.03, .94, 'Date: {}'.format(specific_time.iso), color='white', 
          transform=ax.transAxes, fontsize='x-large')

ss = SolarSystem(Object("Sun", 28, 'red', [0, 0, 0], [0, 0, 0]))
ss.time = Time(sim_start_date).jd

colors = ['gray', 'orange', 'blue', 'chocolate']
sizes = [0.38, 0.95, 1., 0.53]
names = ['Mercury', 'Venus', 'Earth', 'Mars']
texty = [.47, .73, 1, 1.5]

# 수성~화성 추가(Horizons ID 1~4)
print("행성 데이터를 가져오는 중...")
for i, nasaid in enumerate([1, 2, 3, 4]):
    try:
        print(f"{names[i]} 데이터 처리 중...")
        obj = Horizons(id=nasaid, location="@sun", epochs=ss.time, id_type='id').vectors()
        
        ss.add_planet(Object(nasaid,
                             20 * sizes[i],
                             colors[i],
                             [np.double(obj[xi]) for xi in ['x', 'y', 'z']], 
                             [np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']]))
        
        ax.text(0, -(texty[i] + 0.1), 0, names[i], color=colors[i], 
                zorder=1000, ha='center', fontsize='large')
        
        print(f"{names[i]} 추가 완료")
    except Exception as e:
        print(f"{names[i]} 데이터 가져오기 실패: {e}")

print("태양계 시뮬레이션 초기화 완료!")
plt.tight_layout()
plt.show()

# %% code 71.
# 프레임마다 하루씩 진행
def animate(i):
    return ss.evolve()
    
from matplotlib.animation import FuncAnimation

ani = FuncAnimation(fig, animate,
                    frames=len(dts),  # 앞에서 만든 dts 길이만큼
                    blit=True)
                    

# %% code 72.
import matplotlib
import matplotlib.pyplot as plt

# 애니메이션 용량 한도 100 MB로(기본 약 20 MB)
matplotlib.rcParams['animation.embed_limit'] = 100

matplotlib.rcParams['animation.html'] = 'jshtml'
matplotlib.rcParams['animation.writer'] = 'ffmpeg'  # ffmpeg이 있을 때

print(f"Animation embed limit set to: {matplotlib.rcParams['animation.embed_limit']} MB")
print(f"Animation HTML format: {matplotlib.rcParams['animation.html']}")

from IPython.display import HTML
HTML(ani.to_jshtml())

# %% code 73.
import matplotlib
matplotlib.rcParams['animation.html'] = 'html5'
print(f"Animation HTML format: {matplotlib.rcParams['animation.html']}")
HTML(ani.to_html5_video())

# %% code 74.
fname = 'Solar_System_3D_Animation_Class_Based'

ani.save(f'{proj_dir}/{fname}.mp4', fps=60, dpi=150,
         writer='ffmpeg')  # ffmpeg 필요
print(f"동영상이 저장되었습니다: {proj_dir}/{fname}.mp4")

# %% code 75.
ani.save(f'{proj_dir}/{fname}.gif',
            fps=30,           # MP4보다 낮춰 용량 줄이기
            dpi=100,
            writer='pillow')
print(f"GIF 파일이 저장되었습니다: {proj_dir}/{fname}.gif")
