# 지구과학 데이터 사이언스 1 | III-08. 색등급도 그리기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 103.
from pathlib import Path

# (HLA 데이터셋 이름, 파일 이름, 구글 드라이브 사본 ID)
files = [
('hst_11233_06_wfpc2_f814w_f450w_wf', 'hst_11233_06_wfpc2_multiwave_wf_daophot_trm.cat', '1aMI1vD-beXV788GMLI62aIQU6rKBPLjh'),
('hst_11233_06_wfpc2_f450w_wf', 'hst_11233_06_wfpc2_f450w_wf_daophot_trm.cat', '1FDmjaJUcYDVgaRBnTRH1iGMDrAzFKNGl'),
('hst_11233_06_wfpc2_f814w_wf', 'hst_11233_06_wfpc2_f814w_wf_daophot_trm.cat', '19fESuCZx0bZ2q87qN-MaGvwJJpTUo0hr')
]

for dataset, fname, fid in files:
    url = f"https://hla.stsci.edu/cgi-bin/getdata.cgi?dataset={dataset}&filename={fname}"
    try:  # 허블 레거시 아카이브에서 직접 받기
        du.download(url, Path(proj_dir) / fname)
    except Exception:  # 실패하면 구글 드라이브 사본
        du.download(f"https://docs.google.com/uc?export=download&id={fid}", Path(proj_dir) / fname)

# 이름순: [0] f450w, [1] f814w, [2] multiwave
fpaths = sorted(Path(proj_dir).glob('*.cat'))

# %% code 104.
n_lines = 40

print(f"파일 내용 출력 (처음 {n_lines}줄):")
print("="*40)

# 운영체제와 상관없이 읽기
try:
    with open(fpaths[2], encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= n_lines:
                break
            print(f"{i+1:3d}: {line.rstrip()}")
except UnicodeDecodeError:
    # UTF-8이 안 되면 CP949
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
du.preview_text(fpaths[2], n=50)

# %% code 106.
import numpy as np

# 데이터가 시작되는 줄 수(파일을 열어 확인)
skiprows = 35

DAO_array = np.loadtxt(
    f'{fpaths[2]}',
    comments='#',
    dtype=float,
    delimiter=None,  # 공백 여러 칸도 구분자
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

# 색등급도(CMD)
plt.plot(DAO_array[:,5]-DAO_array[:,6], DAO_array[:,5], 'o', ms=2, alpha=0.2)

# 등급 축 뒤집기(밝을수록 위)
plt.gca().invert_yaxis()

plt.show()

# %% code 109.
print("DAO_array[:,5].min(): {}".format(DAO_array[:,5].min()))
print("DAO_array[:,5].max(): {}".format(DAO_array[:,5].max()))
print("DAO_array[:,6].min(): {}".format(DAO_array[:,6].min()))
print("DAO_array[:,6].max(): {}".format(DAO_array[:,6].max()))
print("DAO_array[:,7].min(): {}".format(DAO_array[:,7].min()))
print("DAO_array[:,7].max(): {}".format(DAO_array[:,7].max()))
print("DAO_array[:,8].min(): {}".format(DAO_array[:,8].min()))
print("DAO_array[:,8].max(): {}".format(DAO_array[:,8].max()))

import numpy as np

num1 = np.arange(0, 11, 2)                   # [0, 2, 4, 6, 8, 10]
print("num1's elements:\n {}".format(num1))

# 마스킹 예
tf   = np.array([False, True, False, True, True, False])

print("tf:\n {}".format(tf))

print("num1's selected elements:\n {}".format(num1[tf]))  # tf가 True인 자리만

# 실제 자료에 마스킹
mask  = np.zeros(len(DAO_array)).astype(bool)

# -999는 측정 실패 표시
for i in range(0, len(DAO_array)):
    # 5~10번 열 중 하나라도 -999이면 제외
    if DAO_array[i, 5] == -999 or DAO_array[i, 6] == -999 \
        or DAO_array[i, 7] == -999 or DAO_array[i, 8] == -999 \
        or DAO_array[i, 9] == -999 or DAO_array[i, 10] == -999:
        mask[i]  = False
    else :
        mask[i]  = True
print("mask:\n {}".format(mask))
# 유효한 행만
DAO_array_masked = DAO_array[mask]      
print("DAO_array_masked.shape: {}".format(DAO_array_masked.shape))
print("DAO_array_masked[:5]:\n {}".format(DAO_array_masked[:5]))

# %% code 110.
import numpy as np
import matplotlib.pyplot as plt

# 색등급도(CMD)
plt.plot(DAO_array[mask,5]-DAO_array[mask,6], DAO_array[mask,5], 'o', ms=2, alpha=0.2)

# 등급 축 뒤집기(밝을수록 위)
plt.gca().invert_yaxis()

plt.show()

# %% code 111.
import numpy as np

ch1, ch2 = "F450", "F814"
data_type  = "WFPC2_WFC"
object_name = 'M80'

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10.5,8))

