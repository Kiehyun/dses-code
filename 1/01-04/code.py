# 지구과학 데이터 사이언스 1 | I-04. Python 모듈
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 36.
import math                               # math 모듈을 임포트
help(math)                                # math 모듈의 도움말 정보를 출력
print(f"math.sin(0.5): {math.sin(0.5)}")  # 0.5 라디안의 사인 값을 계산하고 출력
print(f"math.e: {math.e}")                # 자연상수 e (약 2.718281828...)의 값을 출력

from math import pi  # math 모듈에서 원주율(pi) 상수만을 직접 임포트
print(f"pi: {pi}")   # 원주율 파이 값 (약 3.141592653...)을 출력

import datetime                 # datetime 모듈 전체를 임포트
now1 = datetime.datetime.now()  # 모듈명.클래스명.메서드명 형태로 현재 날짜와 시간을 가져옴
print("now1:", now1)            # 현재 날짜와 시간을 출력 (예: 2025-08-03 16:30:45.123456)

from datetime import datetime  # datetime 모듈에서 datetime 클래스만을 직접 임포트
now2 = datetime.now()          # 클래스명.메서드명 형태로 바로 사용 (모듈명 생략 가능)
print("now2:", now2)           # 현재 날짜와 시간을 출력 (now1과 동일한 결과)

# %% code 37.
import numpy
a = numpy.random.rand(6)
print("a :", a)                                       # 0과 1 사이의 난수로 이루어진 배열 출력
print("numpy.ndarray.max(a):", numpy.ndarray.max(a))  # 배열 a의 최대값을 출력

import numpy as np                              # numpy 모듈을 np로 별칭하여 사용
a = np.random.rand(6)
print("a :", a)                                 # 0과 1 사이의 난수로 이루어진 배열 출력
print("np.ndarray.max(a):", np.ndarray.max(a))  # 배열 a의 최댓값을 출력

# %% code 38.
# 패키지 설치
!pip install numpy

# 특정 버전 패키지 설치
!pip install pandas==1.5.3

# 패키지 업그레이드
!pip install --upgrade pandas 

# 현재 설치된 패키지 목록 확인
!pip list 

# %% code 39.
from pathlib import Path                      # 객체 지향적 경로 처리를 위한 pathlib 모듈에서 Path 클래스 임포트
cwd = Path.cwd()                              # cwd()는 current working directory의 줄임말로 현재 작업 중인 디렉토리의 경로를 반환
print(f"Current working directory: {cwd}")    # 현재 작업 디렉토리 경로를 출력
home = Path.home()                            # 사용자의 홈 디렉토리 경로를 반환 (Windows: C:\Users\사용자명, Linux/Mac: /home/사용자명)
print(f"Home directory: {home}")              # 홈 디렉토리 경로를 출력
file_path = Path('/home/user/data.txt')       # 문자열 경로를 Path 객체로 변환하여 생성
print(f"File path from string: {file_path}")  # 문자열에서 생성된 Path 객체를 출력
relative = Path('my_folder/my_file.txt')      # 현재 디렉토리를 기준으로 하는 상대 경로로 Path 객체 생성
print(f"Relative path: {relative}")           # 상대 경로 Path 객체를 출력
base = Path('/home/user')                     # 기본 경로를 Path 객체로 생성
new_path = base / 'data' / 'file.csv'         # / 연산자를 사용하여 경로를 단계적으로 결합
print(f"New path: {new_path}")                # Windows는 \home\user\data\file.csv, Linux·macOS는 /home/user/data/file.csv(플랫폼에 맞는 경로 구분자로 자동 변환)

# %% code 40.
from pathlib import Path  # 객체 지향적 경로 처리를 위한 pathlib 모듈에서 Path 클래스 임포트
p = Path('.')             # 현재 디렉토리('.')를 나타내는 Path 객체 생성

dirs = [x for x in p.iterdir() if x.is_dir()]  # 현재 디렉토리의 모든 항목 중 디렉토리만 필터링
print("Directories in current path:", dirs)  # 현재 경로에 있는 모든 디렉토리 목록을 출력

ipynb_files = list(Path('.').glob('*.ipynb'))  # 현재 디렉토리의 .ipynb 파일을 검색하여 리스트로 변환
print("Jupyter Notebook files in current path:", ipynb_files)  # 현재 경로에 있는 모든 Jupyter Notebook 파일 목록 출력

