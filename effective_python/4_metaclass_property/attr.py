# 32. 지연 속성에는 __getattr__, __getattribute__, __setattr__을 사용하자.

'''
파이썬의 언어 후크를 이용하면 시스템들을 연계하는 범용 코드를 쉽게 만들수 있다.
예를 들어 데이터베이스의 로우를 파이썬 객체로 표현한다고 하자. 데이터베이스의 로우 형태, 필드를 알아야만 이에 대응하는 객체를 만들 수 있을 것 같다.
하지만 파이썬에서는 객체와 데이터베이스를 연결하는 코드에서 로우의 스키마를 몰라도 된다. 코드를 범용으로 만들면 된다.

사용하기에 앞서 정의부터 해야 하는 일반 인스턴스 속성, @property 메서드, 디스크립터로는 이렇게 할 수 없다.
파이썬은 __getattr__이라는 특별한 메소드로 이런 동적 동작을 가능하게 한다.
클래스에 __getattr__ 메소드를 정의하면 객체으 인스턴스 딕셔너리에서 속성을 찾을 수 없을 때마다 이 메소드가 호출된다.
'''

class LazyDB(object):
    def __init__(self):
        self.exists = 5
    def __getattr__(self, name):
        value = f'Value for {name}'
        setattr(self, name, value)
        return value

data = LazyDB()
print('Before:', data.__dict__)
print('foo:', data.foo)
print('after:', data.__dict__)

'''
__getattr__이 실제로 호출되는 시점을 보여주려고 LazyDB에 로깅을 추가한다.
무한 반복을 피하려고 super().__getattr__()로 실제 프로퍼티 값을 얻어오는 부분을 눈여겨보자.
'''
