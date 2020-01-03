from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from app.models.base import db

login_manager = LoginManager()

mail = Mail()


def create_app():
    # __name__ 指的是 app 而不是 fishbook,所以 app 才是应用程序的根目录
    app = Flask(__name__, static_folder='static')
    # app.config.from_object('config')
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    register_blueprint(app)

    # app 和登陆插件 flash-login 关联
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登陆或注册'

    mail.init_app(app)

    # app 和 sql alchemy 关联
    db.init_app(app)
    # 根据模型创建数据库表
    # db.create_all(app=app)
    with app.app_context():
        db.create_all()

    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)


