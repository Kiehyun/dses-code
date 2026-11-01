# 지구과학 데이터 사이언스 1 | I-03. Python 코딩 시작하기
# 책에 실린 코드만 모았습니다. 설명은 책을 참고하세요.

# %% code 1.
x = 0              #x에 0을 담아 둔다.
y = 'Hello world'  #y에 'Hello world'라는 문자열을 담아 둔다.   
x                  #x에 들어 있는 내용을 출력한다.

# %% code 2.
y = 'Hello world'  #y에 'Hello world'를 담아 둔다.
y                  #y에 담겨있는 내용을 출력한다.

# %% code 3.
y1      =      'Hello world'  #y1에 'Hello world'를 담아 둔다.
y1                            #y1에 담겨있는 내용을 출력한다.

# %% code 4.
class = 'Hello world'  #class는 예약어 이므로 파란색이 되며 식별자로 쓸 수 없다. 

# %% code 5.
print('This text will be printed to the command line ....')  #괄호()안의 내용을 화면에 출력한다.
y = 'Hello world'  #y에 'Hello world'를 담아 둔다.
y                  #변수명만 적어준 경우에는 마지막행이 아니면 출력이 되지 않는다.
print(y)           #print 문을 사용하면 항상 출력된다.
print("y")         #"y"라는 문자를 출력한다.
y                  #변수명만 적어준 경우에는 마지막행에 있을때만 출력된다.

# %% code 6.
a = 3                                  # 정수형(integer)
b = 3.14                               # 실수형(float, 부동소수점수)
c = 3.14159                            # 부동소수점수
d = 5.1e10                             # 과학적 표기법 5.1×10^10
e = 2.5 + 5.3j                         # 복소수
print("type(a): ", type(a), "a: ", a)  # 3을 출력함
print("type(b): ", type(b), "b: ", b)  # 3.14를 출력함
print("type(c): ", type(c), "c: ", c)  # 3.14159를 출력함
print("type(d): ", type(d), "d: ", d)  # 5.1e10을 출력함
print("type(e): ", type(e), "e: ", e)  # 복소수를 출력함

hungry = True        # 불린 리터럴
need_coffee = False  # 또 다른 불린 리터럴
print("type(hungry): ", type(hungry), "hungry: ", hungry)  # True를 출력함
print("type(need_coffee): ", type(need_coffee), "need_coffee: ", need_coffee)  # False를 출력함

# %% code 7.
my_value1 = 'I love programming in Python.'    #my_value1이라는 식별자에 'I love programming in Python'을 담아둔다.
print(my_value1)                               #my_value1이라는 식별자에 담겨져 있는 내용이 출력된다.
my_value2 = "'I love programming in Python.'"  #my_value2 라는 식별자에 작은 따옴표가 포함된 "'I love programming in Python'"을 담아둔다.
print(type(my_value1))
print(my_value2)                               #my_value2이라는 식별자에 담겨져 있는 내용이 출력된다.
my_value3 = '"I love programming in Python."'  #my_value3 라는 식별자에 큰 따옴표가 포함된 '"I love programming in Python"'을 담아둔다.
print(my_value3)                               #my_value3이라는 식별자에 담겨져 있는 내용이 출력된다.

# %% code 8.
my_value4 = '\'I love programming in Python.\''  #
print(my_value4)                                 #my_value4이라는 식별자에 담겨져 있는 내용이 출력된다.
my_value5 = "\n\t   Hello      wo\nrld!   \n\n\t\nBye."
print(my_value5)

# %% code 9.
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

# %% code 10.
text_add1 = 'abc' + ' ' +'def'
print("text_add1 :", text_add1)

text_add2 = "=+"*5
print("text_add2 :", text_add2)

# %% code 11.
our_string = 'python is the best language ever'
print("our_string.capitalize() :", our_string.capitalize())  # 문자열의 첫 글자를 대문자로
filename = '../data/PTF_d022683_f02_c06_u000114210_p12_refimg.fits'
print("filename.endswith('fits') :", filename.endswith('fits'))  # 주어진 문자열로 끝나는지 확인한다.
our_string ='python is the best language ever'
print("our_string.find('the') :", our_string.find('the'))  # 문자열에서 'the'가 처음으로 나타나는 위치를 찾는다.
print("our_string.split(' ') :", our_string.split(' '))  # 문자열을 공백으로 나누어 리스트로 반환한다.

