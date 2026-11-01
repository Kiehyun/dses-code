# 지구과학 데이터 사이언스 1 | I-04. Python 모듈
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 37.
import math
help(math)                                # 도움말 출력
print(f"math.sin(0.5): {math.sin(0.5)}")  # 각도 단위는 라디안
print(f"math.e: {math.e}")                # 자연상수 e

from math import pi  # 필요한 이름만 불러오기
print(f"pi: {pi}")

import datetime
now1 = datetime.datetime.now()  # 모듈.클래스.메서드
print("now1:", now1)

from datetime import datetime  # datetime 클래스만 불러오기
now2 = datetime.now()          # 클래스.메서드(모듈명 생략)
print("now2:", now2)

# %% code 38.
import numpy
a = numpy.random.rand(6)  # 0과 1 사이 난수 6개
print("a :", a)
print("numpy.ndarray.max(a):", numpy.ndarray.max(a))

import numpy as np  # 별칭 np로 불러오기
a = np.random.rand(6)
print("a :", a)
print("np.ndarray.max(a):", np.ndarray.max(a))

# %% code 39.
# 패키지 설치
!pip install numpy

# 특정 버전 패키지 설치
!pip install pandas==1.5.3

# 패키지 업그레이드
!pip install --upgrade pandas 

# 현재 설치된 패키지 목록 확인
!pip list 

# %% code 40.
from pathlib import Path
cwd = Path.cwd()  # 현재 작업 폴더(current working directory)
print(f"Current working directory: {cwd}")
home = Path.home()  # 홈 폴더(Windows: C:\Users\사용자명, Linux·macOS: /home/사용자명)
print(f"Home directory: {home}")
file_path = Path('/home/user/data.txt')  # 문자열로 Path 객체 만들기
print(f"File path from string: {file_path}")
relative = Path('my_folder/my_file.txt')  # 상대 경로
print(f"Relative path: {relative}")
base = Path('/home/user')
new_path = base / 'data' / 'file.csv'  # / 연산자로 경로 결합
print(f"New path: {new_path}")         # 운영체제에 맞는 구분자로 표시(Windows는 \)

# %% code 41.
from pathlib import Path
p = Path('.')

dirs = [x for x in p.iterdir() if x.is_dir()]  # 폴더만 고르기
print("Directories in current path:", dirs)

ipynb_files = list(Path('.').glob('*.ipynb'))  # .ipynb 파일 찾기
print("Jupyter Notebook files in current path:", ipynb_files)

# %% code 42.
from datetime import datetime, date, time
now = datetime.now()
print("now :", now)
print("type(now):", type(now))

dt = datetime(2025, 4, 22, 16, 20, 0)  # 년, 월, 일, 시, 분, 초
d = date(2025, 4, 22)                  # 날짜만
t = time(16, 20, 0)                    # 시간만
print("dt:", dt)
print("d:", d)
print("t:", t)
print("type(d):", type(d))
print("type(t):", type(t))

# %% code 43.
from datetime import datetime, timedelta
now = datetime.now()
str_date = now.strftime("%Y-%m-%d %H:%M:%S")  # datetime → 문자열
print("Formatted date string:", str_date)
dt = datetime.strptime("2025-04-22 16:20:00", "%Y-%m-%d %H:%M:%S")  # 문자열 → datetime
print("Parsed datetime object:", dt)
now = datetime.now()
tomorrow = now + timedelta(days=1)  # 하루 뒤
diff = tomorrow - now               # 시간 차(timedelta)
print("Time difference:", diff)
print("type(diff):", type(diff))

# %% code 44.
list_1d = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # 1차원 리스트
list_2d = [ [1, 2, 3, 4, 5, 6],
            [7, 8, 9, 10, 11, 12] ]  # 2차원 리스트
list_3d = [ [   [1, 2, 3], [4, 5, 6] ],
            [   [7, 8, 9], [10, 11, 12] ] ]  # 3차원 리스트

# 각 리스트의 길이
print(f"len(list_1d): {len(list_1d)}")
print("len(list_2d): {}".format(len(list_2d)))  # 행의 개수
print("len(list_3d): ", (len(list_3d)))         # 최상위 원소의 개수

