# 지구과학 데이터 사이언스 1 | III-04. 인공위성의 궤도 나타내기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅲ-41.
TLE_NOAA14 = '''NOAA 14                 
1 23455U 94089A   97320.90946019  .00000140  00000-0  10191-3 0  2621
2 23455  99.0090 272.6745 0008546 223.1686 136.8816 14.11711747148495'''

# %% code Ⅲ-42.
fname = "elements.txt"

# CelesTrak에서 최근 30일 발사 위성의 TLE 받기
from pathlib import Path

# 그 기간 발사 위성이 없으면 404 오류 → 우주정거장(stations) 데이터
try:
    du.download("https://celestrak.org/NORAD/elements/gp.php?GROUP=last-30-days&FORMAT=tle", Path(proj_dir) / (fname), overwrite=True)
except Exception:
    du.download("https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle", Path(proj_dir) / (fname), overwrite=True)

# %% code Ⅲ-43.
from skyfield.api import Loader

# Skyfield 데이터 파일 저장 위치
load = Loader(str(proj_dir))  

ts   = load.timescale()
print("ts: {}".format(ts))

# DE421 천체력(행성 위치)
planets = load('de421.bsp')
print("planets: {}".format(planets))

earth   = planets['earth']
print("earth: {}".format(earth))

# %% code Ⅲ-44.
import numpy as np
import matplotlib.pyplot as plt

re = 6378.  # 지구 반지름(km)

def earth_graticule(re=6378., step=15):
    """지구의 경선 · 위선 좌표 목록(원 하나가 x, y, z 배열 3줄)"""
    theta = np.linspace(0, 2*np.pi, 201)
    cth, sth, zth = np.cos(theta), np.sin(theta), np.zeros_like(theta)
    # 경선: xz 평면의 원을 z축 둘레로 step°씩 돌림
    lons = []
    for phi in np.radians(np.arange(0, 180, step)):
        cph, sph = np.cos(phi), np.sin(phi)
        lons.append(re*np.vstack((cth*cph, cth*sph, sth)))
    # 위선: 위도 phi에서 적도면과 나란한 원
    lats = []
    for phi in np.radians(np.arange(-75, 90, step)):
        cph, sph = np.cos(phi), np.sin(phi)
        lats.append(re*np.vstack((cth*cph, sth*cph, zth+sph)))
    return lons, lats

def plot_earth(ax, **kwargs):
    """3D 축에 지구의 경선 · 위선 그리기(아래에서 만든 lons, lats 사용)"""
    for x, y, z in lons + lats:
        ax.plot(x, y, z, '-k', **kwargs)

lons, lats = earth_graticule(re)
print("len(lons): {}".format(len(lons)))
print("len(lats): {}".format(len(lats)))

fig = plt.figure(figsize=[10, 10])
ax  = fig.add_subplot(1, 1, 1, projection='3d')

plot_earth(ax)

ax.set_aspect('equal')

plt.show()

# %% code Ⅲ-45.
from skyfield.api import EarthSatellite, Loader
import numpy as np

# NOAA 14 기상 위성의 TLE(기준 시각 1997-11-16)
TLE = """NOAA 14
1 23455U 94089A   97320.90946019  .00000140  00000-0  10191-3 0  2621
2 23455  99.0090 272.6745 0008546 223.1686 136.8816 14.11711747148495
"""
# 위성 이름, TLE 1행, 2행
L0, L1, L2 = TLE.splitlines()

print("L1: {}".format(L1))
print("L2: {}".format(L2))

load = Loader('./')
ts = load.timescale()

satellite = EarthSatellite(L1, L2)
print(f"TLE 기준 시각: {satellite.epoch.utc_jpl()}")

# TLE 기준 시각 무렵(1997-11-16)부터 3시간, 0.01시간 간격
hours = np.arange(0, 3, 0.01)
time = ts.utc(1997, 11, 16, hours)

# 위성 위치(km)
Rpos = satellite.at(time).position.km                # 배열 모양: (3, N)
Rposecl = satellite.at(time).ecliptic_position().km
print("Rpos.shape: {}".format(Rpos.shape))
print("Rposecl.shape: {}".format(Rposecl.shape))

# %% code Ⅲ-46.
fig = plt.figure(figsize=[10, 10])
ax  = fig.add_subplot(1, 1, 1, projection='3d')

