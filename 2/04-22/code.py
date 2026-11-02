# 지구과학 데이터 사이언스 2 | IV-02. 단열선도(Skew T-log P) 그리기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 401.
fname = "UPPER_SONDE_47122_ALL_2018_2018_2019.csv"
fid = "1HYYmP07A8pMeRNxJIBcPiMaAkCuxIWpF"

# du.download()로 파일 내려받기
du.download(f"https://docs.google.com/uc?export=download&id={fid}",
            proj_dir / fname)

# %% code 402.
fpaths = du.list_files(proj_dir, "csv")

# %% code 403.
du.preview_text(fpaths[0], n=10)

# %% code 404.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from metpy.plots import SkewT
from metpy.units import units
from metpy.calc import dewpoint, vapor_pressure

# 표준 등압면(hPa)과 포화 혼합비(g/kg)
STANDARD_ISOBARS = [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150,
                    100]
STANDARD_MIXING = [0.4, 1, 2, 3, 5, 8, 12, 16, 20]

# 선 종류 : (색, 선 모양, 굵기, 이름)
LINE_STYLE = {
    'isobar':   ('black',  '-',         0.6, '등압선'),
    'isotherm': ('brown',  '-',         0.6, '등온선'),
    'dry':      ('orange', '-',         0.7, '건조 단열선'),
    'moist':    ('green',  '-',         1.2, '습윤 단열선'),
    'mixing':   ('blue',   (0, (6, 4)), 0.7, '포화 혼합비선'),
}

def draw_skewt_paper(skew, xlim=(-40, 40), ylim=(1050, 100), *,
                     isotherm_step=10, isobars=STANDARD_ISOBARS,
                     dry_step=10, moist_step=5, mixing_ratios=STANDARD_MIXING,
                     draw=('isobar', 'isotherm', 'dry', 'moist', 'mixing'),
                     mixing_label_p=850, legend=True):
    """Skew T-log P 선도의 '용지'(기준선)를 그린다.

    skew           : SkewT 객체
    xlim           : 기온 축 범위 (°C)
    ylim           : 기압 축 범위 (hPa) — (아래, 위) 순서
    isotherm_step  : 등온선 간격 (°C)
    dry_step       : 건조 단열선 간격 (°C)
    moist_step     : 습윤 단열선 간격 (°C)
    mixing_ratios  : 포화 혼합비선 값 (g/kg)
    draw           : 그릴 선의 종류를 고른다
    mixing_label_p : 혼합비 값을 적을 기압 (hPa)
    """
    p_bottom, p_top = max(ylim), min(ylim)

    # 등압선 — 가로 직선
    if 'isobar' in draw:
        color, ls, lw, _ = LINE_STYLE['isobar']
        for p in isobars:
            if p_top <= p <= p_bottom:
                skew.ax.axhline(p, color=color, linestyle=ls, linewidth=lw,
                                alpha=0.6)

    # 등온선 — 오른쪽 위로 기울어진 직선
    if 'isotherm' in draw:
        color, ls, lw, _ = LINE_STYLE['isotherm']
        for t in np.arange(-160, 61, isotherm_step):      # 화면 밖에서 들어오는 선까지
            skew.ax.axvline(t, color=color, linestyle=ls,
                            linewidth=lw * (1.8 if t == 0 else 1.0), alpha=0.6)

    # 건조 단열선
    if 'dry' in draw:
        color, ls, lw, _ = LINE_STYLE['dry']
        skew.plot_dry_adiabats(t0=np.arange(-50, 260, dry_step) * units.degC,
                               colors=color, linestyles=ls, linewidths=lw, alpha=1.0)

    # 습윤 단열선
    if 'moist' in draw:
        color, ls, lw, _ = LINE_STYLE['moist']
        skew.plot_moist_adiabats(t0=np.arange(-40, 45, moist_step) * units.degC,
                                 colors=color, linestyles=ls, linewidths=lw, alpha=1.0)

    # 포화 혼합비선 + 값 표시
    if 'mixing' in draw:
        color, ls, lw, _ = LINE_STYLE['mixing']
        w = np.array(mixing_ratios) / 1000.                     # g/kg → kg/kg
        p_line = np.linspace(p_bottom, max(p_top, 400), 40) * units.hPa
        skew.plot_mixing_lines(mixing_ratio=w, pressure=p_line,
                               colors=color, linestyles=ls, linewidths=lw, alpha=1.0)
        if p_top <= mixing_label_p <= p_bottom:
            t_lab = dewpoint(vapor_pressure(mixing_label_p * units.hPa, w)).to(units.degC)
            for value, t in zip(mixing_ratios, t_lab.magnitude):
                if xlim[0] < t < xlim[1]:
                    skew.ax.text(t, mixing_label_p, f'{value:g}', color=color,
                                 fontsize=7, ha='center', va='center',
                                 clip_on=True,
                                 bbox=dict(boxstyle='round,pad=0.1', fc='white',
                                           ec='none', alpha=0.8))

    skew.ax.set_xlim(*xlim)
    skew.ax.set_ylim(p_bottom, p_top)
    skew.ax.set_xlabel(r'기온 (${\degree \mathrm{C}}$)', fontsize=9)
    skew.ax.set_ylabel(r'기압 (${\mathrm{hPa}}$)', fontsize=9)
    skew.ax.tick_params(labelsize=8)

    # 같은 선이 수십 개이므로 종류마다 하나씩만 범례에 넣는다
    if legend:
        handles = [Line2D([], [], color=LINE_STYLE[k][0], linestyle=LINE_STYLE[k][1],
                          linewidth=max(LINE_STYLE[k][2], 1.2), label=LINE_STYLE[k][3])
                   for k in draw]
        skew.ax.legend(handles=handles, loc='upper right', fontsize=7.5)
    return skew