# 2차원 리스트의 첫 번째 행
print("list_2d[0]: {}".format(list_2d[0]))
print("type(list_2d[0]): ", (type(list_2d[0])))
print(f"len(list_2d[0]): {len(list_2d[0])}")
print("list_2d[0][1]: ", (list_2d[0][1]))

# 3차원 리스트의 첫 번째 원소
print("list_3d[0]:{}".format(list_3d[0]))
print("type(list_3d[0]):{}".format(type(list_3d[0])))
print("len(list_3d[0]):{}".format(len(list_3d[0])))
print("len(list_3d[0][1]):{}".format(len(list_3d[0][1])))
print("list_3d[0][1][0]:{}".format(list_3d[0][1][0]))

# %% code 45.
import numpy as np
arr1 = np.array([[1,2,3],[4,5,6],[7,8,9]])
print("arr1: ", arr1)
print("arr1.dtype: ", arr1.dtype)  # 자료형
print("arr1.ndim: ", arr1.ndim)    # 차원 수
print("arr1.shape: ", arr1.shape)  # 형태(행, 열)

# %% code 46.
import numpy as np
arr2 = np.zeros((3,2))  # 0으로 채운 3×2 배열
print("arr2:", arr2)
print("arr2.dtype:", arr2.dtype)

arr3 = np.ones((3,2))  # 1로 채운 배열
print("arr3:", arr3)

arr4 = np.eye(2)  # 2×2 단위 행렬
print("arr4:", arr4)

arr5 = np.arange(0, 2,0.25)  # range의 실수 버전(끝값 2는 제외)
print("arr5:", arr5)

arr6 = np.linspace(1, 3, 5)  # 1~3을 같은 간격으로 5개
print("arr6:", arr6)

# %% code 47.
import numpy as np
arr7 = np.arange(20)
print("arr7:", arr7)

re_arr7 = arr7.reshape((4,5))  # 4행 5열로 바꾸기
print("re_arr7:", re_arr7)

# %% code 48.
float_re_arr7 = re_arr7.astype(np.float64)  # 자료형 변경
print("float_re_arr7:", float_re_arr7)
print("float_re_arr7.dtype:", float_re_arr7.dtype)
# dtype 'U'는 유니코드 문자열('S'는 바이트 문자열)
string_arr8 = np.array(['1.25', '0.99', '44', '11'], dtype='U')

print("string_arr8:", string_arr8)
print("string_arr8.dtype", string_arr8.dtype)
float_arr8 = string_arr8.astype(np.float32)  # 문자열 → 실수
print("dtype(float_arr8):", float_arr8.dtype)

# %% code 49.
import numpy as np
arr1 = np.array([[1,2,3],[4,5,6],[7,8,9]])
arr2 = np.array([[11,12,13],[14,15,16],[17,18,19]])
print("arr1:\n", arr1)
print("arr2:\n", arr2)
# 같은 위치의 원소끼리 계산
print("arr1 + arr2:\n", arr1 + arr2)
print("arr1 - arr2:\n", arr1 - arr2)
print("arr1 + 3:\n", arr1 + 3)  # 모든 원소에 3을 더함
print("arr1 - 3:\n", arr1 - 3)
print("arr1 * 3:\n", arr1 * 3)
print("arr1 / 3:\n", arr1 / 3)
print("arr1 ** 2:\n", arr1 ** 2)

# %% code 50.
import numpy as np
a = np.array([[-1,2,3],[3,4,8]])
s = np.sum(a)
print('sum=', a.sum())
# axis=0: 열별, axis=1: 행별
print('sum by column=', a.sum(axis=0))  # 세로 방향 합
print('sum by row=', a.sum(axis=1))     # 가로 방향 합
print('mean=', a.mean())
print('sd=', a.std())  # 표준편차

# %% code 51.
import numpy as np
import pandas as pd
np.random.seed(0)  # 난수 고정(실행할 때마다 같은 결과)

# 시리즈 생성
s1 = pd.Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e']) 
print("-"*20+"\ns1:\n", s1)  
print("-"*20+"\ns1.values:", s1.values)
print("-"*20+"\nindex:", s1.index)

# 딕셔너리로 시리즈 생성
d = {'b': 1, 'a': 0, 'c': 2}
s2 = pd.Series(d)
print("-"*20+"\ns2:\n", s2)