# %% code 12.
z = 10                                    # z에 10을 담아 둔다.
print ('I am a fan of the number: ' + z)  # z는 정수형이므로 문자열과 더할 수 없다. str() 함수를 사용하여 z를 문자열로 변환해야 한다.

# %% code 13.
z = 10                                         # z에 10을 담아 둔다.
print ('I am a fan of the number: ' + str(z))  # z를 문자열로 변환하여 출력한다.

# %% code 14.
decimalValue, stringValue, floatValue = 42, 'Hello', 3.14  # 여러 값을 동시에 선언한다.
print ('String of text goes here', decimalValue, stringValue, floatValue) #(1) 여러 값을 쉼표로 구분하여 출력한다.
print ('String of text goes here %d %s %f' % (decimalValue, stringValue, floatValue)) #(2) % 연산자를 사용하여 문자열을 포맷팅한다.
print ('String of text goes here {0:d} {1:s} {2:f}'.format(decimalValue, stringValue, floatValue)) # (3) format() 메서드를 사용하여 문자열을 포맷팅한다.
print (f'String of text goes here {decimalValue} {stringValue} {floatValue}') #(4) f-string을 사용하여 문자열을 포맷팅한다.

# %% code 15.
print("4 + 10 =", 4 + 10)  # 4+10을 계산하여 출력한다.
print("4 - 10 =", 4 - 10)  # 4-10을 계산하여 출력한다.
print("5 * 10 =", 5 * 10)  # 5*10을 계산하여 출력한다.
print("5 / 10 =", 5 / 10)  # 5/10을 계산하여 출력한다.
print("10 % 4 =", 10 % 4)  # 10을 4로 나눈 나머지를 계산하여 출력한다.
print("2**3 =", 2**3)      # 2의 3제곱을 계산하여 출력한다.

# %% code 16.
print("abs(9) :", abs(9))                          # 9의 절대값
print("divmod(8, 4) :", divmod(8, 4))              # 8을 4로 나눈 몫과 나머지로 이루어진 튜플
print("pow(2, 3) :", pow(2, 3))                    # 2의 3제곱을 계산한다.
print("pow(2, 3, 5) :", pow(2, 3, 5))              # (2의 3제곱) % 5를 계산한다.    
print("round(3.14159) :", round(3.14159))          # 3.14159를 반올림한다.
print("round(3.14159, 2) :", round(3.14159, 2))    # 3.14159를 소수점 둘째 자리까지 반올림한다.
print("round(3.14159, -2) :", round(3.14159, -2))  # 3.14159를 십의 자리에서 반올림한다. 
print("divmod(9, 4) :", divmod(9, 4))              # 9을 4로 나눈 몫과 나머지로 이루어진 튜플   

# %% code 17.
print("8 > 10 :", 8 > 10 )             # 단순 비교
print("256 < 725:", 256 < 725)         # 단순 비교
print("10 == 10 :", 10 == 10)          # 단순 비교
print("10 != 10 :", 10 != 10)          # 단순 비교
print("10 == 10 + 1 :", 10 == 10 + 1)  # 단순 비교
print("type(8 > 10) :", type(8 > 10))  # 불린 타입을 확인한다.

# %% code 18.
print("10 == 10 and 10 > 10 :", 10 == 10 and 10 > 10)  # 논리 연산자 사용
print("10 == 10 or 10 > 10 :", 10 == 10 or 10 > 10)  # 논리 연산자 사용
print("not(10 == 10) :", not(10 == 10))              # 논리 연산자 사용
print("not(10 == 10 and 10 > 10) :", not(10 == 10 and 10 > 10))  # 논리 연산자 사용
print("not(10 == 10 or 10 > 10) :", not(10 == 10 or 10 > 10))  # 논리 연산자 사용 

