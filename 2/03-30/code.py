# 지구과학 데이터 사이언스 2 | III-10. 측광 표준화
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅲ-235.
import os
from pathlib import Path

# %% code Ⅲ-236.
fname = ("TrES-4b_LIGHT_R_2024-06-13-15-09-52_"
         "120sec_GSON300_STF-8300M_-10c_1bin.fit")
fid = "1_ha7akgPnktWVQ8_s-r0BGqmqk-c1F_q"

du.download(f"https://docs.google.com/uc?export=download&id={fid}",
            proj_dir / fname)

# %% code Ⅲ-237.
fpaths = du.list_files(proj_dir, "fit*")

# %% code Ⅲ-238.
from astropy.io import fits
fpath = Path(fpaths[0])

hdul = fits.open(fpath)
flt = hdul[0].header["filter"]
for k in ["NAXIS1", "NAXIS2", "DATE-OBS", "EXPTIME", "OBJECT", "FILTER"]:
    if k in hdul[0].header:
        print(f"{k:9s} = {hdul[0].header[k]}")
print("data :", hdul[0].data.dtype, hdul[0].data.shape)

# %% code Ⅲ-239.
from astropy.coordinates import SkyCoord
from astropy import units as u

# %% code Ⅲ-240.
# `astropy.SkyCoord` 객체에 공통으로 쓰임
SKYC_KW = dict(unit=u.deg, frame='icrs')

# %% code Ⅲ-241.
#######################################################
# 망원경과 CCD
if hdul[0].header["CCDNAME"] == "STF-8300M" :
    gain = 0.37
    rdnoise = 9.3
    pix_size = 5.4 * u.um

if hdul[0].header["CCDNAME"] == "STX-16803" :
    gain = 1.27
    rdnoise = 9.0
    pix_size = 9 * u.um

if hdul[0].header["OPTIC"] == "GSON300" :
    focal_length = 1200 * u.mm

if hdul[0].header["OPTIC"] == "RiLA600" :
    focal_length = 3000 * u.mm

print("rdnoise, gain, pix_size, focal_length :", rdnoise, gain, pix_size,
      focal_length)

# %% code Ⅲ-242.
#######################################################
# PIXSCALE
if 'PIXSCALE' in hdul[0].header:
    PIX2ARCSEC = hdul[0].header['PIXSCALE']
else :  # 화소 크기(um, 비닝 반영)와 초점 거리(mm)로 계산
    PIX2ARCSEC = (206.265 * hdul[0].header['XPIXSZ']
                  / hdul[0].header['FOCALLEN'])

PIX2ARCSEC = PIX2ARCSEC # * u.arcsec / u.pixel
print("PIX2ARCSEC :", PIX2ARCSEC)

# %% code Ⅲ-243.
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS

# 관측 시각을 정하려고 관측 시작 시각과 노출 시간 확인
t_start = Time(hdul[0].header['DATE-OBS'], format='isot')
t_expos = hdul[0].header['EXPTIME'] * u.s
t_middle = t_start + t_expos / 2 # 시작 시각 + 노출 시간의 절반

print(f"t_start: {t_start}, t_expos: {t_expos}, t_middle: {t_middle}")

# %% code Ⅲ-244.
# 영상 표시 함수 znorm · zimshow · norm_imshow: Ⅲ-04 「FITS 파일 다루기」의 「zscale로 표시하는 함수(zimshow)」 (dses_utils 에 들어 있음)

# %% code Ⅲ-245.
# 위치 보정 여부 확인 — Ⅲ-06에서 만든 du.checkPSolve(dses_utils)
SOLVE, ASTAP, LOCAL = du.checkPSolve(str(fpath))
print("SOLVE, ASTAP, LOCAL :", SOLVE, ASTAP, LOCAL)

# %% code Ⅲ-246.
from astropy.wcs import WCS

wcs = WCS(hdul[0].header)
print("wcs :", wcs)

wcs.pixel_n_dim

# %% code Ⅲ-247.
# 영상 중심 화소(0부터 센 번호)를 하늘 좌표로 바꿈
nx, ny = hdul[0].header["NAXIS1"], hdul[0].header["NAXIS2"]
cent_coord = wcs.pixel_to_world((nx - 1) / 2, (ny - 1) / 2)
print("cent_coord: {}".format(cent_coord))

