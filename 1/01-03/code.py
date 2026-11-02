# 지구과학 데이터 사이언스 1 | I-03. Python 코딩 시작하기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code Ⅰ-1.
# 괄호 안에서는 원하는 곳에서 줄을 바꿀 수 있음
planets = ['수성', '금성', '지구', '화성',
           '목성', '토성', '천왕성', '해왕성']
total = (1 + 2 + 3
         + 4 + 5)

# 괄호 밖에서는 줄 끝의 \ 로 이어 쓰기
area = 3.14 * \
       2 ** 2

# 괄호 안에 나란히 쓴 문자열은 하나로 이어짐
message = ('괄호 안에 나란히 쓴 문자열은 '
           '하나로 이어 붙여집니다.')

x = 1; y = 2  # 세미콜론으로 한 줄에 두 문장(권장하지 않음)
print(len(planets), total, area, x + y)
print(message)

# %% code Ⅰ-2.
x = 0              # x에 0 저장
y = 'Hello world'  # y에 문자열 'Hello world' 저장
x                  # x의 값 출력(셀의 마지막 줄)

# %% code Ⅰ-3.
y = 'Hello world'
y

# %% code Ⅰ-4.
y1      =      'Hello world'  # = 앞뒤의 공백은 상관없음
y1

# %% code Ⅰ-5.
class = 'Hello world'  # class는 예약어라 식별자로 쓸 수 없음

# %% code Ⅰ-6.
print('괄호 안의 글자가 그대로 출력됩니다.')  # 괄호 안의 내용 출력
y = 'Hello world'
y                                                 # 마지막 줄이 아니면 출력되지 않음
print(y)                                          # print()는 항상 출력
print("y")                                        # 문자 "y" 출력
y                                                 # 마지막 줄이면 자동 출력

# %% code Ⅰ-7.
a = 3           # 정수(int)
b = 3.14        # 실수(float, 부동소수점수)
c = 3.14159
d = 5.1e10      # 과학적 표기법 5.1×10^10
e = 2.5 + 5.3j  # 복소수(complex)
print("type(a): ", type(a), "a: ", a)
print("type(b): ", type(b), "b: ", b)
print("type(c): ", type(c), "c: ", c)
print("type(d): ", type(d), "d: ", d)
print("type(e): ", type(e), "e: ", e)

hungry = True  # 불(bool)
need_coffee = False
print("type(hungry): ", type(hungry), "hungry: ", hungry)
print("type(need_coffee): ", type(need_coffee), "need_coffee: ", need_coffee)

# %% code Ⅰ-8.
my_value1 = 'I love programming in Python.'    # 작은따옴표로 감싼 문자열
print(my_value1)
my_value2 = "'I love programming in Python.'"  # 큰따옴표 안에 작은따옴표
print(type(my_value1))
print(my_value2)
my_value3 = '"I love programming in Python."'  # 작은따옴표 안에 큰따옴표
print(my_value3)

# %% code Ⅰ-9.
my_value4 = '\'I love programming in Python.\''  # \'는 따옴표 문자(이스케이프 문자)
print(my_value4)
my_value5 = "\n\t   Hello      wo\nrld!   \n\n\t\nBye."  # \n 줄바꿈, \t 탭
print(my_value5)

# %% code Ⅰ-10.
my_value5 ="""MIRANDA
O, wonder!
How many goodly creatures are there here!
How beauteous mankind is! O brave new world
That has such people in't!"""
print("my_value5 :", my_value5)

my_value6 ='''MIRANDA
O, wonder!
How many goodly creatures are there here!
How beauteous mankind is! O brave new world
That has such people in't!'''
print("my_value6 :", my_value6)

# %% code Ⅰ-11.
text_add1 = 'abc' + ' ' +'def'
print("text_add1 :", text_add1)

text_add2 = "=+"*5  # 문자열 5번 반복
print("text_add2 :", text_add2)

# %% code Ⅰ-12.
our_string = 'python is the best language ever'
print("our_string.capitalize() :", our_string.capitalize())  # 첫 글자를 대문자로
filename = '../data/PTF_d022683_f02_c06_u000114210_p12_refimg.fits'
print("filename.endswith('fits') :", filename.endswith('fits'))  # 'fits'로 끝나는지 확인
our_string ='python is the best language ever'
print("our_string.find('the') :", our_string.find('the'))  # 'the'가 처음 나오는 위치
print("our_string.split(' ') :", our_string.split(' '))  # 공백 기준으로 나눠 리스트로

# %% code Ⅰ-13.
z = 10
print ('I am a fan of the number: ' + z)  # 정수와 문자열은 더할 수 없음 → TypeError

# %% code Ⅰ-14.
z = 10
print ('I am a fan of the number: ' + str(z))  # str()로 문자열 변환 후 결합

