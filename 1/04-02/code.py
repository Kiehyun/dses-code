# 지구과학 데이터 사이언스 1 | IV-02. 킬링 곡선 그리기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 22.
import matplotlib.pyplot as plt

# 건조 공기의 구성 성분과 부피비(%)
labels = ['질소 (N₂)', '산소 (O₂)', '아르곤 (Ar)', '이산화탄소 (CO₂)', '기타']
sizes = [78.084, 20.946, 0.934, 0.040, 0.001]  # 기타: 나머지 성분의 대략적 합
colors = ['mediumpurple', 'skyblue', 'gold', 'tomato', 'lightgrey']

fig, ax = plt.subplots(figsize=(7.5, 3.6))
wedges, _ = ax.pie(sizes, colors=colors, startangle=90, counterclock=False,
                   wedgeprops={'edgecolor': 'white', 'linewidth': 1})
ax.text(0.15, 0.25, '질소\n78.1 %', ha='center', fontsize=11)      # 큰 조각만 안에 쓴다
ax.text(-0.5, 0.45, '산소\n20.9 %', ha='center', fontsize=10)
ax.axis('equal')  # 원이 찌그러지지 않게

# 작은 성분은 겹치지 않게 범례로
ax.legend(wedges, [f'{n}: {s:.3f} %' for n, s in zip(labels, sizes)],
          title='부피비', loc='upper left', bbox_to_anchor=(1.0, 1.0), fontsize=9, frameon=False)
others_text = ("기타 성분(ppm)\n"
               "네온(Ne) 18.2 · 헬륨(He) 5.24\n"
               "메탄(CH₄) 1.5 · 크립톤(Kr) 1.14\n"
               "수소(H₂) 0.5")
ax.text(1.12, -0.95, others_text, fontsize=8.5, va='bottom', ha='left',
        bbox=dict(facecolor='white', edgecolor='lightgray'))
ax.set_title('대기의 구성 성분 (건조 공기)', fontsize=13)
plt.tight_layout()
plt.show()

# %% code 23.
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.ticker as mticker

# 관측소 (경도, 위도, 이름)
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

ax.add_feature(cfeature.LAND, color='lightgray')
ax.add_feature(cfeature.OCEAN, color='lightblue')
ax.add_feature(cfeature.COASTLINE)

# 경위도 격자선과 눈금(30° 간격)
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='gray', alpha=0.5, linestyle='--')

gl.top_labels = False
gl.right_labels = False
gl.xlines = True
gl.ylines = True

gl.xlocator = mticker.FixedLocator(range(-180, 181, 30))
gl.ylocator = mticker.FixedLocator(range(-90, 91, 30))

gl.xformatter = LongitudeFormatter()
gl.yformatter = LatitudeFormatter()

gl.xlabel_style = {'size': 8}
gl.ylabel_style = {'size': 8}

# 이름을 점 왼쪽에 쓸 관측소(겹침 방지)
left_label_stations = ['MAUNA LOA', 'FANNING ISLAND', 'LA JOLLA PIER']

for lon, lat, name in stations:
    if name == 'MAUNA LOA':
        continue  # 아래에서 따로 강조
    ax.plot(lon, lat, 'ko', markersize=5, transform=ccrs.PlateCarree())
    if name in left_label_stations:
        ax.text(lon - 5, lat, name, fontsize=8, ha='right', transform=ccrs.PlateCarree())
    else:
        ax.text(lon + 3, lat, name, fontsize=8, ha='left', transform=ccrs.PlateCarree())

# 마우나로아는 빨간 점과 빨간 글씨로 강조
ax.plot(-155.58, 19.54, 'ro', markersize=6, transform=ccrs.PlateCarree())
ax.text(-155.58 - 5, 19.54, 'MAUNA LOA', color='red', fontsize=9, fontweight='bold',
        ha='right', transform=ccrs.PlateCarree())

plt.title('대기 관측소 분포 (태평양 중심 지도)', fontsize=12)
plt.tight_layout()
plt.show()

# %% code 24.
from pathlib import Path

fname = "monthly_in_situ_co2_mlo.csv"

# 스크립스 CO₂ 프로그램에서 직접 내려받기
url = "https://keelinglabsites.ucsd.edu/websitedataco2/monthly_in_situ_co2_mlo.csv"
du.download(url, Path(proj_dir) / fname)

# %% code 25.
fpaths = du.list_files(proj_dir, "csv")

# %% code 26.
n_lines = 70  # 출력할 줄 수

print(f"파일 내용 출력 (처음 {n_lines}줄):")
print("="*40)

