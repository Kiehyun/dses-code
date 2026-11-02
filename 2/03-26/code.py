# 지구과학 데이터 사이언스 2 | III-06. FITS 파일 천체 위치 보정
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅲ-134.
# 파일 ID와 저장 경로를 리스트로 정의
files = [
    ("1USKkCup8BTHmBVyg8iC4od1gV19v2MEg",
     "46P-WIRTANEN_LIGHT_R_2018-12-13-17-46-15_"
     "60sec_FSQ106ED-x73_QSI683ws_-30c_2bin.fit"),
    ("1eRogyBdYziV1oO6PV_ZGUlCvf3VRGnlS",
     "IC434_Light_H_2019-10-08-09-38-54_"
     "900sec_GSON300_QSI683ws_-15C_1bin.fit"),
    ("1seA_sztIITefVCJcfNmCW8MLKDjL8HhH",
     "M13_Light_L_2021-06-04-13-10-16_090sec_"
     "TEC140x75_STL-11000M_-19C_1bin.fit")
]

# for 루프를 사용하여 파일 내려받기
for file_id, output_path in files:
    du.download(f"https://docs.google.com/uc?export=download&id={file_id}",
                PROJ / output_path)

# %% code Ⅲ-135.
fpaths = du.list_files(PROJ, "fit*")

# %% code Ⅲ-136.
fpaths[0]

# %% code Ⅲ-137.
from pathlib import Path
from astropy.io import fits

fpath = Path(fpaths[0])
print("fpath", (fpath))

hdul = fits.open(fpath)

print("type(hdul) :", type(hdul))
print("hdul :", hdul)

# %% code Ⅲ-138.
import matplotlib.pyplot as plt

from astropy.visualization import (MinMaxInterval, SqrtStretch,
                                   ImageNormalize)

# ImageNormalize 객체 만들기
norm = ImageNormalize(hdul[0].data, interval=MinMaxInterval(),
                      stretch=SqrtStretch())

fig, axs = plt.subplots(1, 2, figsize=(7.5, 2.5),
                       sharex=False, sharey=False, gridspec_kw=None)

im1 = axs[0].imshow(hdul[0].data, origin='lower')
axs[0].set_title('Original', fontsize=8)

im2 = axs[1].imshow(hdul[0].data, origin='lower', norm=norm)
axs[1].set_title('Normalization', fontsize=8)

fig.suptitle(f'{str(fpaths[0])}', fontsize=8)
fig.colorbar(im1, ax = axs[0], fraction=0.035, pad=0.04)
fig.colorbar(im2, ax = axs[1], fraction=0.035, pad=0.04)
plt.tight_layout()

# %% code Ⅲ-139.
# 영상 표시 함수 znorm · zimshow · norm_imshow 는 Ⅲ-04 「FITS
# 파일 다루기」에서 설명했고 dses_utils 에 들어 있음

# %% code Ⅲ-140.
def checkPSolve(fpath,
                    **kwargs,
                    ):
    """
    Parameters
    ----------
    fpath : path-like
        The path to the original FITS file.

    return
    ----------
    SOLVE, ASTAP, LOCAL :  bool, bool, bool

    """

    fpath = Path(fpath)

    hdul = fits.open(fpath)
    PSKeys = ["CRVAL1", "CRVAL2", "CRPIX1", "CRPIX2",
              "CD1_1", "CD1_2", "CD2_1", "CD2_2",
              "A_0_0", "A_0_1", "A_1_0","A_1_1",
              "PC1_1", "PC1_2", "PC2_1", "PC2_2"]

    chk = 0
    SOLVE = False
    ASTAP = False
    LOCAL = False

    for PSKey in PSKeys :
        if PSKey in hdul[0].header :
            chk += 1
    if chk > 5 :
        SOLVE = True
        LOCAL = False
        ASTAP = False
        try :
            for comment in hdul[0].header["COMMENT"]:
                if "scale:" in comment :
                    LOCAL = True
        except :
            LOCAL = False

        if "PLTSOLVD" in hdul[0].header:
            try :
                ASTAP = hdul[0].header["PLTSOLVD"]
            except :
                ASTAP = False
    else :
        SOLVE = False
        ASTAP = False
        LOCAL = False
    hdul.close()

    return SOLVE, ASTAP, LOCAL

