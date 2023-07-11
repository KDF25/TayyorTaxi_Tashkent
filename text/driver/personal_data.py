from string import Template
from pgsql import pg

from text.function.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class FormPersonalData:

    def __init__(self, data=None):
        self.__data = data
        self.__language = self.__data.get('lang')
        self.__Text_lang = Txt.language[self.__data.get('lang')]

    async def personal_data_form(self):
        await self._unpack_data()
        text = Template("<b>$id</b>: $driver_id\n"
                        "<b>$name</b>: $driver_name\n"
                        "<b>$phone</b>: $driver_phone\n"
                        "<b>$car</b>: $color $driver_car — $number\n")
        text = text.substitute(id=self.__Text_lang.personal_cabinet.id, driver_id=self.__driver_id,
                               name=self.__Text_lang.personal_cabinet.name, driver_name=self.__name,
                               phone=self.__Text_lang.personal_cabinet.phone, driver_phone=self.__phone_driver,
                               car=self.__Text_lang.personal_cabinet.car, driver_car=self.__car, color=self.__color,
                               number=self.__number)
        return text

    async def _unpack_data(self):
        self.__driver_id = self.__data.get('driver_id')
        self.__name = self.__data.get('name')
        self.__phone_driver = self.__data.get('phone_driver')
        self.__car = self.__Text_lang.car.car[self.__data.get('car')]
        self.__color = self.__Text_lang.car.color[self.__data.get('color')]
        self.__number = self.__data.get('number')

    async def change_car(self):
        await self._unpack_driver()
        text = Template("<b>$car</b>: $color $driver_car — $number\n\n"
                        "$new_data")
        text = text.substitute(car=self.__Text_lang.personal_cabinet.car, driver_car=self.__car, color=self.__color,
                               new_data=self.__Text_lang.chain.personal_cabinet.new_data, number=self.__number)
        return text

    async def change_number(self):
        await self._unpack_driver()
        text = Template("<b>$car</b>: $color $driver_car — $number\n\n"
                        "$sample\n\n")
        text = text.substitute(car=self.__Text_lang.personal_cabinet.car, driver_car=self.__car, color=self.__color,
                               sample=self.__Text_lang.questions.registration.number, number=self.__number)
        return text

    async def _unpack_driver(self):
        self.__car = self.__Text_lang.car.car[self.__data.get('car')]
        self.__color = self.__Text_lang.car.color[self.__data.get('color')]
        self.__number = self.__data.get('number')

    async def wallet_form(self):
        await self._unpack_wallet()
        form = Template("<b>$id</b>: $driver_id\n\n"
                        "$wallet👇\n"
                        "<b>$main:</b> $wallet_main $sum\n"
                        "<b>$bonus:</b> $wallet_bonus $sum\n")
        form = form.substitute(id=self.__Text_lang.personal_cabinet.id, driver_id=self.__driver_id,
                               wallet=self.__Text_lang.personal_cabinet.wallet,
                               main=self.__Text_lang.personal_cabinet.common, wallet_main=self.__main,
                               bonus=self.__Text_lang.personal_cabinet.bonus, wallet_bonus=self.__bonus,
                               sum=self.__Text_lang.symbol.sum)
        return form

    async def _unpack_wallet(self):
        self.__driver_id = self.__data.get('driver_id')
        self.__main = await func.int_to_str(num=self.__data.get('wallet')[0])
        self.__bonus = await func.int_to_str(num=self.__data.get('wallet')[1])

    async def pay_way_form(self):
        await self._unpack_pay_way()
        form = Template("<b>$id</b>: $driver_id\n"
                        "<b>$cash</b>: $driver_cash $sum\n")
        form = form.substitute(id=self.__Text_lang.personal_cabinet.id, driver_id=self.__driver_id,
                               cash=self.__Text_lang.chain.personal_cabinet.amount, sum=self.__Text_lang.symbol.sum,
                               driver_cash=self.__cash)
        return form

    async def _unpack_pay_way(self):
        self.__driver_id = self.__data.get('driver_id')
        self.__cash = await func.int_to_str(num=self.__data.get('cash'))

    async def payment_form(self):
        await self._unpack_payment()
        form = Template("$pay_way $type_payment\n"
                        "$amount: <b>$cash</b> $sum\n\n"
                        "<i>$payment</i>")
        form = form.substitute(pay_way=self.__Text_lang.chain.personal_cabinet.pay_way2, type_payment=self.__type,
                               amount=self.__Text_lang.chain.personal_cabinet.amount2, cash=self.__cash,
                               payment=self.__Text_lang.chain.personal_cabinet.payment2, sum=self.__Text_lang.symbol.sum)
        return form

    async def _unpack_payment(self):
        self.__type = self.__data.get('type')
        self.__cash = await func.int_to_str(num=self.__data.get('cash'))

    async def payment_accept(self):
        form = Template("$accept <b>$cash</b> $sum")
        form = form.substitute(accept=self.__Text_lang.chain.personal_cabinet.accept,
                               cash=await func.int_to_str(num=self.__data.get('cash')), sum=self.__Text_lang.symbol.sum)
        return form