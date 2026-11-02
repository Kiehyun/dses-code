# 지구과학 데이터 사이언스 2 | IV-05. 지구의 열수지와 온실효과
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅳ-79.
# 필요한 라이브러리 불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow, Rectangle

%matplotlib inline

# %% code Ⅳ-80.
# 상수
S = 1361.0              # 태양 상수 [W/m^2]
albedo = 0.30           # 지구 전체의 알베도 (무차원)
sigma = 5.670374419e-8  # 슈테판-볼츠만 상수 [W/(m^2·K^4)]

def radiative_equilibrium_T(S=S, albedo=albedo):
    """복사 평형 온도 구하기(단위: K)"""
    absorbed = S * (1 - albedo) / 4          # 단위 면적당 흡수량 [W/m^2]
    return (absorbed / sigma) ** 0.25

T_e = radiative_equilibrium_T()

print(f"단위 면적당 흡수량 : {S * (1 - albedo) / 4:8.2f} W/m^2")
print(f"복사 평형 온도     : {T_e:8.2f} K  =  {T_e - 273.15:6.2f} °C")

# %% code Ⅳ-81.
albedos = np.linspace(0.0, 0.8, 200)
temps = radiative_equilibrium_T(albedo=albedos) - 273.15   # °C

fig, ax = plt.subplots(figsize=(8.3, 4.4))
ax.plot(albedos, temps, color="#2b6cb0", linewidth=2.4)

# 현재 지구
ax.scatter([0.30], [T_e - 273.15], s=90, color="#e2553d", zorder=5)
ax.annotate(f"현재 지구\n(알베도 0.30, {T_e - 273.15:.1f} °C)",
            xy=(0.30, T_e - 273.15), xytext=(0.45, -12),
            arrowprops=dict(arrowstyle="->", color="#e2553d"), fontsize=10)

ax.axhline(0, color="gray", linestyle=":", linewidth=1)
ax.set_xlabel("알베도 (반사되는 비율)")
ax.set_ylabel("복사 평형 온도 (°C)")
ax.set_title("알베도에 따른 지구의 복사 평형 온도", fontsize=12,
             fontweight="bold")
ax.grid(alpha=0.3)
plt.show()

# %% code Ⅳ-82.
T_a = T_e                    # 대기의 온도 = 복사 평형 온도
T_s = 2 ** 0.25 * T_e        # 지표의 온도

print(f"복사 평형 온도(대기 없음) : {T_e:7.2f} K = {T_e - 273.15:6.2f} °C")
print(f"1층 대기 모형의 지표 온도 : {T_s:7.2f} K = {T_s - 273.15:6.2f} °C")
print(f"                    차이 : {T_s - T_e:7.2f} K")
print()
print(f"실제 지구의 평균 기온     :  288.15 K =  15.00 °C")
print(f"실제 온실효과의 크기      : {288.15 - T_e:7.2f} K")

# %% code Ⅳ-83.
N = np.arange(0, 6)                       # 대기 층 수 (0 = 대기 없음)
T_layers = (N + 1) ** 0.25 * T_e - 273.15  # °C

fig, ax = plt.subplots(figsize=(8.3, 4.4))
bars = ax.bar(N, T_layers, color="#4a90d9", width=0.6)
bars[0].set_color("#9aa7b5")              # 대기 없음
bars[1].set_color("#e2553d")              # 1층 모형

for x, y in zip(N, T_layers):
    ax.text(x, y + 1.2, f"{y:.1f}", ha="center", fontsize=10,
            fontweight="bold")

ax.axhline(15, color="green", linestyle="--", linewidth=1.6,
           label="실제 지구 평균 기온 15 °C")
ax.set_xlabel("대기 층 수 $N$")
ax.set_ylabel("지표 온도 (°C)")
ax.set_title("대기 층 수에 따른 지표 온도 (단순 모형)", fontsize=12,
             fontweight="bold")
ax.legend()
ax.grid(axis="y", alpha=0.3)
plt.show()

# %% code Ⅳ-84.
# 들어오는 태양 복사를 100으로 놓았을 때의 값
# (Trenberth 등(2009)의 W/m^2 값을 341.3 = 100으로 환산, 잠열만 23.4 → 24로 조정)
budget = {
    "입사": 100,
    "대기 반사·산란": 23, "지표면 반사": 7,    # 합 30 = 반사
    "대기 흡수(태양)": 23, "지표면 흡수": 47,  # 합 70 = 흡수
    "지표면 방출": 116,
    "대기의 창(우주로)": 12, "대기 흡수(지구복사)": 104,
    "물의 증발(잠열)": 24, "대류·전도(현열)": 5,
    "대기의 복사(우주로)": 58, "대기의 재복사": 98,
}

SUN, EARTH = "#f5c33b", "#e2553d"
TOP, ATM_TOP, GND = 62, 42, 13          # 그림 위 / 대기 상단 / 지표면 높이

