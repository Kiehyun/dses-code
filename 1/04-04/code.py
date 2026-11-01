# 지구과학 데이터 사이언스 1 | IV-04. 대기 중의 수증기량
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 70.
# 프로젝트(자료 저장) 폴더 생성 — 공통 함수 사용
proj_dir = du.make_project_dir(du.current_notebook_name() or "04_04_Water_Vapor_in_the_Atmosphere")
from pathlib import Path

# %% code 71.
fname = "SURFACE_ASOS_116_MI_2019-08_2019-08_2019.csv"
fid = "1NLHwhmqnikHC77DdkelYBPnpwkJv8_rb"

# requests 라이브러리를 이용(나의 구글드라이브에서 공유한 파일을 구글 코랩에서 사용할 경우)
from pathlib import Path

du.download(f"https://docs.google.com/uc?export=download&id={fid}", Path(proj_dir) / fname)

# %% code 72.
fpaths = du.list_files(proj_dir, "csv")

# %% code 73.
du.preview_text(fpaths[0], n=10)

# %% code 74.
from metpy.units import units as u

# 거리(8미터)에 단위 부여
v_distance = 8 * u.m
# 시간(3초)에 단위 부여
v_time = 3 * u.s

# 평균 속도 계산 (거리/시간)
average_velocity = v_distance / v_time

# v_distance의 자료형 출력
print("type(v_distance):{}".format(type(v_distance)))
# 평균 속도 값과 단위 출력
print(f"average_velocity):{average_velocity:0.03f}")

# %% code 75.
import numpy as np
from metpy.units import units as u
import metpy.calc as mpcalc
import matplotlib.pyplot as plt

# 온도 배열 생성 (-20°C ~ 40°C, 0.1°C 간격)
temp_array = np.arange(-20, 40, 0.1) * u.degC

# 포화수증기압 계산
sat_vap_array = mpcalc.saturation_vapor_pressure(temp_array)

# 10도 간격으로 표시할 온도와 해당 인덱스, 포화수증기압 값 추출
tick_temps = np.arange(-20, 41, 10)
tick_indices = [np.abs(temp_array.magnitude - t).argmin() for t in tick_temps]
tick_pressures = sat_vap_array[tick_indices].to(u.hPa).magnitude

# 그래프 그리기
fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(temp_array.magnitude, sat_vap_array.to(u.hPa).magnitude, color='tab:blue', label='포화수증기압')

# 10도 간격마다 점과 값 표시
for t, p in zip(tick_temps, tick_pressures):
    ax.plot(t, p, 'ro')
    ax.annotate(f'{p:.1f}', (t, p), textcoords="offset points", xytext=(0,8), ha='center', fontsize=10, color='red')