try:
    with open(fpaths[0], encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= n_lines:
                break
            print(f"{i+1:3d}: {line.rstrip()}")
except UnicodeDecodeError:
    # UTF-8로 못 읽으면 CP949로 다시 시도
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

df = pd.read_csv(str(fpaths[0]),
                 thousands = ',',
                 skiprows=64,  # 앞쪽 설명문 64줄 건너뛰기
                 names = ['Year',
                          'Month',
                          'Date Excel',           # 엑셀 날짜 일련번호
                          'Date',                 # 십진 연도
                          'CO2',                  # 월평균 CO₂ 농도(ppm)
                          'seasonally adjusted',  # 계절 변동 제거
                          'fit',                  # 맞춤 곡선
                          'seasonally adjusted fit',
                          'CO2 filled',  # 결측을 채운 값
                          'seasonally adjusted filled',
                          'Station'],
                 encoding= 'unicode_escape')

df = df[df.CO2 != -99.99]  # -99.99는 결측값
print("df: ", df)

# %% code 29.
# 간단한 방법: 1년을 365.25일로 근사
df['datetime'] = pd.to_datetime(df['Date'], format='%Y') + pd.to_timedelta((df['Date'] % 1) * 365.25, unit='D')

# 윤년을 고려한 변환(NumPy 벡터 연산)
import numpy as np

def decimal_year_to_datetime_vectorized(decimal_years):
    years = decimal_years.astype(int)
    fractions = decimal_years - years

    start_dates = pd.to_datetime(years, format='%Y')  # 그해 1월 1일

    is_leap = ((years % 4 == 0) & (years % 100 != 0)) | (years % 400 == 0)
    days_in_year = np.where(is_leap, 366, 365)

    days_to_add = (fractions * days_in_year).astype(int)

    return start_dates + pd.to_timedelta(days_to_add, unit='D')

df['datetime'] = decimal_year_to_datetime_vectorized(df['Date'])

print(df[['Date', 'datetime']])

# %% code 30.
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10.5,8))

ax.plot(df['Date'], df['CO2'])

ax.set_xlim(min(df['Date']), max(df['Date']))
ax.set_ylim(min(df['CO2']), max(df['CO2']))

# 축 제목에 LaTeX 수식
ax.set_ylabel(r'$\rm{CO_2}$ Concentration ($\rm{ppm}$)')
ax.set_xlabel(r'Year')

ax.set_title('Mauna Loa Observatory, Hawaii \nMonthly Average Carbon Dioxide Concentration',
             fontdict={'fontsize':16})
plt.show()

# %% code 31.
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10.5,8))

ax.plot(df['datetime'], df['CO2'])  # x축을 datetime으로

ax.set_xlim(min(df['datetime']), max(df['datetime']))
ax.set_ylim(min(df['CO2']), max(df['CO2']))

ax.set_ylabel(r'$\rm{CO_2}$ Concentration ($\rm{ppm}$)')
ax.set_xlabel(r'Year')

ax.set_title('Mauna Loa Observatory, Hawaii \nMonthly Average Carbon Dioxide Concentration',
             fontdict={'fontsize':16})
plt.show()

# %% code 32.
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10.5, 8))

ax.plot(df['Date'], df['CO2'])
ax.scatter(df['Date'], df['CO2'], marker='o', s=5)

ax.set_xlim(min(df['Date']), max(df['Date']))
ax.set_ylim(min(df['CO2']), max(df['CO2']))

ax.set_ylabel(r'$\rm{CO_2}$ Concentration ($\rm{ppm}$)', fontdict={'fontsize':16, 'fontweight':'bold'})
ax.set_xlabel(r'Year', fontdict={'fontsize':16, 'fontweight':'bold'})

# x축 눈금: 큰 눈금 5년, 작은 눈금 1년
ax.set_xticks([i for i in range(1960, 2026, 5)])
ax.set_xticks([i for i in range(1960, 2026, 1)], minor=True)
ax.set_xticklabels([i for i in range(1960, 2026, 5)], fontdict={'fontsize':11, 'fontweight':'bold'})

# y축 눈금: 큰 눈금 5 ppm, 작은 눈금 1 ppm
ax.set_yticks([i for i in range(310, 421, 5)])
ax.set_yticks([i for i in range(310, 421, 1)], minor=True)
ax.set_yticklabels([i for i in range(310, 421, 5)], fontdict={'fontsize':11, 'fontweight':'bold'})
ax.set_yticklabels(sum([[i, ''] for i in [i for i in range(310, 421, 10)]], [])[:-1])  # 10 ppm마다만 숫자

