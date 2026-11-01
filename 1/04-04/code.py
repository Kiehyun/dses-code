# 지구과학 데이터 사이언스 1 | IV-04. 대기 중의 수증기량
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 66.
fname = "SURFACE_ASOS_116_MI_2019-08_2019-08_2019.csv"
fid = "1ZZNmeq9UAaz9-FUD1DR4m3Q9_XzZupxB"  # 구글 드라이브 파일 ID

from pathlib import Path

du.download(f"https://docs.google.com/uc?export=download&id={fid}", Path(proj_dir) / fname)

# %% code 67.
fpaths = du.list_files(proj_dir, "csv")

# %% code 68.
du.preview_text(fpaths[0], n=10);

# %% code 69.
from metpy.units import units as u

v_distance = 8 * u.m  # 8 m
v_time = 3 * u.s      # 3 s

average_velocity = v_distance / v_time  # 단위도 m/s로 함께 계산

print("type(v_distance):{}".format(type(v_distance)))
print(f"average_velocity):{average_velocity:0.03f}")

# %% code 70.
import numpy as np
from metpy.units import units as u
import metpy.calc as mpcalc
import matplotlib.pyplot as plt

temp_array = np.arange(-20, 40, 0.1) * u.degC  # -20~40 °C, 0.1 °C 간격

sat_vap_array = mpcalc.saturation_vapor_pressure(temp_array)

# 10 °C마다 점을 찍을 온도와 그 포화수증기압
tick_temps = np.arange(-20, 41, 10)
tick_indices = [np.abs(temp_array.magnitude - t).argmin() for t in tick_temps]
tick_pressures = sat_vap_array[tick_indices].to(u.hPa).magnitude

fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(temp_array.magnitude, sat_vap_array.to(u.hPa).magnitude, color='tab:blue', label='포화수증기압')

for t, p in zip(tick_temps, tick_pressures):
    ax.plot(t, p, 'ro')
    ax.annotate(f'{p:.1f}', (t, p), textcoords="offset points", xytext=(0,8), ha='center', fontsize=10, color='red')