plot_earth(ax)   # 앞에서 만든 함수로 지구 그리기

# 위성 궤도
x, y, z = Rpos
ax.plot(x, y, z)

ax.set_aspect('equal')
plt.show()

# %% code Ⅲ-47.
def makecubelimits(axis, centers=None, hw=None):
    """
    3D 플롯의 축 비율을 고정하여 정육면체 형태의 플롯 영역을 만드는 함수

    Parameters:
    -----------
    axis : matplotlib 3D axis object
        3D 플롯의 축 객체
    centers : list, optional
        각 축의 중심점 [x_center, y_center, z_center]
        지정하지 않으면 현재 축 범위의 중심으로 자동 계산
    hw : float or list, optional
        축의 반폭(half-width)
        - float: 모든 축에 동일한 반폭 적용
        - list: [x_hw, y_hw, z_hw] 각 축에 다른 반폭 적용
        - None: 현재 축 중 가장 큰 범위를 기준으로 자동 계산
    """
    lims = axis.get_xlim(), axis.get_ylim(), axis.get_zlim()

    # 중심점: 각 축 범위의 가운데
    if centers is None:
        centers = [0.5*sum(pair) for pair in lims]

    # 반폭: 가장 넓은 축 범위의 절반(정육면체 유지)
    if hw is None:
        widths = [pair[1] - pair[0] for pair in lims]
        hw = 0.5*max(widths)

    if np.ndim(hw) == 0:
        hwx = hwy = hwz = hw     # 단일 값이면 모든 축에 같은 반폭
    else:
        hwx, hwy, hwz = hw       # 리스트이면 축마다 다른 반폭

    axis.set_xlim(centers[0]-hwx, centers[0]+hwx)
    axis.set_ylim(centers[1]-hwy, centers[1]+hwy)
    axis.set_zlim(centers[2]-hwz, centers[2]+hwz)

    return centers, hw

fig = plt.figure(figsize=[10, 10])

ax  = fig.add_subplot(1, 1, 1, projection='3d')

plot_earth(ax)

# 위성 궤도
x, y, z = Rpos
ax.plot(x, y, z)

# 축 비율 고정(정육면체)
centers, hw = makecubelimits(ax)

print(f"플롯 중심점: {centers}")
print(f"축 반폭: {hw}")

ax.set_aspect('equal')

plt.show()

# %% code Ⅲ-48.
# TLE epoch(1997-11-16) 무렵의 위성 위치
time = ts.utc(1997, 11, 16, hours)
Rpos = satellite.at(time).position.km

# nan · inf 확인
print("Rpos shape:", Rpos.shape)
print("Rpos contains nan:", np.isnan(Rpos).any())
print("Rpos contains inf:", np.isinf(Rpos).any())

# nan이 있으면 시간 범위와 TLE epoch을 맞추기
r_sat = np.sqrt((Rpos**2).sum(axis=0))

# 고도 = 지구 중심 거리 - 지구 반지름
alt_sat = r_sat - re

plt.figure(figsize=(12, 6))

plt.plot(hours, r_sat, 'b-', linewidth=2, label='지구 중심 거리 (km)')
plt.plot(hours, alt_sat, 'r-', linewidth=2, label='고도 (km)')

plt.xlabel('시간 (hours)', fontsize=14)
plt.ylabel('거리 (km)', fontsize=14)
plt.title(f'{L0} 위성의 지구 중심 거리 및 고도 변화', fontsize=16)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)

print(f"최대 고도: {alt_sat.max():.2f} km")
print(f"최소 고도: {alt_sat.min():.2f} km")
print(f"평균 고도: {alt_sat.mean():.2f} km")

plt.tight_layout()
plt.show()

# %% code Ⅲ-49.
# 스타링크 위성 TLE(STARLINK-1007, 기준 시각 2024-05-21)
# TLE는 글자 위치로 값을 읽는 고정 폭 형식이라 빈칸 수를 바꾸면 안 됨
TLE = """STARLINK-1007
1 44713U 19074A   24142.62636216  .00014211  00000+0  97051-3 0  9998
2 44713  53.0541 256.2864 0001579  91.4399 268.6771 15.06419455249719"""

L0, L1, L2 = TLE.splitlines()

load = Loader(str(proj_dir))
ts   = load.timescale()