# %% code 19.
myLst = []                            # 빈 리스트를 정의
print("myLst: ", myLst)               # 빈 리스트를 출력한다.
print("type(myLst):", type(myLst))    # 빈 리스트의 타입을 출력한다.
myLst2 = [1, 2, 3, 4, 5]              # 리스트에 1, 2, 3, 4, 5 가 들어 있음.
print("myLst2 :", myLst2)             # 리스트를 출력한다.
print("type(myLst2):", type(myLst2))  # 리스트의 타입을 출력한다. 

# %% code 20.
myStrLst = ['Hello', 'Python', 'lists']       # 문자열 값의 리스트를 정의
print("myStrLst: ", myStrLst)                 # 문자열 리스트를 출력한다.
multiLst = [1, 2, 'three', 4, 'five', 'six']  # 복수의 자료형을 포함하는 리스트를 정의
print("multiLst: ", multiLst)                 # 복수의 자료형을 포함하는 리스트를 출력한다.
comboLst = [1, myStrLst, multiLst]            # 리스트를 포함하는 리스트를 정의
print("comboLst: ", comboLst)                 # 리스트를 포함하는 리스트를 출력한다.
my_newLst1 = ['new_item1', 'new_item2', [1, 2, 3, 4], 'new_item3']  # 리스트를 포함하는 리스트를 한 줄로 정의
print("my_newLst1: ", my_newLst1)             # 리스트를 포함하는 리스트를 출력한다.

# %% code 21.
myStrLst = ['Hello', 'Python', 'lists'] 
print("len(myStrLst): ", len(myStrLst))  # 리스트의 길이를 출력한다.
print("myStrLst[2]: ",  myStrLst[2])     # 리스트에서 특정 원소를 얻기
print("myStrLst[-1]: ",  myStrLst[-1])   # 리스트에서 특정 원소를 얻기

my_newLst2 = [1, 2, 3, ['a', 'b', 'c']]
print("my_newLst2[-1][0]: ", my_newLst2[-1][0])  # 리스트에서 특정 원소를 얻기   

# %% code 22.
myStrLst[0:2]                          # 슬라이싱 (슬라이싱의 시작 인덱스의 원소는 포함하고 끝 인덱스의 원소는 제외한다는 점에 유의)
print("myStrLst[:2]: ", myStrLst[:2])   # 시작 인덱스가 생략되면 처음부터 시작한다. 
print("myStrLst[1:]: ", myStrLst[1:])  # 끝 인덱스가 생략되면 끝까지 포함한다.

myStrLst_copy = myStrLst[:]              # 썰기를 통해 리스트의 사본을 생성
print("myStrLst_copy: ", myStrLst_copy)  # 리스트의 사본을 출력한다.    
newLst = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
print("newLst[0:10:1]: ", newLst[0:10:1])  # 썰기에서 세번째 인자를 사용하면 건너뛰기가 됨, 이 예제는 한 칸 씩 이동(step)
my_newLst3 = [1, 2, 3, ['a', 'b', 'c'], 4, 5]
print("my_newLst3[3][:2]: ", my_newLst3[3][:2])  # 리스트의 특정 원소에서 슬라이싱을 사용하여 부분 리스트를 얻는다.

# %% code 23.
newLst1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g']  # 리스트 생성
print("newLst1:", newLst1)                     # 원본 리스트 출력
newLst1.append('h')                            # 리스트 끝에 'h' 추가
print("newLst1(after append):", newLst1)       # append 후 리스트 출력

newLst2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g']  # 새로운 리스트 생성
print("newLst2:", newLst2)                     # 원본 리스트 출력
newLst2.insert(2, 'c')                         # 인덱스 2 위치에 'c' 삽입
print("newLst2(after insert):", newLst2)       # insert 후 리스트 출력

anotherLst = ['a', 'b', 'c']                    # 다른 리스트 생성
print("anotherLst:", anotherLst)                # 원본 리스트 출력
anotherLst.insert(2, newLst2)                   # 인덱스 2 위치에 newLst2 전체 리스트를 삽입
print("anotherLst(after insert):", anotherLst)  # insert 후 리스트 출력 (중첩 리스트가 됨)