# %% code 405.
# 단열선도 전체 그리기 (지상 1050 hPa ~ 100 hPa)
xxlim = [-40, 40]        # 기온 축 범위 (°C)
yylim = [1050, 100]      # 기압 축 범위 (hPa)

fig = plt.figure(figsize=(5.4, 4.6))
skew = SkewT(fig, rotation=45)          # rotation : 등온선을 기울이는 각도

draw_skewt_paper(skew, xlim=xxlim, ylim=yylim)

plt.tight_layout()
plt.savefig(f'{str(proj_dir)}/SkewTlogP_paper_{xxlim[0]}_{xxlim[1]}_{yylim[0]}_{yylim[1]}_kr.png',
            dpi=150)
plt.savefig(f'{str(proj_dir)}/SkewTlogP_paper_{xxlim[0]}_{xxlim[1]}_{yylim[0]}_{yylim[1]}_kr.pdf')
plt.show()
plt.close()

# %% code 406.
# 아래쪽 일부만 확대해 보기 — 범위와 간격만 바꾸어 같은 함수 호출
xxlim = [-30, 10]        # 기온 축 범위 (°C)
yylim = [1050, 700]      # 기압 축 범위 (hPa)

fig = plt.figure(figsize=(6.0, 3.2))
skew = SkewT(fig, rotation=45)

draw_skewt_paper(skew, xlim=xxlim, ylim=yylim,
                 isotherm_step=5,     # 확대했으므로 등온선을 5 °C 간격으로 촘촘히
                 dry_step=5,
                 mixing_label_p=900)

plt.tight_layout()
plt.savefig(f'{str(proj_dir)}/SkewTlogP_crop_{xxlim[0]}_{xxlim[1]}_{yylim[0]}_{yylim[1]}_kr.png',
            dpi=150)
plt.show()
plt.close()

# %% code 407.
import urllib.request
from IPython.display import Image, display

try:
    import pymupdf                      # PyMuPDF 1.24 이상
except ImportError:
    import fitz as pymupdf              # 예전 이름

url = "https://www.noaa.gov/sites/default/files/2022-06/skew_t_fullsize.pdf"
pdf_path = f"{str(proj_dir)}/noaa_skew_t_fullsize.pdf"
png_path = f"{str(proj_dir)}/noaa_skew_t_fullsize.png"

# 1) PDF 내려받기 (이미 받아 두었으면 건너뜀)
if not os.path.exists(pdf_path):
    print("내려받는 중입니다 …")
    # 브라우저와 같은 머리말
    ua = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    req = urllib.request.Request(url, headers={"User-Agent": ua,
                                               "Accept": "application/pdf,*/*"})
    with urllib.request.urlopen(req, timeout=60) as res, open(pdf_path, "wb") as f:
        f.write(res.read())
print(f"파일 크기: {os.path.getsize(pdf_path) / 1e3:.0f} KB")

# 2) 첫 쪽을 그림으로 바꾸기
doc = pymupdf.open(pdf_path)
page = doc[0]
print(f"쪽 수: {doc.page_count},  용지 크기: {page.rect.width:.0f} x {page.rect.height:.0f} pt")

pix = page.get_pixmap(dpi=110)          # dpi 를 올리면 더 또렷해집니다
pix.save(png_path)
doc.close()

# 3) 노트북에 표시
display(Image(filename=png_path, width=1000))

# %% code 408.
import matplotlib.pyplot as plt
from metpy.plots import SkewT

# 새 그림 만들기
fig = plt.figure(figsize=(5.4, 4.6)) 

# 단열선도 그리기
skew = SkewT(fig)

# 차트와 축 제목 넣기
skew.ax.set_title('Skew T-log P 단열선도\n', fontsize=10) 
skew.ax.set_xlabel(r'기온 (${\degree \mathrm{C}}$)', fontsize=9)
skew.ax.set_ylabel(r'기압 (${\mathrm{hPa}}$)', fontsize=9)
skew.ax.tick_params(labelsize=8)

plt.show()

# %% code 409.
import matplotlib.pyplot as plt
from metpy.plots import SkewT

# 새 그림 만들기
fig = plt.figure(figsize=(5.4, 4.6)) 

# 온도축과 기압축 범위 지정
xxlim = [-50, 50]       #온도축
yylim = [1050.1, 99.9]  #기압축

# 온도축 기울기 지정
skew = SkewT(fig, rotation=45)

skew.ax.set_title('Skew T-log P 단열선도\n', fontsize=10) 
skew.ax.set_xlabel(r'기온 (${\degree \mathrm{C}}$)', fontsize=9)
skew.ax.set_ylabel(r'기압 (${\mathrm{hPa}}$)', fontsize=9)

