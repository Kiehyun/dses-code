# 지구과학 데이터 사이언스 2 | III-05. CCD 관측 데이터 전처리
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 127.
fname = "ccd_preprocessing_STX-16803_2016-12-09.zip"
fid = "10M1bSJtK1kYirN_43EzvcksaYnjPatbq"

# 저자의 구글 드라이브에 공유한 파일을 내려받음(안에서 gdown 사용)
du.download(f"https://drive.google.com/uc?id={fid}", proj_dir / fname)

# %% code 128.
import os
from pathlib import Path
if not (proj_dir).exists():
    os.mkdir(str(proj_dir))
    print (f"{str(proj_dir)} is created...")
else : 
    print (f"{str(proj_dir)} already exists...")

MASTERDIR = proj_dir / "master_files"
MASTERDIR.mkdir(parents=True, exist_ok=True)
REDUCEDDIR = proj_dir / "reduced_files"
REDUCEDDIR.mkdir(parents=True, exist_ok=True)

# %% code 129.
import shutil

# 내려받은 압축 파일 찾기
fpaths = du.list_files(proj_dir, "zip")

try:
    shutil.unpack_archive(str(fpaths[0]), str(proj_dir))
    print(f"{str(fpaths[0])} is unpacked to {str(proj_dir)}")
except Exception as e:
    print(f"Error unpacking {str(fpaths[0])}: {e}")

# %% code 130.
from zipfile import ZipFile
with ZipFile(str(fpaths[0]), 'r') as zip_ref:
    zip_ref.extractall(str(proj_dir))
    print(str(fpaths[0]), "is unpacked to", str(proj_dir))

# %% code 131.
fpaths = du.list_files(proj_dir, "fit*")

# %% code 132.
from astropy.io import fits

fpath = Path(fpaths[0])
print(f"fpath: {fpath}")
print(f"type(fpath): {type(fpath)}")

hdul = fits.open(str(fpath), unit="adu")

print("type(hdul) :", type(hdul))
print("type(hdul[0]) :", type(hdul[0]))

# %% code 133.
print("type(hdul[0].header) :", type(hdul[0].header))
for _k in ["NAXIS1", "NAXIS2", "DATE-OBS", "EXPTIME", "OBJECT", "FILTER"]:
    if _k in hdul[0].header:
        print(f"{_k:9s} = {hdul[0].header[_k]}")

# %% code 134.
print("hdul[0].header['DATE-OBS'] :", hdul[0].header['DATE-OBS'])
print("type(hdul[0].header['DATE-OBS']) :", type(hdul[0].header['DATE-OBS']))

# %% code 135.
print("type(hdul[0].data) :", type(hdul[0].data))
print("hdul[0].data.dtype :", hdul[0].data.dtype)
print("hdul[0].data.shape :", hdul[0].data.shape)
print("hdul[0].data :", hdul[0].data)

# %% code 136.
bias_list = du.list_files(proj_dir, pattern="BIAS_*.fit*")

# %% code 137.
# 영상 표시 함수 znorm · zimshow · norm_imshow는 Ⅲ-04 「FITS 파일 다루기」에서 설명했고 dses_utils에 들어 있음
from astropy.visualization import ImageNormalize, LinearStretch, ZScaleInterval, simple_norm

# %% code 138.
fpath = bias_list[0]
print(fpath)
import numpy as np
import matplotlib.pyplot as plt

from astropy.io import fits
hdul = fits.open(fpath)

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = axs[0].imshow(hdul[0].data,
            origin='lower',
            cmap='viridis',
                    )

im2 = du.zimshow(axs[1],
            hdul[0].data,
            cmap='viridis',
            )

