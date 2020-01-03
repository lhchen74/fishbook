# from app.view_models.book import BookViewModel


# class MyGifts:
#     def __init__(self, gifts_of_mine, wish_count):
#         self.gifts = []
#
#         self.__gifts_of_mine = gifts_of_mine
#         self.__wish_count = wish_count
#
#         self.gifts = self.__parse()
#
#     def __parse(self):
#         temp_gifts = []
#         for gift in self.__gifts_of_mine:
#             my_gift = self.__matching(gift)
#             temp_gifts.append(my_gift)
#         return temp_gifts
#
#     def __matching(self, gift):
#         count = 0
#         for wish in self.__wish_count:
#             if wish['isbn'] == gift.isbn:
#                 count = wish['count']
#         r = {
#             'id': gift.id,
#             'book': BookViewModel(gift.book),
#             'wishes_count': count
#         }
#         return r

