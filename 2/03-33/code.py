# 지구과학 데이터 사이언스 2 | III-13. 차등 측광과 소행성 광도 곡선
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 382.
import shutil

fname = "925ALPHONSINA_V_2016-11-08_RiLA600_reduced.zip"
fid = "1MTFCA4uXo3HpsJ0tYeawIwTWVpQinHyQ"
du.download(f"https://drive.google.com/uc?id={fid}", proj_dir / fname)
shutil.unpack_archive(str(proj_dir / fname), str(proj_dir))   # 압축 풀기

# %% code 383.
fpaths = du.list_files(proj_dir, "fit*")

# %% code 384.
import re
from pathlib import Path
import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from photutils.aperture import CircularAperture as CAp
from photutils.aperture import CircularAnnulus as CAn

fpath = Path(fpaths[0])                      # 첫 영상
hdul = fits.open(str(fpath), unit="adu")
hdr = hdul[0].header
flt = hdr["FILTER"]                          # 영상의 필터(이 데이터는 V)
for _k in ["NAXIS1", "NAXIS2", "DATE-OBS", "EXPTIME", "OBJECT", "FILTER", "CCDNAME"]:
    print(f"{_k:9s} = {hdr[_k]}")

# CCD 사양(헤더의 CCDNAME으로 고름)
if hdr["CCDNAME"] == "STF-8300M":
    gain, rdnoise = 0.37, 9.3
elif hdr["CCDNAME"] == "STX-16803":
    gain, rdnoise = 1.27, 9.0

# 구경 · 고리 반지름(Ⅲ-08과 같음): FWHM 어림값의 배수
FWHM_INIT = 6
R_AP, R_IN, R_OUT = 1.5 * FWHM_INIT, 4 * FWHM_INIT, 6 * FWHM_INIT

wcs = WCS(hdr)
SKYC_KW = dict(unit=u.deg, frame="icrs")
Suwon = EarthLocation(lon=127.005 * u.deg, lat=37.308889 * u.deg, height=101 * u.m)
observatory_code = "P64"
OBJID = str(int(re.match(r"\d+", fpath.name).group()))   # 파일 이름 앞의 소행성 번호(0000925 -> 925)
print("gain, rdnoise :", gain, rdnoise, "/ 소행성 번호 :", OBJID)

# %% code 385.
from astroquery.jplhorizons import Horizons
from astroquery.mpc import MPC

def asteroid_ephem(objid, times):
    """소행성의 예보 위치(Horizons, 응답하지 않으면 MPC 천체력을 1분 간격으로 받아 보간)"""
    try:
        eph = Horizons(id=objid, id_type="smallbody", location=observatory_code,
                       epochs=list(times.jd)).ephemerides().to_pandas()
        return eph[["targetname", "datetime_str", "RA", "DEC"]]
    except Exception as e:                       # 서버 오류 등
        print(f"Horizons 응답 없음({type(e).__name__}) → MPC 천체력으로 대신 조회")
        t0 = Time(times[0].isot[:16])            # 첫 시각의 분 단위 내림
        n = int(np.ceil((times[-1] - t0).to_value(u.min))) + 2
        eph = MPC.get_ephemeris(objid, location=observatory_code, start=t0,
                                step=1 * u.min, number=n)
        dt = (Time(eph["Date"]) - t0).to_value(u.min)
        x = (times - t0).to_value(u.min)
        return pd.DataFrame({"targetname": f"{objid} " + hdr["OBJECT"].split("-", 1)[-1].title(),   # 0000925-ALPHONSINA -> Alphonsina
                             "datetime_str": times.isot,
                             "RA": np.interp(x, dt, eph["RA"]),
                             "DEC": np.interp(x, dt, eph["Dec"])})

# 모든 영상의 노출 중앙 시각과 그 시각의 소행성 예보 위치
t_mids = []
for f in fpaths:
    h = fits.getheader(f)
    t_mids.append(Time(h["DATE-OBS"], format="isot") + h["EXPTIME"] * u.s / 2)
t_mids = Time(t_mids)
ny, nx = hdul[0].data.shape
img_center = wcs.pixel_to_world((nx - 1) / 2, (ny - 1) / 2)   # 영상 중심
eph_all = asteroid_ephem(OBJID, t_mids)
# 소행성 방향의 대기질량(고도에서 계산)
altaz = SkyCoord(eph_all["RA"].values * u.deg, eph_all["DEC"].values * u.deg, **SKYC_KW)\
    .transform_to(AltAz(obstime=t_mids, location=Suwon))
