import datetime
import json

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from pgsql import pg
from text.language.main import Text_main
from text.function.function import TextFunc

Txt = Text_main()
func = TextFunc()


class Start:
    @staticmethod
    async def choose_language():
        markup = InlineKeyboardMarkup(row_width=3)
        b_rus = InlineKeyboardButton(text=Txt.settings.rus, callback_data='rus')
        b_ozb = InlineKeyboardButton(text=Txt.settings.uzb, callback_data='uzb')
        b_eng = InlineKeyboardButton(text=Txt.settings.eng, callback_data='eng')
        markup.row(b_ozb, b_rus, b_eng)
        return markup


class InlineClient:
    def __init__(self, language: str, sub_id=None, condition=True, data=None, order_client_id=None,
                 order_accept_id=None,
                 order_driver_id=None):
        self.__order_driver_id = order_driver_id
        self.__markup = None
        self.__language = language
        self.__Text_lang = Txt.language[language]
        self.__sub_id = sub_id
        self.__condition = condition
        self.__data = data
        self.__order_client_id = order_client_id
        self.__order_accept_id = order_accept_id
        self.__back = InlineKeyboardButton(text=self.__Text_lang.buttons.common.back, callback_data="back")

    async def menu_back(self):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(self.__back)
        return markup

    async def menu_towns(self):
        self.__markup = InlineKeyboardMarkup(row_width=2)
        # await self._main_town()
        await self._towns()
        if self.__condition is True:
            self.__markup.add(self.__back)
        return self.__markup

    async def _towns(self):
        for index, town in enumerate(await pg.id_and_town(language=self.__language)):
            b = InlineKeyboardButton(text=town[1], callback_data=f"town_{town[0]}")
            if index == 0 or index == 1:
                self.__markup.add(b)
            else:
                self.__markup.insert(b)

    async def menu_districts(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        await self._districts()
        self.__markup.add(self.__back)
        return self.__markup

    async def _districts(self):
        for district in await pg.select_to_districts(from_town=self.__data.get('from_town'),
                                                     to_town=self.__data.get('to_town'),
                                                     places=self.__data.get('places'),
                                                     client_id=self.__data.get('client_id')):
            text = await pg.id_to_district(sub_id=district[0], language=self.__language)
            b = InlineKeyboardButton(text=f"{text} ({district[1]})", callback_data=f"district_{district[0]}")
            self.__markup.insert(b)

    async def menu_spots(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        await self._spots()
        self.__markup.add(self.__back)
        return self.__markup

    async def _spots(self):
        for spot in await pg.select_to_spots(from_town=self.__data.get('from_town'), to_town=self.__data.get('to_town'),
                                             to_district=self.__data.get('to_district'),
                                             places=self.__data.get('places'), client_id=self.__data.get('client_id')):
            text = await pg.id_to_spot(sub_id=spot[0], language=self.__language)
            b = InlineKeyboardButton(text=f"{text} ({spot[1]})", callback_data=f"spot_{spot[0]}")
            self.__markup.insert(b)

    async def menu_sub_spots(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        await self._sub_spots()
        self.__markup.add(self.__back)
        return self.__markup

    async def _sub_spots(self):
        for sub_spot in await pg.select_to_subspots(from_town=self.__data.get('from_town'),
                                                    to_town=self.__data.get('to_town'),
                                                    to_spot=self.__data.get('to_spot'),
                                                    places=self.__data.get('places'),
                                                    client_id=self.__data.get('client_id')):
            text = await pg.id_to_sub_spot(sub_id=sub_spot[0], language=self.__language)
            b = InlineKeyboardButton(text=f"{text} ({sub_spot[1]})", callback_data=f"subspot_{sub_spot[0]}")
            self.__markup.add(b)

    async def menu_places(self):
        self.__markup = InlineKeyboardMarkup(row_width=4)
        await self._places()
        self.__markup.add(self.__back)
        return self.__markup

    async def _places(self):
        for i, place in enumerate(Txt.places.places):
            b = InlineKeyboardButton(text=place, callback_data=f"places_{i + 1}")
            self.__markup.insert(b)

    async def menu_share_phone(self):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(self.__back)
        return markup

    async def menu_count_sub_spots(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        await self._count_sub_spots()
        self.__markup.add(self.__back)
        return self.__markup

    async def _count_sub_spots(self):
        for sub_spot in await pg.select_count_spots(from_spot=self.__data.get('from_spot'),
                                                    to_spot=self.__data.get('to_spot'),
                                                    places=self.__data.get('places'),
                                                    client_id=self.__data.get('client_id')):
            text = await pg.id_to_sub_spot(sub_id=sub_spot[0], language=self.__language)
            b = InlineKeyboardButton(text=f"{text} ({sub_spot[1]})", callback_data=f"newsub_{sub_spot[0]}")
            self.__markup.add(b)

    async def menu_list(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        await self._sort()
        b1 = InlineKeyboardButton(text=self.__sort_values[0], callback_data=f"sort_distance")
        b2 = InlineKeyboardButton(text=self.__sort_values[1], callback_data=f"sort_money")
        b3 = InlineKeyboardButton(text=self.__sort_values[2], callback_data=f"sort_time")
        self.__markup.row(b1, b2, b3)
        await self._list()
        self.__markup.add(self.__back)
        return self.__markup

    async def _sort(self):
        self.__sort_values = ['📍', '💵', '⏰']
        await self._lists()

    async def _list(self):
        for order_id, price, date_time, distance in self.__list:
            price = await func.int_to_str(num=price)
            # location_driver = json.loads(distance)
            # distance = await func.distance(location_driver=location_driver, location_client=self.__data['location'])
            distance = await func.distance_to_str(distance=distance)
            time = datetime.datetime.strftime(date_time, "%H:%M")
            text = f"📍 {distance} | 💵 {price} | ⏰ в {time}"
            b_order = InlineKeyboardButton(text=text, callback_data=f"order_{order_id}")
            self.__markup.insert(b_order)

    async def _lists(self):
        if self.__condition == 'sort_time' or self.__condition is True:
            self.__sort_values[2] = '✅ ⏰'
            self.__list = await pg.select_list(from_town=self.__data.get('from_town'),
                                               to_spot=self.__data.get('to_spot'),
                                               location=self.__data.get('location'),
                                               to_subspot=self.__data.get('to_subspot'),
                                               places=self.__data.get('places'),
                                               client_id=self.__data.get('client_id'))
        elif self.__condition == 'sort_money':
            self.__sort_values[1] = '✅ 💵'
            self.__list = await pg.sort_money(from_town=self.__data.get('from_town'),
                                              to_spot=self.__data.get('to_spot'),
                                              location=self.__data.get('location'),
                                              to_subspot=self.__data.get('to_subspot'),
                                              places=self.__data.get('places'),
                                              client_id=self.__data.get('client_id'))
        elif self.__condition == 'sort_distance':
            self.__sort_values[0] = '✅ 📍'
            self.__list = await pg.sort_distance(from_town=self.__data.get('from_town'),
                                                 to_spot=self.__data.get('to_spot'),
                                                 location=self.__data.get('location'),
                                                 to_subspot=self.__data.get('to_subspot'),
                                                 places=self.__data.get('places'),
                                                 client_id=self.__data.get('client_id'))

    async def menu_order(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Text_lang.buttons.passenger.location,
                                  callback_data=f"location_{self.__order_driver_id}")
        b2 = InlineKeyboardButton(text=self.__Text_lang.buttons.common.order,
                                  callback_data=f"book_{self.__order_driver_id}")
        markup.add(b1, b2, self.__back)
        return markup

    async def menu_more(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b = InlineKeyboardButton(text=self.__Text_lang.buttons.passenger.choose_more, callback_data="back")
        markup.add(b)
        return markup

    async def menu_accept_order(self):
        markup = InlineKeyboardMarkup(row_width=2)
        Driver = self.__Text_lang.buttons.driver
        b1 = InlineKeyboardButton(text=Driver.accept, callback_data=f"accept_{self.__order_client_id}")
        b2 = InlineKeyboardButton(text=Driver.reject, callback_data=f"reject_{self.__order_client_id}")
        markup.add(b1).add(b2)
        return markup

    async def menu_cancel(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Text_lang.buttons.passenger.location,
                                  callback_data=f"location_{self.__order_accept_id}")
        b2 = InlineKeyboardButton(text=self.__Text_lang.buttons.cancel.client,
                                  callback_data=f"cancel_{self.__order_accept_id}")

        markup.add(b1, b2)
        return markup

    async def menu_delete(self):
        markup = InlineKeyboardMarkup(row_width=2)
        b1 = InlineKeyboardButton(text=self.__Text_lang.buttons.common.no, callback_data=f"no_{self.__order_accept_id}")
        b2 = InlineKeyboardButton(text=self.__Text_lang.buttons.common.da,
                                  callback_data=f"yes_{self.__order_accept_id}")
        markup.add(b1, b2)
        return markup

    async def menu_on_spot(self):
        markup = InlineKeyboardMarkup(row_width=2)
        b1 = InlineKeyboardButton(text=self.__Text_lang.buttons.common.on_spot,
                                  callback_data=f"yes_{self.__order_accept_id}")
        markup.add(b1)
        return markup
