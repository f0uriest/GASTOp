def bar(x, y):
    print(x+y)


class foo():
    def __init__(self, x):
        self.x = x

    def bar(self, y=None):
        if not y:
            y = self.x
        print(y)
