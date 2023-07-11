from string import Template
from aiogram.utils.markdown import hlink
from text.language.main import Text_main
from text.function.function import TextFunc

Txt = Text_main()
func = TextFunc()


class FormRegistration:
    def __init__(self, data=None):
        self.__data = data
        self.__Text_lang = Txt.language[self.__data.get('lang')]

    async def agreement(self):
        car = self.__Text_lang.car.car[self.__data.get('car')]
        color = self.__Text_lang.car.color[self.__data.get('color')]
        text = Template("<b>$name</b>: $driver_name\n"
                        "<b>$phone</b>: +$driver_phone\n"
                        "<b>$car</b>: $color $driver_car — $car_number\n\n"
                        "$question $rules")
        text = text.substitute(name=self.__Text_lang.personal_cabinet.name, driver_name=self.__data.get('name'),
                               phone=self.__Text_lang.personal_cabinet.phone, driver_phone=self.__data.get('phone'),
                               car=self.__Text_lang.personal_cabinet.car, driver_car=car, color=color,
                               car_number=self.__data.get('number'),
                               question=self.__Text_lang.questions.registration.agreement,
                               rules=await self._rules())
        return text

    async def _rules(self):
        text = Template('$text1')
        text = text.substitute(text1=hlink(url=self.__Text_lang.url.driver.rules,
                                           title=self.__Text_lang.questions.registration.rules))
        return text

    async def _how_to_use(self):
        text = Template('$text1')
        text = text.substitute(text1=hlink(url=self.__Text_lang.url.driver.how_to_use,
                                           title=self.__Text_lang.questions.registration.how_to_use))
        return text

    async def finish(self):
        form = Template("<b>$id</b>: $driver_id\n"
                        "<b>$money</b>: $driver_money $sum\n\n"
                        "$congratulation\n\n"
                        "👉 $how_to_use\n"
                        "👉 $rules\n\n"
                        "<i>$online</i>")
        form = form.substitute(id=self.__Text_lang.personal_cabinet.id, driver_id=self.__data.get('user_id'),
                               money=self.__Text_lang.personal_cabinet.wallet, sum=self.__Text_lang.symbol.sum,
                               driver_money=await func.int_to_str(num=Txt.money.wallet.wallet),
                               congratulation=self.__Text_lang.personal_cabinet.congratulation,
                               how_to_use=await self._how_to_use(), rules=await self._rules(),
                               online=self.__Text_lang.personal_cabinet.online)
        return form
