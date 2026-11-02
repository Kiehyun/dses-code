# 지구과학 데이터 사이언스 2 | III-09. PSF 측광
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅲ-217.
fname = ("M13_LIGHT_V_2025-04-26-14-10-00_60sec_"
         "GSON300_STF-8300M_-19c_1bin_cal.fits")
fid = "1DffJFv7AKpm_7WMD1Xza4Y1RznPvJ1Dr"

du.download(f"https://drive.google.com/uc?id={fid}", proj_dir / fname)

# %% code Ⅲ-218.
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales
from astropy.coordinates import SkyCoord
import astropy.units as u

fpath = proj_dir / fname
data = fits.getdata(fpath).astype(float)
hdr = fits.getheader(fpath)
wcs = WCS(hdr)

for k in ["OBJECT", "DATE-OBS", "EXPTIME", "FILTER", "OPTIC", "CCDNAME", "NAXIS1", "NAXIS2"]:
    print(f"{k:9s} = {hdr[k]}")

plt.rcParams.update({"xtick.labelsize": 9, "ytick.labelsize": 9})   # 책 판형에 맞춘 눈금 글자 크기
gain, rdnoise = 0.37, 9.3                                  # STF-8300M (e-/ADU, e-)
pixscale = proj_plane_pixel_scales(wcs).mean() * 3600      # 화소 하나의 각크기(arcsec)
m13 = SkyCoord("16h41m41.6s", "+36d27m41s")                # M13 중심
cx, cy = wcs.world_to_pixel(m13)                           # 성단 중심의 화소 좌표
print(f"화소 축척 {pixscale:.3f} arcsec/px, 성단 중심 (x, y) = ({cx:.1f}, {cy:.1f})")

# %% code Ⅲ-219.
from astropy.visualization import simple_norm

def show(ax, img, title, percent=99.5):
    im = ax.imshow(img, origin="lower", cmap="gray",
                   norm=simple_norm(img, "asinh", percent=percent))
    ax.set_title(title, fontsize=9)
    return im

core = (slice(int(cy) - 100, int(cy) + 100), slice(int(cx) - 100, int(cx) + 100))  # 중심부 200x200 화소

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.8))
show(axs[0], data, "M13, V 60 s (1500x1500 px)")
axs[0].add_patch(plt.Rectangle((cx - 100, cy - 100), 200, 200, ec="r", fc="none"))
show(axs[1], data[core], "중심부 200x200 px", percent=99.9)
plt.tight_layout()
plt.show()

# %% code Ⅲ-220.
from astropy.stats import SigmaClip
from photutils.background import Background2D, MMMBackground

bkg = Background2D(data, (64, 64), filter_size=(3, 3),
                   sigma_clip=SigmaClip(sigma=3.0),
                   bkg_estimator=MMMBackground())          # DAOPHOT 방식 최빈값 어림
sub = data - bkg.background                               # 배경을 뺀 영상
bkg_rms = np.median(bkg.background_rms)
print(f"배경 중앙값 {np.median(bkg.background):.1f} ADU, 배경 잡음 {bkg_rms:.1f} ADU")

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4))
im0 = axs[0].imshow(bkg.background, origin="lower", cmap="viridis")
axs[0].set_title("배경 지도 (ADU)", fontsize=9)
plt.colorbar(im0, ax=axs[0], fraction=0.046, pad=0.04)
show(axs[1], sub, "배경을 뺀 영상")
plt.tight_layout()
plt.show()

# %% code Ⅲ-221.
from photutils.detection import DAOStarFinder

def xy_cols(tab):
    """photutils 버전에 따라 다른 중심 열 이름(x_centroid 또는 xcentroid)"""
    return ("x_centroid", "y_centroid") if "x_centroid" in tab.colnames else ("xcentroid", "ycentroid")

FWHM_INIT = 4.5
found0 = DAOStarFinder(threshold=4 * bkg_rms, fwhm=FWHM_INIT,
                       min_separation=1.5 * FWHM_INIT)(sub)