# 모든 화소를 감싸는 가장 작은 원의 반지름 = 네 모서리까지 거리의 최댓값
corners = wcs.pixel_to_world([-0.5, nx - 0.5, -0.5, nx - 0.5],
                             [-0.5, -0.5, ny - 0.5, ny - 0.5])
rad = cent_coord.separation(corners).max().to(u.deg)
print("rad: {}".format(rad))  # 시야각(FOV)으로 구한 반지름

pos_sky = SkyCoord(cent_coord, unit='deg')
pos_pix = pos_sky.to_pixel(wcs=wcs)

print("pos_sky: {}".format(pos_sky))
print("pos_pix: {}".format(pos_pix))

# %% code Ⅲ-248.
import numpy as np

#######################################################
# FWHM 초기 추정값(화소)
FWHM_INIT = 6

# 측광 변수
FWHM = FWHM_INIT
R_AP = 1.5*FWHM_INIT  # 구경 반지름
R_IN = 4*FWHM_INIT    # 고리(annulus) 안쪽 반지름
R_OUT = 6*FWHM_INIT   # 고리(annulus) 바깥쪽 반지름

Mag_Low = 11.5
Mag_High = 15

Mag_target = 12.5
Mag_delta = 2
ERR_Min = 0.5
#######################################################
from astroquery.vizier import Vizier

# r 등급 10.5~14.5, r 등급 오차 < 0.1, r 필터 관측 횟수 > 5
ps1_filters = {"rmag": f"{Mag_target-Mag_delta}..{Mag_target+Mag_delta}",
               "e_rmag": "<0.10", "nr": ">5"}
vquery = Vizier(columns=["**", "+_r"], column_filters=ps1_filters,
                row_limit=-1)
PS1_stars_all = vquery.query_region(cent_coord, radius=rad,
                                    catalog="II/349/ps1")[0]
print("type(PS1_stars_all) :", type(PS1_stars_all))
print("len(PS1_stars_all) :", len(PS1_stars_all))

# %% code Ⅲ-249.
df_stars_all = PS1_stars_all.to_pandas()
print("type(df_stars_all) :", type(df_stars_all))
print("len(df_stars_all) :", len(df_stars_all))
df_stars_all.head()

# %% code Ⅲ-250.
# 비교 측광에 맞지 않는 천체를 나타내는 f_objID(objInfoFlag)의 비트 위치
# 관측 횟수 부족·낮은 품질, 퀘이사, 변광성, 일시 천체, 태양계 천체, 은하
PS1_DEL_FLAG_BITS = [0, 1, 2, 3, 5, 7, 8, 9, 10, 23, 24]

def select_in_fov(tab, wcs, shape, bezel=0):
    """화소 좌표 x, y 열을 더하고 가장자리 안쪽의 별만 남김."""
    coo = SkyCoord(tab["RAJ2000"], tab["DEJ2000"], **SKYC_KW)
    x, y = wcs.world_to_pixel(coo)
    tab["x"], tab["y"] = x, y
    ny, nx = shape
    inside = ((x > bezel) & (x < nx - 1 - bezel)
              & (y > bezel) & (y < ny - 1 - bezel))
    print(f"FOV   : {len(tab)} -> {inside.sum()} (bezel {bezel:.1f} px)")
    return tab[inside]

def drop_ps1_flags(tab, drop_by_kron=True):
    """f_objID 깃발과 크론 등급으로 비교성에 맞지 않는 천체를 뺌."""
    flags = np.ma.filled(tab["f_objID"], 0).astype(np.int64)
    bad = np.zeros(len(tab), dtype=bool)
    for bit in PS1_DEL_FLAG_BITS:
        bad |= ((flags >> bit) & 1).astype(bool)
    print(f"flags : {len(tab)} -> {(~bad).sum()}")
    tab = tab[~bad]
    if drop_by_kron:                     # 점광원 등급 - 크론 등급 > 0.05
        dmag = np.ma.filled(tab["imag"] - tab["iKmag"], 0.0)
        galaxy = dmag > 0.05
        print(f"Kron  : {len(tab)} -> {(~galaxy).sum()}")
        tab = tab[~galaxy]
    return tab