# 난수로 시리즈 생성
r = pd.Series(np.random.randn(5))
s3 = pd.Series(r)
print("-"*20+"\ns3:\n", s3)
s3.index=['d', 'b', 'a', 'c', 'e']  # 인덱스 바꾸기
print("-"*20+"\ns3:\n", s3)

# %% code 52.
print("-"*20+"\ns1[:3]:", s1[:3])
print("-"*20+"\ns1[1:4]:", s1[1:4])  # 위치 1~3
print("-"*20+"\ns1[s1 > s1.median()]:", s1[s1 > s1.median()])  # 중앙값보다 큰 원소만(불린 인덱싱)
print("-"*20+"\ns1.iloc[[4, 3, 1]]:", s1.iloc[[4, 3, 1]])  # 위치로 고르기

# %% code 53.
np.exp(s2)
print("s2.dtype:", s2.dtype)
s2.dtype
print("np.exp(s2):", np.exp(s2))  # 원소마다 지수 함수 적용

s3_ar = s3.array  # pandas 배열
print("-"*20+"\ns3_ar:", s3_ar)
s3_ndar = s3.to_numpy()  # NumPy 배열로 변환
print("s3_ndar:", s3_ndar)

# %% code 54.
print("s3['a']:", s3['a'])  # 인덱스 이름으로 접근
s3['e'] = 12.
print("-"*20+"\ns3:\n", s3)

print("-"*20+"\n'e' in s3:", 'e' in s3)  # 인덱스가 있는지 확인
print("'f' in s3:", 'f' in s3)

print("-"*20+"\ns3.get('f'):", s3.get('f'))         # 없으면 None
print("s3.get('f', np.nan):", s3.get('f', np.nan))  # 없으면 기본값 NaN

# %% code 55.
print("s1 + s1:\n", s1 + s1)
print("-"*20+"\ns1 * 2:\n", s1 * 2)
print("-"*20+"\nnp.exp(s1):\n", np.exp(s1))

print("s1[1:] + s1[:-1]:\n", s1[1:] + s1[:-1])  # 인덱스가 같은 원소끼리 더함(짝이 없으면 NaN)

s = pd.Series(np.random.randn(5), name='something')
print("-"*20+"\ns:\n", s)
print("-"*20+"\ns.name:", s.name)

s = s.rename("different")  # 이름 바꾸기
print("s.name(after rename):", s.name)

# %% code 56.
import pandas as pd
import numpy as np

d = {'one': pd.Series([1., 2., 3.], index=['a', 'b', 'c'])}
df1 = pd.DataFrame(d)
print("df1:\n", df1)

