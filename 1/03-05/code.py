# 지구과학 데이터 사이언스 1 | III-05. 태양계 시뮬레이션
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 53.
# astropy 라이브러리에서 Time 클래스를 가져옴 (천문학적 시간 처리용)
from astropy.time import Time

# 특정 시간을 설정 (2017년 1월 1일)
specific_time = Time("2017-01-01")

# NASA JPL Horizons 데이터베이스에서 천체 데이터를 가져오기 위한 라이브러리
from astroquery.jplhorizons import Horizons

# 태양계 첫번째 행성(수성)의 위치와 속도 벡터 얻기
obj1 = Horizons(id = 1,                    # 천체 ID (1 = 수성)
                location="@sun",                # 관측 위치 (태양 중심)
                epochs=specific_time.jd,        # 시간 (줄리안 데이 형식)
                id_type='majorbody').vectors()  # 주요 천체 타입으로 벡터 데이터 요청

# 결과 자료형 출력
print("type(obj1): ", type(obj1))

# 수성의 위치와 속도 벡터 데이터 출력
print("obj1: ",obj1)

# %% code 54.
import numpy as np
from astropy.time import Time, TimeDelta

# 특정 시각을 문자열로 정의
specific_time_str = "2017-01-01"
print("type(specific_time_str):", type(specific_time_str))  # 문자열 타입 확인
print("specific_time_str", specific_time_str)

# Time 함수를 이용하여 문자열을 astropy Time 객체로 변환
specific_time = Time(specific_time_str)

print("specific_time:", specific_time)               # Time 객체 출력
print("type(specific_time): ", type(specific_time))  # Time 객체 타입 확인

# 줄리안 데이(Julian Day) 형식으로 시간 객체 생성
specific_time_jd = Time(specific_time.jd, format="jd")
print("type(specific_time.jd):", type(specific_time.jd))  # 줄리안 데이 값의 타입 확인
print("specific_time.jd: ", specific_time.jd)  # 줄리안 데이 값 출력
print("specific_time_jd.iso: {}".format(specific_time_jd.iso))  # ISO 형식으로 변환하여 출력

# 시뮬레이션 시작 및 종료 시간 설정
start_time_text = "2017-01-01"  # 시작 날짜
end_time_text = "2017-02-01"    # 종료 날짜

dt = 1  # 시간 간격 (1일)

def astropyTime_range(start, end, delta):
    """
    시작 시간부터 종료 시간까지 일정한 간격으로 시간을 생성하는 제너레이터 함수
    
    Parameters:
    start: 시작 시간 (astropy Time 객체)
    end: 종료 시간 (astropy Time 객체)
    delta: 시간 간격 (TimeDelta 객체)
    """
    current = start       # 현재 시간을 시작 시간으로 초기화
    while current < end:  # 현재 시간이 종료 시간보다 작을 때까지 반복
        yield current     # 현재 시간 반환
        current += delta  # 시간 간격만큼 증가

# 시작 시간부터 종료 시간까지 1일 간격으로 시간 목록 생성
dts = [dt.iso for dt in 
       astropyTime_range(Time(start_time_text), Time(end_time_text), 
       TimeDelta(dt, format='jd'))]

print("len(dts) :", len(dts))  # 생성된 시간 목록의 길이 출력
print("dts :", dts)            # 생성된 시간 목록 출력 (ISO 형식)

# %% code 55.
import matplotlib.pyplot as plt

# 4x4 인치 크기의 그림 생성
fig = plt.figure(figsize=[4, 4])

# 축 설정: 전체 영역 사용, x축과 y축 범위를 -1.8부터 1.8까지 설정
ax = plt.axes([0., 0., 1., 1.], 
              xlim=(-1.8, 1.8), 
              ylim=(-1.8, 1.8))

# 축의 비율을 동일하게 설정 (원이 찌그러지지 않도록)
ax.set_aspect('equal')

# x축과 y축 레이블 설정
ax.set_xlabel('x')
ax.set_ylabel('y')

# 격자 표시
ax.grid(True)

# 태양을 원점(0, 0)에 그리기
plot = ax.scatter(0, 0,                    # 위치: 원점 (0, 0)
                  color = "red",      # 색상: 빨간색 (태양을 상징)
                  s = 28**2,          # 크기: 28의 제곱 (점의 크기는 제곱 단위)
                  edgecolors = None,  # 테두리 색상: 없음
                  zorder = 10)        # 그리기 순서: 10 (다른 객체보다 앞에 표시)

# %% code 56.
import matplotlib.pyplot as plt

# 배경을 검게 만들기 위한 어두운 테마 적용
plt.style.use('dark_background')

