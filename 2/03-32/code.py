# 지구과학 데이터 사이언스 2 | III-12. SkyBoT으로 소행성 찾기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅲ-287.
import os
from pathlib import Path

# %% code Ⅲ-288.
# 파일 이름과 파일 ID를 리스트로 저장
files = [
    {"fname": ("0000481-EMITA_LIGHT_R_2023-11-13-15-09-08_150sec_"
               "GSON300_STF-8300M_-29c_1bin.fit"),
     "fid": "1VeIm-dkmCQMb41tZ2ib_0QwiygYl7-RD"},
    {"fname": ("0000481-EMITA_LIGHT_R_2023-11-13-18-26-08_150sec_"
               "GSON300_STF-8300M_-29c_1bin.fit"),
     "fid": "13NKJi5YMF5rJnG-zP7L6sYpDf8naXRY5"},
]

# for 루프를 사용하여 파일 내려받기
for file in files:
    du.download(f"https://drive.google.com/uc?id={file['fid']}",
                proj_dir / file["fname"])

# %% code Ⅲ-289.
fpaths = du.list_files(proj_dir, "fit*")

# %% code Ⅲ-290.
from astropy.io import fits

fpath = Path(fpaths[0])
hdul = fits.open(str(fpath))
for k in ["NAXIS1", "NAXIS2", "DATE-OBS", "EXPTIME", "OBJECT", "FILTER"]:
    if k in hdul[0].header:
        print(f"{k:9s} = {hdul[0].header[k]}")
print("data :", hdul[0].data.dtype, hdul[0].data.shape)

# %% code Ⅲ-291.
from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz

# 관측소
Suwon = EarthLocation(lon=127.005 * u.deg, lat=37.308889 * u.deg,
                                 height=101 * u.m)
observatory_code = "P64"

#####################################################################
# `astropy.SkyCoord` 객체에 공통으로 쓰는 인수
SKYC_KW = dict(unit=u.deg, frame='icrs')

# %% code Ⅲ-292.
#######################################################
# 망원경과 CCD
if hdul[0].header["CCDNAME"] == "STF-8300M" :
    val_figsize=(7.5, 5.6)
    gain = 0.37
    rdnoise = 9.3
    pix_size = 5.4 * u.um
    val_fraction = 0.035

if hdul[0].header["CCDNAME"] == "STX-16803" :
    val_figsize=(7.5, 6.8)
    gain = 1.27
    rdnoise = 9.0
    pix_size = 9 * u.um
    val_fraction = 0.0455

if hdul[0].header["OPTIC"] == "GSON300" :
    focal_length = 1200 * u.mm

if hdul[0].header["OPTIC"] == "RiLA600" :
    focal_length = 3000 * u.mm

print("rdnoise, gain, pix_size, focal_length :", rdnoise, gain, pix_size,
      focal_length)

# %% code Ⅲ-293.
#######################################################
# PIXSCALE
if 'PIXSCALE' in hdul[0].header:
    PIX2ARCSEC = hdul[0].header['PIXSCALE']
else :  # 화소 크기(um, 비닝 반영)와 초점 거리(mm)로 계산
    PIX2ARCSEC = (206.265 * hdul[0].header['XPIXSZ']
                  / hdul[0].header['FOCALLEN'])

PIX2ARCSEC = PIX2ARCSEC # * u.arcsec / u.pixel
print("PIX2ARCSEC :", PIX2ARCSEC)

# %% code Ⅲ-294.
#######################################################
# FWHM 초기 추정값(화소)
FWHM_INIT = 6

# 측광 변수
R_AP = 1.5*FWHM_INIT  # 구경 반지름
R_IN = 4*FWHM_INIT    # 고리(annulus) 안쪽 반지름
R_OUT = 6*FWHM_INIT   # 고리(annulus) 바깥쪽 반지름

Mag_UP = 16
#######################################################