# %% code Ⅲ-141.
SOLVE, ASTAP, LOCAL = checkPSolve(str(fpaths[0]))
print("SOLVE, ASTAP, LOCAL :", SOLVE, ASTAP, LOCAL)
SOLVE, ASTAP, LOCAL = checkPSolve(str(fpaths[1]))
print("SOLVE, ASTAP, LOCAL :", SOLVE, ASTAP, LOCAL)
SOLVE, ASTAP, LOCAL = checkPSolve(str(fpaths[2]))
print("SOLVE, ASTAP, LOCAL :", SOLVE, ASTAP, LOCAL)

# %% code Ⅲ-142.
import os
from astroquery.astrometry_net import AstrometryNet

ast = AstrometryNet()

# API 키는 코드에 적지 않고 환경 변수에서 읽음(nova.astrometry.net 에서 발급)
api_key = os.environ.get("ASTROMETRY_NET_API_KEY", "")
if api_key:
    ast.api_key = api_key
    print("환경 변수 ASTROMETRY_NET_API_KEY 에서 API 키를 읽었습니다.")
else:
    print("환경 변수 ASTROMETRY_NET_API_KEY 가 없습니다. 새 파일을 위치 보정하려면 키를 설정하세요.\n"
          "(이미 위치 보정된 파일은 키 없이 다룰 수 있습니다)")

# %% code Ⅲ-143.
print(fpaths[0])
SOLVE, ASTAP, LOCAL = checkPSolve(str(fpaths[0]))
print("SOLVE, ASTAP, LOCAL :", SOLVE, ASTAP, LOCAL)
print("before solving :", "헤더 카드", len(hdul[0].header), "개")

solve_timeout = 600
if SOLVE:
    print("이미 위치 보정된 파일이므로 다시 풀지 않습니다.")
elif not api_key:                       # ast.api_key 는 키가 없으면 RuntimeError를 냄
    print("API 키가 없어 위치 보정을 건너뜁니다.")
else:
    wcs_header = ast.solve_from_image(str(fpaths[0]),
                            solve_timeout = solve_timeout)
    if wcs_header :
        with fits.open(str(fpaths[0]), mode='update') as hdul:
            for card in wcs_header :
                if card in ("COMMENT", "HISTORY", ""):     # 설명 카드는 건너뜀
                    continue
                hdul[0].header.set(card, wcs_header[card],
                                   wcs_header.comments[card])
            hdul.flush()

        print(str(fpaths[0])+" is updated...")

        SOLVE, ASTAP, LOCAL = checkPSolve(str(fpaths[0]))
        print("SOLVE, ASTAP, LOCAL :", SOLVE, ASTAP, LOCAL)

# %% code Ⅲ-144.
#########################################
# 천체 위치 보정기(AstrometrySolver)
#########################################
from astroquery.exceptions import TimeoutError as AQTimeoutError

def AstrometrySolver(fpath,
                    ast = ast,
                    submission_id = None,
                    solve_timeout = 600,
                    **kwargs,
                    ):
    """
    FITS 파일 하나를 nova.astrometry.net으로 위치 보정하고 결과 WCS를 헤더에 써넣습니다.

    Parameters
    ----------
    fpath : path-like
        위치 보정할 FITS 파일 경로

    Returns
    -------
    SOLVE, ASTAP, LOCAL : bool, bool, bool
        함수를 부르기 전의 위치 보정 상태
    """

    fpath = Path(fpath)
    print(f"check plate solving : {fpath.name}")
    SOLVE, ASTAP, LOCAL = checkPSolve(str(fpath))
    print("SOLVE, ASTAP, LOCAL:", SOLVE, ASTAP, LOCAL)

    if SOLVE :
        print(f"{fpath.name} is already solved...")
    else :
        # 키는 위치 보정이 필요할 때만 확인
        if not os.environ.get("ASTROMETRY_NET_API_KEY"):
            print("API 키가 없어 위치 보정을 건너뜁니다.")
            return SOLVE, ASTAP, LOCAL
        try_again = True

        try :
            while try_again:
                try:
                    if not submission_id:
                        wcs_header = ast.solve_from_image(str(fpath),
                                            solve_timeout = solve_timeout)
                    else:
                        wcs_header = ast.monitor_submission(submission_id,
                                                            solve_timeout = solve_timeout)
                # astroquery의 시간 초과 예외(내장 TimeoutError와 다름)
                except AQTimeoutError as e:
                    submission_id = e.args[1]
                else:
                    # 결과를 받았으므로 종료
                    try_again = False

            if not wcs_header:
                # 위치 보정에 실패했을 때 실행할 코드
                print("fits file solving failure...")

            else:
                # 위치 보정에 성공했을 때 실행할 코드
                print("fits file solved successfully...")

                with fits.open(str(fpath), mode='update') as hdul:
                    for card in wcs_header :
                        if card in ("COMMENT", "HISTORY", ""):   # 설명 카드는 건너뜀
                            continue
                        hdul[0].header.set(card, wcs_header[card],
                                           wcs_header.comments[card])
                    hdul.flush()

                print(str(fpath)+" is updated...")

        except Exception as err:
            print("Err :", err)

    return SOLVE, ASTAP, LOCAL

