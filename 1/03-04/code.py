# 지구과학 데이터 사이언스 1 | III-04. 인공위성의 궤도 나타내기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 41.
TLE_NOAA14 = '''NOAA 14                 
1 23455U 94089A   97320.90946019  .00000140  00000-0  10191-3 0  2621
2 23455  99.0090 272.6745 0008546 223.1686 136.8816 14.11711747148495'''

# %% code 42.
fname = "elements.txt"

# CelesTrak에서 최근 30일 발사 위성의 TLE 받기
from pathlib import Path

# 그 기간 발사 위성이 없으면 404 오류 → 우주정거장(stations) 자료
try:
    du.download("https://celestrak.org/NORAD/elements/gp.php?GROUP=last-30-days&FORMAT=tle", Path(proj_dir) / (fname), overwrite=True)
except Exception:
    du.download("https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle", Path(proj_dir) / (fname), overwrite=True)

# %% code 43.
from skyfield.api import Loader

# Skyfield 자료 파일 저장 위치
load = Loader(str(proj_dir))  

ts   = load.timescale()
print("ts: {}".format(ts))

# DE421 천체력(행성 위치)
planets = load('de421.bsp')
print("planets: {}".format(planets))

earth   = planets['earth']
print("earth: {}".format(earth))

# %% code 44.
import numpy as np
from math import pi

halfpi, pi, twopi = [f*np.pi for f in (0.5, 1, 2)]
degs, rads = 180/pi, pi/180  # 도 ↔ 라디안 변환

# 지구 반지름(km)
re = 6378.

theta = np.linspace(0, twopi, 201)
cth, sth, zth = [f(theta) for f in [np.cos, np.sin, np.zeros_like]]

# 경선
lon0 = re*np.vstack((cth, zth, sth))
lons = []
for phi in rads*np.arange(0, 180, 15):
    cph, sph = [f(phi) for f in (np.cos, np.sin)]
    lon = np.vstack((lon0[0]*cph - lon0[1]*sph,
                     lon0[1]*cph + lon0[0]*sph,
                     lon0[2]) )
    lons.append(lon)

# 위선
lat0 = re*np.vstack((cth, sth, zth))
lats = []
for phi in rads*np.arange(-75, 90, 15):
    cph, sph = [f(phi) for f in (np.cos, np.sin)]
    lat = re*np.vstack((cth*cph, sth*cph, zth+sph))
    lats.append(lat)

print("len(lons): {}".format(len(lons)))
print("len(lats): {}".format(len(lats)))

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize=[10, 10])

ax  = fig.add_subplot(1, 1, 1, projection='3d')

for x, y, z in lons:
    ax.plot(x, y, z, '-k')
for x, y, z in lats:
    ax.plot(x, y, z, '-k')

ax.set_aspect('equal')

plt.show()

# %% code 45.
from skyfield.api import EarthSatellite, Loader
import numpy as np

# TLE 자료(뒤의 NOAA 14가 쓰임)
TLE = """STARLINK-1007
1 44713U 19074A 24142.62636216 .00014211 00000+0 97051-3 0 9998
2 44713 53.0541 256.2864 0001579 91.4399 268.6771 15.06419455249719
"""
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

hours = np.arange(0, 3, 0.01)
time = ts.utc(2018, 2, 7, hours)

# 위성 위치(km)
Rpos = satellite.at(time).position.km                # 배열 모양: (3, N)
Rposecl = satellite.at(time).ecliptic_position().km
print("Rpos.shape: {}".format(Rpos.shape))
print("Rposecl.shape: {}".format(Rposecl.shape))

hours = np.arange(0, 3, 0.01)
time = ts.utc(2018, 2, 7, hours)

# %% code 46.
halfpi, pi, twopi = [f*np.pi for f in (0.5, 1, 2)]
degs, rads = 180/pi, pi/180

# 지구 반지름(km)
re = 6378.