# 등온선(isotherm) 그리는 함수 정의
def add_isothermal(skew) :
 # 등온선의 녹색 영역 표시
    for t in range(-160, 61, 40) :
        skew.ax.axvspan(t, t + 20, color='green', alpha=0.10, linewidth=0)

 # 갈색 등온선 그리기
    for t in range(-160, 61, 2) :
        if t % 10 :
            skew.ax.axvline(t, color='brown', linestyle='-', linewidth=0.25,
                            alpha=0.35)
    for t in range(-160, 61, 10) :
        skew.ax.axvline(t, color='brown', linestyle='-', linewidth=1.0,
                        alpha=0.85)
    skew.ax.axvline(0, color='brown', linestyle='-', linewidth=1.8,
                    label='등온선')

 # 가로(기온)축 표시하기
    skew.ax.set_xlim(xxlim[0], xxlim[1])
    skew.ax.tick_params(axis="x", labelsize=8, pad=6, rotation=45,
                        labelcolor='brown')
    skew.ax.tick_params(axis="y", labelsize=8, pad=0.5)

 #등온선 글자
    # 10 °C 간격으로 적기
    for i in range(0, 36, 2):
        if i < 16:
            plt.text(-i*5-10.5, 1050 / 10**(i/35), '{0}'.format(-i*5-10), 
                horizontalalignment='left', verticalalignment='center', 
                fontsize=7, rotation=45, color='brown', alpha=0.7)
        if i < 30:
            plt.text(-i*5+29.5, 1050 / 10**(i/35), '{0}'.format(-i*5+30), 
                horizontalalignment='left', verticalalignment='center', 
                fontsize=7, rotation=45, color='brown', alpha=0.7)
        if i > 7 : 
            plt.text(-i*5+69.5, 1050 / 10**(i/35), '{0}'.format(-i*5+70), 
                horizontalalignment='left', verticalalignment='center', 
                fontsize=7, rotation=45, color='brown', alpha=0.7)    

#등온선 그리는 함수
add_isothermal(skew)

plt.show()

# %% code 410.
import numpy as np
import matplotlib.pyplot as plt
from metpy.plots import SkewT

# 새 그림 만들기
fig = plt.figure(figsize=(5.4, 4.6)) 

# 온도축과 기압축 범위 지정
xxlim = [-50, 50]       #온도축
yylim = [1050.1, 99.9]  #기압축

# 온도축 기울기 지정
skew = SkewT(fig, rotation=45)

skew.ax.set_title('Skew T-log P 단열선도\n', fontsize=10) 
skew.ax.set_xlabel(r'기온 (${\degree \mathrm{C}}$)', fontsize=9)
skew.ax.set_ylabel(r'기압 (${\mathrm{hPa}}$)', fontsize=9)
skew.ax.tick_params(labelsize=8)

# 등압선 그리는 함수 정의
def add_isobar(skew):
    skew.ax.set_ylim(yylim[0], yylim[1])
    yts1 = list(np.arange(1050, 99, -10))  # 10 hPa 간격 (가는 선) 표시
    skew.ax.set_yticks(yts1)

 # 50 hPa 간격
    yts2 = list(np.arange(1050, 99, -50))  # 50 hPa 간격 (굵은 선) 표시
    yticklabels=[]
    i=0
    for ytick in yts2 : 
        # 눈금 글자는 100 hPa 간격만 — 로그 눈금이라 아래쪽에서 50 hPa 간격 글자가 겹침
        yticklabels.append(ytick if ytick % 100 == 0 else '')
        for j in range(4):
            yticklabels.append('')
        skew.plot([ytick, ytick], [-150,100], 'k', linewidth=0.6)
    
 #등압선 글자
        if ytick >= 200 : 
            plt.text(-20-(np.log(1050)-np.log(1050-i*50))*35, ytick, '{0}'.format(ytick), 
                horizontalalignment='left', verticalalignment='center', 
                fontsize=7, color='black', alpha=.30)
        if ytick >= 500 : 
            plt.text(20-(np.log(1050)-np.log(1050-i*50))*35, ytick, '{0}'.format(ytick), 
                horizontalalignment='left', verticalalignment='center', 
                fontsize=7, color='black', alpha=.30)

    skew.ax.set_yticklabels(yticklabels[:-4], minor=False)
    
    return skew

#등압선 그리는 함수
add_isobar(skew)
 
plt.show()

# %% code 411.
import numpy as np
import metpy.calc as mpcalc
import matplotlib.pyplot as plt
from metpy.plots import SkewT
from metpy.units import units

# 새 그림 만들기
fig = plt.figure(figsize=(5.4, 4.6))

# 온도축과 기압축 범위 지정
xxlim = [-50, 50]       #온도축
yylim = [1050.1, 99.9]  #기압축

# 온도축 기울기 지정
skew = SkewT(fig, rotation=45)

skew.ax.set_title('건조 단열선\n', fontsize=10)
skew.ax.set_xlabel(r'기온 (${\degree \mathrm{C}}$)', fontsize=9)
skew.ax.set_ylabel(r'기압 (${\mathrm{hPa}}$)', fontsize=9)
skew.ax.tick_params(labelsize=8)

# 건조 단열선 그리는 함수 정의
def add_dry_adiabats(skew, t0=np.arange(-30, 180, 10), label_p=530,
                     label_every=1):
    """건조 단열선을 그리고, 선마다 1000 hPa 기준 온도(=온위)를 적는다."""
    t0 = np.asarray(t0)
    skew.plot_dry_adiabats(t0=t0 * units.degC,
                           colors='orange', linestyles='-', linewidths=1.0,
                           alpha=1.0, label='건조 단열선')

    # 글자 위치 계산
    t_at_label = mpcalc.dry_lapse(label_p * units.hPa, t0 * units.degC,
                                  reference_pressure=1000 * units.hPa).to(units.degC).magnitude

    # label_every 개마다 글자 적기
    for t_start, t_lab in list(zip(t0, np.atleast_1d(t_at_label)))[::label_every]:
        skew.ax.text(t_lab, label_p, f'{t_start:g}',
                     ha='center', va='center', fontsize=7, color='orange', clip_on=True,
                     bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.85))
    return skew

