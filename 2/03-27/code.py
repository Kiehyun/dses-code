# 지구과학 데이터 사이언스 2 | III-07. FITS 이미지 정렬과 합성
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅲ-157.
# 구글 드라이브에 공유해 둔 압축 파일 받기(du.download 가 gdown 을 조용히 사용)
fname = "IC1848_Light_H_2017-01-16.zip"
fid = "1EHVrbmZoPMH4tXpL7bL7KWOV2QZD1E4S"

du.download(f"https://drive.google.com/uc?id={fid}", proj_dir / fname)

# %% code Ⅲ-158.
import os
from pathlib import Path
if not (proj_dir).exists():
    os.mkdir(str(proj_dir))
    print (f"{str(proj_dir)} is created...")
else : 
    print (f"{str(proj_dir)} already exists...")

# %% code Ⅲ-159.
import shutil

# 내려받은 압축 파일 찾기
fpaths = du.list_files(proj_dir, "zip")

shutil.unpack_archive(str(fpaths[0]), str(proj_dir))
print(str(fpaths[0]), "is unpacked to", str(proj_dir))

# %% code Ⅲ-160.
fpaths = du.list_files(proj_dir, pattern="*wcs.fit*")

# %% code Ⅲ-161.
from astropy.io import fits

hdul1 = fits.open(fpaths[0])
hdul2 = fits.open(fpaths[1])
hdul1.info()     # HDU 목록: 0번에 영상, 1번부터는 미리보기 · 장비 정보
for k in ["DATE-OBS", "EXPTIME", "FILTER"]:
    print(f"{k:9s} = {hdul1[0].header.get(k)}")
print("영상 배열 :", hdul1[0].data.dtype, hdul1[0].data.shape, hdul2[0].data.shape)

# %% code Ⅲ-162.
import numpy as np
import matplotlib.pyplot as plt

# 서브플롯에 쓸 제목과 이미지 정의
titles = ['1st image', '2nd image']
images = [hdul1[0].data, hdul2[0].data]

# 그림과 서브플롯 만들기
fig, axes = plt.subplots(1, 2, figsize=(7.5, 4.7))

vmax = int(np.median(hdul1[0].data) * 1.1)

# 축·제목·이미지를 차례로 돌며 서브플롯 채우기
for ax, title, image in zip(axes, titles, images):
    ax.set_title(title, fontsize=11, y=1.03)
    ax.tick_params(labelsize=9)
    im = ax.imshow(image, vmax=vmax)

# 컬러바 추가
cbar_ax = fig.add_axes([0.92, 0.288, 0.022, 0.43])  # 왼쪽, 아래, 너비, 높이
fig.colorbar(im, cax=cbar_ax)

plt.suptitle('IC1848 images', fontsize=12)
plt.show()

# %% code Ⅲ-163.
import numpy as np
import matplotlib.pyplot as plt

# 서브플롯에 쓸 제목과 이미지 정의
titles = ['1st image', '2nd image']
images = [hdul1[0].data[:100, :100], hdul2[0].data[:100, :100]]

# 그림과 서브플롯 만들기
fig, axes = plt.subplots(1, 2, figsize=(7.5, 4.7))

vmax = int(np.median(hdul1[0].data) * 1.1)

# 축·제목·이미지를 차례로 돌며 서브플롯 채우기
for ax, title, image in zip(axes, titles, images):
    ax.set_title(title, fontsize=11, y=1.03)
    ax.tick_params(labelsize=9)
    ax.grid()
    im = ax.imshow(image, vmax=vmax)

# 컬러바 추가
cbar_ax = fig.add_axes([0.92, 0.221, 0.022, 0.56])  # 왼쪽, 아래, 너비, 높이
fig.colorbar(im, cax=cbar_ax)

plt.suptitle('IC1848 images [:100, :100]', fontsize=12)
plt.show()

# %% code Ⅲ-164.
import numpy as np
import astroalign as aa

# 데이터를 리틀엔디언 형식으로 변환
source_data = np.asarray(hdul2[0].data, dtype=np.float32)
target_data = np.asarray(hdul1[0].data, dtype=np.float32)

# 정렬 실행
registered_image1, footprint1 = aa.register(source_data, target_data)
registered_image2, footprint2 = aa.register(target_data, source_data)

print(type(registered_image1))
print(type(footprint1))

# %% code Ⅲ-165.
import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(7.5, 7))
fig.subplots_adjust(hspace=0.35)   # 아랫줄 제목이 윗줄 눈금과 겹치지 않게
axes = axes.flatten()

