# 지구과학 데이터 사이언스 2 | III-04. FITS 파일 다루기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 90.
# 파일 ID와 저장 경로를 리스트로 정의
files = [
    ('1YZqev797sh5SyJIXzdwQBJ34-9w91Rsm', 'm42-001L.fit'),
    ("1qJQdbmdeHg23sPdLKRGfPq93Sfo1HT_3",
     "46P-WIRTANEN_LIGHT_R_2018-12-13-17-46-15_"
     "60sec_FSQ106ED-x73_QSI683ws_-30c_2bin.fit"),
    ("1mCX_QfgbyskObkF9I_IDRk2oYWHOQjxs",
     "IC434_Light_H_2019-10-08-09-38-54_"
     "900sec_GSON300_QSI683ws_-15C_1bin.fit"),
    ("1h15EMnhYb02KNhLkuqyUdR00fZV4xf3C",
     "M13_Light_L_2021-06-04-13-10-16_090sec_"
     "TEC140x75_STL-11000M_-19C_1bin.fit"),
    ("1NhaUjTvlXLFLIAmHXZyD7jt5IcLbMySU",
     "241GERMANIA_LIGHT_R_2023-11-07-18-38-15_"
     "150sec_GSON300_STF-8300M_-19c_1bin.fit")
]

# for 루프를 사용하여 파일 다운로드
for file_id, output_path in files:
    du.download(f"https://docs.google.com/uc?export=download&id={file_id}",
                proj_dir / output_path)

# %% code 91.
fpaths = du.list_files(proj_dir, "fit*")
print(f"fpaths[0]: {fpaths[0]}")

# %% code 92.
from pathlib import Path
from astropy.io import fits

fpath = Path(fpaths[4])
print("fpath", (fpath))

hdul = fits.open(fpath)

print("type(hdul) :", type(hdul))
print("hdul :", hdul)
print("len(hdul) :", len(hdul))
print("type(hdul[0]) :", type(hdul[0]))

# %% code 93.
print("type(hdul[0].header) :", type(hdul[0].header))
print("hdul[0].header :", f"헤더 카드 {len(hdul[0].header)}개")

print("hdul[0].header['DATE-OBS'] :", hdul[0].header['DATE-OBS'])
print("type(hdul[0].header['DATE-OBS']) :", type(hdul[0].header['DATE-OBS']))

import astropy.units as u
print("type(hdul[0].header['OBJCTDEC'])", type(hdul[0].header['OBJCTDEC']))
print("hdul[0].header['OBJCTDEC']", hdul[0].header['OBJCTDEC'])

print("type(hdul[0].data) :", type(hdul[0].data))
print("hdul[0].data.dtype :", hdul[0].data.dtype)
print("hdul[0].data.shape :", hdul[0].data.shape)
print("hdul[0].data :", hdul[0].data)

# %% code 94.
import numpy as np
import matplotlib.pyplot as plt

# 1행 2열 subplot 생성
fig, axes = plt.subplots(1, 2, figsize=(7.5, 3))

# 첫 번째 subplot - 기본 컬러맵
im1 = axes[0].imshow(hdul[0].data, origin='lower')
axes[0].set_title('Default colormap')
fig.colorbar(im1, ax=axes[0], fraction=0.035, pad=0.04)

# 두 번째 subplot - 그레이스케일 + 가우시안 보간
im2 = axes[1].imshow(hdul[0].data, cmap='gray', interpolation='gaussian',
                     origin='lower')
axes[1].set_title('Gray colormap with Gaussian interpolation')
fig.colorbar(im2, ax=axes[1], fraction=0.035, pad=0.04)

plt.tight_layout()
plt.show()

# %% code 95.
from astropy.visualization import (MinMaxInterval, SqrtStretch, LogStretch,
                                   ImageNormalize)

# ImageNormalize 객체 만들기
norm_sqrt = ImageNormalize(hdul[0].data, interval=MinMaxInterval(),
                          stretch=SqrtStretch())

norm_log = ImageNormalize(hdul[0].data, interval=MinMaxInterval(),
                         stretch=LogStretch())

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.8),
                       sharex=False, sharey=False, gridspec_kw=None)

# 제곱근 정규화
im0 = axs[0].imshow(hdul[0].data,
                   origin='lower',
                   norm=norm_sqrt,
                   )
axs[0].set_title('Square Root Normalization', fontsize=10)

# 로그 정규화
im1 = axs[1].imshow(hdul[0].data,
                   origin='lower',
                   norm=norm_log,
                   )
axs[1].set_title('Log Normalization', fontsize=10)

# 컬러바 추가
fig.colorbar(im0, ax=axs[0], fraction=0.035, pad=0.04)
fig.colorbar(im1, ax=axs[1], fraction=0.035, pad=0.04)

plt.tight_layout()
plt.show()

# %% code 96.
from warnings import warn
from astropy.visualization import (
    ImageNormalize,
    LinearStretch,
    ZScaleInterval,
    simple_norm,
)

# %% code 97.
def znorm(image, stretch=LinearStretch(), **kwargs):
    """
    이미지에 ZScale 간격과 스트레칭을 적용한 정규화 객체를 생성합니다.
    
    Parameters:
    -----------
    image : array-like
        정규화할 이미지 데이터
    stretch : astropy stretch object
        적용할 스트레칭 함수 (기본값: LinearStretch)
    **kwargs : dict
        ZScaleInterval에 전달할 추가 키워드 인수
    
    Returns:
    --------
    ImageNormalize object
        정규화된 이미지 객체
    """
    return ImageNormalize(image, interval=ZScaleInterval(**kwargs),
                          stretch=stretch)

