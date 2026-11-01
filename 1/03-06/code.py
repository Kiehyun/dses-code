# 지구과학 데이터 사이언스 1 | III-06. SDO HMI 이미지에서 흑점 탐지
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 76.
from pathlib import Path

fname = "20170228_231038_1024_HMII.jpg"
fid = "1yxW326FtXQY_D9VL0DST_pv8QiZ2GBeW"

# SDO에서 직접 받을 경우
# url = "https://sdo.gsfc.nasa.gov/assets/img/browse/2017/02/28/20170228_231038_1024_HMII.jpg"
# 구글 드라이브에 미리 저장해 둔 파일을 받을 경우
url = f"https://docs.google.com/uc?export=download&id={fid}"
du.download(url, Path(proj_dir) / fname)

# 다운로드한 이미지 파일 목록
fpaths = sorted(Path(proj_dir).glob('*.jpg'))

# %% code 77.
import cv2  # OpenCV 라이브러리를 불러옵니다.

# 이미지 파일 경로 리스트를 출력합니다.
print(f"str(fpaths): {str(fpaths)}")        # fpaths 전체 리스트를 문자열로 출력
print(f"str(fpaths[0]): {str(fpaths[0])}")  # 리스트의 첫 번째 이미지 경로를 문자열로 출력

# 이미지를 넘파이 배열(ndarray) 형태로 읽어옵니다.
# cv2.IMREAD_UNCHANGED 옵션은 이미지의 알파 채널(투명도 등)까지 모두 읽어옵니다.
sun_im = cv2.imread(str(fpaths[0]), cv2.IMREAD_UNCHANGED)

# 이미지 데이터의 타입을 출력합니다.
# 일반적으로 numpy.ndarray 타입이 출력됩니다.
print("type(sun_im): ", type(sun_im))

import numpy as np
print("np.shape(sun_im): ", np.shape(sun_im))  # 이미지의 shape(차원 정보)를 출력합니다.
print("sun_im.ndim: ", sun_im.ndim)            # 이미지의 차원 수(ndim)를 출력합니다.

# 이미지의 크기(너비, 높이)를 구합니다.
# 일반적으로 이미지 shape는 (높이, 너비, 채널) 순서입니다.
im_height, im_width = sun_im.shape[:2]              # 채널 정보는 무시하고, 앞의 두 값만 사용합니다.
im_center_x, im_center_y = im_width/2, im_height/2  # 이미지의 중심 좌표를 계산합니다.

import matplotlib.pyplot as plt
# 그래프(이미지) 크기를 가로 10, 세로 10으로 설정합니다.
plt.rcParams["figure.figsize"] = [10,10]

# 이미지를 화면에 표시합니다.
plt.imshow(sun_im, 
           cmap = 'gray',           # 흑백 이미지일 경우 'gray' 컬러맵을 사용합니다.
           origin='upper',          # 이미지의 원점을 왼쪽 위로 설정합니다.
           interpolation = 'None')  # 보간(interpolation) 없이 이미지를 표시합니다.

# X, Y축의 눈금값(숫자)을 숨기고 싶을 때 아래 주석을 해제하세요.
# plt.xticks([]), plt.yticks([]) 

plt.show()  # 이미지를 화면에 출력합니다.

# %% code 78.
# 이미지에서 원(태양)을 검출하기 위해 HoughCircles 함수 사용
# sun_im: 입력 이미지 (흑백 이미지여야 함)
# cv2.HOUGH_GRADIENT: 허프 변환 방법 지정
# 2: 해상도 비율 (dp), 입력 이미지와 누적기(accumulator) 간의 비율
# 200: 원 중심 간 최소 거리 (픽셀 단위)
sun_circle = cv2.HoughCircles(sun_im, cv2.HOUGH_GRADIENT, 2, 200)

# 검출된 원 정보 출력 (x, y, r)
print("sun_circle: ", sun_circle)

# 검출된 첫 번째 원들의 정보 출력
print("sun_circle[0]: ", sun_circle[0])
print("sun_circle[0][0]: ", sun_circle[0][0])

# 첫 번째 원의 (x, y, r) 좌표 출력
print("sun_circle[0, 0, :]: ", sun_circle[0, 0, :])

# (x, y, r) 좌표와 반지름을 정수형으로 변환
sun_circle = np.round(sun_circle[0,0,:]).astype(int)
print('circle of sun', sun_circle )

# %% code 79.
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# sun_im: 태양 이미지 데이터 (예: 2차원 배열)
# sun_circle: (x, y, 반지름) 형태의 원 정보 (태양의 중심 좌표와 반지름)

