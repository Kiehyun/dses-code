# 지구과학 데이터 사이언스 1 | IV-03. 에어코리아 자료 시각화하기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 40.
# 프로젝트(자료 저장) 폴더 생성 — 공통 함수 사용
proj_dir = du.make_project_dir(du.current_notebook_name() or "04_03_Visualizing_AirKorea_Data")
from pathlib import Path

# %% code 41.
# 파일 ID와 파일 이름을 튜플 목록으로 묶기
files = [
    ('146hh8byBZ7r-afm8FgbjNWrSLfFC2juV', '2016-01.zip'),
    ('1iHzRAIDmhjN_W7QgVh8kzk1MNJk4GUj8', '2016-02.zip'),
    ('1t9pqzXjHQQGfoBWDZNGAGxR3_ONyOdlm', '2016-03.zip'),
    ('1NN3-VAfAgUOAW01dYk8wBMm4N6PDe5Cc', '2016-04.zip')
]

# 튜플 목록으로 파일 내려받기
for file_id, file_name in files:
    du.download(
        f"https://docs.google.com/uc?export=download&id={file_id}",
        proj_dir / file_name
    )

# %% code 42.
fpaths = du.list_files(proj_dir, "zip")

# %% code 43.
import shutil
for fpath in fpaths:
    shutil.unpack_archive(str(fpath), str(proj_dir))
    print(f"Unzip {fpath} to {proj_dir}")  

# %% code 44.
fpaths = du.list_files(proj_dir, "csv")

# %% code 45.
du.preview_text(fpaths[0], n=10)

# %% code 46.
#package 불러오기
import pandas as pd

# 빈 DataFrame 생성
df = pd.DataFrame()

for fpath in fpaths :
    # 파일은 UTF-8로 저장되어 있습니다(윈도우 기본 인코딩 cp949로 읽으면 오류).
    df_month = pd.read_csv(str(fpath),
                encoding = 'utf-8',
                sep=',')
    df = pd.concat([df, df_month], ignore_index=True)
display(df)

# %% code 47.
print("df['측정일시'].dtype: {}".format(df['측정일시'].dtype))
df['O_datetime-1hr'] = df['측정일시'] - 1

df['YMdh-1hr_str'] = df['O_datetime-1hr'].astype(str)
df['YMdhms-1hr_str'] = df['YMdh-1hr_str'].str.slice(start=0, stop=8) + " " + df['YMdh-1hr_str'].str.slice(start=8, stop=10) + ":00:00"
df['YMdhms-1hr_dt'] = pd.to_datetime(df['YMdhms-1hr_str'])
print(df)

# %% code 48.
print("len(df['측정소코드'].unique()):\n {}".format(len(df['측정소코드'].unique())))
df = df.set_index(['측정소코드'], drop=False)
print(df)

# %% code 49.
print("len(df['YMdhms-1hr_dt'].unique()):\n {}".format(len(df['YMdhms-1hr_dt'].unique())))
df = df.set_index(['YMdhms-1hr_dt'], drop=False)
print(df)

# %% code 50.
df_MI = df.set_index(['측정소코드','YMdhms-1hr_dt'], drop=False)
print(df_MI)

# %% code 51.
print("len(df_MI['측정소코드'].unique()): {}".format(len(df_MI['측정소코드'].unique())))
print("df_MI['측정소코드'].unique(): \n{}".format(df_MI['측정소코드'].unique()))

# %% code 52.
Ocode = 632151 

print("len(df_MI[(df_MI['측정소코드'] == Ocode)]: {}".\
      format(len(df_MI[(df_MI['측정소코드'] == Ocode)])))

print(df_MI[(df_MI["측정소코드"] == Ocode)])

# %% code 53.
print("len(df_MI[(df_MI['YMdhms-1hr_dt'] >= '2016-01-01 00:00:00') & (df_MI['YMdhms-1hr_dt'] < '2016-02-01 00:00:00')]): {}".\
      format(len(df_MI[(df_MI['YMdhms-1hr_dt'] >= '2016-01-01 00:00:00') & (df_MI['YMdhms-1hr_dt'] < '2016-02-01 00:00:00')])))

print(df_MI[(df_MI["YMdhms-1hr_dt"] >= '2016-01-01 00:00:00') & (df_MI["YMdhms-1hr_dt"] < '2016-02-01 00:00:00')])

# %% code 54.
print(df_MI[["NO2", "O3"]])