# %% code 98.
def zimshow(
    ax,
    image,
    stretch=LinearStretch(),
    cmap=None,
    origin="lower",
    zscale_kw={},
    **kwargs
    ):
    """
    ZScale 정규화를 사용하여 이미지를 표시하는 함수입니다.
    
    Parameters:
    -----------
    ax : matplotlib axes
        이미지를 그릴 matplotlib axes 객체
    image : array-like
        표시할 이미지 데이터
    stretch : astropy stretch object
        적용할 스트레칭 함수 (기본값: LinearStretch)
    cmap : str or colormap
        사용할 컬러맵
    origin : str
        이미지 원점 위치 (기본값: "lower")
    zscale_kw : dict
        ZScale에 전달할 키워드 인수
    **kwargs : dict
        imshow에 전달할 추가 키워드 인수
    
    Returns:
    --------
    AxesImage
        matplotlib imshow 객체
    """
    im = ax.imshow(
        image,
        norm=znorm(image, stretch=stretch, **zscale_kw),
        origin=origin,
        cmap=cmap,
        **kwargs
    )
    return im

# %% code 99.
def norm_imshow(
    ax,
    data,
    origin="lower",
    stretch="linear",
    power=1.0,
    asinh_a=0.1,
    min_cut=None,
    max_cut=None,
    min_percent=None,
    max_percent=None,
    percent=None,
    clip=True,
    log_a=1000,
    invalid=-1.0,
    zscale=False,
    vmin=None,
    vmax=None,
    **kwargs
):
    """
    다양한 정규화 옵션을 사용하여 이미지를 표시하는 함수입니다.
    
    Parameters:
    -----------
    ax : matplotlib axes
        이미지를 그릴 matplotlib axes 객체
    data : array-like
        표시할 이미지 데이터
    origin : str
        이미지 원점 위치 (기본값: "lower")
    stretch : str
        스트레칭 방법 ("linear", "log", "sqrt", "asinh", "power" 등)
    power : float
        power 스트레칭에 사용할 지수 (기본값: 1.0)
    asinh_a : float
        asinh 스트레칭에 사용할 매개변수 (기본값: 0.1)
    min_cut, max_cut : float
        픽셀 값의 최소/최대 절단값
    min_percent, max_percent : float
        백분위수 기반 최소/최대 절단값
    percent : float
        대칭적 백분위수 절단값
    clip : bool
        범위를 벗어난 값을 클리핑할지 여부 (기본값: True)
    log_a : float
        로그 스트레칭에 사용할 매개변수 (기본값: 1000)
    invalid : float
        유효하지 않은 픽셀에 사용할 값 (기본값: -1.0)
    zscale : bool
        ZScale 정규화 사용 여부 (기본값: False)
    vmin, vmax : float
        수동으로 설정할 최소/최대 표시값
    **kwargs : dict
        imshow에 전달할 추가 키워드 인수
    
    Returns:
    --------
    AxesImage
        matplotlib imshow 객체
    """
 # vmin이 설정되었는데 min_cut도 설정된 경우 경고
    if vmin is not None and min_cut is not None:
        warn("vmin will override min_cut.")

 # vmax가 설정되었는데 max_cut도 설정된 경우 경고
    if vmax is not None and max_cut is not None:
        warn("vmax will override max_cut.")

 # ZScale 정규화를 사용하는 경우
    if zscale:
        zs = ImageNormalize(data, interval=ZScaleInterval())
        min_cut = vmin = zs.vmin  # ZScale의 최솟값 사용
        max_cut = vmax = zs.vmax  # ZScale의 최댓값 사용

 # vmin 또는 vmax가 명시적으로 설정된 경우
    if vmin is not None or vmax is not None:
        im = ax.imshow(data, origin=origin, vmin=vmin, vmax=vmax, **kwargs)
    else:
 # simple_norm을 사용한 정규화 적용
        im = ax.imshow(
            data,
            origin=origin,
            norm=simple_norm(
                data=data,
                stretch=stretch,          # 스트레칭 방법
                power=power,              # power 스트레칭 지수
                asinh_a=asinh_a,          # asinh 스트레칭 매개변수
                min_cut=min_cut,          # 최소 절단값
                max_cut=max_cut,          # 최대 절단값
                min_percent=min_percent,  # 최소 백분위수
                max_percent=max_percent,  # 최대 백분위수
                percent=percent,          # 대칭 백분위수
                clip=clip,                # 클리핑 여부
                log_a=log_a,              # 로그 스트레칭 매개변수
                invalid=invalid           # 유효하지 않은 값 처리
            ),
            **kwargs)
    return im

# %% code 100.
fig, axs = plt.subplots(1, 2, figsize=(7.5, 2.5),
                       sharex=False, sharey=False, gridspec_kw=None)


# ImageNormalize 객체 만들기
norm = ImageNormalize(hdul[0].data, interval=MinMaxInterval(),
                      stretch=SqrtStretch())

im0 = axs[0].imshow(hdul[0].data,
                origin='lower',
                norm=norm,
                )

axs[0].set_title('Normalization', fontsize=9)