# 눈금을 안쪽으로, 네 변 모두에
ax.tick_params(direction='in', length=8, width=1, colors='k',
               grid_color='k', grid_alpha=0.5,
               bottom=True, top=True, left=True, right=True)
ax.tick_params(direction='in', length=3, width=1, colors='k',
               grid_color='k', grid_alpha=0.5, which = 'minor',
               bottom=True, top=True, left=True, right=True)

ax.set_title('Mauna Loa Observatory, Hawaii \nMonthly Average Carbon Dioxide Concentration',
             y=1.05,  # 제목 아래 여백
             loc = 'left',
             fontdict={'fontsize':16, 'fontweight':'bold', 'horizontalalignment': 'left'})

# 그래프 위 작은 글씨(자료 출처)
ax.text(1958, 422, r'Data from Scripps $\rm{CO_2}$ Program',
             fontdict={'fontsize':12})
ax.text(1985, 422, r'Last updated June 2021', fontdict={'fontsize':12})

plt.show()

# %% code 33.
import numpy as np
import matplotlib.pyplot as plt

co2 = df[['Date', 'CO2', 'seasonally adjusted', 'fit']].replace(-99.99, np.nan)
recent = co2[co2['Date'] >= co2['Date'].max() - 4]  # 최근 4년
styles = {'CO2': dict(label='관측값', lw=0.8, marker='o', ms=2),
          'seasonally adjusted': dict(label='계절 변동 제거', lw=2),
          'fit': dict(label='맞춤 곡선', lw=1, ls='--', color='k')}

fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.5))
for ax, d, title in zip(axes, [co2, recent], ['전체 기간', '최근 4년']):
    for col, kw in styles.items():
        ax.plot(d['Date'], d[col], **kw)
    ax.set_title(title)
    ax.set_xlabel('Year')
    ax.grid(alpha=0.3)
axes[0].set_ylabel(r'$\rm{CO_2}$ Concentration ($\rm{ppm}$)')
axes[1].legend()
plt.tight_layout()
plt.show()

# %% code 34.
# 계절 성분 = 관측값 - 계절 변동 제거 값
seasonal = co2['CO2'] - co2['seasonally adjusted']
cycle = seasonal.groupby(df['Month']).mean()
print(cycle.round(2).to_string())
print(f"가장 높은 달: {cycle.idxmax()}월, 가장 낮은 달: {cycle.idxmin()}월, "
      f"진폭: {cycle.max() - cycle.min():.1f}ppm")

# %% code 35.
# 12달이 모두 있는 해만 연평균
annual = df.groupby('Year')['CO2'].agg(['mean', 'count'])
annual = annual.loc[annual['count'] == 12, 'mean']
growth = (annual.diff() / annual.index.to_series().diff()).dropna()  # ppm/년

rate = growth.groupby(growth.index // 10 * 10).mean()  # 10년 단위 평균
for decade, r in rate.items():
    print(f'{decade}년대: {r:.2f}ppm/년')

fig, ax = plt.subplots(figsize=(7.5, 3.6))
ax.bar([f'{d}년대' for d in rate.index], rate.values, color='tomato')
for x, r in enumerate(rate.values):
    ax.text(x, r + 0.05, f'{r:.2f}', ha='center', fontsize=9)
ax.set_ylabel('연평균 증가율 (ppm/년)')
ax.set_title('마우나로아 CO₂ 농도의 10년 단위 증가율')
plt.tight_layout()
plt.show()

# %% code 36.
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10.5, 8))
ax.set_xlim(min(df['Date']), max(df['Date']))
ax.set_ylim(min(df['CO2']), max(df['CO2']))

ax.set_xlabel('Year', fontsize=16, fontweight='bold')
ax.set_ylabel(r'$\rm{CO_2}$ Concentration ($\rm{ppm}$)', fontsize=16, fontweight='bold')

ax.set_xticks(range(1960, 2026, 5))
ax.set_xticks(range(1960, 2026, 1), minor=True)
ax.set_yticks(range(310, 421, 5))
ax.set_yticks(range(310, 421, 1), minor=True)

ax.tick_params(direction='in', length=8, width=1, colors='k', which='major')
ax.tick_params(direction='in', length=3, width=1, colors='k', which='minor')

ax.set_title('Mauna Loa Observatory, Hawaii\nMonthly Average CO₂ Concentration',
             loc='left', y=1.05, fontsize=16, fontweight='bold')