# %% code 41.
from datetime import datetime, date, time  # datetime 모듈에서 날짜/시간 관련 클래스들을 임포트
now = datetime.now()                       # 현재 시스템의 날짜와 시간을 포함하는 datetime 객체를 생성
print("now :", now)                        # 현재 날짜와 시간을 출력 (예시: 2025-08-03 16:20:00.123456)
print("type(now):", type(now))             # now 객체의 자료형을 출력 

dt = datetime(2025, 4, 22, 16, 20, 0)  # 년, 월, 일, 시, 분, 초를 지정하여 datetime 객체 생성
d = date(2025, 4, 22)                  # 년, 월, 일만 지정하여 date 객체 생성
t = time(16, 20, 0)                    # 시, 분, 초만 지정하여 time 객체 생성
print("dt:", dt)                       # datetime 객체 출력 (날짜와 시간 모두 포함)
print("d:", d)                         # date 객체 출력 (날짜만 포함)
print("t:", t)                         # time 객체 출력 (시간만 포함)
print("type(d):", type(d))             # date 객체의 자료형 출력 
print("type(t):", type(t))             # time 객체의 자료형 출력 

# %% code 42.
from datetime import datetime, timedelta
now = datetime.now()
str_date = now.strftime("%Y-%m-%d %H:%M:%S")
print("Formatted date string:", str_date)  # '2025-04-22 16:20:00' 형식의 문자열로 변환된 날짜 출력
dt = datetime.strptime("2025-04-22 16:20:00", "%Y-%m-%d %H:%M:%S")
print("Parsed datetime object:", dt)  # 문자열을 datetime 객체로 변환된 결과 출력
now = datetime.now()
tomorrow = now + timedelta(days=1)
diff = tomorrow - now
print("Time difference:", diff)   # 1 day, 0:00:00 형식으로 날짜 차이를 출력
print("type(diff):", type(diff))  # timedelta 객체의 자료형 출력

# %% code 43.
list_1d = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]               # 1차원 리스트
list_2d = [ [1, 2, 3, 4, 5, 6],
            [7, 8, 9, 10, 11, 12] ]           # 2차원 리스트
list_3d = [ [   [1, 2, 3], [4, 5, 6] ],
            [   [7, 8, 9], [10, 11, 12] ] ]   # 3차원 리스트

# 각 리스트의 길이 출력
print(f"len(list_1d): {len(list_1d)}")          # 1차원 리스트의 길이
print("len(list_2d): {}".format(len(list_2d)))  # 2차원 리스트의 길이 (행의 개수)
print("len(list_3d): ", (len(list_3d)))         # 3차원 리스트의 길이 (최상위 요소의 개수)

# 2차원 리스트의 첫 번째 행 접근
print("list_2d[0]: {}".format(list_2d[0]))       # 첫 번째 행 출력
print("type(list_2d[0]): ", (type(list_2d[0])))  # 첫 번째 행의 자료형
print(f"len(list_2d[0]): {len(list_2d[0])}")     # 첫 번째 행의 길이
print("list_2d[0][1]: ", (list_2d[0][1]))        # 첫 번째 행의 두 번째 요소

# 3차원 리스트의 첫 번째 요소 접근
print("list_3d[0]:{}".format(list_3d[0]))            # 첫 번째 2차원 배열
print("type(list_3d[0]):{}".format(type(list_3d[0])))  # 첫 번째 요소의 자료형
print("len(list_3d[0]):{}".format(len(list_3d[0])))  # 첫 번째 2차원 배열의 길이
print("len(list_3d[0][1]):{}".format(len(list_3d[0][1])))  # 첫 번째 2차원 배열의 두 번째 행 길이
print("list_3d[0][1][0]:{}".format(list_3d[0][1][0]))  # 첫 번째 2차원 배열의 두 번째 행의 첫 번째 요소

# %% code 44.
import numpy as np
arr1 = np.array([[1,2,3],[4,5,6],[7,8,9]])
print("arr1: ", arr1)              # 배열 출력
print("arr1.dtype: ", arr1.dtype)  # 배열의 자료형 출력
print("arr1.ndim: ", arr1.ndim)    # 배열의 차원 수 출력
print("arr1.shape: ", arr1.shape)  # 배열의 형태 출력