im1 = zimshow(axs[1], hdul[0].data,
                origin='lower',
                )

axs[1].set_title(f'Zimshow', fontsize=9)

fig.colorbar(im0, ax = axs[0], fraction=0.035, pad=0.04)
fig.colorbar(im1, ax = axs[1], fraction=0.035, pad=0.04)

plt.tight_layout()

# %% code 101.
print("fpaths[2]", (fpaths[2]))
hdul2 = fits.open(str(fpaths[2]))

fig, axs = plt.subplots(1, 2, figsize=(7.5, 2.5),
                       sharex=False, sharey=False, gridspec_kw=None)

im0 = zimshow(axs[0], hdul2[0].data,
                origin='lower',
                cmap='coolwarm',
                )
axs[0].set_title('coolwarm colormap', fontsize=8)

im1 = zimshow(axs[1], hdul2[0].data,
                origin='lower',
                cmap='gray',
                )
axs[1].set_title('gray colormap', fontsize=8)

fig.suptitle(f'{str(fpaths[2])}', fontsize=8)
fig.colorbar(im0, ax = axs[0], fraction=0.031, pad=0.04)
fig.colorbar(im1, ax = axs[1], fraction=0.031, pad=0.04)
plt.tight_layout()

# %% code 102.
import numpy as np
import matplotlib.pyplot as plt
from astropy.nddata import Cutout2D
import textwrap

hdul =  fits.open(str(fpaths[0]), unit="adu")

fig_set = plt.figure(figsize=(7.5, 3.8))

ax0 = plt.subplot2grid((2,4), (0,0),
                    colspan=2, rowspan=2,
                    fig=fig_set)
im0 = zimshow(ax0, hdul[0].data,
            origin='lower',
            )
plt.colorbar(im0,
             ax = ax0,
             fraction=0.0345, pad=0.04)
ax0.set_title(textwrap.fill(fpaths[0].name, 40), fontsize=9)   # 긴 파일 이름은 두 줄로

cutsizes = 101

# 1/4 영역
ax20 = plt.subplot2grid((2,4), (0,2),
                       fig=fig_set)
cut_hdu = Cutout2D(
            data = hdul[0].data,
            position = (500, 500),
            size=(cutsizes, cutsizes)  # CCD 영역 잘라 내기
            )
im20 = zimshow(ax20, cut_hdu.data,
    origin='lower'
    )
ax20.set_ylabel('pixels')
ax20.grid(ls=':')
ax20.set_title(f'1/4 image area', fontsize=9)
plt.colorbar(im20,
            ax=ax20,
            fraction=0.0455, pad=0.04)

# 2/4 영역
ax21 = plt.subplot2grid((2,4), (0,3),
                       fig=fig_set)
cut_hdu = Cutout2D(
            data = hdul[0].data,
            position = (hdul[0].data.shape[1] - 500, 500),
            size=(cutsizes, cutsizes)  # CCD 영역 잘라 내기
            )
im21 = zimshow(ax21 ,cut_hdu.data,
    origin='lower'
    )
ax21.set_ylabel('pixels')
ax21.grid(ls=':')
ax21.set_title(f'2/4 image area', fontsize=9)
plt.colorbar(im21,
            ax=ax21,
            fraction=0.0455, pad=0.04)

# 3/4 영역
ax30 = plt.subplot2grid((2,4), (1,2),
                       fig=fig_set)
cut_hdu = Cutout2D(
            data = hdul[0].data,
            position = (500, hdul[0].data.shape[0] - 500),
            size=(cutsizes, cutsizes)  # CCD 영역 잘라 내기
            )
im30 = zimshow(ax30, cut_hdu.data,
    origin='lower'
    )
ax30.set_ylabel('pixels')
ax30.grid(ls=':')
ax30.set_title(f'3/4 image area', fontsize=9)
plt.colorbar(im30,
            ax=ax30,
            fraction=0.0455, pad=0.04)

# 4/4 영역
ax31 = plt.subplot2grid((2,4), (1,3),
                       fig=fig_set)
cut_hdu = Cutout2D(
            data = hdul[0].data,
            position = (hdul[0].data.shape[1] - 500,
                        hdul[0].data.shape[0] - 500),
            size=(cutsizes, cutsizes)  # CCD 영역 잘라 내기
            )
im31 = zimshow(ax31, cut_hdu.data,
    origin='lower'
    )
ax31.set_ylabel('pixels')
ax31.grid(ls=':')
ax31.set_title(f'4/4 image area', fontsize=9)
plt.colorbar(im31,
            ax=ax31,
            fraction=0.0455, pad=0.04)

plt.tight_layout()
plt.show()

# %% code 103.
import matplotlib.patches as patches
from astropy.nddata import Cutout2D
import textwrap