# 위성 객체와 위치 계산
sat = EarthSatellite(L1, L2, L0, ts)
print(f"TLE 기준 시각: {sat.epoch.utc_jpl()}")

# TLE 기준 시각부터 3시간, 0.01시간 간격
hours = np.arange(0, 3, 0.01)
time = ts.tt_jd(sat.epoch.tt + hours/24)

Rpos = sat.at(time).position.km
print(Rpos.shape)

# 3D 궤도 그리기(지구는 앞에서 만든 plot_earth 함수로)
fig = plt.figure(figsize=[10, 10])
ax  = fig.add_subplot(1, 1, 1, projection='3d')

x, y, z = Rpos
ax.plot(x, y, z)
plot_earth(ax)

centers, hw = makecubelimits(ax)
print("플롯 중심점: ", centers)
print("축 반폭:     ", hw)

plt.show()

# 지구 중심 거리와 고도
r_sat = np.sqrt((Rpos**2).sum(axis=0))
alt_sat = r_sat - re

plt.figure()
plt.plot(hours, r_sat, label='지구 중심 거리')
plt.plot(hours, alt_sat, label='고도')
plt.xlabel('시간 (hours)', fontsize=14)
plt.ylabel('지구 중심 거리 또는 고도 (km)', fontsize=14)
plt.legend()
plt.show()

# 축 비율을 고정한 3D 궤도
fig = plt.figure(figsize=[12, 10])
ax = fig.add_subplot(1, 1, 1, projection='3d')

plot_earth(ax, alpha=0.3)

x, y, z = Rpos
ax.plot(x, y, z, 'r-', linewidth=2, label='Starlink 위성 궤도')

ax.set_xlabel('X (km)', fontsize=12)
ax.set_ylabel('Y (km)', fontsize=12)
ax.set_zlabel('Z (km)', fontsize=12)

ax.set_title('Starlink 위성의 3D 궤도 시각화 (축 비율 고정)', fontsize=14)
ax.legend()

centers, hw = makecubelimits(ax)

ax.set_aspect('equal')

plt.tight_layout()
plt.show()

# %% code Ⅲ-50.
import requests

# CelesTrak 새 주소(예전 stations.txt는 404)
url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle"

try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()  # HTTP 오류면 예외 발생
    
    print("TLE 데이터 내려받기 완료!")
    print(f"응답 상태 코드: {response.status_code}")
    print(f"데이터 크기: {len(response.text)} bytes")
    
except requests.exceptions.RequestException as e:
    print(f"TLE 데이터 내려받기 실패: {e}")
    response = None

iss_tle = []  # 내려받기에 실패해도 이름은 있도록 미리 비워 두기

# ZARYA: ISS 첫 모듈 이름(TLE에서 ISS를 찾는 표지)
if response:
    lines = response.text.splitlines()
    
    for i, line in enumerate(lines):
        if "ISS (ZARYA)" in line:
            iss_tle = lines[i:i+3]  # 위성 이름 + TLE 2줄
            break
    
    if iss_tle:
        print("\n✓ ISS 최신 TLE 데이터:")
        for j, l in enumerate(iss_tle):
            if j == 0:
                print(f"  위성명: {l}")
            else:
                print(f"  TLE Line {j}: {l}")
    else:
        print("⚠  ISS (ZARYA) TLE를 찾지 못했습니다.")
        print("텍스트에서 사용 가능한 위성들:")
        for line in lines[:10]:
            if line.strip():
                print(f"  - {line}")
else:
    print("네트워크 오류로 인해 TLE 데이터를 가져올 수 없습니다.")

# %% code Ⅲ-51.
from datetime import date
from skyfield.api import EarthSatellite

# ISS 위성 객체(앞에서 받은 최신 TLE: 이름, 1행, 2행)
sat = EarthSatellite(iss_tle[1], iss_tle[2], iss_tle[0].strip(), ts)
print(f"TLE 기준 시각: {sat.epoch.utc_jpl()}")

# 오늘 날짜(UTC) 0시부터 3시간, 0.01시간 간격
today = date.today()
print(f"오늘 날짜: {today}")
hours = np.arange(0, 3, 0.01)
time = ts.utc(today.year, today.month, today.day, hours)

# 위성의 위치(지구 중심 좌표, km)
Rpos = sat.at(time).position.km
print("Rpos.shape:", Rpos.shape)

# %% code Ⅲ-52.
fig = plt.figure(figsize=[10, 10])
ax  = fig.add_subplot(1, 1, 1, projection='3d')