# 축 설정: 전체 영역 사용, x축과 y축 범위를 -1.8부터 1.8까지 설정
ax = plt.axes([0., 0., 1., 1.], 
              xlim=(-1.8, 1.8), 
              ylim=(-1.8, 1.8))

# 축의 비율을 동일하게 설정 (원이 찌그러지지 않도록)
ax.set_aspect('equal')

# x축과 y축 레이블 설정 (어두운 테마에서 자동으로 밝은 색으로 표시됨)
ax.set_xlabel('x')
ax.set_ylabel('y')

# 격자선 제거 (우주 공간의 현실적인 표현을 위해)
ax.grid(False)

# 축과 축 레이블 완전히 제거 (순수한 우주 공간 효과)
ax.axis('off')

# 태양을 원점(0, 0)에 그리기
plot = ax.scatter(0, 0,                    # 위치: 좌표계의 중심점 (0, 0)
                  color = "red",      # 색상: 빨간색 (태양의 특성을 상징)
                  s = 28**2,          # 크기: 28의 제곱 (점의 크기는 제곱 단위로 지정)
                  edgecolors = None,  # 테두리 색상: 없음 (깔끔한 표현)
                  zorder = 10)        # 그리기 순서: 10 (다른 객체들보다 앞에 표시)

# %% code 57.
# astropy 라이브러리에서 Time 클래스를 가져옴 (천문학적 시간 처리용)
from astropy.time import Time
# 특정 시간을 설정 (2017년 1월 1일)
specific_time = Time("2017-01-01")

# NASA JPL Horizons 데이터베이스에서 천체 데이터를 가져오기 위한 라이브러리 import
from astroquery.jplhorizons import Horizons
# 수성(id=1)의 위치와 속도 벡터 데이터 요청
obj1 = Horizons(id = 1,                    # 천체 ID (1 = 수성)
                location="@sun",                # 관측 위치 (태양 중심)
                epochs=specific_time.jd,        # 시간 (줄리안 데이 형식)
                id_type='majorbody').vectors()  # 주요 천체 타입으로 벡터 데이터 요청

# 결과 데이터의 타입 확인
print("type(obj1): ", type(obj1))
# 수성의 전체 위치와 속도 벡터 데이터 출력
print("obj1: ", obj1)

# 위치 벡터의 각 성분 출력 (천문단위 AU)
print("obj1['x']: ", obj1['x'])  # x축 방향 위치 성분
print("obj1['y']: ", obj1['y'])  # y축 방향 위치 성분
print("obj1['z']: ", obj1['z'])  # z축 방향 위치 성분

# 속도 벡터의 각 성분 출력 (AU/day)
print("obj1['vx']: ", obj1['vx'])  # x축 방향 속도 성분
print("obj1['vy']: ", obj1['vy'])  # y축 방향 속도 성분
print("obj1['vz']: ", obj1['vz'])  # z축 방향 속도 성분

# %% code 58.
# astropy 라이브러리에서 Time 클래스를 가져옴 (천문학적 시간 처리용)
from astropy.time import Time
# 특정 시간을 설정 (2017년 1월 1일)
specific_time = Time("2017-01-01")

# matplotlib 라이브러리 가져오기 (그래프 그리기용)
import matplotlib.pyplot as plt
# 어두운 배경 테마 적용 (우주 공간 느낌 연출)
plt.style.use('dark_background')
# 축 설정: 전체 영역 사용, x축과 y축 범위를 -1.8부터 1.8까지 설정
ax = plt.axes([0., 0., 1., 1.],
              xlim=(-1.8, 1.8), 
              ylim=(-1.8, 1.8))

# 축의 비율을 동일하게 설정 (원이 찌그러지지 않도록)
ax.set_aspect('equal')
# 격자선 제거 (우주 공간의 현실적인 표현을 위해)
ax.grid(False)
# 축과 축 레이블 완전히 제거 (순수한 우주 공간 효과)
ax.axis('off')

# 태양을 원점(0, 0)에 그리기
plot = ax.scatter(0, 0,                    # 위치: 좌표계의 중심점 (0, 0)
                  color="red",      # 색상: 빨간색 (태양의 특성을 상징)
                  s=28**2,          # 크기: 28의 제곱 (점의 크기는 제곱 단위로 지정)
                  edgecolors=None,  # 테두리 색상: 없음 (깔끔한 표현)
                  zorder=10)        # 그리기 순서: 10 (다른 객체들보다 앞에 표시)

