
import datetime
from math import ceil
from datetime_now import dt_now

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from pgsql import pg
from text.language.main import Text_main
from text.function.function import TextFunc

Txt = Text_main()
func = TextFunc()


class InlineDriverData:
    def __init__(self, language: str):
        self.__markup = None
        self.__language = language
        self.__Text_lang = Txt.language[language]
        self.__back = InlineKeyboardButton(text=self.__Text_lang.buttons.common.back, callback_data="back")

    async def menu_cars(self):
        self.__markup = InlineKeyboardMarkup(row_width=3)
        await self._cars()
        self.__markup.add(self.__back)
        return self.__markup

    async def _cars(self):
        for index in self.__Text_lang.car.car:
            b = InlineKeyboardButton(text=self.__Text_lang.car.car[index], callback_data=f"car_{index}")
            self.__markup.insert(b)

    async def menu_color(self):
        self.__markup = InlineKeyboardMarkup(row_width=3)
        await self._color()
        self.__markup.add(self.__back)
        return self.__markup

    async def _color(self):
        for index in self.__Text_lang.car.color:
            b = InlineKeyboardButton(text=self.__Text_lang.car.color[index], callback_data=f"color_{index}")
            self.__markup.insert(b)

    async def menu_back(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        self.__markup.add(self.__back)
        return self.__markup

    async def menu_agreement(self):
        self.__markup = InlineKeyboardMarkup(row_width=2)
        b_no = InlineKeyboardButton(text=self.__Text_lang.buttons.common.no, callback_data='back')
        b_yes = InlineKeyboardButton(text=self.__Text_lang.buttons.common.yes, callback_data='agree')
        self.__markup.add(b_no, b_yes, self.__back)
        return self.__markup


class InlineDriver:
    def __init__(self, language: str, sub_id=None, condition=True, data=None, town1=None, town2=None,
                 order_client_id=None, order_accept_id=None, order_driver_id=None, district=None):
        self.__markup = None
        self.__language = language
        self.__Text_lang = Txt.language[language]
        self.__sub_id = sub_id
        self.__condition = condition
        self.__district = district
        self.__data = data
        self.__town1 = town1
        self.__town2 = town2
        self.__order_client_id = order_client_id
        self.__order_accept_id = order_accept_id
        self.__order_driver_id = order_driver_id
        self.__back = InlineKeyboardButton(text=self.__Text_lang.buttons.common.back, callback_data="back")

    async def menu_back(self):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(self.__back)
        return markup

    async def menu_towns(self):
        self.__markup = InlineKeyboardMarkup(row_width=2)
        await self._towns()
        if self.__condition is True:
            self.__markup.add(self.__back)
        return self.__markup

    async def _towns(self):
        for index, town in enumerate(await pg.id_and_town(language=self.__language)):
            if index == 0:
                b = InlineKeyboardButton(text=town[1], callback_data=f"city_{town[0]}")
                self.__markup.add(b)
            elif index == 1:
                b = InlineKeyboardButton(text=town[1], callback_data=f"town_{town[0]}")
                self.__markup.add(b)
            else:
                b = InlineKeyboardButton(text=town[1], callback_data=f"town_{town[0]}")
                self.__markup.insert(b)

    async def menu_districts(self):
        self.__markup = InlineKeyboardMarkup(row_width=2)
        await self._districts()
        self.__markup.add(self.__back)
        return self.__markup

    async def _districts(self):
        # for spot in await pg.id_and_spots(town1=str(self.__town1), town2=str(self.__town2), language=self.__language):
        for district in await pg.id_and_district(sub_id=self.__sub_id, language=self.__language):
            b = InlineKeyboardButton(text=district[1], callback_data=f"district_{district[0]}")
            self.__markup.insert(b)

    async def menu_spots_city(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        await self._spots_city()
        self.__markup.add(self.__back)
        return self.__markup

    async def _spots_city(self):
        for spot in await pg.id_and_spots_city(sub_id=self.__sub_id, language=self.__language):
            b = InlineKeyboardButton(text=spot[1], callback_data=f"spot_{spot[0]}")
            self.__markup.add(b)

    async def menu_spots(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        await self._spots()
        self.__markup.add(self.__back)
        return self.__markup

    async def _spots(self):
        for spot in await pg.id_and_spots(sub_id=self.__sub_id, language=self.__language):
            b = InlineKeyboardButton(text=spot[1], callback_data=f"spot_{spot[0]}")
            self.__markup.add(b)

    async def menu_sub_spots(self):
        self.__markup = InlineKeyboardMarkup(row_width=2)
        await self._sub_spots()
        self.__markup.add(self.__back)
        return self.__markup

    async def _sub_spots(self):
        if self.__district is None:
            for sub_spot in await pg.id_and_sub_spots(sub_id=self.__sub_id, language=self.__language):
                b = InlineKeyboardButton(text=sub_spot[1], callback_data=f"subspot_{sub_spot[0]}")
                self.__markup.add(b)
        else:
            for sub_spot in await pg.district_id_and_sub_spots(sub_id=self.__sub_id, language=self.__language):
                b = InlineKeyboardButton(text=sub_spot[1], callback_data=f"subspot_{sub_spot[0]}")
                self.__markup.add(b)

    async def menu_places(self):
        self.__markup = InlineKeyboardMarkup(row_width=4)
        await self._places()
        self.__markup.add(self.__back)
        return self.__markup

    async def _places(self):
        for i, place in enumerate(Txt.places.places):
            b_num = InlineKeyboardButton(text=place, callback_data=f"places_{i+1}")
            self.__markup.insert(b_num)

    async def menu_price(self):
        self.__markup = InlineKeyboardMarkup(row_width=3)
        await self._price()
        self.__markup.add(self.__back)
        return self.__markup

    async def _price(self):
        for price in Txt.money.driver.price:
            text = await func.int_to_str(num=price)
            b = InlineKeyboardButton(text=text, callback_data=f"price_{price}")
            self.__markup.insert(b)

    async def menu_time(self):
        self.__markup = InlineKeyboardMarkup(row_width=3)
        await self._time()
        self.__markup.add(self.__back)
        return self.__markup

    async def _time(self):
        now = dt_now.now()
        day = now.day
        year = now.year
        month = now.month
        hour = now.hour
        minute = now.minute
        for i in range(0, 24):
            minute = ceil(minute / 30) * 30
            date = datetime.datetime(day=day, month=month, year=year, hour=hour, minute=0) + \
                   datetime.timedelta(minutes=minute)
            time = datetime.datetime.strftime(date, "%H:%M")
            minute += 30
            b = InlineKeyboardButton(text=time, callback_data=f"time_{date}")
            self.__markup.insert(b)

    async def menu_book(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Text_lang.buttons.driver.location, callback_data='location')
        b2 = InlineKeyboardButton(text=self.__Text_lang.buttons.common.yes, callback_data='book')
        self.__markup.add(b1, b2, self.__back)
        return self.__markup

    async def menu_route_cancel(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Text_lang.buttons.driver.location, callback_data="location")
        b2 = InlineKeyboardButton(text=self.__Text_lang.buttons.driver.route_cancel, callback_data="cancel")
        markup.add(b1, b2)
        return markup

    async def menu_route_choose(self):
        markup = InlineKeyboardMarkup(row_width=2)
        b1 = InlineKeyboardButton(text=self.__Text_lang.buttons.common.no, callback_data="no")
        b2 = InlineKeyboardButton(text=self.__Text_lang.buttons.common.da, callback_data="yes")
        markup.add(b1, b2).add(self.__back)
        return markup

    async def menu_more(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b = InlineKeyboardButton(text=self.__Text_lang.buttons.passenger.choose_more,
                                 callback_data=f"passenger_{self.__order_client_id}")
        markup.add(b)
        return markup

    async def menu_cancel(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b = InlineKeyboardButton(text=self.__Text_lang.buttons.cancel.client,
                                 callback_data=f"cancel_{self.__order_accept_id}")
        markup.add(b)
        return markup

    async def menu_delete(self):
        markup = InlineKeyboardMarkup(row_width=2)
        b1 = InlineKeyboardButton(text=self.__Text_lang.buttons.common.no, callback_data=f"no_{self.__order_accept_id}")
        b2 = InlineKeyboardButton(text=self.__Text_lang.buttons.common.da, callback_data=f"yes")
        markup.add(b1, b2)
        return markup

    async def menu_on_spot(self):
        markup = InlineKeyboardMarkup(row_width=2)
        b1 = InlineKeyboardButton(text=self.__Text_lang.buttons.common.on_spot,
                                  callback_data=f"yes_{self.__order_driver_id}")
        markup.add(b1)
        return markup

    async def menu_cancel_driver(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b = InlineKeyboardButton(text=self.__Text_lang.buttons.cancel.client,
                                 callback_data=f"DriverCancel_{self.__order_accept_id}")
        markup.add(b)
        return markup

    async def menu_delete_driver(self):
        markup = InlineKeyboardMarkup(row_width=2)
        b1 = InlineKeyboardButton(text=self.__Text_lang.buttons.common.no,
                                  callback_data=f"DriverNo_{self.__order_accept_id}")
        b2 = InlineKeyboardButton(text=self.__Text_lang.buttons.common.da,
                                  callback_data=f"DriverYes_{self.__order_accept_id}")
        markup.add(b1, b2)
        return markup

    async def menu_cancel_client(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b = InlineKeyboardButton(text=self.__Text_lang.buttons.cancel.client,
                                 callback_data=f"ClientCancel_{self.__order_accept_id}")
        markup.add(b)
        return markup

    async def menu_delete_client(self):
        markup = InlineKeyboardMarkup(row_width=2)
        b1 = InlineKeyboardButton(text=self.__Text_lang.buttons.common.no,
                                  callback_data=f"ClientNo_{self.__order_accept_id}")
        b2 = InlineKeyboardButton(text=self.__Text_lang.buttons.common.da,
                                  callback_data=f"ClientYes_{self.__order_accept_id}")
        markup.add(b1, b2)
        return markup

    async def menu_rate(self):
        self.__markup = InlineKeyboardMarkup(row_width=1)
        await self._rate()
        return self.__markup

    async def _rate(self):
        for index in range(5, 0, -1):
            text = "⭐️" * index
            b = InlineKeyboardButton(text=text, callback_data=f"rate_{index}_{self.__order_accept_id}")
            self.__markup.add(b)

    async def menu_location_driver(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b = InlineKeyboardButton(text=self.__Text_lang.buttons.driver.location,
                                 callback_data=f"point_{self.__order_accept_id}")
        markup.add(b)
        return markup

    async def menu_location_client(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b = InlineKeyboardButton(text=self.__Text_lang.buttons.passenger.location,
                                 callback_data=f"point_{self.__order_accept_id}")
        markup.add(b)
        return markup


class InlinePersonalCabinet:
    def __init__(self, language: str, url: str = None):
        self.__markup = None
        self.__url = url
        self.__language = language
        self.__Text_lang = Txt.language[language]
        self.__back = InlineKeyboardButton(text=self.__Text_lang.buttons.common.back, callback_data="back")

    async def menu_personal_data(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Text_lang.buttons.personal_cabinet.data.name, callback_data=f"name")
        b2 = InlineKeyboardButton(text=self.__Text_lang.buttons.personal_cabinet.data.phone, callback_data=f"phone")
        b3 = InlineKeyboardButton(text=self.__Text_lang.buttons.personal_cabinet.data.car, callback_data=f"auto")
        markup.add(b1, b2, b3, self.__back)
        return markup

    async def menu_auto(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b1 = InlineKeyboardButton(text=self.__Text_lang.buttons.personal_cabinet.data.model, callback_data=f"model")
        b2 = InlineKeyboardButton(text=self.__Text_lang.buttons.personal_cabinet.data.number, callback_data=f"number")
        b3 = InlineKeyboardButton(text=self.__Text_lang.buttons.personal_cabinet.data.color, callback_data=f"colors")
        markup.add(b1, b2, b3, self.__back)
        return markup

    async def menu_model(self):
        self.__markup = InlineKeyboardMarkup(row_width=3)
        await self._car()
        self.__markup.add(self.__back)
        return self.__markup

    async def _car(self):
        for index in self.__Text_lang.car.car:
            b = InlineKeyboardButton(text=self.__Text_lang.car.car[index], callback_data=f"car_{index}")
            self.__markup.insert(b)

    async def menu_color(self):
        self.__markup = InlineKeyboardMarkup(row_width=3)
        await self._color()
        self.__markup.add(self.__back)
        return self.__markup

    async def _color(self):
        for index in self.__Text_lang.car.color:
            b = InlineKeyboardButton(text=self.__Text_lang.car.color[index], callback_data=f"color_{index}")
            self.__markup.insert(b)

    async def menu_back(self):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(self.__back)
        return markup

    async def menu_balance(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b = InlineKeyboardButton(text=self.__Text_lang.buttons.personal_cabinet.wallet.balance, callback_data="balance")
        markup.add(b, self.__back)
        return markup

    async def menu_cash(self):
        self.__markup = InlineKeyboardMarkup(row_width=2)
        await self._cash()
        self.__markup.add(self.__back)
        return self.__markup

    async def _cash(self):
        for cash in Txt.money.wallet.price:
            text = await func.int_to_str(num=cash)
            b = InlineKeyboardButton(text=text, callback_data=f"cash_{cash}")
            self.__markup.insert(b)

    async def menu_pay_way(self):
        markup = InlineKeyboardMarkup(row_width=3)
        b1 = InlineKeyboardButton(text=self.__Text_lang.buttons.personal_cabinet.wallet.payme, callback_data="Payme")
        b2 = InlineKeyboardButton(text=self.__Text_lang.buttons.personal_cabinet.wallet.click, callback_data="Click")
        b3 = InlineKeyboardButton(text=self.__Text_lang.buttons.personal_cabinet.wallet.paynet, callback_data="Paynet")
        markup.add(b1, b2, b3).add(self.__back)
        return markup

    async def menu_payment(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b = InlineKeyboardButton(text=self.__Text_lang.buttons.personal_cabinet.wallet.pay, callback_data="pay")
        markup.add(b, self.__back)
        return markup

    async def payme_url(self):
        markup = InlineKeyboardMarkup(row_width=1)
        url_button = InlineKeyboardButton(text=self.__Text_lang.buttons.personal_cabinet.wallet.pay, url=self.__url)
        markup.add(url_button, self.__back)
        return markup

    async def click_url(self):
        markup = InlineKeyboardMarkup(row_width=1)
        url_button = InlineKeyboardButton(text=self.__Text_lang.buttons.personal_cabinet.wallet.pay, url=self.__url)
        markup.add(url_button, self.__back)
        return markup

    async def menu_quiz(self):
        markup = InlineKeyboardMarkup(row_width=1)
        b = InlineKeyboardButton(text=self.__Text_lang.quiz.yes, callback_data="quizback")
        markup.add(b, self.__back)
        return markup