d = {'one': pd.Series([1., 2., 3.], index=['a', 'b', 'c']), 'two': pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
df2 = pd.DataFrame(d)
print("-"*20+"\ndf2:\n", df2)

df3 = pd.DataFrame(d, index=['d', 'b', 'a'])
print("-"*20+"\ndf3:\n", df3)

df4 = pd.DataFrame(d, index=['d', 'b', 'a'], columns=['two', 'three'])  # 없는 열 'three'는 NaN
print("-"*20+"\ndf4:\n", df4)

# %% code 57.
d = {'one': [1., 2., 3., 4.], 'two': [4., 3., 2., 1.]}
df5 = pd.DataFrame(d)
print("df5:\n", df5)

print("-"*20+"\ndf5.index:", df5.index)
print("df5.columns:", df5.columns)

df6 = pd.DataFrame(d, index=['a', 'b', 'c', 'd'])  # 인덱스 지정
print("-"*20+"\ndf6:\n", df6)

# %% code 58.
data = np.zeros((2,), dtype=[('A', 'i4'), ('B', 'f4'), ('C', 'S10')])  # 구조화 배열(A: 정수, B: 실수, C: 10바이트 문자열)
print("data:", data)
df7 = pd.DataFrame(data)    
print("-"*20+"\ndf7:\n", df7)

data[:] = [(1, 2., 'Hello'), (2, 3., "World")]
print("-"*20+"\ndata:", data)
df8 = pd.DataFrame(data)
print("-"*20+"\ndf8:\n", df8)

df9 = pd.DataFrame(data, index=['first', 'second'])  # 인덱스 지정
print("-"*20+"\ndf9:\n", df9)

df10 = pd.DataFrame(data, columns=['C', 'A', 'B'])  # 열 순서 지정
print("-"*20+"\ndf10:\n", df10)

data2 = [{'a': 1, 'b': 2}, {'a': 5, 'b': 10, 'c': 20}]
df11 = pd.DataFrame(data2)  # 딕셔너리 리스트로 생성(없는 값은 NaN)
print("-"*20+"\ndf11:\n", df11)

df12 = pd.DataFrame({('a', 'b'): {('A', 'B'): 1, ('A', 'C'): 2},
              ('a', 'a'): {('A', 'C'): 3, ('A', 'B'): 4},
              ('a', 'c'): {('A', 'B'): 5, ('A', 'C'): 6},
              ('b', 'a'): {('A', 'C'): 7, ('A', 'B'): 8},
              ('b', 'b'): {('A', 'D'): 9, ('A', 'B'): 10}})
print("-"*20+"\ndf12:\n", df12)                      # 튜플 키 → 다중 인덱스(MultiIndex)
print("-"*20+"\ndf12['a']['b']:\n", df12['a']['b'])  # 다중 인덱스 열 접근
print("-"*20+"\ndf12['a', 'b']:\n", df12['a', 'b'])  # 튜플로 접근

# %% code 59.
data = {"names": ["Kilho", "Kilho", "Kilho", "Charles", "Charles"],
           "year": [2014, 2015, 2016, 2015, 2016],
           "points": [1.5, 1.7, 3.6, 2.4, 2.9]}
df3 = pd.DataFrame(data, columns=["year", "names", "points", "penalty"],
                          index=["one", "two", "three", "four", "five"])
print("df3:\n", df3)
print("-"*20+"\ntype(df3['year']): {}".format(type(df3['year'])))  # 열 하나 → Series
print("type(df3[['year']]): {}".format(type(df3[['year']])))  # 이중 괄호 → DataFrame
print("type(df3.year): {}".format(type(df3.year)))  # 점 표기법
print("type(df3[['year', 'points']]): {}".format(type(df3[['year', 'points']])))

# names 열을 인덱스로
df3 = df3.set_index('names')
print("-"*20+"\ndf3.describe() :\n", df3.describe())  # 기술통계

print("-"*20+"\ndf3.iloc[1]:\n ",  df3.iloc[1])  # 위치 1(두 번째 행)
print("-"*20+"\ndf3.loc['Kilho']:\n", df3.loc["Kilho"])  # 인덱스 이름으로

df3 = df3.reset_index()  # 인덱스를 다시 열로
print("-"*20+"\ndf3:\n", df3)

# %% code 60.
# DataFrame 생성
data = {'names': ['Kilho', 'Kilho', 'Kilho', 'Charles', 'Charles'],
        'year': [2014, 2015, 2016, 2015, 2016],
        'points': [1.5, 1.7, 3.6, 2.4, 2.9]}
df = pd.DataFrame(data, columns=['year', 'names', 'points'], index=['one', 'two', 'three', 'four', 'five'])
print("-"*20+"\ndf:\n", df)
df['penalty'] = 0.5  # 모든 행에 같은 값
print("-"*20+"\ndf:\n", df)

# 배열로 열 추가
df['zeros'] = np.arange(5)
print("-"*20+"\ndf:\n", df)

# Series로 열 추가(인덱스 기준으로 맞춤)
val = pd.Series([-1.2, -1.5, -1.7, -2.5, -2.2], index=df.index)
df['debt'] = val
print("-"*20+"\ndf:\n", df)

# 계산 결과로 열 추가
df['net_points'] = df['points'] - df['penalty']
print("-"*20+"\ndf:\n", df)

# 조건식으로 불린 열 추가
df['high_points'] = df['net_points'] > 2.0
print("-"*20+"\ndf:\n", df)

# 열 삭제
del df['high_points']
print("-"*20+"\ndf:\n", df)

# 위치 1(두 번째)의 행 삭제
df = df.drop(df.index[1])
print("-"*20+"\ndf:\n", df)

# names 중복은 마지막 행만 남기고 인덱스로
df = df.drop_duplicates(subset='names', keep='last').set_index('names')
print("-"*20+"\ndf:\n", df)

# %% code 61.
d1 = {'one': pd.Series([1., 2., 3.], index=['a', 'b', 'c'])}
df1 = pd.DataFrame(d1)
print("df1:\n", df1)

d2 = {'one': pd.Series([3., 4., 5.], index=['c', 'd', 'e'])}
df2 = pd.DataFrame(d2)
print("-"*20+"\ndf2:\n", df2)

df1_df2 = pd.concat((df1, df2), ignore_index=True, axis=0)  # 위아래로 이어 붙이기(인덱스 새로 매김)
print("df1_df2:\n", df1_df2)
print("-"*20+"\ndf1_df2.index:\n", df1_df2.index)

print("-"*20+"\ndf1_df2.duplicated():\n", df1_df2.duplicated())  # 중복 행 확인

# %% code 62.
import pandas as pd

df = pd.DataFrame(
    {'price': [100, 200, 300],
     'weight': [20.3, 15.1, 25.9]},
    index=['idx_a', 'idx_b', 'idx_c'])
print("df:\n", df)

# iterrows(): 행 단위 반복
for idx, row in df.iterrows():
    print("** 인덱스 이름:", idx)
    print(idx, row)
    print("------"*5)

# items(): 열 단위 반복
for col, item in df.items():
    print("** 열 이름:", col)
    print(col, item)
    print("-----"*5)

# itertuples(): 행을 튜플로 반복
for row in df.itertuples():
    print(row)

# %% code 63.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter

np.random.seed(19680801)  # 난수 고정

X = np.linspace(0.5, 3.5, 100)
Y1 = 3+np.cos(X)
Y2 = 1+np.cos(1+X/0.75)/2
Y3 = np.random.uniform(Y1, Y2, len(X))

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1, aspect=1)

