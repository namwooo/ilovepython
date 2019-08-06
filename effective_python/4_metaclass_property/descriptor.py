# 31. 재사용 가능한 @property 메소드에는 디스크립터를 사용하자.
'''
@property는 같은 클래스에 속한 여러 속성에 재사용하지 못한다는 단점이 있다. 예를 들어, 학생들의 시험성적을 매긴다고 해보자.
시험은 여러 과목으로 구성되어 있고 과목별 점수가 있다.
'''
# class Exam:
# def __init__(self):
# self._writing_grade = 0
# self._math_grade = 0
# @staticmethod
# def _check_grade(value):
# if not (0 <= value <= 100):
# raise ValueError('Grade must be between 0 and 100')

# @property
# def writing_grade(self):
# return self._writing_grade
# @writing_grade.setter
# def writing_grade(self, value):
# self._check_grade(value)
# self._writing_grade = value

# @property
# def math_grade(self):
# return self._math_grade
# @math_grade.setter
# def math_grade(self, value):
# self._check_grade(value)
# self._math_grade = value
'''
각 속성에 @property와 _check_grade를 반복적으로 작성해야 하기 때문에 코드가 금방 장황해진다. 파이썬에서 이런 작업을 할 때 더 좋은 방법은 디스크립터를 사용하는 것이다.
디스크립터 클래스는 반복 코드 없이도 성적 검증을 재사용할 수 있게 해주는 __get__과 __set__메소드르 제공한다. 이런 목적으로는 믹스인보다 디스크립터가 좋은 방법이다.
디스크립터를 이용하면 한 클래스의 서로 다른 많은 속성에 같은 로직을 재사용할 수 있기 때문이다.
'''

# class Grade:
# def __init__(self):
# self._value = 0

# def __get__(self, instance, instance_type):
# """
# 이 예제에서 instance는 Exam을 객체이고, instance_type은 Exam 클래스이다.
# """
# return self._value

# def __set__(self, instance, value):
# if not (0 <= value <= 100):
# raise ValueError('Grade must be between 0 and 100')
# self._value = value

# def __delete__(self, instance):
# pass

# class Exam:
# # 클래스 속성
# math_grade = Grade()
# writing_grade = Grade()
# science_grade = Grade()

'''
저자는 디스크립터에 대한 정의를 약하게 가져갔다. 일반적으로 디스크립터란 행위를 바인딩하는 객체 속성으로 사용된다. 속성 접근이 디스크립터 프로토콜 메소드에 의해 오버라이드된다.
__get__(), __set__() and __delete__() 메소드가 정의된 객체는 디스크립터로 취급된다.
'''

'''
다시 예제로 돌아와서 프로퍼티를 할당하고, 그 프로퍼티에 접근해보자.
'''

# exam = Exam()
# exam.writing_grade = 40
# print('exam의 writing 점수:', exam.writing_grade)

'''
불행히도 위의 코드는 잘못 구현되어 제대로 동작하지 않는다. 문제는 한 Grade 인스턴스가 모든 Exam 인스턴스의 클래스 속성에 공유된다는 점이다.
이 속성에 대응하는 Grade 인스턴스는 프로그램에서 Exam 인스턴스를 생성할 때마다 생성되는게 아니라 Exam클래스가 처음 정의할 때 한번만 생성된다.
'''

# exam2 = Exam()
# exam2.writing_grade = 100
# print('exam2의 writing 점수:', exam2.writing_grade)
# print('exam의 writing 점수:', exam.writing_grade)

'''
이 문제를 해결하기위해 각 Exam 인스턴스별로 값을 추적하는 Grade 클래스를 만들어보자.
여기서는 딕셔너리에 각 인스턴스의 상태를 저장하는 방법으로 값을 추적한다.
'''

# class Grade:
# def __init__(self):
# self._values = {}
# def __get__(self, instance, instance_type):
# if instance is None: return self
# return self._values.get(instance, 0)

# def __set__(self, instance, value):
# if not (0 <= value <= 100):
# raise ValueError('Grade must be between 0 and 100')
# self._values[instance] = value

# class Exam:
# # 클래스 속성
# math_grade = Grade()
# writing_grade = Grade()
# science_grade = Grade()

# exam1 = Exam()
# exam1.math_grade = 90
# print('exam1의 수학 점수:', exam1.math_grade)

# exam2 = Exam()
# exam2.math_grade = 100
# print('exam2의 수학 점수:', exam2.math_grade)

# print(Exam.math_grade._values)

'''
위 코드는 메모리 누수 문제가 있다. _values 딕셔너리는 프로그램의 수명 동안 __set__에 전달된 모든 Exam 인스턴스의 참조를 저장한다.
결국 Exam 인스턴스의 참조 개수가 0이 되지 않아 가비지 컬렉터가 정리하지 못한다.
파이썬의 내장 모듈 weakref를 사용하면 이 문제를 해결할 수 있다. 이 모듈은 _values에 사용한 간단한 딕셔너리를 대체할 수 있는 WeakKeyDictionary라는
특별한 클래스를 제공한다. WeakKeyDictionary 클래스 고유의 동작은 런타임에 마지막으로 남은 Exam 인스턴스의 참조를 갖고 있다는 사실을 알면
키 집합에서 Exam 인스턴스를 제거하는 것이다.
'''

# import weakref

# class Grade:
# def __init__(self):
# self._values = weakref.WeakKeyDictionary()

# ...

'''
Exam 인스턴스의 __dict__에 해당 grade를 삽입하는 방법을 사용하는 사람도 있다. Grade 클래스를 사용한다는 것은
점수에 대한 정보를 Grade 객체가 담고 있다는 의미를 내포한다. 점수라는 프러퍼티는 Grade가 가지는 것이 의미상 더 낫다.
'''

# class Grade:
# def __get__(self, instance, owner):
# return instance.__dict__.get(self.name, 0)

# def __set__(self, instance, value):
# if not (0 <= value <= 100):
# raise ValueError('Grade must be between 0 and 100')
# instance.__dict__[self.name] = value

# def __set_name__(self, owner, name):
# self.name = name

# class Exam:
# writing_grade = Grade()
# math_grade = Grade()

# def __init__(self):
# self.name = 'test'

# exam1 = Exam()
# exam2 = Exam()
# exam1.writing_grade = 100
# exam2.writing_grade = 90
# exam1.math_grade = 50
# print(exam1.writing_grade)
# print(exam2.writing_grade)
# print(exam1.__dict__)
# print(exam2.__dict__)
# print(Exam.__dict__['math_grade'].__dict__)





'''
참조자료
https://docs.python.org/3/howto/descriptor.html
'''
