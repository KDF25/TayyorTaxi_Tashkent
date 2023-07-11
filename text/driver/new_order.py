
from string import Template
from pgsql import pg

from text.function.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class FormNewOrderDriver:
    def __init__(self, data: dict, language: str):
        self.__data = data
        self.__language = language

    async def new_order_driver(self):
        self.__language = self.__data.get("lang")
        await self._unpack()
        text = Template("$accept_order\n\n"
                        "🔻 <b>$client_info</b> 🔻\n\n"
                        "📱 <b>$phone</b>: +$phone_client\n"
                        "🅰️ <b>$from_place</b>: $from_town, $spot\n"
                        "🅱️ <b>$to_place</b>:  $to_town, $to_subspot\n"
                        "💺 <b>$place</b>: $place_client\n\n"
                        "⏰ $time <b>$time_trip</b>\n" 
                        "💵 $cost $place_client $passenger — <b>$final_cost</b> $sum\n\n"
                        "⚠️$active_orders")
        text = text.substitute(accept_order=self.__Text_lang.order.driver.accept,
                               client_info=self.__Text_lang.order.driver.info,
                               phone=self.__Text_lang.chain.passenger.phone, phone_client=self.__phone_client,
                               from_place=self.__Text_lang.chain.passenger.from_place,
                               from_town=self.__from_town, spot=self.__Text_lang.chain.driver.spot,
                               to_place=self.__Text_lang.chain.passenger.to_place,
                               to_town=self.__to_town, to_subspot=self.__to_subspot,
                               time=self.__Text_lang.chain.passenger.time, time_trip=self.__time,
                               place=self.__Text_lang.chain.passenger.num, place_client=self.__places,
                               cost=self.__Text_lang.chain.driver.cost, final_cost=self.__cost,
                               passenger=self.__Text_lang.chain.passenger.passenger,  sum=self.__Text_lang.symbol.sum,
                               active_orders=self.__Text_lang.order.active_orders)
        return text

    async def new_order_client(self):
        self.__language = self.__data.get("lang_client")
        await self._unpack()
        text = Template("$accept\n\n"
                        "⏰ $time <b>$time_trip</b>\n\n"
                        "🤵 <b>$name</b>: $driver_name ⭐️$rate\n"
                        "📱 <b>$phone</b>: +$driver_phone\n"
                        "🚙 <b>$car</b>: $driver_car\n\n"
                        "🔻 <b>$client_info</b> 🔻\n\n"
                        "📱 <b>$phone</b>: +$client_phone\n"
                        "🅰️ <b>$from_place</b>: $from_town\n"
                        "🅱️ <b>$to_place</b>:  $to_town, $to_subspot\n\n"                       
                        "💵 $cost $place_client $passenger — <b>$final_cost</b> $sum\n\n"
                        "⚠️$active_orders")
        text = text.substitute(accept=self.__Text_lang.order.client.accept,
                               time=self.__Text_lang.chain.passenger.time, time_trip=self.__time,
                               name=self.__Text_lang.chain.passenger.driver, driver_name=self.__name, rate=self.__rate,
                               car=self.__Text_lang.chain.passenger.car, driver_car=self.__car,
                               client_info=self.__Text_lang.chain.passenger.info,
                               phone=self.__Text_lang.chain.passenger.phone,
                               client_phone=self.__phone_client, driver_phone=self.__phone_driver,
                               from_place=self.__Text_lang.chain.passenger.from_place,
                               from_town=self.__from_town,
                               to_place=self.__Text_lang.chain.passenger.to_place,
                               to_town=self.__to_town, to_subspot=self.__to_subspot, place_client=self.__places,
                               cost=self.__Text_lang.chain.passenger.cost, sum=self.__Text_lang.symbol.sum,
                               passenger=self.__Text_lang.chain.passenger.passenger, final_cost=self.__cost,
                               active_orders=self.__Text_lang.order.active_orders)
        return text

    async def on_spot(self):
        await self._unpack()
        text = Template('$common\n\n'
                        '⏰ $time <b>$time_trip</b>\n\n'
                        '$on_spot\n'
                        '<b>$from_town</b>')
        text = text.substitute(common=self.__Text_lang.on_spot.common,
                               time=self.__Text_lang.on_spot.time, time_trip=self.__time,
                               on_spot=self.__Text_lang.on_spot.on_spot,
                               from_town=self.__from_town)
        return text

    async def _unpack(self):
        self.__Text_lang = Txt.language[self.__language]
        self.__phone_driver = self.__data.get("phone_driver")
        self.__phone_client = self.__data.get("phone_client")
        self.__name = self.__data.get("name")
        self.__car = self.__data.get("car_value")
        self.__rate = self.__data.get('rate')
        self.__from_town = self.__data.get("from_town")
        self.__to_town = self.__data.get("to_town")
        self.__to_subspot = self.__data.get("to_subspot")
        self.__time = self.__data.get("time")
        self.__places = Txt.places.places_dict[self.__data.get("places")]
        self.__price = await func.int_to_str(num=self.__data.get('price'))
        self.__cost = await func.int_to_str(num=self.__data.get("cost"))
        await self._unpack_spots()

    async def _unpack_spots(self):
        self.__from_town = await pg.id_to_town(sub_id=self.__from_town, language=self.__language)
        self.__to_town = await pg.id_to_town(sub_id=self.__to_town, language=self.__language)
        self.__to_subspot = await pg.id_to_sub_spot(sub_id=self.__to_subspot, language=self.__language)