xc, yc = xy_cols(found0)
print("찾은 별:", len(found0))

# %% code Ⅲ-222.
from scipy.spatial import cKDTree
from photutils.psf import fit_fwhm

def isolated_bright(tab, d_iso=20, peak_rng=(1000, 30000), r_min=300, edge=20):
    """고립되고 밝지만 포화되지 않은, 성단 바깥 별의 표지(bool 배열)"""
    x, y = np.asarray(tab[xc]), np.asarray(tab[yc])
    dist, _ = cKDTree(np.c_[x, y]).query(np.c_[x, y], k=2)    # 가장 가까운 이웃까지 거리
    ny, nx = sub.shape
    return ((dist[:, 1] > d_iso)
            & (tab["peak"] > peak_rng[0]) & (tab["peak"] < peak_rng[1])
            & (np.hypot(x - cx, y - cy) > r_min)
            & (x > edge) & (x < nx - edge) & (y > edge) & (y < ny - edge))

sel = isolated_bright(found0)
fwhms = fit_fwhm(sub, xypos=np.c_[found0[xc][sel], found0[yc][sel]], fit_shape=7)
FWHM = float(np.median(fwhms))
print(f"고른 별 {sel.sum()}개, FWHM 중앙값 {FWHM:.2f} px = {FWHM * pixscale:.2f} arcsec "
      f"(16~84 백분위 {np.percentile(fwhms, 16):.2f}~{np.percentile(fwhms, 84):.2f} px)")

# %% code Ⅲ-223.
finder = DAOStarFinder(threshold=4 * bkg_rms, fwhm=FWHM, min_separation=1.5 * FWHM)
found = finder(sub)
print("FWHM 으로 다시 찾은 별:", len(found))

# %% code Ⅲ-224.
from astropy.nddata import NDData
from astropy.table import Table
from photutils.psf import extract_stars

sel = isolated_bright(found)
psf_cat = Table({"x": found[xc][sel], "y": found[yc][sel]})
stars = extract_stars(NDData(sub), psf_cat, size=19)
print("PSF 별:", len(stars))

fig, axs = plt.subplots(2, 6, figsize=(7.5, 2.9))
for ax, star in zip(axs.flat, stars):
    ax.imshow(star.data, origin="lower", cmap="viridis",
              norm=simple_norm(star.data, "log", percent=99.5))
    ax.set_xticks([]); ax.set_yticks([])
plt.suptitle("ePSF 를 만들 별(앞 12개)", fontsize=9)
plt.tight_layout()
plt.show()

# %% code Ⅲ-225.
from photutils.psf import EPSFBuilder

result = EPSFBuilder(oversampling=2, maxiters=10, progress_bar=False)(stars)
# photutils 3 은 결과 객체(.epsf), 2.x 는 (epsf, 맞춘 별) 튜플을 돌려줌
epsf = result.epsf if hasattr(result, "epsf") else result[0]
print("ePSF 격자:", epsf.data.shape, "(오버샘플링 2)")

# %% code Ⅲ-226.
from astropy.modeling.functional_models import Gaussian1D

from matplotlib.ticker import FuncFormatter
ov = 2
img = epsf.data / epsf.data.max()
n = img.shape[0]
yy, xx = np.indices(img.shape)
rr = np.hypot(xx - (n - 1) / 2, yy - (n - 1) / 2) / ov       # 원래 화소 단위 반지름
r_edges = np.arange(0, 8.25, 0.25)
r_mid = 0.5 * (r_edges[1:] + r_edges[:-1])
prof = [img[(rr >= a) & (rr < b)].mean() for a, b in zip(r_edges[:-1], r_edges[1:])]
gauss = Gaussian1D(1, 0, FWHM / 2.3548)(r_mid)

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.3))
axs[0].imshow(img, origin="lower", cmap="viridis", norm=simple_norm(img, "log", percent=99.9))
axs[0].set_title("ePSF (2배 오버샘플링)", fontsize=9)
axs[1].semilogy(r_mid, prof, "o", ms=3, label="ePSF")
axs[1].semilogy(r_mid, gauss, "-", label=f"가우스 (FWHM {FWHM:.2f} px)")
axs[1].set_ylim(1e-4, 1.5)
axs[1].yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))   # 0.001 처럼 소수로 표시
axs[1].set_xlabel("반지름 (px)"); axs[1].set_ylabel("상대 밝기")
axs[1].legend(fontsize=8); axs[1].grid(ls=":")
plt.tight_layout()
plt.show()