theta = np.linspace(0, twopi, 201)
cth, sth, zth = [f(theta) for f in [np.cos, np.sin, np.zeros_like]]

# 경선
lon0 = re*np.vstack((cth, zth, sth))
lons = []
for phi in rads*np.arange(0, 180, 15):
    cph, sph = [f(phi) for f in (np.cos, np.sin)]
    lon = np.vstack((lon0[0]*cph - lon0[1]*sph,
                     lon0[1]*cph + lon0[0]*sph,
                     lon0[2]) )
    lons.append(lon)

# 위선
lat0 = re*np.vstack((cth, sth, zth))
lats = []
for phi in rads*np.arange(-75, 90, 15):
    cph, sph = [f(phi) for f in (np.cos, np.sin)]
    lat = re*np.vstack((cth*cph, sth*cph, zth+sph))
    lats.append(lat)

fig = plt.figure(figsize=[10, 10])

ax  = fig.add_subplot(1, 1, 1, projection='3d')

for x, y, z in lons:
    ax.plot(x, y, z, '-k')
for x, y, z in lats:
    ax.plot(x, y, z, '-k')

# 위성 궤도
x, y, z = Rpos
ax.plot(x, y, z)

ax.set_aspect('equal')

plt.show()

# %% code 47.
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
    lims = ax.get_xlim(), ax.get_ylim(), ax.get_zlim()
    
    # 중심점: 각 축 범위의 가운데
    if centers == None:
        centers = [0.5*sum(pair) for pair in lims]
        print(f"중심점 자동 계산: {centers}")

    # 반폭: 가장 넓은 축 범위의 절반(정육면체 유지)
    if hw == None:
        widths = [pair[1] - pair[0] for pair in lims]
        hw = 0.5*max(widths)
        
        ax.set_xlim(centers[0]-hw, centers[0]+hw)
        ax.set_ylim(centers[1]-hw, centers[1]+hw)
        ax.set_zlim(centers[2]-hw, centers[2]+hw)
        print(f"반폭 자동 계산: {hw}")
    else:
        try:
            # hw가 리스트이면 축마다 다른 반폭
            hwx, hwy, hwz = hw
            print(f"각 축에 다른 반폭 적용: x={hwx}, y={hwy}, z={hwz}")

            ax.set_xlim(centers[0]-hwx, centers[0]+hwx)
            ax.set_ylim(centers[1]-hwy, centers[1]+hwy)
            ax.set_zlim(centers[2]-hwz, centers[2]+hwz)
        except:
            # hw가 단일 값이면 모든 축에 같은 반폭
            print(f"모든 축에 동일한 반폭 적용: {hw}")
            ax.set_xlim(centers[0]-hw, centers[0]+hw)
            ax.set_ylim(centers[1]-hw, centers[1]+hw)
            ax.set_zlim(centers[2]-hw, centers[2]+hw)

    return centers, hw

fig = plt.figure(figsize=[10, 10])

ax  = fig.add_subplot(1, 1, 1, projection='3d')

for x, y, z in lons:
    ax.plot(x, y, z, '-k')
for x, y, z in lats:
    ax.plot(x, y, z, '-k')

# 위성 궤도
x, y, z = Rpos
ax.plot(x, y, z)

# 축 비율 고정(정육면체)
centers, hw = makecubelimits(ax)

print(f"플롯 중심점: {centers}")
print(f"축 반폭: {hw}")

ax.set_aspect('equal')

plt.show()

# %% code 48.
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

# %% code 49.
TLE = """STARLINK-1007
1 44713U 19074A 24142.62636216 .00014211 00000+0 97051-3 0 9998
2 44713 53.0541 256.2864 0001579 91.4399 268.6771 15.06419455249719"""

L0, L1, L2 = TLE.splitlines()

halfpi, pi, twopi = [f*np.pi for f in [0.5, 1, 2]]
degs, rads = 180/pi, pi/180

load = Loader(str(proj_dir))  
ts   = load.timescale()

planets = load('de421.bsp')
earth   = planets['earth']