# %% code Ⅲ-295.
from astropy.time import Time
# 관측 시각을 정하기 위해 관측 시간과 노출 시간 확인
t_start = Time(hdul[0].header['DATE-OBS'], format='isot')
t_expos = hdul[0].header['EXPTIME'] * u.s
t_middle = t_start + t_expos / 2 # 시작 시각 + 노출 시간의 절반
print(f"t_start: {t_start}, t_expos: {t_expos}, t_middle: {t_middle}")

# %% code Ⅲ-296.
# 위치 보정 여부 확인 — Ⅲ-06 「FITS 파일 천체 위치 보정」에서 만든 du.checkPSolve(dses_utils)
SOLVE, ASTAP, LOCAL = du.checkPSolve(str(fpath))
print("SOLVE, ASTAP, LOCAL :", SOLVE, ASTAP, LOCAL)

# %% code Ⅲ-297.
from astropy.wcs import WCS

wcs = WCS(hdul[0].header)

# 영상 중심 화소(0부터 센 번호)를 하늘 좌표로 바꿈
nx, ny = hdul[0].header["NAXIS1"], hdul[0].header["NAXIS2"]
cent = wcs.pixel_to_world((nx - 1) / 2, (ny - 1) / 2).icrs
cent_coord = SkyCoord(cent.ra, cent.dec, **SKYC_KW)

# 망원경이 가리킨 좌표에서 영상 중심까지 하늘에서 잰 어긋남
# (spherical_offsets_to: 적경 방향은 cos(적위), 방위각 방향은 cos(고도)를 곱한 각거리)
tel_coord = SkyCoord(hdul[0].header['RA'], hdul[0].header['DEC'], **SKYC_KW)
offset_RA, offset_DEC = [o.to(u.arcmin) for o in tel_coord.spherical_offsets_to(cent_coord)]

altaz = AltAz(obstime=t_middle, location=Suwon)
cent_aa = cent_coord.transform_to(altaz)
tel_aa = SkyCoord(az=hdul[0].header['CENTAZ'] * u.deg,
                  alt=hdul[0].header['CENTALT'] * u.deg, frame=altaz)
offset_AZ, offset_ALT = [o.to(u.arcmin) for o in tel_aa.spherical_offsets_to(cent_aa)]

print(f"image center (RA, DEC): ({cent_coord.ra:.03f}, "
      f"{cent_coord.dec:.03f})")
print(f"telescope center (RA, DEC): ({tel_coord.ra:.03f}, {tel_coord.dec:.03f})")
print(f"offset (RA cos DEC, DEC): ({offset_RA:.03f}, {offset_DEC:.03f})")
print(f"offset (AZ cos ALT, ALT): ({offset_AZ:.03f}, {offset_ALT:.03f})")

# %% code Ⅲ-298.
import requests
import pandas as pd
from astropy.coordinates import Angle
from astroquery.imcce import Skybot