eph_all["airmass"] = altaz.secz.value

# 첫 영상에서의 픽셀 좌표와 밤사이 지나간 길
xt, yt = wcs.world_to_pixel(SkyCoord(eph_all["RA"].values, eph_all["DEC"].values, **SKYC_KW))
targ_ap = CAp((xt[0], yt[0]), r=R_AP)
targ_an = CAn((xt[0], yt[0]), r_in=R_IN, r_out=R_OUT)
print(f"영상 {len(fpaths)}장, {t_mids[0].isot[11:16]} ~ {t_mids[-1].isot[11:16]} UT")
print(f"{eph_all['targetname'][0]}: 첫 영상 (x, y) = ({xt[0]:.1f}, {yt[0]:.1f}), "
      f"밤사이 움직인 거리 {np.hypot(xt[-1] - xt[0], yt[-1] - yt[0]):.0f} px")

# %% code 386.
from astroquery.vizier import Vizier

# 영상을 모두 덮는 원(중심 · 반지름) 안의 PS1 별을 받음
corners = wcs.pixel_to_world([-0.5, nx - 0.5, -0.5, nx - 0.5], [-0.5, -0.5, ny - 0.5, ny - 0.5])
rad = img_center.separation(corners).max().to(u.deg)
base = "g" if flt == "B" else "r"           # 영상 필터에 가까운 PS1 등급(B -> g, 그 밖 -> r)
vquery = Vizier(columns=["**", "+_r"], row_limit=-1, timeout=300,
                column_filters={f"{base}mag": "11.0..15.0", f"e_{base}mag": "<0.10"})
q = vquery.query_region(img_center, radius=rad, catalog="II/349/ps1")[0]
print(f"PS1   : {len(q)} (반지름 {rad:.3f})")

q = du.select_in_fov(q, wcs, hdul[0].data.shape, bezel=5 * FWHM_INIT)   # 가장자리 30 px 안쪽
q = du.drop_ps1_flags(q, drop_by_kron=True)                             # 품질 깃발 · 은하
q = du.drop_star_groups(q, crit_sep=6 * FWHM_INIT)                      # 36 px 안의 쌍
q = du.add_jc_mags(q)                                                   # g, r -> B, V, R

# 소행성이 지나간 길에서 2 * R_OUT 안에 드는 별 빼기
d_track = np.hypot(np.subtract.outer(np.asarray(q["x"]), xt),
                   np.subtract.outer(np.asarray(q["y"]), yt)).min(axis=1)
print(f"track : {len(q)} -> {(d_track > 2 * R_OUT).sum()} ({2 * R_OUT:.0f} px)")
df_stars = q[d_track > 2 * R_OUT].to_pandas()

# %% code 387.
from astropy.stats import sigma_clip
from photutils.aperture import ApertureStats

xy = np.c_[df_stars["x"], df_stars["y"]]
ph = du.apphot_annulus(hdul[0].data, CAp(xy, r=R_AP), CAn(xy, r_in=R_IN, r_out=R_OUT),
                       gain=gain, rdnoise=rdnoise)
dm = ph["mag"].to_numpy() - df_stars[f"{flt}mag"].to_numpy()   # 별마다의 m - M
peak = ApertureStats(hdul[0].data, CAp(xy, r=R_AP)).max
good = (ph["merr"].to_numpy() < 0.1) & (peak < 40000) & np.isfinite(dm)
print(f"후보 {len(df_stars)}개 -> 오차 · 포화 조건 {good.sum()}개", end="")
clip = sigma_clip(dm[good], sigma=3, maxiters=5, cenfunc="median", stdfunc="mad_std")
good[np.flatnonzero(good)[clip.mask]] = False
comp_ids = np.flatnonzero(good)                                 # 비교성(df_stars의 행 번호)
print(f" -> 3σ 클리핑 뒤 비교성 {len(comp_ids)}개")
z0 = np.median(dm[good])
print(f"첫 영상: 영점 Z = {z0:.3f}, 비교성 잔차의 표준편차 {np.std(dm[good] - z0, ddof=1):.3f} mag, "
      f"{flt} 등급 {df_stars.loc[comp_ids, f'{flt}mag'].min():.1f} ~ {df_stars.loc[comp_ids, f'{flt}mag'].max():.1f}")

