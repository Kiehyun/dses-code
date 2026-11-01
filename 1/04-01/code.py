# 지구과학 데이터 사이언스 1 | IV-01. 기상청 AWS 자료 시각화하기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 1.
from pathlib import Path

fname = "SURFACE_ASOS_116_MI_2018-01_2018-12_2018.zip"
fid = "1THyhljJL8p5mhpnqLKNbU5QPC-bVABOI"

# 구글 드라이브에 공유해 둔 파일 내려받기
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
n_lines = 10  # 출력할 줄 수

print(f"파일 내용 출력 (처음 {n_lines}줄):")
print("="*60)

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

# %% code 5.
# # !head -n 50 {fpaths[0]} # list the first 50 lines of the file
# print(f"파일 {fpaths[0]}의 첫 20줄을 출력합니다:")
# !powershell -Command "Get-Content {fpaths[0]} -TotalCount 20"

# %% code 6.
# print("\n=== Python으로 직접 읽기 ===")
# # Python으로 직접 파일 읽기
# import codecs
# try:
# # UTF-8로 시도
# with open(fpaths[0], 'r', encoding='utf-8') as f:
# lines = f.readlines()[:10]
# print("UTF-8로 성공:")
# for line in lines:
# print(line.strip())
# except:
# try:
# # EUC-KR로 시도
# with open(fpaths[0], 'r', encoding='euc-kr') as f:
# lines = f.readlines()[:10]
# print("EUC-KR로 성공:")
# for line in lines:
# print(line.strip())
# except:
# try:
# # CP949로 시도
# with open(fpaths[0], 'r', encoding='cp949') as f:
# lines = f.readlines()[:10]
# print("CP949로 성공:")
# for line in lines:
# print(line.strip())
# except:
# print("모든 인코딩 시도 실패")

# %% code 7.
# 필요한 라이브러리 불러오기
import pandas as pd

# CSV 읽기 (천단위 ',' 처리, 인코딩: EUC-KR)
df = pd.read_csv(str(fpaths[0]), thousands=',', encoding='euc-kr')

# 데이터프레임 출력하여 데이터 확인
print(f"df :\n{df}")

# %% code 8.
# 전체 월별 파일을 합치기 위한 처리
import pandas as pd

# 빈 DataFrame 생성
df_month = pd.DataFrame()

for fpath in fpaths:
 # 파일 인코딩 확인 및 DataFrame으로 읽기
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        print(f"읽는 중: {fpath.name}, 인코딩: {f.encoding}")
    df_month = pd.read_csv(str(fpath), encoding='euc_kr', sep=',')
    df = pd.concat([df, df_month], ignore_index=True)

# 중복 제거
df = df.drop_duplicates()
print(f"총 레코드 수(중복 제거 후): {len(df)}")
print(f"df :\n{df}")

# %% code 9.
# '일시' 컬럼을 datetime으로 변환하고 인덱스 재설정
print(f"type(df['일시'][0]): {type(df['일시'][0])}")
df['dt_YmdHM'] = pd.to_datetime(df['일시'])
print(f"type(df['dt_YmdHM'][0]): {type(df['dt_YmdHM'][0])}")

# 인덱스를 datetime으로 설정
from datetime import timedelta

df['dt_YmdHM-1min'] = df['dt_YmdHM'] - timedelta(minutes=1)
df.index = df['dt_YmdHM-1min']
print(f"df :\n{df}")

# %% code 10.
from datetime import datetime, timedelta

# 특정 날짜 필터링 예시
df_jan51 = df[df['일시'].str.contains('2018-01-05')]
print(f"df_jan51 :\n{df_jan51}")

df_jan52 = df[df['dt_YmdHM-1min'].dt.date == datetime(2018, 1, 5).date()]
print(f"df_jan52 :\n{df_jan52}")

df_jan53 = df[(df['dt_YmdHM-1min'] >= '2018-01-12 00:00') & (df['dt_YmdHM-1min'] < '2018-01-13 00:00')]
# 필터링된 데이터 출력
print(f"df_jan53 :\n{df_jan53}")

# %% code 11.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime, timedelta

# 그림 사이즈를 가로로 길게 지정
fig, ax1 = plt.subplots(figsize=(12.0, 4.0))

df_jan5 = df_jan52  # df_jan52를 df_jan5로 이름 변경

# 기온 그래프 그리기
Temp_line = ax1.plot(df_jan5['dt_YmdHM-1min'], df_jan5['기온(°C)'], label='기온', color='red')

# 첫 번째 y축 설정 (기온)
ax1.set_xlabel('일시', fontsize = 14)
ax1.set_ylabel('기온 (°C)', fontsize = 14, color='red')
ax1.tick_params(axis='y', labelcolor='red')