newLst3 = ['a','b','c','d','e','f']    # 새로운 리스트 생성
print("newLst3:", newLst3)             # 원본 리스트 출력
del newLst3[2]                         # 인덱스 2 위치의 요소('c') 삭제
print("newLst3(after del):", newLst3)  # del 후 리스트 출력

newLst4 = ['a','b','c','d','e','f']       # 새로운 리스트 생성
print("newLst4:", newLst4)                # 원본 리스트 출력
newLst4.remove('e')                       # 'e' 요소를 찾아서 삭제
print("newLst4(after remove):", newLst4)  # remove 후 리스트 출력

newLst5 = ['h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']  # 새로운 리스트 생성
newLst5.extend(['q', 'r'])  # 다른 리스트의 요소를 끝에 추가
print("newLst5:", newLst5)  # extend 후 리스트 출력

# %% code 24.
myTuple1 = ()                           # 빈 튜플 생성
print("len(myTuple1):", len(myTuple1))  # 빈 튜플의 길이 출력 (0)
print("myTuple1:", myTuple1)            # 빈 튜플 출력

myTuple2 = (1, 'two', 3, 'four')        # 서로 다른 자료형을 포함하는 튜플 생성 (정수, 문자열, 정수, 문자열)
print("len(myTuple2):", len(myTuple2))  # 튜플의 길이 출력 (4)
print("myTuple2[2]:", myTuple2[2])      # 인덱스 2 위치의 요소 출력 (3)

# %% code 25.
myDic1 = {}                         # 빈 딕셔너리 생성
print("myDic1:", myDic1)            # 빈 딕셔너리 출력
print("len(myDic1):", len(myDic1))  # 빈 딕셔너리의 길이 출력 (0)

myDic2 = {'name': 'GRB 130702A', 'redshift': 0.145, 'ra': (14, 29, 14.78), 'dec': (15, 46, 26.4)}  # 천체 데이터를 담은 딕셔너리 생성
print("myDic2:", myDic2)                # 딕셔너리 전체 출력
print("len(myDic2):", len(myDic2))      # 딕셔너리의 길이 출력 (4개의 키-값 쌍)
print("myDic2['ra']:", myDic2['ra'])    # 'ra'(적경) 키에 해당하는 값 출력
print("myDic2['dec']:", myDic2['dec'])  # 'dec'(적위) 키에 해당하는 값 출력

myDic3 = {'name': 'GRB 130702A', 'redshift': 0.145, 'ra': (14, 29, 14.78), 'dec': (15, 46, 26.4)}  # 새로운 딕셔너리 생성
print("myDic3:", myDic3)                        # 원본 딕셔너리 출력
myDic3['url'] = 'http://gcn.gsfc.nasa.gov/other/130702A.gcn3'  # 새로운 키-값 쌍 추가
print("myDic3(after 'url' is added):", myDic3)  # 'url' 키가 추가된 후 딕셔너리 출력

myDic4 = {'name': 'GRB 130702A', 'redshift': 0.145, 'ra': (14, 29, 14.78), 'dec': (15, 46, 26.4)}  # 새로운 딕셔너리 생성
print("myDic4:", myDic4)                           # 원본 딕셔너리 출력
del myDic4['name']                                 # 'name' 키와 해당 값 삭제
print("myDic4(after 'name' is deleted):", myDic4)  # 'name' 키가 삭제된 후 딕셔너리 출력

# %% code 26.
myDic5 = {1: 'a', 2: 'b', 1: 'c'}  # 키가 중복된 딕셔너리 생성
print("myDic5:", myDic5)  # 마지막 값이 유지됨

# %% code 27.
# 예제 1: 다중 변수 할당과 비교 연산
a, b, c = 5, 5.0, 15 + 3    # 세 변수에 서로 다른 타입의 값 할당
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

# %% code 28.
test_list = ['one', 'two', 'three']  # 문자열 리스트 생성
for i in test_list:                  # 리스트의 각 요소를 반복
    print(i)  # 각 요소를 한 줄씩 출력