# 위성 객체와 위치 계산
Roadster = EarthSatellite(L1, L2)

print(Roadster.epoch.tt)
hours = np.arange(0, 3, 0.01)

time = ts.utc(2018, 2, 7, hours)

Rpos    = Roadster.at(time).position.km
Rposecl = Roadster.at(time).ecliptic_position().km

print(Rpos.shape)

# 지구 경선 · 위선
re = 6378.

theta = np.linspace(0, twopi, 201)
cth, sth, zth = [f(theta) for f in [np.cos, np.sin, np.zeros_like]]
lon0 = re*np.vstack((cth, zth, sth))
lons = []
for phi in rads*np.arange(0, 180, 15):
    cph, sph = [f(phi) for f in [np.cos, np.sin]]
    lon = np.vstack((lon0[0]*cph - lon0[1]*sph,
                     lon0[1]*cph + lon0[0]*sph,
                     lon0[2]) )
    lons.append(lon)

lat0 = re*np.vstack((cth, sth, zth))
lats = []
for phi in rads*np.arange(-75, 90, 15):
    cph, sph = [f(phi) for f in [np.cos, np.sin]]
    lat = re*np.vstack((cth*cph, sth*cph, zth+sph))
    lats.append(lat)

# 3D 궤도 그리기
if True:    
    fig = plt.figure(figsize=[10, 10])

    ax  = fig.add_subplot(1, 1, 1, projection='3d')

    x, y, z = Rpos
    ax.plot(x, y, z)
    for x, y, z in lons:
        ax.plot(x, y, z, '-k')
    for x, y, z in lats:
        ax.plot(x, y, z, '-k')

    centers, hw = makecubelimits(ax)

    print("centers are: ", centers)
    print("hw is:       ", hw)

    plt.show()

# 지구 중심 거리와 고도
r_Roadster = np.sqrt((Rpos**2).sum(axis=0))
alt_roadster = r_Roadster - re

if True:
    plt.figure()
    plt.plot(hours, r_Roadster)
    plt.plot(hours, alt_roadster)
    plt.xlabel('hours', fontsize=14)
    plt.ylabel('Geocenter radius or altitude (km)', fontsize=14)
    plt.show()

# 축 비율을 고정한 3D 궤도
fig = plt.figure(figsize=[12, 10])
ax = fig.add_subplot(1, 1, 1, projection='3d')

for x, y, z in lons:
    ax.plot(x, y, z, '-k', alpha=0.3)

for x, y, z in lats:
    ax.plot(x, y, z, '-k', alpha=0.3)

x, y, z = Rpos
ax.plot(x, y, z, 'r-', linewidth=2, label='Starlink 위성 궤도')

ax.set_xlabel('X (km)', fontsize=12)
ax.set_ylabel('Y (km)', fontsize=12)
ax.set_zlabel('Z (km)', fontsize=12)

ax.set_title('Starlink 위성의 3D 궤도 시각화 (축 비율 고정)', fontsize=14)
ax.legend()

centers, hw = makecubelimits(ax)

print(f"플롯 중심점: {centers}")
print(f"축 반폭: {hw}")

ax.set_aspect('equal')
 
plt.tight_layout()
plt.show()

# %% code 50.
import requests

# CelesTrak 새 주소(예전 stations.txt는 404)
url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle"

try:
    response = requests.get(url)
    response.raise_for_status()  # HTTP 오류면 예외 발생
    
    print("TLE 데이터 다운로드 완료!")
    print(f"응답 상태 코드: {response.status_code}")
    print(f"데이터 크기: {len(response.text)} bytes")
    
except requests.exceptions.RequestException as e:
    print(f"TLE 데이터 다운로드 실패: {e}")
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

# %% code 51.
from datetime import date, datetime
import pytz

# 오늘 날짜
today = date.today()
print("=== 현재 날짜 정보 ===")
print(f"오늘 날짜: {today}")
print(f"년도: {today.year}")
print(f"월: {today.month}")
print(f"일: {today.day}")

