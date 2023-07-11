import datetime
from string import Template
from pgsql import pg


from text.language.main import Text_main
from text.function.function import TextFunc

Txt = Text_main()
func = TextFunc()


class FormDriver:
    # main text
    def __init__(self, data: dict, question=None):
        self.__data = data
        self.__Text_lang = Txt.language[self.__data.get('lang')]
        self.__question = question
        self.__text = None

    async def main_text(self):
        question_text1 = ''
        question_text2 = ''
        if self.__data.get("from_town_value") is not None:
            from_town = self.__data.get("from_town_value")
            if self.__data.get("to_town_value") is not None:
                to_town = self.__data.get("to_town_value")
                to_subspot = "..."
                if self.__data.get("to_district_value") is not None:
                    to_subspot = f'{self.__data.get("to_district_value")}, ...'
                    if self.__data.get("to_subspot_value") is not None:
                        to_subspot = f'{self.__data.get("to_district_value")}, {self.__data.get("to_subspot_value")}'
                elif self.__data.get("to_subspot_value", None) is not None and self.__data.get("to_district_value") is None:
                    to_subspot = self.__data.get("to_subspot_value")
                question_text2 = f'🅱️ <b>{self.__Text_lang.chain.passenger.to_place}</b>: {to_town}, {to_subspot}\n'
            question_text1 = f'🅰️ <b>{self.__Text_lang.chain.passenger.from_place}</b>: {from_town} ,{self.__Text_lang.chain.driver.spot}\n'
        question_text = f"{question_text1}" \
                        f"{question_text2}" \
                        f"\n{self.__question}"
        return question_text

    async def order(self):
        await self._unpack_order()
        text = Template("🤵 <b>$name</b>: $driver_name ⭐️$rate\n"
                        "📱 <b>$phone</b>: +$phone_driver\n"
                        "🚙 <b>$car</b>: $color $driver_car — <b>$number</b>\n\n"
                        "🅰️ <b>$from_place</b>: $from_town, $spot\n"
                        "🅱️ <b>$to_place</b>: $to_town, $to_sub_spot\n"
                        "💺 <b>$place</b>: $driver_place\n\n"
                        "⏰ $time <b>$driver_time</b>\n"
                        "💵 $price — <b>$driver_price</b> $sum\n\n"
                        "$alright")
        text = text.substitute(name=self.__Text_lang.chain.driver.name, driver_name=self.__name, rate=self.__rate,
                               phone=self.__Text_lang.chain.driver.phone, phone_driver=self.__phone_driver,
                               car=self.__Text_lang.chain.driver.car, color=self.__color, driver_car=self.__car,
                               number=self.__number,
                               from_place=self.__Text_lang.chain.driver.from_place, from_town=self.__from_town,
                               spot=self.__Text_lang.chain.driver.spot,
                               to_place=self.__Text_lang.chain.driver.to_place,
                               to_town=self.__to_town, to_sub_spot=self.__to_sub_spot,
                               place=self.__Text_lang.chain.driver.places, driver_place=self.__driver_places,
                               time=self.__Text_lang.chain.driver.time, driver_time=self.__driver_time,
                               price=self.__Text_lang.chain.driver.price, driver_price=self.__driver_price,
                               sum=self.__Text_lang.symbol.sum, alright=self.__Text_lang.chain.driver.alright)
        return text

    async def _unpack_order(self):
        self.__name, self.__phone_driver, self.__car, self.__color, self.__number, self.__rate = \
            await pg.select_parametrs_driver(driver_id=self.__data.get('driver_id'))
        self.__car = self.__Text_lang.car.car[self.__car]
        self.__color = self.__Text_lang.car.color[self.__color]
        self.__from_town = self.__data.get("from_town_value")
        self.__to_town = self.__data.get("to_town_value")
        self.__driver_places = Txt.places.places_dict[self.__data.get("places")]
        self.__driver_price = await func.int_to_str(num=self.__data.get("price"))
        await self._spot()
        await self._time()

    async def _time(self):
        date_time = self.__data.get("date_time")
        time = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        self.__driver_time = datetime.datetime.strftime(time, "%H:%M")

    async def _spot(self):
        if self.__data.get('to_district') is not None:
            self.__to_sub_spot = f'{self.__data.get("to_district_value")}, {self.__data.get("to_subspot_value")}'
        else:
            self.__to_sub_spot = self.__data.get("to_subspot_value")