# 1. 이미지를 화면에 출력
plt.imshow(
    sun_im,               # 출력할 이미지 데이터
    cmap='gray',          # 흑백(그레이스케일) 컬러맵 사용
    origin='upper',       # 이미지의 (0,0) 좌표를 왼쪽 위로 설정
    interpolation='None'  # 보간(interpolation) 없이 원본 픽셀 그대로 표시
)

# 2. 태양의 경계(원을) 그림
circle = Circle(
    (sun_circle[0], sun_circle[1]),  # 원의 중심 좌표 (x, y)
    sun_circle[2],                   # 원의 반지름
    facecolor='none',                # 원 내부는 투명하게 설정
    edgecolor=(0, 0.8, 0.8),         # 원의 테두리 색상 (청록색 계열)
    linewidth=2,                     # 테두리 두께
    alpha=0.5                        # 투명도(0: 완전 투명, 1: 불투명)
)

ax = plt.gca()        # 현재의 Axes 객체(좌표축)를 가져옴
ax.add_patch(circle)  # Axes에 원(circle) 패치 추가

plt.show()          # 화면에 이미지와 원을 함께 출력

# %% code 80.
# 이미지 복사본 생성 (원본 이미지를 보존하기 위해 복사본을 만듦)
sun_im_output = sun_im.copy()
print("sun_im_output: ", sun_im_output)

# 배경을 마스킹하기 위한 배열 생성
# np.ogrid를 사용하여 X, Y 좌표 그리드 생성
X, Y = np.ogrid[0:im_width, 0:im_height]

# 경계(림 다크닝 영역) 두께 설정
boundary_width = 40 # 태양 원의 경계 부분(림 다크닝)을 제거하기 위한 두께(픽셀 단위)

# 마스킹을 위한 불리언 배열 생성
# outer: 경계 바깥쪽(태양 원의 경계에서 boundary_width만큼 안쪽을 제외한 바깥 영역)
outer = (X - sun_circle[0]) ** 2 + (Y - sun_circle[1]) ** 2 > (sun_circle[2] - boundary_width) ** 2 

# inner: 경계 안쪽(태양 원의 경계에서 boundary_width만큼 안쪽 영역)
inner = (X - sun_circle[0]) ** 2 + (Y - sun_circle[1]) ** 2 < (sun_circle[2] - boundary_width) ** 2 

# 배열 타입 출력 (디버깅용)
print ("type(outer): ", type(outer))
print ("type(inner):", type(inner))

# 배열 크기 출력 (디버깅용)
print (np.shape(outer), np.shape(inner))

# outer 배열 값 출력 (디버깅용)
print ("outer:", outer)
# inner 배열 값 출력 (디버깅용)
print ("inner", inner)

# %% code 81.
# 8 bit image에서 흰색은 255이다. 
sun_im_output[outer] = 255

print ('boundary width :', boundary_width)

fig, ax = plt.subplots()

# 이미지 나타내기
plt.imshow(sun_im_output, 
           cmap = 'gray', 
           origin='upper',
           interpolation = 'None')

# 원 그리기
circle = Circle((sun_circle[0], sun_circle[1]), sun_circle[2], 
                facecolor='none',
                edgecolor=(0, 0.8, 0.8), linewidth=2, alpha=0.5)
ax.add_patch(circle) 

plt.show()

# %% code 82.
# 흑점(태양의 어두운 점)으로 예상되는 픽셀을 얻기 위한 코드

# 흑점으로 판단할 밝기 기준값 설정 (이 값보다 어두우면 흑점으로 간주)
bright_criterion = 70 

# 흑점 픽셀을 표시할 마스킹 배열 생성 (모든 값을 False로 초기화)
# shape는 (im_width, im_height)로, 이미지 크기와 동일
sunspot_mask  = np.zeros((im_width, im_height)).astype(bool)

# 흑점 후보 픽셀의 정보를 저장할 리스트 (각 원소는 [y, x, 밝기값])
check_pixel = []

# 이미지의 모든 픽셀을 하나씩 순회
for i in range(0, im_width):      # 행(y축, 세로) 방향으로 반복
    for j in range(0, im_height): # 열(x축, 가로) 방향으로 반복
 # 현재 픽셀의 밝기값이 기준값보다 작으면 (즉, 어두운 픽셀이면)
        if(sun_im_output[i,j] < bright_criterion):
            sunspot_mask[i,j] = 0  # sunspot_mask에서 해당 위치를 0(흑점)으로 표시
 # 흑점 후보 픽셀의 [y좌표, x좌표, 밝기값]을 리스트에 저장
            check_pixel.append([j, i, sun_im_output[i,j]]) 
        else : 
            sunspot_mask[i,j] = 1  # 밝은 픽셀은 1(비흑점)로 표시

