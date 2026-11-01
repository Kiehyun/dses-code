# 지구과학 데이터 사이언스 1 | IV-07. 엘니뇨와 남방진동
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 104.
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import numpy as np

# 1행 2행으로 subplot 생성 (1행: 전체 세계지도, 2행: ENSO 영역 지도)
fig = plt.figure(figsize=(10, 10))

# 1행: 전체 세계 지도
ax1 = fig.add_subplot(2, 1, 1, projection=ccrs.PlateCarree(central_longitude=180))
ax1.set_global()
ax1.stock_img()
ax1.set_title("세계 지도", fontsize=14)

# 2행: ENSO 영역 지도
ax2 = fig.add_subplot(2, 1, 2, projection=ccrs.PlateCarree(central_longitude=180))
ax2.set_extent([120, 300, -30, 30], crs=ccrs.PlateCarree())
ax2.stock_img()

# 격자선 및 레이블 설정
gl = ax2.gridlines(
    crs=ccrs.PlateCarree(),
    draw_labels=True,
    linewidth=0.5, color='gray',
    alpha=0.5, linestyle='--'
)
gl.top_labels = False
gl.xlocator = mticker.FixedLocator(np.arange(-180, 180, 30))
gl.ylocator = mticker.FixedLocator(np.arange(-90, 90, 15))
gl.xformatter = LongitudeFormatter()
gl.yformatter = LatitudeFormatter()
gl.xlabel_style = {'size': 8, 'color': 'k'}
gl.ylabel_style = {'size': 8, 'color': 'k'}

# 주요 도시(Darwin, Tahiti) 위치 표시
latDarwin, lonDarwin = -12, 130
latTahiti, lonTahiti = -17, -149

ax2.scatter(lonDarwin, latDarwin, color='red', marker='o', transform=ccrs.PlateCarree())
ax2.text(lonDarwin, latDarwin-5, "Darwin", color='red', fontsize=8, transform=ccrs.PlateCarree())

ax2.scatter(lonTahiti, latTahiti, color='red', marker='o', transform=ccrs.PlateCarree())
ax2.text(lonTahiti, latTahiti-5, "Tahiti", color='red', fontsize=8, transform=ccrs.PlateCarree())

# ENSO 관련 해역(니뇨 영역) 경계선 좌표 정의
latsNino1 = [0, -10, -10, 0, 0]
lonsNino1 = [-90, -90, -80, -80, -90]
latsNino3 = [5, -5, -5, 5, 5]
lonsNino3 = [-150, -150, -90, -90, -150]
latsNino34 = [5, -5, -5, 5, 5]
lonsNino34 = [-170, -170, -120, -120, -170]
latsNino4 = [5, -5, -5, 5, 5]
lonsNino4 = [-200, -200, -150, -150, -200]

# 각 영역 경계선 및 라벨 표시
ax2.plot(lonsNino1, latsNino1, color='black', linewidth=0.75, transform=ccrs.Geodetic())
ax2.text(lonsNino1[0], latsNino1[1]-4, "NINO 1+2", color='black', fontsize=8, transform=ccrs.PlateCarree())

ax2.plot(lonsNino3, latsNino3, color='orange', linewidth=0.75, transform=ccrs.Geodetic())
ax2.text((lonsNino3[0]+lonsNino3[2])/2, latsNino3[1]-4, "NINO 3", color='orange', fontsize=8, transform=ccrs.PlateCarree())

ax2.plot(lonsNino34, latsNino34, color='purple', linewidth=0.75, transform=ccrs.Geodetic())
ax2.text((lonsNino34[0]+lonsNino34[2])/2, latsNino34[0]+3, "NINO 3.4", color='purple', fontsize=8, transform=ccrs.PlateCarree())