from scipy.spatial import cKDTree

def drop_star_groups(tab, crit_sep):
    """서로 crit_sep 화소보다 가까운 별은 짝을 모두 뺌."""
    pts = np.column_stack([tab["x"], tab["y"]])
    pairs = cKDTree(pts).query_pairs(r=crit_sep)   # 가까운 쌍 (i, j)
    grouped = np.zeros(len(tab), dtype=bool)
    for i, j in pairs:
        grouped[[i, j]] = True
    print(f"group : {len(tab)} -> {(~grouped).sum()} ({crit_sep:.1f} px)")
    return tab[~grouped]

def add_jc_mags(tab):
    """g, r 등급으로 B, V, R 등급과 g-r 색지수를 계산해 열로 더함."""
    def col(name):                       # 빈 값은 NaN 인 실수 배열로
        return np.ma.filled(tab[name], np.nan).astype(float)
    gr = col("gmag") - col("rmag")
    e_gr = np.hypot(col("e_gmag"), col("e_rmag"))   # 제곱합의 제곱근
    tab["grcolor"], tab["e_grcolor"] = gr, e_gr
    # 밴드: (상수항, (g-r) 계수, 변환식의 흩어짐, 기준 등급) - Tonry+2012
    pars = dict(B=(0.213, 0.587, 0.034, "gmag"),
                V=(0.006, 0.474, 0.012, "rmag"),
                R=(-0.138, -0.131, 0.015, "rmag"))
    for band, (c0, c1, sc, base) in pars.items():
        tab[f"{band}mag"] = c0 + c1 * gr + col(base)
        # 편미분 계수: 기준 등급이 g 이면 (1 + c1, -c1), r 이면 (c1, 1 - c1)
        dg, dr = (1 + c1, -c1) if base == "gmag" else (c1, 1 - c1)
        tab[f"e_{band}mag"] = np.sqrt((dg * col("e_gmag"))**2
                                      + (dr * col("e_rmag"))**2 + sc**2)
    return tab

# %% code Ⅲ-251.
df_stars_all = PS1_stars_all.to_pandas()
df_stars_all = df_stars_all.dropna(subset=["gmag", "rmag"])
print(df_stars_all.columns)

ps1_stars = select_in_fov(PS1_stars_all.copy(), wcs, hdul[0].data.shape,
                          bezel=5*FWHM_INIT)
ps1_stars = drop_star_groups(ps1_stars, crit_sep=6*FWHM_INIT)
ps1_stars = drop_ps1_flags(ps1_stars)
ps1_stars = add_jc_mags(ps1_stars)

df_stars = ps1_stars.to_pandas()
print("len(df_stars):", len(df_stars))
df_stars = df_stars.dropna(subset=["gmag", "rmag"])
print("len(df_stars):", len(df_stars))

# %% code Ⅲ-252.
import numpy as np

pos_stars_all = np.array([df_stars_all["RAJ2000"].array,
                          df_stars_all["DEJ2000"].array]).T
pos_stars_all = SkyCoord(pos_stars_all, **SKYC_KW).to_pixel(wcs)
pos_stars_all = np.transpose(pos_stars_all)
# pos_stars_all # PS1 query 모든 별

pos_stars = np.array([df_stars["RAJ2000"].array, df_stars["DEJ2000"].array]).T
pos_stars = SkyCoord(pos_stars, **SKYC_KW).to_pixel(wcs)
pos_stars = np.transpose(pos_stars)
# pos_stars # PS1 query 중 비교 측광에 사용될 별

# %% code Ⅲ-253.
from photutils.aperture import CircularAperture as CAp
from photutils.aperture import CircularAnnulus as CAn
ap_stars = CAp(positions=pos_stars, r=R_IN)
ap_stars_all = CAp(positions=pos_stars_all, r=R_IN)

# %% code Ⅲ-254.
import matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 1, figsize=(7.5, 5),
                        subplot_kw={'projection': wcs},
                        sharex=False, sharey=False, gridspec_kw=None)

im = du.zimshow(axs, hdul[0].data, )
axs.coords.grid(True, color='white', ls=':')
axs.coords['ra'].set_axislabel('Right Ascension (J2000)', minpad=0.5,
                               fontsize=8)