# %% code 388.
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6.4, 5.6), subplot_kw={"projection": wcs})
du.zimshow(ax, hdul[0].data, cmap="gray")
ax.plot(xt, yt, ":", color="c", lw=1.5, label="소행성이 지나간 길")
targ_an.plot(ax=ax, color="r", lw=1)
targ_ap.plot(ax=ax, color="b", lw=1)
CAp(xy[~good], r=R_IN).plot(ax=ax, color="0.6", lw=0.8)
CAp(xy[good], r=R_IN).plot(ax=ax, color="orange", lw=1)
for n in comp_ids:
    ax.text(xy[n, 0] + 20, xy[n, 1] + 20, n, color="orange", fontsize=7)
ax.coords["ra"].set_axislabel("Right Ascension (J2000)", fontsize=9.5)
ax.coords["dec"].set_axislabel("Declination (J2000)", fontsize=9.5)
ax.coords["ra"].set_ticklabel(size=9)
ax.coords["dec"].set_ticklabel(size=9)
ax.set_title(f"925 Alphonsina와 비교성 ({flt}, {t_mids[0].isot[:16]} UT)", fontsize=11)
from matplotlib.lines import Line2D
ring = dict(ls="", marker="o", mfc="none", ms=8)
handles = [Line2D([], [], ls=":", color="c", label="소행성이 지나간 길"),
           Line2D([], [], color="b", label="소행성(첫 영상)", **ring),
           Line2D([], [], color="orange", label="비교성", **ring),
           Line2D([], [], color="0.6", label="뺀 후보", **ring)]
ax.legend(handles=handles, loc="lower left", fontsize=8)
plt.tight_layout()
plt.show()

# %% code 389.
from astropy.io import fits

def phot_frame(fpath, ra, dec, ids):
    """영상 한 장에서 소행성(ra, dec)과 비교성(df_stars의 행 ids)을 구경 측광"""
    data = fits.getdata(fpath).astype(float)
    w = WCS(fits.getheader(fpath))
    x0, y0 = w.world_to_pixel(SkyCoord(ra * u.deg, dec * u.deg, **SKYC_KW))
    pt = du.apphot_annulus(data, CAp([x0, y0], r=R_AP), CAn([x0, y0], r_in=R_IN, r_out=R_OUT),
                           gain=gain, rdnoise=rdnoise)
    c = df_stars.loc[ids]
    xs, ys = w.world_to_pixel(SkyCoord(c["RAJ2000"].values * u.deg, c["DEJ2000"].values * u.deg, **SKYC_KW))
    ps = du.apphot_annulus(data, CAp(np.c_[xs, ys], r=R_AP), CAn(np.c_[xs, ys], r_in=R_IN, r_out=R_OUT),
                           gain=gain, rdnoise=rdnoise)
    ps.index = list(ids)
    return pt.iloc[0], ps

def zero_point(ps, ids):
    """비교성 ids의 (기기 등급 - 표준 등급) 중앙값과 그 표준 오차, 쓴 별 수"""
    dm = ps.loc[ids, "mag"].to_numpy() - df_stars.loc[ids, f"{flt}mag"].to_numpy()
    dm = dm[np.isfinite(dm)]
    zp = np.median(dm)
    return zp, np.std(dm - zp, ddof=1) / np.sqrt(len(dm)), len(dm)

# 점검성: 첫 영상에서 소행성과 밝기가 가장 비슷한 비교성
pt0, _ = phot_frame(fpaths[0], eph_all["RA"][0], eph_all["DEC"][0], comp_ids)
chk = comp_ids[np.argmin(np.abs(df_stars.loc[comp_ids, f"{flt}mag"].to_numpy() - (pt0["mag"] - z0)))]
ens_ids = comp_ids[comp_ids != chk]                 # 영점(앙상블)에 쓰는 비교성
print(f"점검성 {chk}번 ({flt} = {df_stars.loc[chk, f'{flt}mag']:.2f}), 앙상블 비교성 {len(ens_ids)}개")

rows = []
for f, t, (_, e) in zip(fpaths, t_mids, eph_all.iterrows()):
    pt, ps = phot_frame(f, e["RA"], e["DEC"], comp_ids)
    zp, e_zp, n = zero_point(ps, ens_ids)
    rows.append({"utc": t.isot[11:19], "jd": t.jd,
                 flt: pt["mag"] - zp, f"e_{flt}": np.hypot(pt["merr"], e_zp),
                 "check": ps.loc[chk, "mag"] - zp, "e_check": np.hypot(ps.loc[chk, "merr"], e_zp),
                 "zeropt": zp, "e_zeropt": e_zp, "n_comp": n, "airmass": e["airmass"]})
df_lc = pd.DataFrame(rows)
df_lc.to_csv(proj_dir / f"925_Alphonsina_{flt}_lightcurve.csv", index=False)
df_lc.round(3)