ax.set_title('온도에 따른 포화수증기압 곡선', fontsize=16)
ax.set_xlabel('온도 (°C)', fontsize=14)
ax.set_ylabel('포화수증기압 (hPa)', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(fontsize=12)
plt.savefig(f'{proj_dir}/saturation_vapor_pressure_curve.pdf', dpi=300, bbox_inches='tight')
print(f"'saturation_vapor_pressure_curve.pdf' saved in {proj_dir}")
plt.show()

# %% code 71.
import numpy as np
from metpy.units import units as u
import metpy.calc as mpcalc
import matplotlib.pyplot as plt
import platform

temp_array = np.arange(-20, 40.1, 0.1) * u.degC  # -20~40 °C, 0.1 °C 간격
press = 1000 * u.hPa                             # 기준 기압

sat_mr = mpcalc.saturation_mixing_ratio(press, temp_array)  # 포화 혼합비
sat_sh = mpcalc.specific_humidity_from_mixing_ratio(sat_mr)  # 포화 비습

# 10 °C마다 점을 찍을 온도와 그 값
tick_temps = np.arange(-20, 41, 10)
tick_indices = [np.abs(temp_array.magnitude - t).argmin() for t in tick_temps]
tick_mr = sat_mr[tick_indices].to_base_units().magnitude * 1000  # kg/kg → g/kg
tick_sh = sat_sh[tick_indices].to_base_units().magnitude * 1000  # kg/kg → g/kg

fig, axs = plt.subplots(1, 2, figsize=(12.0, 4.3))

# 1) 포화 혼합비
ax = axs[0]
ax.plot(temp_array.magnitude, sat_mr.magnitude * 1000, color='tab:green', label='포화 혼합비')
for t, mr in zip(tick_temps, tick_mr):
    ax.plot(t, mr, 'ro')
    ax.annotate(f'{mr:.1f}', (t, mr), textcoords="offset points", xytext=(0,8), ha='center', fontsize=10, color='red')
ax.set_title('온도에 따른 포화 혼합비 곡선', fontsize=16)
ax.set_xlabel('온도 (°C)', fontsize=14)
ax.set_ylabel('포화 혼합비 (g/kg)', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(fontsize=12)

# 2) 포화 비습
ax = axs[1]
ax.plot(temp_array.magnitude, sat_sh.magnitude * 1000, color='tab:purple', label='포화 비습')
for t, sh in zip(tick_temps, tick_sh):
    ax.plot(t, sh, 'ro')
    ax.annotate(f'{sh:.1f}', (t, sh), textcoords="offset points", xytext=(0,8), ha='center', fontsize=10, color='red')
ax.set_title('온도에 따른 포화 비습 곡선', fontsize=16)
ax.set_xlabel('온도 (°C)', fontsize=14)
ax.set_ylabel('포화 비습 (g/kg)', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(fontsize=12)

plt.tight_layout()
plt.show()

# %% code 72.
import pandas as pd

df = pd.read_csv(fpaths[0],
                 thousands=',',  # 천 단위 쉼표 처리
                 encoding='euc-kr')

print("type(df['일시'][0]):{}".format(type(df['일시'][0])))

df['dt_YmdHM'] = pd.to_datetime(df['일시'])  # 문자열 → datetime

print("type(df['dt_YmdHM'][0]):{}".format(type(df['dt_YmdHM'][0])))

df.index = df['dt_YmdHM']

from datetime import timedelta

# 직전 1분 측정값이므로 1분 당긴 시각을 인덱스로
df['dt_YmdHM-1min'] = df['dt_YmdHM'] - timedelta(minutes=1)

df.index = df['dt_YmdHM-1min']

print(f"df :\n{df}")

# %% code 73.
print("df : \n", df)

# %% code 74.
# 현지기압 관측값이 없으므로 1000 hPa로 가정
df['현지기압(hPa)'] = 1000

# 기온 · 상대습도 → 이슬점온도
df['이슬점온도(°C)'] = mpcalc.dewpoint_from_relative_humidity(
            df["기온(°C)"].values * u.degC, df["습도(%)"].values * u.percent
        )

# 기압 · 기온 · 이슬점온도 → 습구온도
df['습구온도(°C)'] = mpcalc.wet_bulb_temperature(
            df["현지기압(hPa)"].values * u.hPa,
            df["기온(°C)"].values * u.degC,
            df["이슬점온도(°C)"].values * u.degC
        )

print("df[['기온(°C)', '습도(%)', '이슬점온도(°C)', '습구온도(°C)']] :\n",
      df[['기온(°C)', '습도(%)', '이슬점온도(°C)', '습구온도(°C)']])

# %% code 75.
# 기압 · 기온 · 상대습도 → 혼합비
df['혼합비(kg/kg)'] = mpcalc.mixing_ratio_from_relative_humidity(
            df["현지기압(hPa)"].values * u.hPa,
            df["기온(°C)"].values * u.degC, df["습도(%)"].values * u.percent
        )

# 기압 · 이슬점온도 → 비습
df['비습(kg/kg)'] = mpcalc.specific_humidity_from_dewpoint(
            df["현지기압(hPa)"].values * u.hPa,
            df['이슬점온도(°C)'].values * u.degC,
        )

# 기압 · 혼합비 → 수증기압
df['수증기압(hPa)'] = mpcalc.vapor_pressure(
            df["현지기압(hPa)"].values * u.hPa,
            df["혼합비(kg/kg)"].values * u.kg / u.kg
        )

print("df[['현지기압(hPa)', '혼합비(kg/kg)', '비습(kg/kg)', '수증기압(hPa)']] :\n",
      df[['현지기압(hPa)', '혼합비(kg/kg)', '비습(kg/kg)', '수증기압(hPa)']])

# %% code 76.
def absolute_humidity_from_vapor_pressure(e, T):
    """
    수증기압(e, hPa)과 기온(T, °C 또는 K)으로부터 절대습도(g/m^3)를 계산합니다.
    AH = 217 * e / T(K)
    """
    from metpy.units import units as u
    import numpy as np

    # 기온을 켈빈으로
    if hasattr(T, 'units') and T.units == u.degC:
        T_K = T.to(u.kelvin)
    elif hasattr(T, 'units') and T.units == u.kelvin:
        T_K = T
    else:
        T_K = T + 273.15  # 단위 없는 배열은 °C로 간주

    if hasattr(e, 'magnitude'):  # 단위가 붙은 값이면 숫자만 꺼내기
        e_hPa = e.to(u.hPa)
        AH = 217 * e_hPa.magnitude / T_K.magnitude  # g/m^3
    else:
        AH = 217 * e / T_K  # g/m^3

    return AH

df['절대습도(g/m^3)'] = absolute_humidity_from_vapor_pressure(
    df["수증기압(hPa)"].values * u.hPa, df["기온(°C)"].values * u.degC
)

print("df[['수증기압(hPa)', '절대습도(g/m^3)']] :\n",
      df[['수증기압(hPa)', '절대습도(g/m^3)']])

# %% code 77.
df.to_csv(f"{proj_dir}/{fpaths[0].stem}_result.csv", index=False)
print(f"파일 저장 완료: {proj_dir}/{fpaths[0].stem}_result.csv")