# 두 번째 y축 생성 (습도용)
ax2 = ax1.twinx()

# 습도 그래프 그리기
Humi_line = ax2.plot(df_jan5['dt_YmdHM-1min'], df_jan5['습도(%)'], label='습도', color='blue')

# 두 번째 y축 설정 (습도)
ax2.set_ylabel('상대습도 (%)', fontsize = 14, color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

# 그래프 제목 설정
ax1.set_title('2018년 1월 5일의 기온과 상대습도의 변동 (관악산)', 
          y=1.05,   # 제목 아래쪽 여백
          fontdict={'fontsize':18,'fontweight':'bold'})

# x축 레이블 회전 (시간이 겹치지 않도록)
plt.xticks(rotation=45)

# 범례 추가 (두 개의 축에서 범례를 합쳐서 표시)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

# 레이아웃 자동 조정
plt.tight_layout()
plt.show()

# %% code 12.
import pandas as pd
import numpy as np

# 날짜 컬럼 추가 (시간 정보 제거)
df['date'] = df['dt_YmdHM-1min'].dt.date

print(f"\n전체 데이터 개수: {len(df)}")

# 1. 날짜별로 그룹화하여 각 날의 최대 누적 강수량 구하기
daily_max_rainfall = df.groupby('date')['누적강수량(mm)'].max().reset_index()

print("\n날짜별 최대 강수량 미리보기:")
print(daily_max_rainfall.head(10))

# 2. 비가 조금이라도 내린 날 찾기 (강수량 > 0)
rainy_days = daily_max_rainfall[daily_max_rainfall['누적강수량(mm)'] > 0]

print(f"\n비가 내린 날들의 강수량 통계:")
print(rainy_days['누적강수량(mm)'].describe())

# 3. 비가 내린 날의 개수 계산
num_rainy_days = len(rainy_days)
total_days = len(daily_max_rainfall)
percentage = (num_rainy_days / total_days) * 100

print(f"\n=== 결과 ===")
print(f"전체 날짜 수: {total_days}일")
print(f"비가 내린 날 수: {num_rainy_days}일")
print(f"비가 내린 날의 비율: {percentage:.1f}%")

# 4. 추가 분석: 월별 비오는 날 수
df['month'] = df['dt_YmdHM-1min'].dt.month
monthly_rainy_days = df.groupby(['date', 'month'])['누적강수량(mm)'].max().reset_index()
monthly_rainy_days = monthly_rainy_days[monthly_rainy_days['누적강수량(mm)'] > 0]
monthly_count = monthly_rainy_days.groupby('month').size()

print(f"\n월별 비오는 날 수:")
months = ['1월', '2월', '3월', '4월', '5월', '6월', 
          '7월', '8월', '9월', '10월', '11월', '12월']
for month_num, count in monthly_count.items():
    print(f"{months[month_num-1]}: {count}일")

# %% code 13.
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 데이터 전처리 (기존 코드)
df['date'] = df['dt_YmdHM-1min'].dt.date
daily_max_rainfall = df.groupby('date')['누적강수량(mm)'].max().reset_index()
rainy_days = daily_max_rainfall[daily_max_rainfall['누적강수량(mm)'] > 0]
num_rainy_days = len(rainy_days)
total_days = len(daily_max_rainfall)

# 월별 비오는 날 수 계산
df['month'] = df['dt_YmdHM-1min'].dt.month
monthly_rainy_days = df.groupby(['date', 'month'])['누적강수량(mm)'].max().reset_index()
monthly_rainy_days = monthly_rainy_days[monthly_rainy_days['누적강수량(mm)'] > 0]
monthly_count = monthly_rainy_days.groupby('month').size()

# 월별 전체 날짜 수 계산
monthly_total_days = df.groupby('month')['date'].nunique()

# 시각화
fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.6))
fig.suptitle('2018년 강수량 분석 결과', fontsize=16, fontweight='bold')

# 1. 비가 내린 날 vs 비가 안 내린 날 (파이 차트)
ax1 = axes[0, 0]
labels = ['비가 내린 날', '비가 안 내린 날']
sizes = [num_rainy_days, total_days - num_rainy_days]
colors = ['lightblue', 'lightcoral']
explode = (0.1, 0)  # 첫 번째 조각을 약간 분리

wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                   explode=explode, startangle=90, shadow=True)
ax1.set_title(f'전체 {total_days}일 중 비가 내린 날의 비율', fontsize=12, fontweight='bold')

# 2. 월별 비오는 날 수 (막대 그래프)
ax2 = axes[0, 1]
months = ['1월', '2월', '3월', '4월', '5월', '6월', 
          '7월', '8월', '9월', '10월', '11월', '12월']
month_nums = range(1, 13)