# 건조 단열선 그리기
add_dry_adiabats(skew)

# 축 범위 지정
skew.ax.set_xlim(xxlim[0], xxlim[1])
skew.ax.set_ylim(yylim[0], yylim[1])

plt.show()

# %% code 412.
import numpy as np
import metpy.calc as mpcalc
import matplotlib.pyplot as plt
from metpy.plots import SkewT
from metpy.units import units

# 새 그림 만들기
fig = plt.figure(figsize=(5.4, 4.6))

# 온도축과 기압축 범위 지정
xxlim = [-50, 50]       #온도축
yylim = [1050.1, 99.9]  #기압축

# 온도축 기울기 지정
skew = SkewT(fig, rotation=45)

skew.ax.set_title('습윤 단열선\n', fontsize=10)
skew.ax.set_xlabel(r'기온 (${\degree \mathrm{C}}$)', fontsize=9)
skew.ax.set_ylabel(r'기압 (${\mathrm{hPa}}$)', fontsize=9)
skew.ax.tick_params(labelsize=8)

# 습윤 단열선 그리는 함수 정의
def add_moist_adiabats(skew, t0=np.arange(-30, 40, 2), label_p=530,
                       label_every=1):
    """습윤 단열선을 그리고, 선마다 1000 hPa 기준 온도를 적는다.

    t0 에 100 °C 가 넘는 값을 넣으면 포화수증기압이 대기압보다 커져
    계산이 되지 않는다(MetPy 가 'ODE Integration failed' 오류를 낸다).
    실제 대기에서 뜻이 있는 -30 ~ 40 °C 범위만 쓴다.
    """
    t0 = np.asarray(t0)
    skew.plot_moist_adiabats(t0=t0 * units.degC,
                             colors='green', linestyles='-', linewidths=1.0,
                             alpha=1.0, label='습윤 단열선')

    # 글자 위치 계산
    t_at_label = mpcalc.moist_lapse(np.array([1000., label_p]) * units.hPa,
                                    t0 * units.degC,
                                    reference_pressure=1000 * units.hPa)
    t_at_label = np.atleast_2d(t_at_label.to(units.degC).magnitude)[:, -1]

    # label_every 개마다 글자 적기
    for t_start, t_lab in list(zip(t0, t_at_label))[::label_every]:
        if np.isnan(t_lab):
            continue
        skew.ax.text(t_lab, label_p, f'{t_start:g}',
                     ha='center', va='center', fontsize=7, color='green', clip_on=True,
                     bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.85))
    return skew

# 습윤 단열선 그리기
add_moist_adiabats(skew)

# 축 범위 지정
skew.ax.set_xlim(xxlim[0], xxlim[1])
skew.ax.set_ylim(yylim[0], yylim[1])

plt.show()

# %% code 413.
import numpy as np
import metpy.calc as mpcalc
import matplotlib.pyplot as plt
from metpy.plots import SkewT
from metpy.units import units

# 새 그림 만들기
fig = plt.figure(figsize=(5.4, 4.6))

# 온도축과 기압축 범위 지정
xxlim = [-50, 50]       #온도축
yylim = [1050.1, 99.9]  #기압축

# 온도축 기울기 지정
skew = SkewT(fig, rotation=45)

skew.ax.set_title('포화 혼합비선\n', fontsize=10)
skew.ax.set_xlabel(r'기온 (${\degree \mathrm{C}}$)', fontsize=9)
skew.ax.set_ylabel(r'기압 (${\mathrm{hPa}}$)', fontsize=9)
skew.ax.tick_params(labelsize=8)

# 포화 혼합비선 그리는 함수 정의
def add_mixing_lines(skew, mixing_ratios=(0.1, 0.2, 0.4, 1, 2, 3, 5, 8, 12, 16, 20, 24),
                     p_range=(1050, 400), label_p=850, label_every=1):
    """포화 혼합비선을 그리고, 선마다 혼합비 값(g/kg)을 적는다."""
    w = np.array(mixing_ratios) / 1000.          # g/kg -> kg/kg
    pressure = np.linspace(p_range[0], p_range[1], 40) * units.hPa

    skew.plot_mixing_lines(mixing_ratio=w, pressure=pressure,
                           colors='blue', linestyles='--', linewidths=1.0,
                           alpha=1.0, label='포화 혼합비선')

    # 글자 위치 = 그 지점의 이슬점
    t_at_label = mpcalc.dewpoint(
        mpcalc.vapor_pressure(label_p * units.hPa, w)).to(units.degC).magnitude

    for value, t_lab in list(zip(mixing_ratios, np.atleast_1d(t_at_label)))[::label_every]:
        skew.ax.text(t_lab, label_p, f'{value:g}',
                     ha='center', va='center', fontsize=7, color='blue', clip_on=True,
                     bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.85))
    return skew

# 포화 혼합비선 그리기
add_mixing_lines(skew)

# 축 범위 지정
skew.ax.set_xlim(xxlim[0], xxlim[1])
skew.ax.set_ylim(yylim[0], yylim[1])

plt.show()

# %% code 414.
import numpy as np
import metpy.calc as mpcalc
import matplotlib.pyplot as plt
from metpy.plots import SkewT
from metpy.units import units

# 새 그림 만들기
fig = plt.figure(figsize=(5.4, 4.6)) 

