import datetime


class A:
    create_time = None

    def __init__(self):
        self.create_time = datetime.datetime.now()
        print('__init__ A')


class B(A):
    pass
    # def __init__(self):
    #     super().__init__()
    #     print('__init__ B')


b = B()
# 没有实现自己的 __init__, 会调用父类的 __init__
print(b.create_time)

