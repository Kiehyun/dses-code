# 지구과학 데이터 사이언스 2 | III-05. CCD 관측 데이터 전처리
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 130.
fname = "ccd_preprocessing_STX-16803_2016-12-09.zip"
fid = "15TgCCi0aA-V7NHZxId-YyV7IaejVHlGK"

# 저자의 구글 드라이브에 공유한 파일을 내려받음(안에서 gdown 사용)
du.download(f"https://drive.google.com/uc?id={fid}", proj_dir / fname)

# %% code 131.
from pathlib import Path

# 마스터 프레임과 보정한 영상을 저장할 폴더(이미 있으면 그대로 둠)
MASTERDIR = proj_dir / "master_files"
MASTERDIR.mkdir(parents=True, exist_ok=True)
REDUCEDDIR = proj_dir / "reduced_files"
REDUCEDDIR.mkdir(parents=True, exist_ok=True)
print(MASTERDIR, REDUCEDDIR)

# %% code 132.
import shutil

# 내려받은 압축 파일 찾기
fpaths = du.list_files(proj_dir, "zip")

try:
    shutil.unpack_archive(str(fpaths[0]), str(proj_dir))
    print(f"{str(fpaths[0])} is unpacked to {str(proj_dir)}")
except Exception as e:
    print(f"Error unpacking {str(fpaths[0])}: {e}")

# %% code 133.
fpaths = du.list_files(proj_dir, "fit*")

# %% code 134.
from astropy.io import fits

fpath = Path(fpaths[0])
data, hdr = fits.getdata(fpath, header=True)    # 영상 배열과 헤더를 함께 읽음
print(fpath.name)
for k in ["NAXIS1", "NAXIS2", "DATE-OBS", "EXPTIME", "OBJECT", "FILTER"]:
    if k in hdr:
        print(f"{k:9s} = {hdr[k]}")
print(f"data : {type(data).__name__}, {data.dtype}, {data.shape}, 평균 {data.mean():.1f} ADU")

# %% code 135.
bias_list = du.list_files(proj_dir, pattern="BIAS_*.fit*")

# %% code 136.
fpath = bias_list[0]
print(fpath)
import numpy as np
import matplotlib.pyplot as plt

from astropy.io import fits
hdul = fits.open(fpath)

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = axs[0].imshow(hdul[0].data, origin='lower', cmap='viridis')

im2 = du.zimshow(axs[1], hdul[0].data, cmap='viridis')

axs[0].set_title(f'{fpath.name}', fontsize=10)
axs[1].set_title('zimshow', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {hdul[0].data.min()}, Mean value: {hdul[0].data.mean():.02f}, Max value: {hdul[0].data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 137.
from ccdproc import combine

method = "median"

bias = combine(bias_list,       # ccdproc은 numpy 배열이 아니라 파이썬 리스트만 받음
               method = method,         # 기본값이 average라서 median으로 지정
               unit='adu')

print("type(bias) :", type(bias))

# %% code 138.
import textwrap
public = [a for a in dir(bias) if not a.startswith("_")]   # 밑줄로 시작하는 내부용 이름은 빼기
print(f"공개 속성 · 메서드 {len(public)}개 :")
print(textwrap.fill(", ".join(public), width=76))
print("type(bias.data) :", type(bias.data))

# %% code 139.
print("bias.data.dtype :", type(bias.data.dtype))
bias.data = bias.data.astype(np.float32)
print("bias.data.dtype :", type(bias.data.dtype))

# %% code 140.
def show_image_hist(data, title, hist_frac=0.1, bins=50):
    """왼쪽에 zscale 영상, 오른쪽에 화소값 히스토그램, 그림 아래에 최솟값 · 평균 · 최댓값을 그립니다.

    hist_frac: 히스토그램 가로 범위를 평균의 ±몇 배로 할지(0.1이면 ±10%). None이면 전체 범위.
    """
    data = np.asarray(data, dtype=float)
    fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4))
    im = du.zimshow(axs[0], data, origin="lower", cmap="viridis")
    rng = None if hist_frac is None else (data.mean() * (1 - hist_frac), data.mean() * (1 + hist_frac))
    axs[1].hist(data.ravel(), bins=bins, range=rng)
    axs[0].set_title(title, fontsize=10)
    axs[1].set_title("Histogram of pixel values", fontsize=10)
    plt.colorbar(im, ax=axs[0], fraction=0.0455, pad=0.04)
    fig.text(0.5, 0.02, f"Min value: {data.min():.2f}, Mean value: {data.mean():.2f}, "
             f"Max value: {data.max():.2f}", ha="center", fontsize=9)   # 그림 아래 가운데
    plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
    plt.show()

