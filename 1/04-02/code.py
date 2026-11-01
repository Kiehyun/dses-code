# 지구과학 데이터 사이언스 1 | IV-02. 킬링 곡선 그리기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 22.
import matplotlib.pyplot as plt


# 대기 구성 성분과 비율
labels = [
    '질소 (N₂)', 
    '산소 (O₂)', 
    '아르곤 (Ar)', 
    '이산화탄소 (CO₂)', 
    '기타'
]
sizes = [
    78.084,  # N2
    20.946,  # O2
    0.934,   # 아르곤
    0.040,   # 이산화탄소
    0.001    # All others (대략 나머지 합산)
]
colors = ['mediumpurple', 'skyblue', 'gold', 'tomato', 'lightgrey']

# 파이 차트 그리기
plt.figure(figsize=(6, 4))
patches, texts, autotexts = plt.pie(
    sizes, 
    labels=labels, 
    colors=colors, 
    autopct='%1.3f%%', 
    startangle=140,
    wedgeprops={'edgecolor': 'black'},
    textprops={'fontsize': 10},
    pctdistance=0.8,   # % 텍스트 위치 (중심에서 조금 바깥으로)
    labeldistance=1.2  # 라벨 위치 (조금 더 바깥으로)
)

# All others 구성 성분
others_text = (
    "기타 성분 (ppm 기준):\n" "- 네온 (Ne): 18.2\n" "- 헬륨 (He): 5.24\n" "- 메탄 (CH₄): 1.5\n" "- 크립톤 (Kr): 1.14\n" "- 수소 (H₂): 0.5" )

# All others 성분 설명 추가 (차트 오른쪽 바깥에 표시)
plt.text(1.3, 0.6, others_text, fontsize=10, va='top', ha='left',
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

plt.title('대기의 구성 성분 (건조 공기)', fontsize=14)
plt.axis('equal')  # 원형 비율 유지
plt.tight_layout()
plt.show()

# %% code 23.
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.ticker as mticker

# 관측소 위치 데이터 (경도, 위도, 이름)
stations = [
    (-155.58, 19.54, 'MAUNA LOA'),
    (-117.25, 32.87, 'LA JOLLA PIER'),
    (-155.45, 19.50, 'CAPE KUMUKAHI'),
    (-158.00, 4.00, 'FANNING ISLAND'),
    (-157.42, 1.87, 'CHRISTMAS ISLAND'),
    (-170.72, -14.27, 'AMERICAN SAMOA'),
    (179.42, -29.25, 'KERMADEC ISLANDS'),
    (174.78, -41.28, 'NEW ZEALAND'),
    (0.0, -90.00, 'SOUTH POLE'),
    (-70.78, -64.77, 'PALMER STATION'),
    (-110.00, 30.00, 'BAJA CALIFORNIA SUR'),
    (-145.00, 50.00, 'STATION P'),
    (-157.39, 71.32, 'POINT BARROW'),
    (-62.33, 82.50, 'ALERT')
]

# 태평양 중심 지도
plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
ax.set_global()

# 지도 배경
ax.add_feature(cfeature.LAND, color='lightgray')
ax.add_feature(cfeature.OCEAN, color='lightblue')
ax.add_feature(cfeature.COASTLINE)

# 경위도 격자선 추가
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='gray', alpha=0.5, linestyle='--')

# 격자선 라벨 설정
gl.top_labels = False
gl.right_labels = False
gl.xlines = True
gl.ylines = True

# 경도와 위도 간격 설정
gl.xlocator = mticker.FixedLocator(range(-180, 181, 30))  # 60도 간격
gl.ylocator = mticker.FixedLocator(range(-90, 91, 30))    # 30도 간격

# 경위도 포맷터 설정
gl.xformatter = LongitudeFormatter()
gl.yformatter = LatitudeFormatter()

# 라벨 폰트 크기 설정
gl.xlabel_style = {'size': 8}
gl.ylabel_style = {'size': 8}

# 특별히 왼쪽에 표시할 기지
left_label_stations = ['MAUNA LOA', 'FANNING ISLAND', 'LA JOLLA PIER']

