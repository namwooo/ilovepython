class Grade:
    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        instance.__dict__[self.name] = value
        print(instance.__dict__)

    def __set_name__(self, owner, name):
        self.name = name

# class Grade:
#     def __init__(self):
#         self._values = {}
            
#     def __get__(self, instance, owner):
#         if instance is None: return self
#         return self._values.get(instance, 0)

#     def __set__(self, instance, value):
#         if not (0 <= value <= 100):
#             raise ValueError('Grade must be between 0 and 100')
#         self._values[instance] = value

#     def __set_name__(self, owner, name):
#         self.name = name

class Exam:
    writing_grade = Grade()
    math_grade = Grade()

    def __init__(self):
        self.name = 'test'

exam1 = Exam()
exam2 = Exam()
exam1.writing_grade = 100
exam2.writing_grade = 90
print(exam1.writing_grade)
print(exam2.writing_grade)
print(exam1.__dict__)
print(exam2.__dict__)