ax.text(1958, 422, 'Data from Scripps CO₂ Program', fontsize=12)
ax.text(1985, 422, 'Last updated June 2021', fontsize=12)

# 첫 자료점만 그려 두고 애니메이션에서 갱신
line, = ax.plot(df['Date'].iloc[0], df['CO2'].iloc[0])
point = ax.scatter(df['Date'].iloc[0], df['CO2'].iloc[0], s=5)

# %% code 37.
def animate(i):
    line.set_data(df['Date'].iloc[:i], df['CO2'].iloc[:i])  # i번째까지 선으로
    point.set_offsets([df['Date'].iloc[i], df['CO2'].iloc[i]])  # 현재 점
    return line, point

from matplotlib.animation import FuncAnimation
ani = FuncAnimation(fig, animate, frames=len(df['Date']), blit=True)

from IPython.display import HTML

# 환경에 따라 표시 방법을 차례로 시도
try:
    HTML(ani.to_jshtml())
except:
    import matplotlib
    matplotlib.rcParams['animation.html'] = 'html5'
    try:
        HTML(ani.to_html5_video())
    except:
        from matplotlib import rc
        rc('animation', html='jshtml')
        ani

HTML(ani.to_jshtml())

# %% code 38.
fname = 'Keeling_curve_MLO'

# MP4로 저장, 실패하면 GIF, 그다음 HTML
try:
    ani.save(f'{proj_dir}/{fname}.mp4', fps=60, dpi=150, writer='ffmpeg')
    print(f"동영상이 저장되었습니다: {proj_dir}/{fname}.mp4")
except Exception as e:
    print(f"MP4 저장 중 오류 발생: {e}")

    try:
        ani.save(f'{proj_dir}/{fname}.gif', fps=30, dpi=100, writer='pillow')
        print(f"GIF 파일이 저장되었습니다: {proj_dir}/{fname}.gif")
    except Exception as e2:
        print(f"GIF 저장 중 오류 발생: {e2}")

        try:
            with open(f'{proj_dir}/{fname}.html', 'w') as f:
                f.write(ani.to_jshtml())
            print(f"HTML 파일이 저장되었습니다: {proj_dir}/{fname}.html")
        except Exception as e3:
            print(f"HTML 저장 중 오류 발생: {e3}")

# %% code 39.
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO

url = "https://keelinglabsites.ucsd.edu/websitedataco2/monthly_in_situ_co2_mlo.csv"

# 1) 최신 자료를 내려받아 데이터 행만 고르기
response = requests.get(url)
response.raise_for_status()

lines = response.text.splitlines()

data_lines = [line for line in lines if re.match(r'^\s*\d{4}\s*,', line) ]  # 연도(네 자리)로 시작하는 행

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

# 2) 숫자로 바꾸고 결측 표시(-99.99, -999)는 NaN으로
numeric_columns = [
    'CO2', 'seasonally adjusted', 'fit', 'seasonally adjusted fit',
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

# 3) 시간 간격에 맞춘 보간(양 끝 바깥은 채우지 않음)
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

# 4) 축 범위를 10 단위로 내림
x_min = int(df1['Date'].min() // 10 * 10)
x_max = int(df1['Date'].max() // 10 * 10)

y_min = int(df1['seasonally adjusted filled'].min() // 10 * 10)
y_max = int(df1['seasonally adjusted filled'].max() // 10 * 10)

# 5) 그리기(앞의 킬링 곡선과 같은 꾸밈)
fig, ax = plt.subplots(figsize=(10.5, 8))

ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

ax.set_ylabel(
    r'$\rm{CO_2}$ Concentration ($\rm{ppm}$)',
    fontdict={'fontsize': 16, 'fontweight': 'bold'}
)

ax.set_xlabel(r'Year', fontdict={'fontsize': 16, 'fontweight': 'bold'})

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
    direction='in', length=8, width=1, colors='k', grid_color='k',
    grid_alpha=0.5, bottom=True, top=True, left=True, right=True
)

ax.tick_params(
    direction='in', length=3, width=1, colors='k', grid_color='k',
    grid_alpha=0.5, which='minor', bottom=True, top=True, left=True,
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
    x_min, y_max + 2, r'Data from Scripps $\rm{CO_2}$ Program',
    fontdict={'fontsize': 12}
)

ax.text(
    x_min + 20, y_max + 2, f'Last updated {int(df1["Year"].max())}',
    fontdict={'fontsize': 12}
)

ax.plot(df1['Date'], df1['seasonally adjusted filled'])
ax.scatter(df1['Date'], df1['seasonally adjusted filled'], marker='o', s=5)

plt.show()
