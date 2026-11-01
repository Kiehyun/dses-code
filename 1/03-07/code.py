# 지구과학 데이터 사이언스 1 | III-07. H-R도 그리기(히파르코스 성표)
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 89.
from pathlib import Path
import requests

fname = "asu.tsv"
fpath = Path(proj_dir) / fname

# VizieR 질의: 히파르코스 본표(I/239/hip_main)의 다섯 열, 행 수 제한 없음
params = {"-source": "I/239/hip_main",
          "-out": ["HIP", "Vmag", "Plx", "B-V", "SpType"],
          "-out.max": "unlimited", "-oc.form": "dec"}

if not fpath.exists():
    for host in ["vizier.cds.unistra.fr", "vizier.cfa.harvard.edu"]:  # CDS, 미러
        try:
            r = requests.get(f"https://{host}/viz-bin/asu-tsv", params=params, timeout=300)
            r.raise_for_status()
            if r.text.count("\n") < 118218:  # 별 118,218개보다 적으면 덜 받은 것
                raise IOError("받은 행 수가 모자랍니다")
            fpath.write_bytes(r.content)
            print(f"{host}에서 내려받음: {fpath}")
            break
        except Exception as e:
            print(f"{host} 실패: {e}")
    else:  # 두 서버 모두 안 되면 구글 드라이브 사본
        du.download("https://docs.google.com/uc?export=download&id=1TkmU9cE-C4XSQfiDppBk06Jhmyow3ftJ", fpath)

print(f"{fpath} ({fpath.stat().st_size:,} 바이트)")

# %% code 90.
from pathlib import Path 
fpaths = sorted(list(Path(proj_dir).glob('*.tsv')))
print(f"fpaths: {fpaths}")
print(f"len(fpaths): {len(fpaths)}")

# %% code 91.
# 파일 앞 40줄 출력(공통 함수, 인코딩 자동 판별)
head = du.preview_text(fpaths[0], n=40)  # 출력한 줄 목록은 head에 담아 둠

# %% code 92.
import numpy as np
import pandas as pd

# 구분선(------) 줄까지가 설명 · 열 이름 · 단위
with open(fpaths[0], encoding='utf-8') as f:
    n_skip = next(i for i, line in enumerate(f) if line.startswith('---')) + 1

# 구분자: 탭(VizieR 직접 받기) 또는 세미콜론(웹 양식 · 드라이브 사본)
# 열: HIP 번호, V 등급, 연주시차(mas), B-V 색지수, 분광형
df = pd.read_table(
    fpaths[0], skiprows=n_skip, sep=r'[;\t]', header=None, index_col=0,
    names=['HIP', 'Vmag', 'Plx', 'B-V', 'SpType'],
    dtype={'Vmag': str, 'Plx': str, 'B-V': str, 'SpType': str},  # 값은 문자열로
    engine='python').sort_index()

print(f"df.shape:\n{df.shape}")
print(f"df:\n", df)

# %% code 93.
print("df[['Vmag', 'Plx', 'B-V']]:\n", df[['Vmag', 'Plx', 'B-V']])
print("type(df['Vmag'][1]), type(df['Plx'][1]), type(df['B-V'][1]):", 
        type(df['Vmag'][1]), type(df['Plx'][1]), type(df['B-V'][1])) 

# %% code 94.
print("df.describe() :", df.describe())

# 문자열 양쪽 공백 제거
f = lambda x: x.str.strip()
print("type(f)", type(f))
print("f", f)

df_clean = df.apply(f)

# 빈 문자열 → NaN
df_clean = df_clean.replace('', np.nan)

df_clean = df_clean.dropna()

print('***NaN 값이 제거된 후 df_clean에 대한 describe 결과***')
print("df_clean.describe():\n", df_clean.describe())

# 문자열 → 실수
df_clean['Vmag'] = df_clean['Vmag'].astype(np.float64)
df_clean['Plx'] = df_clean['Plx'].astype(np.float64)
df_clean['B-V'] = df_clean['B-V'].astype(np.float64)

print("type(df_clean['Vmag'][1]), type(df_clean['Plx'][1]), type(df_clean['B-V'][1]) :", 
      type(df_clean['Vmag'][1]), type(df_clean['Plx'][1]), type(df_clean['B-V'][1]))

# %% code 95.
# 연주시차가 0 이하인 별 제외(거리를 구할 수 없음)
df_clean = df_clean[df_clean['Plx'] > 0].copy()
print(f"Plx > 0 인 별: {len(df_clean)}개")

# 절대등급: M = V + 5 log(p/100), p는 연주시차(mas)
df_clean['M_V'] = df_clean['Vmag'] + 5 * np.log10(df_clean['Plx']/100.)

print("df_clean:\n", df_clean)

# %% code 96.
# G8, F5처럼 「알파벳+숫자」로 시작하는 분광형만 남기기
f = lambda s: (len(s) >= 2) and (s[0].isalpha()) and (s[1].isdigit())
i = df_clean['SpType'].apply(f)
df_clean = df_clean[i]
print("분광형으로 거른 뒤 df_clean:\n", df_clean)

# %% code 97.
# 분광형 앞 두 글자(예: G8)
f = lambda s: s[0:2]
df_clean['SpType2'] = df_clean['SpType'].apply(f)

print("df_clean:\n", df_clean)

# 첫 글자 = 분광형(O, B, A, …)
f = lambda s: s[0]
clases = df_clean['SpType'].map(f)

print('***df_clean에서 각 분광형별 개수 세기***')
print(clases.value_counts())