# %% code 55.
print("type(df_MI.xs(632151)): {}".format(type(df_MI.xs(632151))))
print(df_MI.xs(632151))

# %% code 56.
print("type(df_MI.xs('2016-01-01 00:00:00', level=1)):{}".format(type(df_MI.xs('2016-01-01 00:00:00', level=1))))
print(df_MI.xs("2016-01-01 00:00:00", level=1))

# %% code 57.
Ocode = 632151
DATA_column1 = "O3"
DATA_column2 = "NO2"

begin_datetime_str = '2016-04-01 00:00:00'
end_datetime_str = '2016-05-01 00:00:00'

df_MI_selected1 = df_MI[(df_MI['YMdhms-1hr_dt'] >= begin_datetime_str) &\
      (df_MI['YMdhms-1hr_dt'] < end_datetime_str) &\
      (df_MI["측정소코드"] == Ocode)][[DATA_column1, DATA_column2]]

# %% code 58.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# 한글 폰트 설정
rc('font', family='NanumGothic')  # 또는 'Malgun Gothic', 'AppleGothic' 등

plt.figure(figsize=(12, 8))

plt.title("Histogram of {0} concentration (측정소코드 : {1})".\
        format(DATA_column1, str(Ocode)), fontsize=20, pad=20)
  
plt.hist(df_MI_selected1[DATA_column1])
plt.grid(True)

plt.annotate('created by guitar79@gs.hs.kr\nAir quality procuct using AirKorea data',
        xy=(1, 0), xytext=(12, -28), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points')

plt.annotate('period : {} ~ {}'\
        .format(begin_datetime_str, end_datetime_str),
        xy=(0, 0), xytext=(12, -28), va='top', ha='left',
        xycoords='axes fraction', textcoords='offset points')

plt.annotate('mean : {0:.02f}, max: {1:.02f}, min: {2:.02f}'\
        .format(np.nanmean(df_MI_selected1[DATA_column1]), 
        np.nanmax(df_MI_selected1[DATA_column1]),
        np.nanmin(df_MI_selected1[DATA_column1])),
        xy=(0, 0), xytext=(12, -44), va='top', ha='left',
        xycoords='axes fraction', textcoords='offset points')

# plt.savefig("{0}_{1}_{2}_hist.png"\
# .format(fpath[0][-4], Ocode, DATA_column1)) 
# print("{0}_{1}_{2}_hist.png is created..."\
# .format(fullname[-4], Ocode, DATA_column1))

# %% code 59.
print("type(df_MI_selected1.xs(Ocode).index) : {}".format(type(df_MI_selected1.xs(Ocode).index)))
print("df_MI_selected1.xs(Ocode).index) :\n {}".format(df_MI_selected1.xs(Ocode).index))

# %% code 60.
from datetime import timedelta
import matplotlib.dates as dates
import matplotlib.ticker as ticker

#그래프를 그려보자.
fig, ax1 = plt.subplots(figsize=(12.0, 3.3))

#x축 레이블
ax1.set_xlabel('time (year-month-day)', fontsize = 14)

# 달마다 날수가 달라 약간의 근사가 들어간다
ax1.xaxis.set_major_locator(dates.MonthLocator())
ax1.xaxis.set_minor_locator(dates.DayLocator())

#ax1.xaxis.set_major_formatter(ticker.NullFormatter())
#ax1.xaxis.set_minor_formatter(dates.DateFormatter('%d'))
ax1.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
ax1.xaxis.set_minor_formatter(ticker.NullFormatter())

ax1.set_xlim(np.nanmin(df_MI_selected1[DATA_column1].xs(Ocode).index), np.nanmax(df_MI_selected1[DATA_column1].xs(Ocode).index))
ax1.set_xticks(np.arange(np.nanmin(df_MI_selected1[DATA_column1].xs(Ocode).index), np.nanmax(df_MI_selected1[DATA_column1].xs(Ocode).index), 
        timedelta(days=1)), minor = False)

ax2 = ax1.twinx()

#그림
line1 = ax1.plot(df_MI_selected1[DATA_column1].xs(Ocode).index, df_MI_selected1[DATA_column1].xs(Ocode), 'r-', label=DATA_column1)
line2 = ax1.plot(df_MI_selected1[DATA_column2].xs(Ocode).index, df_MI_selected1[DATA_column2].xs(Ocode), 'b-', label=DATA_column2)

# y축 이름·눈금·눈금값 색을 선 색과 맞추기
ax1.set_ylabel('{} concentration ({})'.format(DATA_column1, "ppm"), fontsize = 14)
ax1.tick_params('y')
ax2.set_ylabel('{} concentration ({})'.format(DATA_column2, "ppm"), fontsize = 14)
ax2.tick_params('y')

ax1.set_title('Variation of {} and {} concentraion'.format(DATA_column1, DATA_column2), 
          y=1.05,   # 제목 아래 여백
          fontdict={'fontsize':18,'fontweight':'bold'})

# 이 줄들을 추가했다
lns = line1 + line2
labs = [l.get_label() for l in lns]

plt.legend(lns, labs, loc='upper right', bbox_to_anchor=(0.995, 0.995))

plt.grid(True)

fig.tight_layout()
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0.1)