def plot_image_with_cutouts(fpath, location, cutsizes=101):
    hdul = fits.open(str(fpath), unit="adu")
    data = hdul[0].data

    fig_set = plt.figure(figsize=(7.5, 3.8))

    def add_subplot(position, data, title):
        ax = plt.subplot2grid((2,4), position, fig=fig_set)
        im = zimshow(ax, data, origin='lower')
        ax.set_ylabel('pixels')
        ax.grid(ls=':')
        ax.set_title(title, fontsize=9)
        plt.colorbar(im, ax=ax, fraction=0.0455, pad=0.04)
        return im

    def add_rectangle(x, y, label):
        rect = patches.Rectangle((x-cutsizes/2, y-cutsizes/2), cutsizes,
                                cutsizes, linewidth=1,
                                edgecolor='r', facecolor='none')
        ax1.add_patch(rect)
        ax1.text(x, y, label)

 # 전체 이미지
    ax1 = plt.subplot2grid((2,4), (0,0), colspan=2, rowspan=2, fig=fig_set)
    im1 = zimshow(ax1, data, origin='lower')
    plt.colorbar(im1, ax=ax1, fraction=0.0345, pad=0.04)
    ax1.set_title(textwrap.fill(fpath.name, 40), fontsize=9)   # 긴 파일 이름은 두 줄로


 # 4개의 부분 이미지
    positions = [(0,2), (0,3), (1,2), (1,3)]
    corners = [(location, data.shape[0] - location),
                (data.shape[1] - location, data.shape[0] - location),
                (location, location),
                (data.shape[1] - location, location),
                ]

    for i, (pos, corner) in enumerate(zip(positions, corners), 1):
        cut_hdu = Cutout2D(data=data, position=corner,
                           size=(cutsizes, cutsizes))
        add_subplot(pos, cut_hdu.data, f'{i}/4 image area')
        add_rectangle(corner[0], corner[1], f"{i}/4")

    plt.tight_layout()
    plt.show()

# 함수 사용 예
# plot_image_with_cutouts('path_to_your_fits_file.fits', location)

# %% code 104.
# 함수 사용 예
plot_image_with_cutouts(fpaths[0], 500)

# %% code 105.
from astropy.modeling.functional_models import Moffat1D, Gaussian1D
from scipy.special import gamma as G
import numpy as np

def norm_gauss(sigma):
    return 1/np.sqrt(2 * np.pi * sigma**2)

def norm_moffat(width, power):
    return G(power) / (width * np.sqrt(np.pi) * G(power - 1/2))

def HWHM_moffat(width, power):
    return width * np.sqrt( 2**(1/power) - 1)

x       = np.arange(0,8,0.1)
sigma   = np.array([1, 2])
width   = np.array([2, 5])
power   = np.array([1.5, 2.5])


plt.figure(figsize=(7.5, 3.6))
ax1 = plt.subplot(1,2,1)
ax2 = plt.subplot(1,2,2)
for s in sigma:
    gauss  = Gaussian1D(amplitude=1, mean=0, stddev=s)
    ax1.plot(x, norm_gauss(s)*gauss(x), ls=":",
             label="sigma={0:.0f}, HWHM={1:.1f}".format(s, 2.355*s/2))
    ax2.plot(x, -2.5 * np.log10(norm_gauss(s)*gauss(x)), ls=":",
             label="sigma={0:.0f}, HWHM={1:.1f}".format(s, 2.355*s/2))

for w in width:
    for p in power:
        moffat = Moffat1D(amplitude=1, x_0=0, gamma=w, alpha=p)
        HWHM   = HWHM_moffat(w, p)
        ax1.plot(x, norm_moffat(w, p) * moffat(x), lw=2,
                 label='width={0:.0f}, power={1:.1f}, HWHM={2:.1f}'.format(w, p, HWHM))
        ax2.plot(x, -2.5*np.log10(norm_moffat(w, p) * moffat(x)), lw=2,
                 label='width={0:.0f}, power={1:.1f}, HWHM={2:.1f}'.format(w, p, HWHM))

ax1.grid(ls=":")
ax2.grid(ls=":")
ax2.set_ylim(1, 5)
ax2.invert_yaxis()
ax2.set_title('log scale = magnitude scale')
ax1.legend(*ax2.get_legend_handles_labels(), fontsize=8, loc='upper right')   # 범례는 왼쪽 그래프의 빈 곳에
plt.tight_layout()
plt.show()

# %% code 106.
# 함수 사용 예
plot_image_with_cutouts(fpaths[0], 700)

# %% code 107.
import matplotlib.pyplot as plt
hdul = fits.open(str(fpaths[0]), unit="adu")
data = hdul[0].data

row_index = 910  # 특정 행 인덱스
row_data = data[row_index, :]

plt.figure(figsize=(7.5, 1.9))  # 가로 길이를 길게 설정
plt.plot(row_data)
plt.xlabel('Pixel Number')
plt.ylabel('Pixel Value')
plt.title(f'Pixel Values of Row {row_index}')
plt.grid(True, which='both')  # 그리드 추가
plt.minorticks_on()           # 마이너 틱 추가
plt.show()

# %% code 108.
import matplotlib.pyplot as plt

def plot_row_pixels(fpath, row_index, col_center, width):
  """
  FITS 파일에서 특정 행의 픽셀 값을 추출하여 가로 너비를 지정하여 세로축으로 plot합니다.

  Args:
    fpath: FITS 파일 경로
    row_number: 추출할 행 번호
    width: 그래프 가로 길이
  """
  hdul = fits.open(str(fpath), unit="adu")
  data = hdul[0].data
  row_data = data[row_index, col_center-width:col_center+width]

  plt.figure(figsize=(8, 4.0))  # 가로 길이를 길게 설정
  plt.plot(row_data)
  plt.xlabel("Column Number")
  plt.ylabel("Pixel Value")
  plt.title(f"Pixel Values of Row {row_index}, center pixel {col_center}\n {fpath.name}",
            fontsize = 10)
  plt.grid(True)  # 그리드 추가

 # 마이너 틱과 레이블 추가
  plt.minorticks_on()
  plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')
  plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')

  plt.show()

