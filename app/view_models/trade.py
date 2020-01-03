from app.view_models.book import BookViewModel


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        if single.create_time:
            time = single.create_date_time.strftime('%Y-%m-%d')
        else:
            time = 0
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )


class MyTrades:
    """
    相当于 MyGifts 和 MyWishes 的基类，由于 MyGifts 和 MyWishes 基本相同
    所以直接使用基类代替 MyGifts 和 MyWishes
    """
    def __init__(self, trades_of_mine, count_list):
        self.trades = []

        self.__trades_of_mine = trades_of_mine
        self.__count_list = count_list

        self.trades = self.__parse()

    def __parse(self):
        temp_trades = []
        for trade in self.__trades_of_mine:
            my_trade = self.__matching(trade)
            temp_trades.append(my_trade)
        return temp_trades

    def __matching(self, trade):
        count = 0
        for per in self.__count_list:
            if per['isbn'] == trade.isbn:
                count = per['count']
        r = {
            'id': trade.id,
            'book': BookViewModel(trade.book),
            'count': count
        }
        return r