# %% code 98.
# OBAFGKM 분광형만 남기기
f = lambda s: s[0] in 'OBAFGKM'
df_clean = df_clean[df_clean['SpType'].map(f)]

f = lambda s: s[0]
clases = df_clean['SpType'].map(f)

print('***df_clean에서 각 분광형별 개수 세기***')
print(clases.value_counts())

# %% code 99.
df_clean.to_csv(Path(proj_dir) / "HIP_clean.csv")
print(f"df_clean을 저장함: {Path(proj_dir) / 'HIP_clean.csv'}")

# 분광형 순서 → 숫자
orden = {'O':'0', 'B':'1', 'A':'2', 'F':'3', 'G':'4', 'K':'5', 'M':'6'}

# 예: G8 → '48'(가로축 값)
f = lambda s: orden[s[0]]+s[1]
df_clean['SpType2'] = df_clean['SpType2'].apply(f)

print("df_clean:\n", df_clean)

# %% code 100.
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6,8))

# 가로축: 분광형, 세로축: 절대등급
ax.scatter(df_clean['SpType2'].astype(np.int32), df_clean['M_V'],
           s=50, edgecolors='none', alpha=0.015, c='k')

# 세로축 뒤집기(밝을수록 위)
ax.set_xlim(0, 70)
ax.set_ylim(15, -10)
ax.grid()
ax.tick_params(axis='both', labelsize=14)

# O~M 눈금(10칸씩)
ax.set_xticks(range(5,75,10))
ax.set_xticklabels(['O', 'B', 'A', 'F', 'G', 'K', 'M'])

ax.set_title('H-R도\n(히파르코스 성표)', fontsize=16)
ax.set_xlabel('분광형', fontsize=16)
ax.set_ylabel('절대 등급 ($M_V$)', fontsize=16)

plt.show()

# %% code 101.
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6,8))

# 가로축: 색지수(B-V), 세로축: 절대등급
ax.scatter(df_clean['B-V'], df_clean['M_V'], s=1, edgecolors='none', c='k')

# 세로축 뒤집기(밝을수록 위)
ax.set_xlim(-0.5, 2.5)
ax.set_ylim(15, -10)
ax.grid()
ax.tick_params(axis='both', labelsize=14)

ax.set_title('H-R도\n(히파르코스 성표)', fontsize=16)
ax.set_xlabel('색지수 ($B-V$)', fontsize=12)
ax.set_ylabel('절대 등급 ($M_V$)', fontsize=12)

plt.show()

# %% code 102.
# 광도 계급(I, V 등)이 적힌 별
f = lambda s: ('I' in s) or ('V' in s)
b = df_clean['SpType'].map(f)
print("b:", b)
print("sum(b):", sum(b))

# %% code 103.
# 광도 계급별 (이름, 조건) — 긴 표기부터 확인해 짧은 표기와 헷갈리지 않게 함
lum_classes = {
    'VII': ('백색왜성(옛 표기)', lambda s: 'VII' in s),
    'VI':  ('준왜성',   lambda s: ('VI' in s) and ('VII' not in s)),
    'V':   ('주계열성', lambda s: ('V' in s) and ('VI' not in s) and ('IV' not in s)),
    'IV':  ('준거성',   lambda s: 'IV' in s),
    'III': ('거성',     lambda s: 'III' in s),
    'II':  ('밝은 거성', lambda s: ('II' in s) and ('III' not in s) and ('VII' not in s)),
    'I':   ('초거성',   lambda s: ('I' in s) and ('II' not in s) and ('V' not in s)),
}

masks = {}  # 계급별로 고른 별(불 Series)
for cls, (name, f) in lum_classes.items():
    masks[cls] = df_clean['SpType'].map(f)
    print(f"{cls:>3} {name}: {masks[cls].sum()}개")

# 두 계급 이상에 중복으로 센 별(예: 'III-IV')
n_class = sum(m.astype(int) for m in masks.values())
print(f"두 계급 이상에 중복으로 센 별: {(n_class > 1).sum()}개")

# %% code 104.
def plot_lum_class(b, c, label):
    ''' b: 선택할 별을 나타내는 불 Series
        c: 색상
        label: 범례에 표시할 이름
    '''
    x = df_clean['B-V'][b]
    y = df_clean['M_V'][b]
    ax.scatter(x, y, c = c, s=6, edgecolors='none', label = label)

fig = plt.figure(figsize=(6,8))
ax = fig.add_subplot(111)

ax.set_xlim(-0.5, 2.5)
ax.set_ylim(15, -15)
ax.grid()

ax.set_title('H-R도\n(히파르코스 성표)', fontsize=16)
ax.set_xlabel('색지수 ($B-V$)', fontsize=12)
ax.set_ylabel('절대 등급 ($M_V$)', fontsize=12)

# 광도 계급별로 그리기(앞에서 만든 masks 사용)
colors = {'VII': 'magenta', 'VI': 'blue', 'V': 'black', 'IV': 'grey',
          'III': 'green', 'II': 'orange', 'I': 'yellow'}
for cls, (name, f) in lum_classes.items():
    plot_lum_class(masks[cls], colors[cls], f'{cls}: {name}')

ax.tick_params(axis='both', labelsize=14)
legend = ax.legend(loc='lower left', scatterpoints=1, markerscale = 5, shadow=True)  # 자리 고정(별이 많으면 'best' 계산이 느림)
frame = legend.get_frame()

frame.set_facecolor('0.90')
frame.set_edgecolor('0.50')
plt.show()
