import datetime
from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, BotBlocked

from config import bot
from handlers.driver.driver import Driver
from keyboards.inline.driver import InlineDriver
from keyboards.reply.user import Reply
from pgsql import pg

from text.driver.active_order import FormActiveOrderDriver
from text.client.new_order import FormNewOrderClient
from text.function.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


driver = Driver()


class Delete:
    def __init__(self, data: dict):
        self.__data = data

    async def start(self):
        await self._unpack()
        await self._update()
        await self._mailing()

    async def _unpack(self):
        order_client_id, client_id, order_driver_id, driver_id, phone_client, \
            from_town, to_town, to_district, to_subspot, datetime_trip, places, price, cost = \
            await pg.orderid_to_order_accepted(order_accept_id=self.__data.get('order_accept_id'))
        self.__data['order_client_id'] = order_client_id
        self.__data['order_driver_id'] = order_driver_id
        self.__data['client_id'] = client_id
        self.__data['places'] = places

    async def _update(self):
        await pg.update_order_driver_remove_places(order_driver_id=self.__data.get('order_driver_id'),
                                                   places=self.__data.get('places'))
        # print('remove', self.__data.get('order_driver_id'), self.__data.get('places'))
        await pg.cancel_active_order(order_accept_id=self.__data.get('order_accept_id'), driver=True)

    async def _mailing(self):
        await self._mailing_driver()
        try:
            await self._mailing_client()
        except BotBlocked:
            print('cancel')
            await pg.block_status(user_id=self.__data.get('client_id'), status=False)

    async def _mailing_driver(self):
        with suppress(MessageNotModified):
            Text_lang = Txt.language[self.__data.get("lang")]
            await bot.edit_message_text(chat_id=self.__data.get('driver_id'), message_id=self.__data.get('message_id'),
                                        text=Text_lang.cancel.driver.order)

    async def _mailing_client(self):
        language_client = await pg.select_language(user_id=self.__data.get('client_id'))
        print(self.__data)
        Text_lang = Txt.language[language_client]
        reply = Reply(language=language_client)
        form = FormNewOrderClient(language=language_client, driver_id=self.__data.get('driver_id'))
        inline = InlineDriver(order_client_id=self.__data.get('order_client_id'), language=language_client)
        await bot.send_message(chat_id=self.__data.get('client_id'), text=Text_lang.menu.passenger,
                               reply_markup=await reply.main_menu())
        await bot.send_message(chat_id=self.__data.get('client_id'), text=await form.order_delete(),
                               reply_markup=await inline.menu_more())


class ActiveOrderDriver(StatesGroup):
    active_order_driver = State()

    def __init__(self):
        self.__data = None

    @staticmethod
    async def menu_active_order(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data['order_accept_id'] = int(call.data.split("_")[1])
        with suppress(MessageNotModified):
            form = FormActiveOrderDriver(language=data.get('lang'), order_accept_id=data.get('order_accept_id'))
            inline = InlineDriver(language=data.get('lang'), order_accept_id=data.get('order_accept_id'))
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.order_view(), reply_markup=await inline.menu_cancel())
        await call.answer()

    @staticmethod
    async def menu_order_cancel(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data['order_accept_id'] = int(call.data.split("_")[1])
            Text_lang = Txt.language[data.get('lang')]
        with suppress(MessageNotModified):
            inline = InlineDriver(language=data.get('lang'), order_accept_id=data.get('order_accept_id'))
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=Text_lang.cancel.driver.driver, reply_markup=await inline.menu_delete())
        await call.answer()

    @staticmethod
    async def menu_order_delete(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data['message_id'] = call.message.message_id
        delete = Delete(data=await state.get_data())
        await delete.start()

    async def active_order_check(self, data: dict):
        self.__data = data
        exist = await pg.check_active_order_driver(driver_id=data.get('driver_id'))
        if exist is True:
            await self._exist()
        else:
            await self._not_exist()

    async def _exist(self):
        await self._expired()
        await self._not_expired()

    async def _not_exist(self):
        Text_lang = Txt.language[self.__data.get('lang')]
        reply = Reply(language=self.__data.get('lang'))
        await bot.send_message(chat_id=self.__data.get('driver_id'), text=Text_lang.active_order.no_active_order,
                               reply_markup=await reply.main_menu())

    async def _expired(self):
        for order_accept_id in await pg.select_order_accepted_to_driver_expired(driver_id=self.__data.get('driver_id')):
            form = FormActiveOrderDriver(order_accept_id=order_accept_id[0], language=self.__data.get('lang'))
            await bot.send_message(chat_id=self.__data.get('driver_id'), text=await form.order_view())

    async def _not_expired(self):
        for order_accept_id in await pg.select_order_accepted_to_driver_not_expired(driver_id=self.__data.get('driver_id')):
            form = FormActiveOrderDriver(order_accept_id=order_accept_id[0], language=self.__data.get('lang'))
            inline = InlineDriver(language=self.__data.get('lang'), order_accept_id=order_accept_id[0])
            await bot.send_message(chat_id=self.__data.get('driver_id'), text=await form.order_view(),
                                   reply_markup=await inline.menu_cancel())

    def register_handlers_active_order_driver(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_order_cancel, lambda x: x.data.startswith("cancel"),               state=self.active_order_driver)
        dp.register_callback_query_handler(self.menu_order_delete, text="yes",                                          state=self.active_order_driver)
        dp.register_callback_query_handler(self.menu_active_order, lambda x: x.data.startswith("no"),                   state=self.active_order_driver)