now = datetime.now()
print(f"\n현재 시간: {now.strftime('%Y-%m-%d %H:%M:%S')}")

from skyfield.api import Loader, EarthSatellite
from skyfield.timelib import Time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 3D 축 비율 고정 함수(앞과 같음)
def makecubelimits(axis, centers=None, hw=None):
    lims = ax.get_xlim(), ax.get_ylim(), ax.get_zlim()
    if centers == None:
        centers = [0.5*sum(pair) for pair in lims] 

    if hw == None:
        widths  = [pair[1] - pair[0] for pair in lims]
        hw      = 0.5*max(widths)
        ax.set_xlim(centers[0]-hw, centers[0]+hw)
        ax.set_ylim(centers[1]-hw, centers[1]+hw)
        ax.set_zlim(centers[2]-hw, centers[2]+hw)
        print("hw was None so set to:", hw)
    else:
        try:
            hwx, hwy, hwz = hw
            print("ok hw requested: ", hwx, hwy, hwz)

            ax.set_xlim(centers[0]-hwx, centers[0]+hwx)
            ax.set_ylim(centers[1]-hwy, centers[1]+hwy)
            ax.set_zlim(centers[2]-hwz, centers[2]+hwz)
        except:
            print("nope hw requested: ", hw)
            ax.set_xlim(centers[0]-hw, centers[0]+hw)
            ax.set_ylim(centers[1]-hw, centers[1]+hw)
            ax.set_zlim(centers[2]-hw, centers[2]+hw)

    return centers, hw

halfpi, pi, twopi = [f*np.pi for f in [0.5, 1, 2]]
degs, rads = 180/pi, pi/180

load = Loader(str(proj_dir))  
ts   = load.timescale()

planets = load('de421.bsp')
earth   = planets['earth']

# ISS 위성 객체
Roadster = EarthSatellite(iss_tle[1], iss_tle[2])

print(Roadster.epoch.tt)
# 0~3시간, 0.01시간 간격
hours = np.arange(0, 3, 0.01)

# 오늘 날짜(UTC)
from datetime import date
time = ts.utc(date.today().year, date.today().month, date.today().day, hours)

print("time: {}".format(time))

# 위성의 위치 계산
Rpos    = Roadster.at(time).position.km
Rposecl = Roadster.at(time).ecliptic_position().km

print(Rpos.shape)

# 지구 반지름(km)
re = 6378.

# 지구 경선 · 위선
theta = np.linspace(0, twopi, 201)
cth, sth, zth = [f(theta) for f in [np.cos, np.sin, np.zeros_like]]

lon0 = re*np.vstack((cth, zth, sth))
lons = []
for phi in rads*np.arange(0, 180, 15):
    cph, sph = [f(phi) for f in [np.cos, np.sin]]
    lon = np.vstack((lon0[0]*cph - lon0[1]*sph,
                     lon0[1]*cph + lon0[0]*sph,
                     lon0[2]) )
    lons.append(lon)

lat0 = re*np.vstack((cth, sth, zth))
lats = []
for phi in rads*np.arange(-75, 90, 15):
    cph, sph = [f(phi) for f in [np.cos, np.sin]]
    lat = re*np.vstack((cth*cph, sth*cph, zth+sph))
    lats.append(lat)

# 3D 궤도 그리기
if True:    
    fig = plt.figure(figsize=[10, 10])

    ax  = fig.add_subplot(1, 1, 1, projection='3d')

    for x, y, z in lons:
        ax.plot(x, y, z, '-k', linewidth=0.5)
    for x, y, z in lats:
        ax.plot(x, y, z, '-k', linewidth=0.5)
    x, y, z = Rpos
    ax.plot(x, y, z, label='ISS 궤도')

    centers, hw = makecubelimits(ax)

    print(f"플롯 중심점: {centers}")
    print(f"축 반폭: {hw}")

    ax.set_aspect('equal')

    ax.set_title('국제우주정거장(ISS) 궤도')
    ax.legend()
    plt.show()

