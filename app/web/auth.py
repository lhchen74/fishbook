from flask import render_template, request, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.utils import redirect

from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.models.base import db
from app.models.user import User
from . import web

from app.libs.email import send_mail


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()
        redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # remember=True 默认时间是 365 天
            # 如果需要修改需要在配置文件中添加 REMEMBER_COOKIE_DURATION
            login_user(user, remember=True)
            # 访问 http://localhost:8000/my/gifts 需要登陆权限
            # 会跳转到登陆页面, 并携带 next 参数 http://localhost:8000/login?next=/my/gifts
            next_url = request.args.get('next')
            # next 为空跳转到主页
            # next 不是以 / 开头，例如 http://www.baidu.com, 跳转到 index, 防止重定向攻击
            if not next_url or not next_url.startswith('/'):
                next_url = url_for('web.index')
            return redirect(next_url)
        else:
            flash('账号不存在或密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            # 如果 user 为空后续的流程不会处理, 页面会呈现 Not_Found
            # fist_or_404 -> first -> Abort -> HttpException
            user = User.query.filter_by(email=account_email).first_or_404()
            send_mail(account_email, '重置密码', 'email/reset_password.html',
                      user=user, token=user.generate_token())
            flash('验证邮件已经发送到 {}, 请注意查收'.format(account_email))

    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        password = form.password1.data
        success = User.reset_password(password, token)
        if success:
            flash('重置密码成功，请使用新密码登陆')
            return redirect(url_for('web.login'))
        else:
            flash('重置密码失败')
    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
