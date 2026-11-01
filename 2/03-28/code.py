# 지구과학 데이터 사이언스 2 | III-08. 구경 측광
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 245.
# 한글 폰트 설정 — 공통 유틸리티(dses_utils) 사용
import dses_utils as du
import matplotlib.pyplot as plt
du.set_korean_font()

# %% code 246.
import os
from pathlib import Path
if not (proj_dir).exists():
    os.mkdir(str(proj_dir))
    print (f"{str(proj_dir)} is created...")
else : 
    print (f"{str(proj_dir)} already exists...")

# %% code 247.
fname = ("TrES-4b_LIGHT_R_2024-06-13-15-09-52_"
         "120sec_GSON300_STF-8300M_-10c_1bin.fit")
fid = "19Y2TMjSFUgldAWiXftpHHcFZ7N92ebhP"

du.download(f"https://docs.google.com/uc?export=download&id={fid}",
            proj_dir / fname)

# %% code 248.
fpaths = du.list_files(proj_dir, "fit*")

# %% code 249.
from astropy.io import fits

hdul = fits.open(str(fpaths[0]), unit="adu")

print("type(hdul) :", type(hdul))
print("type(hdul[0]) :", type(hdul[0]))

# %% code 250.
print("type(hdul[0].header) :", type(hdul[0].header))
for _k in ["NAXIS1", "NAXIS2", "DATE-OBS", "EXPTIME", "OBJECT", "FILTER"]:
    if _k in hdul[0].header:
        print(f"{_k:9s} = {hdul[0].header[_k]}")

# %% code 251.
print("hdul[0].header['DATE-OBS'] :", hdul[0].header['DATE-OBS'])
print("type(hdul[0].header['DATE-OBS']) :", type(hdul[0].header['DATE-OBS']))

# %% code 252.
print("type(hdul[0].data) :", type(hdul[0].data))
print("hdul[0].data.dtype :", hdul[0].data.dtype)
print("hdul[0].data.shape :", hdul[0].data.shape)
print("hdul[0].data :", hdul[0].data)

# %% code 253.
# 위치 보정 여부 확인 — Ⅲ-06 「FITS 파일 천체 위치 보정」에서 만든 du.checkPSolve(dses_utils)
SOLVE, ASTAP, LOCAL = du.checkPSolve(str(fpaths[0]))
print("SOLVE :", SOLVE)

# %% code 254.
from astropy.visualization import ZScaleInterval, ImageNormalize
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy import units as u

#####################################################################
# 관측 위치: 경기과학고등학교 관측소(수원, MPC 관측소 코드 P64)
LOCATION = dict(lon=127.005, lat=37.308889, elevation=101)
GSHS = EarthLocation(lon=127.005 * u.deg, lat=37.308889 * u.deg,
                     height=101 * u.m)
MPC_obscode = "P64"
#######################################################
# `astropy.SkyCoord` 객체에 공통으로 쓰임
SKYC_KW = dict(unit=u.deg, frame='icrs')

# 대략적인 추정값으로만 쓰이므로 정확하지 않아도 됨
#PIX2ARCSEC = 1.24*u.arcsec
if 'PIXSCALE' in hdul[0].header:
    PIX2ARCSEC = hdul[0].header['PIXSCALE']
else :
    # 픽셀 크기(um, 비닝 반영)와 초점 거리(mm)로 계산
    PIX2ARCSEC = 206.265 * hdul[0].header['XPIXSZ'] / hdul[0].header['FOCALLEN']

if hdul[0].header["CCDNAME"] == "STF-8300M" :
    gain = 0.37
    rdnoise = 9.3

if hdul[0].header["CCDNAME"] == "STX-16803" :
    gain = 1.27
    rdnoise = 9.0

print("rdnoise, gain, PIX2ARCSEC :", rdnoise, gain, PIX2ARCSEC)

# %% code 255.
from astropy.time import Time
from astropy.wcs import WCS
from astropy.nddata import Cutout2D
from astroquery.jplhorizons import Horizons

# 관측 시각을 정하려고 관측 시작 시각과 노출 시간 확인
t_start = Time(hdul[0].header['DATE-OBS'], format='isot')
t_expos = hdul[0].header['EXPTIME'] * u.s
t_middle = t_start + t_expos / 2 # 시작 시각 + 노출 시간의 절반

