# 지구과학 데이터 사이언스 1 | III-06. SDO HMI 이미지에서 흑점 탐지
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 78.
from pathlib import Path

fname = "20170228_231038_1024_HMII.jpg"
url = "https://sdo.gsfc.nasa.gov/assets/img/browse/2017/02/28/" + fname

# NASA SDO 웹사이트에서 직접 받기(실패하면 구글 드라이브 사본)
try:
    du.download(url, Path(proj_dir) / fname)
except Exception:
    du.download("https://docs.google.com/uc?export=download&id=1J-1zkRni9VPFT_alsnljSHEBEphdPPMQ", Path(proj_dir) / fname)

fpaths = sorted(Path(proj_dir).glob('*.jpg'))

# %% code 79.
import cv2

print(f"str(fpaths): {str(fpaths)}")
print(f"str(fpaths[0]): {str(fpaths[0])}")

# 이미지를 넘파이 배열로 읽기
# IMREAD_UNCHANGED: 알파 채널까지 그대로
sun_im = cv2.imread(str(fpaths[0]), cv2.IMREAD_UNCHANGED)

print("type(sun_im): ", type(sun_im))

import numpy as np
print("np.shape(sun_im): ", np.shape(sun_im))
print("sun_im.ndim: ", sun_im.ndim)

# shape는 (높이, 너비[, 채널]) 순서
im_height, im_width = sun_im.shape[:2]
im_center_x, im_center_y = im_width/2, im_height/2

import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = [10,10]

plt.imshow(sun_im, cmap = 'gray', origin='upper', interpolation = 'None')

# 눈금을 숨기려면 아래 주석 해제
# plt.xticks([]), plt.yticks([]) 

plt.show()

# %% code 80.
# 허프 변환으로 원(태양) 검출, 입력은 흑백 이미지
# 2: 누적기 해상도 비율(dp), 200: 원 중심 사이 최소 거리(픽셀)
sun_circle = cv2.HoughCircles(sun_im, cv2.HOUGH_GRADIENT, 2, 200)

# 검출된 원: (x, y, 반지름)
print("sun_circle: ", sun_circle)

print("sun_circle[0]: ", sun_circle[0])
print("sun_circle[0][0]: ", sun_circle[0][0])

print("sun_circle[0, 0, :]: ", sun_circle[0, 0, :])

# 정수로 반올림
sun_circle = np.round(sun_circle[0,0,:]).astype(int)
print('circle of sun', sun_circle )

# %% code 81.
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# sun_circle: (x, y, 반지름)

plt.imshow(sun_im, cmap='gray', origin='upper', interpolation='None')

circle = Circle(
    (sun_circle[0], sun_circle[1]), sun_circle[2], facecolor='none',
    edgecolor=(0, 0.8, 0.8), linewidth=2, alpha=0.5
)

ax = plt.gca()
ax.add_patch(circle)

plt.show()

# %% code 82.
# 원본 보존용 복사본
sun_im_output = sun_im.copy()
print("sun_im_output: ", sun_im_output)

# 배경 마스크: 0번 축이 세로(y, 행), 1번 축이 가로(x, 열)
Y, X = np.ogrid[0:im_height, 0:im_width]

boundary_width = 40  # 림 다크닝 영역 두께(픽셀)

# outer: 반지름 - boundary_width 바깥
outer = (X - sun_circle[0]) ** 2 + (Y - sun_circle[1]) ** 2 > (sun_circle[2] - boundary_width) ** 2 

inner = (X - sun_circle[0]) ** 2 + (Y - sun_circle[1]) ** 2 < (sun_circle[2] - boundary_width) ** 2 

print ("type(outer): ", type(outer))
print ("type(inner):", type(inner))

print (np.shape(outer), np.shape(inner))

print ("outer:", outer)
print ("inner", inner)

# %% code 83.
# 8비트 영상에서 255는 흰색
sun_im_output[outer] = 255

print ('boundary width :', boundary_width)

fig, ax = plt.subplots()

plt.imshow(sun_im_output, cmap = 'gray', origin='upper',
           interpolation = 'None')

circle = Circle((sun_circle[0], sun_circle[1]), sun_circle[2], 
                facecolor='none',
                edgecolor=(0, 0.8, 0.8), linewidth=2, alpha=0.5)
ax.add_patch(circle) 

plt.show()

# %% code 84.
# 이보다 어두우면 흑점 후보
bright_criterion = 70 

# True: 흑점이 아닌 픽셀(뒤에서 흰색으로 칠함)
sunspot_mask  = np.zeros((im_height, im_width)).astype(bool)

# 흑점 후보 픽셀 정보: [x, y, 픽셀값]
check_pixel = []

for i in range(0, im_height):     # 행(y축, 세로) 방향으로 반복
    for j in range(0, im_width):  # 열(x축, 가로) 방향으로 반복
        if(sun_im_output[i,j] < bright_criterion):
            sunspot_mask[i,j] = 0  # 0: 흑점
            check_pixel.append([j, i, sun_im_output[i,j]]) 
        else : 
            sunspot_mask[i,j] = 1  # 1: 흑점 아님