# 점과 라벨 표시
for lon, lat, name in stations:
    if name == 'MAUNA LOA':
        continue  # Mauna Loa는 아래에서 따로 그림
    ax.plot(lon, lat, 'ko', markersize=5, transform=ccrs.PlateCarree())
    if name in left_label_stations:
        ax.text(lon - 5, lat, name, fontsize=8, ha='right', transform=ccrs.PlateCarree())
    else:
        ax.text(lon + 3, lat, name, fontsize=8, ha='left', transform=ccrs.PlateCarree())

# Mauna Loa는 빨간 점 + 빨간 글씨 (검은 점/글씨 없음)
ax.plot(-155.58, 19.54, 'ro', markersize=6, transform=ccrs.PlateCarree())
ax.text(-155.58 - 5, 19.54, 'MAUNA LOA', color='red', fontsize=9, fontweight='bold',
        ha='right', transform=ccrs.PlateCarree())

plt.title('대기 관측소 분포 (태평양 중심 지도)', fontsize=12)
plt.tight_layout()
plt.show()

# %% code 24.
from pathlib import Path

fname = "monthly_in_situ_co2_mlo.csv"

# 스크립스 CO2 프로그램에서 직접 내려받기
url = "https://keelinglabsites.ucsd.edu/websitedataco2/monthly_in_situ_co2_mlo.csv"
du.download(url, Path(proj_dir) / fname)

# %% code 25.
fpaths = du.list_files(proj_dir, "csv")

# %% code 26.
n_lines = 70  # 출력할 줄 수

print(f"파일 내용 출력 (처음 {n_lines}줄):")
print("="*40)

# 순수 파이썬으로 구현 (운영체제 무관)
try:
    with open(fpaths[0], encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= n_lines:
                break
            print(f"{i+1:3d}: {line.rstrip()}")
except UnicodeDecodeError:
 # UTF-8로 읽기 실패시 다른 인코딩 시도
    try:
        with open(fpaths[0], encoding='cp949') as f:
            for i, line in enumerate(f):
                if i >= n_lines:
                    break
                print(f"{i+1:3d}: {line.rstrip()}")
    except Exception as e2:
        print(f"파일 읽기 실패 (UTF-8, CP949 모두 실패): {e2}")
except Exception as e:
    print(f"파일 읽기 실패: {e}")

print("="*60)

# %% code 27.
# # !head -n 70 {fpaths[0]} # list the first 50 lines of the file
# print(f"파일 {fpaths[0]}의 첫 70줄을 출력합니다:")
# !powershell -Command "Get-Content {fpaths[0]} -TotalCount 70"

# %% code 28.
import pandas as pd

# CSV 파일을 읽어서 DataFrame으로 변환
df = pd.read_csv(str(fpaths[0]),           # 파일 경로 (문자열로 변환)
                 thousands = ',',  # 천 단위 구분자로 쉼표 사용
                 skiprows=64,      # 처음 64행을 건너뛰고 읽기 시작
                 names = ['Year',  # 연도
                          'Month',                    # 월
                          'Date Excel',               # 엑셀 날짜 형식
                          'Date',                     # 날짜
                          'CO2',                      # CO2 농도 원본 데이터
                          'seasonally adjusted',      # 계절 조정된 CO2 데이터
                          'fit',                      # 피팅된 데이터
                          'seasonally adjusted fit',  # 계절 조정된 피팅 데이터
                          'CO2 filled',               # 결측값이 채워진 CO2 데이터
                          'seasonally adjusted filled',  # 계절 조정된 채워진 데이터
                          'Station'],                 # 측정소 정보
                 encoding= 'unicode_escape') # 유니코드 이스케이프 인코딩 사용

df = df[df.CO2 != -99.99]
print("df: ", df)  # 읽어온 DataFrame 출력

# %% code 29.
df['datetime'] = pd.to_datetime(df['Date'], format='%Y') + pd.to_timedelta((df['Date'] % 1) * 365.25, unit='D')

# 방법 3: numpy를 사용한 벡터화된 방법
import numpy as np

def decimal_year_to_datetime_vectorized(decimal_years):
    years = decimal_years.astype(int)
    fractions = decimal_years - years
    
 # 각 연도의 시작일을 만들기
    start_dates = pd.to_datetime(years, format='%Y')
    
 # 윤년 체크를 위한 벡터화된 함수
    is_leap = ((years % 4 == 0) & (years % 100 != 0)) | (years % 400 == 0)
    days_in_year = np.where(is_leap, 366, 365)
    
 # 일수 계산 및 추가
    days_to_add = (fractions * days_in_year).astype(int)
    
    return start_dates + pd.to_timedelta(days_to_add, unit='D')

# 방법 3 적용 (대용량 데이터에 효율적)
df['datetime'] = decimal_year_to_datetime_vectorized(df['Date'])

# 결과 확인
print(df[['Date', 'datetime']])

# %% code 30.
import matplotlib.pyplot as plt

#차트 크기 설정
fig, ax = plt.subplots(figsize=(10.5,8))

ax.plot(df['Date'], df['CO2'])

# X축 Y축 범위 설정
ax.set_xlim(min(df['Date']), max(df['Date']))
ax.set_ylim(min(df['CO2']), max(df['CO2']))

# Y축 제목에 latex 수식 넣기
ax.set_ylabel(r'$\rm{CO_2}$ Concentration ($\rm{ppm}$)')
ax.set_xlabel(r'Year')

# 차트 제목 폰트 크기 크게
ax.set_title('Mauna Loa Observatory, Hawaii \nMonthly Average Carbon Dioxide Concentration',
             fontdict={'fontsize':16})
plt.show()

# %% code 31.
import matplotlib.pyplot as plt

#차트 크기 설정
fig, ax = plt.subplots(figsize=(10.5,8))

ax.plot(df['datetime'], df['CO2'])

# X축 Y축 범위 설정
ax.set_xlim(min(df['datetime']), max(df['datetime']))
ax.set_ylim(min(df['CO2']), max(df['CO2']))

# Y축 제목에 latex 수식 넣기
ax.set_ylabel(r'$\rm{CO_2}$ Concentration ($\rm{ppm}$)')
ax.set_xlabel(r'Year')

# 차트 제목 폰트 크기 크게
ax.set_title('Mauna Loa Observatory, Hawaii \nMonthly Average Carbon Dioxide Concentration',
             fontdict={'fontsize':16})
plt.show()

# %% code 32.
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10.5, 8))

