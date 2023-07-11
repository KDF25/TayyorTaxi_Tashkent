from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageToDeleteNotFound

from config import bot
from keyboards.reply.user import Reply
from pgsql import pg
from text.function.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class DriversRate(StatesGroup):

    def __init__(self):

        self.__rate = None
        self.__driver_id = None
        self.__order_accept_id = None

    async def menu_rate(self, call: types.CallbackQuery, state: FSMContext):
        dta = call.data.split('_')
        self.__rate = int(dta[1])
        self.__order_accept_id = int(dta[2])
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
            await self._rates()
            await call.answer()
            with suppress(MessageToDeleteNotFound):
                await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await bot.send_message(chat_id=call.from_user.id, text=Text_lang.rate.rate_dict[self.__rate],
                                   reply_markup=await reply.main_menu())
        await state.set_state("MenuClient:menu_client_level1")

    async def _rates(self):
        driver_id = await pg.update_drivers_rate(order_accept_id=self.__order_accept_id, rate=self.__rate)
        rates = await pg.select_drivers_rate(order_accept_id=self.__order_accept_id)
        new_rate = await func.new_rate(rates=rates)
        await pg.update_drivers_new_rate(driver_id=driver_id, new_rate=new_rate)

    def register_handlers_drivers_rate_client(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_rate, lambda x: x.data.startswith("rate"),  state='*')
