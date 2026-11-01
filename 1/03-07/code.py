# 지구과학 데이터 사이언스 1 | III-07. H-R도 그리기(히파르코스 성표)
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 87.
from pathlib import Path

fname = "asu.tsv"
fid = "1e-LMG8Q3HBIRphwxiLabUs9bkB5dQODE"

# 구글 드라이브에 미리 저장해 둔 파일 내려받기
url = f"https://docs.google.com/uc?export=download&id={fid}"
du.download(url, Path(proj_dir) / fname)

# %% code 88.
# pathlib을 사용하여 지정한 폴더 내의 .tsv 파일 목록을 확인하는 코드입니다.
from pathlib import Path 
fpaths = sorted(list(Path(proj_dir).glob('*.tsv')))
print(f"fpaths: {fpaths}")            # .tsv 파일들의 전체 경로 리스트를 출력합니다.
print(f"len(fpaths): {len(fpaths)}")  # .tsv 파일의 개수를 출력합니다.

# %% code 89.
n_lines = 40  # 출력할 줄 수

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

# %% code 90.
import numpy as np
import pandas as pd

# HIP catalogue 파일을 읽어서 Pandas DataFrame으로 만듭니다.
# - 파일의 앞부분 35행은 설명이므로 skiprows=35로 건너뜁니다.
# - 데이터 구분자는 세미콜론(;)입니다.
# - 컬럼 이름은 'HIP', 'Vmag', 'Plx', 'B-V', 'SpType'로 지정합니다.
# - 첫 번째 컬럼(HIP)을 인덱스로 사용합니다.
df = pd.read_table(fpaths[0], skiprows=35, sep=';', header=None, index_col=0,
                   names = ['HIP', 'Vmag', 'Plx', 'B-V', 'SpType'],
                   engine='python')

print(f"df.shape:\n{df.shape}")
print(f"df:\n", df)

# %% code 91.
# 한 컬럼씩 시리즈로 반환하여 확인 데이터 확인
print("df[['Vmag', 'Plx', 'B-V']]:\n", df[['Vmag', 'Plx', 'B-V']])
# 자료형 확인
print("type(df['Vmag'][1]), type(df['Plx'][1]), type(df_clean['B-V'][1]):", 
        type(df['Vmag'][1]), type(df['Plx'][1]), type(df['B-V'][1])) 

# %% code 92.
# 데이터프레임의 요약 통계(describe) 출력
print("df.describe() :", df.describe())

# 각 셀의 문자열 양쪽 공백을 제거하는 람다 함수 정의
f = lambda x: x.str.strip()
print("type(f)", type(f))
print("f", f)

# 데이터프레임의 모든 셀에 공백 제거 함수 적용
df_clean = df.apply(f)

# 빈 문자열을 np.nan으로 변환
df_clean = df_clean.replace('', np.nan)

# NaN이 포함된 행 제거
df_clean = df_clean.dropna()

print('***NaN 값이 제거된 후 df_clean에 대한 describe 결과***')
# NaN이 제거된 데이터프레임의 요약 통계 출력
print("df_clean.describe():\n", df_clean.describe())

# 문자열을 실수형(float64)으로 변환 (빈 문자열/공백/NaN 처리 후 변환)
df_clean['Vmag'] = df_clean['Vmag'].astype(np.float64)
df_clean['Plx'] = df_clean['Plx'].astype(np.float64)
df_clean['B-V'] = df_clean['B-V'].astype(np.float64)

# 변환된 자료형 확인 (float64로 잘 변환되었는지 확인)
print("type(df_clean['Vmag'][1]), type(df_clean['Plx'][1]), type(df_clean['B-V'][1]) :", 
      type(df_clean['Vmag'][1]), type(df_clean['Plx'][1]), type(df_clean['B-V'][1]))

# %% code 93.
# 절대등급(M_V) 계산하여 새로운 컬럼으로 추가
df_clean['M_V'] = df_clean['Vmag'] + 5 * np.log10(df_clean['Plx']/100.)

# df_clean 데이터프레임 전체 출력
print("df_clean:\n", df_clean)

# %% code 94.
# 알파벳+숫자(예: G8, F5) 형태가 아닌 행은 제거합니다.
f = lambda s: (len(s) >= 2) and (s[0].isalpha()) and (s[1].isdigit())  # 첫 글자가 알파벳이고 두 번째 글자가 숫자인지 확인
i = df_clean['SpType'].apply(f)  # 조건을 만족하는 행만 True로 반환
df_clean = df_clean[i]           # 조건을 만족하는 행만 남김
print("df_clean after SpType filtering:\n", df_clean)  # 필터링 후 데이터프레임 출력

