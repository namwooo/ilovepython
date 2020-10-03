# 32. 지연 속성에는 __getattr__, __getattribute__, __setattr__을 사용하자.

'''
파이썬의 언어 후크를 이용하면 시스템들을 연계하는 범용 코드를 쉽게 만들수 있다.
예를 들어 데이터베이스의 로우를 파이썬 객체로 표현한다고 하자. 데이터베이스의 로우 형태, 필드를 알아야만 이에 대응하는 객체를 만들 수 있을 것 같다.
하지만 파이썬에서는 객체와 데이터베이스를 연결하는 코드에서 로우의 스키마를 몰라도 된다. 코드를 범용으로 만들면 된다.

사용하기에 앞서 정의부터 해야 하는 일반 인스턴스 속성, @property 메서드, 디스크립터로는 이렇게 할 수 없다.
파이썬은 __getattr__이라는 특별한 메소드로 이런 동적 동작을 가능하게 한다.
클래스에 __getattr__ 메소드를 정의하면 객체으 인스턴스 딕셔너리에서 속성을 찾을 수 없을 때마다 이 메소드가 호출된다.
'''

# class LazyDB:
#     def __init__(self):
#         self.exists = 5

#     def __getattr__(self, name):
#         value = f'Value for {name}'
#         setattr(self, name, value)
#         return value

# data = LazyDB()
# print('Before:', data.__dict__)
# print('foo:', data.foo)
# print('after:', data.__dict__)

'''
__getattr__이 실제로 호출되는 시점을 보여주려고 LazyDB에 로깅을 추가한다.
무한 반복을 피하려고 super().__getattr__()로 실제 프로퍼티 값을 얻어오는 부분을 눈여겨보자.
'''

# class LoggingLazyDB(LazyDB):
#     def __getattr__(self, name):
#         print(f'Called __getattr__{name}')
#         return super().__getattr__(name)

# data = LoggingLazyDB()
# print('exists:', data.exists)
# print('foo:', data.foo)
# print('foo:', data.foo)

'''
exists 속성은 인스턴스 딕셔너리에 있으므로 __getattr__이 절대 호출되지 않는다.
foo속성은 원래는 인스턴스 딕셔너리에 없으므로 처음에는 __getattr__이 호출된다. 
하지만 foo에 대응하는 __getattr__호출은 setattr을 호출하며, setattr은 인스턴스 딕셔너리에 foo를 저장한다.
두 번째로 접근할 때는 __getattr__이 호출되지 않는다.
이런 동작은 스키마리스 데이터에 지연 접근하는 경우에 특히 도움이 된다. __getattr__이 프로퍼티 로딩이라는 어려운 작업을
한번만 실행하면 다음 접근부터는 기존 결과를 가져온다.
'''

'''
데이터베이스 시스템에서 트랜잭션도 원한다고 하자. 사용자가 속성에 접근할 때는 대응하는 데이터베이스의 로우가 여전히 유효한지,
트렌젝션이 여전히 열려 있는지 알고 싶다고 해보자. __getattr__후크는 인스턴스 딕셔너리를 사용하여 빠르게 속성에 접근할 수 있다. 그러나, 객체의 인스턴스 딕셔너리에 없는 속성에 접근하려고 할때만 호출 되므로
모든 로우 접근에 필요한 로직에는 알맞지 않다. 파이썬에는 이런 쓰임새를 고려한 __getattribute__라는 또 다른 후크가 있다. 이 특별한 메소드는 객체의 속성에 접근할 때마다 호출되며, 심지어 해당 속성이
속성 딕셔너리에 있을 때도 호출된다. 이런 동작 덕분에 속성에 접근할 때마다 전역 트랜잭션 상태를 확인하는 작업 등에 쓸 수 있다. 여기서는 __getattribute__가 호출될 때마다 로그를 남기려고 ValidatingDB를 정의한다.
'''

# class ValidatingDB:
#     def __init__(self):
#         self.exists = 5

#     def __getattribute__(self, name): # name of attribute
#         print(f'Called __getattribute__{name}')
#         try:
#             return super().__getattribute__(name)
#         except AttributeError:
#             value = f'Value for {name}'
#             setattr(self, name, value)
#             return value

# data = ValidatingDB()
# print('exists:', data.exists)
# print('foo:', data.foo)
# print('foo:', data.foo)

'''
In the event that a dynamically accessed property shouldn't exist, you can raise an AttributeError
to cause Python's standard missing property behavior for both __getattr__ and __getattribute__.
'''

# class MissingPropertyDB:
#     def __getattr__(self, name):
#         if name == 'bad_name':
#             raise AttributeError(f'{name} is missing')

# data = MissingPropertyDB()
# data.bad_name

'''
Now, I want to lazily push data to the database when values are assigned to your Python object.
You can do this with __setattr__, a language hook that intercept arbitrary attribute assignments.
Unlike __getattr__ and __getattribute___, there's no need for two separate methods.
The __setattr__ method is always called every time an attribute is assigned on an instance.
'''


class LoggingSavingDB:
    def __setattr__(self, name, value):
        print(f'called __setattr__{name}: {value}')
        super().__setattr__(name, value)


data = LoggingSavingDB()
data.row = 1
data.row = 2

'''
The problem with __getattribute__ and __setattr__ is that they're called on every attribute access for an object,
even when I may not want that to happen. For example, I access attribute on object to look up keys in an associated dictionary.
self._data actually calls __getattribtue__ method recursively until it reaches its stack limit.
'''


class BrokenDictionaryDB:
    def __init__(self, data):
        self._data = {}

    def __getattribute__(self, name):
        return self._data[name]


'''
The solution is to use the super().__getattribute__ method on your instance to fetch values
from the instance attribute dictionary. It avoids the recursion.
'''


class DictionaryDB:
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):  # object 부모 클래스의 __getattribute__를 오버라이딩한다.
        data_dict = super().__getattribute__('_data')
        # 속성을 직접 접근하지 않고, super()를 써서 object 부모 클래스 __getattribute__를 호출한다.
        return data_dict[name]

    def __setattr__(self, name, value):
        super().__setattr__(name, value)


db = DictionaryDB({'data': 1})
print(db.data)
