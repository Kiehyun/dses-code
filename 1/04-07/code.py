# 지구과학 데이터 사이언스 1 | IV-07. 엘니뇨와 남방진동
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅳ-109.
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(10, 10))

# 1) 위: 세계 지도
ax1 = fig.add_subplot(2, 1, 1, projection=ccrs.PlateCarree(central_longitude=180))
ax1.set_global()
ax1.stock_img()
ax1.set_title("세계 지도", fontsize=14)

# 2) 아래: 적도 태평양(ENSO 해역)
ax2 = fig.add_subplot(2, 1, 2, projection=ccrs.PlateCarree(central_longitude=180))
ax2.set_extent([120, 300, -30, 30], crs=ccrs.PlateCarree())
ax2.stock_img()

gl = ax2.gridlines(
    crs=ccrs.PlateCarree(), draw_labels=True, linewidth=0.5, color='gray',
    alpha=0.5, linestyle='--'
)
gl.top_labels = False
gl.xlocator = mticker.FixedLocator(np.arange(-180, 180, 30))
gl.ylocator = mticker.FixedLocator(np.arange(-90, 90, 15))
gl.xformatter = LongitudeFormatter()
gl.yformatter = LatitudeFormatter()
gl.xlabel_style = {'size': 8, 'color': 'k'}
gl.ylabel_style = {'size': 8, 'color': 'k'}

# 다윈 · 타히티: SOI를 계산하는 두 지점
latDarwin, lonDarwin = -12, 130
latTahiti, lonTahiti = -17, -149

ax2.scatter(lonDarwin, latDarwin, color='red', marker='o', transform=ccrs.PlateCarree())
ax2.text(lonDarwin, latDarwin-5, "Darwin", color='red', fontsize=8, transform=ccrs.PlateCarree())

ax2.scatter(lonTahiti, latTahiti, color='red', marker='o', transform=ccrs.PlateCarree())
ax2.text(lonTahiti, latTahiti-5, "Tahiti", color='red', fontsize=8, transform=ccrs.PlateCarree())

# 3) 니뇨 영역 경계(꼭짓점 위도 · 경도, 서경은 음수)
#    경위선을 따르는 사각형이므로 PlateCarree로 잇는다(Geodetic은 대원으로 이어 변이 휜다)
latsNino1 = [0, -10, -10, 0, 0]
lonsNino1 = [-90, -90, -80, -80, -90]
latsNino3 = [5, -5, -5, 5, 5]
lonsNino3 = [-150, -150, -90, -90, -150]
latsNino34 = [5, -5, -5, 5, 5]
lonsNino34 = [-170, -170, -120, -120, -170]
latsNino4 = [5, -5, -5, 5, 5]
lonsNino4 = [-200, -200, -150, -150, -200]  # -200° = 160°E

ax2.plot(lonsNino1, latsNino1, color='black', linewidth=0.75, transform=ccrs.PlateCarree())
ax2.text(lonsNino1[0], latsNino1[1]-4, "NINO 1+2", color='black', fontsize=8, transform=ccrs.PlateCarree())

ax2.plot(lonsNino3, latsNino3, color='orange', linewidth=0.75, transform=ccrs.PlateCarree())
ax2.text((lonsNino3[0]+lonsNino3[2])/2, latsNino3[1]-4, "NINO 3", color='orange', fontsize=8, transform=ccrs.PlateCarree())

ax2.plot(lonsNino34, latsNino34, color='purple', linewidth=0.75, transform=ccrs.PlateCarree())
ax2.text((lonsNino34[0]+lonsNino34[2])/2, latsNino34[0]+3, "NINO 3.4", color='purple', fontsize=8, transform=ccrs.PlateCarree())

ax2.plot(lonsNino4, latsNino4, color='blue', linewidth=0.75, transform=ccrs.PlateCarree())
ax2.text((lonsNino4[0]+lonsNino4[2])/2, latsNino4[1]-3.5, "NINO 4", color='blue', fontsize=8, transform=ccrs.PlateCarree())

ax2.set_title("ENSO 관련 해역(니뇨 영역)", fontsize=14)
plt.tight_layout()

plt.savefig(f"{proj_dir}/ENSO_map.png", dpi=300, bbox_inches='tight')
plt.show()

# %% code Ⅳ-110.
import re
import requests
from pathlib import Path

# ONI: NOAA CPC 공식 파일
url1 = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"
oni_path = Path(proj_dir) / "oni.ascii.txt"

# SOI: 갱신 때마다 폴더(연-월)가 바뀌므로 안내 페이지에서 현재 주소 찾기
base = "https://climatedataguide.ucar.edu"
page = base + "/climate-data/southern-oscillation-indices-signal-noise-and-tahitidarwin-slp-soi"
try:
    html = requests.get(page, headers={"User-Agent": "Mozilla/5.0"}, timeout=60).text
    url2 = base + re.search(r"/sites/default/files/[\w-]+/SOI\.signal\.txt", html).group(0)