ax.plot(DAO_array[mask,5]-DAO_array[mask,6], DAO_array[mask,5], 'o', ms=2, alpha=0.2)

ax.set_xlabel('Color Index ({} - {})'.format(ch1, ch2), fontdict={'fontsize':14})
ax.set_ylabel('Magnitude ({})'.format(ch1), fontdict={'fontsize':14})

ax.set_title('C-M diagram of {} ({})'.format(object_name, data_type),
             fontdict={'fontsize':16})

ax.grid()
plt.gca().invert_yaxis()  # 등급 축 뒤집기

plt.annotate('using The Hubble Space Telescope data',
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

# -999(결측) 행 제외
for i in range(0, len(DAO_array)):
    if DAO_array[i, 5] == -999 or DAO_array[i, 6] == -999\
        or DAO_array[i, 7] == -999 or DAO_array[i, 8] == -999:
        mask[i] = False
    else:
        mask[i] = True

data_type1 = "WFPC2_MagAP2"
data_type2 = "WFPC2_TotMag"

fig = plt.figure(figsize=(12.0, 6.0))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

# 왼쪽: MagAP2 등급(5 · 6번 열), 오른쪽: TotMag 등급(7 · 8번 열)
ax1.plot(DAO_array[mask,5] - DAO_array[mask,6], DAO_array[mask,5], 'o', ms=2, alpha=0.2)
ax2.plot(DAO_array[mask,7] - DAO_array[mask,8], DAO_array[mask,7], 'o', ms=2, alpha=0.2)

ax1.set_xlabel(f'Color Index ({ch1} - {ch2})', fontdict={'fontsize':14})
ax1.set_ylabel(f'Magnitude ({ch1})', fontdict={'fontsize':14})
ax2.set_xlabel(f'Color Index ({ch1} - {ch2})', fontdict={'fontsize':14})
ax2.set_ylabel(f'Magnitude ({ch1})', fontdict={'fontsize':14})

ax1.invert_yaxis()
ax2.invert_yaxis()
ax1.grid()
ax2.grid()

ax1.set_title(f'C-M diagram of {object_name} ({data_type1})',
             fontdict={'fontsize':16})
ax2.set_title(f'C-M diagram of {object_name} ({data_type2})',
             fontdict={'fontsize':16})

plt.annotate('using The Hubble Space Telescope data',
        xy=(1, 0), xytext=(0, -50), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points')

plt.savefig(f'{proj_dir}/{object_name}_{data_type1}_{data_type2}_CMD.png',
            dpi=300, bbox_inches='tight')
print(f'{proj_dir}/{object_name}_{data_type1}_{data_type2}_CMD.png is created...')

plt.show()

# %% code 113.
import pandas as pd
import matplotlib.pyplot as plt

file_path = f'{fpaths[2]}'  # multiwave 파일
skiprows = 35               # 앞 설명 줄 수

df = pd.read_csv(
    file_path,
    sep=r'\s+',   # 공백 여러 칸이 구분자
    comment='#',  # '#' 줄은 건너뛰기
    header=None,
    skiprows=skiprows
)

# 5~8번 열에 -999가 있는 행 제외
mask = ~(
    (df[5] == -999) | (df[6] == -999) |
    (df[7] == -999) | (df[8] == -999)
)
df_masked = df[mask]

ch1, ch2 = "F606", "F814"     # 필터 이름
data_type1  = "WFPC2 WFC"
data_type2  = "WFPC2 TotMag"
object_name = 'M4'

fig = plt.figure(figsize=(12.0, 6.0))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

# 왼쪽: MagAP2 등급
ax1.plot(df_masked[5] - df_masked[6], df_masked[5], 'o', ms=2, alpha=0.2)
ax1.set_xlabel(f'Color Index ({ch1} - {ch2})', fontsize=14)
ax1.set_ylabel(f'Magnitude ({ch1})', fontsize=14)
ax1.set_title(f'C-M diagram of {object_name} ({data_type1})', fontsize=16)
ax1.invert_yaxis()                                 # 등급이 작을수록 밝으므로 y축 반전
ax1.grid()

# 오른쪽: TotMag 등급
ax2.plot(df_masked[7] - df_masked[8], df_masked[7], 'o', ms=2, alpha=0.2)
ax2.set_xlabel(f'Color Index ({ch1} - {ch2})', fontsize=14)
ax2.set_ylabel(f'Magnitude ({ch1})', fontsize=14)
ax2.set_title(f'C-M diagram of {object_name} ({data_type2})', fontsize=16)
ax2.invert_yaxis()
ax2.grid()

# 아래쪽에 출처 표기
plt.annotate('using The Hubble Space Telescope data',
        xy=(1, 0), xytext=(0, -50), va='top', ha='right',
        xycoords='axes fraction', textcoords='offset points')

plt.show()

# %% code 114.
n_lines = 65

print(f"파일 내용 출력 (처음 {n_lines}줄):")
print("="*40)

# 운영체제와 상관없이 읽기
try:
    with open(fpaths[0], encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= n_lines:
                break
            print(f"{i+1:3d}: {line.rstrip()}")
except UnicodeDecodeError:
    # UTF-8이 안 되면 CP949
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
n_lines = 65

print(f"파일 내용 출력 (처음 {n_lines}줄):")
print("="*40)

# 운영체제와 상관없이 읽기
try:
    with open(fpaths[1], encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= n_lines:
                break
            print(f"{i+1:3d}: {line.rstrip()}")
except UnicodeDecodeError:
    # UTF-8이 안 되면 CP949
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
print(f"파일 {fpaths[0]}의 첫 65줄을 출력합니다:")
du.preview_text(fpaths[0], n=65)

# %% code 117.
# print(f"파일 {fpaths[1]}의 첫 65줄을 출력합니다:")
# du.preview_text(fpaths[1], n=65)

# %% code 118.
import numpy as np

# 데이터가 시작되는 줄 수(파일을 열어 확인)
skiprows = 60

F450_array = np.loadtxt(
    f'{fpaths[0]}',
    comments='#',
    dtype=float,
    delimiter=None,  # 공백 여러 칸도 구분자
    skiprows=skiprows
)

F814_array = np.loadtxt(
    f'{fpaths[1]}', comments='#', dtype=float, delimiter=None,
    skiprows=skiprows
)
print("type(F450_array):", type(F450_array))
print("type(F814_array):", type(F814_array))
print("F450_array[1, :]: {}".format(F450_array[1, :]))
print("F814_array[1, :]: {}".format(F814_array[1, :]))  

# %% code 119.
print("F450.shape: {}".format(F450_array.shape))
print("F814.shape: {}".format(F814_array.shape))
print("F450[:,4:6]: {}".format(F450_array[:,4:6]))
print("F814[:,4:6]: {}".format(F814_array[:,4:6]))

# %% code 120.
import numpy as np

mask = np.zeros(len(F450_array)).astype(bool)  # True: 쓸 별
color = np.zeros(len(F450_array))              # 색지수

# 두 필터 목록에서 ID가 같은 별 짝짓기
for i in range(0, len(F450_array)):
    ID_ch1 = F450_array[i, 4]  # 4번 열: 별 ID
    for j in range(0, len(F814_array)):
        ID_ch2 = F814_array[j, 4]
        if ID_ch1 == ID_ch2:
            mask[i] = True
            # 색지수 = F450 등급 - F814 등급
            color[i] = F450_array[i, 5] - F814_array[j, 5]
            break  # 찾으면 다음 별로

print("len(color):{}".format(len(color)))
print("len(F450[mask]):{}".format(len(F450_array[mask])))
print("len(color):{}".format(len(color)))
print("len(color[mask]):{}".format(len(color[mask])))

# %% code 121.
color[mask]

# %% code 122.
import numpy as np
import matplotlib.pyplot as plt

# 색등급도(CMD)
plt.plot(color[mask], F450_array[mask, 5], 'o', ms=2, alpha=0.2)

# 등급 축 뒤집기(밝을수록 위)
plt.gca().invert_yaxis()

plt.show()
