import json

from flask import jsonify, request, flash, render_template
from flask_login import current_user

from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.fish_book import FishBook
# from . import web __init__.py 导入
from app.view_models.book import BookCollection, BookViewModel
# from app.web.blueprint import web
from app.view_models.trade import TradeInfo
from . import web
from app.forms.book import SearchForm


@web.route('/test')
def test():
    """"
        http://localhost:8000/test
        第一次请求输出 1 和 None
        第二次请求输出 2 和 None
        说明 request 是线程隔离对象，none_local 不是
    """
    from flask import request
    from app.libs.none_local import none_local
    print(none_local.v)
    none_local.v = 2
    print(getattr(request, 'v', None))
    setattr(request, 'v', 2)
    return ''


@web.route('/test_template')
def test_template():
    r = {
        'name': None,
        'age': 18
    }
    flash('hello, flask')
    flash('hello, python', category='error')
    flash('hello, Jinja2', category='error')
    return render_template('test.html', data=r)


# @web.route('/book/search/<q>/<page>')
@web.route('/book/search')
def search():
    """
        isbn: http://t.yushu.im/v2/book/isbn/{isbn}
        q: http://t.yushu.im/v2/book/search?q={}&start={}&count={}
        q start count isbn
        q isbn => q (不需要用户区分关键字查询和 isbn 查询, q 代表普通关键字或 isbn)
        start count => page
    """
    # q = request.args['q']
    # page = request.args['page']
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        # request.args 是不可变的字典，可以用 to_dict 转换为可变字典
        # args_dict = request.args.to_dict()
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        fish_book = FishBook()

        if isbn_or_key == 'isbn':
            fish_book.search_by_isbn(q)
            # result = FishBook.search_by_isbn(q)
            # result = BookViewModel.package_single(result, q)
        else:
            fish_book.search_by_keyword(q, page)
            # result = FishBook.search_by_keyword(q, page)
            # result = BookViewModel.package_single(result, q)

        books.fill(fish_book, q)
        # return json.dumps(result), 200, {'content-type': 'application/json'}
        # return jsonify(books)
        # python 默认不能直接序列化对象，需要传递处理函数，将具体的解释权交给函数的调用方
        # return json.dumps(books, default=lambda obj: obj.__dict__)
    else:
        flash("搜索关键字不符合要求，请重新输入")
        # return jsonify(form.errors)
    return render_template('search_result.html', books=books, form=form)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_is_wishes = False

    # 取书籍所有详情数据
    fish_book = FishBook()
    fish_book.search_by_isbn(isbn)
    # book = BookViewModel(fish_book.books[0])
    book = BookViewModel(fish_book.first)

    # 检查书籍是否在礼物清单或心愿清单中
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_is_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    # 交易模型
    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    return render_template("book_detail.html", book=book,
                           wishes=trade_wishes_model, gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts, has_in_washes=has_is_wishes)