except Exception:
    # 2026년 11월 확인한 주소
    url2 = base + "/sites/default/files/2026-04/SOI.signal.txt"
soi_path = Path(proj_dir) / "SOI.signal.txt"
print("SOI 주소:", url2)

# 주기적으로 갱신되는 데이터라 늘 새로 받기(overwrite)
du.download(url1, oni_path, overwrite=True)
du.download(url2, soi_path, overwrite=True)

# %% code Ⅳ-111.
fpaths = du.list_files(proj_dir, "txt")

# %% code Ⅳ-112.
du.preview_text(oni_path, n=10);  # ONI 파일 앞 10줄

# %% code Ⅳ-113.
du.preview_text(soi_path, n=10);  # SOI 파일 앞 10줄

# %% code Ⅳ-114.
import pandas as pd
import numpy as np

# 공백으로 나뉜 표: SEAS(3개월 묶음), YR(연도), TOTAL(수온), ANOM(편차 = ONI)
df_ONI = pd.read_csv(oni_path, sep=r"\s+")

# 3개월 묶음 이름 → 가운데 달
SEAS_MID = {"DJF": 1, "JFM": 2, "FMA": 3, "MAM": 4, "AMJ": 5, "MJJ": 6,
            "JJA": 7, "JAS": 8, "ASO": 9, "SON": 10, "OND": 11, "NDJ": 12}

df_ONI['dt_date'] = pd.to_datetime(dict(year=df_ONI['YR'],
                                        month=df_ONI['SEAS'].map(SEAS_MID),
                                        day=1))
df_ONI['ONI'] = df_ONI['ANOM']
df_ONI.index = df_ONI['dt_date']

print("df_ONI : \n", df_ONI)

# %% code Ⅳ-115.
import numpy as np

arr = np.loadtxt(soi_path)
print("arr.shape :", arr.shape)
print("arr : \n", arr)

arr1 = arr[:,1:]  # 첫 열(연도)을 빼고 12개월 값만
print("arr1.shape :", arr1.shape)
print("arr1 : \n", arr1)

arr2 = arr1.reshape(-1)  # 1차원으로 펼침
print("arr2.shape :", arr2.shape)
print("arr2 : \n", arr2)

from datetime import datetime
from dateutil.relativedelta import relativedelta

# 파일의 첫해 1월부터 한 달씩 날짜 목록
StartDtStr = f"{int(arr[0, 0])}-01-01"
EndDTStr = f"{int(arr[-1, 0]) + 1}-01-01"

StartDT = datetime.strptime(StartDtStr, "%Y-%m-%d")
EndDT = datetime.strptime(EndDTStr, "%Y-%m-%d")

date1 = StartDT
proc_dates = []
while date1 < EndDT:
    proc_dates.append(date1)
    date1 +=  relativedelta(months=1)

print("len(proc_dates): {}".format(len(proc_dates)))
print(f"proc_dates: {proc_dates}")

# %% code Ⅳ-116.
import pandas as pd

# (날짜, SOI) 쌍으로 DataFrame 만들기
df_SOI = pd.DataFrame(list(zip(proc_dates, arr2)), columns = ["date", "SOI"])
df_SOI['dt_date'] = pd.to_datetime(df_SOI['date'])
df_SOI.index = df_SOI['dt_date']
df_SOI['SOI'] = df_SOI['SOI'].replace(-99.9, np.nan)  # -99.9는 결측값
print("df_SOI :", df_SOI)

# %% code Ⅳ-117.
import matplotlib.pyplot as plt
from matplotlib import rc

fig, ax = plt.subplots(figsize=(12.0, 4.0))
ax.plot(df_ONI['dt_date'], df_ONI['ONI'].astype(float), label='ONI')
ax.set_title('니뇨 3.4 지역의 해양 엘니뇨 지수(ONI)', fontsize=18, fontweight='bold')
ax.set_xlabel('시간(년)', fontsize=14)
ax.set_ylabel('수온 편차 (°C)', fontsize=14)
plt.show()

# %% code Ⅳ-118.
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12.0, 4.0))

ax.plot(df_ONI['dt_date'], df_ONI['ONI'].astype(float), "k-", linewidth=0.5)

ax.set_xlim([df_ONI['dt_date'].min(), df_ONI['dt_date'].max()])
ax.set_ylim([-3, 3])

ax.axhline(y = 0, color = 'black', linestyle = '-')

# ONI가 +1 °C보다 크면 빨강, -1 °C보다 작으면 파랑으로 채우기
ax.fill_between(df_ONI['dt_date'], df_ONI['ONI'].astype(float), 1,
                where=df_ONI['ONI'].astype(float) > 1,
                color='red', alpha=0.7)

ax.fill_between(df_ONI['dt_date'], df_ONI['ONI'].astype(float), -1,
                where= df_ONI['ONI'].astype(float) < -1,
                color='blue', alpha=0.7)