axs.coords['ra'].set_ticklabel_position('bl')
axs.coords['dec'].set_axislabel('Declination (J2000)', minpad=0.4, fontsize=8)
axs.coords['dec'].set_ticklabel_position('bl')
axs.coords['ra'].set_axislabel_position('b')     # 축 이름이 겹치지 않게
axs.coords['dec'].set_axislabel_position('l')
axs.coords['ra'].set_major_formatter('hh:mm')
axs.coords['dec'].set_major_formatter('dd:mm')
axs.coords['ra'].display_minor_ticks(True)
axs.coords['dec'].display_minor_ticks(True)
axs.coords['ra'].set_minor_frequency(2)
axs.coords['dec'].set_minor_frequency(2)
axs.tick_params(labelsize=8)

for i in range(min(10, len(pos_stars))):   # 번호는 중심에 가까운 10개에만 붙임
    axs.text(pos_stars[i][0], pos_stars[i][1], f"Star #{str(i)}", fontsize=7,
             color='w')

ap_stars_all.plot(ax=axs, color='w', lw=1)
ap_stars.plot(ax=axs, color='r', lw=1)

axs.set_title(f"fname: {fpath.name}\n Comparison stars of PS1 (red, r = {Mag_target-Mag_delta}~{Mag_target+Mag_delta})",
              fontsize=10,)

cbar = plt.colorbar(im, ax = axs, fraction=0.035, pad=0.04, )
cbar.ax.tick_params(labelsize=8)

axs.annotate(f'Number of star(s): {len(pos_stars)}', fontsize=8,
    xy=(0, 0), xytext=(-10, -50), va='top', ha='left',
    xycoords='axes fraction', textcoords='offset points')

plt.tight_layout()
plt.savefig(proj_dir / f"{fpath.stem}_PS1_comparison.png")

plt.show()
#plt.close()

# %% code Ⅲ-255.
fig, axs = plt.subplots(1, 1, figsize=(7.5, 5),
                        subplot_kw={'projection': wcs},
                        sharex=False, sharey=False, gridspec_kw=None)

im = du.zimshow(axs, hdul[0].data, )

_phot_stars = []

for i, row in df_stars.iterrows():
    pos_star = SkyCoord(row["RAJ2000"], row["DEJ2000"],
                        **SKYC_KW).to_pixel(wcs)
    ap = CAp([pos_star[0], pos_star[1]], r=R_AP)
    an = CAn([pos_star[0], pos_star[1]], r_in=R_IN, r_out=R_OUT)
    _phot_star = du.apphot_annulus(hdul[0].data, ap, an,
                                gain=gain, rdnoise=rdnoise)
    _phot_star[f"{flt}mag"] = row[f"{flt}mag"]
    _phot_star[f"e_{flt}mag"] = row[f"e_{flt}mag"]
    _phot_star["gmag"] = row["gmag"]
    _phot_star["e_gmag"] = row["e_gmag"]
    _phot_star["rmag"] = row["rmag"]
    _phot_star["e_rmag"] = row["e_rmag"]
    _phot_star["grcolor"] = row["grcolor"]
    _phot_star["e_grcolor"] = row["e_grcolor"]
    _phot_star["id"] = i
    _phot_star["objID"] = int(row["objID"])
    _phot_stars.append(_phot_star)
    if i < 10:                           # 번호와 등급은 0~9번 별에만 적음
        axs.text(pos_star[0]+10, pos_star[1]+10,
                 f"star {i}:{row[f'{flt}mag']:.01f}", fontsize=8, color="w")
    ap.plot(ax=axs, color="orange")
 # an.plot(ax=axs, color="w")

axs.coords.grid(True, color='white', ls=':')
axs.coords['ra'].set_axislabel('Right Ascension (J2000)', minpad=0.5,
                               fontsize=8)
axs.coords['ra'].set_ticklabel_position('b')
axs.coords['dec'].set_axislabel('Declination (J2000)', minpad=0.4, fontsize=8)
axs.coords['dec'].set_ticklabel_position('l')
axs.coords['ra'].set_major_formatter('hh:mm')
axs.coords['dec'].set_major_formatter('dd:mm')

axs.coords['ra'].display_minor_ticks(True)
axs.coords['dec'].display_minor_ticks(True)
axs.coords['ra'].set_minor_frequency(2)
axs.coords['dec'].set_minor_frequency(2)
axs.tick_params(labelsize=8)

