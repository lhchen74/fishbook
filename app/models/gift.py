from flask import current_app
from sqlalchemy import Integer, Column, Boolean, ForeignKey, String, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
# from app.models.wish import Wish
from app.spider.fish_book import FishBook

from collections import namedtuple

EachGiftWishCounts = namedtuple('EachGiftWishCounts', ['count', 'isbn'])


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)

    # 对象代表一个礼物，是具体的，不应该有返回最近多个礼物的方法
    # 类代表礼物这一事物，它是抽象的，不是具体的一个，类方法返回多个礼物是合理的
    # 如果某段代码具有具体的意义，应该提取到 model 中，而不是放在视图函数中
    # 执行会报 sql_mode=only_full_group_by 错误，因为 mysql 版本造成的问题
    # only_full_group_by 模式说明查询和用到的字段都必须在 group_by 中出现
    # 可以 set @@global_sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO
    # ,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'
    # 或者 set @@sql_mode = '...'  去除 only_full_group_by
    @classmethod
    def recent(cls):

        recent_gift = Gift.query\
            .filter_by(launched=False)\
            .group_by(Gift.isbn)\
            .order_by(desc(Gift.create_time))\
            .limit(current_app.config['RECENT_BOOK_COUNT'])\
            .distinct().all()
        return recent_gift

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query\
            .filter_by(uid=uid, launched=False)\
            .order_by(desc(Gift.create_time))\
            .all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        # db.session.query() 中传入需要查询的
        # filter 需要传递过滤表达式不是关键字参数
        # count_list = [(2, isbn1), (1, isbn2)]
        count_list = db.session.query(func.count(Wish.id), Wish.isbn)\
                .filter(Wish.launched == False, Wish.status == 1, Wish.isbn.in_(isbn_list))\
                .group_by(Wish.isbn).all()
        # 不应该在外部通过 w[0], w[1] 访问，而应该转为字典或者对象（命名元组）
        # count_list = [EachGiftWishCounts(w[0], w(1)) for w in count_list]
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    @property
    def book(self):
        """
        根据 isbn 查询图书数据
        :return:
        """
        fish_book = FishBook()
        fish_book.search_by_isbn(self.isbn)
        return fish_book.first
