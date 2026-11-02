# 지구과학 데이터 사이언스 1 | IV-01. 기상청 AWS 데이터 시각화하기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 1.
from pathlib import Path

fname = "SURFACE_ASOS_116_MI_2018-01_2018-12_2018.zip"
fid = "1bUOR1wEmCPCCH8iY23shQ5d_c2td_kt-"  # 구글 드라이브 파일 ID

du.download(f"https://docs.google.com/uc?export=download&id={fid}", Path(proj_dir) / fname)

# %% code 2.
fpaths = du.list_files(proj_dir, "zip")

# %% code 3.
import shutil
shutil.unpack_archive(str(fpaths[0]), str(Path(proj_dir)))

from zipfile import ZipFile
with ZipFile(str(fpaths[0]), 'r') as zip_ref:
    zip_ref.extractall(str(Path(proj_dir)))

fpaths = du.list_files(proj_dir, "csv")

# %% code 4.
du.preview_text(fpaths[0], n=10);  # 앞 10줄(인코딩 자동)

# %% code 5.
import pandas as pd

# 천 단위 쉼표 처리, 기상청 데이터는 EUC-KR 인코딩
df = pd.read_csv(str(fpaths[0]), thousands=',', encoding='euc-kr')

print(f"df :\n{df}")

# %% code 6.
# 월별 파일 모두 합치기
import pandas as pd

df_month = pd.DataFrame()

for fpath in fpaths:
    print(f"읽는 중: {fpath.name} (인코딩: euc-kr)")
    df_month = pd.read_csv(str(fpath), encoding='euc_kr', sep=',')
    df = pd.concat([df, df_month], ignore_index=True)

df = df.drop_duplicates()  # 첫 달 파일이 두 번 들어가므로 중복 제거
print(f"총 레코드 수(중복 제거 후): {len(df)}")
print(f"df :\n{df}")

# %% code 7.
# 문자열 '일시'를 datetime으로 변환
print(f"type(df['일시'][0]): {type(df['일시'][0])}")
df['dt_YmdHM'] = pd.to_datetime(df['일시'])
print(f"type(df['dt_YmdHM'][0]): {type(df['dt_YmdHM'][0])}")

from datetime import timedelta

# 직전 1분 측정값이므로 1분 당긴 시각을 인덱스로
df['dt_YmdHM-1min'] = df['dt_YmdHM'] - timedelta(minutes=1)
df.index = df['dt_YmdHM-1min']
print(f"df :\n{df}")

# %% code 8.
from datetime import datetime, timedelta

# 같은 날짜를 고르는 세 가지 방법
df_jan51 = df[df['일시'].str.contains('2018-01-05')]
print(f"df_jan51 :\n{df_jan51}")

df_jan52 = df[df['dt_YmdHM-1min'].dt.date == datetime(2018, 1, 5).date()]
print(f"df_jan52 :\n{df_jan52}")

df_jan53 = df[(df['dt_YmdHM-1min'] >= '2018-01-12 00:00') & (df['dt_YmdHM-1min'] < '2018-01-13 00:00')]
print(f"df_jan53 :\n{df_jan53}")

# %% code 9.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime, timedelta

fig, ax1 = plt.subplots(figsize=(12.0, 4.0))

df_jan5 = df_jan52

# 1) 기온: 왼쪽 y축
Temp_line = ax1.plot(df_jan5['dt_YmdHM-1min'], df_jan5['기온(°C)'], label='기온', color='red')

ax1.set_xlabel('일시', fontsize = 14)
ax1.set_ylabel('기온 (°C)', fontsize = 14, color='red')
ax1.tick_params(axis='y', labelcolor='red')

# 2) 습도: x축을 공유하는 오른쪽 y축
ax2 = ax1.twinx()

Humi_line = ax2.plot(df_jan5['dt_YmdHM-1min'], df_jan5['습도(%)'], label='습도', color='blue')