titles = [
    '1st image', '2nd image', '2nd image(aligned to 1st image)',
    '1st image(aligned to 2nd image)'
]
images = [
    hdul1[0].data[:100, :100],
    hdul2[0].data[:100, :100],
    registered_image1[:100, :100],
    registered_image2[:100, :100]
]

vmax = int(np.median(hdul1[0].data) * 1.1)

for ax, title, image in zip(axes, titles, images):
    ax.set_title(title, fontsize=11, y=1.03)
    ax.tick_params(labelsize=9)
    ax.grid()
    im = ax.imshow(image, vmax=vmax)

cbar_ax = fig.add_axes([0.92, 0.123, 0.022, 0.76])  # 왼쪽, 아래, 너비, 높이
fig.colorbar(im, cax=cbar_ax)

plt.suptitle('IC1848 images [:100, :100]', fontsize=13)
plt.show()

# %% code Ⅲ-166.
import numpy as np
from astropy.io import fits

def save_aligned(fname, data, ref_header):
    hdr = ref_header.copy()          # 기준 영상의 헤더를 복사
    for key in ("BZERO", "BSCALE"):  # 정수형 저장용 키워드는 지움
        hdr.remove(key, ignore_missing=True)
    fits.writeto(fname, data.astype(np.float32), header=hdr, overwrite=True)
    print(f"{fname} is created...")

# 1st 영상에 맞춘 2nd 영상
save_aligned(f"{fpaths[1].parent/fpaths[1].stem}_aligned.fit", registered_image1, hdul1[0].header)
# 2nd 영상에 맞춘 1st 영상
save_aligned(f"{fpaths[0].parent/fpaths[0].stem}_aligned.fit", registered_image2, hdul2[0].header)

# %% code Ⅲ-167.
aligned_list = du.list_files(proj_dir, pattern="*_aligned.fit")

# %% code Ⅲ-168.
from astropy.io import fits

hdul3 = fits.open(f"{fpaths[0].parent/fpaths[0].stem}_aligned.fit")
hdul4 = fits.open(f"{fpaths[1].parent/fpaths[1].stem}_aligned.fit")

images = [
    (hdul1[0].data, '1st image'),
    (hdul4[0].data, '2nd image (aligned)')
]

import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(7.5, 4.7))

vmax = int(np.median(hdul1[0].data) * 1.1)

for ax, (image, title) in zip(axes, images):
    ax.tick_params(labelsize=9)
    ax.set_title(title, fontsize=11, y=1.03)
    im = ax.imshow(image, vmax=vmax)

cbar_ax = fig.add_axes([0.92, 0.288, 0.022, 0.43])  # 왼쪽, 아래, 너비, 높이
fig.colorbar(im, cax=cbar_ax)

plt.suptitle('IC1848 images', fontsize=12)
plt.show()

# %% code Ⅲ-169.
from astropy.io import fits

import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(7.5, 4.7))

ax1 = fig.add_subplot(121)
ax3 = fig.add_subplot(122)

ax1.tick_params(labelsize=9)
ax3.tick_params(labelsize=9)

ax1.set_title('1st image', fontsize=11, y=1.03)
ax3.set_title('2nd image(aligned to 1st image)', fontsize=11, y=1.03)
vmax = int(np.median(hdul1[0].data)*1.1)

ax1.grid()
ax3.grid()

#FITS 파일 표시 
im1 = ax1.imshow(hdul1[0].data[:100, :100], vmax=vmax)
im3 = ax3.imshow(hdul4[0].data[:100, :100], vmax=vmax)

cbar_ax12 = fig.add_axes([0.92, 0.221, 0.022, 0.56]) # 왼쪽, 아래, 너비, 높이
fig.colorbar(im1, cax=cbar_ax12)

plt.suptitle('IC1848 images [:100, :100]', fontsize=12)
#fig.tight_layout()

plt.show()

# %% code Ⅲ-170.
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

# 서브플롯에 쓸 제목과 이미지 정의
titles = [
    '1st image', '2nd image', '2nd image(aligned to 1st image)',
    '1st image(aligned to 2nd image)'
]
images = [
    hdul1[0].data[:100, :100],
    hdul2[0].data[:100, :100],
    hdul4[0].data[:100, :100],
    hdul3[0].data[:100, :100]
]

# 그림과 서브플롯 만들기
fig, axes = plt.subplots(2, 2, figsize=(7.5, 7))
fig.subplots_adjust(hspace=0.35)   # 아랫줄 제목이 윗줄 눈금과 겹치지 않게
axes = axes.flatten()