# 월별 비오는 날 수 (없는 월은 0으로 처리)
rainy_counts = [monthly_count.get(i, 0) for i in month_nums]

bars = ax2.bar(months, rainy_counts, color='skyblue', alpha=0.7, edgecolor='navy', linewidth=1)
ax2.set_title('월별 비오는 날 수', fontsize=12, fontweight='bold')
ax2.set_ylabel('비오는 날 수')
ax2.set_xlabel('월')
ax2.grid(True, alpha=0.3)

# 막대 위에 숫자 표시
for bar, count in zip(bars, rainy_counts):
    if count > 0:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                str(count), ha='center', va='bottom', fontweight='bold')

ax2.tick_params(axis='x', rotation=45)

# 3. 월별 비오는 날 비율 (선 그래프)
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

# 데이터 포인트에 값 표시
for i, (month, percentage) in enumerate(zip(months, monthly_percentages)):
    ax3.text(i, percentage + 1, f'{percentage:.1f}%', 
             ha='center', va='bottom', fontweight='bold', fontsize=9)

# 4. 강수량 분포 (히스토그램)
ax4 = axes[1, 1]
rainfall_amounts = rainy_days['누적강수량(mm)'].values
ax4.hist(rainfall_amounts, bins=20, color='lightgreen', alpha=0.7, edgecolor='darkgreen')
ax4.set_title('비가 내린 날의 강수량 분포', fontsize=12, fontweight='bold')
ax4.set_xlabel('누적강수량 (mm)')
ax4.set_ylabel('빈도')
ax4.grid(True, alpha=0.3)

# 통계 정보 추가
mean_rainfall = rainfall_amounts.mean()
ax4.axvline(mean_rainfall, color='red', linestyle='--', linewidth=2, 
            label=f'평균: {mean_rainfall:.1f}mm')
ax4.legend()

plt.tight_layout()
plt.show()

# 추가 분석: 계절별 비오는 날 통계
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

# 강수량 통계 요약
print(f"\n=== 강수량 통계 요약 ===")
print(f"비가 내린 날 수: {num_rainy_days}일")
print(f"평균 강수량: {rainy_days['누적강수량(mm)'].mean():.2f}mm")
print(f"최대 강수량: {rainy_days['누적강수량(mm)'].max():.2f}mm")
print(f"최소 강수량: {rainy_days['누적강수량(mm)'].min():.2f}mm")
print(f"중간값: {rainy_days['누적강수량(mm)'].median():.2f}mm")

# %% code 14.
import pandas as pd
import numpy as np
from datetime import datetime

def calculate_temperature_averages(df, datetime_col='dt_YmdHM-1min', temp_col='기온(°C)'):
    """
    일평균 기온과 월평균 기온을 두 가지 방법으로 계산
    
    Parameters:
    df: DataFrame with datetime and temperature columns
    datetime_col: 날짜시간 컬럼명
    temp_col: 기온 컬럼명
    """
    
 # 날짜시간 컬럼을 datetime 형식으로 변환
    df[datetime_col] = pd.to_datetime(df[datetime_col])
    
 # 날짜별로 그룹화하기 위한 date 컬럼 생성
    df['date'] = df[datetime_col].dt.date
    df['year_month'] = df[datetime_col].dt.to_period('M')
    
 # ========== 방법 1: 일최고/일최저 기온의 산술평균 ==========
    print("=" * 50)
    print("방법 1: 일최고/일최저 기온의 산술평균")
    print("=" * 50)
    
 # 일별 최고/최저 기온 계산
    daily_extremes = df.groupby('date')[temp_col].agg(['min', 'max']).reset_index()
    daily_extremes.columns = ['date', 'daily_min', 'daily_max']
    
 # 일평균 기온 계산 (최고+최저)/2
    daily_extremes['daily_avg_method1'] = (daily_extremes['daily_min'] + daily_extremes['daily_max']) / 2
    
    print("일별 최고/최저 기온 및 일평균 기온:")
    print(daily_extremes.head(10))
    
 # 월평균 기온 계산 (일평균들의 평균)
    daily_extremes['year_month'] = pd.to_datetime(daily_extremes['date']).dt.to_period('M')
    monthly_avg_method1 = daily_extremes.groupby('year_month')['daily_avg_method1'].mean().reset_index()
    monthly_avg_method1.columns = ['year_month', 'monthly_avg_method1']
    
    print("\n월평균 기온 (방법 1):")
    print(monthly_avg_method1)
    
 # ========== 방법 2: 모든 관측값의 직접 평균 ==========
    print("\n" + "=" * 50)
    print("방법 2: 모든 관측값의 직접 평균")
    print("=" * 50)
    
 # 일평균 기온 계산 (해당 날짜의 모든 관측값 평균)
    daily_avg_method2 = df.groupby('date')[temp_col].mean().reset_index()
    daily_avg_method2.columns = ['date', 'daily_avg_method2']
    
    print("일평균 기온 (모든 관측값 평균):")
    print(daily_avg_method2.head(10))
    
 # 월평균 기온 계산 (해당 월의 모든 관측값 평균)
    monthly_avg_method2 = df.groupby('year_month')[temp_col].mean().reset_index()
    monthly_avg_method2.columns = ['year_month', 'monthly_avg_method2']
    
    print("\n월평균 기온 (방법 2):")
    print(monthly_avg_method2)
    
 # ========== 두 방법 비교 ==========
    print("\n" + "=" * 50)
    print("두 방법 비교")
    print("=" * 50)
    
 # 일평균 기온 비교
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
    
 # 월평균 기온 비교
    monthly_comparison = pd.merge(monthly_avg_method1, monthly_avg_method2, on='year_month')
    monthly_comparison['monthly_difference'] = monthly_comparison['monthly_avg_method1'] - monthly_comparison['monthly_avg_method2']
    
    print("\n월평균 기온 비교:")
    print(monthly_comparison)
    print(f"\n월평균 기온 차이 통계:")
    print(f"평균 차이: {monthly_comparison['monthly_difference'].mean():.3f}°C")
    print(f"최대 차이: {monthly_comparison['monthly_difference'].max():.3f}°C")
    print(f"최소 차이: {monthly_comparison['monthly_difference'].min():.3f}°C")
    print(f"표준편차: {monthly_comparison['monthly_difference'].std():.3f}°C")
    
 # 결과 반환
    results = {
        'daily_method1': daily_extremes,
        'daily_method2': daily_avg_method2,
        'monthly_method1': monthly_avg_method1,
        'monthly_method2': monthly_avg_method2,
        'daily_comparison': daily_comparison,
        'monthly_comparison': monthly_comparison
    }
    
    return results