ax2.set_ylabel('상대습도 (%)', fontsize = 14, color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

ax1.set_title('2018년 1월 5일의 기온과 상대습도의 변동 (관악산)',
          y=1.05,  # 제목 아래쪽 여백
          fontdict={'fontsize':18,'fontweight':'bold'})

plt.xticks(rotation=45)  # 시각 눈금 겹침 방지

# 3) 두 축의 범례를 하나로 합치기
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.tight_layout()
plt.show()

# %% code 10.
import pandas as pd
import numpy as np

df['date'] = df['dt_YmdHM-1min'].dt.date  # 날짜만(시각 제거)

print(f"\n전체 데이터 개수: {len(df)}")

# 1) 날짜별 누적강수량의 최댓값 = 그날의 강수량
daily_max_rainfall = df.groupby('date')['누적강수량(mm)'].max().reset_index()

print("\n날짜별 최대 강수량 미리보기:")
print(daily_max_rainfall.head(10))

# 2) 비가 조금이라도 내린 날
rainy_days = daily_max_rainfall[daily_max_rainfall['누적강수량(mm)'] > 0]

print(f"\n비가 내린 날들의 강수량 통계:")
print(rainy_days['누적강수량(mm)'].describe())

# 3) 비 온 날 수와 비율
num_rainy_days = len(rainy_days)
total_days = len(daily_max_rainfall)
percentage = (num_rainy_days / total_days) * 100

print(f"\n=== 결과 ===")
print(f"전체 날짜 수: {total_days}일")
print(f"비가 내린 날 수: {num_rainy_days}일")
print(f"비가 내린 날의 비율: {percentage:.1f}%")

# 4) 월별 비 온 날 수
df['month'] = df['dt_YmdHM-1min'].dt.month
monthly_rainy_days = df.groupby(['date', 'month'])['누적강수량(mm)'].max().reset_index()
monthly_rainy_days = monthly_rainy_days[monthly_rainy_days['누적강수량(mm)'] > 0]
monthly_count = monthly_rainy_days.groupby('month').size()

print(f"\n월별 비오는 날 수:")
months = ['1월', '2월', '3월', '4월', '5월', '6월',
          '7월', '8월', '9월', '10월', '11월', '12월']
for month_num, count in monthly_count.items():
    print(f"{months[month_num-1]}: {count}일")

# %% code 11.
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 앞 셀과 같은 전처리
df['date'] = df['dt_YmdHM-1min'].dt.date
daily_max_rainfall = df.groupby('date')['누적강수량(mm)'].max().reset_index()
rainy_days = daily_max_rainfall[daily_max_rainfall['누적강수량(mm)'] > 0]
num_rainy_days = len(rainy_days)
total_days = len(daily_max_rainfall)

df['month'] = df['dt_YmdHM-1min'].dt.month
monthly_rainy_days = df.groupby(['date', 'month'])['누적강수량(mm)'].max().reset_index()
monthly_rainy_days = monthly_rainy_days[monthly_rainy_days['누적강수량(mm)'] > 0]
monthly_count = monthly_rainy_days.groupby('month').size()

monthly_total_days = df.groupby('month')['date'].nunique()  # 월별 관측 일수

fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.6))
fig.suptitle('2018년 강수량 분석 결과', fontsize=16, fontweight='bold')

# 1) 파이 차트: 비 온 날의 비율
ax1 = axes[0, 0]
labels = ['비가 내린 날', '비가 안 내린 날']
sizes = [num_rainy_days, total_days - num_rainy_days]
colors = ['lightblue', 'lightcoral']
explode = (0.1, 0)  # 첫 조각을 약간 떼어 놓기

wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                   explode=explode, startangle=90, shadow=True)
ax1.set_title(f'전체 {total_days}일 중 비가 내린 날의 비율', fontsize=12, fontweight='bold')

# 2) 막대그래프: 월별 비 온 날 수
ax2 = axes[0, 1]
months = ['1월', '2월', '3월', '4월', '5월', '6월',
          '7월', '8월', '9월', '10월', '11월', '12월']
month_nums = range(1, 13)

rainy_counts = [monthly_count.get(i, 0) for i in month_nums]  # 비 온 날이 없는 달은 0

bars = ax2.bar(months, rainy_counts, color='skyblue', alpha=0.7, edgecolor='navy', linewidth=1)
ax2.set_title('월별 비오는 날 수', fontsize=12, fontweight='bold')
ax2.set_ylabel('비오는 날 수')
ax2.set_xlabel('월')
ax2.grid(True, alpha=0.3)

for bar, count in zip(bars, rainy_counts):  # 막대 위에 날수 쓰기
    if count > 0:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                str(count), ha='center', va='bottom', fontweight='bold')

ax2.tick_params(axis='x', rotation=45)

# 3) 선 그래프: 월별 비 온 날의 비율
ax3 = axes[1, 0]
monthly_percentages = []
for i in month_nums:
    rainy_count = monthly_count.get(i, 0)
    total_count = monthly_total_days.get(i, 1)
    percentage = (rainy_count / total_count) * 100
    monthly_percentages.append(percentage)

ax3.plot(months, monthly_percentages, marker='o', linewidth=2, markersize=8,
         color='darkblue', markerfacecolor='red', markeredgecolor='darkblue')
ax3.set_title('월별 비오는 날 비율', fontsize=12, fontweight='bold')
ax3.set_ylabel('비율 (%)')
ax3.set_xlabel('월')
ax3.grid(True, alpha=0.3)
ax3.tick_params(axis='x', rotation=45)

for i, (month, percentage) in enumerate(zip(months, monthly_percentages)):
    ax3.text(i, percentage + 1, f'{percentage:.1f}%',
             ha='center', va='bottom', fontweight='bold', fontsize=9)

# 4) 히스토그램: 비 온 날의 강수량 분포
ax4 = axes[1, 1]
rainfall_amounts = rainy_days['누적강수량(mm)'].values
ax4.hist(rainfall_amounts, bins=20, color='lightgreen', alpha=0.7, edgecolor='darkgreen')
ax4.set_title('비가 내린 날의 강수량 분포', fontsize=12, fontweight='bold')
ax4.set_xlabel('누적강수량 (mm)')
ax4.set_ylabel('빈도')
ax4.grid(True, alpha=0.3)

mean_rainfall = rainfall_amounts.mean()
ax4.axvline(mean_rainfall, color='red', linestyle='--', linewidth=2,
            label=f'평균: {mean_rainfall:.1f}mm')
