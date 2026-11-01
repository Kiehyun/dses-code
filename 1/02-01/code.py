# 지구과학 데이터 사이언스 1 | II-01. 물리량 계산하기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 1.
from pint import UnitRegistry            # pint 라이브러리에서 UnitRegistry를 가져옴
u = UnitRegistry()                       # UnitRegistry의 인스턴스를 생성
print("type(u):", type(u))               # u의 자료형을 출력
distance = 24.0 * u.meter                # 24.0이라는 수치에 'meter' 단위를 곱하여 물리량(Quantity)을 생성
print("type(distance)", type(distance))  # distance의 자료형을 출력
print("distance", distance)              # distance의 값을 출력
print("dir(distance):", dir(distance))   # distance 객체의 속성과 메서드를 출력

# %% code 2.
print("distance.magnitude:", distance.magnitude)  # 수치 값(크기)을 출력
print("distance.units:", distance.units)          # 단위를 출력
print("distance.dimensionality:", distance.dimensionality)  # 차원을 출력
print(f'distance**2:P: {distance**2:P}')          # 제곱한 값을 읽기 쉬운 형식으로 출력
print(f'distance**2:~P: {distance**2:~P}')        # 제곱한 값을 단위를 간략화한 형식으로 출력
print(f'distance**2:~L: {distance**2:~L}')        # 제곱한 값을 LaTeX 형식으로 출력
print(f'distance**2:~H : {distance**2:~H}')       # 제곱한 값을 HTML 형식으로 출력

# %% code 3.
h = 6.626e-34 * u.J * u.s      # (플랑크 상수)
c = 3.0e+8 * u.m / u.s         # (광속)
k = 1.38e-23 * u.J / u.K       # (볼츠만 상수)
wavelengths = 0.0000005 * u.m  # (파장)
T = 6000. * u.K                # (온도)
print("h: {}".format(h))
print("c: {}".format(c))
print("k: {}".format(k))
print("wavelengths: {}".format(wavelengths))
print("T: {}".format(T))
distance = 8 * u.m
time = 4 * u.s
average_velocity = distance / time
# cm/s로 변환하여 출력
print(f'average_velocity.to(u.cm/u.s): {average_velocity.to(u.cm/u.s)}')
# km/s로 변환하여 출력
print(f'average_velocity.to(u.km/u.s): {average_velocity.to(u.km/u.s)}')

# %% code 4.
length1 = 15 * u.meter
length2 = 300 * u.centimeter
time1 = 10 * u.second
print("length1 + length2 =", length1 + length2)  # 15 m + 3 m = 18 m  # 덧셈 (자동 단위 변환)
print("length1 - length2 =", length1 - length2)  # 15 m - 3 m = 12 m  # 뺄셈
area = length1 * length2                         # 곱셈
print("area =", area)                            # 15 m * 3 m = 45 m²
speed = length1 / time1                          # 나눗셈
print("speed =", speed)                          # 15 m / 10 s = 1.5 m/s
# 단위 변환
print("speed.to('km/h') =", speed.to('km/h'))  # m/s → km/h
# 단위가 맞지 않는 덧셈 (오류 발생)
try:
    print(length1 + time1)
except Exception as e:
    print("오류 (단위 불일치):", e)

# %% code 5.
import scipy.constants as const
# print("dir(const):", dir(const)) # scipy.constants의 속성과 메서드를 출력
# print("const.physical_constants:", const.physical_constants) # 물리 상수의 정보를 출력
constR1 = const.physical_constants["molar gas constant"]    # 기체 상수를 가져옴    
print("type(constR1):", type(constR1))
print("constR1:", constR1)

# 태양의 광도 추가 (scipy.constants에는 없으므로 직접 정의)
# 태양 광도: 3.828 × 10^26 W
solar_luminosity = (3.828e26, 'W', 0.0)    # (값, 단위, 불확실성) 형태로 정의
print("type(solar_luminosity):", type(solar_luminosity))
print("solar_luminosity:", solar_luminosity)

# 또는 scipy.constants에서 직접 값 가져오기
print(f"천문단위(AU): {const.au} m")       # 천문단위 (m)

# %% code 6.
import astropy.units as u
distance = 8 * u.m  # 8미터를 정의합니다.
print("type(distance):{}".format(type(distance)))
print("distance:{}".format(distance ))
# print("dir(distance):", dir(distance)) 

time = 4 * u.s
average_velocity = distance / time
print("type(average_velocity):{}".format(type(average_velocity)))
print("average_velocity:{}".format(average_velocity))