# %% code Ⅲ-227.
from photutils.psf import PSFPhotometry, SourceGrouper

FIT_SHAPE = (7, 7)
grouper = SourceGrouper(min_separation=2.5 * FWHM)
psfphot = PSFPhotometry(epsf, FIT_SHAPE, grouper=grouper,
                        aperture_radius=FWHM,                 # 밝기 초깃값을 잴 구경
                        xy_bounds=(2, 2), group_warning_threshold=1000)

init = Table({"x": found[xc], "y": found[yc], "flux": found["flux"]})
error = np.sqrt(np.clip(sub + bkg.background, 0, None) / gain + (rdnoise / gain)**2)  # 화소 오차(ADU)
psf_tab = psfphot(sub, error=error, init_params=init)

gsize = np.asarray(psf_tab["group_size"])
print("맞춘 별:", len(psf_tab))
print("묶음으로 함께 맞춘 별:", (gsize > 1).sum(), "/ 가장 큰 묶음:", gsize.max(), "개")
print("품질 표시(flags)가 붙은 별:", (np.asarray(psf_tab["flags"]) > 0).sum())
psf_tab["id", "group_id", "group_size", "x_fit", "y_fit", "flux_fit", "flux_err", "qfit", "flags"][:5]

# %% code Ⅲ-228.
resid = psfphot.make_residual_image(sub, psf_shape=(19, 19))
model = sub - resid

outer = (slice(1250, 1450), slice(1250, 1450))                    # 바깥쪽 200x200 화소
fig, axs = plt.subplots(2, 3, figsize=(7.5, 5.2))
for row, (reg, name) in enumerate([(core, "중심부"), (outer, "바깥쪽")]):
    vmin, vmax = -3 * bkg_rms, 15 * bkg_rms
    for col, (img, ttl) in enumerate([(sub, "원본"), (model, "PSF 모형"), (resid, "잔차")]):
        axs[row, col].imshow(img[reg], origin="lower", cmap="gray", vmin=vmin, vmax=vmax)
        axs[row, col].set_title(f"{name}: {ttl}", fontsize=9)
        axs[row, col].set_xticks([]); axs[row, col].set_yticks([])
    print(f"{name}: 원본 표준편차 {np.std(sub[reg]):6.1f}, 잔차 표준편차 {np.std(resid[reg]):6.1f} ADU "
          f"(배경 잡음 {bkg_rms:.1f})")
plt.tight_layout()
plt.show()

# %% code Ⅲ-229.
from photutils.psf import CircularGaussianPRF

gpsf = CircularGaussianPRF(fwhm=FWHM)
gpsf.fwhm.fixed = True                                     # FWHM 은 고정, 위치·밝기만 맞춤
init_iso = Table({"x": psf_cat["x"], "y": psf_cat["y"], "flux": found["flux"][sel]})
phot_g = PSFPhotometry(gpsf, FIT_SHAPE, aperture_radius=FWHM)
phot_e = PSFPhotometry(epsf, FIT_SHAPE, aperture_radius=FWHM)
tab_g = phot_g(sub, init_params=init_iso)
tab_e = phot_e(sub, init_params=init_iso)
res_g = phot_g.make_residual_image(sub, psf_shape=(19, 19))
res_e = phot_e.make_residual_image(sub, psf_shape=(19, 19))
print(f"qfit 중앙값  가우스 {np.median(tab_g['qfit']):.3f}, ePSF {np.median(tab_e['qfit']):.3f}")
dm_ge = -2.5 * np.log10(np.asarray(tab_g["flux_fit"]) / np.asarray(tab_e["flux_fit"]))
print(f"등급 차 (가우스 - ePSF) 중앙값 {np.median(dm_ge):+.3f} mag")

