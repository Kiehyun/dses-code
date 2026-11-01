# 지구과학 데이터 사이언스 1 | IV-05. 해수면의 높이 변동 그래프
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 81.
# 스마트 조석예보 자료 내려받기 주소와 조건(지점 코드, 지점 이름, 연월)
from pathlib import Path
from urllib.parse import urlencode

BASE_URL = "https://www.khoa.go.kr/swtc/getDownTideData.do"
OBS_ID, OBS_NAME, YYYYMM = "DT_0001", "인천", "202006"

for interval in [1, 10, 60]:  # 1분 · 10분 · 60분 간격
    params = urlencode({"obsPostId": OBS_ID, "date": YYYYMM,
                        "timeInterval": interval, "obsPostName": OBS_NAME})
    fname = f"[{interval}MinTide]{YYYYMM}_{OBS_ID}.txt"
    du.download(f"{BASE_URL}?{params}", Path(proj_dir) / fname)

# %% code 82.
fpaths = du.list_files(proj_dir, "txt")

# %% code 83.
du.preview_text(fpaths[0], n=10)

# %% code 84.
import pandas as pd
# 이름순 정렬이라 fpaths[0]은 10분, [1]은 1분, [2]는 60분 간격
print("str(fpaths[2])", str(fpaths[2]))
df_60min = pd.read_csv(str(fpaths[2]),
                 skiprows=5,  # 머리글 5줄 건너뛰기
                 thousands = ',',
                 names = ['str_YmdHM', 'height(cm)'],
                 encoding= 'unicode_escape',
                 )
print("df_60min :", df_60min )

# %% code 85.
print("df_60min.columns :", df_60min.columns )
print("type(df_60min['str_YmdHM'][0]): {}".format(type(df_60min['str_YmdHM'][0])))
print("type(df_60min['height(cm)']): {}".format(type(df_60min['height(cm)'][0])))
df_60min['dt_YmdHM'] = pd.to_datetime(df_60min['str_YmdHM'])
df_60min.index = df_60min['dt_YmdHM']
print("df_60min: ", df_60min)

# %% code 86.
# 시각이 오름차순인지 확인
is_sorted = df_60min['dt_YmdHM'].is_monotonic_increasing
print("dt_YmdHM 오름차순 정렬 여부:", is_sorted)

num_missing = df_60min['height(cm)'].isnull().sum()
print("height(cm) 결측치 개수:", num_missing)

# dt_YmdHM이 인덱스이자 열이므로 정렬 기준을 골라 오류 방지
if 'dt_YmdHM' in df_60min.index.names:
    df_60min = df_60min.sort_index()
else:
    df_60min = df_60min.sort_values(by='dt_YmdHM')

df_60min = df_60min.interpolate(method='linear')  # 결측은 선형 보간

# 양 끝처럼 보간이 안 되는 결측은 앞뒤 값으로
df_60min = df_60min.fillna(method='bfill').fillna(method='ffill')

# %% code 87.
# 10분 간격 자료: 읽기 → 정렬 → 결측 처리
df_10min = pd.read_csv(
    str(fpaths[0]), skiprows=5, thousands=',',
    names=['str_YmdHM', 'height(cm)'], encoding='unicode_escape'
)
df_10min['dt_YmdHM'] = pd.to_datetime(df_10min['str_YmdHM'])
df_10min.index = df_10min['dt_YmdHM']
df_10min = df_10min.sort_index()
df_10min = df_10min.interpolate(method='linear')
df_10min = df_10min.fillna(method='bfill').fillna(method='ffill')
print("df_10min :", df_10min)

# 1분 간격 자료도 같은 방법으로
df_1min = pd.read_csv(
    str(fpaths[1]), skiprows=5, thousands=',',
    names=['str_YmdHM', 'height(cm)'], encoding='unicode_escape'
)
df_1min['dt_YmdHM'] = pd.to_datetime(df_1min['str_YmdHM'])
df_1min.index = df_1min['dt_YmdHM']
df_1min = df_1min.sort_index()
df_1min = df_1min.interpolate(method='linear')
df_1min = df_1min.fillna(method='bfill').fillna(method='ffill')
print("df_1min :", df_1min)