# 현재 날짜를 화면 왼쪽 상단에 표시
ax.text(.03, .94,                          # 위치: x=0.03, y=0.94 (축 좌표 기준)
        'Date: {}'.format(specific_time),  # 표시할 텍스트: 날짜 정보
        color='w',                         # 글자 색상: 흰색
        transform=ax.transAxes,            # 좌표 변환: 축 좌표계 사용
        fontsize='x-large')                # 글자 크기: 매우 큰 크기

# 수성, 금성, 지구, 화성 추가하기
from astroquery.jplhorizons import Horizons    # NASA JPL Horizons 데이터베이스 접근용
sizes = [0.38, 0.95, 1., 0.53]                 # 행성들의 상대적 크기 (지구=1.0 기준)
names = ['Mercury', 'Venus', 'Earth', 'Mars']  # 행성 이름 목록
for i in range(4):                             # 4개 행성에 대해 반복
 # NASA JPL Horizons에서 행성 데이터 가져오기
    obj = Horizons(id = i+1,               # 천체 ID (1=수성, 2=금성, 3=지구, 4=화성)
                   location = "@sun",                # 관측 위치 (태양 중심)
                   epochs = specific_time.jd,        # 시간 (줄리안 데이 형식)
                   id_type = 'majorbody').vectors()  # 주요 천체 타입으로 벡터 데이터 요청

 # 행성을 x, y 좌표에 점으로 그리기
    plot = ax.scatter(obj["x"], obj["y"],  # 위치: 행성의 x, y 좌표
                      s = (10 * sizes[i])**2,  # 크기: 상대적 크기에 비례하여 설정
                      edgecolors = None,       # 테두리 색상: 없음
                      zorder = 10)             # 그리기 순서: 10 (앞에 표시)
    
 # 행성 이름을 행성 위쪽에 표시
    ax.text(obj["x"], obj["y"]+0.1,        # 위치: 행성 좌표에서 y축으로 0.1만큼 위
            names[i],          # 표시할 텍스트: 행성 이름
            zorder=1000,       # 그리기 순서: 1000 (가장 앞에 표시)
            ha='center',       # 수평 정렬: 중앙 정렬
            fontsize='large')  # 글자 크기: 큰 크기

# %% code 59.
# astropy 라이브러리에서 Time 클래스를 가져와서 특정 시간 객체 생성
from astropy.time import Time
specific_time = Time("2017-01-01")  # 2017년 1월 1일로 시간 설정

# matplotlib을 이용한 그래프 생성 및 설정
import matplotlib.pyplot as plt
plt.style.use('dark_background')  # 어두운 배경 테마 적용 (우주 공간 효과)

# 그래프 축 설정: 전체 화면 사용, x와 y 축 범위를 -1.8에서 1.8로 설정
ax = plt.axes([0., 0., 1., 1.], xlim=(-1.8, 1.8), ylim=(-1.8, 1.8))
ax.set_aspect('equal')  # 축 비율을 1:1로 설정 (원이 찌그러지지 않도록)
ax.grid(False)          # 격자선 제거
ax.axis('off')          # 축과 축 레이블 완전히 제거

# 태양을 좌표 원점(0, 0)에 빨간색 점으로 표시
sun = ax.scatter(0, 0, color="red", s=28**2, edgecolors=None, zorder=10)

# 화면 왼쪽 상단에 현재 날짜 표시
ax.text(.03, .94, 'Date: {}'.format(specific_time), color='w', 
        transform=ax.transAxes, fontsize='x-large')

# NASA JPL Horizons 데이터베이스에서 지구 데이터 가져오기
from astroquery.jplhorizons import Horizons
# 지구(id=3)의 2017년 1월 1일 위치와 속도 벡터 정보 요청
obj = Horizons(id=3,                    # 천체 ID: 3은 지구
               location="@sun",          # 관측 위치: 태양 중심
               epochs=specific_time.jd,  # 시간: 줄리안 데이 형식
               id_type='id').vectors()   # 벡터 데이터 요청

# 지구를 그래프에 점으로 표시 (x, y 좌표 사용)
plot = ax.scatter(obj["x"], obj["y"], s=10**2, edgecolors=None, zorder=10)

# 지구 위치 위쪽에 "Earth" 라벨 표시
ax.text(obj["x"], obj["y"]+0.1, "Earth", zorder=1000, ha='center', fontsize='large')

# 시간 객체 재정의 (중복이지만 명확성을 위해)
from astropy.time import Time
specific_time = Time("2017-01-01")

# 지구의 위치 벡터 정보 다시 가져오기
from astroquery.jplhorizons import Horizons
obj = Horizons(id=3, location="@sun", epochs=specific_time.jd, id_type='id').vectors()

# 지구의 x, y, z 좌표 출력 (3차원 위치 벡터 확인)
print([obj[xi] for xi in ['x', 'y', 'z']])