def minor_tick(x, pos):  # 정수 위치에는 보조 눈금 이름을 쓰지 않음
    if not x % 1.0:
        return ""
    return "%.2f" % x

ax.xaxis.set_major_locator(MultipleLocator(1.000))
ax.xaxis.set_minor_locator(AutoMinorLocator(4))
ax.yaxis.set_major_locator(MultipleLocator(1.000))
ax.yaxis.set_minor_locator(AutoMinorLocator(4))
ax.xaxis.set_minor_formatter(FuncFormatter(minor_tick))

ax.set_xlim(0, 4)
ax.set_ylim(0, 4)

ax.tick_params(which='major', width=1.0)
ax.tick_params(which='major', length=10)
ax.tick_params(which='minor', width=1.0, labelsize=10)
ax.tick_params(which='minor', length=5, labelsize=10, labelcolor='0.25')

ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)

ax.plot(X, Y1, c=(0.25, 0.25, 1.00), lw=2, label="Blue signal", zorder=10)
ax.plot(X, Y2, c=(1.00, 0.25, 0.25), lw=2, label="Red signal")
ax.plot(X, Y3, linewidth=0,
        marker='o', markerfacecolor='w', markeredgecolor='k')

ax.set_title("Anatomy of a figure", fontsize=20, verticalalignment='bottom')
ax.set_xlabel("X axis label")
ax.set_ylabel("Y axis label")

ax.legend()

def circle(x, y, radius=0.15):  # 설명할 위치에 원 표시
    from matplotlib.patches import Circle
    from matplotlib.patheffects import withStroke
    circle = Circle((x, y), radius, clip_on=False, zorder=10, linewidth=1,
                    edgecolor='black', facecolor=(0, 0, 0, .0125),
                    path_effects=[withStroke(linewidth=5, foreground='w')])
    ax.add_artist(circle)

def text(x, y, text):  # 설명 글자
    ax.text(x, y, text, backgroundcolor="white",
            ha='center', va='top', weight='bold', color='blue')

# 보조 눈금 이름
circle(0.50, -0.10)
text(0.50, -0.32, "Minor tick label")

# 주 눈금
circle(-0.03, 4.00)
text(0.03, 3.80, "Major tick")

# 보조 눈금
circle(0.00, 3.50)
text(0.00, 3.30, "Minor tick")

# 주 눈금 이름
circle(-0.15, 3.00)
text(-0.15, 2.80, "Major tick label")

# x축 이름
circle(1.80, -0.27)
text(1.80, -0.45, "X axis label")

# y축 이름
circle(-0.27, 1.80)
text(-0.27, 1.6, "Y axis label")

# 제목
circle(1.60, 4.13)
text(1.60, 3.93, "Title")

