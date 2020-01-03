from contextlib import contextmanager


class Resource:
    # def __enter__(self):
    #     print("connect to resource")
    #     return self
    #
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     if exc_tb:
    #         print("process exception")
    #     else:
    #         print("no exception")
    #     print("close connection")

    def query(self):
        print("query data")


@contextmanager
def make_resource():
    """
    结合原来不是上下文管理器的类定义上下文管理器
    """
    print("connect to resource")
    yield Resource()
    print("close connection")


with make_resource() as r:
    r.query()


@contextmanager
def book_mark():
    print("<<", end="")
    yield
    print(">>", end="")


with book_mark():
    print("fluent python", end="")
