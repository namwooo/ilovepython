# 33. Validate subclasses with metaclasses

'''
Metaclasses can be used to verify that a class was defined correctly.
When I build a complex class hierachy, I want to enforce style, require overriding methods,
or have strict relationship between class attributes.
Metaclasses enable these use cases by providing a reliable way to run validation code each time a new subclass is defined.
'''

# class Meta(type):
#     def __new__(meta, name, bases, class_dict):
#         print((meta, name, bases, class_dict))
#         return type.__new__(meta, name, bases, class_dict)

# class MyClass(metaclass=Meta):
#     data = 123

#     def foo(self):
#         pass

# MyClass()

'''
I can add functionality to the Meta.__new__ method in order to validate all of the parameters of a class before it's defined.
For example, say I want to represent any type of multisided polygon.
'''

class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        if bases != (): # 추상 클래스에 대해서는 검증하지 않는다.
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)

class Polygon(metaclass=ValidatePolygon):
    sides = None

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180

print(type(Polygon))

class Triangle(Polygon):
    print('before sides')
    sides = 3
    print('after sides')
print('after class')

print(type(Triangle))

'''
The validation does not allow me to create polygon with fewer than three sides.
I consider this is one safety barrier not to create wrong class.
'''

'''
Things to Remember
Use metaclasses to ensure that subclasses are well formed at the time they are defined,
before objects of their type are constructed.

The __new__method of metaclasses is run after the class statement's entire body has been processed.
'''