class FormDriverCancel:
    def __init__(self, language: str, driver_id: int):
        self.__language = language
        self.__Text_lang = Txt.language[language]
        self.__driver_id = driver_id

    async def order(self):
        await self._unpack_order()
        text = Template("🤵 <b>$name</b>: $driver_name ⭐️$rate\n"
                        "📱 <b>$phone</b>: +$phone_driver\n"
                        "🚙 <b>$car</b>: $color $driver_car — $number\n\n"
                        "🅰️ <b>$from_place</b>: $from_town, $spot\n"
                        "🅱️ <b>$to_place</b>: $to_town, $to_sub_spot\n"
                        "💺 <b>$place</b>: $driver_place\n\n"
                        "⏰ $time <b>$driver_time</b>\n"
                        "💵 $price — <b>$driver_price</b> $sum")
        text = text.substitute(name=self.__Text_lang.chain.driver.name, driver_name=self.__name, rate=self.__rate,
                               phone=self.__Text_lang.chain.driver.phone, phone_driver=self.__phone_driver,
                               car=self.__Text_lang.chain.driver.car, color=self.__color, driver_car=self.__car,
                               number=self.__number,
                               from_place=self.__Text_lang.chain.driver.from_place, from_town=self.__from_town,
                               spot=self.__Text_lang.chain.driver.spot,
                               to_place=self.__Text_lang.chain.driver.to_place,
                               to_town=self.__to_town, to_sub_spot=self.__to_sub_spot,
                               place=self.__Text_lang.chain.driver.places, driver_place=self.__driver_places,
                               time=self.__Text_lang.chain.driver.time, driver_time=self.__driver_time,
                               price=self.__Text_lang.chain.driver.price, driver_price=self.__driver_price,
                               sum=self.__Text_lang.symbol.sum)
        return text

    async def _unpack_order(self):
        self.__name, self.__phone_driver, self.__car, self.__color, self.__number, self.__rate = \
            await pg.select_parametrs_driver(driver_id=self.__driver_id)
        self.__from_town, self.__to_town, self.__to_district, self.__to_sub_spot, self.__datetime, \
            self.__driver_places, self.__driver_price = await pg.route_parameters(driver_id=self.__driver_id)
        await self._unpack_route()
        await self._unpack_car()
        await self._unpack_smt()

    async def _unpack_route(self):
        self.__from_town = await pg.id_to_town(language=self.__language, sub_id=self.__from_town)
        self.__to_town = await pg.id_to_town(language=self.__language, sub_id=self.__to_town)
        await self._spot()
        # self.__to_sub_spot = await pg.id_to_sub_spot(language=self.__language, sub_id=self.__to_sub_spot)

    async def _spot(self):
        if self.__to_district is not None:
            self.__to_district = await pg.id_to_district(sub_id=self.__to_district, language=self.__language)
            self.__to_sub_spot = await pg.id_to_sub_spot(sub_id=self.__to_sub_spot, language=self.__language)
            self.__to_sub_spot = f'{self.__to_district}, {self.__to_sub_spot}'
        else:
            self.__to_sub_spot = await pg.id_to_sub_spot(sub_id=self.__to_sub_spot, language=self.__language)

    async def _unpack_car(self):
        self.__car = self.__Text_lang.car.car[self.__car]
        self.__color = self.__Text_lang.car.color[self.__color]

    async def _unpack_smt(self):
        self.__driver_time = datetime.datetime.strftime(self.__datetime, "%H:%M")
        self.__driver_places = Txt.places.places_dict[self.__driver_places]
        self.__driver_price = await func.int_to_str(num=self.__driver_price)

