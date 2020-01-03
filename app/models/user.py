from math import floor

from flask import current_app
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as SignatureSerializer

from app import login_manager
from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.fish_book import FishBook


class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    _password = Column('password', String(128), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        fish_book = FishBook()
        fish_book.search_by_isbn(isbn)
        if not fish_book.first:
            return False
        # 不允许同一个用户同时赠送多本书
        # 一个用户不可能同时成为赠送者和索要者
        # 即既不在赠送清单也不在心愿清单才能添加
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600):
        s = SignatureSerializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(new_password, token):
        s = SignatureSerializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token.encode('utf-8'))
        except:
            # token过期或者非法
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True

    def can_send_drift(self):
        """
        1. 鱼豆数量必须大于等于1
        2. 每索取两本书自己就必须赠送一本书
        """
        if self.beans < 1:
            return False

        success_gifts_count = Gift.query.filter_by(
            uid=self.id,
            launched=True
        ).count()

        success_receive_count = Drift.query.filter_by(
            requester_id=self.id,
            pending=PendingStatus.Success
        ).count()

        if floor(success_gifts_count) >= floor(success_receive_count / 2):
            return True
        else:
            return False

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )

    @property
    def send_receive(self):
        return '{}/{}'.format(self.send_counter, self.receive_counter)

    # 如果 id 不是主键，需要定义 get_id 指明 user 的 key
    # def get_id(self):
    #     return self.id


# 用于验证用户是否登陆
@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