# %% code 141.
show_image_hist(bias.data, "The master bias by median combine", hist_frac=None)

# %% code 142.
show_image_hist(bias.data, "The master bias by median combine")

# %% code 143.
fpath = bias_list[0]
print(fpath)
show_image_hist(fits.getdata(fpath), "The bias image (one file)")

# %% code 144.
import matplotlib.patches as patches
from astropy.nddata import Cutout2D

def plot_image_with_cutouts(all_data, cutsizes=101, location=500):
    """영상 전체와 네 모서리(가장자리에서 location 화소 안쪽)를 잘라 함께 그립니다.
    Ⅲ-04의 같은 이름 함수와 달리 파일 경로 대신 2차원 배열을 받습니다."""
    fig_set = plt.figure(figsize=(7.5, 3.8))

    def add_subplot(position, data, title):
        ax = plt.subplot2grid((2,4), position, fig=fig_set)
        im = du.zimshow(ax, data, origin='lower')
        ax.set_ylabel('pixels')
        ax.grid(ls=':')
        ax.set_title(title, fontsize=9)
        plt.colorbar(im, ax=ax, fraction=0.0455, pad=0.04)
        return im

    def add_rectangle(x, y, label):
        # Cutout2D는 (x, y)를 가운데 두고 자르므로 네모도 가운데에 맞춤
        rect = patches.Rectangle((x - cutsizes/2, y - cutsizes/2), cutsizes, cutsizes,
                                 linewidth=1, edgecolor='r', facecolor='none')
        ax1.add_patch(rect)
        ax1.text(x, y, label)

 # 전체 이미지
    ax1 = plt.subplot2grid((2,4), (0,0), colspan=2, rowspan=2, fig=fig_set)
    im1 = du.zimshow(ax1, all_data, origin='lower', cmap='viridis')
    ax1.set_title('The whole image', fontsize=9)
    plt.colorbar(im1, ax=ax1, fraction=0.0455, pad=0.04)

 # 4개의 부분 이미지
    positions = [(0,2), (0,3), (1,2), (1,3)]
    corners = [(location, all_data.shape[0] - location),
               (all_data.shape[1] - location, all_data.shape[0] - location),
               (location, location),
               (all_data.shape[1] - location, location),
               ]

    for i, (pos, corner) in enumerate(zip(positions, corners), 1):
        cut_hdu = Cutout2D(data=all_data, position=corner,
                           size=(cutsizes, cutsizes))
        add_subplot(pos, cut_hdu.data, f'{i}/4 image area')
        add_rectangle(corner[0], corner[1], f"{i}/4")

    plt.tight_layout()
    plt.show()

# %% code 145.
# 함수 사용 예
plot_image_with_cutouts(bias.data)

# %% code 146.
dark_list = du.list_files(proj_dir, pattern="DARK_*.fit*")

# %% code 147.
dark_150sec_list = du.list_files(proj_dir, pattern="DARK_*_150sec_*.fit*")

# %% code 148.
import numpy as np
from ccdproc import combine

method = "median"

dark0_150sec = combine(dark_150sec_list,       # ccdproc은 numpy 배열이 아니라 파이썬 리스트만 받음
                        method = method,         # 기본값이 average라서 median으로 지정
                        unit = 'adu')

# float32로 변환
dark0_150sec.data = dark0_150sec.data.astype(np.float32)

# %% code 149.
dark0_150sec.write(f"{MASTERDIR}/master_dark0_150sec_{method}.fits",
                   overwrite =True)
print(f"{MASTERDIR}/master_dark0_150sec_{method}.fits is created...")

# %% code 150.
# 30초 다크도 150초와 같은 방법으로 합성해 저장
dark_30sec_list = du.list_files(proj_dir, pattern="DARK_*_30sec_*.fit*")
dark0_30sec = combine(dark_30sec_list, method = method, unit = 'adu')
dark0_30sec.data = dark0_30sec.data.astype(np.float32)

