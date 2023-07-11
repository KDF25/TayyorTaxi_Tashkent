from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, BotBlocked

from config import bot
from keyboards.inline.client import InlineClient
from keyboards.reply.user import Reply
from pgsql import pg
from text.client.active_order import FormActiveOrderClient
from text.function.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class Delete:
    def __init__(self, data: dict):
        self.__data = data

    async def start(self):
        await self._unpack_order()
        await self._update_cancel()
        await self._mailing()

    async def _unpack_order(self):
        order_client_id, client_id, order_driver_id, driver_id, phone_client, \
            from_town, to_town, to_district, to_subspot, datetime_trip, places, price, cost = \
            await pg.orderid_to_order_accepted(order_accept_id=self.__data.get('order_accept_id'))
        self.__data['order_driver_id'] = order_driver_id
        self.__data['driver_id'] = driver_id
        self.__data['places'] = places
        self.__data['wallet_return'] = (await func.percent_price(price=price)) * places

    async def _update_cancel(self):
        await pg.update_driver_wallet_payment(driver_id=self.__data.get('driver_id'),
                                              cash=self.__data.get('wallet_return'))
        await pg.cancel_active_order(order_accept_id=self.__data.get('order_accept_id'), client=True)
        await pg.update_order_driver_remove_places(order_driver_id=self.__data.get('order_driver_id'),
                                                   places=self.__data.get('places'))

    async def _mailing(self):
        await self._mailing_client()
        try:
            await self._mailing_driver()
        except BotBlocked:
            await pg.block_status(user_id=self.__data.get('driver_id'), status=False)

    async def _mailing_client(self):
        with suppress(MessageNotModified):
            Text_lang = Txt.language[self.__data.get('lang')]
            await bot.edit_message_text(chat_id=self.__data.get('client_id'), message_id=self.__data.get('message_id'),
                                        text=Text_lang.cancel.client.order)

    async def _mailing_driver(self):
        language = await pg.select_language(user_id=self.__data.get('driver_id'))
        form = FormActiveOrderClient(order_accept_id=self.__data.get('order_accept_id'), language=language)
        reply = Reply(language=language)
        await bot.send_message(chat_id=self.__data.get('driver_id'), text=await form.order_cancel(),
                               reply_markup=await reply.main_menu())


class ActiveOrderClient(StatesGroup):
    active_order_client = State()

    def __init__(self):
        self.__data = None

    @staticmethod
    async def menu_location(call: types.CallbackQuery, state: FSMContext):
        location = await pg.active_location(order_accept_id=int(call.data.split("_")[1]))
        await bot.send_location(chat_id=call.from_user.id, latitude=location['latitude'], longitude=location['longitude'])
        await call.answer()

    @staticmethod
    async def menu_order_cancel(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data['order_accept_id'] = int(call.data.split("_")[1])
            Text_lang = Txt.language[data.get('lang')]
        with suppress(MessageNotModified):
            inline = InlineClient(language=data.get('lang'), order_accept_id=data.get('order_accept_id'))
            await bot.edit_message_text(chat_id=call.from_user.id, text=Text_lang.cancel.client.question_order,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_delete())

    @staticmethod
    async def menu_order_delete(call: types.CallbackQuery, state: FSMContext):
        print(call)
        async with state.proxy() as data:
            data['message_id'] = call.message.message_id
            data['order_accept_id'] = int(call.data.split("_")[1])
        delete = Delete(data=await state.get_data())
        await delete.start()

    @staticmethod
    async def menu_active_order(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data['order_accept_id'] = int(call.data.split("_")[1])
        with suppress(MessageNotModified):
            inline = InlineClient(language=data.get('lang'), order_accept_id=data.get('order_accept_id'))
            form = FormActiveOrderClient(language=data.get('lang'), order_accept_id=data.get('order_accept_id'))
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.order_view(), reply_markup=await inline.menu_cancel())
        await call.answer()

    async def active_order_check(self, data: dict):
        self.__data = data
        exist = await pg.check_active_order_client(client_id=data.get('client_id'))
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
        await bot.send_message(chat_id=self.__data.get('client_id'), text=Text_lang.active_order.no_active_order,
                               reply_markup=await reply.main_menu())

    async def _expired(self):
        for order_accept_id in await pg.select_order_accepted_to_client_expired(client_id=self.__data.get('client_id')):
            form = FormActiveOrderClient(order_accept_id=order_accept_id[0], language=self.__data.get('lang'))
            await bot.send_message(chat_id=self.__data.get('client_id'), text=await form.order_view())

    async def _not_expired(self):
        for order_accept_id in await pg.select_order_accepted_to_client_not_expired(client_id=self.__data.get('client_id')):
            form = FormActiveOrderClient(order_accept_id=order_accept_id[0], language=self.__data.get('lang'))
            inline = InlineClient(language=self.__data.get('lang'), order_accept_id=order_accept_id[0])
            await bot.send_message(chat_id=self.__data.get('client_id'), text=await form.order_view(),
                                   reply_markup=await inline.menu_cancel())

    def register_handlers_active_order_client(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_order_cancel, lambda x: x.data.startswith("cancel"),               state=self.active_order_client)
        dp.register_callback_query_handler(self.menu_order_delete, lambda x: x.data.startswith("yes"),                  state=self.active_order_client)
        dp.register_callback_query_handler(self.menu_active_order, lambda x: x.data.startswith("no"),                   state=self.active_order_client)
        dp.register_callback_query_handler(self.menu_location, lambda x: x.data.startswith("location"),                 state=self.active_order_client)