# 예시 사용
row_number = 910  # 추출할 행 번호
col_center = 420  # 중심 픽셀 번호
width = 50        # 가로 픽셀 너비

plot_row_pixels(fpaths[0], row_number, col_center, width)

# %% code 109.
def plot_row_pixels_fwhm(fpath, row_number, conter, width):
    """
    FITS 파일에서 특정 행의 픽셀 값을 추출하여 가로 너비를 지정하여 세로축으로 plot합니다.

    Args:
    fpath: FITS 파일 경로
    row_number: 추출할 행 번호
    width: 그래프 가로 길이
    """
    hdul = fits.open(str(fpath), unit="adu")
    data = hdul[0].data
    row_data = data[row_number, conter-width:conter+width]

    plt.figure(figsize=(8, 4.0))  # 가로 길이를 길게 설정
    plt.plot(row_data)

 # FWHM 계산
    x = np.arange(len(row_data))
    y = row_data

 # 최댓값과 그 위치 찾기
    peak_value = np.max(y)
    peak_index = np.argmax(y)

 # 최댓값의 절반 계산
    half_max = peak_value  / 2.0

 # 최댓값의 절반에 가장 가까운 위치 찾기
    left_index = np.argmin(np.abs(y[:peak_index] - half_max))
    right_index = np.argmin(np.abs(y[peak_index:] - half_max)) + peak_index

 # FWHM 계산
    fwhm = x[right_index] - x[left_index]

 # FWHM 표시
    plt.axvline(x=left_index, color='r', linestyle='--',
                label=f'FWHM = {fwhm:.2f}')
    plt.axvline(x=right_index, color='r', linestyle='--')
    plt.axhline(y=half_max, linestyle='--',
                label=f'half maximum = {half_max:.0f}')
    plt.legend()
    plt.ylim(0, peak_value*1.1)
    plt.xlabel("Column Number")
    plt.ylabel("Pixel Value")
    plt.title(f"Pixel Values of Row {row_number}, center pixel {conter}\n {fpath.name}",
              fontsize = 10)
    plt.grid(True)  # 그리드 추가

 # 마이너 틱과 레이블 추가
    plt.minorticks_on()
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')

    plt.show()


plot_row_pixels_fwhm(fpaths[0], row_number, col_center, width)

# %% code 110.
import matplotlib.pyplot as plt

def plot_row_pixels_fwhm_from_background(fpath, row_number, conter, width):
    """
    FITS 파일에서 특정 행의 픽셀 값을 추출하여 가로 너비를 지정하여 세로축으로 plot합니다.

    Args:
    fpath: FITS 파일 경로
    row_number: 추출할 행 번호
    width: 그래프 가로 길이
    """
    hdul = fits.open(str(fpath), unit="adu")
    data = hdul[0].data
    row_data = data[row_number, conter-width:conter+width]

    plt.figure(figsize=(8, 4.0))  # 가로 길이를 길게 설정
    plt.plot(row_data)

 # FWHM 계산
    x = np.arange(len(row_data))
    y = row_data

 # 최댓값과 그 위치 찾기
    peak_value = np.max(y)
    peak_index = np.argmax(y)

 # 최댓값의 절반 계산
    half_max = ((peak_value - np.median(y)) / 2.0) + np.median(y)

 # 최댓값의 절반에 가장 가까운 위치 찾기
    left_index = np.argmin(np.abs(y[:peak_index] - half_max))
    right_index = np.argmin(np.abs(y[peak_index:] - half_max)) + peak_index

 # FWHM 계산
    fwhm = x[right_index] - x[left_index]

 # FWHM 표시
    plt.axvline(x=left_index, color='r', linestyle='--',
                label=f'FWHM = {fwhm:.2f}')
    plt.axvline(x=right_index, color='r', linestyle='--')
    plt.axhline(y=half_max, color='g', linestyle='--',
                label=f'half maximum from background value= {half_max:.0f}')
    plt.axhline(y=np.median(y), color='m', linestyle='--',
                label=f'background value = {np.median(y):.0f}')
    plt.legend()
    plt.ylim(0, peak_value*1.1)
    plt.xlabel("Column Number")
    plt.ylabel("Pixel Value")
    plt.title(f"Pixel Values of Row {row_number}, center pixel {conter}\n {fpath.name}",
              fontsize = 10)
    plt.grid(True)  # 그리드 추가

 # 마이너 틱과 레이블 추가
    plt.minorticks_on()
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')

    plt.show()


plot_row_pixels_fwhm_from_background(fpaths[0], row_number, col_center, width)

# %% code 111.
fpath = Path(fpaths[0])                     # 아래 그림 주석의 파일 이름
hdul =  fits.open(str(fpath), unit="adu")

FWHM = 5

# %% code 112.
from photutils.segmentation import detect_threshold
thresh_snr = detect_threshold(data=hdul[0].data, n_sigma=3)   # 배경 + 3σ (절대 화소값)
print('type(thresh_snr) :', type(thresh_snr))
print('thresh_snr.shape :', thresh_snr.shape)
print('detect_threshold', thresh_snr)
thresh_snr = thresh_snr[0][0]

# %% code 113.
from astropy.stats import sigma_clip, sigma_clipped_stats