# 온도축과 기압축 범위 지정
xxlim = [-50, 50]       #온도축
yylim = [1050.1, 99.9]  #기압축

# 온도축 기울기 지정
skew = SkewT(fig, rotation=45)

skew.ax.set_title('Skew T-log P 단열선도\n', fontsize=10) 
skew.ax.set_xlabel(r'기온 (${\degree \mathrm{C}}$)', fontsize=9)
skew.ax.set_ylabel(r'기압 (${\mathrm{hPa}}$)', fontsize=9)

#등온선 그리는 함수
add_isothermal(skew)

#기압축 그리는 함수
add_isobar(skew)

# 건조 단열선 — 라벨은 300 hPa 높이에
add_dry_adiabats(skew, label_p=300, label_every=2)

# 습윤 단열선 — 라벨은 600 hPa 높이에
add_moist_adiabats(skew, label_p=600, label_every=5)

# 포화 혼합비선 — 라벨은 850 hPa 높이에
add_mixing_lines(skew, label_p=850, label_every=2)

#legend 추가
plt.legend(loc='upper left', fontsize=7)

plt.show()

# %% code 415.
# 패키지 불러오기
import pandas as pd

# CSV 파일을 데이터프레임으로 읽기
df = pd.read_csv(str(fpaths[0]), thousands = ',', encoding= 'euc-kr')
print("행 · 열 :", df.shape)
df.head()

# %% code 416.
# 기온·이슬점이 모두 NaN인 행 제거
df = df.dropna(subset=('기온(°C)', '이슬점온도(°C)'), how='all').reset_index(drop=True)
print("행 · 열 :", df.shape)
df.head()

# %% code 417.
print("df['일시(UTC)'].iloc[0]:{}".format(df['일시(UTC)'].iloc[0]))
print("type(df['일시(UTC)'].iloc[0]):{}".format(type(df['일시(UTC)'].iloc[0])))

# %% code 418.
df['dt_YmdHM'] = pd.to_datetime(df['일시(UTC)'])
print("type(df['dt_YmdHM'].iloc[0]):{}".format(type(df['dt_YmdHM'].iloc[0])))

df.index = df['dt_YmdHM']
df.head(3)

# %% code 419.
from datetime import datetime

# 원하는 관측시간을 입력
target_date = datetime(2018, 1, 12, 12)
target_date_strf = target_date.strftime('%Y-%m-%d %H:%M')
target_date_strf

# %% code 420.
from datetime import datetime

# 원하는 관측시간을 입력
target_date = datetime(2018, 1, 12, 12)
target_date_strf = target_date.strftime('%Y-%m-%d %H:%M')

print("target_date_strf: {}".format(target_date_strf))
print("type(target_date_strf): {}".format(type(target_date_strf)))

df_selected_time = df[(df['dt_YmdHM'] == target_date_strf)]

df_selected_time = df_selected_time.sort_values('기압(hPa)', ascending=False)

print("층 수 :", len(df_selected_time))
df_selected_time.head()

# %% code 421.
f = lambda s: target_date_strf in s
ids  = df['일시(UTC)'].apply(f)

df_selected_time = df[ids]
df_selected_time = df_selected_time.sort_values('기압(hPa)', ascending=False)
print("층 수 :", len(df_selected_time))   # 앞 셀과 같은 46개 층

# %% code 422.
import numpy as np
import metpy.calc as mpcalc
from metpy.units import units as u

# MetPy로 단위가 붙은 물리량 만들기 — 46개 층을 다 찍으면 길어서 앞 5개 층만 출력
for col, unit in [('기압(hPa)', u.hPa), ('기온(°C)', u.degC), ('이슬점온도(°C)', u.degC),
                  ('풍속(knot)', u.knots), ('풍향(deg)', u.degrees)]:
    q = df_selected_time[col].values * unit
    print(f"{col:12s}: {q[:5]}")

# 뒤 셀에서 계산 결과를 볼 때는 대표 기압 층만 골라 본다
levels = [1025, 1000, 925, 867, 850, 800, 700, 500, 300, 200]   # hPa

def show_levels(cols):
    """정한 기압 층(levels)에서 cols 열만 보여 준다."""
    return df_selected_time.set_index('기압(hPa)').loc[levels, cols]

# %% code 423.
import numpy as np
import metpy.calc as mpcalc
from metpy.units import units as u

# 바람 벡터 계산
df_selected_time['u_wind'], df_selected_time['v_wind'] = mpcalc.wind_components(df_selected_time['풍속(knot)'].values * u.knots, 
                          np.deg2rad(df_selected_time['풍향(deg)'].values * u.deg))

show_levels(['u_wind', 'v_wind'])

# %% code 424.
import numpy as np
import metpy.calc as mpcalc
from metpy.units import units as u
                   
# 습구온도 계산
df_selected_time['wet_bulb_T'] = \
        mpcalc.wet_bulb_temperature(df_selected_time['기압(hPa)'].values * u.hPa, 
                df_selected_time['기온(°C)'].values * u.degC,
                df_selected_time['이슬점온도(°C)'].values * u.degC)

# %% code 425.
import numpy as np
import metpy.calc as mpcalc
from metpy.units import units as u
                   
# 온위 계산
df_selected_time['potential_T'] = \
        mpcalc.potential_temperature(df_selected_time['기압(hPa)'].values * u.hPa, 
                df_selected_time['기온(°C)'].values * u.degC)

show_levels(['potential_T'])

