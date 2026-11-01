# 지구과학 데이터 사이언스 1 | II-02. 플랑크 곡선 그리기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 13.
# 플랑크 곡선(흑체 복사 스펙트럼) 계산 예제
h = 6.626e-34  # J s  (플랑크 상수)
c = 3.0e+8     # m s-1 (광속)
k = 1.38e-23   # J K-1 (볼츠만 상수)

import numpy as np

# 0.01 um(=10 nm) ~ 3 um 까지 0.01 um 간격의 파장 배열 생성 (단위: m)
wavelengths = np.arange(1e-8, 3e-6, 1e-8)   # m (파장)

T = 6000.           # K  (온도)

# 플랑크 복사 공식의 분자 부분 (상수)
a = 2.0*h*c**2 

# 플랑크 복사 공식의 지수 부분 계산
b = h*c/(wavelengths*k*T)

# 플랑크 복사 공식에 따라 파장별 intensity(복사 세기) 계산
intensities = a / ( (wavelengths**5) * (np.exp(b) - 1.0) )

# 파장 배열 출력
# print ("wavelengths: {}".format(wavelengths))
# 파장 배열의 길이(개수) 출력
print ("len(wavelengths): {}".format(len(wavelengths)))
# 계산된 intensity(복사 세기) 배열 출력
# print ("intensities: {}".format(intensities))
# intensity 배열의 길이(개수) 출력
print ("len(intensities): {}".format(len(intensities)))

# %% code 14.
import matplotlib.pyplot as plt

# 파장(wavelengths)을 nm 단위로 변환하여 플랑크 곡선(intensities) 그리기, 6000K는 파란색 선으로 표시
plt.plot(wavelengths*1e9, intensities, 'b-', label = '6000 K') # 6000 K 파란 선

# 그래프 제목 설정
plt.title('Planck Curve')

# x축 라벨 설정 (Latex 포맷 사용, nm 단위)
plt.xlabel(r'Wavelengths [$\rm{nm}$]') # raw 문자열을 쓰면 LaTeX 수식을 넣을 수 있다

# y축 라벨 설정
plt.ylabel('Intensity')

# 범례(legend) 표시
plt.legend()

# 그래프 출력
plt.show() # 그래프 출력

# %% code 15.
from astropy import units as u
h = 6.626e-34 * u.J * u.s      # (플랑크 상수)
c = 3.0e+8  * u.m / u.s        # (광속)
k = 1.38e-23 * u.J / u.K       # (볼츠만 상수)
wavelengths = 0.0000005 * u.m  # (파장)
T = 6000. * u.K                # (온도)

print ("h: {}".format(h))
print ("c: {}".format(c))
print ("k: {}".format(k))
print ("wavelengths: {}".format(wavelengths))
print ("T: {}".format(T))

# %% code 16.
from astropy import constants as const

# 플랑크 상수(const.h) 출력
print("const.h:{}".format(const.h))
# 빛의 속도(const.c) 출력
print("const.c:{}".format(const.c))
# 볼츠만 상수(const.k_B) 출력
print("const.k_B:{}".format(const.k_B))

# %% code 17.
def planckQ(wavelengths, T):
 # 플랑크 곡선 공식의 분자 부분 (상수)
    a = 2.0 * const.h * const.c**2
 # 플랑크 곡선 공식의 지수 부분 계산
    b = const.h * const.c / (wavelengths * const.k_B * T)
 # 플랑크 곡선 공식에 따라 파장별 intensity(복사 세기) 계산
    intensity = a / (((wavelengths.to(u.m))**5) * (np.exp(b) - 1.0))
    return intensity

wavelengths = np.arange(1e-8, 3e-6, 1e-8) * u.m   # 파장 배열 생성 (단위: m)
Temperatures = np.arange(4000, 7001, 1000) * u.K  # 온도 배열 생성 (단위: K)

intensities = planckQ(wavelengths, T)  # 주어진 온도 T에서 파장별 intensity 계산

# print(f'intensities : {intensities.value} {intensities.unit}') # intensity 값과 단위 출력
print(f'len(intensities) : {len(intensities)}')  # intensity 길이 출력

plt.figure()  # 새로운 그림(figure) 생성

for T in Temperatures : 
    intensity = planckQ(wavelengths, T)  # 각 온도별 플랑크 곡선 계산
    plt.plot(wavelengths, intensity, label="{0:.0f}".format(T))  # 곡선 그리기 및 온도 라벨

plt.title('Planck Curves')  # 그래프 제목 설정


plt.xlabel(f'Wavelengths [{wavelengths.to(u.um).unit:latex_inline}]')  # x축 라벨(파장, 단위 포함)
plt.ylabel(f'Spectral radiance [{intensity.to(u.kW/u.m/u.m/u.nm).unit:latex_inline}]')  # y축 라벨(스펙트럼 복사 세기, 단위 포함)

