import datetime
from string import Template

from pgsql import pg
from text.function.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class FormActiveOrderDriver:

    def __init__(self, order_accept_id: int, language: str):
        self.__language = language
        self.__Text_lang = Txt.language[self.__language]
        self.__order_accept_id = order_accept_id

    async def order_view(self):
        await self._unpack()
        text = Template("🔻 <b>$client_info</b> 🔻\n\n"
                        "📱 <b>$phone</b>: +$client_phone\n"
                        "🅰️ <b>$from_place</b>: $from_town, $spot\n"
                        "🅱️ <b>$to_place</b>:  $to_town, $to_subspot\n"
                        "💺 <b>$places</b>: $place_client\n\n"
                        "⏰ $time <b>$time_trip</b>\n"
                        "💵 $cost $place_client $passenger — <b>$final_cost</b> $sum")
        text = text.substitute(client_info=self.__Text_lang.order.driver.info,
                               phone=self.__Text_lang.chain.passenger.phone, client_phone=self.__phone_client,
                               from_place=self.__Text_lang.chain.passenger.from_place,
                               from_town=self.__from_town, spot=self.__Text_lang.chain.driver.spot,
                               to_place=self.__Text_lang.chain.passenger.to_place,
                               to_town=self.__to_town, to_subspot=self.__to_subspot,
                               places=self.__Text_lang.chain.passenger.num, place_client=self.__places,
                               time=self.__Text_lang.chain.passenger.time, time_trip=self.__time,
                               cost=self.__Text_lang.chain.driver.cost,  final_cost=self.__cost,
                               passenger=self.__Text_lang.chain.passenger.passenger, sum=self.__Text_lang.symbol.sum)
        return text

    async def on_spot(self):
        await self._unpack()
        text = Template('$common\n\n'
                        '⏰ $time <b>$time_trip</b>\n\n'
                        '$on_spot\n'
                        '<b>$from_town</b>')
        text = text.substitute(common=self.__Text_lang.on_spot.common, time=self.__Text_lang.on_spot.time,
                               time_trip=self.__time, on_spot=self.__Text_lang.on_spot.on_spot,
                               from_town=self.__from_town)
        return text

    async def _unpack(self):
        await self._unpack_order()
        await self._unpack_spots()

    async def _unpack_order(self):
        order_client_id, client_id, self.__order_driver_id, self.__driver_id, self.__phone_client, \
            self.__from_town, self.__to_town, self.__to_district, self.__to_subspot, \
            self.__datetime_trip,  self.__places, self.__price, self.__cost = \
            await pg.orderid_to_order_accepted(order_accept_id=self.__order_accept_id)
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