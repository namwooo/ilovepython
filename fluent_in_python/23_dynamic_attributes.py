import inspect
import json
from collections import abc

JSON_PATH = './osconfeed.json'


class Record:
    __index = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f'<{cls_name} serial={self.serial!r}>'

    @staticmethod
    def fetch(key):
        if Record.__index is None:
            Record.__index = load()
        return Record.__index[key]


class Event(Record):

    def __repr__(self):
        if hasattr(self, 'name'):
            cls_name = self.__class__.__name__
            return f'<{cls_name} {self.name!r}>'
        else:
            return super().__repr__()

    @property
    def venue(self):
        key = f'venue.{self.venue_serial}'
        return self.__class__.fetch(key)

    @property
    def speakers(self):
        spkr_serials = self.__dict__['speakers']
        fetch = self.__class__.fetch
        return [fetch(f'speaker.{key}') for key in spkr_serials]


def load(path=JSON_PATH):
    records = {}
    with open(path) as fp:
        raw_data = json.load(fp)
    for collection, raw_records in raw_data['Schedule'].items():
        record_type = collection[:-1]
        cls_name = record_type.capitalize()
        cls = globals().get(cls_name, Record)
        if inspect.isclass(cls) and issubclass(cls, Record):
            factory = cls
        else:
            factory = Record
        for raw_record in raw_records:
            key = f'{record_type}.{raw_record["serial"]}'
            records[key] = factory(**raw_record)

    return records


class LineItem:

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    def get_weight(self):
        return self.__weight

    def set_weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')

    weight = property(get_weight, set_weight)


class Class:
    data = 'the class data attr'

    @property
    def prop(self):
        return 'the prop value'

    def __getattribute__(self, item):
        return self.__dict__[item]


class FrozenJSON:
    """A read-only fasade for navigating a JSON-like object using attribute notation"""

    def __init__(self, mapping):
        self.__data = dict(mapping)

    def __getattr__(self, name):
        try:
            return getattr(self.__data, name)
        except AttributeError:
            return FrozenJSON.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


def test():
    a = 1
    print(locals())
    print(globals())


# feed = FrozenJSON({"Schedule":
#                        {"conferences": [{"serial": 115}],
#                         "events": [
#                             {"serial": 34505,
#                              "name": "Why Schools Don´t Use Open Source to Teach Programming",
#                              "event_type": "40-minute conference session",
#                              "time_start": "2014-07-23 11:30:00",
#                              "time_stop": "2014-07-23 12:10:00",
#                              "venue_serial": 1462,
#                              "description": "Aside from the fact that high school programming...",
#                              "website_url": "http://oscon.com/oscon2014/public/schedule/detail/34505",
#                              "speakers": [157509],
#                              "categories": ["Education"]}
#                         ],
#                         "speakers": [
#                             {"serial": 157509,
#                              "name": "Robert Lefkowitz",
#                              "photo": None,
#                              "url": "http://sharewave.com/",
#                              "position": "CTO",
#                              "affiliation": "Sharewave",
#                              "twitter": "sharewaveteam",
#                              "bio": "Robert ´r0ml´ Lefkowitz is the CTO at Sharewave, a startup..."}
#                         ],
#                         "venues": [
#                             {"serial": 1462,
#                              "name": "F151",
#                              "category": "Conference Venues"}
#                         ]
#                         }
#                    })
# print(feed.Schedule.events)

import abc


class Validated(abc.ABC):

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __set__(self, instance, value):
        value = self.validate(self.storage_name, value)
        instance.__dict__[self.storage_name] = value

    @abc.abstractmethod
    def validate(self, name, value):
        """return """


v = FrozenJSON({'a': 1})


def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]


def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]


def display(obj):
    cls = type(obj)
    if cls is type:
        return '<class {}>'.format(obj.__name__)
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return '<{} object>'.format(cls_name(obj))


def print_args(name, *args):
    pseudo_args = ', '.join(display(x) for x in args)
    print('-> {}.__{}__({})'.format(cls_name(args[0]), name, pseudo_args))


class Overriding:
    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:
    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NonOverriding:
    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Managed:
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    def spam(self):
        print('-> Managed.spam({})'.format(display(self)))

    @property
    def test(self):
        return 1