def jpl_sb_ident(center, half_width, epoch, mpc_code="P64", vmag_lim=20):
    """JPL SB Ident API로 시야 안 소행성 목록을 받아 SkyBoT과 같은 열 이름으로 돌려줌"""
    ra = center.ra.to_string(unit=u.hourangle, sep="-", precision=1, pad=True)
    dec = center.dec.to_string(unit=u.deg, sep="-", precision=0, pad=True, alwayssign=True)
    # 음수 적위는 M
    dec = dec.replace("-", "M", 1) if dec.startswith("-") else dec.lstrip("+")
    params = {"sb-kind": "a", "mpc-code": mpc_code,
              "obs-time": epoch.utc.strftime("%Y-%m-%d_%H:%M:%S"),
              "fov-ra-center": ra, "fov-dec-center": dec,
              "fov-ra-hwidth": half_width.to(u.deg).value,
              "fov-dec-hwidth": half_width.to(u.deg).value,
              "two-pass": "true", "vmag-lim": vmag_lim}
    data = requests.get("https://ssd-api.jpl.nasa.gov/sb_ident.api",
                        params=params, timeout=300).json()
    rows = data.get("data_second_pass") or []
    df = pd.DataFrame(rows, columns=data.get("fields_second"))
    if df.empty:
        return pd.DataFrame(columns=["Number", "Name", "RA", "DEC", "V", "RA_rate", "DEC_rate"])
    name = df["Object name"].str.extract(r"^(?:(\d+)\s+)?([^(]*?)\s*(?:\((.+)\))?$")
    out = pd.DataFrame({
        "Number": name[0].fillna(name[2]),                 # 번호가 없으면 임시 부호
        "Name": name[1].where(name[1] != "", name[2]),
        "RA": Angle(df["Astrometric RA (hh:mm:ss)"], unit=u.hourangle).deg,
        "DEC": Angle(df['Astrometric Dec (dd mm\'ss")'].str.replace("'", "m")
                     .str.replace('"', "s").str.replace(" ", "d", n=1), unit=u.deg).deg,
        "V": pd.to_numeric(df["Visual magnitude (V)"], errors="coerce"),
        "RA_rate": pd.to_numeric(df['RA rate ("/h)'], errors="coerce"),    # cos δ 곱한 값
        "DEC_rate": pd.to_numeric(df['Dec rate ("/h)'], errors="coerce"),
    })
    return out

try:
    results_ast = Skybot.cone_search(cent_coord, 30*u.arcmin, t_middle,
                                     find_comets=False)   # 혜성은 빼고 소행성만
    df_ast = results_ast.to_pandas()
    print("SkyBoT에서 받은 소행성:", len(df_ast))
except Exception as e:                       # 서버 오류 · 주소 변경 등
    print(f"SkyBoT 응답 없음({type(e).__name__}) → JPL SB Ident로 대신 조회")
    df_ast = jpl_sb_ident(cent_coord, 30*u.arcmin, t_middle,
                          mpc_code=observatory_code)
    print("JPL SB Ident에서 받은 소행성:", len(df_ast))
df_ast[["Number", "Name", "RA", "DEC", "V"]].head(10)   # 앞의 10개만 표시

# %% code Ⅲ-299.
df_targ = df_ast[df_ast['V'] < Mag_UP]
df_targ = df_targ.sort_values(by=['V'])
df_targ = df_targ.reset_index(drop=True)
df_targ[["Number", "Name", "RA", "DEC", "V"]]

# %% code Ⅲ-300.
import pandas as pd
from astroquery.jplhorizons import Horizons

def small_body_ephem(number, epochs, centers):
    """Horizons 천체력 표. Horizons가 응답하지 않으면 JPL SB Ident로 위치·밝기·빠르기만 받음"""
    try:
        eph = Horizons(id=number,
                       id_type="smallbody",      # 499(화성) 같은 대형 천체 ID와 혼동 방지
                       location=observatory_code,
                       epochs=[t.jd for t in epochs]).ephemerides()
        return eph.to_pandas()
    except Exception as e:                       # 서버 오류 등
        print(f"Horizons 응답 없음({type(e).__name__}) → JPL SB Ident로 대신 조회({number})")
        rows = []
        for t, c in zip(epochs, centers):
            d = jpl_sb_ident(c, 30 * u.arcmin, t, mpc_code=observatory_code, vmag_lim=25)
            r = d[d["Number"] == str(number)].iloc[0]
            rows.append({"targetname": f"{number} {r['Name']}", "datetime_str": t.isot,
                         "RA": r["RA"], "DEC": r["DEC"], "V": r["V"],
                         "RA_rate": r["RA_rate"], "DEC_rate": r["DEC_rate"]})
        return pd.DataFrame(rows)

if df_targ.empty:
    pass
else:
    # 이 천체들의 위치 예보를 질의함
    df_targ_eph = pd.concat([small_body_ephem(row["Number"], [t_middle], [cent_coord])
                             for _, row in df_targ.iterrows()], axis=0)
    df_targ_eph = df_targ_eph.reset_index(drop=True)
    df_targ_eph = pd.concat([df_targ, df_targ_eph], axis=1)
    print(df_targ_eph[["Number", "targetname", "datetime_str"]])