# %% code 88.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime, timedelta

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

# %% code 89.
import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as ticker

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
        timedelta(days=0.5)), minor=True)  # 12시간 간격 작은 눈금

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

# %% code 90.
# 6월 7~9일 자료만
start_date = df_1min['dt_YmdHM'].dt.floor('D').min().replace(day=7)
end_date = df_1min['dt_YmdHM'].dt.floor('D').min().replace(day=10)
df_1min_selected = df_1min[(df_1min['dt_YmdHM'] >= start_date) & (df_1min['dt_YmdHM'] < end_date)]

# 하루씩 나누기
dfs = []
titles = []
for day in range(7, 10):
    day_start = start_date.replace(day=day)
    day_end = start_date.replace(day=day+1)
    dfs.append(df_1min[(df_1min['dt_YmdHM'] >= day_start) & (df_1min['dt_YmdHM'] < day_end)])
    titles.append(f'2020년 6월 {day}일')

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

# %% code 91.
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 하루치(1440분)씩 30일로 나누기
days = []
date_labels = []
start_day = df_1min['dt_YmdHM'].dt.floor('D').min()
for i in range(30):
    day_start = start_day + pd.Timedelta(days=i)
    day_end = day_start + pd.Timedelta(days=1)
    day_data = df_1min[(df_1min['dt_YmdHM'] >= day_start) & (df_1min['dt_YmdHM'] < day_end)]['height(cm)'].values
    # 1440개보다 적으면 뒤를 NaN으로 채우기
    if len(day_data) < 1440:
        day_data = np.pad(day_data, (0, 1440 - len(day_data)), constant_values=np.nan)
    days.append(day_data)
    date_labels.append(day_start.strftime('%d'))  # '01', '02', ...

height_matrix = np.array(days)  # 30일 × 1440분

plt.figure(figsize=(10, 10))
xticks = np.arange(0, 1441, 60)
xticklabels = [f"{h:02d}" for h in range(25)]  # 0~24시

sns.heatmap(
    height_matrix, cmap='viridis', cbar_kws={'label': '해수면 높이 (cm)'},
    xticklabels=False, yticklabels=date_labels
)
plt.xticks(ticks=xticks, labels=xticklabels, rotation=0)
plt.yticks(rotation=0)
plt.xlabel('시(hour)')
plt.ylabel('날짜 (6월)')
plt.title('2020년 6월 인천 해수면 높이(1분 간격) 히트맵')
plt.tight_layout()

# %% code 92.
# 2024년 1~12월 60분 간격 자료를 달마다 내려받기
year_dir = Path(proj_dir) / "2024"
for month in range(1, 13):
    yyyymm = f"2024{month:02d}"
    params = urlencode({"obsPostId": OBS_ID, "date": yyyymm,
                        "timeInterval": 60, "obsPostName": OBS_NAME})
    du.download(f"{BASE_URL}?{params}", year_dir / f"[60MinTide]{yyyymm}_{OBS_ID}.txt")

# %% code 93.
# 12개 파일을 이어 붙이고 시간순 정렬, 결측 보간
fpaths_2024 = du.list_files(year_dir, "txt", show=False)
df_year = pd.concat([pd.read_csv(f, skiprows=5, thousands=',',
                                 names=['str_YmdHM', 'height(cm)'],
                                 encoding='unicode_escape')
                     for f in fpaths_2024])
df_year.index = pd.to_datetime(df_year['str_YmdHM'])
df_year = df_year.sort_index()
h = pd.to_numeric(df_year['height(cm)'], errors='coerce')
n_missing = h.isna().sum()
df_year['height(cm)'] = h.interpolate().bfill().ffill()

h = df_year['height(cm)']
print(f"파일 {len(fpaths_2024)}개, 데이터 {len(h):,}개, 결측값 {n_missing}개")
print(f"기간: {h.index[0]} ~ {h.index[-1]}")
print(f"평균 {h.mean():.1f}cm, 최고 {h.max():.0f}cm({h.idxmax():%m월 %d일 %H시}), "
      f"최저 {h.min():.0f}cm({h.idxmin():%m월 %d일 %H시})")

