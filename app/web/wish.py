from flask import current_app, flash, url_for, render_template
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from app.libs.email import send_mail
from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import MyTrades
from . import web

__author__ = '七月'


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbn_list = [gift.isbn for gift in wishes_of_mine]
    wish_count_list = Wish.get_gift_counts(isbn_list)
    my_wishes_view_model = MyTrades(wishes_of_mine, wish_count_list)
    return render_template('my_wish.html', wishes=my_wishes_view_model.trades)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            # current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(wish)
    else:
        flash('这本书已经在赠送清单或心愿清单，请不要重复添加')
        # book_detail -> save_to_gifts -> book_detail
        # 这里 book_detail会重新渲染，可以考虑 使用 Ajax 和静态文件缓存
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    """
    向需要此书的人发送一个邮件，如果这个人接受就会发起一个鱼漂 (drift)
    """
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.\
        filter_by(uid=current_user.id, isbn=wish.isbn).\
        first()
    if not gift:
        flash('你还没有上传此书，'
              '请点击"加入到赠送清单"添加此书。添加前请确认你拥有此书')
    else:
        send_mail(wish.user.email, '有人想送你一本书',
                  'email/satisfy_wish.html', wish=wish, gift=gift)
        flash('已向她/他发送邮件，如果她/他愿意接受你的赠送，你将收到一个鱼漂')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    wish = Wish.query\
        .filter_by(isbn=isbn, launched=False)\
        .first_or_404()

    with db.auto_commit():
        wish.delete()

    return redirect(url_for('web.my_wish'))