# plt.savefig("{0}_{1}_{2}_{3}_plot.png"\
# .format(fullname[-4], Ocode, DATA_column1, DATA_column2)) 
# print("{0}_{1}_{2}_{3}_plot.png is created..."\
# .format(fullname[-4], Ocode, DATA_column1, DATA_column2))

plt.annotate('created by guitar79@gs.hs.kr\nAir quality procuct using AirKorea data',
        xy=(1, 0), xytext=(12, -28), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points')

plt.annotate('period : {} ~ {}'\
        .format(begin_datetime_str, end_datetime_str),
        xy=(0, 0), xytext=(12, -28), va='top', ha='left',
        xycoords='axes fraction', textcoords='offset points')

plt.annotate('mean : {0:.02f}, max: {1:.02f}, min: {2:.02f}'\
        .format(np.nanmean(df_MI_selected1[DATA_column1]), 
        np.nanmax(df_MI_selected1[DATA_column1]),
        np.nanmin(df_MI_selected1[DATA_column1])),
        xy=(0, 0), xytext=(12, -44), va='top', ha='left',
        xycoords='axes fraction', textcoords='offset points')

# plt.savefig("{0}_{1}_{2}_hist.png"\
# .format(fullname[-4], Ocode, DATA_column1)) 
# print("{0}_{1}_{2}_hist.png is created..."\
# .format(fullname[-4], Ocode, DATA_column1))

# %% code 61.
import matplotlib.pyplot as plt

# df_MI 전체 숫자 컬럼에 대한 상관계수 계산
corr = df_MI.corr(numeric_only=True)

fig, ax = plt.subplots(figsize=(10, 8))

im = ax.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)

# 컬러바 추가
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Pearson correlation coefficient', fontsize=12)

# 축 눈금 설정
ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.index)))

ax.set_xticklabels(corr.columns, rotation=45, ha='right', fontsize=11)
ax.set_yticklabels(corr.index, fontsize=11)

# 각 칸에 상관계수 값 표시
for i in range(len(corr.index)):
    for j in range(len(corr.columns)):
        ax.text(
            j, i,
            f'{corr.iloc[i, j]:.2f}',
            ha='center',
            va='center',
            color='black',
            fontsize=10
        )

ax.set_title(
    'Correlation Matrix of df_MI',
    fontsize=15,
    fontweight='bold'
)

plt.tight_layout()
plt.show()

cbar.set_label('Pearson correlation coefficient', fontsize=12)

# 축 눈금 설정
ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.index)))

ax.set_xticklabels(corr.columns, rotation=45, ha='right', fontsize=11)
ax.set_yticklabels(corr.index, fontsize=11)

# 각 칸에 상관계수 값 표시
for i in range(len(corr.index)):
    for j in range(len(corr.columns)):
        ax.text(
            j, i,
            f'{corr.iloc[i, j]:.2f}',
            ha='center',
            va='center',
            color='black',
            fontsize=10
        )

ax.set_title('Correlation Matrix of Air Pollutants', fontsize=15, fontweight='bold')

plt.tight_layout()
plt.show()

# %% code 62.
import numpy as np
import matplotlib.pyplot as plt

#그래프를 그려보자.
fig, ax1 = plt.subplots(figsize=(5, 5))

#그림
ax1.scatter(df_MI_selected1[DATA_column1].xs(Ocode),
            df_MI_selected1[DATA_column2].xs(Ocode), s=2)

ax1.set_title('{} vs {}'.format(DATA_column1, DATA_column2), 
          y=1.05,   # 제목 아래 여백
          fontdict={'fontsize':18,'fontweight':'bold'})

ax1.set_xlabel('{} concentration ({})'.format(DATA_column1, "ppm"), fontsize = 14)
ax1.set_ylabel('{} concentration ({})'.format(DATA_column2, "ppm"), fontsize = 14)