ax4.legend()

plt.tight_layout()
plt.show()

# 계절별 비 온 날
print("\n=== 계절별 비오는 날 통계 ===")
seasons = {
    '봄': [3, 4, 5],
    '여름': [6, 7, 8],
    '가을': [9, 10, 11],
    '겨울': [12, 1, 2]
}

for season, months_in_season in seasons.items():
    season_rainy_days = sum(monthly_count.get(month, 0) for month in months_in_season)
    season_total_days = sum(monthly_total_days.get(month, 0) for month in months_in_season)
    season_percentage = (season_rainy_days / season_total_days) * 100
    print(f"{season}: {season_rainy_days}일 ({season_percentage:.1f}%)")

print(f"\n=== 강수량 통계 요약 ===")
print(f"비가 내린 날 수: {num_rainy_days}일")
print(f"평균 강수량: {rainy_days['누적강수량(mm)'].mean():.2f}mm")
print(f"최대 강수량: {rainy_days['누적강수량(mm)'].max():.2f}mm")
print(f"최소 강수량: {rainy_days['누적강수량(mm)'].min():.2f}mm")
print(f"중간값: {rainy_days['누적강수량(mm)'].median():.2f}mm")

# %% code 12.
import pandas as pd
import numpy as np
from datetime import datetime

def calculate_temperature_averages(df, datetime_col='dt_YmdHM-1min', temp_col='기온(°C)'):
    """
    일평균 기온과 월평균 기온을 두 가지 방법으로 계산
    
    Parameters:
    df: DataFrame with datetime and temperature columns
    datetime_col: 날짜시간 열 이름
    temp_col: 기온 열 이름
    """

    df[datetime_col] = pd.to_datetime(df[datetime_col])

    df['date'] = df[datetime_col].dt.date
    df['year_month'] = df[datetime_col].dt.to_period('M')

    # ===== 방법 1: (일최고 + 일최저) / 2 =====
    print("=" * 50)
    print("방법 1: 일최고/일최저 기온의 산술평균")
    print("=" * 50)

    daily_extremes = df.groupby('date')[temp_col].agg(['min', 'max']).reset_index()
    daily_extremes.columns = ['date', 'daily_min', 'daily_max']

    daily_extremes['daily_avg_method1'] = (daily_extremes['daily_min'] + daily_extremes['daily_max']) / 2

    print("일별 최고/최저 기온 및 일평균 기온:")
    print(daily_extremes.head(10))

    # 월평균 = 일평균들의 평균
    daily_extremes['year_month'] = pd.to_datetime(daily_extremes['date']).dt.to_period('M')
    monthly_avg_method1 = daily_extremes.groupby('year_month')['daily_avg_method1'].mean().reset_index()
    monthly_avg_method1.columns = ['year_month', 'monthly_avg_method1']

    print("\n월평균 기온 (방법 1):")
    print(monthly_avg_method1)

    # ===== 방법 2: 모든 관측값의 평균 =====
    print("\n" + "=" * 50)
    print("방법 2: 모든 관측값의 직접 평균")
    print("=" * 50)

    daily_avg_method2 = df.groupby('date')[temp_col].mean().reset_index()
    daily_avg_method2.columns = ['date', 'daily_avg_method2']

    print("일평균 기온 (모든 관측값 평균):")
    print(daily_avg_method2.head(10))

    monthly_avg_method2 = df.groupby('year_month')[temp_col].mean().reset_index()
    monthly_avg_method2.columns = ['year_month', 'monthly_avg_method2']

    print("\n월평균 기온 (방법 2):")
    print(monthly_avg_method2)

    # ===== 두 방법 비교 =====
    print("\n" + "=" * 50)
    print("두 방법 비교")
    print("=" * 50)

    daily_comparison = pd.merge(daily_extremes[['date', 'daily_avg_method1']],
                               daily_avg_method2, on='date')
    daily_comparison['daily_difference'] = daily_comparison['daily_avg_method1'] - daily_comparison['daily_avg_method2']

    print("일평균 기온 비교:")
    print(daily_comparison.head(10))
    print(f"\n일평균 기온 차이 통계:")
    print(f"평균 차이: {daily_comparison['daily_difference'].mean():.3f}°C")
    print(f"최대 차이: {daily_comparison['daily_difference'].max():.3f}°C")
    print(f"최소 차이: {daily_comparison['daily_difference'].min():.3f}°C")
    print(f"표준편차: {daily_comparison['daily_difference'].std():.3f}°C")

    monthly_comparison = pd.merge(monthly_avg_method1, monthly_avg_method2, on='year_month')
    monthly_comparison['monthly_difference'] = monthly_comparison['monthly_avg_method1'] - monthly_comparison['monthly_avg_method2']

    print("\n월평균 기온 비교:")
    print(monthly_comparison)
    print(f"\n월평균 기온 차이 통계:")
    print(f"평균 차이: {monthly_comparison['monthly_difference'].mean():.3f}°C")
    print(f"최대 차이: {monthly_comparison['monthly_difference'].max():.3f}°C")
    print(f"최소 차이: {monthly_comparison['monthly_difference'].min():.3f}°C")
    print(f"표준편차: {monthly_comparison['monthly_difference'].std():.3f}°C")

    results = {
        'daily_method1': daily_extremes,
        'daily_method2': daily_avg_method2,
        'monthly_method1': monthly_avg_method1,
        'monthly_method2': monthly_avg_method2,
        'daily_comparison': daily_comparison,
        'monthly_comparison': monthly_comparison
    }

    return results

