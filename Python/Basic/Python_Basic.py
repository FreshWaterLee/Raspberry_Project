# 출력 print
print('test')

''' 주석 처리 ''''''
1234
5678
'''
## 반복문 작성 (For 문)
## i는 in 뒤에 있는 변수 혹은 range의 데이터는 순차적으로 꺼냄
for i in range(2):
    print(i)

## 데이터 입력 받기 input()
##문자열로 데이터를 받는다 (정수를 입력을 해도)
age = input('나이를 입력:')
print(age)
##그러므로 원하는 데이터 타입으로 변환할려면 데이터타입(input())
age = int(input('나이를 입력:'))
print(age+5)

## 파이썬에서 변수 선언시 데이터타입을 입력안해도 된다(알아서 변환을 함)
name = '홍길동'
print(type(name))

