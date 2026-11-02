# 지구과학 데이터 사이언스 1 | IV-06. 기상위성 천리안 이미지 RGB 합성
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅳ-99.
# 국가기상위성센터에서 2019-07-10 10:45 영상 다섯 채널 내려받기
from pathlib import Path

du.download(f"http://nmsc.kma.go.kr/IMG/COMS/MI/L1/L1B/201907/10/coms_mi_le1b_vis_en010ge_201907101045.png", Path(proj_dir) / 'coms_mi_le1b_vis_en010ge_201907101045.png')
du.download(f"http://nmsc.kma.go.kr/IMG/COMS/MI/L1/L1B/201907/10/coms_mi_le1b_ir01_en040ge_201907101045.png", Path(proj_dir) / 'coms_mi_le1b_ir01_en040ge_201907101045.png')
du.download(f"http://nmsc.kma.go.kr/IMG/COMS/MI/L1/L1B/201907/10/coms_mi_le1b_ir02_en040ge_201907101045.png", Path(proj_dir) / 'coms_mi_le1b_ir02_en040ge_201907101045.png')
du.download(f"http://nmsc.kma.go.kr/IMG/COMS/MI/L1/L1B/201907/10/coms_mi_le1b_swir_en040ge_201907101045.png", Path(proj_dir) / 'coms_mi_le1b_swir_en040ge_201907101045.png')
du.download(f"http://nmsc.kma.go.kr/IMG/COMS/MI/L1/L1B/201907/10/coms_mi_le1b_wv_en040ge_201907101045.png", Path(proj_dir) / 'coms_mi_le1b_wv_en040ge_201907101045.png')

# %% code Ⅳ-100.
# 내려받은 원본 영상만(이 노트북이 만든 합성 · 이어 붙인 그림은 빼고)
fpaths = [p for p in du.list_files(proj_dir, "png") if "_le1b_" in str(p)]

# %% code Ⅳ-101.
from PIL import Image

# 파일 이름의 채널 표시로 고른다(순서에 기대지 않음)
pick = lambda ch: next(p for p in fpaths if f"_{ch}_" in str(p))
vis_filename = pick("vis")
ir1_filename = pick("ir01")
ir2_filename = pick("ir02")
swir_filename = pick("swir")
wv_filename = pick("wv")

# R = 가시, G = 적외 1, B = 적외 2
red = Image.open(vis_filename)
green = Image.open(ir1_filename)
blue = Image.open(ir2_filename)

print("type(red) :", type(red))
print("red :", red)

# %% code Ⅳ-102.
import numpy as np
red_arr = np.array(red)  # 이미지 → ndarray
print("type(red_arr) : {}".format(type(red_arr)))
print(red_arr.shape)  # (세로, 가로, 채널)

# 24비트 RGB → 8비트 흑백('L')
red = red.convert('L')
green = green.convert('L')
blue = blue.convert('L')

print (type(red))
print (red)

redA = np.array(red)
print(redA.shape)
print (type(red))
print (red)

# %% code Ⅳ-103.
import matplotlib.pyplot as plt

print ('*'*80)
print ('display COMS_MI image')

fig = plt.figure(figsize=(10,8))
plt.imshow(red, cmap = 'gray', interpolation = 'None')

plt.xticks([]), plt.yticks([])  # 눈금 숨기기
plt.show()

# %% code Ⅳ-104.
from PIL import Image

print("변환 전 크기")
print("red size  :", red.size)
print("green size:", green.size)
print("blue size :", blue.size)

# 채널을 합치려면 크기가 같아야 함
target_size = red.size

green = green.resize(target_size)
blue = blue.resize(target_size)

# 모두 8비트 흑백('L')으로
red = red.convert("L")
green = green.convert("L")
blue = blue.convert("L")

print("변환 후 크기")
print("red size  :", red.size)
print("green size:", green.size)
print("blue size :", blue.size)

rgb = Image.merge("RGB", (red, green, blue))

rgb.save(f"{proj_dir}/coms_mi_rgb_201907101045.png")

print ("type(rgb) :", type(rgb))
print ("rgb :", rgb)

# 2행 2열: VIS, IR1 / IR2, RGB
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

vis_img = Image.open(vis_filename)
ir1_img = Image.open(ir1_filename)
ir2_img = Image.open(ir2_filename)
rgb_img = rgb

axes[0, 0].imshow(vis_img, cmap='gray')
axes[0, 0].set_title('VIS')
axes[0, 1].imshow(ir1_img, cmap='gray')
axes[0, 1].set_title('IR1')
axes[1, 0].imshow(ir2_img, cmap='gray')
axes[1, 0].set_title('IR2')
axes[1, 1].imshow(rgb_img)
axes[1, 1].set_title('RGB')

for ax in axes.flat:
    ax.set_xticks([])
    ax.set_yticks([])

plt.tight_layout()
plt.show()

# %% code Ⅳ-105.
print ("red.width:{}".format(red.width))
print ("red.height:{}".format(red.height))

# %% code Ⅳ-106.
# 가로로 두 장 붙일 빈 RGB 이미지(너비 2배)
new_im=Image.new('RGB', (red.width*2,red.height*1))
print (type(new_im))

new_im.paste(red, (0, 0))  # 붙일 위치(왼쪽 위 모서리)
new_im.paste(green, (green.width, 0))
print (type(new_im))
print (new_im)

# %% code Ⅳ-107.
# 세로로 두 장 붙일 빈 RGB 이미지(높이 2배)
new_im=Image.new('RGB', (red.width*1,red.height*2))
new_im.paste(red, (0, 0))
new_im.paste(green, (0, green.height))
print (type(new_im))
print (new_im)
new_im  # 셀의 마지막 값이 이미지면 화면에 표시

# %% code Ⅳ-108.
# 여섯 장을 2행 3열로 이어 붙이기
from PIL import Image
img_filenames = [vis_filename, ir1_filename, ir2_filename, swir_filename, wv_filename,
        f"{proj_dir}/coms_mi_rgb_201907101045.png"]
images = [Image.open(f) for f in img_filenames]
w, h = images[0].width, images[0].height  # 모두 같은 크기라고 가정
new_im = Image.new('RGB', (w*3, h*2))
for idx, im in enumerate(images):
    x= (idx % 3) * w   # 열 위치
    y= (idx // 3) * h  # 행 위치
    new_im.paste(im, (x, y))
new_im.save(f"{proj_dir}/coms_mi_6ch_stitched.png")
print(f"{proj_dir}/coms_mi_6ch_stitched.png is created")
display(new_im)