cbar = plt.colorbar(im, ax = axs, fraction=0.035, pad=0.04, )

axs.set_title(f"fname: {fpath.name}\n {flt} magnitude of PS1 comparison"
              f" stars (r = {Mag_target-Mag_delta}~{Mag_target+Mag_delta})",
              fontsize=10,)
axs.annotate(f'Number of star(s): {len(pos_stars)}', fontsize=8,
                            xy=(0, 0), xytext=(-10, -50), va='top', ha='left',
                            xycoords='axes fraction',
                            textcoords='offset points')

plt.tight_layout()
plt.savefig(proj_dir / f"{fpath.stem}_PS1_magnitude.png")

plt.show()

# %% code Ⅲ-256.
print("type(_phot_stars) :", type(_phot_stars))
print("len(_phot_stars) :", len(_phot_stars))

# %% code Ⅲ-257.
import pandas as pd
df_phot_stars = pd.concat(_phot_stars)
# phot_stars = phot_stars.loc[phot_stars["objID"] != 110823405221754720].copy() # star 15
print("type(df_phot_stars):",type(df_phot_stars))
print("len(df_phot_stars):",len(df_phot_stars))
print("df_phot_stars.columns:", df_phot_stars.columns)
# print(phot_stars)
df_phot_stars

# %% code Ⅲ-258.
df_phot_stars_na = df_phot_stars.dropna()
print(len(df_phot_stars_na))

df_phot_stars_na = df_phot_stars[df_phot_stars["merr"] < ERR_Min]
# phot_stars_na = phot_stars_na.set_index('id', drop=True)
df_phot_stars_na = df_phot_stars_na.reset_index(drop=True)
print(len(df_phot_stars_na))
# print(df_phot_stars_na)
df_phot_stars_na

# %% code Ⅲ-259.
merr_total1 = np.sqrt((df_phot_stars_na["merr"])**2 + (df_phot_stars_na[f"e_{flt}mag"])**2)

# === 영점(zero point)과 오차 계산
_xx = np.linspace(Mag_Low, Mag_High)
dmag = df_phot_stars_na["mag"] - df_phot_stars_na[f"{flt}mag"]             # m - M (별마다의 영점)
zeropt_med = np.median(dmag)
zeropt_avg = np.average(dmag, weights=1/merr_total1**2)
resid = dmag - zeropt_med                      # 영점 잔차
dzeropt = np.max([1/np.sqrt(np.sum(1/merr_total1**2)),        # 가중 평균의 오차
                  np.std(resid, ddof=1)/np.sqrt(len(resid))])  # 잔차의 표준 오차
merr_total2 = np.sqrt(merr_total1**2 + dzeropt**2)  # 별마다의 오차 + 영점 오차
print(f"N = {len(resid)}, Z(중앙값) = {zeropt_med:.3f}, Z(가중 평균) = {zeropt_avg:.3f}")
print(f"잔차 표준편차 = {np.std(resid, ddof=1):.3f}, "
      f"가중 평균의 오차 = {1/np.sqrt(np.sum(1/merr_total1**2)):.4f}, "
      f"σ_Z = {dzeropt:.4f}")

# %% code Ⅲ-260.
def linf(x, a, b):
    return a + b*x
from scipy.optimize import curve_fit

# === 맞춤 직선 찾기
# scipy.optimize.curve_fit 으로 직선 맞춤
poptm, _ = curve_fit(linf, df_phot_stars_na[f"{flt}mag"],
                     df_phot_stars_na["mag"],
                     sigma= df_phot_stars_na["merr"], absolute_sigma=True)
poptc, pcovc = curve_fit(linf, df_phot_stars_na["grcolor"],
                         df_phot_stars_na["mag"] - df_phot_stars_na[f"{flt}mag"],
                         sigma=merr_total2, absolute_sigma=True)
ec = np.sqrt(np.diag(pcovc))   # 절편과 기울기의 오차
print(f"색항: 기울기 = {poptc[1]:+.4f} ± {ec[1]:.4f} ({abs(poptc[1])/ec[1]:.1f}σ), "
      f"절편 = {poptc[0]:.3f} ± {ec[0]:.3f}")
