import datetime
from string import Template

from pgsql import pg
from text.language.main import Text_main

Txt = Text_main()


class FormOnSpotDriver:

    def __init__(self, order_driver_id: int, language: str, client_id=None):
        self.__language = language
        self.__Text_lang = Txt.language[self.__language]
        self.__order_driver_id = order_driver_id
        self.__client_id = client_id

    async def on_spot_view(self):
        await self._unpack_order()
        await self._unpack_spots(language=self.__language)
        text = Template("$on_spot\n\n"
                        "<b>$from_town</b>\n\n"
                        "⏰ $time <b>$time_trip</b>")
        text = text.substitute(on_spot=self.__Text_lang.on_spot.on_spot,
                               from_town=self.__from_town,
                               time=self.__Text_lang.on_spot.time, time_trip=self.__time_trip)
        return text

    async def on_spot_inform_driver(self):
        await self._unpack_phone_clients()
        text = Template("$inform\n\n"
                        "🔻 $info 🔻\n\n"
                        "$phone_client")
        text = text.substitute(inform=self.__Text_lang.on_spot.inform_client, info=self.__Text_lang.on_spot.info,
                               phone_client=self.__phone_client)
        return text

    async def on_spot_inform_client(self):
        await self._unpack_order()
        await self._unpack_client()
        await self._unpack_car()
        await self._unpack_spots(language=self.__language_client)
        text = Template("$inform\n\n"
                        "<b>$from_town</b>\n\n"
                        "🚙 <b>$color $car  —  $number</b>\n"
                        "📱 <b>$phone</b>: +$phone_driver")
        text = text.substitute(inform=self.__Text_lang_client.on_spot.driver,
                               from_town=self.__from_town,
                               phone=self.__Text_lang_client.on_spot.phone, phone_driver=self.__phone_driver,
                               color=self.__color, car=self.__car, number=self.__number)
        return text

    async def _unpack_order(self):
        self.__phone_driver, self.__driver_id, self.__from_town, datetime_trip = \
            await pg.orderid_to_order_driver(order_driver_id=self.__order_driver_id)
        self.__time_trip = datetime.datetime.strftime(datetime_trip, "%H:%M")

    async def _unpack_spots(self, language: str):
        self.__from_town = await pg.id_to_town(sub_id=self.__from_town, language=language)

    async def _unpack_phone_clients(self):
        index = 1
        for client in await pg.orderid_to_clients(order_driver_id=self.__order_driver_id):
            self.__phone_client = f"{self.__Text_lang.on_spot.passenger} <b>№{index}:</b> +{client[0]}\n"
            index += index

    async def _unpack_client(self):
        self.__language_client = await pg.select_language(user_id=self.__client_id)
        self.__Text_lang_client = Txt.language[self.__language_client]

    async def _unpack_car(self):
        name, phone_driver, self.__car, self.__color, self.__number, self.__rate =  \
            await pg.select_parametrs_driver(driver_id=self.__driver_id)
        self.__car = self.__Text_lang_client.car.car[self.__car]
        self.__color = self.__Text_lang_client.car.color[self.__color]