# 시각화 함수
def plot_temperature_comparison(results):
    """
    두 방법의 결과를 시각화
    """
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib import font_manager
    
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.6))
    fig.suptitle('기온 계산 방법 비교', fontsize=16, fontweight='bold')
    
 # 일평균 기온 비교
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
    
 # 일평균 기온 차이
    axes[0, 1].plot(dates, daily_comp['daily_difference'], color='red', alpha=0.7)
    axes[0, 1].set_title('일평균 기온 차이 (방법1 - 방법2)', fontsize=14, fontweight='bold')
    axes[0, 1].set_ylabel('기온 차이 (°C)')
    axes[0, 1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    axes[0, 1].grid(True, alpha=0.3)
    
 # 월평균 기온 비교
    monthly_comp = results['monthly_comparison']
    month_labels = [str(ym) for ym in monthly_comp['year_month']]
    
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
    
 # 월평균 기온 차이
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

# 함수 실행
results = calculate_temperature_averages(df, 'dt_YmdHM-1min', '기온(°C)')

# 시각화
plot_temperature_comparison(results)

# %% code 15.
# resample 메서드의 반환 타입 확인 (DatetimeIndexResampler 객체)
print("type(df.resample('D'): {}".format(type(df.resample('D'))))
print("df.resample('D') :", df.resample('D'))

# 일별('D') 단위로 리샘플링하여 각 날짜별 최댓값 계산
df_daily_max = df.resample('D').max()
print("df_daily_max :\n{}".format(df_daily_max))

# %% code 16.
print(f"원본 데이터 형태: {df.shape}")
print(f"인덱스 타입: {type(df.index)}")
print(f"인덱스 빈도: {df.index.freq}")
print(f"인덱스 범위: {df.index.min()} ~ {df.index.max()}")
print("\n원본 데이터 샘플:")
print(df.head())

# 2. DatetimeIndex 속성 확인
print("\n=== 2. DatetimeIndex 속성 확인 ===")
print(f"연도: {df.index.year[:5].values}")
print(f"월: {df.index.month[:5].values}")
print(f"일: {df.index.day[:5].values}")
print(f"요일: {df.index.dayofweek[:5].values}")  # 0=월요일, 6=일요일
print(f"요일명: {df.index.day_name()[:5].values}")

# 3. 월별 리샘플링 (다운샘플링)
print("\n=== 3. 월별 리샘플링 (다운샘플링) ===")
# 월 시작일 기준으로 리샘플링
df_monthly_start = df.resample('MS').agg({
    '기온(°C)': 'mean',
    '습도(%)': 'mean'
})

# 월 마지막일 기준으로 리샘플링
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

# 4. 주별 리샘플링
print("\n=== 4. 주별 리샘플링 ===")
df_weekly = df.resample('W').agg({
    '기온(°C)': 'mean',
    '습도(%)': 'mean'
})

print(f"주별 리샘플링 후 데이터 형태: {df_weekly.shape}")
print(f"주별 리샘플링 후 인덱스 빈도: {df_weekly.index.freq}")
print("\n주별 리샘플링 결과:")
print(df_weekly.head())

print("="*30) # 데이터를 읽기 쉽게 구분해줌.
print("df.index: {}".format(df.index))

print("="*30) # 데이터를 읽기 쉽게 구분해줌.
print("type(df.resample('ME').max()): {}".format(type(df.resample('ME').max())))

print("="*30) # 데이터를 읽기 쉽게 구분해줌.
print("df.resample('ME').max().index: {}".format(df.resample('ME').max().index))

print("="*30) # 데이터를 읽기 쉽게 구분해줌.
print("df.resample('ME').max().index.month: {}".format(df.resample('ME').max().index.month))
print("df.resample('ME').max().index.month_name(): {}".format(df.resample('ME').max().index.month_name()))
print(f"YYYY-MM: {df.resample('ME').max().index.strftime('%Y-%m')[:5].values}")
print(f"Month Year: {df.resample('ME').max().index.strftime('%B %Y')[:5].values}")

# %% code 17.
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


# 일별 통계 데이터 생성 (기존 일별 데이터 활용)
daily_stats = df.copy()
daily_stats['기온범위'] = \
      daily_stats['기온(°C)'].rolling(window=1).max() \
      - daily_stats['기온(°C)'].rolling(window=1).min()

# 일별 최고/최저 기온 계산 (7일 이동평균으로 스무딩)
daily_stats['일평균기온'] = daily_stats['기온(°C)']
daily_stats['일최고기온'] = daily_stats['기온(°C)'].rolling(window=7).max()
daily_stats['일최저기온'] = daily_stats['기온(°C)'].rolling(window=7).min()
daily_stats['일평균습도'] = daily_stats['습도(%)']

print("일별 통계 데이터:")
print(daily_stats[['일평균기온', '일최고기온', '일최저기온', '일평균습도']].head())
print(f"\n데이터 형태: {daily_stats.shape}")

# 시각화 - 3행 2열로 변경
plt.figure(figsize=(12.0, 10.0))

# 1행 1열: 일별 기온 분포 (박스플롯)
plt.subplot(3, 2, 1)
box_data = [daily_stats['일평균기온'].dropna(), 
           daily_stats['일최고기온'].dropna(), 
           daily_stats['일최저기온'].dropna()]
box_labels = ['일평균기온', '일최고기온', '일최저기온']
colors = ['lightblue', 'lightcoral', 'lightcyan']

bp = plt.boxplot(box_data, labels=box_labels, patch_artist=True)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
plt.title('일별 기온 분포 (박스플롯)', fontsize=14, fontweight='bold')
plt.ylabel('기온 (°C)')
plt.grid(True, alpha=0.3)

# 1행 2열: 연도별 일평균 기온 히트맵 (월별 집계)
plt.subplot(3, 2, 2)
# 연도와 월 정보 추가
daily_stats_copy = daily_stats.copy()
daily_stats_copy['연도'] = daily_stats_copy.index.year
daily_stats_copy['월'] = daily_stats_copy.index.month

# 피벗 테이블 생성 (일별 데이터를 월별로 평균)
heatmap_data = daily_stats_copy.groupby(['연도', '월'])['일평균기온'].mean().unstack()

sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='RdYlBu_r', 
            cbar_kws={'label': '기온 (°C)'})