ax.plot(df['Date'], df['CO2'])
ax.scatter(df['Date'], df['CO2'], marker='o', s=5)

# X축 Y축 범위 설정
ax.set_xlim(min(df['Date']), max(df['Date']))
ax.set_ylim(min(df['CO2']), max(df['CO2']))

# Y축 제목에 latex 수식 넣기
# X, Y축 제목에 크기 조정 및 굵게
ax.set_ylabel(r'$\rm{CO_2}$ Concentration ($\rm{ppm}$)', fontdict={'fontsize':16, 'fontweight':'bold'})
ax.set_xlabel(r'Year', fontdict={'fontsize':16, 'fontweight':'bold'})

#X축 틱 추가하기 (5년 간격, 1년 간격)
ax.set_xticks([i for i in range(1960, 2026, 5)])
ax.set_xticks([i for i in range(1960, 2026, 1)], minor=True)
ax.set_xticklabels([i for i in range(1960, 2026, 5)], fontdict={'fontsize':11, 'fontweight':'bold'})

#Y축 틱 추가하기 (5 ppm 간격, 1 ppm 간격)
ax.set_yticks([i for i in range(310, 421, 5)])
ax.set_yticks([i for i in range(310, 421, 1)], minor=True)
ax.set_yticklabels([i for i in range(310, 421, 5)], fontdict={'fontsize':11, 'fontweight':'bold'})
ax.set_yticklabels(sum([[i, ''] for i in [i for i in range(310, 421, 10)]], [])[:-1])

#ax.tick_params(axis='both', minor=True, bottom=True, top=True, left=True, right=True)

#틱 길이, 방향 설정
ax.tick_params(direction='in', length=8, width=1, colors='k',
               grid_color='k', grid_alpha=0.5, 
               bottom=True, top=True, left=True, right=True)
ax.tick_params(direction='in', length=3, width=1, colors='k',
               grid_color='k', grid_alpha=0.5, which = 'minor', 
               bottom=True, top=True, left=True, right=True)