print(f"t_start: {t_start}, t_expos: {t_expos}, t_middle: {t_middle}")

# %% code 256.
#######################################################
# FWHM 초기 추정값(픽셀)
FWHM_INIT = 6

FWHM = FWHM_INIT
from photutils.segmentation import detect_threshold
thresh = detect_threshold(data=hdul[0].data, n_sigma=3)
thresh = thresh[0][0]
print('detect_threshold (배경 + 3σ, 절대 화소값):', thresh)

from astropy.stats import sigma_clipped_stats
avg, med, std = sigma_clipped_stats(hdul[0].data)  # 기본값은 3σ, 5회 반복
# DAOStarFinder 의 threshold 는 배경 위로 얼마나 높은지(상대 높이)이므로 5σ 를 씀
thresh = 5. * std
print(f"avg : {avg:.03f}, med: {med:.03f}, std: {std:.03f}, thresh: {thresh:.03f}")

# 측광 변수
R_AP = 1.5 * FWHM_INIT  # 구경 반지름
R_IN = 4 * FWHM_INIT    # 고리(annulus) 안쪽 반지름
R_OUT = 6 * FWHM_INIT   # 고리(annulus) 바깥쪽 반지름

print("FWHM, thresh :", FWHM, thresh)

# %% code 257.
from photutils.detection import DAOStarFinder

fpath = fpaths[0]
print("fpath", (fpath))

hdul =  fits.open(str(fpath), unit="adu")

FWHM = FWHM_INIT

DAOfind = DAOStarFinder(
                        fwhm = FWHM,
                        threshold = thresh,
 # sharplo = 0.2, sharphi = 1.0, # default values: sharplo=0.2, sharphi=1.0,
 # roundlo = 0, roundhi = 1.0, # default values -1 and +1
 # sigma_radius = 3, # default values 1.5
 # ratio = 0.5, # 1.0: circular gaussian
                        exclude_border = True         # 가장자리에 가까운 천체 제외
                        )

DAOfound = DAOfind(hdul[0].data)
print("len(DAOfound) :",len(DAOfound))

# %% code 258.
print("type(DAOfound) :", type(DAOfound))
print(DAOfound.colnames)
DAOfound

# %% code 259.
DAOfound.write(f"{proj_dir}/{fpath.stem}_DAOStarfinder_fwhm_{FWHM}_{thresh}.csv",
                            overwrite = True, format='ascii.fast_csv')

# %% code 260.
df = DAOfound.to_pandas()
print(type(df))
df

# %% code 261.
# 영상 표시 함수 znorm · zimshow · norm_imshow 는 Ⅲ-04 「FITS 파일 다루기」에서 설명했고 dses_utils 에 들어 있음

# %% code 262.
import numpy as np
pos = np.transpose((DAOfound['x_centroid'], DAOfound['y_centroid']))

print("type(pos) :", type(pos))
print("pos.shape :", pos.shape)
print("pos :", pos)

# %% code 263.
from astropy.wcs import WCS

wcs = WCS(hdul[0].header)
print("wcs :", wcs)

wcs.pixel_n_dim

# %% code 264.
from photutils.aperture import CircularAperture as CAp
from photutils.aperture import CircularAnnulus as CAn
apert = CAp(pos, r=R_AP)
#구경(aperture)
annul = CAn(positions=pos, r_in=R_IN, r_out=R_OUT)
#고리(annulus)

# %% code 265.
import matplotlib.pyplot as plt

fig, axs = plt.subplots(1, 1, figsize=(7.5, 5),
                        subplot_kw={'projection': wcs},
                        sharex=False, sharey=False, gridspec_kw=None)

im = du.zimshow(axs, hdul[0].data, )
axs.set_title('World coordinate system', fontsize=9)
axs.coords.grid(True, color='white', ls=':')
axs.coords['ra'].set_axislabel('Right Ascension (J2000)', minpad=0.5,
                               fontsize=9)
axs.coords['ra'].set_ticklabel_position('bl')
axs.coords['dec'].set_axislabel('Declination (J2000)', minpad=0.4, fontsize=9)
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