print("len(check_pixel): ", len(check_pixel))
print("check_pixel: ", check_pixel)

# 흑점이 아닌 픽셀은 흰색으로
sun_im_output[sunspot_mask] = 255 
print("sun_im_output: ", sun_im_output)

fig, ax = plt.subplots() 

plt.imshow(sun_im_output, cmap = 'gray', origin='upper',
           interpolation = 'None')

circle = Circle((sun_circle[0], sun_circle[1]), sun_circle[2],
                facecolor='none', edgecolor=(0, 0.8, 0.8), linewidth=2,
                alpha=0.5)
ax.add_patch(circle)

plt.show()

# %% code 85.
check_pixel = np.asarray(check_pixel)
print("check_pixel:", check_pixel)

# 0으로 채운 im_height × im_width 배열(행 = y, 열 = x)
image = [[0 for a in range(im_width)] for b in range(im_height)] 

image = np.array(image)

# 흑점 후보 위치는 1: 배열은 [행(y), 열(x)] 순서이므로 image[y, x]
for x, y, value in check_pixel:
    image[y, x] = 1

print("type(image): ", type(image))

fig, ax = plt.subplots()

plt.imshow(image, cmap = 'gray', origin='upper', interpolation = 'None')

circle = Circle((sun_circle[0], sun_circle[1]), sun_circle[2],
                facecolor='none', edgecolor=(0, 0.8, 0.8), linewidth=2,
                alpha=0.5)
ax.add_patch(circle)

plt.show()

# %% code 86.
fig, ax = plt.subplots()

plt.imshow(image.T,  # 잘못된 예: 행과 열을 바꿔(전치) 표시
           cmap = 'gray', 
           interpolation = 'None')

circle = Circle((sun_circle[0], sun_circle[1]), sun_circle[2], 
                facecolor='none',
                edgecolor=(0, 0.8, 0.8), linewidth=2, alpha=0.5)
ax.add_patch(circle) 

plt.show()

# %% code 87.
import math

# 흑점의 위도 · 경도(라디안)
def latitude(y):
    # sun_circle[1]: 중심 y, sun_circle[2]: 반지름
    return math.asin((sun_circle[1] - y) / sun_circle[2])

def longitude(x, y):
    return math.asin((x - sun_circle[0]) / (sun_circle[2] * math.cos(latitude(y))))

# DFS(깊이 우선 탐색)의 8방향 이동
# 상, 우상, 우, 우하, 하, 좌하, 좌, 좌상
dx = [0, 1, 1, 1, 0, -1, -1, -1]
dy = [1, 1, 0, -1, -1, -1, 0, 1]

def dfs(x, y):
    global x_pixel_sum
    global y_pixel_sum
    global num_pixel
    image[y][x] = -1  # 방문 표시(-1)로 재방문 막기(배열은 [y][x] 순서)
    x_pixel_sum += x
    y_pixel_sum += y
    num_pixel += 1

    for i in range(0, len(dx)):
        # 이웃이 흑점(1)이면 재귀 호출
        if(image[y+dy[i]][x+dx[i]] == 1):
            dfs(x+dx[i], y+dy[i])

# 이보다 픽셀이 많아야 흑점
pixel_num_criterion = 2

# [x 평균, y 평균, 픽셀 수]
sunspot_data = []

for y in range(0, im_height):
    for x in range(0, im_width):
        if(image[y][x] == 1):
            x_pixel_sum = 0
            y_pixel_sum = 0
            num_pixel = 0
            dfs(x, y)
            if num_pixel > pixel_num_criterion:
                x_average = x_pixel_sum / num_pixel
                y_average = y_pixel_sum / num_pixel
                latit = latitude(y_average)
                longi = longitude(x_average, y_average)
                latit = math.degrees(latit)
                longi = math.degrees(longi)
                # 경도 · 위도로 저장하려면
                # sunspot_data.append([longi, latit, num_pixel])
                sunspot_data.append([int(x_average), int(y_average), num_pixel])
print ('*'*80)
print ('흑점 개수 : ', len(sunspot_data))
print ('흑점 데이터 [x, y, 픽셀 수] : ', sunspot_data)

# %% code 88.
sunspot_data = np.asarray(sunspot_data)
print("sunspot_data:\n", sunspot_data)

if len(sunspot_data) == 0 : 
    print('영상에서 흑점을 찾지 못했습니다.')
else :
    fig, ax = plt.subplots()
    
    plt.imshow(sun_im, cmap = 'gray', interpolation = 'None')
    
    circle = Circle((sun_circle[0], sun_circle[1]), sun_circle[2],
                    facecolor='none', edgecolor=(0, 0.8, 0.8), linewidth=3,
                    alpha=0.5)
    ax.add_patch(circle)
    
    # 흑점 위치
    plt.plot(sunspot_data[:,0], sunspot_data[:,1], 'ro', markersize=3)
    
    plt.savefig(f'{str(fpaths[0].parents[0])}/{fpaths[0].stem}.png')
    print(f'{str(fpaths[0].parents[0])}/{fpaths[0].stem}.png 파일을 만들었습니다.')

    plt.show()