axs[0].set_title(f'{fpath.name}', fontsize=10)
axs[1].set_title('zimshow', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {hdul[0].data.min()}, Mean value: {hdul[0].data.mean():.02f}, Max value: {hdul[0].data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 139.
from ccdproc import combine

method = "median"

bias = combine(bias_list,       # ccdproc은 numpy 배열이 아니라 파이썬 리스트만 받음
               method = method,         # 기본값이 average라서 median으로 지정
               unit='adu')

print("type(bias) :", type(bias))

# %% code 140.
import textwrap
public = [a for a in dir(bias) if not a.startswith("_")]   # 밑줄로 시작하는 내부용 이름은 빼기
print(f"공개 속성 · 메서드 {len(public)}개 :")
print(textwrap.fill(", ".join(public), width=76))
print("type(bias.data) :", type(bias.data))

# %% code 141.
print("bias.data.dtype :", type(bias.data.dtype))
bias.data = bias.data.astype(np.float32)
print("bias.data.dtype :", type(bias.data.dtype))

# %% code 142.
import os
from pathlib import Path
if not (proj_dir).exists():
    os.mkdir(str(proj_dir))
    print (f"{str(proj_dir)} is created...")
else : 
    print (f"{str(proj_dir)} already exists...")

MASTERDIR = proj_dir / "master_files"
MASTERDIR.mkdir(parents=True, exist_ok=True)
REDUCEDDIR = proj_dir / "reduced_files"
REDUCEDDIR.mkdir(parents=True, exist_ok=True)

# %% code 143.
fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = du.zimshow(axs[0], bias.data,
            origin='lower',)

im2 = axs[1].hist(bias.data,
                )

axs[0].set_title(f'The master bias by median combine', fontsize=10)
axs[1].set_title('The histrogram of pixel value', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {bias.data.min()}, Mean value: {bias.data.mean():.02f}, Max value: {bias.data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 144.
fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = du.zimshow(axs[0],
            bias.data,
            cmap='viridis',
            origin='lower',)

im2 = axs[1].hist(bias.data,
                  range=(bias.data.mean()*.9, bias.data.mean()*1.1),
                  )

axs[0].set_title(f'The master bias by median combine', fontsize=10)
axs[1].set_title('The histrogram of pixel value', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {bias.data.min()}, Mean value: {bias.data.mean():.02f}, Max value: {bias.data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 145.
fpath = bias_list[0]
print(fpath)
hdul = fits.open(fpath)

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = du.zimshow(axs[0],
            hdul[0].data,
            cmap='viridis',
            origin='lower',)

im2 = axs[1].hist(hdul[0].data,
                  range=(hdul[0].data.mean()*.9, hdul[0].data.mean()*1.1),
                  )

axs[0].set_title(f'The bias image (one file)', fontsize=10)
axs[1].set_title('The histrogram of pixel value', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {hdul[0].data.min()}, Mean value: {hdul[0].data.mean():.02f}, Max value: {hdul[0].data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 146.
import numpy as np
from astropy.nddata import Cutout2D

fig_set = plt.figure(figsize=(7.5, 3.8))

ax1 = plt.subplot2grid((2,4), (0,0),
                    colspan=2, rowspan=2,
                    fig=fig_set)
im1 = du.zimshow(ax1,
            bias.data,
            origin='lower',
            cmap='viridis',
            )
plt.colorbar(im1,
             ax = ax1,
             fraction=0.0455, pad=0.04)

cutsizes = 101
# 1/4 영역
ax20 = plt.subplot2grid((2,4), (0,2),
                       fig=fig_set)

cut_hdu = Cutout2D(
            data = bias.data,
            position = (500, 500),
            size=(cutsizes, cutsizes)  # CCD 영역 잘라 내기
            )
im20 = du.zimshow(ax20,
        cut_hdu.data,
        origin='lower',
        cmap='viridis',
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
            data = bias.data,
            position = (bias.data.shape[1] - 500, 500),
            size=(cutsizes, cutsizes)  # CCD 영역 잘라 내기
            )
im21 = du.zimshow(ax21,
        cut_hdu.data,
        origin='lower',
        cmap='viridis',
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
            data = bias.data,
            position = (500, bias.data.shape[0] - 500),
            size=(cutsizes, cutsizes)  # CCD 영역 잘라 내기
            )
im30 = du.zimshow(ax30,
        cut_hdu.data,
        origin='lower',
        cmap='viridis',
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
            data = bias.data,
            position = (bias.data.shape[1] - 500, bias.data.shape[0] - 500),
            size=(cutsizes, cutsizes)  # CCD 영역 잘라 내기
            )
im31 = du.zimshow(ax31,
        cut_hdu.data,
        origin='lower',
        cmap='viridis',
    )
ax31.set_ylabel('pixels')
ax31.grid(ls=':')
ax31.set_title(f'4/4 image area', fontsize=9)
plt.colorbar(im31,
            ax=ax31,
            fraction=0.0455, pad=0.04)

plt.tight_layout()
plt.show()

# %% code 147.
import matplotlib.patches as patches

def plot_image_with_cutouts(all_data, cutsizes=101):
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
        rect = patches.Rectangle((x, y), cutsizes,
                                cutsizes, linewidth=1,
                                edgecolor='r', facecolor='none')
        ax1.add_patch(rect)
        ax1.text(x, y, label)

 # 전체 이미지
    ax1 = plt.subplot2grid((2,4), (0,0), colspan=2, rowspan=2, fig=fig_set)
    im1 = du.zimshow(ax1, all_data, origin='lower', cmap='viridis')
    ax1.set_title('The whole image', fontsize=9)
    plt.colorbar(im1, ax=ax1, fraction=0.0455, pad=0.04)

 # 4개의 부분 이미지
    positions = [(0,2), (0,3), (1,2), (1,3)]
    corners = [(500, all_data.shape[0] - 500),
                (all_data.shape[1] - 500, all_data.shape[0] - 500),
                (500, 500),
                (all_data.shape[1] - 500, 500),
                ]

    for i, (pos, corner) in enumerate(zip(positions, corners), 1):
        cut_hdu = Cutout2D(data=all_data, position=corner,
                           size=(cutsizes, cutsizes))
        add_subplot(pos, cut_hdu.data, f'{i}/4 image area')
        add_rectangle(corner[0], corner[1], f"{i}/4")

    plt.tight_layout()
    plt.show()

# 함수 사용 예
# plot_image_with_cutouts(bias.data)

# %% code 148.
# 함수 사용 예
plot_image_with_cutouts(bias.data)

# %% code 149.
dark_list = du.list_files(proj_dir, pattern="DARK_*.fit*")

# %% code 150.
dark_150sec_list = du.list_files(proj_dir, pattern="DARK_*_150sec_*.fit*")

# %% code 151.
import numpy as np
from ccdproc import combine

method = "median"

dark0_150sec = combine(dark_150sec_list,       # ccdproc은 numpy 배열이 아니라 파이썬 리스트만 받음
                        method = method,         # 기본값이 average라서 median으로 지정
                        unit = 'adu')

# float32로 변환
dark0_150sec.data = dark0_150sec.data.astype(np.float32)

# %% code 152.
dark0_150sec.write(f"{MASTERDIR}/master_dark0_150sec_{method}.fits",
                   overwrite =True)
print(f"{MASTERDIR}/master_dark0_150sec_{method}.fits is created...")

# %% code 153.
import os
from pathlib import Path
if not (proj_dir).exists():
    os.mkdir(str(proj_dir))
    print (f"{str(proj_dir)} is created...")
else : 
    print (f"{str(proj_dir)} already exists...")

MASTERDIR = proj_dir / "master_files"
MASTERDIR.mkdir(parents=True, exist_ok=True)
REDUCEDDIR = proj_dir / "reduced_files"
REDUCEDDIR.mkdir(parents=True, exist_ok=True)

# 30초 다크도 150초와 같은 방법으로 합성해 저장
dark_30sec_list = du.list_files(proj_dir, pattern="DARK_*_30sec_*.fit*")
dark0_30sec = combine(dark_30sec_list, method = method, unit = 'adu')
dark0_30sec.data = dark0_30sec.data.astype(np.float32)

dark0_30sec.write(f"{MASTERDIR}/master_dark0_30sec_{method}.fits",
                   overwrite =True)
print(f"{MASTERDIR}/master_dark0_30sec_{method}.fits is created...")

# %% code 154.
fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = du.zimshow(axs[0],
            dark0_150sec.data,
            origin='lower',
            cmap='viridis',
            )

im2 = axs[1].hist(dark0_150sec.data,
                range=(dark0_150sec.data.mean()*.9,
                       dark0_150sec.data.mean()*1.1),
                )

axs[0].set_title(f'The master dark0_150sec by median combine', fontsize=10)
axs[1].set_title('The histrogram of pixel value', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {dark0_150sec.data.min()}, Mean value: {dark0_150sec.data.mean():.02f}, Max value: {dark0_150sec.data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 155.
fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = du.zimshow(axs[0],
            dark0_30sec.data,
            origin='lower',
            cmap='viridis',
            )

im2 = axs[1].hist(dark0_30sec.data,
                range=(dark0_30sec.data.mean()*.9,
                       dark0_30sec.data.mean()*1.1),
                )

axs[0].set_title(f'The master dark0_30sec by median combine', fontsize=10)
axs[1].set_title('The histrogram of pixel value', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {dark0_30sec.data.min()}, Mean value: {dark0_30sec.data.mean():.02f}, Max value: {dark0_30sec.data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 156.
fpath = dark_150sec_list[0]
print(fpath)
hdul = fits.open(fpath)

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = du.zimshow(axs[0],
            hdul[0].data,
            cmap='viridis',
            origin='lower',)

im2 = axs[1].hist(hdul[0].data,
                  range=(hdul[0].data.mean()*.9, hdul[0].data.mean()*1.1),
                  )

axs[0].set_title(f'The dark image 150sec(one file)', fontsize=10)
axs[1].set_title('The histrogram of pixel value', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {hdul[0].data.min()}, Mean value: {hdul[0].data.mean():.02f}, Max value: {hdul[0].data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 157.
fpath = dark_30sec_list[0]
print(fpath)
hdul = fits.open(fpath)

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = du.zimshow(axs[0],
            hdul[0].data,
            cmap='viridis',
            origin='lower',)

im2 = axs[1].hist(hdul[0].data,
                  range=(hdul[0].data.mean()*.9, hdul[0].data.mean()*1.1),
                  )

axs[0].set_title(f'The dark image 30sec(one file)', fontsize=10)
axs[1].set_title('The histrogram of pixel value', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {hdul[0].data.min()}, Mean value: {hdul[0].data.mean():.02f}, Max value: {hdul[0].data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 158.
from ccdproc import CCDData, ccd_process
# 바이어스 빼기
dark_150sec = ccd_process(dark0_150sec, master_bias = bias)
dark_30sec = ccd_process(dark0_30sec, master_bias = bias)

dark_150sec.data = dark_150sec.data.astype(np.float32)
dark_30sec.data = dark_30sec.data.astype(np.float32)

# %% code 159.
fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = du.zimshow(axs[0],
            dark_150sec.data,
            origin='lower',
            cmap='viridis',
            )

im2 = axs[1].hist(dark_150sec.data,
            range=(dark_150sec.data.mean()*.9, dark_150sec.data.mean()*1.1),
            )

axs[0].set_title(f'The master dark_150sec by median combine', fontsize=10)
axs[1].set_title('The histrogram of pixel value', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {dark_150sec.data.min()}, Mean value: {dark_150sec.data.mean():.02f}, Max value: {dark_150sec.data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 160.
fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = du.zimshow(axs[0],
            dark_30sec.data,
            origin='lower',
            cmap='viridis',
            )

im2 = axs[1].hist(dark_30sec.data,
            range=(dark_30sec.data.mean()*.9, dark_30sec.data.mean()*1.1),
            )

axs[0].set_title(f'The master dark_30sec by median combine', fontsize=10)
axs[1].set_title('The histrogram of pixel value', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {dark_30sec.data.min()}, Mean value: {dark_30sec.data.mean():.02f}, Max value: {dark_30sec.data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 161.
# 저장
dark_150sec.write(f"{MASTERDIR}/master_dark_150sec_{method}.fits",
                  overwrite =True)
print(f"{(MASTERDIR)}/master_dark_150sec_{method}.fits is created...")

dark_30sec.write(f"{(MASTERDIR)}/master_dark_30sec_{method}.fits",
                  overwrite =True)
print(f"{(MASTERDIR)}/master_dark_30sec_{method}.fits is created...")

# %% code 162.
plot_image_with_cutouts(dark_150sec.data)

# %% code 163.
flat_list = du.list_files(proj_dir, pattern="FLAT_V_*.fit*")

# %% code 164.
flat0 = combine(flat_list,       # ccdproc은 numpy 배열이 아니라 파이썬 리스트만 받음
               method='median',         # 기본값이 average라서 median으로 지정
               unit='adu')

# float32로 변환
flat0.data = flat0.data.astype(np.float32)

# %% code 165.
# FITS 파일로 저장
flat0.write(f"{MASTERDIR}/master_flat0_{method}.fits", overwrite =True)
print(f"{MASTERDIR}/master_flat0_{method}.fits is created...")

# %% code 166.
fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = du.zimshow(axs[0], flat0.data,
            origin='lower',
            cmap='viridis',
            )

im2 = axs[1].hist(flat0.data,
                range=(flat0.data.mean()*.7, flat0.data.mean()*1.3),
                )

axs[0].set_title(f'The master flat0 by median combine', fontsize=10)
axs[1].set_title('The histrogram of pixel value', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {flat0.data.min()}, Mean value: {flat0.data.mean():.02f}, Max value: {flat0.data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 167.
fpath = flat_list[0]
print(fpath)
hdul = fits.open(fpath)

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = du.zimshow(axs[0],
            hdul[0].data,
            cmap='viridis',
            origin='lower',)

im2 = axs[1].hist(hdul[0].data,
                  range=(hdul[0].data.mean()*.9, hdul[0].data.mean()*1.1),
                  )

axs[0].set_title(f'The flat image (one file)', fontsize=10)
axs[1].set_title('The histrogram of pixel value', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {hdul[0].data.min()}, Mean value: {hdul[0].data.mean():.02f}, Max value: {hdul[0].data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 168.
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

# %% code 169.
fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = du.zimshow(axs[0], flat.data,
            origin='lower',
            cmap='viridis',
            )

im2 = axs[1].hist(flat.data,
                range=(flat.data.mean()*.8, flat.data.mean()*1.2),
                )

axs[0].set_title(f'The master Flat by median combine', fontsize=10)
axs[1].set_title('The histrogram of pixel value', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {flat.data.min():.02f}, Mean value: {flat.data.mean():.02f}, Max value: {flat.data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 170.
plot_image_with_cutouts(flat.data)

# %% code 171.
flat_norm = flat.copy()
flat_norm.data = flat.data/np.median(flat.data)   # 중앙값 = 1

flat_norm.write(f"{MASTERDIR}/master_flat_norm_{method}.fits", overwrite =True)
print(f"{(MASTERDIR)}/master_flat_norm_{method}.fits is created...")

# %% code 172.
fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = du.zimshow(axs[0], flat_norm.data,
            origin='lower',
            cmap='viridis',
            )

im2 = axs[1].hist(flat_norm.data,
                range=(flat_norm.data.mean()*.8, flat_norm.data.mean()*1.2),
                )

axs[0].set_title(f'The master nomalized Flat by median combine', fontsize=10)
axs[1].set_title('The histrogram of pixel value', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {flat_norm.data.min():.02f}, Mean value: {flat_norm.data.mean():.02f}, Max value: {flat_norm.data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 173.
object_BLCAM_list = du.list_files(proj_dir, pattern="BL-CAM*.fit*")

# %% code 174.
import os
from pathlib import Path
if not (proj_dir).exists():
    os.mkdir(str(proj_dir))
    print (f"{str(proj_dir)} is created...")
else : 
    print (f"{str(proj_dir)} already exists...")

MASTERDIR = proj_dir / "master_files"
MASTERDIR.mkdir(parents=True, exist_ok=True)
REDUCEDDIR = proj_dir / "reduced_files"
REDUCEDDIR.mkdir(parents=True, exist_ok=True)

# 노출 시간이 같은 150초 다크를 쓰므로 크기 조정(dark scale) 없이 그대로 뺌
from ccdproc import CCDData, ccd_process
import astropy.units as u

for fpath in object_BLCAM_list:
    obj = CCDData.read(str(fpath), unit='adu')
    reduced = ccd_process(obj,                         # 입력 이미지
                          master_bias = bias,          # 마스터 바이어스
                          dark_frame = dark_150sec,    # 노출 시간이 같은(150초) 다크
                          master_flat = flat_norm,     # 바이어스·다크를 빼고 정규화한 플랫
                          exposure_key = 'exptime',    # 노출 시간 키워드
                          exposure_unit = u.s,         # 노출 시간 단위
                          )
    reduced.data = reduced.data.astype(np.float32)   # 실수형으로 저장(음수도 그대로 유지)
    reduced.write(f"{REDUCEDDIR}/reduced_{fpath.name}", overwrite =True)
    print(f"{REDUCEDDIR}/reduced_{fpath.name} is created...")

# %% code 175.
fpath = object_BLCAM_list[0]
print(fpath)
hdul_bf = fits.open(fpath)

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = du.zimshow(axs[0], hdul_bf[0].data,
            origin='lower',
            cmap='viridis',
            )

im2 = axs[1].hist(hdul_bf[0].data,
                range=(hdul_bf[0].data.mean()*.9, hdul_bf[0].data.mean()*1.1),
                )

axs[0].set_title(f'Before preprocessing', fontsize=10)
axs[1].set_title('The histrogram of pixel value', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {hdul_bf[0].data.min()}, Mean value: {hdul_bf[0].data.mean():.02f}, Max value: {hdul_bf[0].data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 176.
reduced_fpath = REDUCEDDIR/f"reduced_{fpath.name}"
print(reduced_fpath)
hdul_af = fits.open(str(reduced_fpath))

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = du.zimshow(axs[0], hdul_af[0].data,
            origin='lower',
            cmap='viridis',
            )

im2 = axs[1].hist(hdul_af[0].data,
                range=(hdul_af[0].data.mean()*.9, hdul_af[0].data.mean()*1.1),
                )

axs[0].set_title(f'After preprocessing (No dark scale)', fontsize=10)
axs[1].set_title('The histrogram of pixel value', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {hdul_af[0].data.min()}, Mean value: {hdul_af[0].data.mean():.02f}, Max value: {hdul_af[0].data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 177.
from ccdproc import CCDData, ccd_process
import astropy.units as u

for fpath in object_BLCAM_list:
    obj = CCDData.read(str(fpath), unit='adu')
    reduced_darksc = ccd_process(obj,                    # 입력 이미지
                          master_bias = bias,        # 마스터 바이어스
                          dark_frame = dark_30sec,  # 노출 시간이 다른(30초) 다크
                          master_flat = flat_norm,   # 바이어스·다크를 빼고 정규화한 플랫
                          exposure_key = 'exptime',  # 노출 시간 키워드
                          exposure_unit = u.s,       # 노출 시간 단위
                          dark_scale = True,         # 다크 프레임 크기를 맞출지 여부
                          )
    reduced_darksc.data = reduced_darksc.data.astype(np.float32)
    reduced_darksc.write(f"{REDUCEDDIR}/reduced_darksc_{fpath.name}",
                         overwrite =True)
    print(f"{REDUCEDDIR}/reduced_darksc_{fpath.name} is created... (median: {np.median(reduced_darksc.data):.1f})")

# %% code 178.
fpath = object_BLCAM_list[0]
reduced_darksc_fpath = REDUCEDDIR / f"reduced_darksc_{fpath.name}"
print(reduced_darksc_fpath)
hdul_af_darksc = fits.open(str(reduced_darksc_fpath))

fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.4),
                        sharex=False, sharey=False, gridspec_kw=None)

im1 = du.zimshow(axs[0], hdul_af_darksc[0].data,
            origin='lower',
            cmap='viridis',
            )

im2 = axs[1].hist(hdul_af_darksc[0].data,
                range=(hdul_af_darksc[0].data.mean()*.9,
                       hdul_af_darksc[0].data.mean()*1.1),
                )

axs[0].set_title(f'After preprocessing (dark scale)', fontsize=10)
axs[1].set_title('The histrogram of pixel value', fontsize=10)

plt.colorbar(im1, fraction=0.0455, pad=0.04)
fig.text(0.5, 0.02, f"Min value: {hdul_af_darksc[0].data.min()}, Mean value: {hdul_af_darksc[0].data.mean():.02f}, Max value: {hdul_af_darksc[0].data.max()}",
         ha="center", fontsize=9)   # 그림 아래 가운데
plt.tight_layout(pad=1.0, rect=(0, 0.07, 1, 1))
plt.show()

# %% code 179.
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

# %% code 180.
plot_image_with_cutouts(hdul_af[0].data)

# %% code 181.
plot_image_with_cutouts(hdul_af_darksc[0].data)

# %% code 182.
import pandas as pd
import astropy.units as u
from astropy.io import fits
from ccdproc import CCDData, combine, ccd_process, subtract_bias

# %% code 183.
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

# %% code 184.
bias_files = summary.loc[summary["IMAGETYP"] == "BIAS", "file"].tolist()
print("len(bias_files):", len(bias_files))

mbias = combine(bias_files, method="median", unit="adu")
mbias.data = mbias.data.astype(np.float32)

fname = MASTERDIR / "master_bias.fits"
mbias.write(fname, overwrite=True)
print(f"{fname} is created...")

# %% code 185.
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

# %% code 186.
flat_df = summary.loc[summary["IMAGETYP"] == "FLAT"]
print("len(flat_df):", len(flat_df))
flat_df

# %% code 187.
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

# %% code 188.
mflats_norm = {}                     # 필터 -> 정규화한 마스터 플랫

for filt, mflat in mflats.items():
    mflat_norm = mflat.copy()
    mflat_norm.data = mflat.data / np.median(mflat.data)   # 중앙값 = 1

    fname = MASTERDIR / f"master_flat_{filt.upper()}_norm.fits"
    mflat_norm.write(fname, overwrite=True)
    mflats_norm[filt] = mflat_norm
    print(f"{fname} is created... (median: {np.median(mflat.data):.1f})")

# %% code 189.
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
                      master_flat=mflats_norm[filt],  # 필터가 같은 플랫
                      exposure_key="exptime",
                      exposure_unit=u.s,
                      dark_scale=False)               # 기본값 False
    red.data = red.data.astype(np.float32)

    fname = REDUCEDDIR / f"red_auto_{fpath.name}"
    red.write(fname, overwrite=True)
    print(f"{fname} is created... (median: {np.median(red.data):.1f})")

# %% code 190.
for _, row in df_light_bl.iterrows():
    fpath = Path(row["file"])
    ccd = CCDData.read(fpath, unit="adu")
    filt = ccd.header["FILTER"]
    red = ccd_process(ccd,
                      master_bias=mbias,
                      dark_frame=mdarks[30.0],       # 노출 시간이 다른 다크
                      master_flat=mflats_norm[filt],
                      exposure_key="exptime",
                      exposure_unit=u.s,
                      dark_scale=True)                # 노출 시간에 맞춤
    red.data = red.data.astype(np.float32)

    fname = REDUCEDDIR / f"red_auto_darksc_{fpath.name}"
    red.write(fname, overwrite=True)
    print(f"{fname} is created... (median: {np.median(red.data):.1f})")

# %% code 191.
df_light_tt = df_light.loc[df_light["OBJECT"] == "TT-ARI"].reset_index(drop=True)
print("len(df_light_tt):", len(df_light_tt))

reduced_tt = []
for _, row in df_light_tt.iterrows():
    fpath = Path(row["file"])
    ccd = CCDData.read(fpath, unit="adu")
    red = ccd_process(ccd,
                      master_bias=mbias,
                      dark_frame=mdarks[ccd.header["EXPTIME"]],   # 30초 다크
                      master_flat=mflats_norm[ccd.header["FILTER"]],
                      exposure_key="exptime",
                      exposure_unit=u.s,
                      dark_scale=False)
    red.data = red.data.astype(np.float32)
    fname = REDUCEDDIR / f"red_auto_{fpath.name}"
    red.write(fname, overwrite=True)
    reduced_tt.append(red)
    print(f"{fname.name} (median: {np.median(red.data):.1f})")

fig, axs = plt.subplots(1, len(reduced_tt), figsize=(7.5, 2.0))
for ax, red, (_, row) in zip(axs, reduced_tt, df_light_tt.iterrows()):
    du.zimshow(ax, red.data)
    ax.set_title(red.header["DATE-OBS"][11:19], fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])
plt.suptitle("TT Ari, V 30 s (bias, dark 30 s, flat)", fontsize=11)
plt.tight_layout()
plt.show()