# 파란색 그래프
circle(1.75, 2.80)
text(1.75, 2.60, "Line\n(line plot)")

# 빨간색 그래프
circle(1.20, 0.60)
text(1.20, 0.40, "Line\n(line plot)")

# 산점도
circle(3.20, 1.75)
text(3.20, 1.55, "Markers\n(scatter plot)")

# 격자
circle(3.00, 3.00)
text(3.00, 2.80, "Grid")

# 범례
circle(3.70, 3.80)
text(3.70, 3.60, "Legend")

# 축 영역(Axes)
circle(0.5, 0.5)
text(0.5, 0.3, "Axes")

# 그림 전체(Figure)
circle(-0.3, 0.65)
text(-0.3, 0.45, "Figure")

color = 'blue'
ax.annotate('Spines', xy=(4.0, 0.35), xytext=(3.3, 0.5),
            weight='bold', color=color,
            arrowprops=dict(arrowstyle='->',
                            connectionstyle="arc3",
                            color=color))

ax.annotate('', xy=(3.15, 0.0), xytext=(3.45, 0.45),
            weight='bold', color=color,
            arrowprops=dict(arrowstyle='->',
                            connectionstyle="arc3",
                            color=color))

ax.text(4.0, -0.4, "Made with http://matplotlib.org",
        fontsize=10, ha="right", color='.5')

plt.show()

# %% code 64.
import matplotlib.pyplot as plt
# 한글 폰트를 설정하지 않으면 '축' 같은 한글이 표시되지 않음

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.plot(x, y)
plt.title("Sample Plot")
plt.xlabel("X축")
plt.ylabel("Y축")
plt.grid(True)
plt.show()

# %% code 65.
import matplotlib.pyplot as plt

# 2행 2열 서브플롯
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# 첫 번째 그래프 (0,0)
axes[0, 0].plot([1, 2])
axes[0, 0].set_title('Graph 1: [1, 2]')
axes[0, 0].grid(True)

# 두 번째 그래프 (0,1)
axes[0, 1].plot([2, 3, 5, 10])
axes[0, 1].set_title('Graph 2: [2, 3, 5, 10]')
axes[0, 1].grid(True)

# 세 번째 그래프 (1,0)
axes[1, 0].plot([1, 2, 3, 4], [2, 3, 5, 10])
axes[1, 0].set_title('Graph 3: x=[1,2,3,4], y=[2,3,5,10]')
axes[1, 0].grid(True)

# 네 번째 그래프 (1,1)
data_dict = {'data_x': [1, 2, 3, 4, 5], 'data_y': [2, 3, 5, 10, 8]}
axes[1, 1].plot('data_x', 'data_y', data=data_dict)
axes[1, 1].set_title('Graph 4: Dictionary data')
axes[1, 1].grid(True)

plt.tight_layout()
plt.show()

# %% code 66.
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# 첫 번째 플롯 (0,0) - 폰트 스타일링
axes[0,0].plot([1, 2, 3, 4], [2, 3, 5, 10])
axes[0,0].set_xlabel('X-Axis', labelpad=15, 
    fontdict={'family': 'serif', 'color': 'b', 'weight': 'bold', 'size': 14})
axes[0,0].set_ylabel('Y-Axis', labelpad=20, 
    fontdict={'family': 'monospace', 'color': 'deeppink', 'weight': 'normal', 'size': 'xx-large'})
axes[0,0].set_title('Font Styling')

# 두 번째 플롯 (0,1) - 레이블 위치 조정
axes[0,1].plot([1, 2, 3, 4], [2, 3, 5, 10])
axes[0,1].set_xlabel('X-Axis', loc='right')
axes[0,1].set_ylabel('Y-Axis', loc='top')
axes[0,1].set_title('Label Position')

# 세 번째 플롯 (0,2) - 기본 범례
axes[0,2].plot([1, 2, 3, 4], [2, 3, 5, 10], label='Price ($)')
axes[0,2].set_xlabel('X-Axis')
axes[0,2].set_ylabel('Y-Axis')
axes[0,2].legend()
axes[0,2].set_title('Basic Legend')

# 네 번째 플롯 (1,0) - 범례 위치 지정
axes[1,0].plot([1, 2, 3, 4], [2, 3, 5, 10], label='Price ($)')
axes[1,0].set_xlabel('X-Axis')
axes[1,0].set_ylabel('Y-Axis')
axes[1,0].legend(loc='lower right')
axes[1,0].set_title('Legend Position')