# %% code Ⅲ-145.
AstrometrySolver(fpaths[0])
AstrometrySolver(fpaths[1])
AstrometrySolver(fpaths[2])

# %% code Ⅲ-146.
SOLVE, ASTAP, LOCAL = checkPSolve(str(fpaths[0]))
print("SOLVE, ASTAP, LOCAL :", SOLVE, ASTAP, LOCAL)
SOLVE, ASTAP, LOCAL = checkPSolve(str(fpaths[1]))
print("SOLVE, ASTAP, LOCAL :", SOLVE, ASTAP, LOCAL)
SOLVE, ASTAP, LOCAL = checkPSolve(str(fpaths[2]))
print("SOLVE, ASTAP, LOCAL :", SOLVE, ASTAP, LOCAL)

# %% code Ⅲ-147.
def show_header(header, n_head=8):
    """헤더 앞부분과 WCS 관련 카드만 출력하고 나머지는 줄임"""
    cards = list(header.cards)
    for card in cards[:n_head]:
        print(card)
    print(f"... (중략 — 전체 {len(cards)}장 중 앞 {n_head}장과 WCS 카드만 표시)")
    wcs_keys = ("CTYPE", "CUNIT", "CRVAL", "CRPIX", "CD1_", "CD2_",
                "PC1_", "PC2_", "CDELT", "EQUINOX", "RADESYS")
    for card in cards[n_head:]:
        if card.keyword.startswith(wcs_keys):
            print(card)

print("fpaths[0] :", fpaths[0])
hdul0 = fits.open(str(fpaths[0]))
show_header(hdul0[0].header)

# %% code Ⅲ-148.
print("fpaths[1] :", fpaths[1])
hdul1 = fits.open(str(fpaths[1]))
show_header(hdul1[0].header)

# %% code Ⅲ-149.
print("fpaths[2] :", fpaths[2])
hdul2 = fits.open(str(fpaths[2]))
show_header(hdul2[0].header)

# %% code Ⅲ-150.
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS

wcs0 = WCS(hdul0[0].header)
wcs1 = WCS(hdul1[0].header)
wcs2 = WCS(hdul2[0].header)

# %% code Ⅲ-151.
print("wcs0 :", wcs0)
print("wcs1 :", wcs1)
print("wcs2 :", wcs2)
print("wcs0.world_axis_physical_types :", wcs0.world_axis_physical_types)
print("wcs1.world_axis_physical_types :", wcs1.world_axis_physical_types)

# %% code Ⅲ-152.
import numpy as np
from astropy.wcs.utils import proj_plane_pixel_scales

for name, w, h in [("hdul0", wcs0, hdul0[0].header),
                   ("hdul1", wcs1, hdul1[0].header),
                   ("hdul2", wcs2, hdul2[0].header)]:
    scale = proj_plane_pixel_scales(w) * 3600  # 도 → 각초
    fov_x = scale[0] * h["NAXIS1"] / 60        # 각초 → 각분
    fov_y = scale[1] * h["NAXIS2"] / 60
    print(f"{name}: CRVAL = ({w.wcs.crval[0]:.4f}, {w.wcs.crval[1]:.4f}) deg, "
          f"CRPIX = ({w.wcs.crpix[0]:.1f}, {w.wcs.crpix[1]:.1f}), "
          f"화소 축척 = {scale[0]:.3f}″/px, 시야 = {fov_x:.1f}′ × {fov_y:.1f}′")

# %% code Ⅲ-153.
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection=wcs1)   # hdul1(IC434) 영상의 WCS
im = plt.imshow(hdul1[0].data, origin='lower', cmap="viridis",)

