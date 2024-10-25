from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.utils.exceptions import MessageNotModified, BotBlocked

from config import bot
from keyboards.inline.driver import InlineDriver
from keyboards.reply.user import Reply
from pgsql import pg
from text.client.new_order import FormNewOrderClient
from text.driver.active_order import FormActiveOrderDriver
from text.function.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


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
        self.__data['driver_id'] = driver_id
        self.__data['client_id'] = client_id
        self.__data['places'] = places

    async def _update(self):
        await pg.update_order_driver_remove_places(order_driver_id=self.__data.get('order_driver_id'),
                                                   places=self.__data.get('places'))
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
            print(self.__data)
            await bot.edit_message_text(chat_id=self.__data.get('driver_id'), message_id=self.__data.get('message_id'),
                                        text=Text_lang.cancel.driver.order)

    async def _mailing_client(self):
        language_client = await pg.select_language(user_id=self.__data.get('client_id'))
        Text_lang = Txt.language[language_client]
        reply = Reply(language=language_client)
        form = FormNewOrderClient(language=language_client, driver_id=self.__data.get('driver_id'))
        inline = InlineDriver(order_client_id=self.__data.get('order_client_id'), language=language_client)
        await bot.send_message(chat_id=self.__data.get('client_id'), text=Text_lang.menu.passenger,
                               reply_markup=await reply.main_menu())
        await bot.send_message(chat_id=self.__data.get('client_id'), text=await form.order_delete(),
                               reply_markup=await inline.menu_more())


class ReminderDriver(StatesGroup):

    @staticmethod
    async def menu_order(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data['order_accept_id'] = int(call.data.split("_")[1])
        with suppress(MessageNotModified):
            form = FormActiveOrderDriver(language=data.get('lang'), order_accept_id=data.get('order_accept_id'))
            inline = InlineDriver(language=data.get('lang'), order_accept_id=data.get('order_accept_id'))
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.on_spot(), reply_markup=await inline.menu_cancel_driver())
        await call.answer()

    @staticmethod
    async def menu_order_cancel(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data['order_accept_id'] = int(call.data.split("_")[1])
            Text_lang = Txt.language[data.get('lang')]
        with suppress(MessageNotModified):
            inline = InlineDriver(language=data.get('lang'), order_accept_id=data.get('order_accept_id'))
            await bot.edit_message_text(chat_id=call.from_user.id, reply_markup=await inline.menu_delete_driver(),
                                        text=Text_lang.cancel.client.question_order, message_id=call.message.message_id)
        await call.answer()

    @staticmethod
    async def menu_order_delete(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data['order_accept_id'] = int(call.data.split("_")[1])
            data['message_id'] = call.message.message_id
            delete = Delete(data=data)
            await delete.start()

    def register_handlers_reminder_driver(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_order_cancel, lambda x: x.data.startswith("DriverCancel"), state="*")
        dp.register_callback_query_handler(self.menu_order_delete, lambda x: x.data.startswith("DriverYes"), state="*")
        dp.register_callback_query_handler(self.menu_order, lambda x: x.data.startswith("DriverNo"), state="*")