resid_c = (df_phot_stars_na["mag"] - df_phot_stars_na[f"{flt}mag"]
           - linf(df_phot_stars_na["grcolor"], *poptc))
print(f"색항을 보정한 뒤 잔차 표준편차 = {np.std(resid_c, ddof=1):.3f}")
print(f"g - r 범위: {df_phot_stars_na['grcolor'].min():.2f} ~ "
      f"{df_phot_stars_na['grcolor'].max():.2f}")

# 비교: PS1 이 포화되기 쉬운 밝은 별(g 또는 r < 14)을 뺀 색항
faint = (df_phot_stars_na["gmag"] > 14) & (df_phot_stars_na["rmag"] > 14)
d14 = df_phot_stars_na[faint]
poptc14, pcovc14 = curve_fit(linf, d14["grcolor"], d14["mag"] - d14[f"{flt}mag"],
                             sigma=merr_total2[faint], absolute_sigma=True)
resid14 = d14["mag"] - d14[f"{flt}mag"] - linf(d14["grcolor"], *poptc14)
print(f"g, r > 14 인 별 {faint.sum()}개: 기울기 = {poptc14[1]:+.4f} ± "
      f"{np.sqrt(pcovc14[1, 1]):.4f}, 보정 전 잔차 표준편차 = "
      f"{np.std(d14['mag'] - d14[f'{flt}mag'], ddof=1):.3f}, 보정 후 = "
      f"{np.std(resid14, ddof=1):.3f}")

# %% code Ⅲ-261.
import logging
logging.getLogger("fontTools").setLevel(logging.ERROR)   # PDF 글꼴 저장 알림 감춤

d = df_phot_stars_na
dm = d["mag"] - d[f"{flt}mag"]                          # 별마다의 m - M
errkw = dict(fmt="+", ms=5, ecolor="lightgray", elinewidth=0.5)

fig, axs = plt.subplots(1, 3, figsize=(7.5, 3.4), constrained_layout=True)
axs[0].errorbar(d[f"{flt}mag"], dm, xerr=d[f"e_{flt}mag"], yerr=d["merr"], **errkw)
axs[1].errorbar(d["grcolor"], dm, xerr=d["e_grcolor"], yerr=merr_total2, **errkw)
xx = np.array([d["grcolor"].min(), d["grcolor"].max()])
axs[1].plot(xx, linf(xx, *poptc), "g-", lw=1, label=f"색항 기울기 {poptc[1]:+.3f}")
for ax in axs[:2]:
    ax.axhline(zeropt_med, color="r", lw=1, label=f"Z(중앙값) {zeropt_med:.3f}")
    ax.axhline(zeropt_avg, color="b", lw=1, ls="--", label=f"Z(가중 평균) {zeropt_avg:.3f}")
    ax.axhspan(zeropt_med - dzeropt, zeropt_med + dzeropt, color="r", alpha=0.15)
    ax.set_ylim(zeropt_med - 0.8, zeropt_med + 0.8)
    ax.set_ylabel("$m - M$ (mag)", fontsize=11)
    ax.legend(fontsize=8.5, loc="lower left")
axs[0].set_xlabel(f"$M$ ({flt}, PS1 by Tonry+2012)", fontsize=11)
axs[1].set_xlabel("$g - r$ (PS1)", fontsize=11)

axs[2].errorbar(d[f"{flt}mag"], d["mag"], xerr=d[f"e_{flt}mag"], yerr=d["merr"], **errkw)
xx = np.array([d[f"{flt}mag"].min(), d[f"{flt}mag"].max()])
axs[2].plot(xx, xx + zeropt_med, "r-", lw=1, label="$m = M + Z$")
axs[2].plot(xx, linf(xx, *poptm), "g-", lw=1, label=f"맞춘 직선(기울기 {poptm[1]:.3f})")
axs[2].set_xlabel(f"$M$ ({flt})", fontsize=11)
axs[2].set_ylabel("$m$ (mag)", fontsize=11)
axs[2].legend(fontsize=8.5, loc="upper left")
for ax in axs:
    ax.tick_params(labelsize=9)
    ax.grid(ls=":")