avg, med, std = sigma_clipped_stats(hdul[0].data)  # 기본값은 3σ, 5회 반복
print("avg, med, std :", avg, med, std)
data_sub = hdul[0].data - med                       # 배경을 뺀 영상
thresh = 5.*std                                     # 배경 위 5σ
print("thresh (배경 위 5σ) :", thresh)
print("detect_threshold − 배경 (배경 위 3σ) :", thresh_snr - med)

# %% code 114.
from photutils.detection import DAOStarFinder

DAOfind = DAOStarFinder(
                        fwhm = FWHM,
                        threshold = thresh,
                        exclude_border = True,   # 가장자리 거짓 검출 제외
 # sharplo = 0.2, sharphi = 1.0, # default values: sharplo=0.2, sharphi=1.0,
 # roundlo = -1.0, roundhi = 1.0, # default values -1 and +1
 # sigma_radius = 1.5, # default values 1.5
 # ratio = 1.0, # 1.0: circular gaussian
                        )
DAOfound = DAOfind(data_sub)   # 배경을 뺀 영상
print("len(DAOfound) :",len(DAOfound))
DAOfound

# %% code 115.
print("type(DAOfound) :", type(DAOfound))
print("DAOfound :", DAOfound)

# %% code 116.
print(f"DAOfound.colnames : {DAOfound.colnames}")
print(f"(type(DAOfound['x_centroid']) :", type(DAOfound['x_centroid']))
print(f"DAOfound['x_centroid'] : {DAOfound['x_centroid']}")

# %% code 117.
df = DAOfound.to_pandas()
print(type(df))
df

# %% code 118.
pos = np.transpose((DAOfound['x_centroid'], DAOfound['y_centroid']))
print(f"len(pos): {len(pos)}")
print(f"pos[0]: {pos[0]}")
pos  # DAOfound로 찾아낸 별의 픽셀 좌표

# %% code 119.
from photutils.aperture import CircularAperture as CAp

ap = CAp(pos, r=FWHM*4)