dark0_30sec.write(f"{MASTERDIR}/master_dark0_30sec_{method}.fits",
                   overwrite =True)
print(f"{MASTERDIR}/master_dark0_30sec_{method}.fits is created...")

# %% code 151.
show_image_hist(dark0_150sec.data, "The master dark0_150sec by median combine")

# %% code 152.
show_image_hist(dark0_30sec.data, "The master dark0_30sec by median combine")

# %% code 153.
fpath = dark_150sec_list[0]
print(fpath)
show_image_hist(fits.getdata(fpath), "The dark image 150sec (one file)")

# %% code 154.
fpath = dark_30sec_list[0]
print(fpath)
show_image_hist(fits.getdata(fpath), "The dark image 30sec (one file)")

# %% code 155.
from ccdproc import CCDData, ccd_process
# 바이어스 빼기
dark_150sec = ccd_process(dark0_150sec, master_bias = bias)
dark_30sec = ccd_process(dark0_30sec, master_bias = bias)

dark_150sec.data = dark_150sec.data.astype(np.float32)
dark_30sec.data = dark_30sec.data.astype(np.float32)

# %% code 156.
show_image_hist(dark_150sec.data, "The master dark_150sec by median combine")

# %% code 157.
show_image_hist(dark_30sec.data, "The master dark_30sec by median combine")

# %% code 158.
# 저장
dark_150sec.write(f"{MASTERDIR}/master_dark_150sec_{method}.fits",
                  overwrite =True)
print(f"{(MASTERDIR)}/master_dark_150sec_{method}.fits is created...")

dark_30sec.write(f"{(MASTERDIR)}/master_dark_30sec_{method}.fits",
                  overwrite =True)
print(f"{(MASTERDIR)}/master_dark_30sec_{method}.fits is created...")

# %% code 159.
plot_image_with_cutouts(dark_150sec.data)

# %% code 160.
flat_list = du.list_files(proj_dir, pattern="FLAT_V_*.fit*")

# %% code 161.
flat0 = combine(flat_list,       # ccdproc은 numpy 배열이 아니라 파이썬 리스트만 받음
               method='median',         # 기본값이 average라서 median으로 지정
               unit='adu')

# float32로 변환
flat0.data = flat0.data.astype(np.float32)

# %% code 162.
# FITS 파일로 저장
flat0.write(f"{MASTERDIR}/master_flat0_{method}.fits", overwrite =True)
print(f"{MASTERDIR}/master_flat0_{method}.fits is created...")

# %% code 163.
show_image_hist(flat0.data, "The master flat0 by median combine", hist_frac=0.3)

# %% code 164.
fpath = flat_list[0]
print(fpath)
show_image_hist(fits.getdata(fpath), "The flat image (one file)")

# %% code 165.
import astropy.units as u

# 플랫마다 바이어스와 다크를 뺌(다크는 플랫의 노출 시간에 맞춰 줄임)
flat_ccds = []
for fpath in flat_list:
    ccd = CCDData.read(str(fpath), unit="adu")
    ccd = ccd_process(ccd,                       # 플랫 한 장
                      master_bias = bias,        # 마스터 바이어스
                      dark_frame = dark_30sec,   # 노출 시간이 가장 가까운 30초 다크
                      exposure_key='exptime',    # 노출 시간이 적힌 헤더 키워드
                      exposure_unit=u.s,         # 노출 시간의 단위
                      dark_scale=True)           # 다크를 플랫의 노출 시간에 맞춤
    flat_ccds.append(ccd)

# 밝기가 다른 플랫을 같은 수준(중앙값들의 중앙값)으로 맞춘 뒤 중앙값 합성
levels = np.array([np.median(c.data) for c in flat_ccds])
print("플랫마다 중앙값(ADU):", np.round(levels).astype(int))
flat = combine(flat_ccds, method="median", scale=np.median(levels) / levels)

# float32로 변환
flat.data = flat.data.astype(np.float32)

flat.write(f"{MASTERDIR}/master_flat_{method}.fits", overwrite =True)
print(f"{MASTERDIR}/master_flat_{method}.fits is created...")

# %% code 166.
show_image_hist(flat.data, "The master flat by median combine", hist_frac=0.2)

