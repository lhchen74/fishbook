from flask import Flask, current_app

app = Flask(__name__)

# _request_ctx_stack = LocalStack()
# _app_ctx_stack = LocalStack()
# current_app = LocalProxy(_find_app)
# request = LocalProxy(partial(_lookup_req_object, 'request'))
# session = LocalProxy(partial(_lookup_req_object, 'session'))
# g = LocalProxy(partial(_lookup_app_object, 'g'))

# 当客户端发起一个请求时，flask 会先检查 _app_ctx_stack = LocalStack() 这个栈是否为空，
# 如果为空会将 flask 核心对象 app = Flask(__name__) 推入栈顶
# 然后将 Request 请求对象推入 _request_ctx_stack = LocalStack() 栈顶
#
# current_app = LocalProxy(_find_app)，current_app 引用栈顶元素的 app，即 flask 核心对象
# def _find_app():
#     top = _app_ctx_stack.top
#     if top is None:
#         raise RuntimeError(_app_ctx_err_msg)
#     return top.app
#
# request = LocalProxy(partial(_lookup_req_object, 'request')) request 引用的是 Request 对象
# 对于非请求的单元测试，离线应用如果要使用 flask 核心对象，需要手动入栈
# ctx = app.app_context()
# ctx.push()
# a = current_app
# d = current_app.config['DEBUG']
# ctx.pop()

# app.app_context() 上下文表达式必须返回一个上下文管理器
# 上下文管理器是指实现了上下文协议的对象 __enter__ __exit__
with app.app_context():
    a = current_app
    d = current_app.config['DEBUG']


class Resource:
    def __enter__(self):
        print("connect to resource")
        return self

    # exc_type 异常类型: <class 'ZeroDivisionError'>
    # exc_val 异常的值: division by zero
    # exc_tb 异常堆栈: <traceback object at 0x10e205388>

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print("process exception")
        else:
            print("no exception")
        print("close connection")
        # 如果 with 出现异常，会直接进入 __exit__
        # __exit__ 如果返回 True, 不会在向外面抛出异常
        # __exit__ 如果返回 False, 会继续向外部抛出异常
        # __exit__ 如果什么都不返回，默认返回 None, 代表 False

    def query(self):
        print("query data")


# with 语句 as 后面的变量指的是上下文管理器 __enter__ 方法返回的值
try:
    with Resource() as resource:
        1 / 0
        resource.query()
except Exception as e:
    print(e)

