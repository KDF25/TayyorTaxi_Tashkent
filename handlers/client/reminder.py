from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.utils.exceptions import MessageNotModified, BotBlocked

from config import bot
from keyboards.inline.driver import InlineDriver
from keyboards.reply.user import Reply
from pgsql import pg
from text.client.active_order import FormActiveOrderClient
from text.driver.new_order import FormNewOrderDriver
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


class ReminderClient(StatesGroup):

    @staticmethod
    async def menu_order(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data['order_accept_id'] = int(call.data.split("_")[1])
        with suppress(MessageNotModified):
            form = FormActiveOrderClient(language=data.get('lang'), order_accept_id=data.get('order_accept_id'))
            inline = InlineDriver(language=data.get('lang'), order_accept_id=data.get('order_accept_id'))
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.on_spot(), reply_markup=await inline.menu_cancel_client())
        await call.answer()

    @staticmethod
    async def menu_order_cancel(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data['order_accept_id'] = int(call.data.split("_")[1])
            Text_lang = Txt.language[data.get('lang')]
        with suppress(MessageNotModified):
            inline = InlineDriver(language=data.get('lang'), order_accept_id=data.get('order_accept_id'))
            await bot.edit_message_text(chat_id=call.from_user.id, reply_markup=await inline.menu_delete_client(),
                                        text=Text_lang.cancel.client.question_order, message_id=call.message.message_id)
        await call.answer()

    @staticmethod
    async def menu_order_delete(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data['order_accept_id'] = int(call.data.split("_")[1])
            data['message_id'] = call.message.message_id
        delete = Delete(data=await state.get_data())
        await delete.start()

    def register_handlers_reminder_client(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_order_cancel, lambda x: x.data.startswith("ClientCancel"), state="*")
        dp.register_callback_query_handler(self.menu_order_delete, lambda x: x.data.startswith("ClientYes"), state="*")
        dp.register_callback_query_handler(self.menu_order, lambda x: x.data.startswith("ClientNo"), state="*")