# %% code 426.
# 상대습도 계산
df_selected_time['relative_humidity_from_dewpoint'] = \
        mpcalc.relative_humidity_from_dewpoint(df_selected_time['기온(°C)'].values * u.degC,
                df_selected_time['이슬점온도(°C)'].values * u.degC)

show_levels(['relative_humidity_from_dewpoint'])

# %% code 427.
# 혼합비 계산 (단위 kg/kg)
df_selected_time['saturation_mixing_ratio'] = \
        mpcalc.saturation_mixing_ratio(df_selected_time['기압(hPa)'].values * u.hPa,
                df_selected_time['기온(°C)'].values * u.degC)
df_selected_time['mixing_ratio_from_relative_humidity'] = \
        mpcalc.mixing_ratio_from_relative_humidity(df_selected_time['기압(hPa)'].values * u.hPa,
                df_selected_time['기온(°C)'].values * u.degC,                                   
                df_selected_time['relative_humidity_from_dewpoint'].values * u.dimensionless)  # 0~1 비율
        
show_levels(['saturation_mixing_ratio',
             'mixing_ratio_from_relative_humidity'])

# %% code 428.
# 수증기압 계산 — 두 값 모두 hPa로 맞춘 뒤 숫자만 저장
df_selected_time['saturation_vapor_pressure(hPa)'] = \
        mpcalc.saturation_vapor_pressure(df_selected_time['기온(°C)'].values * u.degC).to('hPa').m
df_selected_time['vapor_pressure(hPa)'] = \
        mpcalc.vapor_pressure(df_selected_time['기압(hPa)'].values * u.hPa, 
                df_selected_time['mixing_ratio_from_relative_humidity'].values * u.dimensionless).to('hPa').m

show_levels(['saturation_vapor_pressure(hPa)', 'vapor_pressure(hPa)'])

# %% code 429.
# 상대습도 계산 (결과는 0~1 비율, 100을 곱하면 %)
df_selected_time['relative_humidity_from_mixing_ratio'] =\
        mpcalc.relative_humidity_from_mixing_ratio(df_selected_time['기압(hPa)'].values * u.hPa,
                df_selected_time['기온(°C)'].values * u.degC,
                df_selected_time['mixing_ratio_from_relative_humidity'].values * u.dimensionless)

show_levels(['relative_humidity_from_mixing_ratio'])

# %% code 430.
import numpy as np
import metpy.calc as mpcalc
from metpy.units import units as u
                   
# 가온도 계산
df_selected_time['virtual_temperature'] =\
        mpcalc.virtual_temperature(df_selected_time['기온(°C)'].values * u.degC,
                df_selected_time['mixing_ratio_from_relative_humidity'].values * u.dimensionless)
    
# 가온위 계산
df_selected_time['virtual_potential_temperature'] =\
        mpcalc.virtual_potential_temperature(df_selected_time['기압(hPa)'].values * u.hPa, 
                df_selected_time['기온(°C)'].values * u.degC,
                df_selected_time['mixing_ratio_from_relative_humidity'].values * u.dimensionless)

show_levels(['virtual_temperature', 'virtual_potential_temperature'])

# %% code 431.
import numpy as np
import metpy.calc as mpcalc
import matplotlib.pyplot as plt
from metpy.plots import SkewT
from metpy.units import units as u

# 새 그림 만들기
fig = plt.figure(figsize=(5.8, 5.0)) 

# 온도축과 기압축 범위 지정
xxlim = [-50, 50]       #온도축
yylim = [1050.1, 99.9]  #기압축

# 온도축 기울기 지정
skew = SkewT(fig, rotation=45)

skew.ax.set_title('Skew T-log P 단열선도\n', fontsize=10) 
skew.ax.set_xlabel(r'기온 (${\degree \mathrm{C}}$)', fontsize=9)
skew.ax.set_ylabel(r'기압 (${\mathrm{hPa}}$)', fontsize=9)

#등온선 그리는 함수
add_isothermal(skew)

#기압축 그리는 함수
add_isobar(skew)

# 건조 단열선 — 라벨은 300 hPa 높이에
add_dry_adiabats(skew, label_p=300, label_every=2)

# 습윤 단열선 — 라벨은 600 hPa 높이에
add_moist_adiabats(skew, label_p=600, label_every=5)

# 포화 혼합비선 — 라벨은 850 hPa 높이에
add_mixing_lines(skew, label_p=850, label_every=2)

# 관측값에 단위 붙이기 — 아래 계산에서 되풀이해 쓴다
p = df_selected_time['기압(hPa)'].values * u.hPa              # 기압
T = df_selected_time['기온(°C)'].values * u.degC              # 기온
Td = df_selected_time['이슬점온도(°C)'].values * u.degC       # 이슬점

# 기온: 원을 찍고 실선으로 잇기
skew.plot(p, T, 'ro', markersize = 8, fillstyle='none', label='기온')
skew.plot(p, T, 'r')

# 이슬점: 삼각형을 찍고 파선으로 잇기
skew.plot(p, Td, 'g^', markersize = 8, fillstyle='none', label='이슬점')
skew.plot(p, Td, 'g', linestyle='--')

# 기압에 따른 바람 표시
skew.plot_barbs(p, df_selected_time['u_wind'], df_selected_time['v_wind'])

# 지면(맨 아래 층) 공기덩이의 상승 경로 — 한 번 계산해 아래에서 되풀이해 쓴다
prof = mpcalc.parcel_profile(p, T[0], Td[0]).to(u.degC)
skew.plot(p, prof, 'k', linewidth=1.5)