# %% code 45.
import numpy as np
arr2 = np.zeros((3,2))
print("arr2:", arr2)              # 배열 출력
print("arr2.dtype:", arr2.dtype)  # 배열의 자료형 출력 

arr3 = np.ones((3,2))
print("arr3:", arr3)  # 배열 출력

arr4 = np.eye(2)
print("arr4:", arr4)  # 단위 행렬 출력

arr5 = np.arange(0, 2,0.25)  # range 함수의 실수 버전으로 이해하자.
print("arr5:", arr5)         # 배열 출력

arr6 = np.linspace(1, 3, 5)  # 정해준 포인트 갯수로 나눔
print("arr6:", arr6)         # 배열 출력

# %% code 46.
import numpy as np
arr7 = np.arange(20)
print("arr7:", arr7)  # 배열 출력

re_arr7 = arr7.reshape((4,5))
print("re_arr7:", re_arr7)  # 재구성된 배열 출력

# %% code 47.
float_re_arr7 = re_arr7.astype(np.float64)          # 자료형 변경
print("float_re_arr7:", float_re_arr7)              # 자료형 변경된 배열 출력
print("float_re_arr7.dtype:", float_re_arr7.dtype)  # 변경된 배열의 자료형 출력
# 수정: 유니코드 문자열은 'U', 바이트 길이는 'S' 로 지정
string_arr8 = np.array(['1.25', '0.99', '44', '11'], dtype='U')

print("string_arr8:", string_arr8)             # 문자열 배열 출력
print("string_arr8.dtype", string_arr8.dtype)  # 문자열 배열의 자료형 출력
float_arr8 = string_arr8.astype(np.float32)
print("dtype(float_arr8):", float_arr8.dtype)  # 문자열 배열을 float로 변환한 결과의 데이터 타입 출력

# %% code 48.
import numpy as np
arr1 = np.array([[1,2,3],[4,5,6],[7,8,9]])           # 3x3 배열 arr1 생성 (1부터 9까지)
arr2 = np.array([[11,12,13],[14,15,16],[17,18,19]])  # 3x3 배열 arr2 생성 (11부터 19까지)
print("arr1:\n", arr1)                               # arr1 배열 출력
print("arr2:\n", arr2)                               # arr2 배열 출력
# 두 배열의 요소별 덧셈 연산 수행 및 결과 출력
print("arr1 + arr2:\n", arr1 + arr2)
print("arr1 - arr2:\n", arr1 - arr2)
print("arr1 + 3:\n", arr1 + 3)    # 각 요소에 3을 더함
print("arr1 - 3:\n", arr1 - 3)    # 각 요소에서 3을 뺌
print("arr1 * 3:\n", arr1 * 3)    # 각 요소에 3을 곱함
print("arr1 / 3:\n", arr1 / 3)    # 각 요소를 3으로 나눔
print("arr1 ** 2:\n", arr1 ** 2)  # 각 요소를 제곱

# %% code 49.
import numpy as np
# 2x3 배열 생성
a = np.array([[-1,2,3],[3,4,8]])
# 배열의 모든 원소의 합 계산
s = np.sum(a)
print('sum=', a.sum())
# 행별/열별 연산 (axis=0: 열별, axis=1: 행별)
print('sum by column=', a.sum(axis=0))  # 각 열의 합 (세로 방향으로 합계)
print('sum by row=', a.sum(axis=1))     # 각 행의 합 (가로 방향으로 합계)
print('mean=', a.mean())                # 전체 평균
print('sd=', a.std())                   # 전체 표준편차

# %% code 50.
import numpy as np
import pandas as pd
np.random.seed(0)

# 시리즈 생성
s1 = pd.Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e']) 
print("-"*20+"\ns1:\n", s1)  
print("-"*20+"\ns1.values:", s1.values)  # 값 출력
print("-"*20+"\nindex:", s1.index)       # 인덱스 출력

# 딕셔너리로 시리즈 생성
d = {'b': 1, 'a': 0, 'c': 2}
s2 = pd.Series(d)
print("-"*20+"\ns2:\n", s2)