plt.legend()  # 범례 표시

plt.show()  # 그래프 출력

# %% code 18.
from astropy.modeling.models import BlackBody

bb_temp = 5778*u.K
bb = BlackBody(temperature = bb_temp)
wavelength = 10000 * u.AA
flux = bb(wavelength)

print('bb_temp : {}'.format(bb_temp))
print("type(bb_temp)", type(bb_temp))
print('wavelength : {}'.format(wavelength))
print('flux : {}'.format(flux))
print("type(flux)", type(flux))

# %% code 19.
print(f'flux: {flux.value:0.1f} {flux.unit}')
print(f'flux: {flux.value:0.8f} {flux.unit:fits}')
print(f'flux: {flux.value:0.0f} {flux.unit:cds}')
print(f'flux: {flux.value:0.0f} {flux.unit:latex}')
print('bb_temp.to(u.deg_C, equivalencies=u.temperature()) : {0.value:0.01f} {0.unit}'\
      .format(bb_temp.to(u.deg_C, equivalencies=u.temperature())))
print('wavelength.to(u.micron)  : {0.value:0.02f} {0.unit:FITS}'\
      .format(wavelength.to(u.micron) ))
print('flux.to(u.W / (u.m**2 * u.Hz * u.sr)) : {0.value:0.08f} {0.unit:FITS}'\
      .format(flux.to(u.W / (u.m**2 * u.Hz * u.sr))))

# %% code 20.
from astropy.visualization import quantity_support

# 5778K(태양 표면 온도) 흑체 모델 생성
bb = BlackBody(temperature=5778*u.K)

# 1000~110000 옹스트롬(Å) 범위의 파장 배열 생성
wavelength = np.arange(1000, 110000) * u.AA

# 각 파장에서의 흑체 복사 플럭스 계산
flux = bb(wavelength)

# astropy의 quantity 단위 지원 활성화
with quantity_support():
    plt.figure(figsize=(6, 5))  # 그림 크기 지정
 # 파장 단위: 마이크로미터(um), 플럭스 단위: W/(m²·Hz·sr)로 변환하여 그리기
    plt.plot(wavelength.to(u.um), flux.to(u.W / (u.m**2 * u.Hz * u.sr)))
 # 최대 플럭스 파장(lambda_max)에 점선 표시 (um 단위)
    plt.axvline(bb.nu_max.to(u.um, equivalencies=u.spectral()).value, ls='--')
    plt.title('Blackbody Spectrum (T=5778 K) [SI Units]')
    plt.xlabel(f'Wavelength [{wavelength.to(u.um).unit:latex_inline}]')
    plt.ylabel(r'Flux [W m$^{-2}$ Hz$^{-1}$ sr$^{-1}$]')
    du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_02_Plotting_Planck_curve_01"))
    plt.show()

# %% code 21.
from astropy import units as u
from astropy import constants as const
import matplotlib.pyplot as plt
import numpy as np
import math

wavelengths = np.arange(100, 2001) * u.nm

# 온도를 리스트에 저장해 보자.
Temperatures = np.arange(3500, 5501, 500) * u.K  # (온도)

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(1, 1, 1)

for T in Temperatures : 
    intensity = planckQ(wavelengths.to(u.m), T)
    plt.plot(wavelengths.to(u.nm), intensity, label="{0:.0f}".format(T)) 

ax.set_facecolor('xkcd:silver')

# X축 Y축 범위 설정
ax.set_xlim(min(wavelengths).value, max(wavelengths).value)
ax.set_ylim(min(intensity).value, max(intensity).value*1.1)

# X축 틱 추가하기 
ax.set_xticks([i for i in np.arange(0., max(wavelengths).value + 3, 500)])
ax.set_xticks([i for i in np.arange(0., max(wavelengths).value + 3, 100)], minor=True)

# 틱 길이, 방향 설정
ax.tick_params(direction='in', length=8, width=1, colors='k',
               grid_color='k', grid_alpha=0.5, 
               bottom=True, top=True, left=True, right=True)
ax.tick_params(direction='in', length=3, width=1, colors='k',
               grid_color='k', grid_alpha=0.5, which = 'minor', 
               bottom=True, top=True, left=True, right=True)

plt.title('The Planck Curve', fontdict={'size':12})
plt.xlabel(f'Wavelength [{wavelengths.unit}]', fontdict={'size':10})  # 단위를 한 줄로
plt.ylabel(f'Spectral energy density [{intensity.unit}]', fontdict={'size':10})  # 단위를 한 줄로

plt.legend()
du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_02_Plotting_Planck_curve_02"))
plt.show()
