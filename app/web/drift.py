from flask import flash, url_for, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import or_, desc
from werkzeug.utils import redirect

from app.forms.book import DriftForm
from app.libs.email import send_mail
from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.view_models.book import BookViewModel
from app.view_models.drift import DriftCollection
from . import web


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书是你自己的，不能向自己索要书籍')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    if not current_user.can_send_drift():
        return render_template('not_enough_beans.html', beans=current_user.beans)

    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)
        send_mail(current_gift.user.email, '有人想要一本书', 'email/get_gift.html',
                  wisher=current_user, gift=current_gift)
        return redirect(url_for('web.pending'))

    # 礼物赠送者的简要信息
    gifter = current_gift.user.summary
    return render_template('drift.html', gifter=gifter,
                           user_beans=current_user.beans, form=form)


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query\
        .filter(or_(Drift.requester_id == current_user.id,
                    Drift.gifter_id == current_user.id))\
        .order_by(desc(Drift.create_time)).all()

    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    with db.auto_commit():
        drift = Drift.query\
            .filter(Gift.uid == current_user.id, Drift.id == did)\
            .first_or_404()
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(current_user.id)
        requester.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    # 超权问题, uid:1 登陆后可以通过修改 url 中的 did 访问其他人的 drift
    # 添加条件 requestor_id=current_user.id，限制只能访问自己的 drift
    # uid:1, did:1
    # uid:1, did:2
    with db.auto_commit():
        drift = Drift.query\
            .filter_by(id=did, requester_id=current_user.id)\
            .first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    with db.auto_commit():
        # 修改 pending 状态为 Success
        drift = Drift.query\
            .filter_by(gifter_id=current_user.id, id=did)\
            .first_or_404()
        drift.pending = PendingStatus.Success

        # 赠送成功后鱼豆增加
        current_user.beans += 1

        # 赠送成功修改礼物状态为赠送成功
        gift = Gift.query\
            .filter_by(id=drift.gift_id)\
            .first_or_404()
        gift.launched = True

        # 赠送成功说明心愿已经达成，修改心愿状态
        # 直接 update
        Wish.query.filter_by(
            isbn=drift.isbn,
            uid=drift.requester_id,
            launched=False
        ).update({Wish.launched: True})

    return redirect(url_for('web.pending'))


def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        # 将 drift_form 的值拷贝到 drift
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_id = current_gift.user.id
        drift.gifter_nickname = current_gift.user.nickname

        book = BookViewModel(current_gift.book)

        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        current_user.beans -= 1

        db.session.add(drift)



