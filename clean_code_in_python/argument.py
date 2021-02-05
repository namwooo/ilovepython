from mlops_utils import get_workspace


def my_func(arg):
    print(f'id of arg before calculation: {id(arg)}')
    arg += " in function"
    print(f'id of arg after calculation: {id(arg)}')
    print(arg)


def my_func2(a, b, c):
    print(a)
    print(b)
    print(c)


if __name__ == '__main__':
    get_workspace()
    test_str = 'test'
    print(f'id of test_str: {id(test_str)}')
    my_func(test_str)
    test_list = list('test')
    my_func(test_list)
    print(test_list)

    my_func2(1, 2, 3)
