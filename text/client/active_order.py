import datetime
from string import Template
from pgsql import pg

from text.function.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class FormActiveOrderClient:

    # active order view
    def __init__(self, order_accept_id: int, language: str):
        self.__language = language
        self.__Text_lang = Txt.language[self.__language]
        self.__order_accept_id = order_accept_id

    async def order_view(self):
        await self._unpack()
        await self._unpack_driver()
        text = Template("🤵‍♂ <b>$driver</b>: $driver_name ⭐️$rate\n"
                        "🚙 $color $car  —  <b>$number</b>\n"
                        "📱 <b>$phone</b>: +$driver_phone\n\n"
                        "🔻 <b>$client_info</b> 🔻\n\n"
                        "📱 <b>$phone</b>: +$client_phone\n"
                        "🅰️ <b>$from_place</b>: $from_town\n"
                        "🅱️ <b>$to_place</b>:  $to_town, $to_subspot\n\n"
                        "⏰ $time <b>$time_trip</b>\n\n"
                        "💵 $cost $places $passenger — <b>$final_cost</b> $sum")
        text = text.substitute(driver=self.__Text_lang.chain.passenger.driver, driver_name=self.__name, rate=self.__rate,
                               color=self.__color, car=self.__car, number=self.__number,
                               phone=self.__Text_lang.chain.passenger.phone,
                               driver_phone=self.__phone_driver, client_phone=self.__phone_client,
                               client_info=self.__Text_lang.order.client.info,
                               from_place=self.__Text_lang.chain.passenger.from_place, from_town=self.__from_town,
                               to_place=self.__Text_lang.chain.passenger.to_place, to_town=self.__to_town,
                               to_subspot=self.__to_subspot,
                               time=self.__Text_lang.chain.passenger.time, time_trip=self.__time,
                               cost=self.__Text_lang.chain.passenger.cost,  places=self.__places,
                               passenger=self.__Text_lang.chain.passenger.passenger,
                               final_cost=self.__cost, sum=self.__Text_lang.symbol.sum)
        return text

    async def order_cancel(self):
        await self._unpack()
        text = Template("$order\n\n"
                        "🔻 <b>$client_info</b> 🔻\n\n"
                        "🅰️ <b>$from_place</b>: $from_town, $spot\n"
                        "🅱️ <b>$to_place</b>:  $to_town, $to_subspot\n"
                        "💺 <b>$places</b>: $client_places\n\n"
                        "⏰ $time <b>$time_trip</b>\n\n"
                        "💵 $cost $client_places $passenger — <b>$final_cost</b> $sum\n\n"
                        "$cancel")
        text = text.substitute(order=self.__Text_lang.cancel.driver.passenger,
                               client_info=self.__Text_lang.order.driver.info,
                               from_place=self.__Text_lang.chain.passenger.from_place,
                               from_town=self.__from_town, spot=self.__Text_lang.chain.driver.spot,
                               to_place=self.__Text_lang.chain.passenger.to_place,
                               to_town=self.__to_town, to_subspot=self.__to_subspot,
                               places=self.__Text_lang.chain.passenger.num, client_places=self.__places,
                               time=self.__Text_lang.chain.passenger.time, time_trip=self.__time,
                               cost=self.__Text_lang.chain.passenger.cost, final_cost=self.__cost,
                               passenger=self.__Text_lang.chain.passenger.passenger, sum=self.__Text_lang.symbol.sum,
                               cancel=self.__Text_lang.cancel.client.order)
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
        await self._unpack_order()
        await self._unpack_spots()

    async def _unpack_order(self):
        order_client_id, client_id, self.__order_driver_id, self.__driver_id, self.__phone_client, \
            self.__from_town, self.__to_town, self.__to_district, self.__to_subspot,  self.__datetime_trip, self.__places, \
            self.__price, self.__cost = await pg.orderid_to_order_accepted(order_accept_id=self.__order_accept_id)
        self.__places = Txt.places.places_dict[self.__places]
        self.__time = datetime.datetime.strftime(self.__datetime_trip, "%H:%M")
        self.__price = await func.int_to_str(num=self.__price)
        self.__cost = await func.int_to_str(num=self.__cost)

    async def _unpack_spots(self):
        self.__from_town = await pg.id_to_town(sub_id=self.__from_town, language=self.__language)
        self.__to_town = await pg.id_to_town(sub_id=self.__to_town, language=self.__language)
        await self._spot()

    async def _spot(self):
        if self.__to_district is not None:
            self.__to_subspot = await pg.id_to_sub_spot(sub_id=self.__to_subspot, language=self.__language)
            self.__to_district = await pg.id_to_district(sub_id=self.__to_district, language=self.__language)
            self.__to_subspot = f'{self.__to_district}, {self.__to_subspot}'
        else:
            self.__to_subspot = await pg.id_to_sub_spot(sub_id=self.__to_subspot, language=self.__language)

    async def _unpack_driver(self):
        self.__name, self.__phone_driver, self.__car, self.__color, self.__number, self.__rate = \
            await pg.select_parametrs_driver(driver_id=self.__driver_id)
        self.__car = self.__Text_lang.car.car[self.__car]
        self.__color = self.__Text_lang.car.color[self.__color]