plt.title('연도별 일평균 기온 히트맵 (월별 집계)', fontsize=14, fontweight='bold')
plt.xlabel('월')
plt.ylabel('연도')

# 2행 1-2열: 일별 기온 변화 (시계열) - 넓게 그리기
plt.subplot(3, 2, (3, 4))  # 3번과 4번 위치를 합쳐서 사용
plt.plot(daily_stats.index, daily_stats['일평균기온'], 
         linewidth=1, label='일평균기온', color='blue', alpha=0.7)
plt.plot(daily_stats.index, daily_stats['일최고기온'], 
         linewidth=1, label='일최고기온(7일 이동평균)', color='red', alpha=0.7)
plt.plot(daily_stats.index, daily_stats['일최저기온'], 
         linewidth=1, label='일최저기온(7일 이동평균)', color='cyan', alpha=0.7)
plt.title('일별 기온 변화 (시계열)', fontsize=14, fontweight='bold')
plt.xlabel('날짜')
plt.ylabel('기온 (°C)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

# 3행 1-2열: 일별 기온 범위 (영역 그래프, 7일 간격 샘플링) - 넓게 그리기
plt.subplot(3, 2, (5, 6))  # 5번과 6번 위치를 합쳐서 사용
daily_stats['기온범위'] = daily_stats['일최고기온'] - daily_stats['일최저기온']

# 영역 그래프 (데이터가 많으므로 샘플링)
sample_idx = daily_stats.index[::7]  # 7일마다 샘플링
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

# 추가 분석: 통계 요약
print("\n=== 일별 기온 통계 요약 ===")
print(f"전체 기간 평균기온: {daily_stats['일평균기온'].mean():.2f}°C")
print(f"전체 기간 최고기온: {daily_stats['일평균기온'].max():.2f}°C")
print(f"전체 기간 최저기온: {daily_stats['일평균기온'].min():.2f}°C")
print(f"평균 기온 범위: {daily_stats['기온범위'].mean():.2f}°C")

# 극값 찾기
max_temp_date = daily_stats['일평균기온'].idxmax()
min_temp_date = daily_stats['일평균기온'].idxmin()
print(f"\n최고 기온 기록: {daily_stats.loc[max_temp_date, '일평균기온']:.2f}°C \
        ({max_temp_date.strftime('%Y년 %m월 %d일')})")
print(f"최저 기온 기록: {daily_stats.loc[min_temp_date, '일평균기온']:.2f}°C \
        ({min_temp_date.strftime('%Y년 %m월 %d일')})")

# 계절별 평균 (선택사항)
print("\n=== 계절별 평균 기온 ===")
seasonal_avg = daily_stats.groupby(daily_stats.index.month).agg({
    '일평균기온': 'mean',
    '일최고기온': 'mean',
    '일최저기온': 'mean'
})

# 계절 정의
seasons = {1: '겨울', 2: '겨울', 3: '봄', 4: '봄', 5: '봄', 6: '여름',
          7: '여름', 8: '여름', 9: '가을', 10: '가을', 11: '가을', 12: '겨울'}

for month, row in seasonal_avg.iterrows():
    season = seasons[month]
    print(f"{month}월 ({season}): 평균 {row['일평균기온']:.1f}°C, "
          f"최고 {row['일최고기온']:.1f}°C, 최저 {row['일최저기온']:.1f}°C")

# 추가: 일별 기온 변화율 분석
print("\n=== 일별 기온 변화 분석 ===")
daily_stats['기온변화'] = daily_stats['일평균기온'].diff()
print(f"평균 일일 기온 변화: {daily_stats['기온변화'].mean():.2f}°C")
print(f"최대 일일 기온 상승: {daily_stats['기온변화'].max():.2f}°C")
print(f"최대 일일 기온 하락: {daily_stats['기온변화'].min():.2f}°C")

# %% code 18.
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 월별 통계 데이터 생성
monthly_stats = df.resample('ME').agg({
    '기온(°C)': ['mean', 'max', 'min'],
    '습도(%)': 'mean'
})

# 컬럼명 정리
monthly_stats.columns = ['월평균기온', '월최고기온', '월최저기온', '월평균습도']

print("월별 통계 데이터:")
print(monthly_stats.head())
print(f"\n데이터 형태: {monthly_stats.shape}")

# 시각화
plt.figure(figsize=(12.0, 8.0))

# 1. 월평균, 최고, 최저 기온 시계열 그래프
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

# 2. 월평균, 최고, 최저 기온 박스플롯
plt.subplot(2, 2, 2)
box_data = [monthly_stats['월평균기온'], monthly_stats['월최고기온'], monthly_stats['월최저기온']]
box_labels = ['월평균기온', '월최고기온', '월최저기온']
colors = ['lightblue', 'lightcoral', 'lightcyan']

bp = plt.boxplot(box_data, labels=box_labels, patch_artist=True)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
plt.title('월별 기온 분포 (박스플롯)', fontsize=14, fontweight='bold')
plt.ylabel('기온 (°C)')
plt.grid(True, alpha=0.3)

# 3. 월별 평균 기온 히트맵 (연도별 x 월별)
plt.subplot(2, 2, 3)
# 연도와 월 정보 추가
monthly_stats_copy = monthly_stats.copy()
monthly_stats_copy['연도'] = monthly_stats_copy.index.year
monthly_stats_copy['월'] = monthly_stats_copy.index.month

# 피벗 테이블 생성
heatmap_data = monthly_stats_copy.pivot_table(
    values='월평균기온', index='연도', columns='월', aggfunc='mean'
)

sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='RdYlBu_r', 
            cbar_kws={'label': '기온 (°C)'})