# CIN(지면~LFC)과 CAPE(LFC~EL) 영역 음영 표시
skew.shade_cin(p, T, prof)
skew.shade_cape(p, T, prof)

# 상승응결고도(LCL)·자유대류고도(LFC)·평형고도(EL) 계산
lcl_pressure, lcl_temperature = mpcalc.lcl(p[0], T[0], Td[0])
skew.plot(lcl_pressure, lcl_temperature, 'ko',                 # LCL: 검은 원
          markersize = 8, fillstyle='none', label='LCL')

LFC_pressure, LFC_temperature = mpcalc.lfc(p, T, Td, prof)
skew.plot(LFC_pressure, LFC_temperature, 'rx',                 # LFC: 빨간 x
          markersize = 8, fillstyle='none', label='LFC')

EL_pressure, EL_temperature = mpcalc.el(p, T, Td, prof)
skew.plot(EL_pressure, EL_temperature, 'bo',                   # EL: 파란 원
          markersize = 8, fillstyle='none', label='EL')

# 가장 불안정한 공기덩이 — 지면에서 300 hPa 두께 안에서 상당온위가 가장 높은 층
mup_pressure, mup_temperature, mup_dewTemperature, mup_index = \
        mpcalc.most_unstable_parcel(p, T, Td)
skew.plot(mup_pressure, mup_temperature, 'bs', markersize=8, fillstyle='none',
        label='가장 불안정한 공기덩이')

# 가강수량과 지면 공기덩이의 CAPE·CIN 계산
precipitable_water = mpcalc.precipitable_water(p, Td)
cape, cin = mpcalc.cape_cin(p, T, Td, prof)
print(f'CAPE : {cape.m:.1f} J/kg,  CIN : {cin.m:.1f} J/kg')
print(f'LCL : {lcl_pressure.m:.1f} hPa,  LFC : {LFC_pressure.m:.1f} hPa,  EL : {EL_pressure.m:.1f} hPa')
print(f'가장 불안정한 공기덩이 : {mup_pressure.m:.1f} hPa,  가강수량 : {precipitable_water.m:.1f} mm')

# 글자를 넣을 아래 여백 먼저 확보
fig.subplots_adjust(bottom=0.27)

# 그림 아래 설명글
info_left = [
    (f'LCL : {lcl_pressure.m:.1f} hPa, {lcl_temperature.m:.1f} °C', 'o',
     'black'),
    (f'LFC : {LFC_pressure.m:.1f} hPa, {LFC_temperature.m:.1f} °C', 'x',
     'red'),
    (f'EL  : {EL_pressure.m:.1f} hPa, {EL_temperature.m:.1f} °C', 'o',
     'blue'),
    (f'가강수량 : {precipitable_water.m:.1f} mm', '', ''),
    (f'가장 불안정한 공기덩이 : {mup_pressure.m:.1f} hPa', '□', 'blue'),
]

info_right = [
    f'파일 : {fpaths[0].name}',
    f'시각 : {target_date_strf} (UTC)',
    'MetPy로 작성',
]

# figure 좌표로 배치
TOP, STEP, SIZE = 0.15, 0.027, 8

for k, (text, mark, mcolor) in enumerate(info_left):
    y = TOP - k * STEP
    if mark:                       # 그림에서 쓰는 기호를 글 앞에 함께 보여 준다
        fig.text(0.055, y, mark, fontsize=SIZE, color=mcolor, ha='center',
                 va='top')
    fig.text(0.075, y, text, fontsize=SIZE, ha='left', va='top')

for k, text in enumerate(info_right):
    fig.text(0.56, TOP - k * STEP, text, fontsize=SIZE, ha='left', va='top')

# 범례(legend) 추가 — 저장하기 전에 넣어야 파일에도 들어감
plt.legend(loc='upper left', fontsize=7)

# 단열선도 저장하기
plt.savefig(f"{proj_dir}/{fpaths[0].stem}_{target_date.strftime('%Y%m%d_%HUTC')}.pdf")   # 파일 이름에 ':'를 쓰지 않음

plt.show()

# %% code 432.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
from metpy.plots import SkewT
from metpy.units import units as u

def select_sounding(df, time_str):
    """시각(UTC 문자열) 하나의 관측만 골라 기압이 낮아지는 순서로 정렬"""
    sel = df[df['일시(UTC)'] == time_str]
    return sel.sort_values('기압(hPa)', ascending=False)

def sounding_indices(sel):
    """지면 공기덩이의 상승 경로와 CAPE · CIN · LCL · LFC · EL · 가강수량 계산"""
    p = sel['기압(hPa)'].values * u.hPa
    T = sel['기온(°C)'].values * u.degC
    Td = sel['이슬점온도(°C)'].values * u.degC
    prof = mpcalc.parcel_profile(p, T[0], Td[0]).to(u.degC)     # 상승 경로
    cape, cin = mpcalc.cape_cin(p, T, Td, prof)
    lcl_p, lcl_t = mpcalc.lcl(p[0], T[0], Td[0])
    lfc_p, lfc_t = mpcalc.lfc(p, T, Td, prof)
    el_p, el_t = mpcalc.el(p, T, Td, prof)
    pw = mpcalc.precipitable_water(p, Td)
    return dict(p=p, T=T, Td=Td, prof=prof,
                CAPE=cape.m, CIN=cin.m, LCL=lcl_p.m, LCL_T=lcl_t.to('degC').m,
                LFC=lfc_p.m, LFC_T=lfc_t.to('degC').m,
                EL=el_p.m, EL_T=el_t.to('degC').m, PW=pw.to('mm').m)