# %% code 95.
# 'SpType' 컬럼에서 앞 두 글자를 추출하여 'SpType2'라는 새로운 컬럼에 저장합니다.
f = lambda s: s[0:2]
df_clean['SpType2'] = df_clean['SpType'].apply(f)

print("df_clean:\n", df_clean)

# 'SpType' 컬럼에서 첫 번째 글자(분광형)를 추출하여 분류합니다.
f = lambda s: s[0]
clases = df_clean['SpType'].map(f)

# 각 분광형별로 별의 개수를 세어 출력합니다.
print('***df_clean에서 각 분광형별 개수 세기***')
print(clases.value_counts())

# %% code 96.
# 'SpType' 컬럼의 첫 글자가 OBAFGKM에 해당하는 별만 남깁니다.
f = lambda s: s[0] in 'OBAFGKM'
df_clean = df_clean[df_clean['SpType'].map(f)]

# 'SpType' 컬럼의 첫 글자(분광형)만 추출합니다.
f = lambda s: s[0]
clases = df_clean['SpType'].map(f)

# 각 분광형별로 별의 개수를 출력합니다.
print('***df_clean에서 각 분광형별 개수 세기***')
print(clases.value_counts())

# %% code 97.
# df_clean을 "HIP_clean.csv" 파일로 저장합니다.
df_clean.to_csv(Path(proj_dir) / "HIP_clean.csv")
print(f"df_clean is saved to {Path(proj_dir) / 'HIP_clean.csv'}")

# 분광형의 순서를 정렬하기 위한 딕셔너리입니다.
orden = {'O':'0', 'B':'1', 'A':'2', 'F':'3', 'G':'4', 'K':'5', 'M':'6'}

# 'SpType2' 컬럼의 첫 글자를 분광형 순서에 맞는 숫자로 변환하고, 두 번째 글자(숫자)와 결합합니다.
f = lambda s: orden[s[0]]+s[1]
df_clean['SpType2'] = df_clean['SpType2'].apply(f)

print("df_clean:\n", df_clean)

# %% code 98.
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6,8))

# 분광형(SpType2)을 가로축, 절대등급(M_V)을 세로축으로 산점도 그리기
ax.scatter(df_clean['SpType2'].astype(np.int32), df_clean['M_V'],
           s=50, edgecolors='none', alpha=0.015, c='k')

# 가로축, 세로축 범위 설정
ax.set_xlim(0, 70)
ax.set_ylim(15, -10)
ax.grid()
ax.tick_params(axis='both', labelsize=14)

# 분광형에 맞는 x축 눈금과 레이블 설정
ax.set_xticks(range(5,75,10))
ax.set_xticklabels(['O', 'B', 'A', 'F', 'G', 'K', 'M'])

# 그래프 제목 및 축 레이블 설정
ax.set_title('H-R Diagram \n (Hipparcos catalog)',
             fontsize=16)
ax.set_xlabel('spectral class',
             fontsize=16)
ax.set_ylabel('Absolute magnitude (M_v)',
             fontsize=16)

plt.show()

# %% code 99.
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6,8))

# 산점도 그리기: x축은 색지수(B-V), y축은 절대등급(M_V)
ax.scatter(df_clean['B-V'], df_clean['M_V'],
           # 점 크기 50, 테두리 없음, 투명도 0.015, 색상 검정
           #s=50, edgecolors='none', alpha=0.015, c='k')
           s=1, edgecolors='none', c='k')  # 점 크기 1, 테두리 없음, 색상 검정

# x축, y축 범위 설정
ax.set_xlim(-0.5, 2.5)
ax.set_ylim(15, -10)
ax.grid()                                  # 격자 표시
ax.tick_params(axis='both', labelsize=14)  # 축 눈금 폰트 크기

# 그래프 제목 및 축 레이블 설정
ax.set_title('H-R Diagram \n (Hipparcos catalog)', fontsize=16)
ax.set_xlabel('Color index(B-V)', fontsize=12)
ax.set_ylabel('Absolute magnitude (M_v)', fontsize=12)

plt.show()

# %% code 100.
# 'SpType' 컬럼에 'I' 또는 'V'가 포함된 별을 찾는 람다 함수입니다.
f = lambda s: ('I' in s) or ('V' in s)
b = df_clean['SpType'].map(f)  # 각 별의 분광형에 대해 조건을 적용하여 불리언 시리즈 생성
print("b:", b)                 # 조건에 해당하는지 여부를 출력
print("sum(b):", sum(b))       # 조건에 해당하는 별의 개수를 출력