# 다섯 번째 플롯 (1,1) - 다중 라인과 범례 스타일링
axes[1,1].plot([1, 2, 3, 4], [2, 3, 5, 10], label='Price ($)')
axes[1,1].plot([1, 2, 3, 4], [3, 5, 9, 7], label='Demand (#)')
axes[1,1].set_xlabel('X-Axis')
axes[1,1].set_ylabel('Y-Axis')
axes[1,1].legend(loc='best', ncol=2, fontsize=14)
axes[1,1].set_title('Multi-line with Legend Styling')

# 여섯 번째 플롯 (1,2) - 범례 프레임과 그림자
axes[1,2].plot([1, 2, 3, 4], [2, 3, 5, 10], label='Price ($)')
axes[1,2].plot([1, 2, 3, 4], [3, 5, 9, 7], label='Demand (#)')
axes[1,2].set_xlabel('X-Axis')
axes[1,2].set_ylabel('Y-Axis')
axes[1,2].legend(loc='best', ncol=2, fontsize=14, frameon=True, shadow=True)
axes[1,2].set_title('Legend with Frame & Shadow')

plt.tight_layout()
plt.show()

# %% code 67.
import matplotlib.pyplot as plt

# y값만 주면 x는 0, 1, ...로 자동 지정
plt.plot([0,1])
plt.savefig(f"{proj_dir}/pic.png")
# PDF(벡터): dpi는 래스터 요소에만 적용, 여백 최소화
plt.savefig(f"{proj_dir}/pic.pdf", dpi=300, bbox_inches='tight', pad_inches=0.1 )
plt.show()

# %% code 68.
import matplotlib.pyplot as plt

fname = f"{proj_dir}/pic.png"

# 이미지를 배열로 읽기
chart_png = plt.imread(fname)

# 보간 없이 원본 픽셀 그대로 표시
plt.imshow(chart_png, interpolation='none')

plt.show()

# %% code 69.
# 한글 폰트 설정과 깨짐 해결
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform

def setup_korean_font():
    """
    공개 글꼴을 먼저 찾고, 없으면 운영체제 글꼴로 한글 폰트를 설정하는 함수
    """
    system = platform.system()
    font_candidates = ['NanumGothic', 'Noto Sans CJK KR']  # 공개 글꼴
    if system == 'Windows':
        font_candidates += ['Malgun Gothic']
    elif system == 'Darwin':  # macOS
        font_candidates += ['AppleGothic']
    
    # 설치된 폰트 이름 목록
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    for font in font_candidates:
        if font in available_fonts:
            plt.rcParams['font.family'] = font
            print(f"한글 폰트 설정 완료: {font}")
            break
    else:
        # 후보 폰트가 없을 때(for-else)
        plt.rcParams['font.family'] = 'DejaVu Sans'
        print("기본 폰트로 설정됨 (한글이 깨질 수 있음)")
    
    # 마이너스 기호 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False
    
    return plt.rcParams['font.family']

current_font = setup_korean_font()

# 폰트 테스트
fig, ax = plt.subplots(figsize=(8, 4))
ax.text(0.5, 0.7, '한글 폰트 테스트', fontsize=20, ha='center', transform=ax.transAxes)
ax.text(0.5, 0.5, f'현재 설정된 폰트: {current_font}', fontsize=14, ha='center', transform=ax.transAxes)
ax.text(0.5, 0.3, '위성의 궤도 분석', fontsize=16, ha='center', transform=ax.transAxes)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_title('한글 표시 테스트')
plt.show()

print(f"\n현재 시스템: {platform.system()}")
print(f"설정된 폰트: {current_font}")
print("한글이 정상적으로 표시되면 설정이 완료되었습니다.")

# %% code 70.
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(4, 3))
ax.plot([1, 2, 3, 4], [2, 3, 5, 10])
ax.set_xlabel("X축")
ax.set_ylabel("Y축")
du.save_figure(fig, proj_dir / "pic_du")  # pic_du.pdf와 pic_du.png로 저장
plt.close(fig)                            # 화면에는 그리지 않음

fpaths = du.list_files(proj_dir, "pdf")    # 데이터 폴더의 PDF 파일 목록