# 차트 제목 왼쪽 정렬
ax.set_title('Mauna Loa Observatory, Hawaii \nMonthly Average Carbon Dioxide Concentration',
             y=1.05,   # 제목 아래 여백
             loc = 'left',
             fontdict={'fontsize':16, 'fontweight':'bold', 'horizontalalignment': 'left'})

# 차트 위에 작은 글씨 추가
ax.text(1958, 422, r'Data from Scripps $\rm{CO_2}$ Program',
             fontdict={'fontsize':12})
ax.text(1985, 422, r'Last updated June 2021',
             fontdict={'fontsize':12})

plt.show()

# %% code 33.
import matplotlib.pyplot as plt

# 그래프 설정
fig, ax = plt.subplots(figsize=(10.5, 8))
ax.set_xlim(min(df['Date']), max(df['Date']))
ax.set_ylim(min(df['CO2']), max(df['CO2']))

# 축 라벨
ax.set_xlabel('Year', fontsize=16, fontweight='bold')
ax.set_ylabel(r'$\rm{CO_2}$ Concentration ($\rm{ppm}$)', fontsize=16, fontweight='bold')

# 눈금 설정
ax.set_xticks(range(1960, 2026, 5))
ax.set_xticks(range(1960, 2026, 1), minor=True)
ax.set_yticks(range(310, 421, 5))
ax.set_yticks(range(310, 421, 1), minor=True)

# 눈금 스타일
ax.tick_params(direction='in', length=8, width=1, colors='k', which='major')
ax.tick_params(direction='in', length=3, width=1, colors='k', which='minor')

# 제목 및 출처
ax.set_title('Mauna Loa Observatory, Hawaii\nMonthly Average CO₂ Concentration',
             loc='left', y=1.05, fontsize=16, fontweight='bold')
ax.text(1958, 422, 'Data from Scripps CO₂ Program', fontsize=12)
ax.text(1985, 422, 'Last updated June 2021', fontsize=12)

# 초기 데이터 포인트
line, = ax.plot(df['Date'].iloc[0], df['CO2'].iloc[0])
point = ax.scatter(df['Date'].iloc[0], df['CO2'].iloc[0], s=5)

# %% code 34.
# 애니메이션 함수 정의
def animate(i):
 # i번째까지의 데이터로 라인 업데이트
    line.set_data(df['Date'].iloc[:i], df['CO2'].iloc[:i])
 # 현재 점의 위치 업데이트
    point.set_offsets([df['Date'].iloc[i], df['CO2'].iloc[i]])
    return line, point

from matplotlib.animation import FuncAnimation
ani = FuncAnimation(fig, animate, 
                     frames=len(df['Date']), 
                     blit=True)

from IPython.display import HTML
# 애니메이션을 표시하는 여러 방법 시도

# 방법 1: 자바스크립트 기반 HTML5 영상
try:
    HTML(ani.to_jshtml())
except:
 # 방법 2: matplotlib 의 HTML writer 사용
    import matplotlib
    matplotlib.rcParams['animation.html'] = 'html5'
    try:
        HTML(ani.to_html5_video())
    except:
 # 방법 3: 다른 표시 방법 사용
        from matplotlib import rc
        rc('animation', html='jshtml')
        ani

HTML(ani.to_jshtml())

# %% code 35.
# 파일명 설정
fname = 'Keeling_curve_MLO'

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

# %% code 36.
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO

url = "https://keelinglabsites.ucsd.edu/websitedataco2/monthly_in_situ_co2_mlo.csv"

# 새 Scripps CSV 직접 다운로드
response = requests.get(url)
response.raise_for_status()

lines = response.text.splitlines()

# 실제 데이터 시작 행 찾기
data_lines = [line for line in lines if re.match(r'^\s*\d{4}\s*,', line) ]

if len(data_lines) == 0:
    raise ValueError("CSV 안에서 데이터 행을 찾지 못했습니다. URL 또는 파일 내용을 확인하세요.")

csv_text = "\n".join(data_lines)