# 흑점 후보로 선택된 픽셀의 개수 출력
print("len(check_pixel): ", len(check_pixel))
# 흑점 후보 픽셀의 좌표와 밝기값 출력
print("check_pixel: ", check_pixel)

# 흑점이 아닌(마스크가 1인) 픽셀은 흰색(255)으로 변경하여 이미지에서 제거
sun_im_output[sunspot_mask] = 255 
print("sun_im_output: ", sun_im_output)

# 시각화를 위한 figure, axis 객체 생성
fig, ax = plt.subplots() 

# 이미지 출력
plt.imshow(sun_im_output, 
           cmap = 'gray',          # 흑백(그레이스케일) 컬러맵 사용
           origin='upper',         # 이미지의 원점(0,0)이 왼쪽 위
           interpolation = 'None'  # 보간 없이 픽셀 그대로 표시
)

# 태양의 원을 이미지 위에 그리기
circle = Circle((sun_circle[0], sun_circle[1]), sun_circle[2], 
                facecolor='none',         # 원 내부는 투명
                edgecolor=(0, 0.8, 0.8),  # 원 테두리 색상 (청록색)
                linewidth=2,              # 테두리 두께
                alpha=0.5)                # 테두리 투명도
ax.add_patch(circle) # ax(좌표축)에 원 추가

# x, y축 눈금값 숨기기 (필요시 주석 해제)
#plt.xticks([]), plt.yticks([]) 

plt.show() # 그래프(이미지) 화면에 출력

# %% code 83.
# check_pixel을 numpy 배열로 변환
check_pixel = np.asarray(check_pixel)
print("check_pixel:", check_pixel)

# 이미지의 각 픽셀을 0으로 초기화한 2차원 리스트 생성 (im_height x im_width 크기)
image = [[0 for a in range(im_width)] for b in range(im_height)] 

# 리스트를 numpy 배열로 변환
image = np.array(image)

# 흑점(어두운 픽셀) 좌표에 해당하는 위치를 1로 변경
for i in check_pixel:
    image[i[0], i[1]] = 1

print("type(image): ", type(image))

# 그래프 그리기 위한 figure와 axes 객체 생성
fig, ax = plt.subplots()

# 이미지 출력
plt.imshow(image, 
           cmap = 'gray',           # 흑백 컬러맵 사용
           origin='upper',          # 이미지의 원점(0,0)을 왼쪽 위로 설정
           interpolation = 'None')  # 보간 없이 픽셀 그대로 표시

# 태양 원 그리기 (sun_circle = (x좌표, y좌표, 반지름))
circle = Circle((sun_circle[0], sun_circle[1]), sun_circle[2], 
                facecolor='none',         # 원 내부는 투명
                edgecolor=(0, 0.8, 0.8),  # 원 테두리 색상 (청록색 계열)
                linewidth=2,              # 테두리 두께
                alpha=0.5)                # 투명도 50%
ax.add_patch(circle)                             # 원을 axes에 추가

# 이미지와 원을 화면에 표시
plt.show()

# %% code 84.
fig, ax = plt.subplots()

# 이미지 나타내기
plt.imshow(image.T, 
           cmap = 'gray', 
           interpolation = 'None')

#원 그리기
circle = Circle((sun_circle[0], sun_circle[1]), sun_circle[2], 
                facecolor='none',
                edgecolor=(0, 0.8, 0.8), linewidth=2, alpha=0.5)
ax.add_patch(circle) 

# x, y축 눈금값 숨기기
#plt.xticks([]), plt.yticks([]) 

plt.show()

# %% code 85.
import math

# 태양 흑점의 위도(latitude)와 경도(longitude)를 계산하는 함수
def latitude(y):
 # y좌표를 이용해 위도를 계산 (아크사인 사용)
 # sun_circle[1]: 태양 원의 중심 y좌표, sun_circle[2]: 태양 원의 반지름
    return math.asin((sun_circle[1] - y) / sun_circle[2])

def longitude(x, y):
 # x, y좌표를 이용해 경도를 계산 (아크사인 사용)
 # 위도 계산 결과를 이용해 경도 계산
    return math.asin((x - sun_circle[0]) / (sun_circle[2] * math.cos(latitude(y))))