# 랜덤 값으로 시리즈 생성
r = pd.Series(np.random.randn(5))
s3 = pd.Series(r)
print("-"*20+"\ns3:\n", s3)
s3.index=['d', 'b', 'a', 'c', 'e']  # 인덱스 변경
print("-"*20+"\ns3:\n", s3)

# %% code 51.
print("-"*20+"\ns1[:3]:", s1[:3])                # Series의 처음 3개 요소 출력
print("-"*20+"\ns1[1:4]:", s1[1:4])              # Series의 1부터 3까지 요소 출력
print("-"*20+"\ns1[s1 > s1.median()]:", s1[s1 > s1.median()])  # Series의 중앙값보다 큰 요소 출력
print("-"*20+"\ns1.iloc[[4, 3, 1]]:", s1.iloc[[4, 3, 1]])  # 특정 위치의 요소 출력

# %% code 52.
np.exp(s2)
print("s2.dtype:", s2.dtype)  # Series의 자료형 출력
s2.dtype
print("np.exp(s2):", np.exp(s2))  # Series의 각 요소에 지수 함수 적용

s3_ar = s3.array
print("-"*20+"\ns3_ar:", s3_ar)  # Series의 array 속성 출력
s3_ndar = s3.to_numpy()
print("s3_ndar:", s3_ndar)  # Series의 to_numpy() 결과 출력

# %% code 53.
print("s3['a']:", s3['a'])  # Series의 'a' 인덱스 요소 출력
s3['e'] = 12.
print("-"*20+"\ns3:\n", s3)  # 기존 'e' 요소의 값을 12로 변경 후 출력

print("-"*20+"\n'e' in s3:", 'e' in s3)  # Series에 'e' 인덱스가 있는지 확인
print("'f' in s3:", 'f' in s3)           # Series에 'f' 인덱스가 있는지 확인 (결과는 False)

print("-"*20+"\ns3.get('f'):", s3.get('f'))         # Series의 'f' 인덱스 요소 가져오기 (없으면 None 반환)
print("s3.get('f', np.nan):", s3.get('f', np.nan))  # Series의 'f' 인덱스 요소 가져오기 (없으면 None 반환)

# %% code 54.
print("s1 + s1:\n", s1 + s1)                 # Series의 요소를 더하기
print("-"*20+"\ns1 * 2:\n", s1 * 2)          # Series의 요소를 2배하기
print("-"*20+"\nnp.exp(s1):\n", np.exp(s1))  # Series의 각 요소에 지수 함수 적용

print("s1[1:] + s1[:-1]:\n", s1[1:] + s1[:-1])  # Series의 슬라이싱 후 요소 더하기

s = pd.Series(np.random.randn(5), name='something')
print("-"*20+"\ns:\n", s)          # Series 전체 출력
print("-"*20+"\ns.name:", s.name)  # Series의 name 속성 출력

s = s.rename("different")
print("s.name(after rename):", s.name)  # Series의 이름 변경 후 출력

# %% code 55.
import pandas as pd  # pandas 사용
import numpy as np   # numpy 사용

d = {'one': pd.Series([1., 2., 3.], index=['a', 'b', 'c'])}
df1 = pd.DataFrame(d)
print("df1:\n", df1)  # df1 출력