# ax.coords['ra'].set_ticks(spacing=5. * u.arcmin)
# ax.coords['dec'].set_ticks(spacing=5. * u.arcmin)
ax.coords['ra'].set_auto_axislabel(True)
ax.coords['dec'].set_auto_axislabel(True)
# ax.coords['ra'].set_ticks_position('lb')
# ax.coords['dec'].set_ticks_position('lb')
ax.coords['ra'].set_ticklabel_visible(True)
ax.coords['ra'].set_ticklabel(size=8)
ax.coords['dec'].set_ticklabel(size=8)
ax.coords['ra'].set_major_formatter('hh:mm:ss')
ax.coords['dec'].set_major_formatter('dd:mm:ss')
ax.coords['ra'].set_ticklabel_position('l')    #왼쪽, 오른쪽, 아래, 위
ax.coords['dec'].set_ticklabel_position('bt')  #왼쪽, 오른쪽, 아래, 위

ax.grid(color='white', ls='dotted')

# overlay = ax.get_coords_overlay('icrs')
# overlay.grid(color='white', ls='dotted')

plt.title('Image display using WCS', fontsize=11, pad=35)
fig.colorbar(im, fraction=0.035, pad=0.04)
plt.tight_layout(pad=0.4, w_pad=1, h_pad=1.0)
plt.show()

# %% code Ⅲ-154.
fig, axs = plt.subplots(1, 1, sharex=False, sharey=False, gridspec_kw=None,
                        subplot_kw={'projection': wcs0})

im = du.zimshow(axs, hdul0[0].data, origin='lower', cmap="viridis")

axs.coords['ra'].set_ticks(spacing=10 * u.arcmin, color='green')
axs.coords['dec'].set_ticks(spacing=10 * u.arcmin, color='orange')
axs.coords['ra'].display_minor_ticks(True)
axs.coords['dec'].display_minor_ticks(True)
axs.coords['ra'].set_ticklabel_visible(True)
axs.coords['dec'].set_ticklabel_visible(True)
axs.coords['ra'].set_ticklabel(size=8)
axs.coords['dec'].set_ticklabel(size=8)
# axs.coords['ra'].set_minor_frequency(10)
# axs.coords['dec'].set_minor_frequency(10)
axs.coords['ra'].set_ticklabel_position('b')   #왼쪽, 오른쪽, 아래, 위
axs.coords['dec'].set_ticklabel_position('l')  #왼쪽, 오른쪽, 아래, 위
axs.coords['ra'].set_major_formatter('hh:mm:ss')
axs.coords['dec'].set_major_formatter('dd:mm:ss')
# axs.coords['ra'].set_auto_axislabel(True)
# axs.coords['dec'].set_auto_axislabel(True)
# axs.coords['ra'].set_axislabel('Right Ascension')
# axs.coords['dec'].set_axislabel('Declination')
axs.coords['ra'].set_axislabel_position('b')   #왼쪽, 오른쪽, 아래, 위
axs.coords['dec'].set_axislabel_position('l')  #왼쪽, 오른쪽, 아래, 위

axs.grid(color='white', ls='dotted')

axs.set_title('Image display using WCS', fontsize=11, pad=30)

fig.colorbar(im, fraction=0.035, pad=0.04)

plt.tight_layout()
plt.show()

# %% code Ⅲ-155.
fig, axs = plt.subplots(1, 2, figsize=(7.5, 2.5),
                        sharex=False, sharey=False, gridspec_kw=None,
                        subplot_kw={'projection': wcs1})

im0 = du.zimshow(axs[0], hdul1[0].data, origin='lower', cmap="viridis")

axs[0].set_title('Image display using WCS', fontsize=10 , pad=30)

im1 = du.zimshow(axs[1], hdul1[0].data, origin='lower', cmap="viridis")

axs[1].coords['ra'].set_auto_axislabel(True)
axs[1].coords['dec'].set_auto_axislabel(True)
axs[1].coords['ra'].set_axislabel('Right Ascension (J2000.0)', minpad=2)
axs[1].coords['dec'].set_axislabel('Declination (J2000.0)', minpad=2)
axs[1].coords['ra'].set_axislabel_position('b')   #왼쪽, 오른쪽, 아래, 위
axs[1].coords['dec'].set_axislabel_position('l')  #왼쪽, 오른쪽, 아래, 위
axs[1].coords['ra'].set_ticklabel_position('b')   #왼쪽, 오른쪽, 아래, 위
axs[1].coords['dec'].set_ticklabel_position('l')  #왼쪽, 오른쪽, 아래, 위

