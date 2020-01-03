### api

isbn查询: <http://t.yushu.im/v2/book/isbn/{isbn}>

关键字查询: <http://t.yushu.im/v2/book/search?q={}&start={}&count={}>

### Thread

进程分配内存资源等
线程利用 cpu 执行代码，线程本身不保存资源，但是可以访问进程资源
GIL python 解释器只允许同一时刻存在单个 cpu, 单个线程执行代码

### LocalStack

Flask 使用线程隔离的意义在于：使当前线程能够正确引用到他自己所创建的对象，
而不是引用到其他线程所创建的对象

### Flask

线程 ID 作为 key 的字典 -> Local -> LocalStack
AppContext RequestContext -> LocalStack
Flask -> AppContext   Request -> RequestContext
current_app -> (LocalStack.top = AppContext top.app = Flask)
request -> (LocalStack.top = RequestContext top.request = Request)

### ViewModel

ViewModel 作用：裁剪，修饰，合并
如果是单页应用，author 建议直接返回，因为客户端 javascript 处理更加灵活，可以很方便替换分隔符
如果是 web, 可以在服务端处理，然后模版渲染比较方便
      
### 类

描述特征（类变量，实例变量）
行为（方法）
如果一个类中大量方法都可以标记为类方法或实例方法，这个类的封装很大可能并不是面向对象，或者说封装的不成功
 
### 单页面多页面

单页面的数据填充是在客户端（javascript Ajax 请求 Api 数据填充）
多页面数据是在服务端渲染

### contextmanager

1. 扩展类，结合原来不是上下文管理器的类定义上下文管理器

```python
from contextlib import contextmanager

class Resource:
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
```

2. 在程序开头和结尾添加特定部分

```python
from contextlib import contextmanager

@contextmanager
def book_mark():
    print("<<", end="")
    yield
    print(">>", end="")


with book_mark():
    print("fluent python", end="")
    
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy    
class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
```
### MVC

业务逻辑应该写在 Model 层, 所谓 Model 并不是数据层（封装不同数据源，在 ORM 中不需要关注数据层）
如果某段代码具有具体的意义，应该提取到 model 中，而不是放在视图函数（Controller) 中

### only_full_group

only_full_group_by 模式说明查询和用到的字段都必须在 group_by 中出现, 可以修改 mysql 设置允许 select 字段不在 group by 中
select @@global.sql_mode
'ONLY_FULL_GROUP_BY, STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
可以 set @@global.sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'
和 set @@sql_mode = '...'  去除 only_full_group_by

set @@global.sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'
set @@sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'


### 循环导入

执行第三步的时候，因为在第一步已经导入，所以不会再重复导入一次 app.models.gift
但是在执行第一步的时候导入并没有执行到 (2), 所以 import Gift 会报 can not import Gift

book.py
from app.models.gift import Gift  1
from app.models.wish import Wish

gift.py
from app.models.wish import Wish  2
class Gift(Base):                (2)
    pass
    
wish.py
from app.models.gift import Gift (3)
class Wish(Base):
    pass
    
    
### callable 对象

1. 简化方法调用
2. 统一调用接口