# %% code 94.
import matplotlib.dates as dates

fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(df_year.index, df_year['height(cm)'], color='royalblue', linewidth=0.5)
ax.xaxis.set_major_locator(dates.MonthLocator())
ax.xaxis.set_major_formatter(dates.DateFormatter('%m월'))
ax.set_xlim(df_year.index[0], df_year.index[-1])
ax.set_title('2024년 인천 해수면 높이 변동(1시간 간격)', fontsize=18, fontweight='bold')
ax.set_xlabel('월', fontsize=14)
ax.set_ylabel('해수면 높이 (cm)', fontsize=14)
ax.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
plt.show()

# %% code 95.
# 월별 평균과 표준편차
monthly = df_year.groupby(df_year.index.month)['height(cm)'].agg(['mean', 'std'])

fig, axes = plt.subplots(1, 2, figsize=(15, 5))
axes[0].plot(monthly.index, monthly['mean'], marker='o', color='navy', linewidth=2)
axes[0].set_title('월별 평균 해수면 높이', fontsize=16, fontweight='bold')
axes[0].set_ylabel('평균 높이 (cm)', fontsize=13)
axes[1].plot(monthly.index, monthly['std'], marker='o', color='seagreen', linewidth=2)
axes[1].set_title('월별 해수면 높이의 표준편차', fontsize=16, fontweight='bold')
axes[1].set_ylabel('표준편차 (cm)', fontsize=13)
for ax in axes:
    ax.set_xticks(range(1, 13))
    ax.set_xlabel('월', fontsize=13)
    ax.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
plt.show()

monthly.columns = ['평균(cm)', '표준편차(cm)']
monthly.index.name = '월'
print(monthly.round(1).T.to_string())

# %% code 96.
t_demo = np.arange(0, 24 * 30, 0.1)  # 30일, 0.1시간 간격
m2 = 275 * np.cos(2 * np.pi * t_demo / 12.4206)
s2 = 115 * np.cos(2 * np.pi * t_demo / 12.0)

waves = [m2, s2, m2 + s2]
colors = ['royalblue', 'darkorange', 'seagreen']
titles = ['달이 만드는 M2(주기 12.42시간, 진폭 275cm)',
          '태양이 만드는 S2(주기 12.00시간, 진폭 115cm)',
          'M2 + S2: 약 14.77일마다 커졌다 작아지는 대조와 소조']

fig, axes = plt.subplots(3, 1, figsize=(15, 9), sharex=True, sharey=True)
for ax, wave, color, title in zip(axes, waves, colors, titles):
    ax.plot(t_demo / 24, wave, color=color, linewidth=0.8)
    ax.axhline(0, color='gray', linewidth=0.8)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_ylabel('높이 (cm)', fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.5)
axes[2].set_xlabel('시간 (일)', fontsize=12)
axes[2].set_xticks(range(0, 31, 5))
plt.tight_layout()
plt.show()

# %% code 97.
y = df_year['height(cm)'].to_numpy()
y_dev = y - y.mean()  # 평균 해수면으로부터의 높이

amp_fft = 2 * np.abs(np.fft.rfft(y_dev)) / len(y_dev)
freq = np.fft.rfftfreq(len(y_dev), d=1.0)  # 1시간 간격
period = np.divide(1, freq, out=np.full_like(freq, np.inf), where=freq > 0)

fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(period, amp_fft, color='steelblue', linewidth=1)
view = (period >= 5) & (period <= 30)
ax.set_xlim(5, 30)
ax.set_ylim(0, amp_fft[view].max() * 1.35)

# 주요 분조 위치(이름, 주기, 글자 높이 비율)
marks = [('M2', 12.4206, 1.28), ('S2', 12.0000, 1.10), ('N2', 12.6583, 0.62),
         ('K1', 23.9345, 0.30), ('O1', 25.8193, 0.22), ('M4', 6.2103, 0.12)]
for name, T, y_rel in marks:
    ax.axvline(T, color='crimson', linestyle='--', alpha=0.4, linewidth=1)
    ax.text(T, amp_fft[view].max() * y_rel, f'{name}\n{T:.2f}h', ha='center',
            va='top', fontsize=10, fontweight='bold', color='crimson')