#######################################################
#### DFS(깊이 우선 탐색)에서 사용할 8방향 이동 벡터 정의 ####
# dx, dy는 각각 x, y방향으로 이동할 수 있는 값의 리스트
# (상, 우상, 우, 우하, 하, 좌하, 좌, 좌상)
dx = [0, 1, 1, 1, 0, -1, -1, -1]
dy = [1, 1, 0, -1, -1, -1, 0, 1]
#######################################################

# DFS(깊이 우선 탐색) 함수 정의
def dfs(x, y):
    global x_pixel_sum
    global y_pixel_sum
    global num_pixel
    image[x][y] = -1  # 방문한 픽셀은 -1로 표시하여 재방문 방지
    x_pixel_sum += x  # x좌표 누적합
    y_pixel_sum += y  # y좌표 누적합
    num_pixel += 1    # 픽셀 개수 카운트

 # 8방향으로 인접한 픽셀을 탐색
    for i in range(0, len(dx)):
 # 인접 픽셀이 흑점(1)인 경우 재귀적으로 DFS 호출
        if(image[x+dx[i]][y+dy[i]] == 1):
            dfs(x+dx[i], y+dy[i])
#######################################################

# 흑점으로 판단할 최소 픽셀 개수 기준
pixel_num_criterion = 2

# 흑점의 x, y 평균좌표와 픽셀 개수를 저장할 리스트
sunspot_data = []

# 이미지 전체를 순회하며 흑점(1) 픽셀을 찾음
for a in range(0, im_width):
    for b in range(0, im_height):
        if(image[a][b] == 1): # 흑점 픽셀 발견 시
            x_pixel_sum = 0
            y_pixel_sum = 0
            num_pixel = 0
            print('DFS...', a, b)
            dfs(a, b)                            # DFS로 연결된 흑점 픽셀 모두 탐색
            if num_pixel > pixel_num_criterion:  # 기준 이상 픽셀일 때만 흑점으로 인정
                x_average = x_pixel_sum / num_pixel  # x좌표 평균
                y_average = y_pixel_sum / num_pixel  # y좌표 평균
                latit = latitude(y_average)          # 위도 계산
                longi = longitude(x_average, y_average)  # 경도 계산
                latit = math.degrees(latit)          # 라디안 → 도(degree) 변환
                longi = math.degrees(longi)
 # 흑점의 경도, 위도, 픽셀 개수 저장 (주석 처리됨)
 # sunspot_data.append([longi, latit, num_pixel])
 # 흑점의 x, y 평균좌표, 픽셀 개수 저장
                sunspot_data.append([int(x_average), int(y_average), num_pixel])
print ('*'*80)
print ('number of sunspot : ', len(sunspot_data))  # 흑점 개수 출력
print ('sunspot data : ', sunspot_data)            # 흑점 데이터(x, y, 픽셀 개수) 출력

# %% code 86.
# sunspot_data를 numpy 배열로 변환
sunspot_data = np.asarray(sunspot_data)
print("sunspot_data:\n", sunspot_data)

# 만약 sunspot_data가 비어 있다면(태양흑점이 없다면)
if len(sunspot_data) == 0 : 
    print('There is no sunspot in the image')  # 흑점이 없다는 메시지 출력
else :
 # 그래프를 그릴 figure와 axis 객체 생성
    fig, ax = plt.subplots()
    
 # 태양 이미지를 불러와서 흑백(cmap='gray')으로 화면에 표시
    plt.imshow(sun_im, 
               cmap = 'gray', 
               interpolation = 'None')
    
 # 태양의 원을 그림 (sun_circle = (x, y, 반지름))
    circle = Circle((sun_circle[0], sun_circle[1]), sun_circle[2], 
                    facecolor='none',         # 내부는 투명
                    edgecolor=(0, 0.8, 0.8),  # 테두리 색상 (청록색 계열)
                    linewidth=3,              # 테두리 두께
                    alpha=0.5)                # 투명도
    ax.add_patch(circle)                             # 원을 axis에 추가    
    
 # 흑점 위치를 빨간색 점('ro')으로 표시, 크기는 3
    plt.plot(sunspot_data[:,0], 
             sunspot_data[:,1], 
             'ro', 
             markersize=3)
    
 # 결과 이미지를 파일로 저장
    plt.savefig(f'{str(fpaths[0].parents[0])}/{fpaths[0].stem}.png')
    print(f'{str(fpaths[0].parents[0])}/{fpaths[0].stem}.png is created...')

 # 그래프를 화면에 표시
    plt.show()