# %% code Ⅲ-301.
duplicated_columns_list = []
list_of_all_columns = list(df_targ_eph.columns)
for column in list_of_all_columns:
    if list_of_all_columns.count(column) > 1 and not column in duplicated_columns_list:
        duplicated_columns_list.append(column)
duplicated_columns_list

for column in duplicated_columns_list:
    list_of_all_columns[list_of_all_columns.index(column)] = column
    list_of_all_columns[list_of_all_columns.index(column)] = column + '_1'

df_targ_eph.columns = list_of_all_columns
#print(df_targ_eph.columns)
df_targ_eph.to_csv(f"{proj_dir}/{fpath.stem}_AST_Mag{Mag_UP}.csv")
df_targ_eph.dropna(subset = ['RA', 'DEC', 'V', 'RA_1', 'DEC_1', 'V_1'],
                   inplace=True)
df_targ_eph[['RA', 'DEC', 'V', 'RA_1', 'DEC_1', 'V_1']]

# %% code Ⅲ-302.
import numpy as np
pos_pix_targ_init = SkyCoord(df_targ_eph['RA']*u.deg, df_targ_eph["DEC"]*u.deg,
                        **SKYC_KW).to_pixel(wcs, origin=0, mode='wcs')
pos_pix_targ_init = np.array(pos_pix_targ_init).T
print("pos_pix_targ_init:", pos_pix_targ_init)

# %% code Ⅲ-303.
# 영상 표시 함수 znorm · zimshow · norm_imshow는 Ⅲ-04 「FITS 파일
# 다루기」에서 설명했고 dses_utils에 들어 있음(du.zimshow 등으로 부름)

# %% code Ⅲ-304.
from photutils.aperture import CircularAperture as CAp
from photutils.aperture import CircularAnnulus as CAn
import matplotlib.pyplot as plt

fig, axs = plt.subplots(1, 1, figsize=val_figsize,
                        subplot_kw={'projection': wcs},
                        sharex=False, sharey=False, gridspec_kw=None)

im = du.zimshow(axs, hdul[0].data, )
axs.set_title('World coordinate system', fontsize=9)
axs.coords.grid(True, color='white', ls=':')
axs.coords['ra'].set_axislabel('Right Ascension (J2000)', minpad=0.5,
                               fontsize=10)
axs.coords['ra'].set_ticklabel_position('bl')
axs.coords['dec'].set_axislabel('Declination (J2000)', minpad=0.4, fontsize=10)
axs.coords['dec'].set_ticklabel_position('bl')
axs.coords['ra'].set_axislabel_position('b')     # 축 이름이 겹치지 않게
axs.coords['dec'].set_axislabel_position('l')
axs.coords['ra'].set_major_formatter('hh:mm')
axs.coords['dec'].set_major_formatter('dd:mm')
axs.coords['ra'].display_minor_ticks(True)
axs.coords['dec'].display_minor_ticks(True)
axs.coords['ra'].set_minor_frequency(2)
axs.coords['dec'].set_minor_frequency(2)
axs.tick_params(labelsize=9)

if df_targ.empty:
    pass
else:
    targ_ap = CAp(pos_pix_targ_init, r=R_AP)
    targ_an = CAn(pos_pix_targ_init, r_in=R_IN, r_out=R_OUT)

    # targ_ap.plot(axs, color="r")
    targ_an.plot(axs, color="r")

    axs.annotate(f"{df_targ_eph[['Number', 'RA', 'DEC', 'V']]}",
            xy=(0, 0), xytext=(0, -0.1), xycoords='axes fraction',
            va='top', ha='left', fontsize = 8)
plt.colorbar(im, ax = axs, fraction=val_fraction, pad=0.04)
plt.suptitle(f"fname: {fpath.name}", fontsize=10)

