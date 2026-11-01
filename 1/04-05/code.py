# 지구과학 데이터 사이언스 1 | IV-05. 해수면의 높이 변동 그래프
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 83.
# 파일 이름과 ID 정의
from pathlib import Path

files = [

    {"name": "[1MinTide]202006_DT_0001.txt", "id": "1l_L631Y-pMMdIqzPpgYMuPBi4w6RNT9c"},
    {"name": "[10MinTide]202006_DT_0001.txt", "id": "1UPJrhqldAm0iAc-B0VghFe9Hv3SImaLs"},
    {"name": "[60MinTide]202006_DT_0001.txt", "id": "1MD_2mXr_2johjIiozdqnNOq1P1jXeOTd"}
]

# 반복문으로 파일 내려받기
for file in files:
    du.download(f"https://docs.google.com/uc?export=download&id={file['id']}", Path(proj_dir) / file['name'])

# %% code 84.
fpaths = du.list_files(proj_dir, "txt")

# %% code 85.
du.preview_text(fpaths[0], n=10)

# %% code 86.
import pandas as pd
print("str(fpaths[2])", str(fpaths[2]))
df_60min = pd.read_csv(str(fpaths[2]),
                 skiprows=5,
                 thousands = ',',
                 names = ['str_YmdHM', 'height(cm)'],
                 encoding= 'unicode_escape',
 #encoding= 'utf8',
                 )
print("df_60min :", df_60min )

# %% code 87.
print("df_60min.columns :", df_60min.columns )
print("type(df_60min['str_YmdHM'][0]): {}".format(type(df_60min['str_YmdHM'][0])))
print("type(df_60min['height(cm)']): {}".format(type(df_60min['height(cm)'][0])))
df_60min['dt_YmdHM'] = pd.to_datetime(df_60min['str_YmdHM'])
df_60min.index = df_60min['dt_YmdHM']
print("df_60min: ", df_60min)

# %% code 88.
# df_60min['dt_YmdHM'] 컬럼이 오름차순으로 정렬되어 있는지 확인
is_sorted = df_60min['dt_YmdHM'].is_monotonic_increasing
print("dt_YmdHM 오름차순 정렬 여부:", is_sorted)

# df_60min['height(cm)']에 결측치가 있는지 확인
num_missing = df_60min['height(cm)'].isnull().sum()
print("height(cm) 결측치 개수:", num_missing)

# df_60min['dt_YmdHM'] 컬럼이 인덱스와 컬럼에 모두 있을 때 정렬 오류 방지
if 'dt_YmdHM' in df_60min.index.names:
 # 인덱스가 dt_YmdHM이면 인덱스 기준으로 정렬
    df_60min = df_60min.sort_index()
else:
 # 아니면 컬럼 기준으로 정렬
    df_60min = df_60min.sort_values(by='dt_YmdHM')

# 결측치 보간 (선형 보간)
df_60min = df_60min.interpolate(method='linear')

# 결측치가 남아있는 경우(양 끝 등)는 앞/뒤 값으로 채움
df_60min = df_60min.fillna(method='bfill').fillna(method='ffill')

# %% code 89.
# 10분 간격 데이터 (fpaths[0]) DataFrame 생성 및 정렬/결측치 처리
df_10min = pd.read_csv(
    str(fpaths[0]),
    skiprows=5,
    thousands=',',
    names=['str_YmdHM', 'height(cm)'],
    encoding='unicode_escape'
)
df_10min['dt_YmdHM'] = pd.to_datetime(df_10min['str_YmdHM'])
df_10min.index = df_10min['dt_YmdHM']
# 정렬
df_10min = df_10min.sort_index()
# 결측치 보간 및 처리
df_10min = df_10min.interpolate(method='linear')
df_10min = df_10min.fillna(method='bfill').fillna(method='ffill')
print("df_10min :", df_10min)

# 1분 간격 데이터 (fpaths[1]) DataFrame 생성 및 정렬/결측치 처리
df_1min = pd.read_csv(
    str(fpaths[1]),
    skiprows=5,
    thousands=',',
    names=['str_YmdHM', 'height(cm)'],
    encoding='unicode_escape'
)
df_1min['dt_YmdHM'] = pd.to_datetime(df_1min['str_YmdHM'])
df_1min.index = df_1min['dt_YmdHM']
# 정렬
df_1min = df_1min.sort_index()
# 결측치 보간 및 처리
df_1min = df_1min.interpolate(method='linear')
df_1min = df_1min.fillna(method='bfill').fillna(method='ffill')
print("df_1min :", df_1min)

# %% code 90.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime, timedelta

# 데이터프레임 df_60min 시각화
fig, ax = plt.subplots(figsize=(15,5))
ax.plot(df_60min['dt_YmdHM'], df_60min['height(cm)'], color='royalblue', label='해수면 높이')
ax.set_title('2020년 6월 인천 해수면 높이 변동(1시간 간격 자료)', 
           fontsize=18, fontweight='bold')
ax.set_xlabel('시간', fontsize=14)
ax.set_ylabel('해수면 높이 (cm)', fontsize=14)
ax.legend(fontsize=12)
ax.grid(True, linestyle=':', alpha=0.5)

plt.tight_layout()
plt.show()

# %% code 91.
import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as ticker

# 데이터프레임 리스트와 타이틀
dfs = [df_60min, df_10min, df_1min]
titles = ['1시간 간격 자료', '10분 간격 자료', '1분 간격 자료']

fig, axes = plt.subplots(3, 1, figsize=(16, 16), sharey=True)