annul.plot(ax=axs, color="r")
for i in range(0, len(pos), 50):   # 별이 많아 번호는 50번마다 붙임
    axs.text(pos[i][0], pos[i][1], f"Star #{i}", fontsize=7, color='w')

cbar = plt.colorbar(im, ax = axs, fraction=0.035, pad=0.04, )
cbar.ax.tick_params(labelsize=8)

plt.suptitle(f"fname: {fpath.name}\n Result of DAOStarFinder", fontsize=10,)

axs.annotate(f'FWHM: {FWHM}', fontsize=8,
    xy=(0, 0), xytext=(-10, -30), va='top', ha='left',
    xycoords='axes fraction', textcoords='offset points')

axs.annotate(f'Sky threshold: {thresh:.02f}', fontsize=8,
    xy=(0, 0), xytext=(-10, -40), va='top', ha='left',
    xycoords='axes fraction', textcoords='offset points')

axs.annotate(f'Number of star(s): {len(DAOfound)}', fontsize=8,
    xy=(0, 0), xytext=(-10, -50), va='top', ha='left',
    xycoords='axes fraction', textcoords='offset points')

plt.tight_layout()
plt.savefig(f"{proj_dir}/{fpath.stem}_starfinder.png")

plt.show()
#plt.close()

# %% code 266.
idx = 7
mask_apert = (apert.to_mask(method='center'))[idx]
star_apply  = mask_apert.multiply(hdul[0].data)
starimg = mask_apert.cutout(hdul[0].data)

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.2),
                        sharex=False, sharey=False, gridspec_kw=None)

im0 = du.zimshow(axs[0], starimg,)

im1 = du.zimshow(axs[1], starimg)
im1 = du.zimshow(axs[1], star_apply, alpha=0.5)

ap = CAp(positions = (int(starimg.shape[0]/2),int(starimg.shape[1]/2)),
                r=R_AP)
ap.plot(ax=axs[0], color='r', lw=1, alpha=0.5)
ap.plot(ax=axs[1], color='r', lw=1, alpha=0.5)

axs[0].set_title('Star area',)
axs[1].set_title('Mask Applied',)

plt.colorbar(im0, ax=axs[0], fraction=0.0455, pad=0.04, )
plt.colorbar(im1, ax=axs[1], fraction=0.0455, pad=0.04, )

plt.tight_layout()
plt.show()

# %% code 267.
print("starimg :", starimg)
print("star_apply :", star_apply)

# %% code 268.
import matplotlib.pyplot as plt
from astropy.nddata import Cutout2D

def plot_cutouts(apert, data, indices, cols, figsize=(6.4, 6.6)):
    """
    지정된 인덱스에 해당하는 마스크를 적용한 cutout 이미지를 여러 개 그리는 함수

    Args:
        apert: 구경 객체(CircularAperture)
        data: 원본 이미지 데이터 (Astropy ImageHDU 또는 ndarray)
        indices: 그릴 cutout의 인덱스 리스트
        cols: 열 수
        figsize: 그래프 크기 (default: (6.4, 6.6))
    """

    ncols = min(len(indices), cols)      # 최대 cols열
    nrows = -(-len(indices) // ncols)    # 필요한 행 수(올림)

    fig, axs = plt.subplots(nrows, ncols, figsize=figsize, squeeze=False)
    axs = axs.flatten()  # 1차원 배열로 변환
    for ax in axs[len(indices):]:        # 남는 칸은 지움
        ax.axis('off')

    for i, idx in enumerate(indices):
        mask_apert = (apert.to_mask(method='center'))[idx]
        star_apply  = mask_apert.multiply(data)
        starimg = mask_apert.cutout(data)

        ap = CAp(positions = (int(starimg.shape[0]/2),int(starimg.shape[1]/2)),
                r=R_AP)

        im0 = du.zimshow(axs[i], starimg, )
        im1 = du.zimshow(axs[i], star_apply, alpha=0.5)

        ap.plot(ax = axs[i], color='r', lw=1, alpha=0.5)

        axs[i].set_title(f"Cutout star #{idx}", fontsize=9)
        axs[i].set_xlabel('X')
        axs[i].set_ylabel('Y')

    # 여백 조절
    plt.tight_layout()
    plt.show()

# 사용 예시
plot_cutouts(apert, hdul[0].data, range(0, 16), 4,  figsize=(6.4, 6.6))

# %% code 269.
from photutils.aperture import aperture_photometry as apphot
apphot_result = apphot(hdul[0].data, apert, method='exact')
print(type(apphot_result))
apphot_result
df_apphot = apphot_result.to_pandas()
df_apphot

# %% code 270.
ap_area   = apert.area
ap_area

# %% code 271.
idx = 7
mask_annul = (annul.to_mask(method='center'))[idx]
sky_apply  = mask_annul.multiply(hdul[0].data)
skyimg = mask_annul.cutout(hdul[0].data)

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.2),
                        sharex=False, sharey=False, gridspec_kw=None)