vmax = int(np.median(hdul1[0].data) * 1.1)

# 축·제목·이미지를 차례로 돌며 서브플롯 채우기
for ax, title, image in zip(axes, titles, images):
    ax.set_title(title, fontsize=11, y=1.03)
    ax.tick_params(labelsize=9)
    ax.grid()
    im = ax.imshow(image, vmax=vmax)

# 컬러바 추가
cbar_ax = fig.add_axes([0.92, 0.123, 0.022, 0.76])  # 왼쪽, 아래, 너비, 높이
fig.colorbar(im, cax=cbar_ax)

plt.suptitle('IC1848 images [:100, :100]', fontsize=13)
plt.show()

# %% code Ⅲ-171.
from astropy.io import fits

hduls_data = []
for fpath in fpaths : 
    hdul = fits.open(fpath)
    hduls_data.append(hdul[0].data)

import numpy as np
import matplotlib.pyplot as plt

fig, axs = plt.subplots(4, 3, figsize=(6.2, 7.0), constrained_layout=True)   # 영상 10장

axs = axs.ravel()

vmax = int(np.median(hduls_data[0])*1.1)
print("len(hduls_data)", len(hduls_data))
for i in range(len(hduls_data)):
    axs[i].set_title('image({})'.format(i), fontsize=10)
    axs[i].grid()
    im = axs[i].imshow(hduls_data[i], vmax=vmax)

for ax in axs[len(hduls_data):]:          # 남는 칸은 비움
    ax.axis('off')
fig.colorbar(im, ax=axs.tolist(), shrink=0.6, pad=0.02)

plt.suptitle('IC1848 images', fontsize=13)

plt.show()

# %% code Ⅲ-172.
import numpy as np
import astroalign as aa

r = 0                                                 # 기준 이미지 번호
target = np.asarray(hduls_data[r], dtype=np.float32)  # 기준 영상

aligned_hduls_data = []
footprints = []
for i in range(len(hduls_data)):
    if i == r:                                           # 기준 영상은 그대로
        aligned_hduls_data.append(target)
        footprints.append(np.zeros(target.shape, dtype=bool))
        continue
    source = np.asarray(hduls_data[i], dtype=np.float32) # 맞출 영상
    registered_image, footprint = aa.register(source, target)
    aligned_hduls_data.append(registered_image)
    footprints.append(footprint)

print("type(aligned_hduls_data): {}".format(type(aligned_hduls_data)))

import matplotlib.pyplot as plt

fig, axs = plt.subplots(4, 3, figsize=(6.2, 7.0), constrained_layout=True)   # 영상 10장

axs = axs.ravel()

vmax = int(np.median(aligned_hduls_data[0])*1.1)

for i in range(len(aligned_hduls_data)):
    axs[i].set_title('image({})'.format(i), fontsize=10)
    axs[i].grid()
    im = axs[i].imshow(aligned_hduls_data[i], vmax=vmax)

for ax in axs[len(aligned_hduls_data):]:          # 남는 칸은 비움
    ax.axis('off')
fig.colorbar(im, ax=axs.tolist(), shrink=0.6, pad=0.02)

plt.suptitle('IC1848 images (aligned)', fontsize=13)

plt.show()

# %% code Ⅲ-173.
import numpy as np
import matplotlib.pyplot as plt

fig, axs = plt.subplots(4, 3, figsize=(6.2, 7.0), constrained_layout=True)   # 영상 10장
axs = axs.ravel()
vmax = int(np.median(aligned_hduls_data[0][:100, :100])*1.1)

for i in range(len(aligned_hduls_data)):
    axs[i].set_title('image({})'.format(i), fontsize=10)
    axs[i].grid()
    im = axs[i].imshow(aligned_hduls_data[i][:100, :100], vmax=vmax)

for ax in axs[len(aligned_hduls_data):]:          # 남는 칸은 비움
    ax.axis('off')
fig.colorbar(im, ax=axs.tolist(), shrink=0.6, pad=0.02)

plt.suptitle('IC1848 images [:100, :100] (aligned)', fontsize=13)
plt.show()