# %% code 390.
hours = (df_lc["jd"] - df_lc["jd"].iloc[0]) * 24          # 첫 영상부터 지난 시간
fig, axs = plt.subplots(3, 1, figsize=(7.5, 6.4), sharex=True,
                        gridspec_kw={"height_ratios": [2.2, 1, 1]})
axs[0].errorbar(hours, df_lc[flt], yerr=df_lc[f"e_{flt}"], fmt="o", ms=4, capsize=2)
axs[0].invert_yaxis()
axs[0].set_ylabel(f"{flt} (mag)", fontsize=11)
axs[0].set_title(f"925 Alphonsina, 2016-11-08 ({t_mids[0].isot[11:16]} UT 부터)", fontsize=12)
dchk = df_lc["check"] - df_lc["check"].mean()
axs[1].errorbar(hours, dchk, yerr=df_lc["e_check"], fmt="s", ms=3, color="C2", capsize=2)
axs[1].set_ylim(0.15, -0.15)
axs[1].set_ylabel("점검성 (mag)", fontsize=11)
axs[2].plot(hours, df_lc["zeropt"], "s", ms=3, color="C1")
axs[2].set_ylabel("영점 (mag)", fontsize=11)
ax2 = axs[2].twinx()
ax2.plot(hours, df_lc["airmass"], "-", color="gray")
ax2.set_ylabel("대기질량", fontsize=11)
axs[2].set_xlabel("시간 (h)", fontsize=11)
for ax in [*axs, ax2]:
    ax.tick_params(labelsize=9)
for ax in axs:
    ax.grid(ls=":")
plt.tight_layout()
plt.show()

v = df_lc[flt]
print(f"소행성: {v.min():.2f} ~ {v.max():.2f} (변광 폭 {v.max() - v.min():.2f} mag), "
      f"등급 오차 중앙값 {df_lc[f'e_{flt}'].median():.3f} mag")
print(f"점검성: 표준편차 {df_lc['check'].std(ddof=1):.3f} mag, 등급 오차 중앙값 {df_lc['e_check'].median():.3f} mag")
print(f"영점: {df_lc['zeropt'].min():.3f} ~ {df_lc['zeropt'].max():.3f} (폭 {df_lc['zeropt'].max() - df_lc['zeropt'].min():.2f} mag), "
      f"대기질량 {df_lc['airmass'].min():.2f} ~ {df_lc['airmass'].max():.2f}")

# %% code 391.
from astropy.timeseries import LombScargle

t_h, mag, emag = hours.to_numpy(), df_lc[flt].to_numpy(), df_lc[f"e_{flt}"].to_numpy()
ls = LombScargle(t_h, mag, emag)
freq, power = ls.autopower(minimum_frequency=1 / 20, maximum_frequency=1 / 2, samples_per_peak=50)
P_half = 1 / freq[np.argmax(power)]               # 가장 높은 봉우리의 주기(h)
P_rot = 2 * P_half                                # 자전 주기 = 두 배
print(f"주기도의 가장 높은 봉우리 {P_half:.2f} h -> 자전 주기 {P_rot:.2f} h")

# 자전 주기로 접기: 위상 0~1, 두 배음 사인 곡선(nterms=2)으로 모양을 맞춤
phase = (t_h / P_rot) % 1
ls2 = LombScargle(t_h, mag, emag, nterms=2)
ph_fit = np.linspace(0, 1, 200)
m_fit = ls2.model(ph_fit * P_rot, 1 / P_rot)

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.2))
axs[0].plot(1 / freq, power, color="steelblue")
axs[0].axvline(P_half, color="r", ls="--", lw=1, label=f"봉우리 {P_half:.2f} h")
axs[0].set_xlabel("주기 (h)", fontsize=11)
axs[0].set_ylabel("세기", fontsize=11)
axs[0].set_title("롬-스카글 주기도", fontsize=12)
axs[0].legend(fontsize=8)
axs[1].errorbar(phase, mag, yerr=emag, fmt="o", ms=3, capsize=2)
axs[1].plot(ph_fit, m_fit, "r-", lw=1)
axs[1].invert_yaxis()
axs[1].set_xlabel(f"위상 (P = {P_rot:.2f} h)", fontsize=11)
axs[1].set_ylabel(f"{flt} (mag)", fontsize=11)
axs[1].set_title("자전 주기로 접은 광도 곡선", fontsize=12)
for ax in axs:
    ax.tick_params(labelsize=9)
    ax.grid(ls=":")
plt.tight_layout()
plt.show()
