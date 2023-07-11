import datetime
from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, BotBlocked

from config import bot
from handlers.driver.active_order import Delete
from handlers.driver.driver import Driver
from keyboards.inline.driver import InlineDriver
from keyboards.reply.user import Reply
from pgsql import pg

from text.driver.on_spot import FormOnSpotDriver

from text.function.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


driver = Driver()


class OnSpotDriver(StatesGroup):
    on_spot_driver = State()

    def __init__(self):
        self.__client_id = None
        self.__call = None
        self.__data = None

    async def menu_on_spot(self, call: types.CallbackQuery, state: FSMContext):
        self.__call = call
        async with state.proxy() as self.__data:
            self.__data['order_driver_id'] = int(call.data.split("_")[1])
            await self._mailing()

    async def _mailing(self):
        await self._mailing_driver()
        await self._mailing_client()

    async def _mailing_driver(self):
        with suppress(MessageNotModified):
            form = FormOnSpotDriver(language=self.__data.get('lang'), order_driver_id=self.__data.get('order_driver_id'))
            await bot.edit_message_text(chat_id=self.__call.from_user.id, message_id=self.__call.message.message_id,
                                        text=await form.on_spot_inform_driver())
            await self.__call.answer()

    async def _mailing_client(self):
        for phone, self.__client_id in await pg.orderid_to_clients(order_driver_id=self.__data.get('order_driver_id')):
            try:
                await self._client()
            except BotBlocked:
                await pg.block_status(user_id=self.__client_id, status=False)

    async def _client(self):
        form = FormOnSpotDriver(language=self.__data.get('lang'), order_driver_id=self.__data.get('order_driver_id'),
                                client_id=self.__client_id)
        await bot.send_message(chat_id=self.__client_id, text=await form.on_spot_inform_client())

    async def on_spot_check(self, data: dict):
        self.__data = data
        exist = await pg.check_active_order_driver(driver_id=data.get('driver_id'))
        if exist is True:
            await self._exist()
        else:
            await self._not_exist()

    async def _exist(self):
        for order_driver_id in await pg.select_order_driver(driver_id=self.__data.get('driver_id')):
            form = FormOnSpotDriver(order_driver_id=order_driver_id[0], language=self.__data.get('lang'))
            inline = InlineDriver(language=self.__data.get('lang'), order_driver_id=order_driver_id[0])
            location = await pg.driver_location(order_driver_id=order_driver_id[0])
            await bot.send_location(chat_id=self.__data.get('driver_id'), latitude=location['latitude'],
                                    longitude=location['longitude'])
            await bot.send_message(chat_id=self.__data.get('driver_id'), text=await form.on_spot_view(),
                                   reply_markup=await inline.menu_on_spot())

    async def _not_exist(self):
        Text_lang = Txt.language[self.__data.get('lang')]
        reply = Reply(language=self.__data.get('lang'))
        await bot.send_message(chat_id=self.__data.get('driver_id'), text=Text_lang.active_order.no_active_order,
                               reply_markup=await reply.main_menu())

    def register_handlers_on_spot_driver(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_on_spot, lambda x: x.data.startswith("yes"),                       state=self.on_spot_driver)