# %% code Ⅲ-174.
def centroid(img, x, y, half=5):
    """(x, y) 주변 상자에서 밝기 가중 평균으로 별의 중심을 구함"""
    xi, yi = int(round(x)), int(round(y))
    cut = np.asarray(img[yi-half:yi+half+1, xi-half:xi+half+1], dtype=float)
    cut = np.clip(cut - np.median(cut), 0, None)       # 상자 안의 배경을 빼고 음수는 0
    yy, xx = np.mgrid[-half:half+1, -half:half+1]
    return xi + (xx*cut).sum()/cut.sum(), yi + (yy*cut).sum()/cut.sum()

ny, nx = target.shape
_, (_, ref_pts) = aa.find_transform(np.asarray(hduls_data[1], dtype=np.float32), target)
# 가장자리 별 제외
ref_pts = [p for p in ref_pts if 10 < p[0] < nx-10 and 10 < p[1] < ny-10]
ref_c = np.array([centroid(target, x, y) for x, y in ref_pts])
print(f"비교에 쓴 별: {len(ref_c)}개")

for i in range(len(hduls_data)):
    if i == r:
        continue
    raw_c = np.array([centroid(hduls_data[i], x, y) for x, y in ref_pts])
    ali_c = np.array([centroid(aligned_hduls_data[i], x, y) for x, y in ref_pts])
    before = np.median(np.hypot(*(raw_c - ref_c).T))
    after = np.median(np.hypot(*(ali_c - ref_c).T))
    print(f"image({i}): 정렬 전 {before:5.2f} px  ->  정렬 후 {after:5.2f} px")

# %% code Ⅲ-175.
import os
from pathlib import Path
if not (proj_dir).exists():
    os.mkdir(str(proj_dir))
    print (f"{str(proj_dir)} is created...")
else : 
    print (f"{str(proj_dir)} already exists...")

import numpy as np

np_average = np.mean(aligned_hduls_data, axis=0)
np_median = np.median(aligned_hduls_data, axis=0)
print("np_average.shape:", np_average.shape)
print("np_median.shape:", np_median.shape)

# %% code Ⅲ-176.
import numpy as np
import matplotlib.pyplot as plt

# 그림과 서브플롯 만들기
fig, axes = plt.subplots(2, 2, figsize=(7.5, 4.7))
titles = ['1st image', '2nd image', 'combined image (np.mean)',
          'combined image (np.median)']
images = [hduls_data[0], hduls_data[1], np_average, np_median]
vmax = int(np.median(hduls_data[0]) * 1.1)

# 이미지 그리기
for ax, title, image in zip(axes.flatten(), titles, images):
    ax.set_title(title, fontsize=11, y=1.03)
    ax.tick_params(labelsize=9)
    ax.grid()
    im = ax.imshow(image, vmax=vmax)
fig.subplots_adjust(hspace=0.45)   # 아랫줄 제목이 윗줄 눈금과 겹치지 않게

# 컬러바 추가
cbar_ax = fig.add_axes([0.92, 0.288, 0.022, 0.428])
fig.colorbar(im, cax=cbar_ax)

plt.suptitle('IC1848 images', fontsize=12)
plt.show()

# %% code Ⅲ-177.
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(7.5, 4.7))

ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.tick_params(labelsize=9)
ax2.tick_params(labelsize=9)

ax1.set_title('combined image (np.mean)', fontsize=11, y=1.03)
ax2.set_title('combined image (np.median)', fontsize=11, y=1.03)
vmax = int(np.median(np_average[:100, :100])*1.1)

ax1.grid()
ax2.grid()
#FITS 파일 표시 
im1 = ax1.imshow(np_average[:100, :100], vmax=vmax)
im2 = ax2.imshow(np_median[:100, :100], vmax=vmax)

cbar_ax12 = fig.add_axes([0.92, 0.221, 0.022, 0.56]) # 왼쪽, 아래, 너비, 높이
fig.colorbar(im1, cax=cbar_ax12)

plt.suptitle('IC1848 images [:100, :100]', fontsize=12)
#fig.tight_layout()

plt.show()

# %% code Ⅲ-178.
import numpy as np
from astropy.nddata import CCDData
from astropy.stats import mad_std

import ccdproc as ccdp

# 정렬한 배열과 가장자리 마스크로 CCDData 목록 만들기
aligned_ccds = [CCDData(data, mask=mask, unit='adu')
                for data, mask in zip(aligned_hduls_data, footprints)]

combined_light_avg_sigma_False = ccdp.combine(aligned_ccds,
                            method = 'average')

combined_light_avg_sigma_True = ccdp.combine(aligned_ccds, method = 'average',
                            sigma_clip=True, sigma_clip_low_thresh=5, sigma_clip_high_thresh=5,
                            sigma_clip_func=np.ma.median, sigma_clip_dev_func=mad_std)