fig.suptitle(f"영점과 색항 ({flt} 필터, 비교성 {len(d)}개)", fontsize=13)
plt.savefig(proj_dir / f"{fpath.stem}_standardization_extended.png")
plt.show()

# %% code Ⅲ-262.
# 뺄 별: g 또는 r 등급이 14보다 밝은 별(PS1 포화 위험)
mask = (df_phot_stars_na["gmag"] <= 14) | (df_phot_stars_na["rmag"] <= 14)
print(f"전체 {len(mask)}개 중 뺄 별 {mask.sum()}개, 남는 별 {(~mask).sum()}개")

# %% code Ⅲ-263.
# 걸러 낸 별을 뺀 비교성(good)으로 영점과 색항을 구함
good = df_phot_stars_na[~mask]
M_cat, m_inst = good[f"{flt}mag"], good["mag"]           # 성표 등급, 기기 등급

# === 영점(zero point)과 오차 계산
merr_total1 = np.sqrt(good["merr"]**2 + good[f"e_{flt}mag"]**2)   # 기기 등급 오차 + 성표 등급 오차
dmag = m_inst - M_cat                                     # m - M (별마다의 영점)
zeropt_med = np.median(dmag)
zeropt_avg = np.average(dmag, weights=1/merr_total1**2)
resid = dmag - zeropt_med                                 # 영점 잔차
dzeropt = np.max([1/np.sqrt(np.sum(1/merr_total1**2)),         # 가중 평균의 오차
                  np.std(resid, ddof=1)/np.sqrt(len(resid))])   # 잔차의 표준 오차
merr_total2 = np.sqrt(merr_total1**2 + dzeropt**2)        # 별마다의 오차 + 영점 오차

# === 직선 맞춤(scipy.optimize.curve_fit): 기기 등급 대 성표 등급, m - M 대 색지수
poptm, _ = curve_fit(linf, M_cat, m_inst, sigma=good["merr"], absolute_sigma=True)
poptc, _ = curve_fit(linf, good["grcolor"], dmag, sigma=merr_total2, absolute_sigma=True)

# === 결과 비교 그림: 왼쪽 m - M 대 성표 등급, 오른쪽 m - M 대 색지수
dm_all = df_phot_stars_na["mag"] - df_phot_stars_na[f"{flt}mag"]
fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.2), sharey=True, constrained_layout=True)
for ax, xcol, xlabel in zip(axs, [f"{flt}mag", "grcolor"],
                            [f"${{{flt}}}_{{PS1}}$", "$g - r$ (PS1)"]):
    ax.plot(df_phot_stars_na.loc[mask, xcol], dm_all[mask], "x", color="gray",
            label="뺀 별")
    ax.errorbar(good[xcol], dmag, yerr=merr_total1,
                fmt="+", color="C0", ecolor="lightgray", elinewidth=0.5, label="남은 별")
    ax.axhline(zeropt_med, color="r", lw=1, label=f"Z(중앙값) = {zeropt_med:.3f} ± {dzeropt:.3f}")
    ax.axhline(zeropt_avg, color="b", lw=1, label=f"Z(가중 평균) = {zeropt_avg:.3f}")
    ax.set(xlabel=xlabel, ylim=(zeropt_med - 0.8, zeropt_med + 0.8))
xx = np.array(axs[1].get_xlim())
axs[1].plot(xx, linf(xx, *poptc), "g-", lw=1, label=f"색항 기울기 {poptc[1]:+.3f}")
axs[0].set_ylabel(f"${{{flt}}}_{{inst}} - {{{flt}}}_{{PS1}}$")
axs[0].legend(fontsize=8.5, loc="lower left")
axs[1].legend(fontsize=8.5, loc="lower left")
plt.show()
print(f"남은 별 {len(dmag)}개: 영점(중앙값) {zeropt_med:.3f}, 가중 평균 {zeropt_avg:.3f}, "
      f"오차 {dzeropt:.3f}, 잔차 표준편차 {np.std(resid, ddof=1):.3f}, 색항 기울기 {poptc[1]:+.3f}")

# %% code Ⅲ-264.
from astropy.stats import sigma_clipped_stats

FWHM = FWHM_INIT
_, _, std = sigma_clipped_stats(hdul[0].data)  # 기본값은 3σ, 5회 반복(배경 표준편차만 씀)
thresh = 5. * std   # 배경 위 높이(상대값)