# numpy를 이용하여 위치 벡터를 배열로 변환
import numpy as np
# 지구의 3차원 위치 벡터를 float64 형태의 numpy 배열로 생성
r = np.array([np.double(obj[xi]) for xi in ['x', 'y', 'z']], dtype=np.float64)
r  # 위치 벡터 r 출력

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

#print(len(dts))
#print(dts)

# 지구 위치 계산하기
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
    acc = -2.959e-4 * r / np.sum(r**2)**(3./2)  # 단위: AU/day²
    v = v + acc * dt
    rs.append(r)
    vs.append(v)
    accs.append(acc)
    xs.append(r[0])
    ys.append(r[1])
 #print("i: {}, r: {}, v: {}, acc: {}".format(i, r, v, acc))
    i += 1
# print("i: {}, r: {}, v: {}, acc: {}".format(i, r, v, acc))

print("len(xs): {}".format(len(xs)))
# print("xs: {}".format(xs))
print("len(ys): {}".format(len(ys)))
# print("ys: {}".format(ys))
print("len(rs): {}".format(len(rs)))
# print("rs: {}".format(rs))

print("len(vs): {}".format(len(vs)))
# print("vs: {}".format(vs))

print("len(accs): {}".format(len(accs)))
# print("accs: {}".format(accs))

print("rs[5][:2]: {}".format(rs[5][:2]))
print("rs[4]: {}".format(rs[4]))
print("rs[5]: {}".format(rs[5]))
#print("[item[:2] for item in rs[2]]: {}".format([item[:2] for item in rs[2]]))

# %% code 61.
import numpy as np
from astropy.time import Time, TimeDelta

# 시뮬레이션 시작 시간과 종료 시간 설정
start_time_text = "2017-01-01"  # 시뮬레이션 시작일 (2017년 1월 1일)
end_time_text = "2020-01-01"    # 시뮬레이션 종료일 (2020년 1월 1일)

dt = 1  # 시간 간격 (1일)

def astropyTime_range(start, end, delta):
    """
    주어진 시작 시간부터 종료 시간까지 일정한 간격으로 시간을 생성하는 제너레이터 함수
    
    Parameters:
    start: 시작 시간 (astropy Time 객체)
    end: 종료 시간 (astropy Time 객체)  
    delta: 시간 간격 (TimeDelta 객체)
    """
    current = start       # 현재 시간을 시작 시간으로 초기화
    while current < end:  # 현재 시간이 종료 시간보다 작을 때까지 반복
        yield current     # 현재 시간을 반환
        current += delta  # 시간 간격만큼 증가

# 시작 시간부터 종료 시간까지 1일 간격으로 시간 목록 생성
dts = [dt.iso for dt in 
       astropyTime_range(Time(start_time_text), Time(end_time_text), 
       TimeDelta(dt, format='jd'))]

#print(len(dts)) # 생성된 시간 목록의 길이 출력 (주석 처리됨)
#print(dts) # 생성된 시간 목록 출력 (주석 처리됨)

plt.style.use('dark_background')
fig = plt.figure(figsize=[6, 6])
ax = plt.axes([0., 0., 1., 1.], xlim=(-1.8, 1.8), ylim=(-1.8, 1.8))
ax.set_aspect('equal')
ax.axis('off')
sun = ax.scatter(0, 0, color="red", s=28**2,
                 edgecolors=None, zorder=10)

# NASA JPL Horizons 데이터베이스에서 지구 위치 데이터 가져오기
from astroquery.jplhorizons import Horizons
obj = Horizons(id=3,                         # 천체 ID (3 = 지구)
               location="@sun",                  # 관측 위치 (태양 중심)
               epochs=Time(start_time_text).jd,  # 시간 (줄리안 데이 형식)
               id_type='id').vectors()           # 벡터 데이터 요청

ax.text(obj["x"], obj["y"]+0.1,
        "Earth", zorder=1000, ha='center', fontsize='large')
plot = ax.scatter(obj["x"], obj["y"],
                  s=10**2, edgecolors=None, zorder=10)
line, = ax.plot([], [], linewidth=1.4)
timestamp = ax.text(.03, .94, 'Date: ', color='w', transform=ax.transAxes, fontsize='x-large')