fig, ax = plt.subplots(figsize=(9.6, 5.6))
ax.set_xlim(0, 100); ax.set_ylim(0, TOP); ax.axis("off")

ax.add_patch(Rectangle((0, ATM_TOP), 100, TOP - ATM_TOP, fc="#1b2440"))   # 우주
ax.add_patch(Rectangle((0, GND), 100, ATM_TOP - GND, fc="#d3e7f7"))       # 대기
ax.add_patch(Rectangle((0, 0), 100, GND, fc="#82c98a"))                   # 지표
for y, t, c in [(TOP - 4, "우주", "#1b2440"), (ATM_TOP - 4, "대기", "#12406b"),
                (GND - 4.5, "지표", "#12406b")]:
    ax.text(97, y, t, fontsize=12, ha="right", va="center", color=c,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=.9, ec="none"))

def arw(x, y, dx, dy, w, c, val=None, vx=0, vy=0, fs=12):
    """화살표 하나와 그 옆의 숫자 그리기"""
    ax.add_patch(FancyArrow(x, y, dx, dy, width=w, head_width=w * 2.1, head_length=2.4,
                            length_includes_head=True, fc=c, ec="none", zorder=4))
    if val is not None:
        ax.text(x + dx / 2 + vx, y + dy / 2 + vy, str(val), fontsize=fs, zorder=6,
                ha="center", va="center", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=.92, ec="none"))

def lab(x, y, t, fs=10, c="#111"):
    ax.text(x, y, t, fontsize=fs, ha="center", va="center", color=c, zorder=6)

# 태양 복사 (노랑)
ax.scatter([6], [TOP - 7], s=2300, c="#ffd94a", zorder=3,
           edgecolors="#eeb200", linewidths=2)
arw(10, TOP - 10, 9, -(TOP - 10 - GND - 1), 2.8, SUN, budget["입사"], vx=-3.6,
    fs=13)
arw(23, ATM_TOP - 2, 7, 13, 1.9, SUN, 30, vx=2.8, fs=12)
lab(34, TOP - 4, "반사 및 산란", 11, "white")
arw(15, GND + 1, 0, 9, 1.4, SUN, budget["대기 흡수(태양)"], vx=-2.6, fs=10)
lab(15, GND + 12, "대기의 흡수", 9.5)
arw(22, GND + 1, 6, 9, 1.0, SUN, budget["지표면 반사"], vx=1.4, vy=-1, fs=10)
lab(28, GND + 12, "지표면 반사", 9.5)
lab(15, GND - 5, f"지표면 흡수  {budget['지표면 흡수']}", 11)

# 지구 복사 (빨강)
arw(52, GND, 0, 16, 2.3, EARTH, budget["지표면 방출"], vx=-4.4, fs=12)
lab(52, GND - 5, "지표면 방출", 10)
arw(46, ATM_TOP - 6, 0, 12, 1.1, EARTH, budget["대기의 창(우주로)"], vx=-3.2,
    fs=10)
lab(41, ATM_TOP + 9, "우주로\n손실", 9.5, "white")
lab(57, GND + 20, f"대기의 흡수  {budget['대기 흡수(지구복사)']}", 10)
arw(62, GND + 22, 0, 14, 1.9, EARTH, budget["대기의 복사(우주로)"], vx=3.2,
    fs=11)
lab(70, ATM_TOP + 3, "대기의 복사", 10.5, "white")
arw(56, ATM_TOP + 6, 0, 10, 2.6, EARTH, 70, vx=4.2, fs=13)
lab(64, TOP - 4, "지구 복사", 11, "white")
arw(70, GND, 0, 11, 1.1, EARTH, budget["물의 증발(잠열)"], vx=-2.6, fs=10)
lab(67, GND - 5, "물의 증발", 9.5)
arw(77, GND, 0, 8, 0.7, EARTH, budget["대류·전도(현열)"], vx=-2.2, fs=10)
lab(80, GND - 5, "대류와 전도", 9.5)
arw(88, GND + 20, 0, -19, 2.2, EARTH, budget["대기의 재복사"], vx=3.6, fs=11)
lab(84, GND + 23, "대기의 재복사", 10)

# 범례
ax.add_patch(FancyArrow(3, 3.6, 4, 0, width=.8, head_width=1.7, head_length=1.1,
                        fc=SUN, ec="none", zorder=6))
ax.text(8.5, 3.6, "태양 복사 에너지", fontsize=10.5, va="center", zorder=6)
ax.add_patch(FancyArrow(28, 3.6, 4, 0, width=.8, head_width=1.7, head_length=1.1,
                        fc=EARTH, ec="none", zorder=6))
ax.text(33.5, 3.6, "지구 복사 에너지", fontsize=10.5, va="center", zorder=6)

ax.set_title("지구의 열수지 — 들어오는 태양 복사를 100으로 놓았을 때",
             fontsize=13, fontweight="bold", pad=12)
plt.show()