print("-"*20)             # 구분선 출력
for i in range(0, 5, 1):  # 0부터 4까지 1씩 증가하며 반복
    print ("value = ", i)  # "value = " 형식으로 각 값을 출력

print("-"*20)           # 구분선 출력
for i in range(4, 10):  # 4, 5, 6, 7, 8, 9를 반환한다.
    print (i)  # 각 숫자를 한 줄씩 출력

print("-"*20)                   # 구분선 출력
for i in range(2001, 2010, 2):  # 2001, 2003, 2005, 2007, 2009를 반환한다.
    print (i**2)  # 각 숫자의 제곱을 출력

print("-"*20)              # 구분선 출력
for i in range(1, 10, 2):  # 1부터 9까지 2씩 증가하며 반복 (홀수)
    print(i, end=" ")  # 줄바꿈 없이 공백으로 구분하여 출력

# %% code 29.
a = [1,2,3,4]  # 리스트 a에 [1,2,3,4] 저장
result1 = []   # 빈 리스트 result1 생성
for num in a:  # 리스트 a의 각 요소를 num에 할당하여 반복
    result1.append(num*3)  # 각 요소에 3을 곱한 값을 result1에 추가

print("result1 :", result1)  # result1 출력 ([3, 6, 9, 12])

print("-"*20)  # 구분선 출력
# 리스트 컴프리헨션: 2부터 9까지의 각 수(x)와 1부터 9까지의 각 수(y)를 곱한 결과들의 리스트 생성
result2 = [x*y for x in range(2,10) for y in range(1,10)]
print("result2 :", result2)  # result2 출력 (구구단 2단부터 9단까지의 모든 곱셈 결과)

# %% code 30.
a = 1         # a 변수에 1을 할당
while a < 5:  # a가 5보다 작은 동안 반복
    a = a * 2  # a를 2배로 증가시킴
    print (a)  # 현재 a 값을 출력

print("-"*20)       # 구분선 출력
treeHit = 0         # 나무를 찍은 횟수를 저장하는 변수를 0으로 초기화
while treeHit < 3:  # 나무를 3번 찍을 때까지 반복
    treeHit = treeHit + 1              # 나무를 찍은 횟수를 1 증가
    print("나무를 %d번 찍었습니다." % treeHit)  # 나무를 찍은 횟수를 출력
    if treeHit == 3:                   # 나무를 3번 찍었다면
        print("나무 넘어갑니다.")  # "나무 넘어갑니다." 메시지 출력

# %% code 31.
coffee = 3    # 커피 재고량을 3개로 초기화
money = 30    # 돈을 30으로 초기화 (0이 아닌 값이므로 True로 평가됨)
while money:  # money가 0이 아닌 동안 반복 (0은 False, 그 외는 True로 평가)
    print("돈을 받았으니 커피를 줍니다.")            # 커피 판매 메시지 출력
    coffee = coffee - 1                  # 커피 재고량을 1개 감소
    print("남은 커피의 양은 %d개입니다." % coffee)  # 남은 커피 개수를 출력
    if coffee == 0:                      # 커피가 모두 떨어졌다면
        print("커피가 다 떨어졌습니다. 판매를 중지합니다.")  # 판매 중지 메시지 출력
        break                              # while 루프를 강제로 종료
print("-"*20)  # 구분선 출력
a = 0          # 변수 a를 0으로 초기화
while a < 10:  # a가 10보다 작은 동안 반복
    a = a + 1                # a를 1씩 증가
    if a % 2 == 0: continue  # a가 짝수이면 다음 반복으로 건너뛰기 (홀수만 출력)
    print(a)                 # 홀수인 a 값을 출력
print("-"*20)  # 구분선 출력
# 이 셀을 실행하면 무한히 반복되므로 주의
while True:  # 무한 루프 (True는 항상 참이므로 계속 반복)
    print("Ctrl+C를 눌러야 while문을 빠져나갈 수 있습니다.")  # 무한 반복 메시지 출력

