'''
Whenever a class inherits from another class, __init_subclass__ is called on that class. This way, it is possible to write classes which change the behavior of subclasses. This is closely related to class decorators, but where class decorators only affect the specific class they’re applied to, __init_subclass__ solely applies to future subclasses of the class defining the method.

classmethod object.__init_subclass__(cls)
This method is called whenever the containing class is subclassed. cls is then the new subclass. If defined as a normal instance method, this method id implicitly converted to a class method. Keyword arguments which are given to a new class are passed to the parent’s class __init_subclass__. 
https://docs.python.org/3/reference/datamodel.html
'''

class Philosopher:
    def __init_subclass__(cls, name, age, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.name = name
        cls.age = age

class KoreanPhilosopher(Philosopher, name='namwoo', age=30):
    pass

print(Philosopher.__dict__)
print(KoreanPhilosopher.__dict__)

'''
The default implementation object.__init_subclass__ does nothing, 
but raises an error if it is called with any arguments.
'''