# %% code Ⅰ-15.
decimalValue, stringValue, floatValue = 42, 'Hello', 3.14  # 여러 변수에 한 번에 할당
print ('출력 예:', decimalValue, stringValue, floatValue)  # (1) 쉼표로 나열
print ('출력 예: %d %s %f' % (decimalValue, stringValue, floatValue))  # (2) % 연산자
# (3) format() 메서드
print ('출력 예: {0:d} {1:s} {2:f}'.format(decimalValue, stringValue, floatValue))
print (f'출력 예: {decimalValue} {stringValue} {floatValue}')  # (4) f-string

# %% code Ⅰ-16.
print("4 + 10 =", 4 + 10)
print("4 - 10 =", 4 - 10)
print("5 * 10 =", 5 * 10)
print("5 / 10 =", 5 / 10)
print("10 % 4 =", 10 % 4)
print("2**3 =", 2**3)

# %% code Ⅰ-17.
print("abs(9) :", abs(9))
print("divmod(8, 4) :", divmod(8, 4))              # (몫, 나머지) 튜플
print("pow(2, 3) :", pow(2, 3))
print("pow(2, 3, 5) :", pow(2, 3, 5))              # (2**3) % 5
print("round(3.14159) :", round(3.14159))
print("round(3.14159, 2) :", round(3.14159, 2))
print("round(3.14159, -2) :", round(3.14159, -2))  # 십의 자리에서 반올림
print("divmod(9, 4) :", divmod(9, 4))

# %% code Ⅰ-18.
print("8 > 10 :", 8 > 10 )
print("256 < 725:", 256 < 725)
print("10 == 10 :", 10 == 10)
print("10 != 10 :", 10 != 10)
print("10 == 10 + 1 :", 10 == 10 + 1)
print("type(8 > 10) :", type(8 > 10))  # 비교 결과는 불(bool)

# %% code Ⅰ-19.
print("10 == 10 and 10 > 10 :", 10 == 10 and 10 > 10)
print("10 == 10 or 10 > 10 :", 10 == 10 or 10 > 10)
print("not(10 == 10) :", not(10 == 10))
print("not(10 == 10 and 10 > 10) :", not(10 == 10 and 10 > 10))
print("not(10 == 10 or 10 > 10) :", not(10 == 10 or 10 > 10))

# %% code Ⅰ-20.
myLst = []
print("myLst: ", myLst)
print("type(myLst):", type(myLst))
myLst2 = [1, 2, 3, 4, 5]
print("myLst2 :", myLst2)
print("type(myLst2):", type(myLst2))

# %% code Ⅰ-21.
myStrLst = ['Hello', 'Python', 'lists']
print("myStrLst: ", myStrLst)
multiLst = [1, 2, 'three', 4, 'five', 'six']  # 여러 자료형을 섞은 리스트
print("multiLst: ", multiLst)
comboLst = [1, myStrLst, multiLst]            # 리스트를 원소로 갖는 리스트
print("comboLst: ", comboLst)
my_newLst1 = ['new_item1', 'new_item2', [1, 2, 3, 4], 'new_item3']
print("my_newLst1: ", my_newLst1)

# %% code Ⅰ-22.
myStrLst = ['Hello', 'Python', 'lists'] 
print("len(myStrLst): ", len(myStrLst))
print("myStrLst[2]: ",  myStrLst[2])    # 인덱스는 0부터
print("myStrLst[-1]: ",  myStrLst[-1])  # 음수 인덱스는 뒤에서부터

my_newLst2 = [1, 2, 3, ['a', 'b', 'c']]
print("my_newLst2[-1][0]: ", my_newLst2[-1][0])  # 마지막 원소(리스트)의 첫 원소

# %% code Ⅰ-23.
print("myStrLst[0:2]: ", myStrLst[0:2])  # 시작 인덱스는 포함, 끝 인덱스는 제외
print("myStrLst[:2]: ", myStrLst[:2])    # 시작 생략 → 처음부터
print("myStrLst[1:]: ", myStrLst[1:])    # 끝 생략 → 끝까지

myStrLst_copy = myStrLst[:]                      # 리스트 사본
print("myStrLst_copy: ", myStrLst_copy)
newLst = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
print("newLst[0:10:1]: ", newLst[0:10:1])        # 세 번째 값은 간격(step)
my_newLst3 = [1, 2, 3, ['a', 'b', 'c'], 4, 5]
print("my_newLst3[3][:2]: ", my_newLst3[3][:2])  # 4번째 원소(리스트)를 다시 슬라이싱

# %% code Ⅰ-24.
newLst1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
print("newLst1:", newLst1)
newLst1.append('h')
print("newLst1(append 뒤):", newLst1)