combined_light_med_sigma_False = ccdp.combine(aligned_ccds, method='median')

combined_light_med_sigma_True = ccdp.combine(aligned_ccds, method = 'median',
                            sigma_clip=True, sigma_clip_low_thresh=5, sigma_clip_high_thresh=5,
                            sigma_clip_func=np.ma.median, sigma_clip_dev_func=mad_std)

print(type(combined_light_avg_sigma_False))
print(type(combined_light_avg_sigma_True))
print(type(combined_light_med_sigma_False))
print(type(combined_light_med_sigma_True))

# %% code Ⅲ-179.
print("type(combined_light_avg_sigma_False): {}".format(type(combined_light_avg_sigma_False)))
print("combined_light_avg_sigma_False.shape: {}".format(combined_light_avg_sigma_False.shape))
print("combined_light_avg_sigma_False: {}".format(combined_light_avg_sigma_False))

# %% code Ⅲ-180.
out_path = proj_dir / "IC1848_combined.fit"
combined_light_avg_sigma_True.write(out_path, overwrite=True)
print(out_path.name, "저장됨")

# %% code Ⅲ-181.
import numpy as np
import matplotlib.pyplot as plt

# 그림과 서브플롯 만들기
fig, axes = plt.subplots(2, 2, figsize=(7.5, 4.7))
titles = ['average (sigma clip off)', 'average (sigma clip on)',
          'median (sigma clip off)', 'median (sigma clip on)']
images = [combined_light_avg_sigma_False.data,
          combined_light_avg_sigma_True.data,
          combined_light_med_sigma_False.data,
          combined_light_med_sigma_True.data]
vmax = int(np.median(combined_light_avg_sigma_False.data) * 1.1)

# 이미지 그리기
for ax, title, image in zip(axes.flatten(), titles, images):
    ax.set_title(title, fontsize=11, y=1.03)
    ax.tick_params(labelsize=9)
    ax.grid()
    im = ax.imshow(image, vmax=vmax)
fig.subplots_adjust(hspace=0.45)   # 아랫줄 제목이 윗줄 눈금과 겹치지 않게

# 컬러바 추가
cbar_ax = fig.add_axes([0.92, 0.288, 0.022, 0.428])
fig.colorbar(im, cax=cbar_ax)

plt.suptitle('IC1848 images', fontsize=12)
plt.show()

# %% code Ⅲ-182.
from astropy.stats import sigma_clipped_stats

box = (slice(1750, 1900), slice(3100, 3250))   # 별·성운이 거의 없는 영역 (y, x)
N = len(aligned_hduls_data)

results = {
    "1장 (기준 영상)": aligned_hduls_data[r],
    "np.mean": np_average,
    "np.median": np_median,
    "ccdproc average": combined_light_avg_sigma_False.data,
    "ccdproc average + clip": combined_light_avg_sigma_True.data,
    "ccdproc median": combined_light_med_sigma_False.data,
    "ccdproc median + clip": combined_light_med_sigma_True.data,
}
noise1 = sigma_clipped_stats(aligned_hduls_data[r][box])[2]
for name, image in results.items():
    _, med, std = sigma_clipped_stats(image[box])
    print(f"{name:24s} 배경 {med:7.1f} ADU, 잡음 {std:6.1f} ADU, 1장 대비 {noise1/std:4.2f}배 감소")
print(f"이론값 sqrt(N) = {np.sqrt(N):.2f}")

# %% code Ⅲ-183.
from astropy.stats import sigma_clip, mad_std

stack = np.ma.masked_array(aligned_hduls_data, mask=footprints)   # 가장자리는 미리 가림
clipped = sigma_clip(stack, sigma=5, axis=0,
                     cenfunc=np.ma.median, stdfunc=mad_std, masked=True)
clip_mask = clipped.mask & ~np.array(footprints)                 # 클리핑으로 걸러진 화소만

n_clip = clip_mask.reshape(N, -1).sum(axis=1)
for i, n in enumerate(n_clip):
    print(f"image({i}): 걸러진 화소 {n:7d}개 ({n/clip_mask[i].size*100:.2f}%)")

k = int(np.argmax(n_clip))
fig, ax = plt.subplots(figsize=(5, 4))
ax.imshow(clip_mask[k], cmap='gray_r', interpolation='nearest')
ax.set_title(f'clipped pixels in image({k})', fontsize=10)
ax.tick_params(labelsize=8)
plt.show()
