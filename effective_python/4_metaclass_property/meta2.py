# 34. Register Class Existence with Metaclasses

'''
Metaclasses can be used to automatically register types in program.
Registration is useful for doing reverse lookups, where you need to map a simple identifier back to a corresponding class.

For example, say you want to implement your own serialized representation of a Python object using JSON.
You need a way to take an object and turn it into a JSON string. 
Here, I do this generically by defining a base class that records the constructor parameters and turns them into a JSON dictionary.
'''

import json 

class Serializable:
    def __init__(self, *args):
        self.args = args
    
    def serialize(self):
        return json.dumps({'args': self.args})

class Point(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f'Point({self.x}, {self.y})'

p = Point(1, 2)
print('object', p)
print('serialized', p.serialize())
print(type(p.serialize()))

'''
Define a class that can deserialize the data from its Serializable parent class.
'''

class Deserialize(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        print(cls) # cls는 classemthod를 호출하는 class 객체가 바인딩된다.
        params = json.loads(json_data)
        return cls(*params['args'])

class BetterPoint(Deserialize):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f'Point({self.x}, {self.y})'

bp = BetterPoint(1, 2)
print('bp object', bp)
data = bp.serialize()
print('bp serialized', data)
print('bp deserialized', bp.deserialize(data))
    
    