for i, (df, title) in enumerate(zip(dfs, titles)):
    ax = axes[i]
    ax.plot(df['dt_YmdHM'], df['height(cm)'], color='royalblue', label='해수면 높이')

    ax.xaxis.set_major_locator(dates.DayLocator())
    ax.xaxis.set_minor_locator(dates.DayLocator())
    ax.xaxis.set_major_formatter(ticker.NullFormatter())
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%d'))

    ax.set_ylim(-200, 1000)
    ax.set_yticks(np.arange(-200, 1001, 100), minor=True)
    ax.set_xlim(min(df['dt_YmdHM']), max(df['dt_YmdHM']))
    ax.set_xticks(np.arange(min(df['dt_YmdHM']), max(df['dt_YmdHM']), 
        timedelta(days=0.5)), minor=True)

    ax.tick_params(axis="x", direction="in", length=8, width=2, 
        color="turquoise", which='major', labelsize=12)
    ax.tick_params(axis="y", direction="in", length=6, width=2, 
        color="orange", which='major', labelsize=10)
    ax.tick_params(axis="x", direction="out", length=2, width=2, 
        color="turquoise", which='minor', labelsize=12)
    ax.tick_params(axis="y", direction="out", length=2, width=2, 
        color="orange", which='minor', labelsize=10)

    ax.grid(axis="x", color="green", alpha=.3, linewidth=.8, linestyle=":")
    ax.grid(axis="y", color="black", alpha=.3, linewidth=.8, linestyle=":")

    ax.set_xlabel('time (day)', fontsize=14)
    if i == 0:
        ax.set_ylabel('height of sea level (cm)', fontsize=14)
    ax.set_title(title, fontsize=16, fontweight='bold', y=1.02)

fig.suptitle('2020년 6월 인천 해수면 높이 변동 (1시간/10분/1분)', 
            fontsize=20, fontweight='bold', y=0.98)
fig.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()

# %% code 92.
# df_1min에서 7일, 8일, 9일 자료만 슬라이싱
start_date = df_1min['dt_YmdHM'].dt.floor('D').min().replace(day=7)
end_date = df_1min['dt_YmdHM'].dt.floor('D').min().replace(day=10)
df_1min_selected = df_1min[(df_1min['dt_YmdHM'] >= start_date) & (df_1min['dt_YmdHM'] < end_date)]

# 날짜별로 분리
dfs = []
titles = []
for day in range(7, 10):
    day_start = start_date.replace(day=day)
    day_end = start_date.replace(day=day+1)
    dfs.append(df_1min[(df_1min['dt_YmdHM'] >= day_start) & (df_1min['dt_YmdHM'] < day_end)])
    titles.append(f'2020년 6월 {day}일')

# 3행 1열로 시각화
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as ticker
import numpy as np

fig, axes = plt.subplots(3, 1, figsize=(12.0, 9.0), sharey=True)

for i, (df, title) in enumerate(zip(dfs, titles)):
    ax = axes[i]
    ax.plot(df['dt_YmdHM'], df['height(cm)'], color='royalblue')
    ax.xaxis.set_major_locator(dates.HourLocator(interval=2))
    ax.xaxis.set_minor_locator(dates.HourLocator())
    ax.xaxis.set_major_formatter(dates.DateFormatter('%H시'))
    ax.set_ylim(-200, 1000)
    ax.set_yticks(np.arange(-200, 1001, 100), minor=True)
    ax.set_xlim(df['dt_YmdHM'].min(), df['dt_YmdHM'].max())
    ax.grid(axis="x", color="green", alpha=.3, linewidth=.8, linestyle=":")
    ax.grid(axis="y", color="black", alpha=.3, linewidth=.8, linestyle=":")
    ax.set_xlabel('시간', fontsize=14)
    if i == 0:
        ax.set_ylabel('해수면 높이 (cm)', fontsize=14)
    ax.set_title(title, fontsize=16, fontweight='bold', y=1.02)

fig.suptitle('2020년 6월 7~9일 인천 해수면 높이 변동 (1분 간격)', fontsize=20, fontweight='bold', y=0.985)
fig.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()

# %% code 93.
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 하루치(1440분)씩 30일 분할
days = []
date_labels = []
start_day = df_1min['dt_YmdHM'].dt.floor('D').min()
for i in range(30):
    day_start = start_day + pd.Timedelta(days=i)
    day_end = day_start + pd.Timedelta(days=1)
    day_data = df_1min[(df_1min['dt_YmdHM'] >= day_start) & (df_1min['dt_YmdHM'] < day_end)]['height(cm)'].values
 # 길이가 1440이 아닐 경우 NaN으로 패딩
    if len(day_data) < 1440:
        day_data = np.pad(day_data, (0, 1440 - len(day_data)), constant_values=np.nan)
    days.append(day_data)
    date_labels.append(day_start.strftime('%d'))  # '06-01', '06-02', ...

# 2D array (30일 x 1440분)
height_matrix = np.array(days)

plt.figure(figsize=(10, 10))
xticks = np.arange(0, 1441, 60)
xticklabels = [f"{h:02d}" for h in range(25)]  # 0~24시

sns.heatmap(
    height_matrix,
    cmap='viridis',
    cbar_kws={'label': '해수면 높이 (cm)'},
    xticklabels=False,
    yticklabels=date_labels
)
plt.xticks(ticks=xticks, labels=xticklabels, rotation=0)
plt.yticks(rotation=0)
plt.xlabel('시(hour)')
plt.ylabel('날짜 (6월)')
plt.title('2020년 6월 인천 해수면 높이(1분 간격) 히트맵')
plt.tight_layout()