im0 = du.zimshow(axs[0], skyimg,)

im1 = du.zimshow(axs[1], skyimg, )
im1 = du.zimshow(axs[1], sky_apply, alpha=0.5)
ap = CAp(positions = (int(skyimg.shape[0]/2),int(skyimg.shape[1]/2)), r=R_AP)
an = CAn(positions = (int(skyimg.shape[0]/2),int(skyimg.shape[1]/2)),
        r_in=R_IN, r_out=R_OUT)

im0 = du.zimshow(axs[0], skyimg, )
im1 = du.zimshow(axs[1], sky_apply, alpha=0.5)

ap.plot(ax = axs[0], color='r', lw=1, alpha=0.5)
an.plot(ax = axs[0], color='y', lw=1, alpha=0.7)
ap.plot(ax = axs[1], color='r', lw=1, alpha=0.5)
an.plot(ax = axs[1], color='y', lw=1, alpha=0.7)

axs[0].set_title('Sky area',)
axs[1].set_title('Mask Applied',)

plt.colorbar(im0, ax=axs[0], fraction=0.0455, pad=0.04, )
plt.colorbar(im1, ax=axs[1], fraction=0.0455, pad=0.04, )

plt.tight_layout()
plt.show()

# %% code 272.
print("skyimg :", skyimg)
print("sky_apply :", sky_apply)

# %% code 273.
import matplotlib.pyplot as plt
from astropy.nddata import Cutout2D

