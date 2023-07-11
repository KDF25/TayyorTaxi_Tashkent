import datetime
from string import Template
from pgsql import pg
from text.language.main import Text_main

Txt = Text_main()


class FormOnSpotClient:

    # active order view
    def __init__(self, order_accept_id: int, language: str):
        self.__language = language
        self.__Text_lang = Txt.language[self.__language]
        self.__order_accept_id = order_accept_id

    async def on_spot_view(self):
        await self._unpack_order()
        await self._unpack_spots(language=self.__language)
        text = Template("$on_spot\n\n"
                        "<b>$from_town</b>\n\n"
                        "⏰ $time <b>$time_trip</b>")
        text = text.substitute(on_spot=self.__Text_lang.on_spot.on_spot, from_town=self.__from_town,
                               time=self.__Text_lang.on_spot.time, time_trip=self.__time_trip)
        return text

    async def on_spot_inform_client(self):
        await self._unpack_order()
        await self._unpack_car()
        text = Template("$inform\n\n"
                        "🚙 <b>$color $car  —  $number</b>\n"
                        "📱 <b>$phone</b>: +$phone_driver")
        text = text.substitute(inform=self.__Text_lang.on_spot.inform_driver,
                               color=self.__color, car=self.__car, number=self.__number,
                               phone=self.__Text_lang.on_spot.phone, phone_driver=self.__phone_driver,)
        return text

    async def on_spot_inform_driver(self):
        await self._unpack_order()
        await self._unpack_driver()
        await self._unpack_spots(language=self.__language_driver)
        text = Template("$inform\n\n"
                        "<b>$from_town</b>\n\n"
                        "📱 <b>$phone</b>: +$phone_client\n"
                        "💺 <b>$places</b>: $places_client")
        text = text.substitute(inform=self.__Text_lang_driver.on_spot.client,
                               from_town=self.__from_town,  phone=self.__Text_lang_driver.on_spot.phone,
                               phone_client=self.__phone_client, places=self.__Text_lang_driver.on_spot.places,
                               places_client=self.__places)
        return text

    async def _unpack_order(self):
        order_client_id, client_id, order_driver_id, self.__driver_id, self.__phone_client,  \
            self.__from_town, to_town, to_district, to_subspot,  datetime_trip, self.__places, price, cost = \
            await pg.orderid_to_order_accepted(order_accept_id=self.__order_accept_id)
        self.__time_trip = datetime.datetime.strftime(datetime_trip, "%H:%M")

    async def _unpack_spots(self, language: str):
        self.__from_town = await pg.id_to_town(sub_id=self.__from_town, language=language)

    async def _unpack_car(self):
        name, self.__phone_driver, self.__car, self.__color, self.__number, self.__rate =  \
            await pg.select_parametrs_driver(driver_id=self.__driver_id)
        self.__car = self.__Text_lang.car.car[self.__car]
        self.__color = self.__Text_lang.car.color[self.__color]

    async def _unpack_driver(self):
        self.__places = Txt.places.places_dict[self.__places]
        self.__language_driver = await pg.select_language(user_id=self.__driver_id)
        self.__Text_lang_driver = Txt.language[self.__language_driver]