d = {'one': pd.Series([1., 2., 3.], index=['a', 'b', 'c']), 'two': pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
df2 = pd.DataFrame(d)
print("-"*20+"\ndf2:\n", df2)  # df2 출력

df3 = pd.DataFrame(d, index=['d', 'b', 'a'])
print("-"*20+"\ndf3:\n", df3)  # df3 출력

df4 = pd.DataFrame(d, index=['d', 'b', 'a'], columns=['two', 'three'])
print("-"*20+"\ndf4:\n", df4)  # df4 출력 (없는 열은 NaN)

# %% code 56.
d = {'one': [1., 2., 3., 4.], 'two': [4., 3., 2., 1.]}
df5 = pd.DataFrame(d)
print("df5:\n", df5)  # DataFrame 출력


print("-"*20+"\ndf5.index:", df5.index)  # DataFrame의 인덱스 출력
print("df5.columns:", df5.columns)       # DataFrame의 열 이름 출력

df6 = pd.DataFrame(d, index=['a', 'b', 'c', 'd'])
print("-"*20+"\ndf6:\n", df6)  # DataFrame 출력 (인덱스 지정)

# %% code 57.
data = np.zeros((2,), dtype=[('A', 'i4'), ('B', 'f4'), ('C', 'S10')])
print("data:", data)  # 구조화된 배열 출력
df7 = pd.DataFrame(data)    
print("-"*20+"\ndf7:\n", df7)  # DataFrame 출력 (구조화된 배열로부터 생성)

data[:] = [(1, 2., 'Hello'), (2, 3., "World")]
print("-"*20+"\ndata:", data)  # 구조화된 배열 출력
df8 = pd.DataFrame(data)
print("-"*20+"\ndf8:\n", df8)  # DataFrame 출력 (구조화된 배열로부터 생성)

df9 = pd.DataFrame(data, index=['first', 'second'])
print("-"*20+"\ndf9:\n", df9)  # DataFrame 출력 (인덱스 지정)

df10 = pd.DataFrame(data, columns=['C', 'A', 'B'])
print("-"*20+"\ndf10:\n", df10)  # DataFrame 출력 (열 순서 변경)

data2 = [{'a': 1, 'b': 2}, {'a': 5, 'b': 10, 'c': 20}]
df11 = pd.DataFrame(data2)
print("-"*20+"\ndf11:\n", df11)  # DataFrame 출력 (딕셔너리 리스트로부터 생성)

df12 = pd.DataFrame({('a', 'b'): {('A', 'B'): 1, ('A', 'C'): 2},
              ('a', 'a'): {('A', 'C'): 3, ('A', 'B'): 4},
              ('a', 'c'): {('A', 'B'): 5, ('A', 'C'): 6},
              ('b', 'a'): {('A', 'C'): 7, ('A', 'B'): 8},
              ('b', 'b'): {('A', 'D'): 9, ('A', 'B'): 10}})
print("-"*20+"\ndf12:\n", df12)                      # DataFrame 출력 (딕셔너리로부터 생성, MultiIndex 사용)
print("-"*20+"\ndf12['a']['b']:\n", df12['a']['b'])  # DataFrame의 MultiIndex 열 접근
print("-"*20+"\ndf12['a', 'b']:\n", df12['a', 'b'])  # DataFrame의 MultiIndex 열 접근 (튜플 사용)

# %% code 58.
data = {"names": ["Kilho", "Kilho", "Kilho", "Charles", "Charles"],
           "year": [2014, 2015, 2016, 2015, 2016],
           "points": [1.5, 1.7, 3.6, 2.4, 2.9]}
df3 = pd.DataFrame(data, columns=["year", "names", "points", "penalty"],
                          index=["one", "two", "three", "four", "five"])
print("df3:\n", df3)                                # df3 출력
print("-"*20+"\ntype(df3['year']): {}".format(type(df3['year'])))  # 단일 열 타입 출력
print("type(df3[['year']]): {}".format(type(df3[['year']])))  # 단일 열을 DataFrame으로 타입 출력
print("type(df3.year): {}".format(type(df3.year)))  # 점 표기법으로 열 타입 출력
print("type(df3[['year', 'points']]): {}".format(type(df3[['year', 'points']])))  # 다중 열 타입 출력

# names 열을 인덱스로 설정
df3 = df3.set_index('names')
print("-"*20+"\ndf3.describe() :\n", df3.describe())  # DataFrame 기술통계 출력

print("-"*20+"\ndf3.iloc[1]:\n ",  df3.iloc[1])  # iloc로 1번 위치(두 번째) 행 출력
print("-"*20+"\ndf3.loc['Kilho']:\n", df3.loc["Kilho"])  # loc로 'Kilho' 인덱스 행 출력

df3 = df3.reset_index()
print("-"*20+"\ndf3:\n", df3)  # 인덱스 초기화 후 df3 출력

# %% code 59.
# DataFrame 생성
data = {'names': ['Kilho', 'Kilho', 'Kilho', 'Charles', 'Charles'],
        'year': [2014, 2015, 2016, 2015, 2016],
        'points': [1.5, 1.7, 3.6, 2.4, 2.9]}
df = pd.DataFrame(data, columns=['year', 'names', 'points'], index=['one', 'two', 'three', 'four', 'five'])
print("-"*20+"\ndf:\n", df)  # DataFrame 출력   
df['penalty'] = 0.5
print("-"*20+"\ndf:\n", df)  # penalty 열 추가 후 출력

# 새로운 열 추가
df['zeros'] = np.arange(5)
print("-"*20+"\ndf:\n", df)  # zeros 열 추가 후 출력

# Series로 열 추가
val = pd.Series([-1.2, -1.5, -1.7, -2.5, -2.2], index=df.index)
df['debt'] = val
print("-"*20+"\ndf:\n", df)  # debt 열 추가 후 출력

# 계산 결과로 새 열 추가
df['net_points'] = df['points'] - df['penalty']
print("-"*20+"\ndf:\n", df)  # net_points 열 추가 후 출력

# 조건식으로 불린 열 추가
df['high_points'] = df['net_points'] > 2.0
print("-"*20+"\ndf:\n", df)  # high_points 열 추가 후 출력

# 열 삭제
del df['high_points']
print("-"*20+"\ndf:\n", df)  # high_points 열 삭제 후 출력

# 1번 위치 인덱스 삭제
df = df.drop(df.index[1])
print("-"*20+"\ndf:\n", df)  # 1번 인덱스 삭제 후 출력

# 중복 제거 후 인덱스 설정
df = df.drop_duplicates(subset='names', keep='last').set_index('names')
print("-"*20+"\ndf:\n", df)  # 중복 제거 및 인덱스 설정 후 출력

# %% code 60.
d1 = {'one': pd.Series([1., 2., 3.], index=['a', 'b', 'c'])}
df1 = pd.DataFrame(d1)
print("df1:\n", df1)  # df1 출력

d2 = {'one': pd.Series([3., 4., 5.], index=['c', 'd', 'e'])}
df2 = pd.DataFrame(d2)
print("-"*20+"\ndf2:\n", df2)  # df2 출력

df1_df2 = pd.concat((df1, df2), ignore_index=True, axis=0)  # df1과 df2 합치기
print("df1_df2:\n", df1_df2)                       # 합친 DataFrame 출력
print("-"*20+"\ndf1_df2.index:\n", df1_df2.index)  # 인덱스 출력

print("-"*20+"\ndf1_df2.duplicated():\n", df1_df2.duplicated())  # 중복 행 확인

# %% code 61.
import pandas as pd

df = pd.DataFrame(
    {'price': [100, 200, 300],
     'weight': [20.3, 15.1, 25.9]},
    index=['idx_a', 'idx_b', 'idx_c'])
print("df:\n", df)

## DataFrame.iterrows() - 행별 반복
for idx, row in df.iterrows():
    print("** 인덱스 이름:", idx)
    print(idx, row)
    print("------"*5)

## DataFrame.items() - 열별 반복  
for col, item in df.items():
    print("** 열 이름:", col)
    print(col, item) # = print(item, sep='\n')
    print("-----"*5)

## DataFrame.itertuples() - 튜플 형태로 행 반복
for row in df.itertuples():
    print(row)

# %% code 62.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter

np.random.seed(19680801)

X = np.linspace(0.5, 3.5, 100)
Y1 = 3+np.cos(X)
Y2 = 1+np.cos(1+X/0.75)/2
Y3 = np.random.uniform(Y1, Y2, len(X))

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1, aspect=1)