# %% code 101.
# Class VII: 백색왜성(white dwarfs) 개수 출력
f = lambda s: 'VII' in s
b = df_clean['SpType'].map(f)
print ("Class VII: white dwarfs, there are %d stars" %sum(b))

# Class VI: 준왜성(subdwarfs) 개수 출력 ('VI'는 포함, 'VII'는 제외)
f = lambda s: ('VI' in s) and ('VII' not in s)
b = df_clean['SpType'].map(f)
print ("Class VI: subdwarfs, there are %d stars" %sum(b))

# Class V: 주계열성(main-sequence) 개수 출력 ('V'는 포함, 'VI', 'IV'는 제외)
f = lambda s: ('V' in s) and ('VI' not in s) and ('IV' not in s)
b = df_clean['SpType'].map(f)
print ("Class V: main-sequence, there are %d stars" %sum(b))

# Class IV: 준거성(subgiants) 개수 출력
f = lambda s: 'IV' in s
b = df_clean['SpType'].map(f)
print ("Class IV: subgiants, there are %d stars" %sum(b))

# Class III: 거성(giants) 개수 출력
f = lambda s: 'III' in s
b = df_clean['SpType'].map(f)
print ("Class III: giants, there are %d stars" %sum(b))

# Class II: 밝은 거성(bright giants) 개수 출력 ('II'는 포함, 'III', 'VII'는 제외)
f = lambda s: ('II' in s) and ('III' not in s) and ('VII' not in s)
b = df_clean['SpType'].map(f)
print ("Class II:  bright giants, there are %d stars" %sum(b))

# Class I: 초거성(supergiants) 개수 출력 ('I'는 포함, 'II', 'V'는 제외)
f = lambda s: ('I' in s) and ('II' not in s) and ('V' not in s)
b = df_clean['SpType'].map(f)
print ("Class I: supergiants, there are %d stars" %sum(b))

# %% code 102.
def plot_lum_class(b, c, label):
    ''' b: 선택할 별을 나타내는 불리언 Series
        c: 색상
        label: 범례에 표시할 라벨
    '''
    x = df_clean['B-V'][b]
    y = df_clean['M_V'][b]
    ax.scatter(x, y, c = c, s=6, edgecolors='none', label = label)

fig = plt.figure(figsize=(6,8))
ax = fig.add_subplot(111)

# x축, y축 범위 설정
ax.set_xlim(-0.5, 2.5)
ax.set_ylim(15, -15)
ax.grid()

# 그래프 제목 및 축 레이블 설정
ax.set_title('H-R Diagram \n (Hipparcos catalog)',
             fontsize=16)
ax.set_xlabel('Color index (B-V)',
             fontsize=12)
ax.set_ylabel('Absolute magnitude (M)',
             fontsize=12)

# 각 광도 계급별로 별을 그리기
f = lambda s: 'VII' in s
b = df_clean['SpType'].map(f)
plot_lum_class(b,'magenta', 'VII: white dwarfs')

f = lambda s: ('VI' in s) and ('VII' not in s)
b = df_clean['SpType'].map(f)
plot_lum_class(b,'blue', 'VI: subdwarfs')

f = lambda s: ('V' in s) and ('VI' not in s) and ('IV' not in s)
b = df_clean['SpType'].map(f)
plot_lum_class(b,'black', 'V: main-sequence')

f = lambda s: 'IV' in s
b = df_clean['SpType'].map(f)
plot_lum_class(b,'grey', 'IV: subgiants')

f = lambda s: 'III' in s
b = df_clean['SpType'].map(f)
plot_lum_class(b,'green', 'III: giants')

f = lambda s: ('II' in s) and ('III' not in s) and ('VII' not in s)
b = df_clean['SpType'].map(f)
plot_lum_class(b,'orange', 'II: bright giants')

f = lambda s: ('I' in s) and ('II' not in s) and ('V' not in s)
b = df_clean['SpType'].map(f)
plot_lum_class(b,'yellow', 'I: supergiants')

# 축 눈금 폰트 크기 설정
ax.tick_params(axis='both', labelsize=14)
legend = ax.legend(scatterpoints=1, markerscale = 5, shadow=True)
frame = legend.get_frame()

frame.set_facecolor('0.90')  # 범례 배경색 설정
frame.set_edgecolor('0.50')  # 범례 테두리 색상 설정
plt.show()