from photutils.detection import DAOStarFinder
DAOfind = DAOStarFinder(
                        fwhm = FWHM,
                        threshold=thresh,
 # sharpness_range=(0.2, 1.0),   # 기본값
 # roundness_range=(-1.0, 1.0),  # 기본값
 # sigma_radius=1.5,             # 기본값
 # ratio=1.0,                    # 1.0: 원형 가우스
                        exclude_border=True         # 가장자리에 가까운 천체 제외
                        )

DAOfound = DAOfind(hdul[0].data)
print("len(DAOfound) :",len(DAOfound))
print(DAOfound.colnames)

df_DAO = DAOfound.to_pandas()
print(type(df_DAO))
df_DAO

# 중심 열 이름: photutils 3.0부터 x_centroid, 그 전 판은 xcentroid
xc, yc = ("x_centroid", "y_centroid") if "x_centroid" in DAOfound.colnames else ("xcentroid", "ycentroid")
pos = np.transpose((DAOfound[xc], DAOfound[yc]))
apert = CAp(pos, r=R_AP)
annul = CAn(positions=pos, r_in= R_IN, r_out=R_OUT)

# %% code Ⅲ-265.
# 검출한 모든 별을 Ⅲ-08 과 같은 방법(du.apphot_annulus)으로 측광
df_apphot = du.apphot_annulus(hdul[0].data, apert, annul, gain=gain, rdnoise=rdnoise)

sky_coord = wcs.pixel_to_world(df_apphot["x_center"], df_apphot["y_center"])
df_apphot["RAJ2000"] = sky_coord.ra.degree
df_apphot["DEJ2000"] = sky_coord.dec.degree
df_apphot["filename"] = fpath.stem
df_apphot["t_middle"] = t_middle.isot
df_apphot["filter"] = flt
df_apphot["zeropt"] = zeropt_med                                 # 밝은 별을 빼고 구한 영점
df_apphot["e_zeropt"] = dzeropt
df_apphot[f"{flt}_magnitude"] = df_apphot["mag"] - zeropt_med     # M = m - Z
df_apphot[f"e_{flt}_magnitude"] = np.hypot(df_apphot["merr"], dzeropt)
df_apphot.to_csv(f"{proj_dir}/{fpath.stem}_result_photometry.csv")

print(f"별 {len(df_apphot)}개 가운데 표준 등급을 구한 별 {df_apphot['mag'].notna().sum()}개 "
      f"(영점 Z = {zeropt_med:.3f} ± {dzeropt:.3f})")
df_apphot[["id", "x_center", "y_center", "msky", "source_sum", "mag", "merr", f"{flt}_magnitude"]].head()

# %% code Ⅲ-266.
df_apphot_sub = df_apphot.dropna(subset=["mag"])

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.2), constrained_layout=True)
axs[0].hist(df_apphot_sub[f"{flt}_magnitude"], bins=np.arange(9, 21, 0.5), edgecolor="white")
axs[0].set_xlabel(f"{flt} (mag)", fontsize=11)
axs[0].set_ylabel("별의 수", fontsize=11)
axs[1].plot(df_apphot_sub[f"{flt}_magnitude"], df_apphot_sub["merr"], "x", ms=4)
axs[1].set_yscale("log")
from matplotlib.ticker import FuncFormatter
axs[1].yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))   # 0.01 꼴 눈금(수식 글꼴 대신)
axs[1].yaxis.set_minor_formatter(FuncFormatter(lambda v, _: ""))
axs[1].set_xlabel(f"{flt} (mag)", fontsize=11)
axs[1].set_ylabel("등급 오차 (mag)", fontsize=11)
for ax in axs:
    ax.tick_params(labelsize=9)
    ax.grid(ls=":")
fig.suptitle(f"모든 별의 표준 등급 ({len(df_apphot_sub)}개)", fontsize=13)
plt.savefig(proj_dir / f"{fpath.stem}_Result_of_standardization.png")
plt.show()

for lim in [0.01, 0.05, 0.1]:
    print(f"등급 오차 < {lim}: {flt} < {df_apphot_sub.loc[df_apphot_sub['merr'] < lim, f'{flt}_magnitude'].max():.1f} 까지")