def plot_temperature_comparison(results):
    """
    두 방법의 결과를 시각화
    """
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib import font_manager

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.6))
    fig.suptitle('기온 계산 방법 비교', fontsize=16, fontweight='bold')

    daily_comp = results['daily_comparison']
    dates = pd.to_datetime(daily_comp['date'])

    axes[0, 0].plot(dates, daily_comp['daily_avg_method1'],
                    label='방법 1 (최고+최저)/2', alpha=0.7)
    axes[0, 0].plot(dates, daily_comp['daily_avg_method2'],
                    label='방법 2 (전체 평균)', alpha=0.7)
    axes[0, 0].set_title('일평균 기온 비교', fontsize=14, fontweight='bold')
    axes[0, 0].set_ylabel('기온 (°C)')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    axes[0, 1].plot(dates, daily_comp['daily_difference'], color='red', alpha=0.7)
    axes[0, 1].set_title('일평균 기온 차이 (방법1 - 방법2)', fontsize=14, fontweight='bold')
    axes[0, 1].set_ylabel('기온 차이 (°C)')
    axes[0, 1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    axes[0, 1].grid(True, alpha=0.3)

    monthly_comp = results['monthly_comparison']
    month_labels = [str(ym) for ym in monthly_comp['year_month']]

    # 두 막대를 나란히 놓을 위치와 폭
    x_pos = range(len(month_labels))
    width = 0.35

    axes[1, 0].bar([x - width/2 for x in x_pos], monthly_comp['monthly_avg_method1'],
                   width, label='방법 1', alpha=0.7)
    axes[1, 0].bar([x + width/2 for x in x_pos], monthly_comp['monthly_avg_method2'],
                   width, label='방법 2', alpha=0.7)
    axes[1, 0].set_title('월평균 기온 비교', fontsize=14, fontweight='bold')
    axes[1, 0].set_ylabel('기온 (°C)')
    axes[1, 0].set_xlabel('월')
    axes[1, 0].set_xticks(x_pos)
    axes[1, 0].set_xticklabels(month_labels, rotation=45)
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    axes[1, 1].bar(x_pos, monthly_comp['monthly_difference'], color='red', alpha=0.7)
    axes[1, 1].set_title('월평균 기온 차이 (방법1 - 방법2)', fontsize=14, fontweight='bold')
    axes[1, 1].set_ylabel('기온 차이 (°C)')
    axes[1, 1].set_xlabel('월')
    axes[1, 1].set_xticks(x_pos)
    axes[1, 1].set_xticklabels(month_labels, rotation=45)
    axes[1, 1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

results = calculate_temperature_averages(df, 'dt_YmdHM-1min', '기온(°C)')

plot_temperature_comparison(results)

# %% code 13.
# resample()만으로는 값이 아니라 Resampler 객체
print("type(df.resample('D'): {}".format(type(df.resample('D'))))
print("df.resample('D') :", df.resample('D'))

# 하루('D') 단위로 묶어 날마다 최댓값
df_daily_max = df.resample('D').max()
print("df_daily_max :\n{}".format(df_daily_max))

# %% code 14.
print(f"원본 데이터 형태: {df.shape}")
print(f"인덱스 타입: {type(df.index)}")
print(f"인덱스 빈도: {df.index.freq}")
print(f"인덱스 범위: {df.index.min()} ~ {df.index.max()}")
print("\n원본 데이터 샘플:")
print(df.head())

print("\n=== 2. DatetimeIndex 속성 확인 ===")
print(f"연도: {df.index.year[:5].values}")
print(f"월: {df.index.month[:5].values}")
print(f"일: {df.index.day[:5].values}")
print(f"요일: {df.index.dayofweek[:5].values}")  # 0=월요일, 6=일요일
print(f"요일명: {df.index.day_name()[:5].values}")

print("\n=== 3. 월별 리샘플링 (다운샘플링) ===")
# 'MS': 월 시작일 기준
df_monthly_start = df.resample('MS').agg({
    '기온(°C)': 'mean',
    '습도(%)': 'mean'
})

# 'ME': 월 마지막 날 기준
df_monthly_end = df.resample('ME').agg({
    '기온(°C)': 'mean',
    '습도(%)': 'mean'
})

print(f"월별 리샘플링 후 데이터 형태 (MS): {df_monthly_start.shape}")
print(f"월별 리샘플링 후 인덱스 빈도 (MS): {df_monthly_start.index.freq}")
print("\n월별 리샘플링 결과 (Month Start):")
print(df_monthly_start.head())

print(f"\n월별 리샘플링 후 데이터 형태 (M): {df_monthly_end.shape}")
print(f"월별 리샘플링 후 인덱스 빈도 (M): {df_monthly_end.index.freq}")
print("\n월별 리샘플링 결과 (Month End):")
print(df_monthly_end.head())

print("\n=== 4. 주별 리샘플링 ===")
df_weekly = df.resample('W').agg({'기온(°C)': 'mean', '습도(%)': 'mean'})

print(f"주별 리샘플링 후 데이터 형태: {df_weekly.shape}")
print(f"주별 리샘플링 후 인덱스 빈도: {df_weekly.index.freq}")
print("\n주별 리샘플링 결과:")
print(df_weekly.head())

print("="*30)
print("df.index: {}".format(df.index))

print("="*30)
print("type(df.resample('ME').max()): {}".format(type(df.resample('ME').max())))

print("="*30)
print("df.resample('ME').max().index: {}".format(df.resample('ME').max().index))

print("="*30)
print("df.resample('ME').max().index.month: {}".format(df.resample('ME').max().index.month))
print("df.resample('ME').max().index.month_name(): {}".format(df.resample('ME').max().index.month_name()))
print(f"YYYY-MM: {df.resample('ME').max().index.strftime('%Y-%m')[:5].values}")
print(f"Month Year: {df.resample('ME').max().index.strftime('%B %Y')[:5].values}")

# %% code 15.
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 1분 데이터를 하루 단위로 묶어 일평균 · 일최고 · 일최저를 구함
daily_stats = df.resample('D').agg(
    일평균기온=('기온(°C)', 'mean'),
    일최고기온=('기온(°C)', 'max'),
    일최저기온=('기온(°C)', 'min'),
    일평균습도=('습도(%)', 'mean'),
)
daily_stats['기온범위'] = daily_stats['일최고기온'] - daily_stats['일최저기온']

print("일별 통계 데이터:")
print(daily_stats[['일평균기온', '일최고기온', '일최저기온', '일평균습도']].head())
print(f"\n데이터 형태: {daily_stats.shape}")

plt.figure(figsize=(12.0, 10.0))

# 1) 박스플롯: 기온 분포
plt.subplot(3, 2, 1)
box_data = [daily_stats['일평균기온'].dropna(),
           daily_stats['일최고기온'].dropna(),
           daily_stats['일최저기온'].dropna()]
box_labels = ['일평균기온', '일최고기온', '일최저기온']
colors = ['lightblue', 'lightcoral', 'lightcyan']

bp = plt.boxplot(box_data, tick_labels=box_labels, patch_artist=True)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
plt.title('일별 기온 분포 (박스플롯)', fontsize=14, fontweight='bold')
plt.ylabel('기온 (°C)')
plt.grid(True, alpha=0.3)

# 2) 히트맵: 월별 평균기온(1년치라 한 줄)
plt.subplot(3, 2, 2)
daily_stats_copy = daily_stats.copy()
daily_stats_copy['연도'] = daily_stats_copy.index.year
daily_stats_copy['월'] = daily_stats_copy.index.month

heatmap_data = daily_stats_copy.groupby(['연도', '월'])['일평균기온'].mean().unstack()

sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='RdYlBu_r',
            cbar_kws={'label': '기온 (°C)'})
plt.title('월별 일평균 기온 히트맵 (2018년)', fontsize=14, fontweight='bold')
plt.xlabel('월')
plt.ylabel('연도')

# 3) 시계열: 기온 변화
plt.subplot(3, 2, (3, 4))  # 3 · 4번 칸을 합쳐 넓게
plt.plot(daily_stats.index, daily_stats['일평균기온'],
         linewidth=1, label='일평균기온', color='blue', alpha=0.7)
plt.plot(daily_stats.index, daily_stats['일최고기온'],
         linewidth=1, label='일최고기온', color='red', alpha=0.7)
plt.plot(daily_stats.index, daily_stats['일최저기온'],
         linewidth=1, label='일최저기온', color='cyan', alpha=0.7)
plt.title('일별 기온 변화 (시계열)', fontsize=14, fontweight='bold')
plt.xlabel('날짜')
plt.ylabel('기온 (°C)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

# 4) 영역 그래프: 기온 범위
plt.subplot(3, 2, (5, 6))  # 5 · 6번 칸을 합쳐 넓게
daily_stats['기온범위'] = daily_stats['일최고기온'] - daily_stats['일최저기온']

sample_idx = daily_stats.index[::7]  # 7일 간격
sample_data = daily_stats.loc[sample_idx]

plt.fill_between(sample_data.index, sample_data['일최저기온'],
                sample_data['일최고기온'], alpha=0.3, color='orange', label='기온 범위')
plt.plot(sample_data.index, sample_data['일평균기온'],
         color='darkblue', linewidth=2, label='일평균기온')
plt.plot(sample_data.index, sample_data['일최고기온'],
         color='red', linewidth=1, linestyle='--', label='일최고기온')
plt.plot(sample_data.index, sample_data['일최저기온'],
         color='blue', linewidth=1, linestyle='--', label='일최저기온')

plt.title('일별 기온 범위 (영역 그래프, 7일 간격 샘플링)', fontsize=14, fontweight='bold')
plt.xlabel('날짜')
plt.ylabel('기온 (°C)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

print("\n=== 일별 기온 통계 요약 ===")
print(f"전체 기간 평균기온: {daily_stats['일평균기온'].mean():.2f}°C")
print(f"일평균기온의 최댓값: {daily_stats['일평균기온'].max():.2f}°C")
print(f"일평균기온의 최솟값: {daily_stats['일평균기온'].min():.2f}°C")
print(f"평균 기온 범위: {daily_stats['기온범위'].mean():.2f}°C")

# 극값과 그 날짜
max_temp_date = daily_stats['일평균기온'].idxmax()
min_temp_date = daily_stats['일평균기온'].idxmin()
print(f"\n일평균기온이 가장 높은 날: {daily_stats.loc[max_temp_date, '일평균기온']:.2f}°C "
      f"({max_temp_date.strftime('%Y년 %m월 %d일')})")
print(f"일평균기온이 가장 낮은 날: {daily_stats.loc[min_temp_date, '일평균기온']:.2f}°C "
      f"({min_temp_date.strftime('%Y년 %m월 %d일')})")

print("\n=== 계절별 평균 기온 ===")
seasonal_avg = daily_stats.groupby(daily_stats.index.month).agg({
    '일평균기온': 'mean',
    '일최고기온': 'mean',
    '일최저기온': 'mean'
})

seasons = {1: '겨울', 2: '겨울', 3: '봄', 4: '봄', 5: '봄', 6: '여름',
          7: '여름', 8: '여름', 9: '가을', 10: '가을', 11: '가을', 12: '겨울'}

for month, row in seasonal_avg.iterrows():
    season = seasons[month]
    print(f"{month}월 ({season}): 평균 {row['일평균기온']:.1f}°C, "
          f"최고 {row['일최고기온']:.1f}°C, 최저 {row['일최저기온']:.1f}°C")

print("\n=== 일별 기온 변화 분석 ===")
daily_stats['기온변화'] = daily_stats['일평균기온'].diff()  # 바로 앞 값과의 차
print(f"평균 일일 기온 변화: {daily_stats['기온변화'].mean():.2f}°C")
print(f"최대 일일 기온 상승: {daily_stats['기온변화'].max():.2f}°C")
print(f"최대 일일 기온 하락: {daily_stats['기온변화'].min():.2f}°C")

# %% code 16.
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 월별 평균 · 최고 · 최저 기온과 평균 습도
monthly_stats = df.resample('ME').agg({
    '기온(°C)': ['mean', 'max', 'min'],
    '습도(%)': 'mean'
})

monthly_stats.columns = ['월평균기온', '월최고기온', '월최저기온', '월평균습도']

print("월별 통계 데이터:")
print(monthly_stats.head())
print(f"\n데이터 형태: {monthly_stats.shape}")

plt.figure(figsize=(12.0, 8.0))

# 1) 시계열: 월평균 · 최고 · 최저 기온
plt.subplot(2, 2, 1)
plt.plot(monthly_stats.index, monthly_stats['월평균기온'],
         marker='o', linewidth=2, label='월평균기온', color='blue')
plt.plot(monthly_stats.index, monthly_stats['월최고기온'],
         marker='^', linewidth=2, label='월최고기온', color='red')
plt.plot(monthly_stats.index, monthly_stats['월최저기온'],
         marker='v', linewidth=2, label='월최저기온', color='cyan')
plt.title('월별 기온 변화 (시계열)', fontsize=14, fontweight='bold')
plt.xlabel('날짜')
plt.ylabel('기온 (°C)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

# 2) 박스플롯
plt.subplot(2, 2, 2)
box_data = [monthly_stats['월평균기온'], monthly_stats['월최고기온'], monthly_stats['월최저기온']]
box_labels = ['월평균기온', '월최고기온', '월최저기온']
colors = ['lightblue', 'lightcoral', 'lightcyan']

bp = plt.boxplot(box_data, tick_labels=box_labels, patch_artist=True)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
plt.title('월별 기온 분포 (박스플롯)', fontsize=14, fontweight='bold')
plt.ylabel('기온 (°C)')
plt.grid(True, alpha=0.3)

# 3) 히트맵: 연도 × 월(1년치라 한 줄)
plt.subplot(2, 2, 3)
monthly_stats_copy = monthly_stats.copy()
monthly_stats_copy['연도'] = monthly_stats_copy.index.year
monthly_stats_copy['월'] = monthly_stats_copy.index.month

heatmap_data = monthly_stats_copy.pivot_table(
    values='월평균기온', index='연도', columns='월', aggfunc='mean'
)

sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='RdYlBu_r',
            cbar_kws={'label': '기온 (°C)'})
plt.title('월평균 기온 히트맵 (2018년)', fontsize=14, fontweight='bold')
plt.xlabel('월')
plt.ylabel('연도')

# 4) 영역 그래프: 기온 범위(최고 - 최저)
plt.subplot(2, 2, 4)
monthly_stats['기온범위'] = monthly_stats['월최고기온'] - monthly_stats['월최저기온']

plt.fill_between(monthly_stats.index, monthly_stats['월최저기온'],
                monthly_stats['월최고기온'], alpha=0.3, color='orange', label='기온 범위')
plt.plot(monthly_stats.index, monthly_stats['월평균기온'],
         color='darkblue', linewidth=2, label='월평균기온')
plt.plot(monthly_stats.index, monthly_stats['월최고기온'],
         color='red', linewidth=1, linestyle='--', label='월최고기온')
plt.plot(monthly_stats.index, monthly_stats['월최저기온'],
         color='blue', linewidth=1, linestyle='--', label='월최저기온')

plt.title('월별 기온 범위 (영역 그래프)', fontsize=14, fontweight='bold')
plt.xlabel('날짜')
plt.ylabel('기온 (°C)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

print("\n=== 월별 기온 통계 요약 ===")
print(f"전체 기간 평균기온: {monthly_stats['월평균기온'].mean():.2f}°C")
print(f"전체 기간 최고기온: {monthly_stats['월최고기온'].max():.2f}°C")
print(f"전체 기간 최저기온: {monthly_stats['월최저기온'].min():.2f}°C")
print(f"평균 기온 범위: {monthly_stats['기온범위'].mean():.2f}°C")

# 극값과 그 달
max_temp_date = monthly_stats['월최고기온'].idxmax()
min_temp_date = monthly_stats['월최저기온'].idxmin()
print(f"\n최고 기온 기록: {monthly_stats.loc[max_temp_date, '월최고기온']:.2f}°C ({max_temp_date.strftime('%Y년 %m월')})")
print(f"최저 기온 기록: {monthly_stats.loc[min_temp_date, '월최저기온']:.2f}°C ({min_temp_date.strftime('%Y년 %m월')})")

print("\n=== 계절별 평균 기온 ===")
seasonal_avg = monthly_stats.groupby(monthly_stats.index.month).agg({
    '월평균기온': 'mean',
    '월최고기온': 'mean',
    '월최저기온': 'mean'
})

seasons = {1: '겨울', 2: '겨울', 3: '봄', 4: '봄', 5: '봄', 6: '여름',
          7: '여름', 8: '여름', 9: '가을', 10: '가을', 11: '가을', 12: '겨울'}

for month, row in seasonal_avg.iterrows():
    season = seasons[month]
    print(f"{month}월 ({season}): 평균 {row['월평균기온']:.1f}°C, "
          f"최고 {row['월최고기온']:.1f}°C, 최저 {row['월최저기온']:.1f}°C")

# %% code 17.
import numpy as np

# 연습용 가상 데이터
ws = np.random.random(100) * 6        # 풍속 0~6 m/s
wd = 80 + np.random.random(100) * 20  # 풍향 90° ± 10°

print("ws : {}".format(ws))
print("wd : {}".format(wd))

from matplotlib import pyplot as plt
from windrose import WindroseAxes

ax = WindroseAxes.from_ax()  # 바람장미용 극좌표 축

ax.bar(wd, ws)

# %% code 18.
# windrose가 쓰는 열 이름으로 복사
df['speed'] = df['풍속(m/s)']
df['direction'] = df['풍향(deg)']

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import seaborn as sns

fig = plt.figure(figsize=(12, 10))

colors = plt.cm.viridis

# 1) 막대형
ax1 = fig.add_subplot(2, 2, 1, projection="windrose")
ax1.bar(df['direction'], df['speed'], normed=True, opening=0.8,
        edgecolor='white', cmap=colors)  # normed: 빈도를 %로
ax1.set_legend(title='풍속 (m/s)', loc='upper left', bbox_to_anchor=(1.1, 1))
ax1.set_title('막대형 바람장미', fontsize=14, fontweight='bold', pad=20)

# 2) 박스형
ax2 = fig.add_subplot(2, 2, 2, projection="windrose")
ax2.box(df['direction'], df['speed'], normed=True, cmap=colors)
ax2.set_legend(title='풍속 (m/s)', loc='upper left', bbox_to_anchor=(1.1, 1))
ax2.set_title('박스형 바람장미', fontsize=14, fontweight='bold', pad=20)

# 3) 등고선 채움형
ax3 = fig.add_subplot(2, 2, 3, projection="windrose")
ax3.contourf(df['direction'], df['speed'], normed=True, cmap=colors)
ax3.set_legend(title='풍속 (m/s)', loc='upper left', bbox_to_anchor=(1.1, 1))
ax3.set_title('등고선 채움형 바람장미', fontsize=14, fontweight='bold', pad=20)

# 4) 등고선형
ax4 = fig.add_subplot(2, 2, 4, projection="windrose")
ax4.contour(df['direction'], df['speed'], normed=True, cmap=colors)
ax4.set_legend(title='풍속 (m/s)', loc='upper left', bbox_to_anchor=(1.1, 1))
ax4.set_title('등고선형 바람장미', fontsize=14, fontweight='bold', pad=20)

fig.suptitle('바람장미 분석 - 4가지 시각화 유형 비교',
             fontsize=18, fontweight='bold', y=1.01)

plt.tight_layout()
plt.subplots_adjust(top=0.93, hspace=0.3, wspace=0.3)

plt.show()

print("=== 바람 데이터 요약 ===")
print(f"전체 데이터 개수: {len(df)}")
print(f"풍속 범위: {df['speed'].min():.1f} - {df['speed'].max():.1f} m/s")
print(f"풍향 범위: {df['direction'].min():.1f} - {df['direction'].max():.1f} degrees")
print(f"평균 풍속: {df['speed'].mean():.2f} m/s")
print(f"최빈 풍향: {df['direction'].mode().values[0]:.1f} degrees")

# %% code 19.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import seaborn as sns

# 풍향 · 풍속을 동서(u) · 남북(v) 성분으로(풍향은 바람이 불어오는 방향이므로 - 부호)
rad = np.deg2rad(df['direction'])
df_uv = pd.DataFrame({'u': -df['speed'] * np.sin(rad),   # 동쪽으로 부는 성분이 +
                      'v': -df['speed'] * np.cos(rad),   # 북쪽으로 부는 성분이 +
                      'speed': df['speed']}, index=df.index)

def mean_wind(rule):
    # u · v는 벡터 평균, 풍속은 산술평균
    m = df_uv.resample(rule).mean().dropna()
    # 평균 u · v를 다시 「불어오는 방향」(0~360°)으로
    m['direction'] = np.rad2deg(np.arctan2(-m['u'], -m['v'])) % 360
    return m[['direction', 'speed']]

# 일평균 · 월평균 바람
df_daily = mean_wind('D')
df_monthly = mean_wind('ME')

fig = plt.figure(figsize=(12, 10))

colors = plt.cm.viridis

# 1) 일평균, 막대형
ax1 = fig.add_subplot(2, 2, 1, projection="windrose")
ax1.bar(df_daily['direction'], df_daily['speed'], normed=True, opening=0.8,
        edgecolor='white', cmap=colors)
ax1.set_legend(title='풍속 (m/s)', loc='upper left', bbox_to_anchor=(1.1, 1))
ax1.set_title('막대형 바람장미 (일평균)', fontsize=14, fontweight='bold', pad=20)

# 2) 월평균, 막대형
ax2 = fig.add_subplot(2, 2, 2, projection="windrose")
ax2.bar(df_monthly['direction'], df_monthly['speed'], normed=True, opening=0.8,
        edgecolor='white', cmap=colors)
ax2.set_legend(title='풍속 (m/s)', loc='upper left', bbox_to_anchor=(1.1, 1))
ax2.set_title('막대형 바람장미 (월평균)', fontsize=14, fontweight='bold', pad=20)

# 3) 일평균, 등고선 채움형
ax3 = fig.add_subplot(2, 2, 3, projection="windrose")
ax3.contourf(df_daily['direction'], df_daily['speed'], normed=True,
            cmap=colors)
ax3.set_legend(title='풍속 (m/s)', loc='upper left', bbox_to_anchor=(1.1, 1))
ax3.set_title('등고선 채움형 바람장미 (일평균)', fontsize=14, fontweight='bold', pad=20)

# 4) 월평균, 등고선 채움형
ax4 = fig.add_subplot(2, 2, 4, projection="windrose")
ax4.contourf(df_monthly['direction'], df_monthly['speed'], normed=True,
            cmap=colors)
ax4.set_legend(title='풍속 (m/s)', loc='upper left', bbox_to_anchor=(1.1, 1))
ax4.set_title('등고선 채움형 바람장미 (월평균)', fontsize=14, fontweight='bold', pad=20)

fig.suptitle('바람장미 분석 - 일평균 vs 월평균 비교',
             fontsize=18, fontweight='bold', y=1.01)

plt.tight_layout()
plt.subplots_adjust(top=0.93, hspace=0.3, wspace=0.3)

plt.show()

print("=== 바람 데이터 요약 ===")
print("\n--- 원본 데이터 ---")
print(f"전체 데이터 개수: {len(df)}")
print(f"풍속 범위: {df['speed'].min():.1f} - {df['speed'].max():.1f} m/s")
print(f"풍향 범위: {df['direction'].min():.1f} - {df['direction'].max():.1f} degrees")
print(f"평균 풍속: {df['speed'].mean():.2f} m/s")

print("\n--- 일평균 데이터 ---")
print(f"일평균 데이터 개수: {len(df_daily)}")
print(f"일평균 풍속 범위: {df_daily['speed'].min():.1f} - {df_daily['speed'].max():.1f} m/s")
print(f"일평균 풍향 범위: {df_daily['direction'].min():.1f} - {df_daily['direction'].max():.1f} degrees")
print(f"일평균 풍속: {df_daily['speed'].mean():.2f} m/s")

print("\n--- 월평균 데이터 ---")
print(f"월평균 데이터 개수: {len(df_monthly)}")
print(f"월평균 풍속 범위: {df_monthly['speed'].min():.1f} - {df_monthly['speed'].max():.1f} m/s")
print(f"월평균 풍향 범위: {df_monthly['direction'].min():.1f} - {df_monthly['direction'].max():.1f} degrees")
print(f"월평균 풍속: {df_monthly['speed'].mean():.2f} m/s")

print("\n--- 월별 바람 데이터 세부사항 ---")
df_monthly_display = df_monthly.copy()
df_monthly_display['Month'] = df_monthly_display.index.strftime('%Y-%m')
for idx, row in df_monthly_display.iterrows():
    print(f"{row['Month']}: 풍향 {row['direction']:.1f}°, 풍속 {row['speed']:.2f} m/s")