# 그래프 제목, 축 이름, 격자, 범례 설정
ax.set_title('온도에 따른 포화수증기압 곡선', fontsize=16)
ax.set_xlabel('온도 (°C)', fontsize=14)
ax.set_ylabel('포화수증기압 (hPa)', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(fontsize=12)
# 그래프 저장
plt.savefig(f'{proj_dir}/saturation_vapor_pressure_curve.pdf', dpi=300, bbox_inches='tight')
print(f"'saturation_vapor_pressure_curve.pdf' saved in {proj_dir}")
# 그래프 출력
plt.show()

# %% code 76.
import numpy as np
from metpy.units import units as u
import metpy.calc as mpcalc
import matplotlib.pyplot as plt
import platform

# 온도 배열 생성 (-20°C ~ 40°C, 0.1°C 간격)
temp_array = np.arange(-20, 40.1, 0.1) * u.degC
press = 1000 * u.hPa  # 기준 기압 1000hPa

# 포화 혼합비, 포화 비습 계산
sat_mr = mpcalc.saturation_mixing_ratio(press, temp_array)  # 포화 혼합비
sat_sh = mpcalc.specific_humidity_from_mixing_ratio(sat_mr) # 포화 비습

# 10도 간격으로 표시할 온도와 해당 인덱스, 값 추출
tick_temps = np.arange(-20, 41, 10)
tick_indices = [np.abs(temp_array.magnitude - t).argmin() for t in tick_temps]
tick_mr = sat_mr[tick_indices].to_base_units().magnitude * 1000  # g/kg 단위 변환
tick_sh = sat_sh[tick_indices].to_base_units().magnitude * 1000  # g/kg 단위 변환

fig, axs = plt.subplots(1, 2, figsize=(12.0, 4.3))

# (1) 포화 혼합비 곡선 그리기
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

# (2) 포화 비습 곡선 그리기
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

# %% code 77.
# pandas 라이브러리 불러오기
import pandas as pd

# CSV 파일을 데이터프레임으로 읽기
df = pd.read_csv(fpaths[0],
                 thousands=',',      # 천 단위 구분자 처리
                 encoding='euc-kr')  # 한글 인코딩

# '일시' 컬럼 자료형 확인
print("type(df['일시'][0]):{}".format(type(df['일시'][0])))

# '일시' 컬럼을 날짜/시간 타입으로 변환
df['dt_YmdHM'] = pd.to_datetime(df['일시'])

# 변환된 컬럼의 자료형 확인
print("type(df['dt_YmdHM'][0]):{}".format(type(df['dt_YmdHM'][0])))

# 인덱스를 날짜/시간 컬럼으로 설정
df.index = df['dt_YmdHM']

# timedelta 불러오기
from datetime import timedelta

# 1분 뺀 새로운 컬럼 생성
df['dt_YmdHM-1min'] = df['dt_YmdHM'] - timedelta(minutes=1)

# 인덱스를 1분 뺀 컬럼으로 재설정
df.index = df['dt_YmdHM-1min']

# 데이터프레임 출력
print(f"df :\n{df}")

# %% code 78.
print("df : \n", df)

# %% code 79.
# 현지기압(hPa) 값을 1000으로 설정 (관측값이 없으므로 임시로 입력)
df['현지기압(hPa)'] = 1000

# 이슬점온도(°C) 계산 (기온과 상대습도를 이용)
df['이슬점온도(°C)'] = mpcalc.dewpoint_from_relative_humidity(
            df["기온(°C)"].values * u.degC, 
            df["습도(%)"].values * u.percent
        )

# 습구온도(°C) 계산 (현지기압, 기온, 이슬점온도를 이용)
df['습구온도(°C)'] = mpcalc.wet_bulb_temperature(
            df["현지기압(hPa)"].values * u.hPa, 
            df["기온(°C)"].values * u.degC, 
            df["이슬점온도(°C)"].values * u.degC
        )

# 주요 컬럼(기온, 습도, 이슬점온도, 습구온도) 출력
print("df[['기온(°C)', '습도(%)', '이슬점온도(°C)', '습구온도(°C)']] :\n", 
      df[['기온(°C)', '습도(%)', '이슬점온도(°C)', '습구온도(°C)']])

# %% code 80.
# 혼합비(kg/kg) 계산 (현지기압, 기온, 상대습도를 이용)
df['혼합비(kg/kg)'] = mpcalc.mixing_ratio_from_relative_humidity(
            df["현지기압(hPa)"].values * u.hPa, 
            df["기온(°C)"].values * u.degC, 
            df["습도(%)"].values * u.percent
        )

# 비습(kg/kg) 계산 (현지기압, 이슬점온도를 이용)
df['비습(kg/kg)'] = mpcalc.specific_humidity_from_dewpoint(
            df["현지기압(hPa)"].values * u.hPa, 
            df['이슬점온도(°C)'].values * u.degC,
        )

# 수증기압(hPa) 계산 (현지기압, 혼합비를 이용)
df['수증기압(hPa)'] = mpcalc.vapor_pressure(
            df["현지기압(hPa)"].values * u.hPa, 
            df["혼합비(kg/kg)"].values * u.kg / u.kg
        )

# 주요 컬럼(현지기압, 혼합비, 비습, 수증기압) 출력
print("df[['현지기압(hPa)', '혼합비(kg/kg)', '비습(kg/kg)', '수증기압(hPa)']] :\n", 
      df[['현지기압(hPa)', '혼합비(kg/kg)', '비습(kg/kg)', '수증기압(hPa)']])

# %% code 81.
# 절대습도(absolute humidity) 계산 함수
# e: 수증기압(hPa), T: 기온(°C 또는 K)
# 반환값: g/m^3 단위의 절대습도

def absolute_humidity_from_vapor_pressure(e, T):
    """
    수증기압(e, hPa)과 기온(T, °C 또는 K)으로부터 절대습도(g/m^3)를 계산합니다.
    AH = 217 * e / T(K)
    """
    from metpy.units import units as u
    import numpy as np

 # T가 섭씨 단위이면 켈빈으로 변환
    if hasattr(T, 'units') and T.units == u.degC:
        T_K = T.to(u.kelvin)
    elif hasattr(T, 'units') and T.units == u.kelvin:
        T_K = T
    else:
 # 단위가 없는 경우(넘파이 배열 등)
        T_K = T + 273.15

 # e가 pint.Quantity면 값만 추출
    if hasattr(e, 'magnitude'):
        e_hPa = e.to(u.hPa)
        AH = 217 * e_hPa.magnitude / T_K.magnitude  # g/m^3
    else:
        AH = 217 * e / T_K  # g/m^3

    return AH

# 절대습도(g/m^3) 컬럼 계산 및 추가
df['절대습도(g/m^3)'] = absolute_humidity_from_vapor_pressure(
    df["수증기압(hPa)"].values * u.hPa, 
    df["기온(°C)"].values * u.degC
)

# 주요 컬럼(수증기압, 절대습도) 출력
print("df[['수증기압(hPa)', '절대습도(g/m^3)']] :\n", 
      df[['수증기압(hPa)', '절대습도(g/m^3)']])

# %% code 82.
df.to_csv(f"{proj_dir}/{fpaths[0].stem}_result.csv", index=False)
print(f"파일 저장 완료: {proj_dir}/{fpaths[0].stem}_result.csv")
