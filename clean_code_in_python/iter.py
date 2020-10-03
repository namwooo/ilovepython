class BaseTokenizer:
    def __init__(self, token):
        self.token = token

    def __iter__(self):
        yield from self.token.split("-")


if __name__ == '__main__':
    tk = BaseTokenizer("28a2320b-fd3f-4627-9792-a2b38e3c46b0")
    print(tk)
    print(list(tk))
    for i in tk:
        print(i)