def plot_cutouts(apert, data, indices, cols, figsize=(6.4, 6.6)):
    """
    지정된 인덱스에 해당하는 마스크를 적용한 cutout 이미지를 여러 개 그리는 함수

    Args:
        apert: 고리 객체(CircularAnnulus)
        data: 원본 이미지 데이터 (Astropy ImageHDU 또는 ndarray)
        indices: 그릴 cutout의 인덱스 리스트
        cols: 열 수
        figsize: 그래프 크기 (default: (6.4, 6.6))
    """

    ncols = min(len(indices), cols)    # 최대 cols열
    nrows = -(-len(indices) // ncols)  # 필요한 행 수(올림)

    fig, axs = plt.subplots(nrows, ncols, figsize=figsize, squeeze=False)
    axs = axs.flatten()            # 1차원 배열로 변환
    for ax in axs[len(indices):]:  # 남는 칸은 지움
        ax.axis('off')

    for i, idx in enumerate(indices):
        mask_annul = (apert.to_mask(method='center'))[idx]
        sky_apply  = mask_annul.multiply(data)
        skyimg = mask_annul.cutout(data)

        im0 = du.zimshow(axs[i], skyimg, )
        im1 = du.zimshow(axs[i], sky_apply, alpha=0.5)

        ap = CAp(positions = (int(skyimg.shape[0]/2),int(skyimg.shape[1]/2)),
                r=R_AP)
        an = CAn(positions = (int(skyimg.shape[0]/2),int(skyimg.shape[1]/2)),
                r_in=R_IN, r_out=R_OUT)

        ap.plot(ax = axs[i], color='r', lw=1, alpha=0.5)
        an.plot(ax = axs[i], color='y', lw=1, alpha=0.7)

        axs[i].set_title(f"Cutout star #{idx}", fontsize=9)
        axs[i].set_xlabel('X')
        axs[i].set_ylabel('Y')

    # 여백 조절
    plt.tight_layout()
    plt.show()

# 사용 예시 (mask_annul, hdul[0].data, 그리고 그릴 인덱스를 지정)
plot_cutouts(annul, hdul[0].data, range(0, 16), 4,  figsize=(6.4, 6.6))

# %% code 274.
import numpy as np
from astropy.stats import sigma_clip

# %% code 275.
def sky_fit(all_sky, method='mode', sky_nsigma=3, sky_iter=5, \
            mode_option='sex', med_factor=2.5, mean_factor=1.5):
    '''
    Estimate sky from given sky values.
    Parameters
    ----------
    all_sky : ~numpy.ndarray
        The sky values as numpy ndarray format. It MUST be 1-d for proper use.
    method : {"mean", "median", "mode"}, optional
        The method to estimate sky value. You can give options to "mode"
        case; see mode_option.
        "mode" is analogous to Mode Estimator Background of photutils.
    sky_nsigma : float, optional
        The input parameter for sky sigma clipping.
    sky_iter : float, optional
        The input parameter for sky sigma clipping.
    mode_option : {"sex", "IRAF", "MMM"}, optional.
        sex  == (med_factor, mean_factor) = (2.5, 1.5)
        IRAF == (med_factor, mean_factor) = (3, 2)
        MMM  == (med_factor, mean_factor) = (3, 2)
    Returns
    -------
    sky : float
        The estimated sky value within the all_sky data, after sigma clipping.
    std : float
        The sample standard deviation of sky value within the all_sky data,
        after sigma clipping.
    nsky : int
        The number of pixels which were used for sky estimation after the
        sigma clipping.
    nrej : int
        The number of pixels which are rejected after sigma clipping.
    -------
    '''
    sky = all_sky.copy()
    if method == 'mean':
        return np.mean(sky), np.std(sky, ddof=1)

    elif method == 'median':
        return np.median(sky), np.std(sky, ddof=1)

    elif method == 'mode':
        sky_clip   = sigma_clip(sky, sigma=sky_nsigma,
                                maxiters=sky_iter, #iters=sky_iter,
                                )
        sky_clipped= sky[np.invert(sky_clip.mask)]
        nsky       = np.count_nonzero(sky_clipped)
        mean       = np.mean(sky_clipped)
        med        = np.median(sky_clipped)
        std        = np.std(sky_clipped, ddof=1)
        nrej       = len(all_sky) - len(sky_clipped)

        if nrej < 0:
            raise ValueError('nrej < 0: check the code')

        if nrej > nsky: # 버린 값 > 남은 값
            raise Warning('More than half of the pixels rejected.')

        if mode_option == 'IRAF':
            if (mean < med):
                sky = mean
            else:
                sky = 3 * med - 2 * mean

        elif mode_option == 'MMM':
            sky = 3 * med - 2 * mean

        elif mode_option == 'sex':
            if (mean - med) / std > 0.3:
                sky = med
            else:
                sky = (2.5 * med) - (1.5 * mean)
        else:
            raise ValueError('mode_option not understood')

        return sky, std, nsky, nrej

# %% code 276.
idx = 1
mask_annul = (annul.to_mask(method='center'))[idx]
annul_weighted = mask_annul.multiply(hdul[0].data)
sky_non0   = np.nonzero(annul_weighted)
sky_pixel  = annul_weighted[sky_non0]

msky, sky_std, nsky, nrej = sky_fit(sky_pixel, method='mode',
                                        mode_option='sex')

print("msky, sky_std, nsky, nrej :", msky, sky_std, nsky, nrej)

# %% code 277.
import numpy as np

# 플럭스로 기기 등급과 그 오차를 계산해 돌려줌
def mag_inst(flux, ferr):
    if flux <= 0:
        # 잘못된 플럭스 값 처리(NaN 반환)
        m_inst = np.nan
        merr = np.nan
    else:
        m_inst = -2.5 * np.log10(flux)
        merr = 2.5 / np.log(10) * ferr / flux
    return m_inst, merr

# %% code 278.
print(2.5 / np.log(10) * 0.01)  # 플럭스 오차 1% 에 해당하는 등급 오차

# %% code 279.
# 모든 별의 구경 · 고리 마스크를 한 번에 만들어 둠
mask_apert = (apert.to_mask(method='center'))
mask_annul = (annul.to_mask(method='center'))

mag_ann  = np.zeros(len(apphot_result))
merr_ann = np.zeros(len(apphot_result))

fig, ax = plt.subplots(figsize=(8, 4.2))

for i in range(len(apphot_result)):
    annul_weighted = mask_annul[i].multiply(hdul[0].data)
    sky_non0   = np.nonzero(annul_weighted)
    sky_pixel  = annul_weighted[sky_non0]
    msky, sky_std, nsky, nrej = sky_fit(sky_pixel, method='mode',
                                        mode_option='sex')

    flux_star = apphot_result['aperture_sum'][i] - msky * ap_area  # 전체 - 하늘 배경

    # 플럭스 오차(ADU): 분산을 모두 ADU^2 단위로 맞춤
    flux_err  = np.sqrt(apphot_result['aperture_sum'][i] / gain    # 포아송 잡음(별 + 하늘)
                        + ap_area * (rdnoise / gain)**2            # 읽기 잡음
                        + (ap_area * sky_std)**2 / nsky )          # 하늘값 어림 오차

    mag_ann[i], merr_ann[i] = mag_inst(flux_star, flux_err)
 # print(i, msky, sky_std, nsky, nrej)
 # print(i, mag_ann[idx], merr_ann[idx])
    try:
        ax.errorbar(i, mag_ann[i], yerr=merr_ann[i],
                    marker='x',
 #ms=10,
                    capsize=3)
    except:
        continue

ax.invert_yaxis()
#ax.set_ylim(ymin=-13, ymax=-10)
plt.xlabel('Star ID')
plt.ylabel('Instrumental mag')
plt.grid(ls=':')
plt.show()

# %% code 280.
for i, row in df_apphot.iterrows():
    annul_weighted = mask_annul[i].multiply(hdul[0].data)
    sky_non0   = np.nonzero(annul_weighted)
    sky_pixel  = annul_weighted[sky_non0]
    msky, sky_std, nsky, nrej = sky_fit(sky_pixel, method='mode',
                                        mode_option='sex')

    flux_star = apphot_result['aperture_sum'][i] - msky * ap_area  # 전체 - 하늘 배경

    # 플럭스 오차(ADU): 분산을 모두 ADU^2 단위로 맞춤
    flux_err  = np.sqrt(apphot_result['aperture_sum'][i] / gain    # 포아송 잡음(별 + 하늘)
                        + ap_area * (rdnoise / gain)**2            # 읽기 잡음
                        + (ap_area * sky_std)**2 / nsky )          # 하늘값 어림 오차

    mag_ann, merr_ann = mag_inst(flux_star, flux_err)
    df_apphot.loc[i, 'msky'] = msky
    df_apphot.loc[i, 'sky_std'] = sky_std
    df_apphot.loc[i, 'nsky'] = nsky
    df_apphot.loc[i, 'nrej'] = nrej
    df_apphot.loc[i, 'flux_star'] = flux_star
    df_apphot.loc[i, 'flux_err'] = flux_err
    df_apphot.loc[i, 'mag_inst'] = mag_ann
    df_apphot.loc[i, 'merr_inst'] = merr_ann

df_apphot.to_csv(f"{str(proj_dir)}/{fpath.stem}_m_inst.csv")
print(f"{str(proj_dir)}/{fpath.stem}_m_inst.csv")

df_apphot

# %% code 281.
from photutils.aperture import aperture_photometry

def apphot_annulus(data, aperture, annulus, gain=1.0, rdnoise=0.0, method="exact"):
    """구경 측광 + 고리의 하늘값 빼기 + ADU 단위 오차를 판다스 표로 돌려줌."""
    # 1. 화소별 오차 지도(ADU)
    error = np.sqrt(np.clip(data, 0, None) / gain + (rdnoise / gain)**2)
    # 2. 구경 안 픽셀값의 합과 그 오차
    phot = aperture_photometry(data, aperture, error=error, method=method).to_pandas()
    # 3. 고리 안 픽셀로 하늘값 어림(sky_fit: 3σ 클리핑 뒤 최빈값)
    masks = annulus.to_mask(method="center")
    if not isinstance(masks, list):          # 위치가 하나뿐일 때
        masks = [masks]
    for i, mask in enumerate(masks):
        msky, ssky, nsky, nrej = sky_fit(mask.get_values(data))
        phot.loc[i, ["msky", "ssky", "nsky", "nrej"]] = msky, ssky, nsky, nrej
    # 4. 하늘을 뺀 별빛과 그 오차(하늘값 어림 오차를 더함)
    phot["aparea"] = aperture.area
    phot["source_sum"] = phot["aperture_sum"] - aperture.area * phot["msky"]
    phot["source_sum_err"] = np.sqrt(phot["aperture_sum_err"]**2
                                     + (aperture.area * phot["ssky"])**2 / phot["nsky"])
    # 5. 기기 등급과 오차, 신호 대 잡음비(du.mag_inst 는 배열도 받음)
    phot["mag"], phot["merr"] = du.mag_inst(phot["source_sum"], phot["source_sum_err"])
    phot["snr"] = (phot["source_sum"] / phot["source_sum_err"]).clip(lower=0)
    return phot

phot_all = apphot_annulus(hdul[0].data, apert, annul, gain=gain, rdnoise=rdnoise)
d_mag = np.abs(phot_all["mag"] - df_apphot["mag_inst"])
d_err = np.abs(phot_all["merr"] - df_apphot["merr_inst"])
print(f"별 {len(phot_all)}개: 반복문과의 차이 — 등급 최대 {np.nanmax(d_mag):.1e}, 등급 오차 최대 {np.nanmax(d_err):.1e}")
phot_all[["id", "msky", "source_sum", "source_sum_err", "mag", "merr", "snr"]].head()

# %% code 282.
from photutils.aperture import aperture_photometry as apphot

# 가장자리에서 떨어지고 주변이 깨끗한, 밝기가 중간쯤인 별 3개
ny, nx = hdul[0].data.shape
ok = ((df_apphot["x_center"] > R_OUT) & (df_apphot["x_center"] < nx - R_OUT)
      & (df_apphot["y_center"] > R_OUT) & (df_apphot["y_center"] < ny - R_OUT)
      & (df_apphot["nrej"] <= 5)
      & (df_apphot["flux_star"] > 5e4) & (df_apphot["flux_star"] < 5e5))
sel = df_apphot[ok].sort_values("flux_star", ascending=False).index[:3]

radii = np.arange(2, 21, 1.0)   # 구경 반지름(픽셀)
fig, ax = plt.subplots(figsize=(8, 4.2))
for idx in sel:
    x0, y0 = pos[idx]
    sky_pixel = CAn((x0, y0), r_in=R_IN, r_out=R_OUT).to_mask(
        method='center').get_values(hdul[0].data)
    msky, sky_std, nsky, nrej = sky_fit(sky_pixel, method='mode',
                                        mode_option='sex')
    snr = []
    for r in radii:
        ap = CAp((x0, y0), r=r)
        tot = apphot(hdul[0].data, ap, method='exact')['aperture_sum'][0]
        flux = tot - msky * ap.area
        err = np.sqrt(tot / gain + ap.area * (rdnoise / gain)**2
                      + (ap.area * sky_std)**2 / nsky)
        snr.append(flux / err)
    snr = np.array(snr)
    r_best = radii[snr.argmax()]
    print(f"Star #{idx}: 최대 SNR {snr.max():.0f} (r = {r_best:.0f} px = "
          f"{r_best / FWHM_INIT:.2f} FWHM), r = R_AP 에서 SNR/최대 = "
          f"{snr[radii == R_AP][0] / snr.max():.3f}")
    ax.plot(radii / FWHM_INIT, snr / snr.max(), marker='.',
            label=f"Star #{idx}")

ax.axvline(R_AP / FWHM_INIT, color='k', ls=':', label='R_AP = 1.5 FWHM')
ax.set(xlabel='구경 반지름 (FWHM 단위, FWHM = 6 px)', ylabel='SNR / 최대 SNR')
ax.grid(ls=':')
ax.legend(fontsize=9)
plt.show()