# %% code 167.
plot_image_with_cutouts(flat.data)

# %% code 168.
flat_norm = flat.copy()
flat_norm.data = flat.data/np.median(flat.data)   # 중앙값 = 1

flat_norm.write(f"{MASTERDIR}/master_flat_norm_{method}.fits", overwrite =True)
print(f"{(MASTERDIR)}/master_flat_norm_{method}.fits is created...")

# %% code 169.
show_image_hist(flat_norm.data, "The master normalized flat by median combine", hist_frac=0.2)

# %% code 170.
object_BLCAM_list = du.list_files(proj_dir, pattern="BL-CAM*.fit*")

# %% code 171.
# 노출 시간이 같은 150초 다크를 쓰므로 크기 조정(dark scale) 없이 그대로 뺌
from ccdproc import CCDData, ccd_process, flat_correct
import astropy.units as u

for fpath in object_BLCAM_list:
    obj = CCDData.read(str(fpath), unit='adu')
    reduced = ccd_process(obj,                         # 입력 이미지
                          master_bias = bias,          # 마스터 바이어스
                          dark_frame = dark_150sec,    # 노출 시간이 같은(150초) 다크
                          exposure_key = 'exptime',    # 노출 시간 키워드
                          exposure_unit = u.s,         # 노출 시간 단위
                          )
    # 플랫 나누기: norm_value를 주지 않으면 플랫을 평균으로 다시 나누므로 중앙값(=1)을 직접 줌
    reduced = flat_correct(reduced, flat_norm, norm_value=np.median(flat_norm.data))
    reduced.data = reduced.data.astype(np.float32)   # 실수형으로 저장(음수도 그대로 유지)
    reduced.write(f"{REDUCEDDIR}/reduced_{fpath.name}", overwrite =True)
    print(f"{REDUCEDDIR}/reduced_{fpath.name} is created...")

# %% code 172.
fpath = object_BLCAM_list[0]
print(fpath)
show_image_hist(fits.getdata(fpath), "Before preprocessing")

# %% code 173.
reduced_fpath = REDUCEDDIR / f"reduced_{fpath.name}"
print(reduced_fpath)
hdul_af = fits.open(str(reduced_fpath))
show_image_hist(hdul_af[0].data, "After preprocessing (No dark scale)")

# %% code 174.
from ccdproc import CCDData, ccd_process, flat_correct
import astropy.units as u

for fpath in object_BLCAM_list:
    obj = CCDData.read(str(fpath), unit='adu')
    reduced_darksc = ccd_process(obj,                    # 입력 이미지
                          master_bias = bias,        # 마스터 바이어스
                          dark_frame = dark_30sec,  # 노출 시간이 다른(30초) 다크
                          exposure_key = 'exptime',  # 노출 시간 키워드
                          exposure_unit = u.s,       # 노출 시간 단위
                          dark_scale = True,         # 다크 프레임 크기를 맞출지 여부
                          )
    # 플랫 나누기: 중앙값(=1)으로 정규화한 플랫을 그대로 씀
    reduced_darksc = flat_correct(reduced_darksc, flat_norm,
                                  norm_value=np.median(flat_norm.data))
    reduced_darksc.data = reduced_darksc.data.astype(np.float32)
    reduced_darksc.write(f"{REDUCEDDIR}/reduced_darksc_{fpath.name}",
                         overwrite =True)
    print(f"{REDUCEDDIR}/reduced_darksc_{fpath.name} is created... (median: {np.median(reduced_darksc.data):.1f})")

# %% code 175.
fpath = object_BLCAM_list[0]
reduced_darksc_fpath = REDUCEDDIR / f"reduced_darksc_{fpath.name}"
print(reduced_darksc_fpath)
hdul_af_darksc = fits.open(str(reduced_darksc_fpath))
show_image_hist(hdul_af_darksc[0].data, "After preprocessing (dark scale)")