def minor_tick(x, pos):
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


def circle(x, y, radius=0.15):
    from matplotlib.patches import Circle
    from matplotlib.patheffects import withStroke
    circle = Circle((x, y), radius, clip_on=False, zorder=10, linewidth=1,
                    edgecolor='black', facecolor=(0, 0, 0, .0125),
                    path_effects=[withStroke(linewidth=5, foreground='w')])
    ax.add_artist(circle)


def text(x, y, text):
    ax.text(x, y, text, backgroundcolor="white",
            ha='center', va='top', weight='bold', color='blue')


# 보조 눈금
circle(0.50, -0.10)
text(0.50, -0.32, "Minor tick label")

# 주 눈금
circle(-0.03, 4.00)
text(0.03, 3.80, "Major tick")

# 보조 눈금
circle(0.00, 3.50)
text(0.00, 3.30, "Minor tick")

# 주 눈금 label
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

# %% code 63.
import matplotlib.pyplot as plt
# 한글 폰트 미설정 시 '축' 등 한글 미표시(code 68 참조)

# 데이터 정의
x = [1, 2, 3, 4, 5]   # x축 좌표값
y = [2, 4, 6, 8, 10]  # y축 좌표값

plt.plot(x, y)            # 선 그래프 그리기
plt.title("Sample Plot")  # 그래프 제목 설정
plt.xlabel("X축")          # X축 레이블 설정
plt.ylabel("Y축")          # Y축 레이블 설정
plt.grid(True)            # 격자 표시 활성화
plt.show()                # 그래프 화면에 출력

