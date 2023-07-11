from string import Template

from pgsql import pg
from text.language.main import Text_main
Txt = Text_main()


class FormNewOrderClient:
    def __init__(self, language: str, driver_id: int):
        self.__Text_lang = Txt.language[language]
        self.__driver_id = driver_id

    async def order_cancel(self):
        await self._unpack_driver()
        text = Template("$cancel\n\n"
                        "🤵 <b>$name</b>: $driver_name ⭐️$rate\n"
                        "🚙 <b>$car</b>: $driver_car\n\n"
                        "$new_driver")
        text = text.substitute(cancel=self.__Text_lang.cancel.client.cancel,
                               name=self.__Text_lang.chain.passenger.driver, driver_name=self.__name, rate=self.__rate,
                               car=self.__Text_lang.chain.passenger.car, driver_car=self.__car,
                               new_driver=self.__Text_lang.cancel.client.new_driver)
        return text

    async def order_delete(self):
        await self._unpack_driver()
        text = Template("$delete\n\n"
                        "🤵 <b>$name</b>: $driver_name ⭐️$rate\n"
                        "🚙 <b>$car</b>: $driver_car\n\n"
                        "$new_driver")
        text = text.substitute(delete=self.__Text_lang.cancel.client.delete,
                               name=self.__Text_lang.chain.passenger.driver, driver_name=self.__name, rate=self.__rate,
                               car=self.__Text_lang.chain.passenger.car, driver_car=self.__car,
                               new_driver=self.__Text_lang.cancel.client.new_driver)
        return text

    async def _unpack_driver(self):
        self.__name, phone, self.__car, color, number, self.__rate = \
            await pg.select_parametrs_driver(driver_id=self.__driver_id)
        self.__car = self.__Text_lang.car.car[self.__car]