# %% code 176.
# 두 보정 결과(150초 다크 vs 30초 다크를 늘려 씀)의 차이를 수치로 비교
diff = hdul_af_darksc[0].data - hdul_af[0].data
print(f"보정 결과 중앙값 (150초 다크)      : {np.median(hdul_af[0].data):.1f} ADU")
print(f"보정 결과 중앙값 (30초 다크 scale) : {np.median(hdul_af_darksc[0].data):.1f} ADU")
print(f"두 결과의 차이 중앙값 / 표준편차   : {np.median(diff):.2f} / {np.std(diff):.2f} ADU")
from astropy.stats import sigma_clipped_stats
sky = (slice(300, 700), slice(1300, 1700))         # 별이 적은 하늘 영역
print(f"하늘 영역 잡음 (150초 다크)        : {sigma_clipped_stats(hdul_af[0].data[sky])[2]:.1f} ADU")
print(f"하늘 영역 잡음 (30초 다크 scale)   : {sigma_clipped_stats(hdul_af_darksc[0].data[sky])[2]:.1f} ADU")

# 바이어스를 뺀 다크의 값이 노출 시간에 비례하는지 확인
m150, m30 = np.median(dark_150sec.data), np.median(dark_30sec.data)
print(f"다크 중앙값  150초: {m150:.2f} ADU, 30초: {m30:.2f} ADU")
print(f"30초 값이 노출에 비례한다면 150초 다크의 중앙값: {m30*150/30:.2f} ADU")

# %% code 177.
plot_image_with_cutouts(hdul_af[0].data)

# %% code 178.
plot_image_with_cutouts(hdul_af_darksc[0].data)

# %% code 179.
import pandas as pd
import astropy.units as u
from astropy.io import fits
from ccdproc import CCDData, combine, ccd_process, subtract_bias, flat_correct

# %% code 180.
KEYS = ("IMAGETYP", "OBJECT", "EXPTIME", "FILTER")

def make_summary(fpaths, keys=KEYS):
    rows = []
    for fpath in fpaths:
        hdr = fits.getheader(fpath)       # 헤더만 읽기
        row = {"file": str(fpath)}
        for key in keys:
            row[key] = hdr.get(key)       # 헤더에 없으면 None
        rows.append(row)
    return pd.DataFrame(rows)

summary = make_summary(du.list_files(proj_dir, "fit*", show=False))
print("len(summary):", len(summary))
summary

# %% code 181.
bias_files = summary.loc[summary["IMAGETYP"] == "BIAS", "file"].tolist()
print("len(bias_files):", len(bias_files))

mbias = combine(bias_files, method="median", unit="adu")
mbias.data = mbias.data.astype(np.float32)

fname = MASTERDIR / "master_bias.fits"
mbias.write(fname, overwrite=True)
print(f"{fname} is created...")

# %% code 182.
dark_df = summary.loc[summary["IMAGETYP"] == "DARK"]
mdarks = {}                         # 노출 시간 -> 마스터 다크

for exptime, group in dark_df.groupby("EXPTIME"):
    mdark = combine(group["file"].tolist(), method="median", unit="adu")
    mdark = subtract_bias(mdark, mbias)        # 바이어스를 뺀 다크
    mdark.data = mdark.data.astype(np.float32)

    fname = MASTERDIR / f"master_dark_{exptime:.0f}sec.fits"
    mdark.write(fname, overwrite=True)
    mdarks[exptime] = mdark
    print(f"{fname} is created... ({len(group)} files)")

# %% code 183.
flat_df = summary.loc[summary["IMAGETYP"] == "FLAT"]
print("len(flat_df):", len(flat_df))
flat_df

# %% code 184.
mflats = {}                          # 필터 -> 마스터 플랫(정규화 전)

for filt, group in flat_df.groupby("FILTER"):
    ccds = [ccd_process(CCDData.read(f, unit="adu"),
                        master_bias=mbias,          # 바이어스 빼기
                        dark_frame=mdarks[30.0],    # 다크 빼기
                        exposure_key="exptime",     # 노출 시간 키워드
                        exposure_unit=u.s,          # 노출 시간 단위
                        dark_scale=True)            # 노출 시간에 맞춰 줄임
            for f in group["file"]]
    levels = np.array([np.median(c.data) for c in ccds])
    mflat = combine(ccds, method="median",
                    scale=np.median(levels) / levels)   # 밝기 수준을 맞춰 합성
    mflat.data = mflat.data.astype(np.float32)

    fname = MASTERDIR / f"master_flat_{filt.upper()}.fits"
    mflat.write(fname, overwrite=True)
    mflats[filt] = mflat
    print(f"{fname} is created... ({len(group)} files)")

