class A:
    def __call__(self):
        return object()


class B:
    def __call__(self):
        return object()


def func():
    return object()


def main(callable):
    """
    统一接口调用，不需要在函数内部判断是对象还是函数
    :param callable:
    :return: object
    """
    callable()


if __name__ == '__main__':
    main(A)
    main(B)
    main(func)