# %% code 7.
# 수치와 단위를 분리하여 출력
print(f'distance.value:0.1f: {distance.value:.1f}, distance.unit: {distance.unit}')
# 수치와 단위를 LaTeX 형식으로 출력
print(f'distance.value:0.8f:{distance.value:0.8f}, distance.unit:fits: {distance.unit:fits}')
# 수치와 단위를 HTML 형식으로 출력
print(f'distance.value:0.8f:{distance.value:0.8f}, distance.unit:cds: {distance.unit:cds}')
# 수치와 단위를 Latex 형식으로 출력
print(f'distance.value:0.2f:{distance.value:0.2f}, distance.unit:latex: {distance.unit:latex}')

# %% code 8.
h = 6.626e-34 * u.J * u.s                  # 플랑크 상수
c = 3.0e+8  * u.m / u.s                    # 광속
k = 1.38e-23 * u.J / u.K                   # 볼츠만 상수
sigma = 5.67e-8 * u.W / (u.m**2 * u.K**4)  # 스테판-볼츠만 상수
G = 6.67e-11 * u.m**3 / (u.kg * u.s**2)    # 중력 상수

print("h (플랑크 상수): {}".format(h))
print("c (광속): {}".format(c))
print("k (볼츠만 상수): {}".format(k))
print("σ (스테판-볼츠만 상수): {}".format(sigma))
print("G (중력 상수): {}".format(G))

# 자유낙하 운동 예제
height = 100 * u.m                 # 높이
g = 9.8 * u.m / u.s**2             # 중력가속도
fall_time = (2 * height / g)**0.5  # 낙하시간 계산

print(f'낙하시간: {fall_time}')
# 분 단위로 변환하여 출력
print(f'낙하시간 (분): {fall_time.to(u.minute)}')
# 밀리초 단위로 변환하여 출력 
print(f'낙하시간 (밀리초): {fall_time.to(u.millisecond)}')

# %% code 9.
import astropy.constants as const
print("const.h:{}".format(const.h))      # 플랑크 상수
print("const.c:{}".format(const.c))      # 광속
print("const.k_B:{}".format(const.k_B))  # 볼츠만 상수
# 천체 질량
print("const.M_sun:{}".format(const.M_sun))      # 태양 질량
print("const.M_earth:{}".format(const.M_earth))  # 지구 질량
print("const.M_jup:{}".format(const.M_jup))      # 목성 질량
# 태양의 물리량
print("const.L_sun:{}".format(const.L_sun))  # 태양 광도
print("const.R_sun:{}".format(const.R_sun))  # 태양 반지름
# 지구의 물리량
print("const.R_earth:{}".format(const.R_earth)) # 지구 반지름
# 기타 천문 상수
print("const.au:{}".format(const.au))  # 천문단위 (지구-태양 평균 거리)
print("const.pc:{}".format(const.pc))  # 파섹

# %% code 10.
from metpy.units import units as u

# 길이, 시간, 속력 등 다양한 물리량 정의
length = 10 * u.meter
time = 2 * u.second
speed = length / time

print("length:", length)
print("time:", time)
print("speed:", speed)

# 단위 변환 예시
speed_kmh = speed.to('km/hour')
print("speed (km/h):", speed_kmh)

# 덧셈, 곱셈 등 연산 예시
length2 = 500 * u.centimeter
total_length = length + length2
print("total_length:", total_length)

area = length * length2
print("area:", area)

# 단위가 맞지 않는 연산(오류 발생)
try:
    print(length + time)
except Exception as e:
    print("오류 (단위 불일치):", e)

# %% code 11.
# 수치(magnitude)와 단위(units) 분리 출력
print("length.magnitude:", length.magnitude)
print("length.units:", length.units)
print("speed.magnitude:", speed.magnitude)
print("speed.units:", speed.units)

# 문자열 변환
print("length(str):", str(length))
print("speed(str):", str(speed))

# 단위 변환 후 출력
print("length (cm):", length.to('centimeter'))
print("speed (mile/hour):", speed.to('mile/hour'))

# f-string 활용
print(f"speed = {speed.magnitude:.2f} [{speed.units}]")
print(f"total_length = {total_length.magnitude} {total_length.units}")
print(f"area = {area.magnitude} {area.units}")

# %% code 12.
from metpy.constants import Rd, g, Cp_d, epsilon

print(f"건조공기 기체상수 Rd: {Rd}")
print(f"중력가속도 g: {g}")
print(f"건조공기 비열 Cp_d: {Cp_d}")
print(f"수증기/건조공기 분자량비 epsilon: {epsilon}")

# 예시: 이상기체 상태방정식 (p = ρ R T)에서 ρ 계산
from metpy.units import units as u

p = 1000 * u.hectopascal  # 기압
T = 300 * u.kelvin        # 온도
rho = p / (Rd * T)        # 밀도 계산
print(f"밀도(ρ) = {rho.to('kg/m^3')}")