info = (f"image center (RA, DEC): ({cent_coord.ra:.03f}, "
        f"{cent_coord.dec:.03f})\n"
        f"telescope center (RA, DEC): ({tel_coord.ra:.03f}, {tel_coord.dec:.03f})\n"
        f"offset (RA cos DEC, DEC): ({offset_RA:.03f}, {offset_DEC:.03f})\n"
        f"offset (AZ cos ALT, ALT): ({offset_AZ:.03f}, {offset_ALT:.03f})")
axs.annotate(info, xy=(0, 0), xytext=(0.6, -0.1), xycoords='axes fraction',
            va='top', ha='left', fontsize = 8)
plt.tight_layout()
plt.savefig(proj_dir / f"{fpath.stem}_AST_Mag{Mag_UP}.png")
plt.show()

# %% code Ⅲ-305.
from astropy.nddata import Cutout2D
from photutils.centroids import centroid_com
from astropy.stats import sigma_clipped_stats

# %% code Ⅲ-306.
if df_targ.empty:
    pass
else:
    cutsizes = 49
    for i, row in df_targ_eph.iterrows():
        try :
            # 1. 소행성 영역 잘라 내기
            cut_hdu = Cutout2D(
                        data = hdul[0].data,
                        position = (pos_pix_targ_init[i]),
                        size=(cutsizes, cutsizes) #CCD 영역 잘라내기
                        )
            avg, med, std = sigma_clipped_stats(cut_hdu.data)  # 기본값은 3σ, 5회 반복

            fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.8),
                        subplot_kw={'projection': wcs},
                        sharex=False, sharey=False, gridspec_kw=None)

            im0 = du.zimshow(axs[0], cut_hdu.data)
            axs[0].plot((cutsizes-1)/2, (cutsizes-1)/2, 'rx')   # 중심 인덱스(49 px → 24)
            axs[0].set_ylabel('pixels')
            axs[0].grid(ls=':')
            axs[0].set_title(f'Asteroid area image', fontsize=9)
            axs[0].annotate(   f"mean: {np.mean(cut_hdu.data):.01f}, std: {np.std(cut_hdu.data):.01f} \nmax: {np.max(cut_hdu.data):.01f}, min: {np.min(cut_hdu.data):.01f} \nNumber of Pixel: {np.shape(cut_hdu.data)[0]:.0f}x{np.shape(cut_hdu.data)[1]:.0f}",
                xy=(0, 0), xytext=(0.1, -0.30), xycoords='axes fraction',
                va='top', ha='left', fontsize=8)
            plt.colorbar(im0, ax=axs[0], label="ADU",
                        fraction=0.0455, pad=0.04)

            # 2. 중심의 dx, dy 구하기
            thresh_3sig = med + 3 * std
            mask_3sig = (cut_hdu.data < thresh_3sig)
            center = centroid_com(data = cut_hdu.data, mask = mask_3sig)

            centerdx = center[0] - ((cutsizes-1)/2)
            centerdy = center[1] - ((cutsizes-1)/2)

            axs[1].grid(ls=':')
            axs[1].set_title(f'The new center of asteroid', fontsize=9)
            im1 = axs[1].imshow(mask_3sig.astype(int), origin="lower")
            axs[1].imshow(cut_hdu.data, alpha=0.4, origin="lower")
            axs[0].plot(*center, 'rx')
            axs[1].annotate(f"center: {center[0]:.02f}, {center[1]:.02f}\ncenter dx, dy: {centerdx:.02f}, {centerdy:.02f}",
                    xy=(0, 0), xytext=(0.01, -0.30), xycoords='axes fraction',
                    va='top', ha='left', fontsize=8)

            plt.colorbar(im1, ax=axs[1], label="mask",
                        fraction=0.0455, pad=0.04)
            plt.suptitle(f"{fpath.name}\nasteroid No.{i}: {row['targetname']}, \n{row['datetime_str']}, V_mag {row['V']}",
                        fontsize=9)

            plt.tight_layout()
            plt.savefig(proj_dir / f"{fpath.stem}_AST_Mag{Mag_UP}_{i:02d}.png")
            plt.show()

        except Exception as err:
            print("Err :", err)
            continue

