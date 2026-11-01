# 지구과학 데이터 사이언스 1 | IV-06. 기상위성 천리안 이미지 RGB 합성
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 94.
# 국가위성센터로 부터 직접 다운로드
from pathlib import Path

du.download(f"http://nmsc.kma.go.kr/IMG/COMS/MI/L1/L1B/201907/10/coms_mi_le1b_vis_en010ge_201907101045.png", Path(proj_dir) / 'coms_mi_le1b_vis_en010ge_201907101045.png')
du.download(f"http://nmsc.kma.go.kr/IMG/COMS/MI/L1/L1B/201907/10/coms_mi_le1b_ir01_en040ge_201907101045.png", Path(proj_dir) / 'coms_mi_le1b_ir01_en040ge_201907101045.png')
du.download(f"http://nmsc.kma.go.kr/IMG/COMS/MI/L1/L1B/201907/10/coms_mi_le1b_ir02_en040ge_201907101045.png", Path(proj_dir) / 'coms_mi_le1b_ir02_en040ge_201907101045.png')
du.download(f"http://nmsc.kma.go.kr/IMG/COMS/MI/L1/L1B/201907/10/coms_mi_le1b_swir_en040ge_201907101045.png", Path(proj_dir) / 'coms_mi_le1b_swir_en040ge_201907101045.png')
du.download(f"http://nmsc.kma.go.kr/IMG/COMS/MI/L1/L1B/201907/10/coms_mi_le1b_wv_en040ge_201907101045.png", Path(proj_dir) / 'coms_mi_le1b_wv_en040ge_201907101045.png')

# %% code 95.
fpaths = du.list_files(proj_dir, "png")

# %% code 96.
from PIL import Image

#RGB 각 채널에 해당하는 파일명 입력
vis_filename = fpaths[3]
ir1_filename = fpaths[0]
ir2_filename = fpaths[1]
swir_filename = fpaths[2]
wv_filename = fpaths[4]

red = Image.open(vis_filename)
green = Image.open(ir1_filename)
blue = Image.open(ir2_filename)

print("type(red) :", type(red))  # red에 담긴 type을 출력
print("red :", red)              # red에 담긴 자료를 출력

# %% code 97.
import numpy as np
red_arr = np.array(red)                            #ndarray로 변환
print("type(red_arr) : {}".format(type(red_arr)))  #자료형 확인
print(red_arr.shape)                               #ndarray로 dimension 확인

# 24bit RGB 파일을 8bit L 파일로 변환-
red = red.convert('L')
green = green.convert('L')
blue = blue.convert('L')

print (type(red))  # red에 담긴 type을 출력
print (red)        # red에 담긴 자료를 출력

redA = np.array(red)
print(redA.shape)
print (type(red))  # red에 담긴 type을 출력
print (red)        # red에 담긴 자료를 출력

# %% code 98.
#package 불러오기
import matplotlib.pyplot as plt

#화면에 이미지를 출력 출력
print ('*'*80)
print ('display COMS_MI image')

fig = plt.figure(figsize=(10,8))
plt.imshow(red, cmap = 'gray', interpolation = 'None')

plt.xticks([]), plt.yticks([])  # x, y축 눈금값 숨기기
plt.show()

# %% code 99.
# 그림 너비 15, 높이 13으로 지정
from PIL import Image

print("변환 전 크기")
print("red size  :", red.size)
print("green size:", green.size)
print("blue size :", blue.size)

# RGB 합성을 위해 모든 채널을 같은 크기로 맞춤
target_size = red.size

green = green.resize(target_size)
blue = blue.resize(target_size)

# 혹시 mode가 L이 아니면 8-bit grayscale로 변환
red = red.convert("L")
green = green.convert("L")
blue = blue.convert("L")

print("변환 후 크기")
print("red size  :", red.size)
print("green size:", green.size)
print("blue size :", blue.size)

rgb = Image.merge("RGB", (red, green, blue))

rgb.save(f"{proj_dir}/coms_mi_rgb_201907101045.png")

print ("type(rgb) :", type(rgb))  # red에 담긴 type을 출력
print ("rgb :", rgb)              # red에 담긴 자료를 출력

# 2행 2열로 이미지 디스플레이 (1,1: vis / 1,2: ir1 / 2,1: ir2 / 2,2: rgb)
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 각 이미지 불러오기
vis_img = Image.open(vis_filename)
ir1_img = Image.open(ir1_filename)
ir2_img = Image.open(ir2_filename)
rgb_img = rgb  # 이미 합성된 객체

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

# %% code 100.
print ("red.width:{}".format(red.width))
print ("red.height:{}".format(red.height))

# %% code 101.
#RGB 모드, 크기 2×1 의 빈 이미지 만들기
new_im=Image.new('RGB', (red.width*2,red.height*1))
print (type(new_im))  # new_im에 담긴 type을 출력

new_im.paste(red, (0, 0))
new_im.paste(green, (green.width, 0))
print (type(new_im))  # new_im에 담긴 type을 출력
print (new_im)        # new_im에 담긴 자료를 출력

# %% code 102.
#RGB 모드, 크기 2×1 의 빈 이미지 만들기
new_im=Image.new('RGB', (red.width*1,red.height*2))
new_im.paste(red, (0, 0))
new_im.paste(green, (0, green.height))
print (type(new_im))  # new_im에 담긴 type을 출력
print (new_im)        # new_im에 담긴 자료를 출력
new_im                # new_im을 화면에 보여줌

# %% code 103.
# 6개의 이미지를 2행 3열로 이어 붙이기
from PIL import Image
# 파일명 리스트 (순서: vis, ir1, ir2, swir, wv, rgb)
img_filenames = [vis_filename, ir1_filename, ir2_filename, swir_filename, wv_filename, 
        f"{proj_dir}/coms_mi_rgb_201907101045.png"]
# 이미지 열기
images = [Image.open(f) for f in img_filenames]
# 각 이미지의 크기 (모두 동일하다고 가정)
w, h = images[0].width, images[0].height
# 새 이미지 생성 (2행 3열)
new_im = Image.new('RGB', (w*3, h*2))
# 이미지 붙이기
for idx, im in enumerate(images):
    x= (idx % 3) * w
    y= (idx // 3) * h
    new_im.paste(im, (x, y))
# 결과 확인 및 저장
new_im.save(f"{proj_dir}/coms_mi_6ch_stitched.png")
print(f"{proj_dir}/coms_mi_6ch_stitched.png is created")
display(new_im)