# 고도 그래프
r_Roadster = np.sqrt((Rpos**2).sum(axis=0))
alt_roadster = r_Roadster - re

if True:
    plt.figure()
    plt.plot(hours, r_Roadster, label='지구 중심 거리')
    plt.plot(hours, alt_roadster, label='고도')
    plt.xlabel('시간 (hours)', fontsize=14)
    plt.ylabel('지구 중심 거리 또는 고도 (km)', fontsize=14)
    plt.title('ISS 고도 변화')
    plt.legend()
    plt.show()

# ISS 궤도 계산(1분 간격)
if 'iss_tle' in locals() and iss_tle:
    print("\n=== ISS 궤도 계산 시작 ===")
    
    # iss_tle[0]은 위성 이름
    if len(iss_tle) >= 3:
        iss_line1 = iss_tle[1]
        iss_line2 = iss_tle[2]
        
        iss = EarthSatellite(iss_line1, iss_line2, name='ISS')
        
        ts = load.timescale()
        
        hours_range = np.arange(0, 3, 1/60)  # 3시간, 1분 간격
        
        time_iss = ts.utc(today.year, today.month, today.day, hours_range)
        
        iss_positions = iss.at(time_iss).position.km
        
        print(f"ISS 위치 데이터 형태: {iss_positions.shape}")
        print(f"계산 시간 범위: {len(hours_range)}개 시점 (3시간, 1분 간격)")
        print(f"ISS Epoch: {iss.epoch.utc_jpl()}")
        
    else:
        print("⚠  TLE 데이터 형식이 올바르지 않습니다.")
else:
    print("⚠  ISS TLE 데이터가 없어 궤도 계산을 수행할 수 없습니다.")
    print("이전 셀에서 TLE 데이터를 먼저 다운로드해주세요.")

# %% code 52.
import requests
from skyfield.api import Loader, EarthSatellite
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

print("=== 스타링크 위성 TLE 데이터 다운로드 ===")

# 1) 스타링크 TLE 내려받기
url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle"

