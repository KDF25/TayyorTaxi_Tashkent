from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, BotBlocked
from config import bot


from keyboards.inline.client import InlineClient
from keyboards.reply.user import Reply
from pgsql import pg

from text.client.on_spot import FormOnSpotClient
from text.language.main import Text_main
from text.function.function import TextFunc


Txt = Text_main()
func = TextFunc()


class OnSpotClient(StatesGroup):
    on_spot = State()

    def __init__(self):
        self.__call = None
        self.__data = None

    async def on_spot_check(self, data: dict):
        self.__data = data
        exist = await pg.check_active_order_client(client_id=data.get('client_id'))
        if exist is True:
            await self._exist()
        else:
            await self._not_exist()

    async def _exist(self):
        await self._expired()
        await self._not_expired()

    async def _expired(self):
        for order_accept_id in await pg.select_order_accepted_to_client_expired(client_id=self.__data.get('client_id')):
            form = FormOnSpotClient(order_accept_id=order_accept_id[0], language=self.__data.get('lang'))
            inline = InlineClient(language=self.__data.get('lang'), order_accept_id=order_accept_id[0])
            location = await pg.active_location(order_accept_id=order_accept_id[0])
            await bot.send_location(chat_id=self.__data.get('client_id'), latitude=location['latitude'],
                                    longitude=location['longitude'])
            await bot.send_message(chat_id=self.__data.get('client_id'), text=await form.on_spot_view(),
                                   reply_markup=await inline.menu_on_spot())

    async def _not_expired(self):
        for order_accept_id in await pg.select_order_accepted_to_client_not_expired(client_id=self.__data.get('client_id')):
            form = FormOnSpotClient(order_accept_id=order_accept_id[0], language=self.__data.get('lang'))
            inline = InlineClient(language=self.__data.get('lang'), order_accept_id=order_accept_id[0])
            location = await pg.active_location(order_accept_id=order_accept_id[0])
            await bot.send_location(chat_id=self.__data.get('client_id'), latitude=location['latitude'],
                                    longitude=location['longitude'])
            await bot.send_message(chat_id=self.__data.get('client_id'), text=await form.on_spot_view(),
                                   reply_markup=await inline.menu_on_spot())

    async def _not_exist(self):
        Text_lang = Txt.language[self.__data.get('lang')]
        reply = Reply(language=self.__data.get('lang'))
        await bot.send_message(chat_id=self.__data.get('client_id'), text=Text_lang.active_order.no_active_order,
                               reply_markup=await reply.main_menu())

    async def menu_on_spot(self, call: types.CallbackQuery, state: FSMContext):
        self.__call = call
        async with state.proxy() as self.__data:
            self.__data['order_accept_id'] = int(call.data.split("_")[1])
            await self._mailing()

    async def _mailing(self):
        await self._mailing_client()
        await self._mailing_driver()

    async def _mailing_client(self):
        with suppress(MessageNotModified):
            form = FormOnSpotClient(language=self.__data.get('lang'), order_accept_id=self.__data.get('order_accept_id'))
            await bot.edit_message_text(chat_id=self.__call.from_user.id, message_id=self.__call.message.message_id,
                                        text=await form.on_spot_inform_client())
            await self.__call.answer()

    async def _mailing_driver(self):
        self.__driver_id = (await pg.orderid_to_order_accepted(order_accept_id=int(self.__call.data.split("_")[1])))[3]
        try:
            await self._driver()
        except BotBlocked:
            await pg.block_status(user_id=self.__driver_id, status=False)

    async def _driver(self):
        form = FormOnSpotClient(language=self.__data.get('lang'), order_accept_id=self.__data.get('order_accept_id'))
        await bot.send_message(chat_id=self.__driver_id, text=await form.on_spot_inform_driver())

    def register_handlers_on_spot_client(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_on_spot, lambda x: x.data.startswith("yes"),                       state=self.on_spot)