ax.grid()
ax.set_xlabel(r'시간(년)', fontsize = 14)
ax.set_ylabel(r'수온 편차 ($\rm{^{\circ}C}$)', fontsize = 14)

ax.set_title('니뇨 3.4 지역의 해양 엘니뇨 지수(ONI)',
          y=1.05,  # 제목 아래 여백
          fontdict={'fontsize':18,'fontweight':'bold'})

fig.tight_layout()
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0.1)

plt.show()

# %% code Ⅳ-119.
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12.0, 4.0))

ax.plot(df_SOI['dt_date'], df_SOI['SOI'].astype(float), "k-", linewidth=0.5)

ax.set_xlabel(r'시간(년)', fontsize = 16)
ax.set_ylabel('SOI (표준화, 단위 없음)', fontsize = 16)

ax.set_xlim([df_SOI['dt_date'].min(), df_SOI['dt_date'].max()])
ax.set_ylim([-6, 6])

ax.axhline(y = 0, color = 'black', linestyle = '-')

# SOI 양수(라니냐 쪽)는 파랑, 음수(엘니뇨 쪽)는 빨강
ax.fill_between(df_SOI['dt_date'], df_SOI['SOI'].astype(float), 0,
                where= df_SOI['SOI'].astype(float) > 0,
                color='blue', alpha=0.7)

ax.fill_between(df_SOI['dt_date'], df_SOI['SOI'].astype(float), 0,
                where= df_SOI['SOI'].astype(float) < 0,
                color='red', alpha=0.7)
ax.grid()
ax.set_title('남방진동지수(SOI)',
          y=1.05,  # 제목 아래 여백
          fontdict={'fontsize':18,'fontweight':'bold'})

plt.setp(ax.get_xticklabels(), fontsize=16)
plt.setp(ax.get_yticklabels(), fontsize=16)

fig.tight_layout()
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0.1)

plt.show()

# %% code Ⅳ-120.
# 달마다 상태 표시: 1(엘니뇨 쪽), -1(라니냐 쪽), 0(중립)
oni = df_ONI['ONI'].astype(float)
state = pd.Series(np.select([oni >= 0.5, oni <= -0.5], [1, -1], 0), index=oni.index)

# 같은 상태가 이어지는 구간마다 번호 붙이기
run_id = (state != state.shift()).cumsum()

rows = []
for _, seg in state.groupby(run_id):
    if seg.iloc[0] == 0 or len(seg) < 5:  # 중립이거나 5개월 미만이면 제외
        continue
    vals = oni.loc[seg.index]
    rows.append({"구분": "엘니뇨" if seg.iloc[0] == 1 else "라니냐",
                 "시작": seg.index[0].to_period("M"),
                 "끝": seg.index[-1].to_period("M"),
                 "개월 수": len(seg),
                 "최댓값": vals.max() if seg.iloc[0] == 1 else vals.min()})
events = pd.DataFrame(rows)

# 최댓값(절댓값)에 따른 강도 구분
events["강도"] = pd.cut(events["최댓값"].abs(), bins=[0.5, 1.0, 1.5, 2.0, np.inf],
                      right=False, labels=["약함", "보통", "강함", "매우 강함"])

print(f"ONI 기간: {oni.index.min():%Y-%m} ~ {oni.index.max():%Y-%m}")
print(events.groupby(["구분", "강도"], observed=False).size().unstack())
print()
print("최근 사례 5개")
print(events.tail(5).to_string(index=False))

# %% code Ⅳ-121.
# 최댓값의 절댓값이 큰 순서로 상위 8개 사례
top = events.sort_values("최댓값", key=abs, ascending=False).head(8)
print(top.to_string(index=False))

# %% code Ⅳ-122.
fig, ax = plt.subplots(figsize=(12.0, 4.0))
ax.plot(df_ONI['dt_date'], oni, "k-", linewidth=0.7)

# 사례 기간마다 색 띠(끝 달은 그달 말일까지)
for _, ev in events.iterrows():
    ax.axvspan(ev["시작"].to_timestamp(), ev["끝"].to_timestamp(how="end"),
               color='red' if ev["구분"] == "엘니뇨" else 'blue', alpha=0.25, linewidth=0)

ax.axhline(y=0, color='black', linewidth=0.8)
for y in (0.5, -0.5):  # 판정 기준선
    ax.axhline(y=y, color='gray', linestyle='--', linewidth=0.8)

ax.set_xlim([df_ONI['dt_date'].min(), df_ONI['dt_date'].max()])
ax.set_ylim([-3, 3])
ax.set_xlabel('시간(년)', fontsize=14)
ax.set_ylabel(r'수온 편차 ($\rm{^{\circ}C}$)', fontsize=14)
ax.set_title('판정 기준(±0.5 °C, 5개월 이상)으로 골라낸 엘니뇨 · 라니냐 사례',
             fontsize=16, fontweight='bold')
fig.tight_layout()
plt.show()