tle_file = proj_dir / "starlink.tle"  # 받은 파일을 저장해 두고 다시 씀
try:
    # CelesTrak은 같은 자료를 짧은 간격으로 다시 받으면 403 오류를 돌려줌
    if not tle_file.exists():
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        tle_file.write_text(response.text, encoding="utf-8")
    lines = tle_file.read_text(encoding="utf-8").splitlines()
    
    print(f"✓ 스타링크 TLE 데이터 다운로드 완료!")
    print(f"  - 총 라인 수: {len(lines)}")
    
    # 2) 첫 번째 스타링크 위성의 TLE 찾기
    starlink_name = None
    starlink_tle = []
    
    for i in range(len(lines)-2):
        # 이름 줄 다음에 '1 ', '2 '로 시작하는 두 줄
        if (lines[i].strip() and 
            i+1 < len(lines) and lines[i+1].strip().startswith('1 ') and
            i+2 < len(lines) and lines[i+2].strip().startswith('2 ')):
            
            starlink_name = lines[i].strip()
            starlink_tle = [lines[i+1].strip(), lines[i+2].strip()]
            break
    
    if starlink_name and starlink_tle:
        print(f"\n✓ 스타링크 위성 TLE 추출 완료:")
        print(f"  위성명: {starlink_name}")
        print(f"  TLE Line 1: {starlink_tle[0]}")
        print(f"  TLE Line 2: {starlink_tle[1]}")
        
        # 3) Skyfield로 궤도 계산
        print(f"\n=== 궤도 계산 시작 ===")
        
        load = Loader(str(proj_dir))
        ts = load.timescale()
        
        sat = EarthSatellite(starlink_tle[0], starlink_tle[1], starlink_name, ts)
        
        # 0~3시간, 0.01시간(약 36초) 간격
        hours = np.arange(0, 3, 0.01)
        from datetime import date
        time = ts.utc(date.today().year, date.today().month, date.today().day, hours)
        
        # 지구 중심 좌표(km)
        Rpos = sat.at(time).position.km
        
        print(f"✓ 궤도 계산 완료:")
        print(f"  - 위성 위치 데이터 형태: {Rpos.shape}")
        print(f"  - 계산 시간 범위: {len(hours)}개 시점 (3시간)")
        print(f"  - 위성 Epoch: {sat.epoch.utc_jpl()}")
        
        # 4) 지구 경선 · 위선
        print(f"\n=== 지구 3D 좌표계 생성 ===")
        
        re = 6378.                            # 지구 반지름(km)
        theta = np.linspace(0, 2*np.pi, 201)
        cth, sth, zth = [f(theta) for f in [np.cos, np.sin, np.zeros_like]]
        
        lon0 = re*np.vstack((cth, zth, sth))
        lons = []
        for phi in np.radians(np.arange(0, 180, 15)):
            cph, sph = np.cos(phi), np.sin(phi)
            lon = np.vstack((lon0[0]*cph - lon0[1]*sph,
                             lon0[1]*cph + lon0[0]*sph,
                             lon0[2]))
            lons.append(lon)
        
        lat0 = re*np.vstack((cth, sth, zth))
        lats = []
        for phi in np.radians(np.arange(-75, 90, 15)):
            cph, sph = np.cos(phi), np.sin(phi)
            lat = re*np.vstack((cth*cph, sth*cph, zth+sph))
            lats.append(lat)
        
        print(f"✓ 지구 좌표계 생성 완료:")
        print(f"  - 경선 개수: {len(lons)}")
        print(f"  - 위선 개수: {len(lats)}")
        
        # 5) 3D 궤도 그리기
        print(f"\n=== 3D 시각화 생성 ===")
        
        fig = plt.figure(figsize=[12, 10])
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        
        for x, y, z in lons:
            ax.plot(x, y, z, '-k', linewidth=0.5, alpha=0.7)
        
        for x, y, z in lats:
            ax.plot(x, y, z, '-k', linewidth=0.5, alpha=0.7)
        
        x, y, z = Rpos
        ax.plot(x, y, z, 'r-', linewidth=2, label=f'{starlink_name}')
        
        # 앞에서 정의한 축 비율 고정 함수
        if 'makecubelimits' in locals():
            centers, hw = makecubelimits(ax)
            print(f"✓ 축 비율 고정 적용: 중심점 {centers}, 반폭 {hw}")
        
        ax.set_xlabel('X (km)', fontsize=12)
        ax.set_ylabel('Y (km)', fontsize=12)
        ax.set_zlabel('Z (km)', fontsize=12)
        ax.set_title(f"스타링크 위성 궤도 시각화\n{starlink_name}", fontsize=14)
        ax.legend(fontsize=12)
        
        # 고도 통계
        r_satellite = np.sqrt((Rpos**2).sum(axis=0))
        alt_satellite = r_satellite - re
        
        print(f"\n=== 위성 궤도 정보 ===")
        print(f"최대 고도: {alt_satellite.max():.2f} km")
        print(f"최소 고도: {alt_satellite.min():.2f} km")
        print(f"평균 고도: {alt_satellite.mean():.2f} km")
        print(f"고도 변화 범위: {alt_satellite.max()-alt_satellite.min():.2f} km")
        
        plt.tight_layout()
        plt.show()
        
    else:
        print("⚠  스타링크 위성 TLE 데이터를 찾을 수 없습니다.")
        print("다운로드된 데이터의 처음 몇 라인:")
        for i, line in enumerate(lines[:10]):
            print(f"  {i+1}: {line}")
            
except requests.exceptions.RequestException as e:
    print(f"✗ 스타링크 TLE 데이터 다운로드 실패: {e}")
    print("네트워크 연결을 확인하거나 나중에 다시 시도해주세요.")