# %% code Ⅲ-307.
fpath2 = Path(fpaths[1])                                   # 약 3시간 20분 뒤 영상
hdul2 = fits.open(str(fpath2))
wcs2 = WCS(hdul2[0].header)
t_middle2 = (Time(hdul2[0].header["DATE-OBS"], format="isot")
             + hdul2[0].header["EXPTIME"] * u.s / 2)
dt = (t_middle2 - t_middle).to(u.hour)
print(f"첫 영상 {t_middle.isot}, 둘째 영상 {t_middle2.isot}, 간격 {dt:.2f}")

# %% code Ⅲ-308.
from photutils.centroids import centroid_sources, centroid_2dg

def measure(data, w, ra, dec):
    """예보 위치 둘레에서 소행성 중심을 찾아 하늘 좌표로 돌려줌"""
    x0, y0 = w.world_to_pixel(SkyCoord(ra * u.deg, dec * u.deg))
    _, med, _ = sigma_clipped_stats(data)
    xc, yc = centroid_sources(data - med, x0, y0, box_size=15,
                              centroid_func=centroid_2dg)
    return w.pixel_to_world(xc[0], yc[0])

rows, tracks = [], {}
for _, row in df_targ_eph.iterrows():
    cent2 = wcs2.pixel_to_world((nx - 1) / 2, (ny - 1) / 2)   # 둘째 영상 중심
    eph = small_body_ephem(row["Number"], [t_middle, t_middle2], [cent_coord, cent2])
    c1 = measure(hdul[0].data, wcs, eph["RA"][0], eph["DEC"][0])
    c2 = measure(hdul2[0].data, wcs2, eph["RA"][1], eph["DEC"][1])
    pred1 = SkyCoord(eph["RA"][0] * u.deg, eph["DEC"][0] * u.deg)
    pred2 = SkyCoord(eph["RA"][1] * u.deg, eph["DEC"][1] * u.deg)
    dra = ((c2.ra - c1.ra) * np.cos(c1.dec)).to(u.arcsec)    # 적경 방향 이동(cos δ 곱함)
    ddec = (c2.dec - c1.dec).to(u.arcsec)
    name = row["targetname"].split(" (")[0]
    tracks[name] = (c1, c2)
    rows.append({"name": name,
                 "move (arcsec)": c1.separation(c2).arcsec,
                 "RA rate meas": (dra / dt).value, "RA rate JPL": eph["RA_rate"].mean(),
                 "DEC rate meas": (ddec / dt).value, "DEC rate JPL": eph["DEC_rate"].mean(),
                 "O-C 1 (arcsec)": c1.separation(pred1).arcsec,
                 "O-C 2 (arcsec)": c2.separation(pred2).arcsec})

df_move = pd.DataFrame(rows).round(2)
df_move

# %% code Ⅲ-309.
fig, axs = plt.subplots(len(tracks), 2, figsize=(7.5, 3.4 * len(tracks)), squeeze=False)
for k, (name, (c1, c2)) in enumerate(tracks.items()):
    mid = SkyCoord((c1.ra + c2.ra) / 2, (c1.dec + c2.dec) / 2)   # 두 위치의 가운데
    for j, (h, w, here, other, t) in enumerate([(hdul, wcs, c1, c2, t_middle),
                                                (hdul2, wcs2, c2, c1, t_middle2)]):
        cut = Cutout2D(h[0].data, mid, (260, 260), wcs=w)
        ax = axs[k, j]
        du.zimshow(ax, cut.data, cmap="gray")
        for c, col in [(here, "r"), (other, "c")]:
            CAp(np.array(cut.wcs.world_to_pixel(c)), r=12).plot(ax, color=col, lw=1.2)
        ax.set_title(f"{name}  {t.isot[11:16]} UT", fontsize=11)
        ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout()
plt.savefig(proj_dir / f"asteroid_motion.png")
plt.show()