ax.set_title('2024년 인천 조위에 들어 있는 주기 성분', fontsize=17, fontweight='bold')
ax.set_xlabel('주기 (시간)', fontsize=13)
ax.set_ylabel('진폭 (cm)', fontsize=13)
ax.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
plt.show()

# %% code 98.
# 분석할 분조: 이름과 주기(시간), 기원
PERIODS = {'M2': 12.4206012, 'S2': 12.0000000, 'N2': 12.6583475, 'K2': 11.9672348,
           'K1': 23.9344696, 'O1': 25.8193417, 'P1': 24.0658902, 'Q1': 26.8683567,
           'M4': 6.2103006, 'MS4': 6.1032725}
ORIGIN = {'M2': '달', 'S2': '태양', 'N2': '달', 'K2': '달+태양', 'K1': '달+태양',
          'O1': '달', 'P1': '태양', 'Q1': '달', 'M4': '달(천해)', 'MS4': '달+태양(천해)'}

def design_matrix(t, periods):
    """열이 [1, cos(w1 t), sin(w1 t), cos(w2 t), sin(w2 t), ...]인 설계행렬"""
    cols = [np.ones_like(t)]
    for T in periods:
        w = 2 * np.pi / T
        cols += [np.cos(w * t), np.sin(w * t)]
    return np.column_stack(cols)

t = (df_year.index - df_year.index[0]).total_seconds().to_numpy() / 3600
A = design_matrix(t, PERIODS.values())
coef, *_ = np.linalg.lstsq(A, y, rcond=None)

rows = []
for i, (name, T) in enumerate(PERIODS.items()):
    a, b = coef[1 + 2 * i], coef[2 + 2 * i]
    rows.append({'분조': name, '주기(시간)': round(T, 4), '기원': ORIGIN[name],
                 '진폭(cm)': round(float(np.hypot(a, b)), 1),
                 '위상(°)': round(float(np.degrees(np.arctan2(b, a)) % 360), 1)})
tide_table = (pd.DataFrame(rows).sort_values('진폭(cm)', ascending=False)
              .reset_index(drop=True))
print(f"평균 해수면 Z0 = {coef[0]:.1f}cm")
print(tide_table.to_string(index=False))

palette = {'달': 'royalblue', '태양': 'darkorange', '달+태양': 'mediumpurple',
           '달(천해)': 'lightsteelblue', '달+태양(천해)': 'plum'}
fig, ax = plt.subplots(figsize=(11, 5))
ax.bar(tide_table['분조'], tide_table['진폭(cm)'],
       color=[palette[o] for o in tide_table['기원']], edgecolor='black')
for x_i, v in enumerate(tide_table['진폭(cm)']):
    ax.text(x_i, v + 5, f'{v:.0f}', ha='center', fontsize=10)
ax.set_title('분조별 진폭(파랑: 달, 주황: 태양, 보라: 달+태양)', fontsize=15, fontweight='bold')
ax.set_xlabel('분조', fontsize=12)
ax.set_ylabel('진폭 (cm)', fontsize=12)
ax.grid(axis='y', linestyle=':', alpha=0.5)
plt.tight_layout()
plt.show()

# %% code 99.
def synth(names):
    """고른 분조만 더해 되살린 파형"""
    out = np.zeros_like(t)
    for i, (name, T) in enumerate(PERIODS.items()):
        if name in names:
            w = 2 * np.pi / T
            out += coef[1 + 2 * i] * np.cos(w * t) + coef[2 + 2 * i] * np.sin(w * t)
    return out

moon = synth({'M2', 'N2', 'O1', 'Q1'})
sun = synth({'S2', 'P1'})
sel = (df_year.index >= '2024-03-01') & (df_year.index < '2024-04-01')

waves = [moon, sun, moon + sun]
colors = ['royalblue', 'darkorange', 'seagreen']
titles = [f'달이 만드는 조석(M2+N2+O1+Q1), 표준편차 {moon.std():.0f}cm',
          f'태양이 만드는 조석(S2+P1), 표준편차 {sun.std():.0f}cm',
          '달 + 태양: 보름 주기의 대조와 소조']