plot_earth(ax, linewidth=0.5)
x, y, z = Rpos
ax.plot(x, y, z, label='ISS 궤도')

centers, hw = makecubelimits(ax)
print(f"플롯 중심점: {centers}")
print(f"축 반폭: {hw}")

ax.set_aspect('equal')
ax.set_title('국제우주정거장(ISS) 궤도')
ax.legend()
plt.show()

# %% code Ⅲ-53.
# 지구 중심 거리와 고도
r_sat = np.sqrt((Rpos**2).sum(axis=0))
alt_sat = r_sat - re

plt.figure()
plt.plot(hours, r_sat, label='지구 중심 거리')
plt.plot(hours, alt_sat, label='고도')
plt.xlabel('시간 (hours)', fontsize=14)
plt.ylabel('지구 중심 거리 또는 고도 (km)', fontsize=14)
plt.title('ISS 고도 변화')
plt.legend()
plt.show()

print(f"최대 고도: {alt_sat.max():.2f} km")
print(f"최소 고도: {alt_sat.min():.2f} km")
print(f"평균 고도: {alt_sat.mean():.2f} km")

# %% code Ⅲ-54.
import requests
from skyfield.api import EarthSatellite

# 1) 스타링크 TLE 내려받기
url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle"

tle_file = proj_dir / "starlink.tle"  # 받은 파일을 저장해 두고 다시 씀
try:
    # CelesTrak은 같은 데이터를 짧은 간격으로 다시 받으면 403 오류를 돌려줌
    if not tle_file.exists():
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        tle_file.write_text(response.text, encoding="utf-8")
    lines = tle_file.read_text(encoding="utf-8").splitlines()
    print(f"스타링크 TLE 총 줄 수: {len(lines)}")
except requests.exceptions.RequestException as e:
    print(f"스타링크 TLE 데이터 내려받기 실패: {e}")
    lines = []

# 2) 첫 번째 스타링크 위성의 TLE 찾기: 이름 줄 다음에 '1 ', '2 '로 시작하는 두 줄
starlink_name, starlink_tle = None, []
for i in range(len(lines)-2):
    if (lines[i].strip() and lines[i+1].startswith('1 ') and lines[i+2].startswith('2 ')):
        starlink_name = lines[i].strip()
        starlink_tle = [lines[i+1].strip(), lines[i+2].strip()]
        break

if starlink_tle:
    print(f"위성명: {starlink_name}")
    print(f"TLE 1행: {starlink_tle[0]}")
    print(f"TLE 2행: {starlink_tle[1]}")

    # 3) 궤도 계산: 오늘 날짜(UTC) 0시부터 3시간, 0.01시간(약 36초) 간격
    sat = EarthSatellite(starlink_tle[0], starlink_tle[1], starlink_name, ts)
    print(f"TLE 기준 시각: {sat.epoch.utc_jpl()}")
    hours = np.arange(0, 3, 0.01)
    today = date.today()
    time = ts.utc(today.year, today.month, today.day, hours)
    Rpos = sat.at(time).position.km   # 지구 중심 좌표(km)

    # 4) 3D 궤도 그리기(앞에서 만든 plot_earth, makecubelimits 사용)
    fig = plt.figure(figsize=[12, 10])
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    plot_earth(ax, linewidth=0.5, alpha=0.7)
    x, y, z = Rpos
    ax.plot(x, y, z, 'r-', linewidth=2, label=f'{starlink_name}')
    centers, hw = makecubelimits(ax)

    ax.set_xlabel('X (km)', fontsize=12)
    ax.set_ylabel('Y (km)', fontsize=12)
    ax.set_zlabel('Z (km)', fontsize=12)
    ax.set_title(f"스타링크 위성 궤도 시각화\n{starlink_name}", fontsize=14)
    ax.legend(fontsize=12)

    # 5) 고도 통계
    alt_satellite = np.sqrt((Rpos**2).sum(axis=0)) - re
    print(f"최대 고도: {alt_satellite.max():.2f} km")
    print(f"최소 고도: {alt_satellite.min():.2f} km")
    print(f"평균 고도: {alt_satellite.mean():.2f} km")

    plt.tight_layout()
    plt.show()
else:
    print("스타링크 위성 TLE 데이터를 찾을 수 없습니다.")
