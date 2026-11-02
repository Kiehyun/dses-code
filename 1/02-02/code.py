# 지구과학 데이터 사이언스 1 | II-02. 플랑크 곡선 그리기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅱ-13.
h = 6.626e-34  # J s, 플랑크 상수
c = 3.0e+8     # m/s, 광속
k = 1.38e-23   # J/K, 볼츠만 상수

import numpy as np

wavelengths = np.arange(1e-8, 3e-6, 1e-8)  # m, 10 nm ~ 3 μm(10 nm 간격)
T = 6000.                                  # K
a = 2.0*h*c**2 
b = h*c/(wavelengths*k*T)
intensities = a / ( (wavelengths**5) * (np.exp(b) - 1.0) )  # 파장별 복사 세기

print ("len(wavelengths): {}".format(len(wavelengths)))
print ("len(intensities): {}".format(len(intensities)))

# %% code Ⅱ-14.
import matplotlib.pyplot as plt

# 파장을 nm로 바꿔 그리기
plt.plot(wavelengths*1e9, intensities, 'b-', label = '6000 K')
plt.title('플랑크 곡선 (6000 K)')
plt.xlabel(r'파장 [$\rm{nm}$]')  # raw 문자열을 쓰면 LaTeX 수식을 넣을 수 있다
plt.ylabel(r'분광 복사휘도 [W m$^{-2}$ m$^{-1}$ sr$^{-1}$]')
plt.legend()
plt.show()

# %% code Ⅱ-15.
from astropy import units as u
h = 6.626e-34 * u.J * u.s      # 플랑크 상수
c = 3.0e+8  * u.m / u.s        # 광속
k = 1.38e-23 * u.J / u.K       # 볼츠만 상수
wavelengths = 0.0000005 * u.m  # 파장(500 nm)
T = 6000. * u.K

print ("h: {}".format(h))
print ("c: {}".format(c))
print ("k: {}".format(k))
print ("wavelengths: {}".format(wavelengths))
print ("T: {}".format(T))

# %% code Ⅱ-16.
from astropy import constants as const

print("const.h:{}".format(const.h))
print("const.c:{}".format(const.c))
print("const.k_B:{}".format(const.k_B))

# %% code Ⅱ-17.
def planckQ(wavelengths, T):
    a = 2.0 * const.h * const.c**2
    b = const.h * const.c / (wavelengths * const.k_B * T)
    # 분광 복사휘도: 단위 면적 · 단위 파장 · 단위 입체각(sr)당 일률
    intensity = a / (((wavelengths.to(u.m))**5) * (np.exp(b) - 1.0)) / u.sr
    return intensity

wavelengths = np.arange(1e-8, 3e-6, 1e-8) * u.m
Temperatures = np.arange(4000, 7001, 1000) * u.K

intensities = planckQ(wavelengths, T)  # T는 앞 셀의 6000 K

print(f'len(intensities) : {len(intensities)}')
print(f'intensities.unit : {intensities.unit}')

# 축에 적을 단위로 값을 바꾼 뒤 그리기
wl_unit = u.um
I_unit = u.kW / (u.m**2 * u.nm * u.sr)

plt.figure()

for T in Temperatures :
    intensity = planckQ(wavelengths, T)
    plt.plot(wavelengths.to(wl_unit).value, intensity.to(I_unit).value,
             label="{0:.0f}".format(T))

plt.title('플랑크 곡선')

plt.xlabel(f'파장 [{wl_unit:latex_inline}]')
plt.ylabel(f'분광 복사휘도 [{I_unit:latex_inline}]')

plt.legend()

plt.show()

# %% code Ⅱ-18.
from astropy.modeling.models import BlackBody

bb_temp = 5778*u.K         # 태양 표면 온도
bb = BlackBody(temperature = bb_temp)
wavelength = 10000 * u.AA  # 10000 Å = 1 μm
flux = bb(wavelength)

print('bb_temp : {}'.format(bb_temp))
print("type(bb_temp)", type(bb_temp))
print('wavelength : {}'.format(wavelength))
print('flux : {}'.format(flux))
print("type(flux)", type(flux))

# %% code Ⅱ-19.
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

# %% code Ⅱ-20.
from astropy.visualization import quantity_support

bb = BlackBody(temperature=5778*u.K)         # 태양 표면 온도
wavelength = np.arange(1000, 110000) * u.AA  # 0.1 ~ 11 μm
flux = bb(wavelength)

with quantity_support():  # 단위가 붙은 값을 바로 그리기
    plt.figure(figsize=(6, 5))
    plt.plot(wavelength.to(u.um), flux.to(u.W / (u.m**2 * u.Hz * u.sr)))
    # 진동수 기준 최대 복사(ν_max)를 파장으로 바꾼 위치
    plt.axvline(bb.nu_max.to(u.um, equivalencies=u.spectral()).value, ls='--')
    plt.title('흑체 복사 스펙트럼 (T = 5778 K)')
    plt.xlabel(f'파장 [{wavelength.to(u.um).unit:latex_inline}]')
    plt.ylabel(r'분광 복사휘도 [W m$^{-2}$ Hz$^{-1}$ sr$^{-1}$]')
    du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_02_Plotting_Planck_curve_01"))
    plt.show()

# %% code Ⅱ-21.
from astropy import units as u
from astropy import constants as const
import matplotlib.pyplot as plt
import numpy as np
import math

wavelengths = np.arange(100, 2001) * u.nm

Temperatures = np.arange(3500, 5501, 500) * u.K

I_unit = u.kW / (u.m**2 * u.nm * u.sr)  # 세로축 단위

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(1, 1, 1)

for T in Temperatures : 
    intensity = planckQ(wavelengths.to(u.m), T).to(I_unit)  # 축 단위로 바꾸기
    plt.plot(wavelengths.to(u.nm).value, intensity.value, label="{0:.0f}".format(T)) 

ax.set_facecolor('xkcd:silver')

# 축 범위
ax.set_xlim(min(wavelengths).value, max(wavelengths).value)
ax.set_ylim(min(intensity).value, max(intensity).value*1.1)

# 주 눈금 500 nm, 보조 눈금 100 nm
ax.set_xticks([i for i in np.arange(0., max(wavelengths).value + 3, 500)])
ax.set_xticks([i for i in np.arange(0., max(wavelengths).value + 3, 100)], minor=True)

# 눈금을 안쪽으로, 네 변 모두(주 눈금 · 보조 눈금)
ax.tick_params(direction='in', length=8, width=1, colors='k',
               grid_color='k', grid_alpha=0.5, 
               bottom=True, top=True, left=True, right=True)
ax.tick_params(direction='in', length=3, width=1, colors='k',
               grid_color='k', grid_alpha=0.5, which = 'minor', 
               bottom=True, top=True, left=True, right=True)

plt.title('플랑크 곡선', fontdict={'size':12})
# 단위를 한 줄로
plt.xlabel(f'파장 [{wavelengths.unit:latex_inline}]', fontdict={'size':10})
# 단위를 한 줄로
plt.ylabel(f'분광 복사휘도 [{I_unit:latex_inline}]', fontdict={'size':10})

plt.legend()
du.save_figure(plt.gcf(), os.path.join(proj_dir, "02_02_Plotting_Planck_curve_02"))
plt.show()