summer_time = '2018-08-28 12:00'
sel_s = select_sounding(df, summer_time)
r_s = sounding_indices(sel_s)
u_s, v_s = mpcalc.wind_components(sel_s['풍속(knot)'].values * u.knots,
                                  sel_s['풍향(deg)'].values * u.deg)

fig = plt.figure(figsize=(5.8, 5.0))
xxlim = [-50, 50]       # 온도축 (기준선 함수가 이 값을 씀)
yylim = [1050.1, 99.9]  # 기압축
skew = SkewT(fig, rotation=45)
skew.ax.set_title('Skew T-log P 단열선도\n', fontsize=10)
skew.ax.set_xlabel(r'기온 (${\degree \mathrm{C}}$)', fontsize=9)
skew.ax.set_ylabel(r'기압 (${\mathrm{hPa}}$)', fontsize=9)

# 기준선
add_isothermal(skew)
add_isobar(skew)
add_dry_adiabats(skew, label_p=300, label_every=2)
add_moist_adiabats(skew, label_p=600, label_every=5)
add_mixing_lines(skew, label_p=850, label_every=2)

# 관측값 : 기온(빨강 원) · 이슬점(초록 삼각형) · 바람
skew.plot(r_s['p'], r_s['T'], 'ro', markersize=8, fillstyle='none', label='기온')
skew.plot(r_s['p'], r_s['T'], 'r')
skew.plot(r_s['p'], r_s['Td'], 'g^', markersize=8, fillstyle='none',
          label='이슬점')
skew.plot(r_s['p'], r_s['Td'], 'g', linestyle='--')
skew.plot_barbs(r_s['p'], u_s, v_s)

# 상승 경로와 CAPE · CIN 음영
skew.plot(r_s['p'], r_s['prof'], 'k', linewidth=1.5)
skew.shade_cin(r_s['p'], r_s['T'], r_s['prof'])
skew.shade_cape(r_s['p'], r_s['T'], r_s['prof'])

# LCL · LFC · EL
skew.plot(r_s['LCL'] * u.hPa, r_s['LCL_T'] * u.degC, 'ko', markersize=8,
          fillstyle='none', label='LCL')
skew.plot(r_s['LFC'] * u.hPa, r_s['LFC_T'] * u.degC, 'rx', markersize=8,
          label='LFC')
skew.plot(r_s['EL'] * u.hPa, r_s['EL_T'] * u.degC, 'bo', markersize=8,
          fillstyle='none', label='EL')

print(f"CAPE : {r_s['CAPE']:.1f} J/kg,  CIN : {r_s['CIN']:.1f} J/kg")
print(f"LCL : {r_s['LCL']:.1f} hPa,  LFC : {r_s['LFC']:.1f} hPa,  EL : {r_s['EL']:.1f} hPa")
print(f"가강수량 : {r_s['PW']:.1f} mm")

# 그림 아래 설명글
fig.subplots_adjust(bottom=0.27)
info_left = [
    (f"LCL : {r_s['LCL']:.1f} hPa, {r_s['LCL_T']:.1f} °C", 'o', 'black'),
    (f"LFC : {r_s['LFC']:.1f} hPa, {r_s['LFC_T']:.1f} °C", 'x', 'red'),
    (f"EL  : {r_s['EL']:.1f} hPa, {r_s['EL_T']:.1f} °C", 'o', 'blue'),
    (f"CAPE : {r_s['CAPE']:.0f} J/kg,  CIN : {r_s['CIN']:.0f} J/kg", '', ''),
    (f"가강수량 : {r_s['PW']:.1f} mm", '', ''),
]
info_right = [
    f'파일 : {fpaths[0].name}',
    f'시각 : {summer_time} (UTC)',
    'MetPy로 작성',
]
TOP, STEP, SIZE = 0.15, 0.027, 8
for k, (text, mark, mcolor) in enumerate(info_left):
    y = TOP - k * STEP
    if mark:
        fig.text(0.055, y, mark, fontsize=SIZE, color=mcolor, ha='center', va='top')
    fig.text(0.075, y, text, fontsize=SIZE, ha='left', va='top')
for k, text in enumerate(info_right):
    fig.text(0.56, TOP - k * STEP, text, fontsize=SIZE, ha='left', va='top')

plt.legend(loc='upper left', fontsize=7)
stamp = pd.Timestamp(summer_time).strftime('%Y%m%d_%HUTC')    # 파일 이름에 쓸 수 있는 꼴
plt.savefig(f'{proj_dir}/{fpaths[0].stem}_{stamp}.pdf')
plt.savefig(f'{proj_dir}/{fpaths[0].stem}_{stamp}.png', dpi=150)
plt.show()

# %% code 433.
rows = {}
for label, t in [('겨울 2018-01-12 12 UTC', '2018-01-12 12:00'),
                 ('여름 2018-08-28 12 UTC', '2018-08-28 12:00')]:
    r = sounding_indices(select_sounding(df, t))
    rows[label] = {'지면 기온(°C)': r['T'][0].m, '지면 이슬점(°C)': r['Td'][0].m,
                   'CAPE(J/kg)': r['CAPE'], 'CIN(J/kg)': r['CIN'],
                   'LCL(hPa)': r['LCL'], 'LFC(hPa)': r['LFC'], 'EL(hPa)': r['EL'],
                   '가강수량(mm)': r['PW']}

compare = pd.DataFrame(rows).round(1)
compare