# 지구의 초기 위치 벡터를 numpy 배열로 변환 (x, y, z 좌표)
r = np.array([np.double(obj[xi]) for xi in ['x', 'y', 'z']], dtype=np.float64)
# 지구의 초기 속도 벡터를 numpy 배열로 변환 (vx, vy, vz 성분)
v = np.array([np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']], dtype=np.float64)
print("r: {}, v: {}".format(r, v))  # 초기 위치와 속도 벡터 출력

# 시뮬레이션 결과를 저장할 리스트들 초기화
xs, ys = [], []            # x, y 좌표를 별도로 저장하는 리스트
rs, vs, accs = [], [], []  # 위치 벡터, 속도 벡터, 가속도 벡터를 저장하는 리스트

i = 0  # 반복 횟수 카운터 초기화

# 오일러 방법을 사용한 궤도 시뮬레이션 루프
while i < (len(dts)):    
 # 위치 업데이트: 새로운 위치 = 이전 위치 + 속도 × 시간간격
    r = r + v * dt
    
 # 태양의 중력에 의한 가속도 계산 (뉴턴의 만유인력 법칙)
 # acc = -GM/r² × (r/|r|) 형태로, 태양을 향하는 방향의 가속도
    acc = -2.959e-4 * r / np.sum(r**2)**(3./2)  # 단위: AU/day²
    
 # 속도 업데이트: 새로운 속도 = 이전 속도 + 가속도 × 시간간격
    v = v + acc * dt
    
 # 계산 결과를 리스트에 저장
    rs.append(r)      # 위치 벡터 저장
    vs.append(v)      # 속도 벡터 저장  
    accs.append(acc)  # 가속도 벡터 저장
    xs.append(r[0])   # x 좌표만 별도 저장
    ys.append(r[1])   # y 좌표만 별도 저장
    
 #print("i: {}, r: {}, v: {}, acc: {}".format(i, r, v, acc)) # 각 단계별 결과 출력 (주석 처리됨)
    i += 1  # 반복 횟수 증가

# 최종 결과 출력
# print("i: {}, r: {}, v: {}, acc: {}".format(i, r, v, acc))

# 계산된 데이터의 크기 및 내용 확인
print("len(xs): {}".format(len(xs)))  # x 좌표 리스트 길이
print("xs: {}".format(xs))            # x 좌표 전체 데이터
print("len(ys): {}".format(len(ys)))  # y 좌표 리스트 길이  
print("ys: {}".format(ys))            # y 좌표 전체 데이터

print("len(rs): {}".format(len(rs)))  # 위치 벡터 리스트 길이
print("rs: {}".format(rs))            # 위치 벡터 전체 데이터

print("len(vs): {}".format(len(vs)))  # 속도 벡터 리스트 길이
print("vs: {}".format(vs))            # 속도 벡터 전체 데이터

print("len(accs): {}".format(len(accs)))  # 가속도 벡터 리스트 길이
print("accs: {}".format(accs))            # 가속도 벡터 전체 데이터

# 특정 시점의 데이터 확인 (검증용)
print("rs[5][:2]: {}".format(rs[5][:2]))  # 6번째 위치 벡터의 x, y 성분
print("rs[4]: {}".format(rs[4]))          # 5번째 위치 벡터 전체
print("rs[5]: {}".format(rs[5]))          # 6번째 위치 벡터 전체
#print("[item[:2] for item in rs[2]]: {}".format([item[:2] for item in rs[2]])) # 주석 처리됨

# %% code 62.
def animate(i):
    plot.set_offsets(rs[i][:2])
    line.set_xdata(xs[:i])
    line.set_ydata(ys[:i])
    timestamp.set_text('Date: ' + Time(dts[i]).iso)
    return plot, line, timestamp

from matplotlib.animation import FuncAnimation
ani = FuncAnimation(fig, animate, 
                     frames=len(dts), 
                     blit=True)

# %% code 63.
import matplotlib
import matplotlib.pyplot as plt

# 애니메이션 용량 한도를 50MB 로 올리기(기본값 약 20MB)
matplotlib.rcParams['animation.embed_limit'] = 50  # 단위: MB

# 선택: 성능을 위해 다른 애니메이션 설정도 조정
matplotlib.rcParams['animation.html'] = 'jshtml'    # 자바스크립트 HTML 사용
matplotlib.rcParams['animation.writer'] = 'ffmpeg'  # ffmpeg 이 있으면 사용

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

# 시뮬레이션 매개변수 설정
sim_start_date = "2018-01-01"     # 태양계 시뮬레이션 시작 날짜
sim_duration = 2 * 365            # 시뮬레이션 기간 (일 단위, 2년)
m_earth = 5.9722e24 / 1.98847e30  # 태양 질량 대비 지구 질량 비율
m_moon = 7.3477e22 / 1.98847e30   # 태양 질량 대비 달 질량 비율

class Object:                     # 태양계 천체 객체 클래스 정의 (태양, 지구, 수성 등)
    def __init__(self, name, rad, color, r, v):
        self.name = name                           # 천체 이름
        self.r    = np.array(r, dtype=np.float64)  # 위치 벡터 (x, y, z 좌표)
        self.v    = np.array(v, dtype=np.float64)  # 속도 벡터 (vx, vy, vz 성분)
        self.xs = []                               # x 좌표 이력 저장 리스트
        self.ys = []                               # y 좌표 이력 저장 리스트
 # matplotlib 산점도 객체 생성 (천체의 현재 위치 표시)
        self.plot = ax.scatter(r[0], r[1], color=color, s=rad**2, edgecolors=None, zorder=10)
 # matplotlib 선 객체 생성 (천체의 궤도 경로 표시)
        self.line, = ax.plot([], [], color=color, linewidth=1.4)

class SolarSystem:                # 태양계 전체를 관리하는 클래스
    def __init__(self, thesun):
        self.thesun = thesun  # 중심별(태양) 객체
        self.planets = []     # 행성들을 저장하는 리스트
        self.time = None      # 현재 시뮬레이션 시간
 # 화면에 날짜 표시를 위한 텍스트 객체 생성
        self.timestamp = ax.text(.03, .94, 'Date: ', color='w', transform=ax.transAxes, fontsize='x-large')
    
    def add_planet(self, planet): # 태양계에 행성 추가 메서드
        self.planets.append(planet)
    
    def evolve(self):             # 시간에 따른 궤도 진화 계산 메서드
        dt = 1.0         # 시간 간격 (1일)
        self.time += dt  # 시뮬레이션 시간 증가
        plots = []       # 갱신할 산점도 객체들을 저장할 리스트
        lines = []       # 갱신할 선 객체들을 저장할 리스트
        
        for p in self.planets:    # 모든 행성에 대해 반복
 # 위치 업데이트: 새로운 위치 = 이전 위치 + 속도 × 시간간격
            p.r += p.v * dt
 # 태양의 중력에 의한 가속도 계산 (뉴턴의 만유인력 법칙)
 # acc = -GM/r² × (r/|r|), 단위: AU/day²
            acc = -2.959e-4 * p.r / np.sum(p.r**2)**(3./2)
 # 속도 업데이트: 새로운 속도 = 이전 속도 + 가속도 × 시간간격
            p.v += acc * dt
 # 좌표 이력에 현재 위치 추가
            p.xs.append(p.r[0])
            p.ys.append(p.r[1])
 # 화면상의 천체 위치 업데이트
            p.plot.set_offsets(p.r[:2])
 # 궤도 경로 선 업데이트
            p.line.set_xdata(p.xs)
            p.line.set_ydata(p.ys)
 # 갱신할 객체들을 리스트에 추가
            plots.append(p.plot)
            lines.append(p.line)
        
 # 화면에 표시되는 날짜 업데이트
        self.timestamp.set_text('Date: ' + Time(self.time, format='jd').iso)
 # 애니메이션을 위해 갱신된 모든 객체들 반환
        return plots + lines + [self.timestamp]

# matplotlib 그래프 설정
fig = plt.figure(facecolor='black')  # 검은색 배경의 그림 생성
plt.style.use('dark_background')     # 어두운 테마 적용

# 축 설정: 전체 화면 사용, x축과 y축 범위를 -1.8에서 1.8로 설정
ax = plt.axes([0., 0., 1., 1.], xlim=(-1.8, 1.8), ylim=(-1.8, 1.8))
ax.set_aspect('equal')  # 축 비율을 1:1로 설정 (원이 찌그러지지 않도록)
ax.axis('off')          # 축과 축 레이블을 숨김 (우주 공간 느낌 연출)

# 태양계 시스템 초기화 (태양을 원점에 생성)
ss = SolarSystem(Object("Sun", 28, 'red', [0, 0, 0], [0, 0, 0]))
ss.time = Time(sim_start_date).jd  # 시뮬레이션 시작 시간을 줄리안 데이로 설정

# 행성들의 시각적 속성 정의
colors = ['gray', 'orange', 'blue', 'chocolate']  # 각 행성의 색상
sizes = [0.38, 0.95, 1., 0.53]                    # 각 행성의 상대적 크기
names = ['Mercury', 'Venus', 'Earth', 'Mars']     # 행성 이름들
texty = [.47, .73, 1, 1.5]                        # 행성 이름 표시 위치 (y좌표)

# 4개 행성 (수성, 금성, 지구, 화성) 추가
for i, nasaid in enumerate([1, 2, 3, 4]):  # NASA JPL ID: 1=수성, 2=금성, 3=지구, 4=화성
 # NASA JPL Horizons 데이터베이스에서 해당 행성의 위치와 속도 데이터 가져오기
    obj = Horizons(id=nasaid, location="@sun", epochs=ss.time, id_type='id').vectors()
    
 # 행성 객체 생성 및 태양계에 추가
    ss.add_planet(Object(nasaid,                    # 행성 ID
                         20 * sizes[i],  # 크기 (기본값에 상대적 크기 곱함)
                         colors[i],      # 색상
 # 위치 벡터 (x, y, z 좌표)
                         [np.double(obj[xi]) for xi in ['x', 'y', 'z']], 
 # 속도 벡터 (vx, vy, vz 성분)
                         [np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']]))
    
 # 각 행성의 이름을 화면 하단에 표시
    ax.text(0, - (texty[i] + 0.1), names[i], color=colors[i], 
            zorder=1000, ha='center', fontsize='large')

# 그래프 화면에 표시
plt.show()

# %% code 66.
# 애니메이션 함수 정의 - 각 프레임마다 호출되어 태양계 상태를 한 단계씩 진화시킴
def animate(i):
    return ss.evolve()  # 태양계 시스템의 evolve() 메서드를 호출하여 행성들의 위치와 속도 업데이트
    
# matplotlib의 애니메이션 모듈 import
import matplotlib.animation as animation

# FuncAnimation 객체 생성 - 태양계 시뮬레이션 애니메이션 설정
ani = animation.FuncAnimation(fig,                # 그래프 figure 객체
                              animate,              # 각 프레임마다 호출할 함수
                              repeat=False,         # 애니메이션 반복 재생 안함
                              frames=sim_duration,  # 총 프레임 수 (시뮬레이션 기간과 동일)
                              blit=True,            # 블리팅 사용 (성능 향상을 위해)
                              interval=20)          # 프레임 간 간격 (밀리초 단위)

# %% code 67.
import matplotlib
import matplotlib.pyplot as plt

# 애니메이션 용량 한도를 50MB 로 올리기(기본값 약 20MB)
matplotlib.rcParams['animation.embed_limit'] = 50  # 단위: MB

# 선택: 성능을 위해 다른 애니메이션 설정도 조정
matplotlib.rcParams['animation.html'] = 'jshtml'    # 자바스크립트 HTML 사용
matplotlib.rcParams['animation.writer'] = 'ffmpeg'  # ffmpeg 이 있으면 사용

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
# 파일명 설정
fname = 'Solar_System_2D_Animation_Class_Based'

try:
 # MP4 형식으로 저장
    ani.save(f'{proj_dir}/{fname}.mp4', 
             fps=60, dpi=150, writer='ffmpeg')
    print(f"동영상이 저장되었습니다: {proj_dir}/{fname}.mp4")
except Exception as e:
    print(f"MP4 저장 중 오류 발생: {e}")
    
 # 대안: GIF 형식으로 저장
    try:
        ani.save(f'{proj_dir}/{fname}.gif', 
                 fps=30, dpi=100, writer='pillow')
        print(f"GIF 파일이 저장되었습니다: {proj_dir}/{fname}.gif")
    except Exception as e2:
        print(f"GIF 저장 중 오류 발생: {e2}")
        
 # 최종 대안: HTML 파일로 저장
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

# 시뮬레이션 기본 설정
sim_start_date = "2018-01-01"
sim_duration = 2 * 365
m_earth = 5.9722e24 / 1.98847e30
m_moon = 7.3477e22 / 1.98847e30

# matplotlib 기본 설정
plt.style.use('dark_background')
fig = plt.figure(figsize=(12, 10), facecolor='black')

# 3D 축 설정
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.grid(False)

# 3D 축 범위 설정
ax.set_xlim3d([-1.8, 1.8])
ax.set_ylim3d([-1.8, 1.8])
ax.set_zlim3d([-1.0, 1.0])

# 축 레이블 및 제목 설정
ax.set_xlabel('X (AU)', color='white')
ax.set_ylabel('Y (AU)', color='white')
ax.set_zlabel('Z (AU)', color='white')
ax.set_title('The Solar System (3D)', color='white', fontsize=16)

# 시뮬레이션 시작 시간 객체 생성
specific_time = Time(sim_start_date)

class Object:
    def __init__(self, name, rad, color, r, v):
        self.name = name
        self.r = np.array(r, dtype=np.float64)
        self.v = np.array(v, dtype=np.float64)
        self.xs = []
        self.ys = []
        self.zs = []
 # 3D 산점도 객체 생성
        self.plot = ax.scatter(r[0], r[1], r[2], color=color, s=rad**2, 
                               edgecolors=None, zorder=10)
 # 3D 선 객체 생성
        self.line, = ax.plot([], [], [], color=color, linewidth=1.4)

class SolarSystem:
    def __init__(self, thesun):
        self.thesun = thesun
        self.planets = []
        self.time = None
 # 화면에 날짜 표시
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
 # 위치 업데이트
            p.r += p.v * dt
 # 태양의 중력에 의한 가속도 계산
            acc = -2.959e-4 * p.r / np.sum(p.r**2)**(3./2)
 # 속도 업데이트
            p.v += acc * dt
 # 좌표 이력 추가
            p.xs.append(p.r[0])
            p.ys.append(p.r[1])
            p.zs.append(p.r[2])
 # 3D 위치 업데이트
            p.plot._offsets3d = ([p.r[0]], [p.r[1]], [p.r[2]])
 # 궤도 경로 업데이트
            p.line.set_data_3d(p.xs, p.ys, p.zs)
            plots.append(p.plot)
            lines.append(p.line)
        
 # 날짜 정보 업데이트
        self.timestamp.set_text('Date: ' + Time(self.time, format='jd').iso)
        return plots + lines + [self.timestamp]

# 태양 추가
sun = ax.scatter(0, 0, 0, color="red", s=28**2, edgecolors=None, zorder=10)

# 시작 시간 표시
ax.text2D(.03, .94, 'Date: {}'.format(specific_time.iso), color='white', 
          transform=ax.transAxes, fontsize='x-large')

# 태양계 시스템 초기화
ss = SolarSystem(Object("Sun", 28, 'red', [0, 0, 0], [0, 0, 0]))
ss.time = Time(sim_start_date).jd

# 행성들의 시각적 속성
colors = ['gray', 'orange', 'blue', 'chocolate']
sizes = [0.38, 0.95, 1., 0.53]
names = ['Mercury', 'Venus', 'Earth', 'Mars']
texty = [.47, .73, 1, 1.5]

# 행성 추가
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
        
 # 행성 이름 표시
        ax.text(0, -(texty[i] + 0.1), 0, names[i], color=colors[i], 
                zorder=1000, ha='center', fontsize='large')
        
        print(f"{names[i]} 추가 완료")
    except Exception as e:
        print(f"{names[i]} 데이터 가져오기 실패: {e}")

print("태양계 시뮬레이션 초기화 완료!")
plt.tight_layout()
plt.show()

# %% code 71.
# 애니메이션 함수 정의 - 각 프레임마다 호출되어 태양계 상태를 진화시킴
def animate(i):
    return ss.evolve()  # 태양계 시스템의 evolve() 메서드 호출하여 행성들 위치 업데이트
    
# matplotlib 애니메이션 모듈에서 FuncAnimation 클래스 import
from matplotlib.animation import FuncAnimation

# FuncAnimation 객체 생성 - 3D 태양계 애니메이션 설정
ani = FuncAnimation(fig, animate,           # figure 객체와 애니메이션 함수 지정
                    frames=len(dts),  # 총 프레임 수 (시간 데이터 목록의 길이)
                    blit=True)        # 블리팅 활성화 (렌더링 성능 향상)
                    

# %% code 72.
import matplotlib
import matplotlib.pyplot as plt

# 애니메이션 용량 한도를 50MB 로 올리기(기본값 약 20MB)
matplotlib.rcParams['animation.embed_limit'] = 100  # 단위: MB

# 선택: 성능을 위해 다른 애니메이션 설정도 조정
matplotlib.rcParams['animation.html'] = 'jshtml'    # 자바스크립트 HTML 사용
matplotlib.rcParams['animation.writer'] = 'ffmpeg'  # ffmpeg 이 있으면 사용

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
# 저장할 파일명 설정
fname = 'Solar_System_3D_Animation_Class_Based'  # 3D 태양계 애니메이션 파일명

ani.save(f'{proj_dir}/{fname}.mp4',  # 저장 경로와 파일명
            fps=60,           # 초당 프레임 수 (60fps)
            dpi=150,          # 해상도 (인치당 도트 수)
            writer='ffmpeg')  # 동영상 인코더 (ffmpeg 사용)
print(f"동영상이 저장되었습니다: {proj_dir}/{fname}.mp4")

# %% code 75.
ani.save(f'{proj_dir}/{fname}.gif',  # GIF 파일로 저장
            fps=30,           # 초당 프레임 수 (30fps, MP4보다 낮음)
            dpi=100,          # 해상도 (MP4보다 낮음)
            writer='pillow')  # GIF 작성기 (Pillow 라이브러리 사용)
print(f"GIF 파일이 저장되었습니다: {proj_dir}/{fname}.gif")