fig, axes = plt.subplots(3, 1, figsize=(15, 9), sharex=True, sharey=True)
for ax, wave, color, title in zip(axes, waves, colors, titles):
    ax.plot(df_year.index[sel], wave[sel], color=color)
    ax.axhline(0, color='gray', linewidth=0.8)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_ylabel('높이 (cm)', fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.xaxis.set_major_locator(dates.DayLocator(interval=5))
    ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
axes[2].set_xlabel('날짜(2024년 3월)', fontsize=12)
plt.tight_layout()
plt.show()

print(f"달 성분 표준편차 {moon.std():.1f}cm, 태양 성분 표준편차 {sun.std():.1f}cm, "
      f"비 {moon.std() / sun.std():.1f}")

# %% code 100.
fit = A @ coef      # 분조 10개로 되살린 조위
resid = y - fit     # 잔차

fig, axes = plt.subplots(2, 1, figsize=(15, 8), sharex=True)
axes[0].plot(df_year.index[sel], y[sel], color='lightgray', linewidth=3.5, label='실제 데이터')
axes[0].plot(df_year.index[sel], fit[sel], color='crimson', linewidth=1, label='분조 10개로 재구성')
axes[0].set_title('실제 데이터와 조화분석 재구성(2024년 3월)', fontsize=16, fontweight='bold')
axes[0].set_ylabel('해수면 높이 (cm)', fontsize=12)
axes[0].legend(fontsize=11)
axes[1].plot(df_year.index[sel], resid[sel], color='gray', linewidth=0.9)
axes[1].axhline(0, color='black', linewidth=0.8)
axes[1].set_title(f'잔차(표준편차 {resid.std():.1f}cm)', fontsize=14, fontweight='bold')
axes[1].set_ylabel('잔차 (cm)', fontsize=12)
axes[1].set_xlabel('날짜(2024년 3월)', fontsize=12)
for ax in axes:
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.xaxis.set_major_locator(dates.DayLocator(interval=5))
    ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
plt.tight_layout()
plt.show()

print(f"설명한 비율 {(1 - resid.var() / y.var()) * 100:.2f}%, 잔차 표준편차 {resid.std():.1f}cm")

# %% code 101.
# Sa(1년) · Ssa(반년)를 더한 12개 분조로 다시 분석
PERIODS_SA = {**PERIODS, 'Sa': 8766.15265, 'Ssa': 4383.07633}
A2 = design_matrix(t, PERIODS_SA.values())
coef2, *_ = np.linalg.lstsq(A2, y, rcond=None)
resid2 = y - A2 @ coef2

r_before = pd.Series(resid, index=df_year.index).groupby(df_year.index.month).mean()
r_after = pd.Series(resid2, index=df_year.index).groupby(df_year.index.month).mean()
print("분조 10개 잔차의 월평균(cm):", r_before.round(1).tolist())
for i, name in enumerate(PERIODS_SA):
    if name in ('Sa', 'Ssa'):
        print(f"{name} 진폭: {np.hypot(coef2[1 + 2 * i], coef2[2 + 2 * i]):.1f}cm")
for n, r in [(10, resid), (12, resid2)]:
    print(f"분조 {n}개: 잔차 표준편차 {r.std():.1f}cm, "
          f"설명한 비율 {(1 - r.var() / y.var()) * 100:.2f}%")

x = np.arange(1, 13)
fig, ax = plt.subplots(figsize=(11, 5))
ax.bar(x - 0.2, r_before, 0.4, color='tomato', edgecolor='black', label='분조 10개')
ax.bar(x + 0.2, r_after, 0.4, color='seagreen', edgecolor='black',
       label='분조 12개(Sa · Ssa 추가)')
ax.axhline(0, color='black', linewidth=0.8)
ax.set_title('연주기 분조를 넣기 전과 후의 월별 잔차 평균', fontsize=15, fontweight='bold')
ax.set_xlabel('월', fontsize=12)
ax.set_ylabel('잔차 평균 (cm)', fontsize=12)
ax.set_xticks(range(1, 13))
ax.legend(fontsize=11)
ax.grid(axis='y', linestyle=':', alpha=0.5)
plt.tight_layout()
plt.show()