plt.title('연도별 월평균 기온 히트맵', fontsize=14, fontweight='bold')
plt.xlabel('월')
plt.ylabel('연도')

# 4. 월별 기온 범위 (최고-최저) 시각화
plt.subplot(2, 2, 4)
monthly_stats['기온범위'] = monthly_stats['월최고기온'] - monthly_stats['월최저기온']

# 영역 그래프
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

# 추가 분석: 통계 요약
print("\n=== 월별 기온 통계 요약 ===")
print(f"전체 기간 평균기온: {monthly_stats['월평균기온'].mean():.2f}°C")
print(f"전체 기간 최고기온: {monthly_stats['월최고기온'].max():.2f}°C")
print(f"전체 기간 최저기온: {monthly_stats['월최저기온'].min():.2f}°C")
print(f"평균 기온 범위: {monthly_stats['기온범위'].mean():.2f}°C")

# 극값 찾기
max_temp_date = monthly_stats['월최고기온'].idxmax()
min_temp_date = monthly_stats['월최저기온'].idxmin()
print(f"\n최고 기온 기록: {monthly_stats.loc[max_temp_date, '월최고기온']:.2f}°C ({max_temp_date.strftime('%Y년 %m월')})")
print(f"최저 기온 기록: {monthly_stats.loc[min_temp_date, '월최저기온']:.2f}°C ({min_temp_date.strftime('%Y년 %m월')})")

