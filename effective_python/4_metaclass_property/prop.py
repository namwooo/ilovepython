# 29. 게터와 세터 대신 일반 속성을 이용하자.

'''
속성을 설정할 때 특별한 동작이 일어나야 하면 @property 데코레이터와 
이에 대응하는 setter 속성을 사용한다. 세터와 게터 메소드의 이름이 의도한 프로퍼티 이름과 일치해야 한다.
'''

class Resistor:
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = voltage
        self.current = current

class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self.ohms
    
    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, 'ohms'):
            raise AttributeError("Can't set attribute")
        if ohms <= 0:
            raise ValueError('value for ohms must be greater than 0')
        self.ohms = ohms
    
'''
위와 같이 속성을 불변으로 만들거나, 할당 받을 값을 체크하는 용도로 세터를 사용할 수 있다.
발생하는 예외들은 FixedResistance.__init__이 Resistor.__init__ 메소드를 호출 하기 때문에 일어난다.
self.ohms 할당문에서 @ohms.setter 메소드가 호출되어 객체 생성이 완료되기 전에 검증 코드가 실행된다.
'''

'''
@property의 단점은 속성에 대응하는 메소드를 서브클래스에서만 공유할 수 있다는 점이다.
서로 관련 없는 클래스는 같은 구현을 공유하지 못한다.
'''

'''
최소한의 정책으로 게터에서 다른 속성을 설정하는 로직을 넣지 않아야한다. 
또한, 모듈을 동적으로 임포트하거나, 느린 헬퍼 함수를 실행하거나, 비용이 많이 드는 쿼리를 수행하지 말아야한다.
이는 최소 놀람 원칙에 어긋난다. 더 복잡하고 느린 작업은 일반 메소들 구현하자.
'''