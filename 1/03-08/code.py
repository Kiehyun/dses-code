# 지구과학 데이터 사이언스 1 | III-08. 색등급도 그리기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 103.
from pathlib import Path

# 구글 드라이브 파일 ID와 저장할 파일 이름
files = [
('1aMI1vD-beXV788GMLI62aIQU6rKBPLjh', 'hst_11233_06_wfpc2_multiwave_wf_daophot_trm.cat'),
('1FDmjaJUcYDVgaRBnTRH1iGMDrAzFKNGl', 'hst_11233_06_wfpc2_f450w_wf_daophot_trm.cat'),
('19fESuCZx0bZ2q87qN-MaGvwJJpTUo0hr', 'hst_11233_06_wfpc2_f814w_wf_daophot_trm.cat')
]

for file_id, output_path in files:
    du.download(f"https://docs.google.com/uc?export=download&id={file_id}", Path(proj_dir) / output_path)

# 다운로드한 파일 목록 (이름순: f450w, f814w, multiwave)
fpaths = sorted(Path(proj_dir).glob('*.cat'))

# %% code 104.
n_lines = 40  # 출력할 줄 수

print(f"파일 내용 출력 (처음 {n_lines}줄):")
print("="*40)

# 순수 파이썬으로 구현 (운영체제 무관)
try:
    with open(fpaths[2], encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= n_lines:
                break
            print(f"{i+1:3d}: {line.rstrip()}")
except UnicodeDecodeError:
 # UTF-8로 읽기 실패시 다른 인코딩 시도
    try:
        with open(fpaths[2], encoding='cp949') as f:
            for i, line in enumerate(f):
                if i >= n_lines:
                    break
                print(f"{i+1:3d}: {line.rstrip()}")
    except Exception as e2:
        print(f"파일 읽기 실패 (UTF-8, CP949 모두 실패): {e2}")
except Exception as e:
    print(f"파일 읽기 실패: {e}")

print("="*60)

# %% code 105.
print(f"파일 {fpaths[2]}의 첫 50줄을 출력합니다:")
du.preview_text(fpaths[2], n=50)  # 파일의 첫 50줄을 출력 (OS 무관)

# %% code 106.
import numpy as np

# 파일의 실제 데이터가 시작되는 줄 번호를 확인하세요!
# 예시: skiprows=35 (파일을 직접 열어서 데이터가 시작되는 줄을 확인)
skiprows = 35  # 필요에 따라 조정

DAO_array = np.loadtxt(
    f'{fpaths[2]}',
    comments='#',
    dtype=float,     # 숫자 데이터만 읽을 때 float 권장
    delimiter=None,  # 여러 공백을 모두 구분자로 인식
    skiprows=skiprows
)

print("type(DAO_array):", type(DAO_array))
print("DAO_array.shape:", DAO_array.shape)

# %% code 107.
# 행 방향 슬라이싱
print("DAO_array[1, :]: {}".format(DAO_array[1, :]))

# 열 방향 슬라이싱
print("DAO_array[:, 1]: {}".format(DAO_array[:, 1]))

print("CI:\n {}".format(DAO_array[:,5]-DAO_array[:,6]))

# %% code 108.
import numpy as np
import matplotlib.pyplot as plt

#색등급도(CMD) 그리기
plt.plot(DAO_array[:,5]-DAO_array[:,6], DAO_array[:,5], 'o', ms=2, alpha=0.2)

# 등급의 축은 반대로
plt.gca().invert_yaxis()

#단열선도 출력
plt.show()

# %% code 109.
# DAO_array의 여러 컬럼(등급 데이터 등)의 최소값과 최대값을 출력합니다.
print("DAO_array[:,5].min(): {}".format(DAO_array[:,5].min()))   # 6번째 열(F606 등급 등)의 최소값
print("DAO_array[:,5].max(): {}".format(DAO_array[:,5].max()))   # 6번째 열의 최대값
print("DAO_array[:,6].min(): {}".format(DAO_array[:,6].min()))   # 7번째 열(F814 등급 등)의 최소값
print("DAO_array[:,6].max(): {}".format(DAO_array[:,6].max()))   # 7번째 열의 최대값
print("DAO_array[:,7].min(): {}".format(DAO_array[:,7].min()))   # 8번째 열의 최소값
print("DAO_array[:,7].max(): {}".format(DAO_array[:,7].max()))   # 8번째 열의 최대값
print("DAO_array[:,8].min(): {}".format(DAO_array[:,8].min()))   # 9번째 열의 최소값
print("DAO_array[:,8].max(): {}".format(DAO_array[:,8].max()))   # 9번째 열의 최대값

import numpy as np

# 0부터 10까지 2씩 증가하는 정수 배열을 생성합니다. (0, 2, 4, 6, 8, 10)
num1 = np.arange(0, 11, 2)                   # [0, 2, 4, 6, 8, 10] 생성
print("num1's elements:\n {}".format(num1))  # num1 배열의 원소들을 출력

# 마스킹(Masking) 예제
tf   = np.array([False, True, False, True, True, False])  # 불리언 배열 생성

print("tf:\n {}".format(tf))  # 마스크 배열 출력

# 불리언 마스킹을 이용해 True인 위치의 값만 선택하여 출력
print("num1's selected elements:\n {}".format(num1[tf]))  # num1에서 tf가 True인 값만 출력

# 실제 데이터에 마스킹 적용 예시
# DAO_array의 행 개수만큼 False로 초기화된 불리언 배열 생성 (모든 값이 False)
mask  = np.zeros(len(DAO_array)).astype(bool)

# "-999" 값이 포함된 행을 찾아서 마스킹 처리
for i in range(0, len(DAO_array)):
 # 6~11번째 열(파이썬 인덱스 5~10) 중 하나라도 -999이면 측정 오류로 간주하여 False로 설정
    if DAO_array[i, 5] == -999 or DAO_array[i, 6] == -999 \
        or DAO_array[i, 7] == -999 or DAO_array[i, 8] == -999 \
        or DAO_array[i, 9] == -999 or DAO_array[i, 10] == -999:
 # 해당 행에 -999가 있으면 사용하지 않음
        mask[i]  = False
    else :
 # 모든 값이 정상(오류 없음)이면 True로 설정하여 사용할 데이터로 마스킹
        mask[i]  = True
# 마스킹된 데이터 출력
print("mask:\n {}".format(mask))  # 마스크 배열 출력    
# 마스킹된 데이터를 이용해 DAO_array에서 유효한 데이터만 선택
DAO_array_masked = DAO_array[mask]      
print("DAO_array_masked.shape: {}".format(DAO_array_masked.shape))  # 마스킹된 배열의 크기 출력     
# 마스킹된 데이터의 첫 5행 출력
print("DAO_array_masked[:5]:\n {}".format(DAO_array_masked[:5]))  # 마스킹된 배열의 첫 5행 출력

# %% code 110.
import numpy as np
import matplotlib.pyplot as plt

#색등급도(CMD) 그리기
plt.plot(DAO_array[mask,5]-DAO_array[mask,6], DAO_array[mask,5], 'o', ms=2, alpha=0.2)

# 등급의 축은 반대로
plt.gca().invert_yaxis()

#단열선도 출력
plt.show()

# %% code 111.
import numpy as np

ch1, ch2 = "F450", "F814"
data_type  = "WFPC2_WFC"
object_name = 'M80'

#색등급도(CMD) 그리기
import matplotlib.pyplot as plt

#차트 크기 설정
fig, ax = plt.subplots(figsize=(10.5,8))

ax.plot(DAO_array[mask,5]-DAO_array[mask,6], DAO_array[mask,5], 'o', ms=2, alpha=0.2)

# Y축 제목
ax.set_xlabel('Color Index ({} - {})'.format(ch1, ch2), fontdict={'fontsize':14})
ax.set_ylabel('Magnitude ({})'.format(ch1), fontdict={'fontsize':14})

# 차트 제목 폰트 크기 크게
ax.set_title('C-M diagram of {} ({})'.format(object_name, data_type),
             fontdict={'fontsize':16})

ax.grid()
plt.gca().invert_yaxis()

plt.annotate('using The Hubble space telescope data',
        xy=(1, 0), xytext=(0, -50), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points')

plt.savefig(f'{proj_dir}/{object_name}_{data_type}_CMD.png',
            dpi=300, bbox_inches='tight')
print(f'{proj_dir}/{object_name}_{data_type}_CMD.png is created...')

plt.show()

# %% code 112.
ch1, ch2 = "F450", "F814"
data_type = "WFPC2_WFC"
object_name = 'M80'

# 결측값(-999) 확인
for i in range(0, len(DAO_array)):
    if DAO_array[i, 5] == -999 or DAO_array[i, 6] == -999\
        or DAO_array[i, 7] == -999 or DAO_array[i, 8] == -999:
        mask[i] = False
    else:
        mask[i] = True

# 자료형 변수 정의 추가
data_type1 = "WFPC2_MagAP2"
data_type2 = "WFPC2_TotMag"

fig = plt.figure(figsize=(12.0, 6.0))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.plot(DAO_array[mask,5] - DAO_array[mask,6], DAO_array[mask,5], 'o', ms=2, alpha=0.2)
ax2.plot(DAO_array[mask,7] - DAO_array[mask,8], DAO_array[mask,7], 'o', ms=2, alpha=0.2)

# 문법 오류 수정: 백틱(`) 제거하고 대시(-) 추가
ax1.set_xlabel(f'Color Index ({ch1} - {ch2})', fontdict={'fontsize':14})
ax1.set_ylabel(f'Magnitude ({ch1})', fontdict={'fontsize':14})
ax2.set_xlabel(f'Color Index ({ch1} - {ch2})', fontdict={'fontsize':14})
ax2.set_ylabel(f'Magnitude ({ch1})', fontdict={'fontsize':14})

ax1.invert_yaxis()
ax2.invert_yaxis()
ax1.grid()
ax2.grid()

# 차트 제목 폰트 크기 크게
ax1.set_title(f'C-M diagram of {object_name} ({data_type1})',
             fontdict={'fontsize':16})
ax2.set_title(f'C-M diagram of {object_name} ({data_type2})',
             fontdict={'fontsize':16})

plt.annotate('created by guitar79@gs.hs.kr\nusing The Hubble space telescope data',
        xy=(1, 0), xytext=(0, -50), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points')

plt.savefig(f'{proj_dir}/{object_name}_{data_type1}_{data_type2}_CMD.png',
            dpi=300, bbox_inches='tight')
print(f'{proj_dir}/{object_name}_{data_type1}_{data_type2}_CMD.png is created...')

plt.show()

# %% code 113.
import pandas as pd
import matplotlib.pyplot as plt

# 파일 경로와 헤더 스킵 줄 수를 지정합니다.
file_path = f'{fpaths[2]}'  # 예시: multiwave 파일 경로
skiprows = 35               # 데이터가 시작되는 줄 번호 (파일 구조에 따라 조정)

# 데이터프레임으로 파일을 읽어옵니다.
df = pd.read_csv(
    file_path,
    sep=r'\s+',           # 공백을 구분자로 사용
    comment='#',            # '#'로 시작하는 주석 행은 무시
    header=None,            # 헤더(컬럼명) 없음
    skiprows=skiprows       # 헤더 및 설명 줄 건너뜀
)

# -999 값이 포함된 행을 제거합니다. (5~8번째 컬럼: 5,6,7,8 인덱스)
mask = ~(
    (df[5] == -999) | (df[6] == -999) |
    (df[7] == -999) | (df[8] == -999)
)
df_masked = df[mask]  # 유효한 데이터만 남김

# 그래프에 사용할 변수 설정
ch1, ch2 = "F606", "F814"     # 필터 이름
data_type1  = "WFPC2 WFC"     # 첫 번째 자료형(예: MagAP2)
data_type2  = "WFPC2 TotMag"  # 두 번째 자료형(예: TotMag)
object_name = 'M4'            # 관측 대상 이름

# 그래프 크기 및 2개의 서브플롯 생성
fig = plt.figure(figsize=(12.0, 6.0))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

# 첫 번째 CMD (MagAP2 등급 사용)
ax1.plot(df_masked[5] - df_masked[6], df_masked[5], 'o', ms=2, alpha=0.2)
ax1.set_xlabel(f'Color Index ({ch1} - {ch2})', fontsize=14)  # x축: 색지수
ax1.set_ylabel(f'Magnitude ({ch1})', fontsize=14)  # y축: 등급
ax1.set_title(f'C-M diagram of {object_name} ({data_type1})', fontsize=16)  # 제목
ax1.invert_yaxis()                                 # 등급이 작을수록 밝으므로 y축 반전
ax1.grid()                                         # 격자 표시

# 두 번째 CMD (TotMag 등급 사용)
ax2.plot(df_masked[7] - df_masked[8], df_masked[7], 'o', ms=2, alpha=0.2)
ax2.set_xlabel(f'Color Index ({ch1} - {ch2})', fontsize=14)  # x축: 색지수
ax2.set_ylabel(f'Magnitude ({ch1})', fontsize=14)  # y축: 등급
ax2.set_title(f'C-M diagram of {object_name} ({data_type2})', fontsize=16)  # 제목
ax2.invert_yaxis()                                 # 등급이 작을수록 밝으므로 y축 반전
ax2.grid()                                         # 격자 표시

# 그래프 하단에 주석 추가
plt.annotate('created by guitar79@gs.hs.kr\n using The Hubble space telescope data',
        xy=(1, 0), xytext=(0, -50), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points')

# 그래프 출력
plt.show()

# %% code 114.
n_lines = 65  # 출력할 줄 수

print(f"파일 내용 출력 (처음 {n_lines}줄):")
print("="*40)

# 순수 파이썬으로 구현 (운영체제 무관)
try:
    with open(fpaths[0], encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= n_lines:
                break
            print(f"{i+1:3d}: {line.rstrip()}")
except UnicodeDecodeError:
 # UTF-8로 읽기 실패시 다른 인코딩 시도
    try:
        with open(fpaths[0], encoding='cp949') as f:
            for i, line in enumerate(f):
                if i >= n_lines:
                    break
                print(f"{i+1:3d}: {line.rstrip()}")
    except Exception as e2:
        print(f"파일 읽기 실패 (UTF-8, CP949 모두 실패): {e2}")
except Exception as e:
    print(f"파일 읽기 실패: {e}")

print("="*60)

# %% code 115.
n_lines = 65  # 출력할 줄 수

print(f"파일 내용 출력 (처음 {n_lines}줄):")
print("="*40)

# 순수 파이썬으로 구현 (운영체제 무관)
try:
    with open(fpaths[1], encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= n_lines:
                break
            print(f"{i+1:3d}: {line.rstrip()}")
except UnicodeDecodeError:
 # UTF-8로 읽기 실패시 다른 인코딩 시도
    try:
        with open(fpaths[1], encoding='cp949') as f:
            for i, line in enumerate(f):
                if i >= n_lines:
                    break
                print(f"{i+1:3d}: {line.rstrip()}")
    except Exception as e2:
        print(f"파일 읽기 실패 (UTF-8, CP949 모두 실패): {e2}")
except Exception as e:
    print(f"파일 읽기 실패: {e}")

print("="*60)

# %% code 116.
print(f"파일 {fpaths[0]}의 첫 65줄을 출력합니다:")  # fpaths[0]에 저장된 파일의 이름을 출력합니다.
du.preview_text(fpaths[0], n=65)         # 파일의 첫 65줄을 출력 (OS 무관)

# %% code 117.
# print(f"파일 {fpaths[1]}의 첫 65줄을 출력합니다:")
# du.preview_text(fpaths[1], n=65)

# %% code 118.
import numpy as np

# 파일의 실제 데이터가 시작되는 줄 번호를 확인하세요!
# 예시: skiprows=35 (파일을 직접 열어서 데이터가 시작되는 줄을 확인)
skiprows = 60  # 필요에 따라 조정

F450_array = np.loadtxt(
    f'{fpaths[0]}',
    comments='#',
    dtype=float,     # 숫자 데이터만 읽을 때 float 권장
    delimiter=None,  # 여러 공백을 모두 구분자로 인식
    skiprows=skiprows
)

F814_array = np.loadtxt(
    f'{fpaths[1]}',
    comments='#',
    dtype=float,     # 숫자 데이터만 읽을 때 float 권장
    delimiter=None,  # 여러 공백을 모두 구분자로 인식
    skiprows=skiprows
)
# F450_array와 F814_array의 타입 출력
print("type(F450_array):", type(F450_array))
print("type(F814_array):", type(F814_array))
# F450_array의 두 번째 행(인덱스 1) 출력
print("F450_array[1, :]: {}".format(F450_array[1, :]))
# F814_array의 두 번째 행(인덱스 1) 출력
print("F814_array[1, :]: {}".format(F814_array[1, :]))  

# %% code 119.
print("F450.shape: {}".format(F450_array.shape))
print("F814.shape: {}".format(F814_array.shape))
print("F450[:,4:6]: {}".format(F450_array[:,4:6]))
print("F814[:,4:6]: {}".format(F814_array[:,4:6]))

# %% code 120.
import numpy as np

# 실제 데이터에 마스킹 적용 예시
# F450_array의 행 개수만큼 False로 초기화된 불리언 배열 생성 (모든 값이 False)
mask = np.zeros(len(F450_array)).astype(bool)  # 마스크 배열 (True: 사용할 데이터, False: 제외)
color = np.zeros(len(F450_array))              # 색지수(CI) 값을 저장할 배열

# 두 파장대(F450, F814)에서 같은 ID를 가진 별만 선별하여 마스킹 및 색지수 계산
for i in range(0, len(F450_array)):
    ID_ch1 = F450_array[i, 4]  # F450 데이터의 5번째 열(ID)
    for j in range(0, len(F814_array)):
        ID_ch2 = F814_array[j, 4]  # F814 데이터의 5번째 열(ID)
        if ID_ch1 == ID_ch2:       # 두 데이터에서 ID가 같으면
            mask[i] = True  # 해당 별을 사용할 데이터로 표시
 # 색지수(CI) 계산: F450 등급 - F814 등급
            color[i] = F450_array[i, 5] - F814_array[j, 5]
            break  # 일치하는 ID를 찾으면 더 이상 비교하지 않고 다음 별로 이동

# 마스킹 및 색지수 계산 결과 출력
print("len(color):{}".format(len(color)))  # 전체 color 배열 길이
print("len(F450[mask]):{}".format(len(F450_array[mask])))  # 마스킹된 F450 데이터 개수
print("len(color):{}".format(len(color)))  # 전체 color 배열 길이(중복)
print("len(color[mask]):{}".format(len(color[mask])))  # 마스킹된 color 데이터 개수

# %% code 121.
color[mask]

# %% code 122.
import numpy as np
import matplotlib.pyplot as plt

#색등급도(CMD) 그리기
plt.plot(color[mask], F450_array[mask, 5], 'o', ms=2, alpha=0.2)

# 등급의 축은 반대로
plt.gca().invert_yaxis()

#단열선도 출력
plt.show()
