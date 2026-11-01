# 지구과학 데이터 사이언스 1 | II-01. 물리량 계산하기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 1.
from pint import UnitRegistry
u = UnitRegistry()
print("type(u):", type(u))
distance = 24.0 * u.meter  # 수치 × 단위 = 물리량(Quantity)
print("type(distance)", type(distance))
print("distance", distance)
print("dir(distance):", dir(distance))

# %% code 2.
print("distance.magnitude:", distance.magnitude)
print("distance.units:", distance.units)
print("distance.dimensionality:", distance.dimensionality)
print(f'distance**2:P: {distance**2:P}')     # 읽기 쉬운 형식
print(f'distance**2:~P: {distance**2:~P}')   # 단위 약어
print(f'distance**2:~L: {distance**2:~L}')   # LaTeX 형식
print(f'distance**2:~H : {distance**2:~H}')  # HTML 형식

# %% code 3.
h = 6.626e-34 * u.J * u.s      # 플랑크 상수
c = 3.0e+8 * u.m / u.s         # 광속
k = 1.38e-23 * u.J / u.K       # 볼츠만 상수
wavelengths = 0.0000005 * u.m  # 파장(500 nm)
T = 6000. * u.K
print("h: {}".format(h))
print("c: {}".format(c))
print("k: {}".format(k))
print("wavelengths: {}".format(wavelengths))
print("T: {}".format(T))
distance = 8 * u.m
time = 4 * u.s
average_velocity = distance / time
print(f'average_velocity.to(u.cm/u.s): {average_velocity.to(u.cm/u.s)}')
print(f'average_velocity.to(u.km/u.s): {average_velocity.to(u.km/u.s)}')

# %% code 4.
length1 = 15 * u.meter
length2 = 300 * u.centimeter
time1 = 10 * u.second
print("length1 + length2 =", length1 + length2)  # 15 m + 3 m = 18 m(단위 자동 변환)
print("length1 - length2 =", length1 - length2)  # 15 m - 3 m = 12 m
area = (length1 * length2).to('m**2')  # cm·m를 m²로 맞춤
print("area =", area)  # 15 m * 3 m = 45 m²
speed = length1 / time1
print("speed =", speed)  # 15 m / 10 s = 1.5 m/s
print("speed.to('km/h') =", speed.to('km/h'))
# 단위가 맞지 않는 덧셈(오류 발생)
try:
    print(length1 + time1)
except Exception as e:
    print("오류 (단위 불일치):", e)

# %% code 5.
import scipy.constants as const
constR1 = const.physical_constants["molar gas constant"]  # 기체 상수(값, 단위, 불확도)
print("type(constR1):", type(constR1))
print("constR1:", constR1)

# 태양 광도는 scipy.constants에 없으므로 직접 정의
solar_luminosity = (3.828e26, 'W', 0.0)  # (값, 단위, 불확도)
print("type(solar_luminosity):", type(solar_luminosity))
print("solar_luminosity:", solar_luminosity)

# scipy.constants에서 값을 바로 가져오기
print(f"천문단위(AU): {const.au} m")

# %% code 6.
import astropy.units as u
distance = 8 * u.m
print("type(distance):{}".format(type(distance)))
print("distance:{}".format(distance ))

time = 4 * u.s
average_velocity = distance / time
print("type(average_velocity):{}".format(type(average_velocity)))
print("average_velocity:{}".format(average_velocity))

# %% code 7.
print(f'distance.value:0.1f: {distance.value:.1f}, distance.unit: {distance.unit}')
print(f'distance.value:0.8f:{distance.value:0.8f}, distance.unit:fits: {distance.unit:fits}')
print(f'distance.value:0.8f:{distance.value:0.8f}, distance.unit:cds: {distance.unit:cds}')
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

# 자유낙하 시간
height = 100 * u.m
g = 9.8 * u.m / u.s**2             # 중력가속도
fall_time = (2 * height / g)**0.5  # t = √(2h/g)

print(f'낙하시간: {fall_time}')
print(f'낙하시간 (분): {fall_time.to(u.minute)}')
print(f'낙하시간 (밀리초): {fall_time.to(u.millisecond)}')

# %% code 9.
import astropy.constants as const
print("const.h:{}".format(const.h))
print("const.c:{}".format(const.c))
print("const.k_B:{}".format(const.k_B))
print("const.M_sun:{}".format(const.M_sun))      # 태양 질량
print("const.M_earth:{}".format(const.M_earth))  # 지구 질량
print("const.M_jup:{}".format(const.M_jup))      # 목성 질량
print("const.L_sun:{}".format(const.L_sun))      # 태양 광도
print("const.R_sun:{}".format(const.R_sun))      # 태양 반지름
print("const.R_earth:{}".format(const.R_earth))  # 지구 반지름
print("const.au:{}".format(const.au))            # 천문단위(지구–태양 평균 거리)
print("const.pc:{}".format(const.pc))            # 파섹

# %% code 10.
from metpy.units import units as u

length = 10 * u.meter
time = 2 * u.second
speed = length / time

print("length:", length)
print("time:", time)
print("speed:", speed)

speed_kmh = speed.to('km/hour')
print("speed (km/h):", speed_kmh)

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
# 수치(magnitude)와 단위(units) 분리
print("length.magnitude:", length.magnitude)
print("length.units:", length.units)
print("speed.magnitude:", speed.magnitude)
print("speed.units:", speed.units)

print("length(str):", str(length))
print("speed(str):", str(speed))

print("length (cm):", length.to('centimeter'))
print("speed (mile/hour):", speed.to('mile/hour'))

print(f"speed = {speed.magnitude:.2f} [{speed.units}]")
print(f"total_length = {total_length.magnitude} {total_length.units}")
print(f"area = {area.magnitude} {area.units}")

# %% code 12.
from metpy.constants import Rd, g, Cp_d, epsilon

print(f"건조공기 기체상수 Rd: {Rd}")
print(f"표준 중력가속도 g: {g}")
print(f"건조공기 비열 Cp_d: {Cp_d}")
print(f"수증기/건조공기 분자량비 epsilon: {epsilon}")

# 이상기체 상태방정식 p = ρRT에서 밀도 ρ 계산
from metpy.units import units as u

p = 1000 * u.hectopascal
T = 300 * u.kelvin
rho = p / (Rd * T)
print(f"밀도(ρ) = {rho.to('kg/m^3')}")
