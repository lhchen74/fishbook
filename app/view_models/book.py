class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.pages = book['pages'] or ''
        self.author = '、'.join(book['author'])
        self.summary = book['summary'] or ''
        self.image = book['image']
        self.price = book['price']
        self.isbn = book['isbn']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property
    def intro(self):
        # 保留 filter 为 True 的元素
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return ' / '.join(intros)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, fish_book, keyword):
        self.total = fish_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in fish_book.books]


class _BookViewModel:
    """
    类的作用：
    1. 描述特征（类变量，实例变量）
    2. 行为（方法）
    如果一个类中大量方法都可以标记为类方法或实例方法，
    这个类的封装很大可能并不是面
    """
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_book_data(data) for data in data['books']]
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'author': '、'.join(data['author']),
            'summary': data['summary'] or '',
            'image': data['image']
        }
        return book