fig, axs = plt.subplots(1, 1, figsize=(7.5, 5.2),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = zimshow(axs, hdul[0].data,
            origin='lower',
            )

ap.plot(color='r', lw=1, alpha=0.5)

###########################################################
# 설명할 내용 적기
plt.title("Result of DAOStarfinder", fontsize = 11,
    ha='center')

plt.annotate(f'filename: {fpath.stem}', fontsize=8,
    xy=(0, 0), xytext=(-10, -60), va='top', ha='left',
    xycoords='axes fraction', textcoords='offset points')

plt.annotate(f'FWHM: {FWHM}', fontsize=8,
    xy=(0, 0), xytext=(-10, -30), va='top', ha='left',
    xycoords='axes fraction', textcoords='offset points')

plt.annotate(f'Threshold above sky: {thresh:.02f}', fontsize=8,
    xy=(0, 0), xytext=(-10, -40), va='top', ha='left',
    xycoords='axes fraction', textcoords='offset points')

plt.annotate(f'Number of star(s): {len(DAOfound)}', fontsize=8,
    xy=(0, 0), xytext=(-10, -50), va='top', ha='left',
    xycoords='axes fraction', textcoords='offset points')

plt.colorbar(im1,
            ax=axs,
            fraction=0.0455, pad=0.04)
plt.tight_layout()
plt.show()

# %% code 120.
DAOfound.sort(['flux'], reverse=True)
DAOfound

# %% code 121.
from astropy.nddata import Cutout2D

def plot_star_cutout(data, daofound, idx, cutsize=51):
  """
  Creates a cutout image around a detected star.

  Args:
      data: The 2D astronomical image data.
      daofound: A dictionary containing star detection results from DAOStarFinder.
      idx: The index of the star to plot.
      cutsize: The size (width and height) of the cutout image (default: 51 pixels).
  """

 # 별의 중심 좌표 추출
  xcentroid = daofound['x_centroid'][idx]
  ycentroid = daofound['y_centroid'][idx]

 # 잘라낸 이미지(cutout) 객체 만들기
  cut_hdu = Cutout2D(data=data, position=(xcentroid, ycentroid),
                     size=(cutsize, cutsize))

 # 잘라낸 이미지를 만들어 표시
  fig, ax = plt.subplots(1, 1, figsize=(3.8, 3.2))
  im = zimshow(ax, cut_hdu.data, origin='lower')

  ax.set_ylabel('pixels', fontsize=9)
  ax.tick_params(labelsize=8)
  ax.grid(ls=':')
  ax.set_title(f'Star #{idx} image area', fontsize=10)
  plt.colorbar(im, ax=ax, fraction=0.0455, pad=0.04).ax.tick_params(labelsize=8)

  plt.tight_layout()
  plt.show()

# 사용 예(hdul과 DAOfound가 준비되어 있다고 가정)
plot_star_cutout(hdul[0].data, DAOfound, 0)  # 첫 번째 별(idx=0)의 잘라낸 이미지 그리기

# %% code 122.
import matplotlib.gridspec as gridspec

def plot_star_cutouts(data, daofound, star_indices, cutsize=51):
    """
    4개의 별의 인덱스를 입력받아 해당 별들의 cutout 이미지를 출력하는 함수

    Args:
        data: 2차원 천문 이미지 데이터
        daofound: DAOStarFinder를 통해 얻은 별 검출 결과
        star_indices: 출력할 별들의 인덱스 리스트 (최대 4개)
        cutsize: cutout 이미지의 크기 (default: 51 pixels)
    """
    plt.figure(figsize=(7.5, 7.5))
 # 출력할 별의 개수 제한 (최대 4개)
    nstars = min(len(star_indices), 4)

 # 그리드 생성
    gs = gridspec.GridSpec(2, 2, wspace=0.4, hspace=0.3)

 # 입력된 인덱스에 해당하는 별들의 cutout 이미지 생성 및 출력
    for i, idx in enumerate(star_indices):
        xcentroid = daofound['x_centroid'][idx]
        ycentroid = daofound['y_centroid'][idx]

        cut_hdu = Cutout2D(data=data, position=(xcentroid, ycentroid),
                           size=(cutsize, cutsize))

        ax = plt.subplot(gs[i])
        im = zimshow(ax, cut_hdu.data, origin='lower')

        ax.set_title(f'Star #{idx} image area')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
 # 각 subplot에 colorbar 추가
        plt.colorbar(im, ax=ax, fraction=0.0455, pad=0.04)

    plt.suptitle('Cutout Images of Detected Stars', fontsize=12)   # 간격은 GridSpec이 정함
    plt.show()

# 예시 사용법 (hdul과 DAOfound가 있다고 가정)
plot_star_cutouts(hdul[0].data, DAOfound, [0, 100, 200, 250])  # 0 · 100 · 200 · 250번 별

# %% code 123.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pylab as pl
from astropy.nddata import Cutout2D

def plot_3D_star_cutout(data, daofound, idx, cutsize=31):
    """
    Creates a cutout image around a detected star.

    Args:
    data: The 2D astronomical image data.
    daofound: A dictionary containing star detection results from DAOStarFinder.
    idx: The index of the star to plot.
    cutsize: The size (width and height) of the cutout image (default: 51 pixels).
    """

 # 별의 중심 좌표 추출
    xcentroid = daofound['x_centroid'][idx]
    ycentroid = daofound['y_centroid'][idx]

 # 잘라낸 이미지(cutout) 객체 만들기
    cut_hdu = Cutout2D(data=data, position=(xcentroid, ycentroid),
                       size=(cutsize, cutsize))
    x, y = np.mgrid[:cut_hdu.data.shape[0],:cut_hdu.data.shape[1]]

 # 3D 플롯 생성
    fig = plt.figure(figsize=(4.5, 3.8))
    ax = fig.add_subplot(111, projection='3d')

 # Surface plot 생성
    im = ax.plot_surface(x, y, cut_hdu.data, rstride=1, cstride=1, linewidth=0, antialiased=False,
                cmap=pl.cm.jet,)

    ax.set_ylabel('pixels', fontsize=9)
    ax.tick_params(labelsize=8)
    ax.grid(ls=':')
    ax.set_title(f'Star #{idx} image area', fontsize=10)
    plt.colorbar(im, ax=ax, fraction=0.02, pad=0.08).ax.tick_params(labelsize=8)

    plt.tight_layout()
    plt.show()

# 사용 예(hdul과 DAOfound가 준비되어 있다고 가정)
plot_3D_star_cutout(hdul[0].data, DAOfound, 0)  # 첫 번째 별(idx=0)의 잘라낸 이미지 그리기

# %% code 124.
import numpy as np
import matplotlib.pyplot as plt
from astropy.nddata import Cutout2D

def plot_3D_star_cutout(data, daofound, star_indices, cutsize=31):
    """
    Creates a cutout image around a detected star.

    Args:
    data: The 2D astronomical image data.
    daofound: A dictionary containing star detection results from DAOStarFinder.
    idx: The index of the star to plot.
    cutsize: The size (width and height) of the cutout image (default: 51 pixels).
    """

    fig, axes = plt.subplots(2, 2,
                             figsize=(7.5, 7.5),
                             subplot_kw={'projection': '3d'})
    axes = axes.flatten()

 # 입력된 인덱스에 해당하는 별들의 cutout 이미지 생성 및 출력
    for i, idx in enumerate(star_indices):
        xcentroid = daofound['x_centroid'][idx]
        ycentroid = daofound['y_centroid'][idx]

 # 잘라낸 이미지(cutout) 객체 만들기
        cut_hdu = Cutout2D(data=data, position=(xcentroid, ycentroid),
                           size=(cutsize, cutsize))
        x, y = np.mgrid[:cut_hdu.data.shape[0],:cut_hdu.data.shape[1]]

 # Surface plot 생성
        axes[i].plot_surface(x, y, cut_hdu.data, rstride=1, cstride=1, linewidth=0, antialiased=False,
                        cmap=pl.cm.jet)

        im = axes[i].plot_surface(x, y, cut_hdu.data, rstride=1, cstride=1, linewidth=0, antialiased=False,
                    cmap=pl.cm.jet,)
        axes[i].set_zlim(0, 65535)
        axes[i].set_ylabel('pixels')
        axes[i].grid(ls=':')
        axes[i].set_title(f'Star #{idx} image area', fontsize=10)
        plt.colorbar(im, ax=axes[i], fraction=0.025, pad=0.12)

    plt.tight_layout()
    plt.show()

# 사용 예(hdul과 DAOfound가 준비되어 있다고 가정)
plot_3D_star_cutout(hdul[0].data, DAOfound, [0, 1, 2, 3])

# %% code 125.
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pylab as pl
from astropy.nddata import Cutout2D
from astropy.io import fits


def peak_label(peak):
    """원래 화소값(배경 포함)의 최댓값으로 노출 상태를 판정"""
    if peak >= 60000:
        return "포화"
    if peak >= 40000:
        return "거의 포화"
    if peak >= 15000:
        return "적정"
    return "어두움"


def plot_3d_surfaces(data, DAOfound, sky, cutsize=31):
    peak_raw = np.asarray(DAOfound['peak']) + sky        # 배경을 더해 원래 화소값으로
    # 가장 밝은 별, 그리고 peak가 45000 · 30000 · 10000 ADU에 가장 가까운 별
    indices = [int(np.argmax(peak_raw))]
    indices += [int(np.argmin(np.abs(peak_raw - level))) for level in (45000, 30000, 10000)]

    fig = plt.figure(figsize=(7.5, 7.5))
    for i, index in enumerate(indices):
        ax = fig.add_subplot(2, 2, i+1, projection='3d')

        cut_hdu = Cutout2D(
            data=data,
            position=(DAOfound['x_centroid'][index],
                      DAOfound['y_centroid'][index]),
            size=(cutsize, cutsize)
        )

        x, y = np.mgrid[:cut_hdu.data.shape[0], :cut_hdu.data.shape[1]]
        im = ax.plot_surface(x, y, cut_hdu.data, cmap=pl.cm.jet,
                             rstride=1, cstride=1, linewidth=0., antialiased=False)

        ax.set_xlabel('pixels')
        ax.grid(ls=':')
        ax.set_title(f"{peak_label(peak_raw[index])} (peak {peak_raw[index]:.0f} ADU)", fontsize=10)
        plt.colorbar(im, ax=ax, fraction=0.025, pad=0.12)

    plt.tight_layout()
    plt.show()

# 함수 사용 예
plot_3d_surfaces(hdul[0].data, DAOfound, sky=med)

# %% code 126.
import numpy as np
import matplotlib.pyplot as plt
from astropy.nddata import Cutout2D

def plot_star_profile_fwhm(data, daofound, idx, cutsize=31):
    """
    Creates a cutout image around a detected star and plots horizontal and vertical profiles with FWHM.

    Args:
    data: The 2D astronomical image data.
    daofound: A dictionary containing star detection results from DAOStarFinder.
    idx: The index of the star to plot.
    cutsize: The size (width and height) of the cutout image (default: 31 pixels).
    """

 # 별의 중심 좌표 추출
    xcentroid = daofound['x_centroid'][idx]
    ycentroid = daofound['y_centroid'][idx]

 # 잘라낸 이미지(cutout) 객체 만들기
    cut_hdu = Cutout2D(data=data, position=(xcentroid, ycentroid),
                       size=(cutsize, cutsize))

 # 가로·세로 방향 프로파일 계산
    horizontal_profile = np.mean(cut_hdu.data, axis=0)
    vertical_profile = np.mean(cut_hdu.data, axis=1)

 # 가로 프로파일의 FWHM 계산
    x = np.arange(len(horizontal_profile))
    y = horizontal_profile
    peak_value = np.max(y)
    peak_index = np.argmax(y)
    half_max = (peak_value - np.median(y)) / 2.0 + np.median(y)
    left_index = np.argmin(np.abs(y[:peak_index] - half_max))
    right_index = np.argmin(np.abs(y[peak_index:] - half_max)) + peak_index
    fwhm_horizontal = x[right_index] - x[left_index]
    left_h, right_h = left_index, right_index

 # 세로 프로파일의 FWHM 계산
    x = np.arange(len(vertical_profile))
    y = vertical_profile
    peak_value = np.max(y)
    peak_index = np.argmax(y)
    half_max = (peak_value - np.median(y)) / 2.0 + np.median(y)
    left_index = np.argmin(np.abs(y[:peak_index] - half_max))
    right_index = np.argmin(np.abs(y[peak_index:] - half_max)) + peak_index
    fwhm_vertical = x[right_index] - x[left_index]
    left_v, right_v = left_index, right_index

 # 그래프 만들기
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.8))

 # 가로 프로파일 그리기
    axes[0].plot(horizontal_profile)
    axes[0].axvline(x=left_h, color='r', linestyle='--',
                    label=f'FWHM = {fwhm_horizontal:.2f}')
    axes[0].axvline(x=right_h, color='r', linestyle='--')
    axes[0].set_xlabel('X (pixels)')
    axes[0].set_ylabel('Pixel Value')
    axes[0].set_title('Horizontal Profile')
    axes[0].legend()

 # 세로 프로파일 그리기
    axes[1].plot(vertical_profile)
    axes[1].axvline(x=left_v, color='r', linestyle='--',
                    label=f'FWHM = {fwhm_vertical:.2f}')
    axes[1].axvline(x=right_v, color='r', linestyle='--')
    axes[1].set_xlabel('Y (pixels)')
    axes[1].set_ylabel('Pixel Value')
    axes[1].set_title('Vertical Profile')
    axes[1].legend()

    plt.tight_layout()
    plt.show()

# 사용 예(hdul과 DAOfound가 준비되어 있다고 가정)
plot_star_profile_fwhm(hdul[0].data, DAOfound, 25)
