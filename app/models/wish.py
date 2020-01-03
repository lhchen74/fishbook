from sqlalchemy import Integer, Column, Boolean, ForeignKey, String, SmallInteger, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
# from app.models.gift import Gift
from app.spider.fish_book import FishBook


class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query \
            .filter_by(uid=uid, launched=False) \
            .order_by(desc(Wish.create_time)) \
            .all()
        return wishes

    @classmethod
    def get_gift_counts(cls, isbn_list):
        from app.models.gift import Gift
        # db.session.query() 中传入需要查询的
        # filter 需要传递过滤表达式不是关键字参数
        # count_list = [(2, isbn1), (1, isbn2)]
        count_list = db.session.query(func.count(Gift.id), Gift.isbn) \
            .filter(Gift.launched == False, Gift.status == 1, Gift.isbn.in_(isbn_list)) \
            .group_by(Gift.isbn).all()
        # 不应该在外部通过 w[0], w[1] 访问，而应该转为字典或者对象（命名元组）
        # count_list = [EachGiftWishCounts(w[0], w(1)) for w in count_list]
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        """
        根据 isbn 查询图书数据
        :return:
        """
        fish_book = FishBook()
        fish_book.search_by_isbn(self.isbn)
        return fish_book.first