# 별마다 잔차를 밝기로 나눠 잘라 낸 뒤 중앙값으로 겹침(잡음을 줄여 공통 무늬만 남김)
def stack_cut(img, tab, h=9):
    cuts = []
    for row in tab:
        x0, y0 = int(round(row["x_fit"])), int(round(row["y_fit"]))
        c = img[y0 - h:y0 + h + 1, x0 - h:x0 + h + 1]
        if c.shape == (2 * h + 1, 2 * h + 1):
            cuts.append(c / row["flux_fit"])
    return np.median(cuts, axis=0)

st = stack_cut(sub, tab_e)
lim = 0.03 * st.max()                                       # 봉우리의 3%
fig, axs = plt.subplots(1, 3, figsize=(7.5, 2.7))
axs[0].imshow(st, origin="lower", cmap="viridis")
axs[0].set_title("별(겹친 영상)", fontsize=9)
for ax, r, t, ttl in [(axs[1], res_g, tab_g, "가우스 잔차"), (axs[2], res_e, tab_e, "ePSF 잔차")]:
    im = ax.imshow(stack_cut(r, t), origin="lower", cmap="RdBu_r", vmin=-lim, vmax=lim)
    ax.set_title(ttl, fontsize=9)
for ax in axs: ax.set_xticks([]); ax.set_yticks([])
plt.colorbar(im, ax=axs[2], fraction=0.046, pad=0.04)
plt.tight_layout()
plt.show()

# %% code Ⅲ-230.
from photutils.aperture import CircularAperture, aperture_photometry

ok = (np.asarray(psf_tab["flags"]) == 0) & (np.asarray(psf_tab["flux_fit"]) > 0)
pt = psf_tab[ok]
xf, yf = np.asarray(pt["x_fit"]), np.asarray(pt["y_fit"])
R_AP = 1.5 * FWHM
ap_tab = aperture_photometry(sub, CircularAperture(np.c_[xf, yf], r=R_AP))

m_psf = -2.5 * np.log10(np.asarray(pt["flux_fit"]))
with np.errstate(invalid="ignore"):
    m_ap = -2.5 * np.log10(np.asarray(ap_tab["aperture_sum"]))
dm = m_ap - m_psf
dnn = cKDTree(np.c_[xf, yf]).query(np.c_[xf, yf], k=2)[0][:, 1]   # 가장 가까운 이웃 거리
r_cl = np.hypot(xf - cx, yf - cy)                                  # 성단 중심 거리

iso = (dnn > 3 * R_AP) & (m_psf < -10) & np.isfinite(dm)           # 고립된 밝은 별
crowd = (dnn < 2 * R_AP) & np.isfinite(dm)                          # 구경이 이웃과 겹치는 별
ap_corr = np.median(dm[iso])
print(f"고립된 밝은 별 {iso.sum()}개: Δm 중앙값 {ap_corr:+.3f} (흩어짐 {np.std(dm[iso]):.3f}) mag")
print(f"이웃과 붙은 별 {crowd.sum()}개: Δm 중앙값 {np.median(dm[crowd]):+.3f} mag")

# %% code Ⅲ-231.
fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4))
for ax, xv, xl in [(axs[0], m_psf, "PSF 기기 등급"), (axs[1], r_cl * pixscale / 60, "성단 중심 거리 (arcmin)")]:
    ax.plot(xv[~crowd], dm[~crowd], ".", ms=3, color="C0", label="떨어진 별")
    ax.plot(xv[crowd], dm[crowd], ".", ms=4, color="C3", label=f"이웃 < {2 * R_AP:.0f} px")
    ax.axhline(ap_corr, color="k", lw=0.8, ls="--", label="고립된 별의 중앙값")
    ax.set_xlabel(xl); ax.set_ylim(0.8, -1.2); ax.grid(ls=":")