newLst2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
print("newLst2:", newLst2)
newLst2.insert(2, 'c')
print("newLst2(insert 뒤):", newLst2)

anotherLst = ['a', 'b', 'c']
print("anotherLst:", anotherLst)
anotherLst.insert(2, newLst2)  # 리스트 전체가 원소 하나로 들어감(중첩 리스트)
print("anotherLst(insert 뒤):", anotherLst)

newLst3 = ['a','b','c','d','e','f']
print("newLst3:", newLst3)
del newLst3[2]
print("newLst3(del 뒤):", newLst3)

newLst4 = ['a','b','c','d','e','f']
print("newLst4:", newLst4)
newLst4.remove('e')  # 값 'e'를 찾아 삭제
print("newLst4(remove 뒤):", newLst4)

newLst5 = ['h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
newLst5.extend(['q', 'r'])  # 다른 리스트의 원소를 끝에 추가
print("newLst5:", newLst5)

# %% code Ⅰ-25.
myTuple1 = ()  # 빈 튜플
print("len(myTuple1):", len(myTuple1))
print("myTuple1:", myTuple1)

myTuple2 = (1, 'two', 3, 'four')  # 서로 다른 자료형도 담을 수 있음
print("len(myTuple2):", len(myTuple2))
print("myTuple2[2]:", myTuple2[2])

# %% code Ⅰ-26.
myDic1 = {}
print("myDic1:", myDic1)
print("len(myDic1):", len(myDic1))

# 감마선 폭발(GRB) 천체 정보
myDic2 = {'name': 'GRB 130702A', 'redshift': 0.145, 'ra': (14, 29, 14.78), 'dec': (15, 46, 26.4)}
print("myDic2:", myDic2)
print("len(myDic2):", len(myDic2))
print("myDic2['ra']:", myDic2['ra'])    # 적경(시, 분, 초)
print("myDic2['dec']:", myDic2['dec'])  # 적위(도, 분, 초)

myDic3 = {'name': 'GRB 130702A', 'redshift': 0.145, 'ra': (14, 29, 14.78), 'dec': (15, 46, 26.4)}
print("myDic3:", myDic3)
myDic3['url'] = 'http://gcn.gsfc.nasa.gov/other/130702A.gcn3'
print("myDic3('url' 추가 뒤):", myDic3)

myDic4 = {'name': 'GRB 130702A', 'redshift': 0.145, 'ra': (14, 29, 14.78), 'dec': (15, 46, 26.4)}
print("myDic4:", myDic4)
del myDic4['name']  # 키 'name'과 그 값 삭제
print("myDic4('name' 삭제 뒤):", myDic4)

# %% code Ⅰ-27.
myDic5 = {1: 'a', 2: 'b', 1: 'c'}  # 키 1이 중복됨
print("myDic5:", myDic5)           # 마지막 값만 남음

# %% code Ⅰ-28.
# 예제 1: 다중 변수 할당과 비교 연산
a, b, c = 5, 5.0, 15 + 3
print("a, b, c 값:", a, b, c)
print("a != b 결과:", a != b)
if a != b:
    print('값이 다릅니다!')
else:
    print('값이 같습니다!')

# 예제 2: 문자열과 숫자 비교
name, age, score = "김철수", 25, 90 + 5
print("-"*20)
print("이름, 나이, 점수:", name, age, score)
print("나이와 점수가 같은가?:", age == score)
if age == score:
    print('나이와 점수가 같네요!')
else:
    print('나이와 점수가 다릅니다!')

# 예제 3: 딕셔너리와 조건문 활용
학생정보 = {'이름': '박영희', '학년': 3, '성적': 'A', '동아리': '축구부'}
print("-"*20)
print("'이름' 키가 존재하는가?:", '이름' in 학생정보)
print("'이름' 키가 없고 '학년' 키가 있는가?:", (not '이름' in 학생정보) and '학년' in 학생정보)
print("'이름'과 '전화번호' 키가 모두 없는가?:", (not '이름' in 학생정보) and (not '전화번호' in 학생정보))

if '이름' in 학생정보:
    print('학생의 이름 정보가 있습니다')
elif '학년' in 학생정보:
    print('이름 정보는 없지만 학년 정보가 있습니다')
else:
    print('이름과 학년 정보가 모두 없습니다')

# 예제 4: 온도와 날씨 정보 딕셔너리
날씨정보 = {'온도': 25, '습도': 60, '풍속': 5, '강수확률': 30}
print("-"*20)
print("'온도' 정보가 있는가?:", '온도' in 날씨정보)
print("'온도' 정보가 없고 '습도' 정보가 있는가?:", (not '온도' in 날씨정보) and '습도' in 날씨정보)
print("'온도'와 '기압' 정보가 모두 없는가?:", (not '온도' in 날씨정보) and (not '기압' in 날씨정보))

if '온도' in 날씨정보:
    print('현재 온도 정보를 확인할 수 있습니다')
elif '습도' in 날씨정보:
    print('온도 정보는 없지만 습도 정보가 있습니다')
else:
    print('온도와 습도 정보가 모두 없습니다')

# %% code Ⅰ-29.
test_list = ['one', 'two', 'three']
for i in test_list:
    print(i)

print("-"*20)
for i in range(0, 5, 1):  # 0, 1, 2, 3, 4
    print ("value = ", i)

print("-"*20)
for i in range(4, 10):  # 4, 5, ..., 9
    print (i)

print("-"*20)
for i in range(2001, 2010, 2):  # 2001, 2003, ..., 2009
    print (i**2)

print("-"*20)
for i in range(1, 10, 2):  # 1부터 9까지 홀수
    print(i, end=" ")  # 줄바꿈 대신 공백

# %% code Ⅰ-30.
a = [1,2,3,4]
result1 = []
for num in a:
    result1.append(num*3)  # 각 원소의 3배를 추가

print("result1 :", result1)

print("-"*20)
# 리스트 컴프리헨션: 구구단 2~9단의 곱
result2 = [x*y for x in range(2,10) for y in range(1,10)]
print("result2 :", result2)

# %% code Ⅰ-31.
a = 1
while a < 5:
    a = a * 2
    print (a)

print("-"*20)
treeHit = 0  # 나무를 찍은 횟수
while treeHit < 3:
    treeHit = treeHit + 1
    print("나무를 %d번 찍었습니다." % treeHit)
    if treeHit == 3:
        print("나무 넘어갑니다.")

# %% code Ⅰ-32.
coffee = 3    # 커피 재고
money = 30
while money:  # 0이 아닌 수는 True로 평가
    print("돈을 받았으니 커피를 줍니다.")
    coffee = coffee - 1
    print("남은 커피의 양은 %d개입니다." % coffee)
    if coffee == 0:
        print("커피가 다 떨어졌습니다. 판매를 중지합니다.")
        break  # while 반복문 종료
print("-"*20)
a = 0
while a < 10:
    a = a + 1
    if a % 2 == 0: continue  # 짝수면 건너뛰고 다음 반복
    print(a)
print("-"*20)
# 주의: 이 반복은 끝나지 않음(■ 중지 단추로 멈춤)
while True:
    print("중지 단추를 눌러야 while문을 빠져나갈 수 있습니다.")

# %% code Ⅰ-33.
def square(n):
    return n * n
print("square(3) :", square(3))

def powers(n):
    return n**2, n**3  # 여러 값은 튜플로 반환
print("powers(3) :", powers(3))

def greet(name):
    """이름을 받아서 인사말을 반환하는 함수"""  # 독스트링(docstring)
    return f"안녕하세요, {name}님!"

print(greet("홍길동"))

def calculate_area(width, height):
    """직사각형의 넓이를 계산하는 함수"""
    area = width * height
    return area
print("넓이:", calculate_area(5, 10))

# 같은 이름으로 다시 정의하면 앞의 함수를 덮어씀
def calculate_area(radius):  # radius는 매개변수
    return 3.14159 * radius ** 2  # 원주율 근삿값(math.pi로 대체 가능)

print("원의 넓이:", calculate_area(5))  # 5는 인수

# %% code Ⅰ-34.
def add(a, b):  # a, b는 매개변수
    return a+b
print("add(3, 4):", add(3, 4))  # 3, 4는 인수

def fibonacci(seed, n):  # 피보나치 수열 만들기
    while len(seed) < n:
        seed.append(seed[-1] + seed[-2])  # 마지막 두 원소의 합을 추가

# return 문 없음: 리스트를 직접 수정
seed = [1, 1]        # 시작값
fibonacci(seed, 10)  # 원소 10개까지 생성
print("seed :", seed)

# %% code Ⅰ-35.
import math

def sinc(x):
    return math.sin(x) / x

print("sinc(0) :", sinc(0))  # x = 0이면 ZeroDivisionError

# %% code Ⅰ-36.
import math

def sinc(x):
    """
    sinc 함수를 계산하는 함수
    sinc(x) = sin(x)/x (x ≠ 0일 때)
    sinc(0) = 1 (x = 0일 때, 극한값)
    """
    try:
        result = math.sin(x) / x
    except ZeroDivisionError:  # x = 0이면 0으로 나누기 오류
        result = 1  # 극한값 sinc(0) = 1
    return result

print("sinc(0) :", sinc(0))  # 예외 처리로 1 반환
print("sinc(0.20) :", sinc(0.20))