# 계절별 평균 (선택사항)
print("\n=== 계절별 평균 기온 ===")
seasonal_avg = monthly_stats.groupby(monthly_stats.index.month).agg({
    '월평균기온': 'mean',
    '월최고기온': 'mean',
    '월최저기온': 'mean'
})

# 계절 정의
seasons = {1: '겨울', 2: '겨울', 3: '봄', 4: '봄', 5: '봄', 6: '여름',
          7: '여름', 8: '여름', 9: '가을', 10: '가을', 11: '가을', 12: '겨울'}

for month, row in seasonal_avg.iterrows():
    season = seasons[month]
    print(f"{month}월 ({season}): 평균 {row['월평균기온']:.1f}°C, "
          f"최고 {row['월최고기온']:.1f}°C, 최저 {row['월최저기온']:.1f}°C")

# %% code 19.
import numpy as np

# 풍속과 풍향 변수 생성
ws = np.random.random(100) * 6        # 최대 풍속을 6 m/s까지 랜덤하게 생성
wd = 80 + np.random.random(100) * 20  # 풍향을 90도 ± 10도 범위로 랜덤하게 생성

print("ws : {}".format(ws))
print("wd : {}".format(wd))

from matplotlib import pyplot as plt
from windrose import WindroseAxes

# 바람장미 그래프를 그리기 위한 좌표축 정의
ax = WindroseAxes.from_ax()

# 막대(bar) 형태로 바람장미 그리기
ax.bar(wd, ws)

# %% code 20.
# DataFrame에 바람장미 그래프 생성을 위한 표준 컬럼명 추가
df['speed'] = df['풍속(m/s)']      # 풍속 데이터를 'speed' 컬럼으로 복사
df['direction'] = df['풍향(deg)']  # 풍향 데이터를 'direction' 컬럼으로 복사

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import seaborn as sns

# 2행 2열 서브플롯 생성 (16x12 인치 크기)
fig = plt.figure(figsize=(12, 10))

# 바람장미 그래프에 사용할 색상 팔레트 설정 (viridis 컬러맵)
colors = plt.cm.viridis

# 1. Bar 형태 바람장미 (좌상단)
ax1 = fig.add_subplot(2, 2, 1, projection="windrose")  # windrose 프로젝션으로 서브플롯 생성
ax1.bar(df['direction'], df['speed'], normed=True, opening=0.8, 
        edgecolor='white', cmap=colors)  # 막대형 바람장미 그리기
ax1.set_legend(title='풍속 (m/s)', loc='upper left', bbox_to_anchor=(1.1, 1))  # 범례 설정
ax1.set_title('막대형 바람장미', fontsize=14, fontweight='bold', pad=20)  # 제목 설정

# 2. Box 형태 바람장미 (우상단)
ax2 = fig.add_subplot(2, 2, 2, projection="windrose")
ax2.box(df['direction'], df['speed'], normed=True, cmap=colors)  # 박스형 바람장미 그리기
ax2.set_legend(title='풍속 (m/s)', loc='upper left', bbox_to_anchor=(1.1, 1))
ax2.set_title('박스형 바람장미', fontsize=14, fontweight='bold', pad=20)

# 3. Contourf 형태 바람장미 (좌하단)
ax3 = fig.add_subplot(2, 2, 3, projection="windrose")
ax3.contourf(df['direction'], df['speed'], normed=True, cmap=colors)  # 등고선 채움형 바람장미 그리기
ax3.set_legend(title='풍속 (m/s)', loc='upper left', bbox_to_anchor=(1.1, 1))
ax3.set_title('등고선 채움형 바람장미', fontsize=14, fontweight='bold', pad=20)