fig.tight_layout()
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0.1)

plt.annotate('created by guitar79@gs.hs.kr\nAir quality procuct using AirKorea data',
        xy=(1, 0), xytext=(12, -28), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points')

# plt.savefig("{0}_{1}_{2}_{3}_scatter.png"\
# .format(fullname[-4], Ocode, DATA_column1, DATA_column2)) 
# print("{0}_{1}_{2}_{3}_scatter.png is created..."\
# .format(fullname[-4], Ocode, DATA_column1, DATA_column2))

# %% code 63.
# 'W-MON' 월요일, 'W-TUE' 화요일, 'W-WED' 수요일, 'W-THU' 목요일, 'W-FRI' 금요일, 'W-SAT' 토요일, 'W-SUN' 일요일

print(df_MI[["SO2", "CO", "O3", "NO2", "PM10", "PM25"]].xs(632151).resample('W-MON').mean())

# %% code 64.
df_MI[["SO2", "CO", "O3", "NO2", "PM10", "PM25"]].xs(632151).resample('W-MON').mean().mean()

# %% code 65.
df_MI["NO2"].xs(632151).resample('W-MON').mean().mean()

# %% code 66.
Weekday_lst = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

import pandas as pd 

df_weekday = pd.DataFrame(data=None, columns = Weekday_lst) 
print(df_weekday)

Wday_lst = ["W-MON", "W-TUE", "W-WED", "W-THU", "W-FRI", "W-SAT", "W-SUN"]
Ocode = 632151

for i in range(len(Weekday_lst)):
    df_weekday[Weekday_lst[i]] = df_MI[["SO2", "CO", "O3", "NO2", "PM10", "PM25"]].xs(Ocode).resample(Wday_lst[i]).mean().mean()
print(df_weekday)

# %% code 67.
DATA_column3 = "SO2"
print("df_weekday.columns: {}".format(df_weekday.columns))

print("df_weekday.loc[DATA_column3,:]: {}\n".format(df_weekday.loc[DATA_column3,:]))

# %% code 68.
#그래프를 그려보자.
fig, ax1 = plt.subplots(figsize=(10, 10))

ax1.bar(df_weekday.columns, df_weekday.loc[DATA_column3,:])

ax1.set_title("Concentration of {}".format(DATA_column3), 
          y=1.05,   # 제목 아래 여백
          fontdict={'fontsize':18,'fontweight':'bold'})

ax1.set_ylabel("{} concentration {}".format(DATA_column3, "ppm"), fontsize = 14)

ax1.set_xlabel("Weekday", fontsize = 14)

fig.tight_layout()
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0.1)

plt.annotate('created by guitar79@gs.hs.kr\nAir quality procuct using AirKorea data',
        xy=(1, 0), xytext=(12, -28), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points')

# plt.savefig("{0}_{1}_bar.png"\
# .format(fullname[-4], Ocode)) 
# print("{0}_{1}_bar.png is created..."\
# .format(fullname[-4], Ocode))

# %% code 69.
#(과제) 아래에 코딩을 완성하여 제출하시오.

DATA_column3 = "SO2"

import numpy as np
import matplotlib.pyplot as plt

y_ax_ratio_var = 0.01

#그래프를 그려보자.
fig, ax1 = plt.subplots(figsize=(10, 10))

ax1.bar(df_weekday.columns, df_weekday.loc[DATA_column3,:])

ax1.set_ylim(np.min(df_weekday.loc[DATA_column3,:]) * (1 - y_ax_ratio_var), 
             np.max(df_weekday.loc[DATA_column3,:]) * (1 + y_ax_ratio_var))

ax1.set_title("Concentration of {}".format(DATA_column3), 
          y=1.05,   # 제목 아래 여백
          fontdict={'fontsize':18,'fontweight':'bold'})

ax1.set_ylabel("{} concentration {}".format(DATA_column3, "ppm"), fontsize = 14)

ax1.set_xlabel("Weekday", fontsize = 14)

fig.tight_layout()
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0.1)

plt.annotate('created by guitar79@gs.hs.kr\nAir quality procuct using AirKorea data',
        xy=(1, 0), xytext=(12, -28), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points')

# plt.savefig("{0}_{1}_bar.png"\
# .format(fullname[-4], Ocode)) 
# print("{0}_{1}_bar.png is created..."\
# .format(fullname[-4], Ocode))
