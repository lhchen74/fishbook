from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message


# def send_async_mail(msg):
#     """
#     Working outside of application context.
#     :param msg:
#     :return:
#     """
#     try:
#         mail.send(msg)
#     # Working outside of application context.
#     #
#     # This typically means that you attempted to use functionality that needed
#     # to interface with the current application object in some way. To solve
#     # this, set up an application context with app.app_context().  See the
#     # documentation for more information.
#     except Exception as e:
#         pass


def send_async_mail(app, msg):
    """
    :param app: flask 核心对象
    :param msg:
    :return:
    """
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_mail(to, subject, template, **kwargs):
    # msg = Message('测试邮件', sender='2938449682@qq.com', body='Test',
    #               recipients=['2938449682@qq.com'])
    msg = Message('[鱼书]' + ' ' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    # 获取 flask 核心对象，不能直接使用 current_app 这个代理对象
    # 因为开启了一个新线程，由于线程隔离传入的 current_app 无法获取 flask 核心对象
    app = current_app._get_current_object()
    thread = Thread(target=send_async_mail, args=[app, msg])
    thread.start()
    # mail.send(msg)
