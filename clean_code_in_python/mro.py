class Base1:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Base1:{self.name}"


class Base2:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Base1:{self.name}"


class Extend(Base1, Base2):
    """Extend Base1 & Base2"""


if __name__ == '__main__':
    print(str(Extend('test')))
    print([cls.__name__ for cls in Extend.mro()])