# %% code 185.
mflats_norm = {}                     # 필터 -> 정규화한 마스터 플랫

for filt, mflat in mflats.items():
    mflat_norm = mflat.copy()
    mflat_norm.data = mflat.data / np.median(mflat.data)   # 중앙값 = 1

    fname = MASTERDIR / f"master_flat_{filt.upper()}_norm.fits"
    mflat_norm.write(fname, overwrite=True)
    mflats_norm[filt] = mflat_norm
    print(f"{fname} is created... (median: {np.median(mflat.data):.1f})")

# %% code 186.
df_light = summary.loc[summary["IMAGETYP"] == "LIGHT"]
df_light_bl = df_light.loc[df_light["OBJECT"] == "BL-CAM"]
df_light_bl = df_light_bl.reset_index(drop=True)
print("len(df_light_bl):", len(df_light_bl))

for _, row in df_light_bl.iterrows():
    fpath = Path(row["file"])
    ccd = CCDData.read(fpath, unit="adu")
    filt = ccd.header["FILTER"]
    expt = ccd.header["EXPTIME"]
    red = ccd_process(ccd,
                      master_bias=mbias,
                      dark_frame=mdarks[expt],        # 노출 시간이 같은 다크
                      exposure_key="exptime",
                      exposure_unit=u.s,
                      dark_scale=False)               # 기본값 False
    flat_n = mflats_norm[filt]                          # 필터가 같은 플랫
    red = flat_correct(red, flat_n, norm_value=np.median(flat_n.data))  # 중앙값 정규화 유지
    red.data = red.data.astype(np.float32)

    fname = REDUCEDDIR / f"red_auto_{fpath.name}"
    red.write(fname, overwrite=True)
    print(f"{fname} is created... (median: {np.median(red.data):.1f})")

# %% code 187.
for _, row in df_light_bl.iterrows():
    fpath = Path(row["file"])
    ccd = CCDData.read(fpath, unit="adu")
    filt = ccd.header["FILTER"]
    red = ccd_process(ccd,
                      master_bias=mbias,
                      dark_frame=mdarks[30.0],       # 노출 시간이 다른 다크
                      exposure_key="exptime",
                      exposure_unit=u.s,
                      dark_scale=True)                # 노출 시간에 맞춤
    flat_n = mflats_norm[filt]                          # 필터가 같은 플랫
    red = flat_correct(red, flat_n, norm_value=np.median(flat_n.data))  # 중앙값 정규화 유지
    red.data = red.data.astype(np.float32)

    fname = REDUCEDDIR / f"red_auto_darksc_{fpath.name}"
    red.write(fname, overwrite=True)
    print(f"{fname} is created... (median: {np.median(red.data):.1f})")

# %% code 188.
df_light_tt = df_light.loc[df_light["OBJECT"] == "TT-ARI"].reset_index(drop=True)
print("len(df_light_tt):", len(df_light_tt))

reduced_tt = []
for _, row in df_light_tt.iterrows():
    fpath = Path(row["file"])
    ccd = CCDData.read(fpath, unit="adu")
    red = ccd_process(ccd,
                      master_bias=mbias,
                      dark_frame=mdarks[ccd.header["EXPTIME"]],   # 30초 다크
                      exposure_key="exptime",
                      exposure_unit=u.s,
                      dark_scale=False)
    flat_n = mflats_norm[ccd.header["FILTER"]]          # 필터가 같은 플랫
    red = flat_correct(red, flat_n, norm_value=np.median(flat_n.data))
    red.data = red.data.astype(np.float32)
    fname = REDUCEDDIR / f"red_auto_{fpath.name}"
    red.write(fname, overwrite=True)
    reduced_tt.append(red)
    print(f"{fname.name} (median: {np.median(red.data):.1f})")

fig, axs = plt.subplots(1, len(reduced_tt), figsize=(7.5, 2.0))
for ax, red, (_, row) in zip(axs, reduced_tt, df_light_tt.iterrows()):
    du.zimshow(ax, red.data)
    ax.set_title(red.header["DATE-OBS"][11:19] + " UT", fontsize=9)   # 세계시
    ax.set_xticks([]); ax.set_yticks([])
plt.suptitle("TT Ari, V 30 s (bias, dark 30 s, flat)", fontsize=11)
plt.tight_layout()
plt.show()
