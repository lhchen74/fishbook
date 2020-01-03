from contextlib import contextmanager
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer


# db = SQLAlchemy()


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


# 扩展 BaseQuery 的 filter_by, 每次查询条件带上 status = 1
# 因为 status = 0 代表软删除的数据，不需要查询出来
############################################
# 1. flask 使用的是自己扩展的 SQLAlchemy rom flask_sqlalchemy import SQLAlchemy
# 2. 在 site-packages 中查找相关 Query 对象，发现没有 filter_by 方法 class BaseQuery(orm.Query)
# 3. 向上查找 orm.Query, 可以查看到定义，所以只要扩展 BaseQuery 即可
#     ```python
#     def filter_by(self, **kwargs):
#         clauses = [
#             _entity_descriptor(self._joinpoint_zero(), key) == value
#             for key, value in kwargs.items()
#         ]
#         return self.filter(sql.and_(*clauses))
#     ```
# 4. 实例化 SqlAlchemy 时替换用自己扩展的 Query 替换原来的 BaseQuery
############################################
class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    # 表示不为 Base 创建数据库表
    __abstract__ = True
    # 不可以给 create_time 默认值，因为 create_time 是类变量
    # 在类定时执行，会导致 create_time 的值都是一样的
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        """
        软删除
        :return:
        """
        self.status = 0

    @property
    def create_date_time(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None