# 4. Contour 형태 바람장미 (우하단)
ax4 = fig.add_subplot(2, 2, 4, projection="windrose")
ax4.contour(df['direction'], df['speed'], normed=True, cmap=colors)  # 등고선형 바람장미 그리기
ax4.set_legend(title='풍속 (m/s)', loc='upper left', bbox_to_anchor=(1.1, 1))
ax4.set_title('등고선형 바람장미', fontsize=14, fontweight='bold', pad=20)

# 전체 그래프의 제목 설정
fig.suptitle('바람장미 분석 - 4가지 시각화 유형 비교', 
             fontsize=18, fontweight='bold', y=1.01)

# 레이아웃 자동 조정
plt.tight_layout()
plt.subplots_adjust(top=0.93, hspace=0.3, wspace=0.3)  # 서브플롯 간격 조정

# 그래프 화면에 출력
plt.show()

# 바람 데이터 기본 통계 정보 출력
print("=== 바람 데이터 요약 ===")
print(f"전체 데이터 개수: {len(df)}")
print(f"풍속 범위: {df['speed'].min():.1f} - {df['speed'].max():.1f} m/s")
print(f"풍향 범위: {df['direction'].min():.1f} - {df['direction'].max():.1f} degrees")
print(f"평균 풍속: {df['speed'].mean():.2f} m/s")
print(f"최빈 풍향: {df['direction'].mode().values[0]:.1f} degrees")

# %% code 21.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import seaborn as sns

# 데이터 준비
# 일평균 데이터 계산
df_daily = df.resample('D').agg({
    'direction': 'mean',
    'speed': 'mean'
}).dropna()

# 월평균 데이터 계산
df_monthly = df.resample('ME').agg({
    'direction': 'mean',
    'speed': 'mean'
}).dropna()

# 2행 2열 서브플롯 생성
fig = plt.figure(figsize=(12, 10))

# 색상 팔레트 설정
colors = plt.cm.viridis

# 1행 1열 - 일평균 Bar 형태
ax1 = fig.add_subplot(2, 2, 1, projection="windrose")
ax1.bar(df_daily['direction'], df_daily['speed'], normed=True, opening=0.8, 
        edgecolor='white', cmap=colors)
ax1.set_legend(title='풍속 (m/s)', loc='upper left', bbox_to_anchor=(1.1, 1))
ax1.set_title('막대형 바람장미 (일평균)', fontsize=14, fontweight='bold', pad=20)

# 1행 2열 - 월평균 Bar 형태
ax2 = fig.add_subplot(2, 2, 2, projection="windrose")
ax2.bar(df_monthly['direction'], df_monthly['speed'], normed=True, opening=0.8, 
        edgecolor='white', cmap=colors)
ax2.set_legend(title='풍속 (m/s)', loc='upper left', bbox_to_anchor=(1.1, 1))
ax2.set_title('막대형 바람장미 (월평균)', fontsize=14, fontweight='bold', pad=20)

# 2행 1열 - 일평균 Contourf 형태
ax3 = fig.add_subplot(2, 2, 3, projection="windrose")
ax3.contourf(df_daily['direction'], df_daily['speed'], 
            normed=True,
            cmap=colors)
ax3.set_legend(title='풍속 (m/s)', loc='upper left', bbox_to_anchor=(1.1, 1))
ax3.set_title('등고선 채움형 바람장미 (일평균)', fontsize=14, fontweight='bold', pad=20)

# 2행 2열 - 월평균 Contourf 형태
ax4 = fig.add_subplot(2, 2, 4, projection="windrose")
ax4.contourf(df_monthly['direction'], df_monthly['speed'], 
            normed=True,
            cmap=colors)
ax4.set_legend(title='풍속 (m/s)', loc='upper left', bbox_to_anchor=(1.1, 1))
ax4.set_title('등고선 채움형 바람장미 (월평균)', fontsize=14, fontweight='bold', pad=20)

# 전체 제목 설정
fig.suptitle('바람장미 분석 - 일평균 vs 월평균 비교', 
             fontsize=18, fontweight='bold', y=1.01)

# 레이아웃 조정
plt.tight_layout()
plt.subplots_adjust(top=0.93, hspace=0.3, wspace=0.3)

# 그래프 출력
plt.show()

# 데이터 기본 정보 출력
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

# 월별 데이터 상세 정보
print("\n--- 월별 바람 데이터 세부사항 ---")
df_monthly_display = df_monthly.copy()
df_monthly_display['Month'] = df_monthly_display.index.strftime('%Y-%m')
for idx, row in df_monthly_display.iterrows():
    print(f"{row['Month']}: 풍향 {row['direction']:.1f}°, 풍속 {row['speed']:.2f} m/s")