overlay1 = axs[1].get_coords_overlay('fk5')
overlay1.grid(color='white', ls='dotted')
# overlay1[0].set_axislabel('Right Ascension (J2000.0)', minpad=2)
# overlay1[1].set_axislabel('Declination (J2000.0)', minpad=2)
# overlay1[0].set_axislabel_position('b')
# overlay1[1].set_axislabel_position('l')
# overlay1[0].set_ticklabel_position('b') #left, right, bottom, top
# overlay1[1].set_ticklabel_position('l') #left, right, bottom, top

axs[1].set_title('Image display using WCS', fontsize=10 , pad=30)

fig.colorbar(im0, ax = axs[0], fraction=0.0315, pad=0.04)
fig.colorbar(im1, ax = axs[1], fraction=0.0315, pad=0.04)

plt.tight_layout(pad=0.4, w_pad=1, h_pad=1.0)
plt.show()

# %% code Ⅲ-156.
fig, axs = plt.subplots(2, 1, figsize=(5.3, 8),
                        sharex=False, sharey=False, gridspec_kw=None,
                        subplot_kw={'projection': wcs2})

im0 = du.zimshow(axs[0], hdul2[0].data, origin='lower', cmap="viridis")

axs[0].coords['ra'].set_ticklabel_position('b')   #왼쪽, 오른쪽, 아래, 위
axs[0].coords['dec'].set_ticklabel_position('l')  #왼쪽, 오른쪽, 아래, 위
axs[0].plot_coord(SkyCoord(249.5*u.deg, 36.5*u.deg, frame="icrs"), "rx")
axs[0].plot_coord(SkyCoord(250*u.deg, 36*u.deg, frame="icrs"), "r+")

overlay0 = axs[0].get_coords_overlay('icrs')
overlay0.grid(color='white', ls='dotted')
overlay0[0].set_axislabel('Right Ascension', minpad=2)
overlay0[1].set_axislabel('Declination', minpad=2)
overlay0[0].set_axislabel_position('b')
overlay0[1].set_axislabel_position('l')
overlay0[0].set_ticklabel_position('b')  #왼쪽, 오른쪽, 아래, 위
overlay0[1].set_ticklabel_position('l')  #왼쪽, 오른쪽, 아래, 위
axs[0].set_title('Image display using WCS (ICRS)', fontsize=12, pad=30)

im1 = du.zimshow(axs[1], hdul2[0].data, origin='lower', cmap="viridis")

# axs[1].coords['ra'].set_axislabel('Right Ascension (J2000.0)')
# axs[1].coords['dec'].set_axislabel('Declination (J2000.0)')
# axs[1].coords['ra'].set_axislabel_position('b') #left, right, bottom, top
# axs[1].coords['dec'].set_axislabel_position('l') #left, right, bottom, top
axs[1].coords['ra'].set_ticklabel_position('b')   #왼쪽, 오른쪽, 아래, 위
axs[1].coords['dec'].set_ticklabel_position('l')  #왼쪽, 오른쪽, 아래, 위
axs[1].grid(color='white', ls=':')

axs[1].plot_coord(SkyCoord(249.5*u.deg, 36.5*u.deg, frame="fk5"), "rx",
                  markersize=10)
axs[1].plot_coord(SkyCoord(250*u.deg, 36*u.deg, frame="fk5"), "r+",
                  markersize=10)

overlay1 = axs[1].get_coords_overlay('fk5')
overlay1.grid(color='white', ls='dotted')
overlay1[0].set_axislabel('Right Ascension (J2000.0)', minpad=2)
overlay1[1].set_axislabel('Declination (J2000.0)', minpad=2)
overlay1[0].set_axislabel_position('b')
overlay1[1].set_axislabel_position('l')
overlay1[0].set_ticklabel_position('b')  #왼쪽, 오른쪽, 아래, 위
overlay1[1].set_ticklabel_position('l')  #왼쪽, 오른쪽, 아래, 위

axs[1].set_title('Image display using WCS (FK5)', fontsize=12, pad=30)

fig.colorbar(im0, ax = axs[0], fraction=0.031, pad=0.04)
fig.colorbar(im1, ax = axs[1], fraction=0.031, pad=0.04)

plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
plt.show()