ax2.plot(lonsNino4, latsNino4, color='blue', linewidth=0.75, transform=ccrs.Geodetic())
ax2.text((lonsNino4[0]+lonsNino4[2])/2, latsNino4[1]-3.5, "NINO 4", color='blue', fontsize=8, transform=ccrs.PlateCarree())

ax2.set_title("ENSO 관련 해역(니뇨 영역)", fontsize=14) 
# 그래프 레이아웃 조정
plt.tight_layout()          

plt.savefig(f"{proj_dir}/ENSO_map.png", dpi=300, bbox_inches='tight')  # 저장
plt.show()  # 그래프 출력

# %% code 105.
fname1 = "ENSO.csv"
fid1 = "1QkkjxaXMhiaurtA2RxV7XUxonZoDwmIr"

fname2 = "SOI.signal.txt"
fid2 = "1n2ZOOvFh6gm0VGc70j3OlzfCkgOvbuKr"

#requests 라이브러리를 이용(나의 구글드라이브에서 공유한 파일을 구글 코랩에서 사용할 경우)
from pathlib import Path

# ENSO/SOI는 주기적으로 갱신되는 피드이므로 항상 최신으로 새로 받습니다.
du.download(f"https://docs.google.com/uc?export=download&id={fid1}", Path(proj_dir) / fname1, overwrite=True)
du.download(f"https://docs.google.com/uc?export=download&id={fid2}", Path(proj_dir) / fname2, overwrite=True)

# %% code 106.
fpaths = du.list_files(proj_dir, ["csv", "txt"])

# %% code 107.
n_lines = 10  # 출력할 줄 수

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

# %% code 108.
n_lines = 10  # 출력할 줄 수

print(f"파일 내용 출력 (처음 {n_lines}줄):")
print("="*40)

# 순수 파이썬으로 구현 (운영체제 무관)
try:
    with open(fpaths[1], encoding='utf-8') as f:
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

# %% code 109.
import pandas as pd
import numpy as np

#파일 인코딩을 확인해 보자.
with open(fpaths[0]) as f:
    print("f.encoding:", f.encoding)
    encoding = f.encoding

# 일반적인 csv 파일 불러오기
df_Kaggle = pd.read_csv(fpaths[0],
 # encoding = encoding,
                encoding = "euc_kr", 
                )

df_Kaggle['dt_date'] = pd.to_datetime(df_Kaggle['Date'])
df_Kaggle.index = df_Kaggle['dt_date']

df_Kaggle = df_Kaggle.mask(df_Kaggle['ONI'] == -99.9, np.nan)

print("df_Kaggle : \n", df_Kaggle)

# %% code 110.
import numpy as np

arr = np.loadtxt(fpaths[1],
 #delimiter=' ', 
			    )
print("arr.shape :", arr.shape)
print("arr : \n", arr)

arr1 = arr[:,1:]
print("arr1.shape :", arr1.shape)
print("arr1 : \n", arr1)

arr2 = arr1.reshape(-1)  # 1차원으로 펼침
print("arr2.shape :", arr2.shape)
print("arr2 : \n", arr2)

from datetime import datetime
from dateutil.relativedelta import relativedelta

StartDtStr = "1866-01-01"
EndDTStr = "2023-1-1"

StartDT = datetime.strptime(StartDtStr, "%Y-%m-%d")
EndDT = datetime.strptime(EndDTStr, "%Y-%m-%d")

date1 = StartDT
proc_dates = []
while date1 < EndDT:
    proc_dates.append(date1)
    date1 +=  relativedelta(months=1)

print("len(proc_dates): {}".format(len(proc_dates)))
print(f"proc_dates: {proc_dates}")

# %% code 111.
# import pandas as pd
import pandas as pd
 
# 리스트로 DataFrame 만들기
df_SOI = pd.DataFrame(list(zip(proc_dates, arr2)),
                  columns = ["date", "SOI"],
              )
