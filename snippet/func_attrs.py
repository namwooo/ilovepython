# # __closure__
# def foo():
#     def bar():
#         print(spam)
#     spam = 'ham'
#     bar()
#     return bar

# b = foo()
# print(b.__closure__[0].cell_contents)

# __annotations__
# def func1(a: int, b: str):
#     pass
# print(func1.__annotations__)

# __kwdefaults__
# def func2(*args, a=1, b=2):
#     pass
# print(func2.__kwdefaults__)

# __self__ and __func__
class MyClass:
    def foo(self):
        print('called foo')
    
    @classmethod
    def bar(cls):
        print(cls)
        print('called bar')

# print(MyClass().foo.__self__) 
# print(MyClass().foo.__func__) 
# print(MyClass.bar.__self__)
# print(MyClass.bar.__func__)
# MyClass.bar()
# MyClass().bar()

# c = MyClass()
# # assign instance method object to local variable.
# f = c.foo
# f()

print(MyClass.foo) # function object
print(MyClass().foo) # bound method object
print(MyClass.bar) # bound method object
print(MyClass().bar) # bound method object

def func():
    print('called func')

c = MyClass()
c.func = func # attributes of a class instance
print(c.func) # function object, unbound

MyClass.func = func # attrubute of class
print(MyClass().func) # bound method object