# %% code Ⅳ-85.
def check(name, incoming, outgoing):
    """들어온 양과 나간 양 견주기"""
    ok = "균형" if abs(incoming - outgoing) < 1e-9 else "★ 어긋남"
    print(f"{name:12} 들어옴 {incoming:6.1f}   나감 {outgoing:6.1f}   → {ok}")

b = budget

# ① 지구 전체 (대기 위쪽 경계)
check("지구 전체",
      b["입사"],
      (b["대기 반사·산란"] + b["지표면 반사"])          # 반사 30
      + b["대기의 창(우주로)"] + b["대기의 복사(우주로)"])  # 방출 70

# ② 지표면
check("지표면",
      b["지표면 흡수"] + b["대기의 재복사"],
      b["지표면 방출"] + b["물의 증발(잠열)"] + b["대류·전도(현열)"])

# ③ 대기
check("대기",
      b["대기 흡수(태양)"] + b["대기 흡수(지구복사)"]
      + b["물의 증발(잠열)"] + b["대류·전도(현열)"],
      b["대기의 복사(우주로)"] + b["대기의 재복사"])

print()
print(f"지표면 방출 {b['지표면 방출']} = 대기 흡수 {b['대기 흡수(지구복사)']}"
      f" + 대기의 창 {b['대기의 창(우주로)']}")

# W/m^2 단위로 바꿔 보기 (100 = 지구 평균 입사량)
unit = S / 4        # 지구 표면 평균 입사량 [W/m^2]
print(f"\n1 (= 1%)은 약 {unit / 100:.2f} W/m^2입니다.")
print(f"지표면이 받는 대기의 재복사 {b['대기의 재복사']}"
      f" → {b['대기의 재복사'] * unit / 100:.0f} W/m^2")

# %% code Ⅳ-86.
import urllib.request, io

headers = {"User-Agent": "Mozilla/5.0 (DSES textbook notebook)"}

def fetch(url):
    """공개 데이터를 내려받아 문자열로 돌려주기"""
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read().decode("utf-8", errors="replace")

# ── 이산화 탄소 연평균 (NOAA, 마우나로아) ──
co2_txt = fetch("https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.txt")
rows = [ln.split() for ln in co2_txt.splitlines() if not ln.startswith("#") and ln.strip()]
co2 = pd.DataFrame(rows, columns=["year", "mean", "unc"]).astype(float)

# ── 전 지구 평균 기온 편차 (NASA GISTEMP) ──
gis_txt = fetch("https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv")
gis = pd.read_csv(io.StringIO(gis_txt), skiprows=1, na_values="***")
temp = gis[["Year", "J-D"]].dropna().astype(float)      # J-D = 1~12월 평균

print(f"CO2  : {co2['year'].min():.0f} ~ {co2['year'].max():.0f}년, "
      f"{co2['mean'].iloc[0]:.1f} → {co2['mean'].iloc[-1]:.1f} ppm")
print(f"기온 : {temp['Year'].min():.0f} ~ {temp['Year'].max():.0f}년, "
      f"최근 편차 {temp['J-D'].iloc[-1]:+.2f} °C")

# %% code Ⅳ-87.
fig, ax1 = plt.subplots(figsize=(7.5, 4.1))

# 왼쪽 축 — 이산화 탄소 농도
line_co2, = ax1.plot(co2["year"], co2["mean"], color="#e2553d", linewidth=2.4,
                     label="이산화 탄소 농도")
ax1.set_xlabel("연도")
ax1.set_ylabel("이산화 탄소 농도 (ppm)", color="#e2553d")
ax1.tick_params(axis="y", labelcolor="#e2553d")

# 오른쪽 축 — 전 지구 평균 기온 편차
ax2 = ax1.twinx()
sel = temp[temp["Year"] >= co2["year"].min()]
line_temp, = ax2.plot(sel["Year"], sel["J-D"], color="#2b6cb0", linewidth=2.0,
                      label="전 지구 평균 기온 편차")
ax2.set_ylabel("기온 편차 (°C, 1951~1980년 평균 기준)", color="#2b6cb0")
ax2.tick_params(axis="y", labelcolor="#2b6cb0")
ax2.axhline(0, color="gray", linestyle=":", linewidth=1)   # 기준선(범례에는 넣지 않음)

# 두 축의 선을 함께 모아 하나의 범례로
lines = [line_co2, line_temp]
ax1.legend(lines, [l.get_label() for l in lines], loc="upper left")
ax1.set_title("이산화 탄소 농도와 전 지구 평균 기온의 변화",
              fontsize=12, fontweight="bold")
ax1.grid(alpha=0.3)
plt.show()

# 두 데이터가 함께 있는 기간의 상관계수
merged = pd.merge(co2[["year", "mean"]], temp, left_on="year", right_on="Year")
print(f"함께 있는 기간 {merged['year'].min():.0f}~{merged['year'].max():.0f}년 "
      f"({len(merged)}개), 상관계수 r = {merged['mean'].corr(merged['J-D']):.3f}")