# %% code 64.
import matplotlib.pyplot as plt

# 2행 2열의 서브플롯 생성
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

# 레이아웃 조정
plt.tight_layout()
plt.show()

# %% code 65.
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# 첫 번째 플롯 (0,0) - 폰트 스타일링
axes[0,0].plot([1, 2, 3, 4], [2, 3, 5, 10])
axes[0,0].set_xlabel('X-Axis', labelpad=15, 
    fontdict={'family': 'serif', 'color': 'b', 'weight': 'bold', 'size': 14})
axes[0,0].set_ylabel('Y-Axis', labelpad=20, 
    fontdict={'family': 'fantasy', 'color': 'deeppink', 'weight': 'normal', 'size': 'xx-large'})
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

# %% code 66.
import matplotlib.pyplot as plt

# [0,1] 리스트로 간단한 선 그래프 그리기 (x축은 자동으로 [0,1]이 됨)
plt.plot([0,1])
# PNG 형식으로 그래프 저장
plt.savefig(f"{proj_dir}/pic.png")
# PDF(벡터) 형식으로 저장(dpi는 래스터 요소에만 적용), 여백을 최소화하고 패딩 0.1 추가
plt.savefig(f"{proj_dir}/pic.pdf", dpi=300, bbox_inches='tight', pad_inches=0.1 )
plt.show()

# %% code 67.
import matplotlib.pyplot as plt

# 파일 경로 설정 (proj_dir 폴더 내의 pic.png 파일)
fname = f"{proj_dir}/pic.png"

# 이미지 파일을 읽어서 배열로 저장
chart_png = plt.imread(fname)

# 이미지를 화면에 표시 (보간법 없이 원본 픽셀 그대로 표시)
plt.imshow(chart_png, interpolation='none')

# 그래프를 화면에 출력
plt.show()

# %% code 68.
# 한글 폰트 설정 및 깨짐 문제 해결
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform

# 운영체제별 한글 폰트 설정
def setup_korean_font():
    """
    운영체제에 따라 적절한 한글 폰트를 설정하는 함수
    """
    system = platform.system()
    
    if system == 'Windows':
        # Windows의 경우 맑은 고딕 또는 굴림 사용
        font_candidates = ['Malgun Gothic', 'Gulim', 'Batang']
    elif system == 'Darwin':  # macOS
        # macOS의 경우 애플 고딕 사용
        font_candidates = ['AppleGothic', 'Arial Unicode MS']
    else:  # Linux
        # Linux의 경우 나눔고딕 또는 Noto Sans CJK 사용
        font_candidates = ['NanumGothic', 'Noto Sans CJK KR', 'DejaVu Sans']
    
    # 사용 가능한 폰트 찾기
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    for font in font_candidates:
        if font in available_fonts:
            plt.rcParams['font.family'] = font
            print(f"한글 폰트 설정 완료: {font}")
            break
    else:
        # 대체 폰트 설정
        plt.rcParams['font.family'] = 'DejaVu Sans'
        print("기본 폰트로 설정됨 (한글이 깨질 수 있음)")
    
    # 마이너스 폰트 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False
    
    return plt.rcParams['font.family']

# 한글 폰트 설정 실행
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

# %% code 69.
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(4, 3))
ax.plot([1, 2, 3, 4], [2, 3, 5, 10])
ax.set_xlabel("X축")
ax.set_ylabel("Y축")
du.save_figure(fig, proj_dir / "pic_du")  # pic_du.pdf와 pic_du.png로 저장
plt.close(fig)                             # 화면에는 그리지 않음

fpaths = du.list_files(proj_dir, "pdf")    # 데이터 폴더의 PDF 파일 목록