# %% code 32.
def square(n):  # 제곱수를 계산하는 함수 정의
    return n * n  # 입력받은 수를 제곱하여 반환
print("square(3) :", square(3))  # square 함수를 호출하여 3의 제곱을 계산하고 출력

def powers(n):  # 제곱과 세제곱을 동시에 계산하는 함수 정의
    return n**2, n**3  # 제곱과 세제곱을 튜플 형태로 반환
print("powers(3) :", powers(3))  # powers 함수를 호출하여 3의 제곱과 세제곱을 계산하고 출력

def greet(name):  # 인사말을 생성하는 함수 정의
    """이름을 받아서 인사말을 반환하는 함수"""  # 함수 설명 문서 (docstring)
    return f"안녕하세요, {name}님!"   # f-string을 사용하여 이름을 포함한 인사말 반환

print(greet("홍길동"))  # greet 함수를 호출하여 "홍길동"에 대한 인사말 출력

def calculate_area(width, height):  # 직사각형의 넓이를 계산하는 함수 정의 (매개변수: 가로, 세로)
    """직사각형의 넓이를 계산하는 함수"""  # 함수 설명 문서
    area = width * height    # 가로 × 세로로 넓이 계산
    return area              # 계산된 넓이 반환
print("넓이:", calculate_area(5, 10))  # 가로 5, 세로 10인 직사각형의 넓이 계산 및 출력

# 원의 넓이를 계산하는 함수 정의 (위의 calculate_area 함수를 덮어씀)
def calculate_area(radius):  # radius는 매개변수 (반지름 값을 저장하는 변수)
    return 3.14159 * radius ** 2  # 원의 넓이 공식: π × r² (원주율 근삿값 3.14159 사용, math.pi로 대체 가능)

# 함수 호출 및 결과 출력
print("원의 넓이:", calculate_area(5))  # 5는 인수 (함수에 전달하는 반지름 값)

# %% code 33.
def add(a, b):  # a, b는 매개변수 (함수에 전달된 값을 저장하는 변수)
    return a+b  # 두 수를 더한 결과를 반환
print("add(3, 4):", add(3, 4))  # 3, 4는 인수 (함수에 전달하는 값) - 결과: 7

def fibonacci(seed, n):  # 피보나치 수열을 생성하는 함수
    while len(seed) < n:  # seed 리스트의 길이가 n보다 작은 동안 반복
        seed.append(seed[-1] + seed[-2])  # 마지막 두 원소의 합을 리스트 끝에 추가

# Note: no return statement  # 주의: return 문이 없음 (리스트를 직접 수정하므로)
seed = [1, 1]          # 피보나치 수열의 시작값 [1, 1]
fibonacci(seed, 10)    # 10개의 피보나치 수열을 생성
print("seed :", seed)  # seed 리스트 출력

# %% code 34.
# import math
# def sinc(x):
#     return math.sin(x) / x
# print("sinc(0) :", sinc(0))  # 주의: x가 0일 때는 정의되지 않으므로, 실제로는 1로 처리하는 것이 일반적입니다.)

# %% code 35.
import math  # 수학 함수들을 사용하기 위해 math 모듈을 임포트

def sinc(x):  # sinc 함수를 정의 (sinc(x) = sin(x)/x)
    """
    sinc 함수를 계산하는 함수
    sinc(x) = sin(x)/x (x ≠ 0일 때)
    sinc(0) = 1 (x = 0일 때, 극한값)
    """
    try:  # 예외 처리를 위한 try 블록 시작
        result = math.sin(x) / x  # sin(x)를 x로 나누어 sinc 값을 계산
    except ZeroDivisionError:  # x가 0일 때 발생하는 0으로 나누기 에러를 처리
        result = 1  # x=0일 때 sinc(0)의 극한값인 1을 할당
    return result  # 계산된 sinc 값을 반환

print("sinc(0) :", sinc(0))        # x=0일 때 sinc 함수 호출 (예외 처리로 1을 반환)
print("sinc(0.20) :", sinc(0.20))  # x=0.2일 때 sinc 함수 호출 및 결과 출력