df1 = pd.read_csv(
    StringIO(csv_text),
    names=[
        'Year', 'Month', 'Date Excel', 'Date',
        'CO2', 'seasonally adjusted',
        'fit', 'seasonally adjusted fit',
        'CO2 filled', 'seasonally adjusted filled',
        'Sta'
    ],
    skipinitialspace=True
)

numeric_columns = [
    'CO2', 'seasonally adjusted',
    'fit', 'seasonally adjusted fit',
    'CO2 filled', 'seasonally adjusted filled'
]

all_numeric_columns = [
    'Year', 'Month', 'Date Excel', 'Date'
] + numeric_columns

for col in all_numeric_columns:
    df1[col] = pd.to_numeric(df1[col], errors='coerce')

df1 = df1.replace([-99.99, -999], np.nan)
df1 = df1.dropna(subset=['Date']).copy()

df1['datetime'] = decimal_year_to_datetime_vectorized(df1['Date'])

print("처리 전 데이터 정보:")
print(f"DataFrame 크기: {df1.shape}")
print("각 컬럼별 NaN 개수:")
print(df1.isnull().sum())

df1_time = df1.set_index('datetime').sort_index()

for col in numeric_columns:
    df1_time[col] = df1_time[col].interpolate(method='time', limit_area='inside')

df1_final = df1_time.reset_index()
df1_final = df1_final.dropna(subset=['Date', 'seasonally adjusted filled']).copy()

print("시간 기반 인터폴레이션 완료!")
print("처리 후 데이터 정보:")
print(f"DataFrame 크기: {df1_final.shape}")
print("각 컬럼별 NaN 개수:")
print(df1_final.isnull().sum())

df1 = df1_final.copy()

x_min = int(df1['Date'].min() // 10 * 10)
x_max = int(df1['Date'].max() // 10 * 10)

y_min = int(df1['seasonally adjusted filled'].min() // 10 * 10)
y_max = int(df1['seasonally adjusted filled'].max() // 10 * 10)

fig, ax = plt.subplots(figsize=(10.5, 8))

ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

ax.set_ylabel(
    r'$\rm{CO_2}$ Concentration ($\rm{ppm}$)',
    fontdict={'fontsize': 16, 'fontweight': 'bold'}
)

ax.set_xlabel(
    r'Year',
    fontdict={'fontsize': 16, 'fontweight': 'bold'}
)

ax.set_xticks([i for i in range(x_min, x_max + 1, 5)])
ax.set_xticks([i for i in range(x_min, x_max + 1, 1)], minor=True)

ax.set_xticklabels(
    [i for i in range(x_min, x_max + 1, 5)],
    fontdict={'fontsize': 11, 'fontweight': 'bold'}
)

ax.set_yticks([i for i in range(y_min, y_max + 1, 5)])
ax.set_yticks([i for i in range(y_min, y_max + 1, 1)], minor=True)

ax.set_yticklabels(
    [i for i in range(y_min, y_max + 1, 5)],
    fontdict={'fontsize': 11, 'fontweight': 'bold'}
)

ax.tick_params(
    direction='in',
    length=8,
    width=1,
    colors='k',
    grid_color='k',
    grid_alpha=0.5,
    bottom=True,
    top=True,
    left=True,
    right=True
)

ax.tick_params(
    direction='in',
    length=3,
    width=1,
    colors='k',
    grid_color='k',
    grid_alpha=0.5,
    which='minor',
    bottom=True,
    top=True,
    left=True,
    right=True
)

ax.set_title(
    'Mauna Loa Observatory, Hawaii\nMonthly Average Carbon Dioxide Concentration',
    y=1.05,
    loc='left',
    fontdict={
        'fontsize': 16,
        'fontweight': 'bold',
        'horizontalalignment': 'left'
    }
)

ax.text(
    x_min,
    y_max + 2,
    r'Data from Scripps $\rm{CO_2}$ Program',
    fontdict={'fontsize': 12}
)

ax.text(
    x_min + 20,
    y_max + 2,
    f'Last updated {int(df1["Year"].max())}',
    fontdict={'fontsize': 12}
)

ax.plot(df1['Date'], df1['seasonally adjusted filled'])
ax.scatter(df1['Date'], df1['seasonally adjusted filled'], marker='o', s=5)

plt.show()
