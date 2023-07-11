import datetime
from string import Template
from pgsql import pg


from text.language.main import Text_main
from text.function.function import TextFunc

func = TextFunc()
Txt = Text_main()


class FormClient:
    # main text
    def __init__(self, data: dict, question=None):
        self.__language_driver = None
        self.__data = data
        self.__Text_lang = Txt.language[self.__data.get('lang')]
        self.__question = question
        self.__text = None

    async def main_text(self):
        question_text1 = ''
        question_text2 = ''
        if self.__data.get("from_town") is not None:
            from_town = self.__data.get("from_town_value")
            if self.__data.get("to_town") is not None:
                to_town = self.__data.get("to_town_value")
                to_subspot = "..."
                if self.__data.get("to_district") is not None:
                    to_subspot = f'{self.__data.get("to_district_value")}, ...'
                    if self.__data.get("to_subspot") is not None:
                        to_subspot = f'{self.__data.get("to_district_value")}, {self.__data.get("to_subspot_value")}'
                elif self.__data.get("to_subspot", None) is not None and self.__data.get("to_district") is None:
                    to_subspot = self.__data.get("to_subspot_value")
                question_text2 = f'🅱️ <b>{self.__Text_lang.chain.passenger.to_place}</b>: {to_town}, {to_subspot}\n'
            question_text1 = f'🅰️ <b>{self.__Text_lang.chain.passenger.from_place}</b>: {from_town}\n'

        question_text = f"{question_text1}" \
                        f"{question_text2}" \
                        f"\n{self.__question}"
        return question_text

    # car text
    async def car_text(self):
        text = Template("$pick- <b>$count</b> $auto\n\n"
                        "$choose_auto")
        text = text.substitute(pick=self.__Text_lang.chain.passenger.car_find1, count=self.__data.get('count'),
                               auto=self.__Text_lang.chain.passenger.car_find2,
                               choose_auto=self.__Text_lang.questions.passenger.auto)
        return text

    # model text
    async def model_text(self):
        car_text = Template("<b>$model</b>: $car\n\n"
                            "$choose_one")
        car_text = car_text.substitute(model=self.__Text_lang.chain.passenger.car, car=self.__data.get('car_value'),
                                       choose_one=self.__Text_lang.questions.passenger.car)
        return car_text

    # order text passenger
    async def order_passenger(self):
        await self._unpack_for_passenger()
        text = Template("🤵‍♂ <b>$name</b>: $driver_name ⭐️$rate\n"
                        "🚙 <b>$car</b>: $driver_car\n\n"

                        "🅰️ <b>$from_place</b>: $from_town, $distance — <b>$metr</b>\n"
                        "🅱️ <b>$to_place</b>: $to_town, $to_subspot\n\n"

                        "⏰ $time <b>$driver_time</b>\n"
                        "💵 $cost $places $passenger — <b>$final_cost</b> $sum")
        text = text.substitute(name=self.__Text_lang.chain.passenger.driver, driver_name=self.__name, rate=self.__rate,
                               car=self.__Text_lang.chain.passenger.car, driver_car=self.__car,
                               from_place=self.__Text_lang.chain.passenger.from_place,
                               from_town=self.__from_town, distance=self.__Text_lang.chain.passenger.distance,
                               metr=self.__distance, to_place=self.__Text_lang.chain.passenger.to_place,
                               to_town=self.__to_town, to_subspot=self.__to_subspot,
                               time=self.__Text_lang.chain.passenger.time, driver_time=self.__time,
                               cost=self.__Text_lang.chain.passenger.cost, places=self.__places,
                               passenger=self.__Text_lang.chain.passenger.passenger, final_cost=self.__cost,
                               sum=self.__Text_lang.symbol.sum)
        return text

    async def _unpack_for_passenger(self):
        await self._unpack_order()
        self.__Text_lang = Txt.language[self.__data.get('lang')]
        self.__price = await func.int_to_str(num=self.__price)
        self.__cost = await func.int_to_str(num=self.__cost)
        self.__phone_client = self.__data.get("phone_client")
        self.__from_town = self.__data.get("from_town_value")
        self.__to_town = self.__data.get("to_town_value")
        self.__places = Txt.places.places_dict[self.__data.get("places")]

        await self._driver_parameters()
        location_driver = await pg.driver_location(order_driver_id=self.__data.get('order_driver_id'))
        self.__distance = await func.distance(location_client=self.__data.get('location'),
                                              location_driver=location_driver)
        await self._spot()

    async def _unpack_order(self):
        self.__driver_id, date_time, places_driver, self.__price = \
            await pg.select_order(order_driver_id=self.__data.get("order_driver_id"))
        self.__cost = self.__price * self.__data.get('places')
        self.__date_time = datetime.datetime.strftime(date_time, "%Y-%m-%d %H:%M:%S")
        self.__time = datetime.datetime.strftime(date_time, "%H:%M")

    async def _driver_parameters(self):
        self.__name, phone_driver, self.__car, color, number, self.__rate = \
            await pg.select_parametrs_driver(driver_id=self.__driver_id)
        self.__car = self.__Text_lang.car.car[self.__car]

    async def _spot(self):
        if self.__data.get('to_district') is not None:
            self.__to_subspot = f'{self.__data.get("to_district_value")}, {self.__data.get("to_subspot_value")}'
        else:
            self.__to_subspot = self.__data.get("to_subspot_value")

    # order text driver
    async def order_driver(self, language):
        self.__language_driver = language
        await self._unpack_for_driver()
        text = Template("$new_order\n\n"
                         "🅰️ <b>$from_place</b>: $from_town, $spot\n"
                         "🅱️ <b>$to_place</b>:  $to_town, $to_subspot\n"
                         "💺 <b>$place</b>: $place_client\n\n"
                         "⏰ $time <b>$time_trip</b>\n"
                         "💵 $cost $place_client $passenger — <b>$final_cost</b> $sum\n\n"
                         "$order\n"
                         "⚠️<i>$order_cost</i>")
        text = text.substitute(new_order=self.__Text_lang_driver.order.driver.new_order,
                               from_place=self.__Text_lang_driver.chain.passenger.from_place,
                               from_town=self.__from_town, spot=self.__Text_lang.chain.driver.spot,
                               to_place=self.__Text_lang_driver.chain.passenger.to_place,
                               to_town=self.__to_town, to_subspot=self.__to_subspot,
                               time=self.__Text_lang_driver.chain.passenger.time, time_trip=self.__time,
                               place=self.__Text_lang_driver.chain.passenger.num, place_client=self.__places,
                               cost=self.__Text_lang.chain.passenger.cost, final_cost=self.__cost,
                               passenger=self.__Text_lang.chain.passenger.passenger,
                               order=self.__Text_lang_driver.order.driver.order, order_cost=self.__text,
                               sum=self.__Text_lang_driver.symbol.sum)
        return text

    async def _unpack_for_driver(self):
        self.__Text_lang_driver = Txt.language[self.__language_driver]
        self.__from_town = self.__data.get("from_town")
        self.__to_town = self.__data.get("to_town")
        self.__to_subspot = self.__data.get("to_subspot")
        self.__time = self.__data.get('time')
        self.__price = await func.int_to_str(num=self.__data.get('price'))
        self.__cost = await func.int_to_str(num=self.__data.get('cost'))
        self.__places = Txt.places.places_dict[self.__data.get("places")]
        await self._unpack_spots()
        await self._order_cost()

    async def _unpack_spots(self):
        self.__from_town = await pg.id_to_town(sub_id=self.__from_town, language=self.__language_driver)
        self.__to_town = await pg.id_to_town(sub_id=self.__to_town, language=self.__language_driver)
        await self._spot2()

    async def _spot2(self):
        if self.__data.get('to_district') is not None:
            self.__to_district = await pg.id_to_district(sub_id=self.__data.get("to_district"),
                                                         language=self.__language_driver)
            self.__to_subspot = await pg.id_to_sub_spot(sub_id=self.__to_subspot, language=self.__language_driver)
            self.__to_subspot = f'{self.__to_district}, {self.__to_subspot}'
        else:
            self.__to_subspot = await pg.id_to_sub_spot(sub_id=self.__to_subspot, language=self.__language_driver)

    async def _order_cost(self):
        tax = await func.percent_price(price=self.__data.get("price"))
        self.__tax = await func.int_to_str(num=(self.__data.get("places") * tax))
        text = Template("$text1 <b>$price</b> $text2")
        self.__text = text.substitute(text1=self.__Text_lang_driver.order.driver.order_cost1, price=self.__tax,
                                      text2=self.__Text_lang_driver.order.driver.order_cost2)