axs[0].set_ylabel(r"$m_{\rm ap} - m_{\rm PSF}$")
axs[0].legend(fontsize=7, loc="lower left")
plt.tight_layout()
plt.show()

# %% code Ⅲ-232.
from photutils.aperture import CircularAperture

gid = pt["group_id"][np.argmax(np.where(r_cl < 150, np.asarray(pt["group_size"]), 0))]
g = np.asarray(pt["group_id"]) == gid
gx, gy = xf[g].mean(), yf[g].mean()
h = 22
box = (slice(int(gy) - h, int(gy) + h + 1), slice(int(gx) - h, int(gx) + h + 1))
ox, oy = int(gx) - h, int(gy) - h

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.6))
vmin, vmax = -3 * bkg_rms, sub[box].max()
axs[0].imshow(sub[box], origin="lower", cmap="gray", norm=simple_norm(sub[box], "asinh", percent=99.8))
CircularAperture(np.c_[xf[g] - ox, yf[g] - oy], r=R_AP).plot(axs[0], color="orange", lw=1)
axs[0].plot(xf[g] - ox, yf[g] - oy, "c+", ms=8)
axs[0].set_title(f"묶음 {gid}: 별 {g.sum()}개", fontsize=9)
axs[1].imshow(resid[box], origin="lower", cmap="gray", vmin=-3 * bkg_rms, vmax=15 * bkg_rms)
axs[1].set_title("PSF 모형을 뺀 잔차", fontsize=9)
for ax in axs:
    ax.set_xlim(-0.5, 2 * h + 0.5); ax.set_ylim(-0.5, 2 * h + 0.5)
    ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout()
plt.show()

print(" 별   x       y     m_PSF   m_ap-보정   차이")
for k in np.flatnonzero(g):
    print(f"{pt['id'][k]:4d} {xf[k]:7.1f} {yf[k]:7.1f} {m_psf[k]:7.3f} {m_ap[k] - ap_corr:8.3f} {m_ap[k] - ap_corr - m_psf[k]:+8.3f}")

# %% code Ⅲ-233.
from photutils.psf import IterativePSFPhotometry

itphot = IterativePSFPhotometry(epsf, FIT_SHAPE, finder=finder, grouper=grouper,
                                aperture_radius=FWHM, xy_bounds=(2, 2),
                                maxiters=3, mode="new", group_warning_threshold=1000)
it_tab = itphot(sub, error=error)
n_iter = np.bincount(np.asarray(it_tab["iter_detected"]))[1:]
print("되풀이마다 찾은 별:", n_iter.tolist(), "→ 모두", len(it_tab))
resid_it = itphot.make_residual_image(sub, psf_shape=(19, 19))
print(f"중심부 잔차 표준편차: 한 번 {np.std(resid[core]):.1f} → 되풀이 {np.std(resid_it[core]):.1f} ADU")

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.6))
for ax, r, ttl in [(axs[0], resid, "한 번 맞춘 잔차"), (axs[1], resid_it, "세 번 되풀이한 잔차")]:
    ax.imshow(r[core], origin="lower", cmap="gray", vmin=-3 * bkg_rms, vmax=15 * bkg_rms)
    ax.set_title(ttl, fontsize=9); ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout()
plt.show()

# %% code Ⅲ-234.
out = pt["id", "group_id", "group_size", "x_fit", "y_fit", "flux_fit", "flux_err", "qfit", "cfit"].to_pandas()
out["mag_psf"] = m_psf
out["merr_psf"] = 1.0857 * out["flux_err"] / out["flux_fit"]
out["mag_ap"] = m_ap
out["dnn_px"] = dnn
ra_dec = wcs.pixel_to_world(xf, yf)
out["ra"], out["dec"] = ra_dec.ra.deg, ra_dec.dec.deg
csv = proj_dir / f"{fpath.stem}_PSF_photometry.csv"
out.to_csv(csv, index=False)
print(csv.relative_to(proj_dir.parent), len(out), "행")
out.head()