df_SOI['dt_date'] = pd.to_datetime(df_SOI['date'])
df_SOI.index = df_SOI['dt_date']
df_SOI['SOI'] = df_SOI['SOI'].replace(-99.9, np.nan)
print("df_SOI :", df_SOI)

# %% code 112.
# 필요한 라이브러리 불러오기
import matplotlib.pyplot as plt
from matplotlib import rc

# 예시 그래프
fig, ax = plt.subplots(figsize=(12.0, 4.0))
ax.plot(df_Kaggle['dt_date'], df_Kaggle['ONI'].astype(float), label='ONI')
ax.set_title('니뇨 3.4 지역의 해양 엘니뇨 지수(ONI)', fontsize=18, fontweight='bold')
ax.set_xlabel('시간(년)', fontsize=14)
ax.set_ylabel('수온 편차 (°C)', fontsize=14)
plt.show()

# %% code 113.
import matplotlib.pyplot as plt

# 그림 사이즈를 가로로 길게 지정
fig, ax = plt.subplots(figsize=(12.0, 4.0))

ax.plot(df_Kaggle['dt_date'], df_Kaggle['ONI'].astype(float), "k-", linewidth=0.5)
#ax.plot(df_Kaggle['dt_date'], df_Kaggle['SOI'], "k-")

ax.set_xlim([df_Kaggle['dt_date'].min(), df_Kaggle['dt_date'].max()])
ax.set_ylim([-3, 3])

ax.axhline(y = 0, color = 'black', linestyle = '-')

ax.fill_between(df_Kaggle['dt_date'], df_Kaggle['ONI'].astype(float), 1,
                where=df_Kaggle['ONI'].astype(float) > 1,
                color='red', alpha=0.7,
                )

ax.fill_between(df_Kaggle['dt_date'], df_Kaggle['ONI'].astype(float), -1,
                where= df_Kaggle['ONI'].astype(float) < -1,
                color='blue', alpha=0.7,
                )
ax.grid()
ax.set_xlabel(r'시간(년)', fontsize = 14)
ax.set_ylabel(r'수온 편차 ($\rm{^{\circ C}}$)', fontsize = 14)

ax.set_title('니뇨 3.4 지역의 해양 엘니뇨 지수(ONI)',
          y=1.05,   # 제목 아래 여백
          fontdict={'fontsize':18,'fontweight':'bold'})

fig.tight_layout()
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0.1)

plt.show()

# %% code 114.
import matplotlib.pyplot as plt

# 그림 사이즈를 가로로 길게 지정
fig, ax = plt.subplots(figsize=(12.0, 4.0))

ax.plot(df_SOI['dt_date'], df_SOI['SOI'].astype(float), "k-", linewidth=0.5)
#ax.plot(dfSubset['dt_date'], dfSubset['SOI'], "k-")

ax.set_xlabel(r'시간(년)', fontsize = 16)
ax.set_ylabel(r'기압 편차 ($\rm{hPa}$)', fontsize = 16)

ax.set_xlim([df_SOI['dt_date'].min(), df_SOI['dt_date'].max()])
ax.set_ylim([-6, 6])

ax.axhline(y = 0, color = 'black', linestyle = '-')

ax.fill_between(df_SOI['dt_date'], df_SOI['SOI'].astype(float), 0, 
                where= df_SOI['SOI'].astype(float) > 0,
                color='blue', alpha=0.7,
                )

ax.fill_between(df_SOI['dt_date'], df_SOI['SOI'].astype(float), 0, 
                where= df_SOI['SOI'].astype(float) < 0,
                color='red', alpha=0.7,
                )
ax.grid()
ax.set_title('다윈과 타히티의 기압 편차(SOI)', 
          y=1.05,   # 제목 아래 여백
          fontdict={'fontsize':18,'fontweight':'bold'})

plt.setp(ax.get_xticklabels(), fontsize=16)
plt.setp(ax.get_yticklabels(), fontsize=16)

fig.tight_layout()
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0.1)

plt.show()
