import asyncio
import datetime
from datetime_now import dt_now
import json
from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageNotModified, BotBlocked

from config import bot
from keyboards.inline.driver import InlineDriver
from keyboards.reply.user import Reply
from pgsql import pg
from text.client.new_order import FormNewOrderClient
from text.driver.new_order import FormNewOrderDriver
from text.function.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class Delay:
    def __init__(self, data: dict):
        self.__data = data

    async def start(self):
        await asyncio.sleep(await self._time())
        await self._mailing_client()

    async def _time(self):
        now = dt_now.now()
        now += datetime.timedelta(minutes=5)
        date_time = datetime.datetime.strptime(self.__data.get('date_time'), "%Y-%m-%d %H:%M:%S")
        sec = (date_time - now).total_seconds()
        sec -= 5*60
        return sec

    async def _mailing_client(self):
        if await self._active_check() is True:
            await self._trip_reminder()
            await asyncio.sleep(50*60)
            await self._rate_reminder()

    async def _active_check(self):
        return await pg.select_order_accept_check(order_accept_id=self.__data.get('order_accept_id'))

    async def _trip_reminder(self):
        await self._driver_reminder()
        await self._client_reminder()

    async def _driver_reminder(self):
        try:
            await self._driver()
        except BotBlocked:
            await pg.block_status(user_id=self.__data.get('driver_id'), status=False)

    async def _client_reminder(self):
        try:
            await self._client()
        except BotBlocked:
            await pg.block_status(user_id=self.__data.get('client_id'), status=False)

    async def _driver(self):
        form = FormNewOrderDriver(data=self.__data, language=self.__data.get('lang'))
        inline = InlineDriver(language=self.__data.get('lang'), order_accept_id=self.__data.get('order_accept_id'))
        reply = Reply(language=self.__data.get('lang'))
        await bot.send_location(chat_id=self.__data.get('driver_id'), reply_markup=await reply.main_menu(),
                                latitude=self.__data.get('location')['latitude'],
                                longitude=self.__data.get('location')['longitude'])
        await bot.send_message(chat_id=self.__data.get('driver_id'), text=await form.on_spot(),
                               reply_markup=await inline.menu_cancel_driver())

    async def _client(self):
        form = FormNewOrderDriver(data=self.__data, language=self.__data.get('lang_client'))
        inline = InlineDriver(language=self.__data.get('lang_client'), order_accept_id=self.__data.get('order_accept_id'))
        reply = Reply(language=self.__data.get('lang_client'))
        await bot.send_location(chat_id=self.__data.get('client_id'), reply_markup=await reply.main_menu(),
                                latitude=self.__data.get('location')['latitude'],
                                longitude=self.__data.get('location')['longitude'])
        await bot.send_message(chat_id=self.__data.get('client_id'), text=await form.on_spot(),
                               reply_markup=await inline.menu_cancel_client())

    async def _rate_reminder(self):
        if await self._active_check() is True:
            try:
                await self._rate()
            except BotBlocked:
                await pg.block_status(user_id=self.__data.get('client_id'), status=False)

    async def _rate(self):
        Text_lang = Txt.language[self.__data.get('lang_client')]
        inline = InlineDriver(language=self.__data.get('lang_client'), order_accept_id=self.__data.get('order_accept_id'))
        await bot.send_message(chat_id=self.__data.get('client_id'), text=Text_lang.questions.passenger.drivers_rate,
                               reply_markup=await inline.menu_rate())


class Accept:
    def __init__(self, call: types.CallbackQuery, data: dict):
        self.__time = None
        self.__client_id = None
        self.__call = call
        self.__data = data
        self.__Text_lang = Txt.language[self.__data.get('lang')]

    async def start(self):
        print('success')
        try:
            await self._update()
            await self._booking()
            await self._mailing()
            await self._wallet_check()
            delay = Delay(data=self.__data)
            await delay.start()
        except BotBlocked:
            await pg.block_status(user_id=self.__data.get('client_id'), status=False)
            await pg.update_orders_client_rejected(order_client_id=self.__data.get('order_client_id'))
            await self.__call.answer(text=self.__Text_lang.alert.driver.accept_order_late, show_alert=True)

    # booking
    async def _booking(self):
        with suppress(MessageToDeleteNotFound):
            await bot.delete_message(chat_id=self.__data.get('driver_id'), message_id=self.__data.get('message_id'))
        self.__data['order_accept_id'] = await pg.order_accepted_rec(order_client_id=self.__data.get('order_client_id'),
                                                                     order_driver_id=self.__data.get('order_driver_id'),
                                                                     client_id=self.__data.get('client_id'),
                                                                     driver_id=self.__data.get('driver_id'),
                                                                     phone_client=self.__data.get('phone_client'),
                                                                     phone_driver=self.__data.get('phone_driver'),
                                                                     from_town=self.__data.get('from_town'),
                                                                     location=self.__data.get('location'),
                                                                     to_town=self.__data.get('to_town'),
                                                                     to_district=self.__data.get('to_district'),
                                                                     to_spot=self.__data.get('to_spot'),
                                                                     to_subspot=self.__data.get('to_subspot'),
                                                                     date_time=self.__data.get('date_time'),
                                                                     places=self.__data.get('places'),
                                                                     price=self.__data.get('price'),
                                                                     cost=self.__data.get('cost'))

    # update
    async def _update(self):
        await self._update_order()
        await self._update_places()
        await self._update_wallet()

    async def _update_places(self):
        await pg.update_order_driver_add_places(order_driver_id=self.__data.get('order_driver_id'),
                                                places=self.__data.get('places'))

    async def _update_order(self):
        await pg.update_orders_client_cancel(client_id=self.__data.get('client_id'),
                                             from_town=self.__data.get('from_town'),
                                             to_town=self.__data.get('to_town'),
                                             order_driver_id=self.__data.get('order_driver_id'))
        await pg.update_orders_client_accepted(order_client_id=self.__data.get('order_client_id'))


    async def _update_wallet(self):
        await self._change_wallet()
        await pg.update_driver_wallet_accept(driver_id=self.__data.get('driver_id'), wallet=self.__wallet)

    async def _change_wallet(self):
        self.__wallet = await pg.select_every_wallet(driver_id=self.__data.get('driver_id'))
        self.__wallet = [i for i in self.__wallet]
        price = self.__data.get('order_price')
        if self.__wallet[2] == self.__wallet[1] == 0:
            self.__wallet[0] -= price
        elif self.__wallet[2] >= 0:
            if self.__wallet[2] >= price:
                self.__wallet[2] -= price
            elif self.__wallet[2] < price:
                price -= self.__wallet[2]
                self.__wallet[2] = 0
                if self.__wallet[1] >= price:
                    self.__wallet[1] -= price
                elif self.__wallet[1] < price:
                    price -= self.__wallet[1]
                    self.__wallet[1] = 0
                    self.__wallet[0] -= price

    # mailing
    async def _mailing(self):
        await self._mailing_client()
        await self._mailing_driver()

    async def _mailing_client(self):
        form = FormNewOrderDriver(data=self.__data, language=self.__data.get('lang_client'))
        reply = Reply(language=self.__data.get('lang_client'))
        inline = InlineDriver(language=self.__data.get('lang_client'), order_accept_id=self.__data.get('order_accept_id'))
        await bot.send_message(chat_id=self.__data.get('client_id'), text='.',
                               reply_markup=await reply.main_menu())
        await bot.send_message(chat_id=self.__data.get('client_id'), text=await form.new_order_client(),
                               reply_markup=await inline.menu_location_client())

    async def _mailing_driver(self):
        form = FormNewOrderDriver(data=self.__data, language=self.__data.get('lang'))
        inline = InlineDriver(language=self.__data.get('lang'), order_accept_id=self.__data.get('order_accept_id'))
        await bot.send_message(chat_id=self.__data.get('driver_id'), text=await form.new_order_driver(),
                               reply_markup=await inline.menu_location_driver())

    ############
    async def _wallet_check(self):
        if await self._wallet() is False:
            await self._mailing_wallet()

    async def _wallet(self):
        wallet = await pg.select_all_wallet(driver_id=self.__data.get('driver_id'))
        tax = Txt.money.wallet.tax
        return bool(wallet >= tax)

    async def _mailing_wallet(self):
        reply = Reply(language=self.__data.get('lang'))
        await bot.send_message(chat_id=self.__data.get('driver_id'), reply_markup=await reply.main_menu(),
                               text=self.__Text_lang.alert.driver.insufficient_funds2)


class Reject:
    def __init__(self, data: dict):
        self.__data = data
        self.__Text_lang = Txt.language[self.__data.get('lang')]
        self.__Text_lang_client = Txt.language[self.__data.get('lang_client')]

    async def start(self):
        await self._update_reject()
        await self._mailing()

    async def _update_reject(self):
        await pg.update_orders_client_rejected(order_client_id=self.__data.get('order_client_id'))

    async def _mailing(self):
        await self._mailing_driver()
        try:
            await self._mailing_client()
        except BotBlocked:
            print('reject')
            await pg.block_status(user_id=self.__data.get('client_id'), status=False)

    async def _mailing_driver(self):
        with suppress(MessageNotModified):
            await bot.edit_message_text(chat_id=self.__data.get('driver_id'), message_id=self.__data.get('message_id'),
                                        text=self.__Text_lang.order.driver.reject)

    async def _mailing_client(self):
        reply = Reply(language=self.__data.get('lang_client'))
        form = FormNewOrderClient(language=self.__data.get('lang_client'), driver_id=self.__data.get('driver_id'))
        inline = InlineDriver(order_client_id=self.__data.get('order_client_id'), language=self.__data.get('lang_client'))
        await bot.send_message(chat_id=self.__data.get('client_id'), text=self.__Text_lang_client.menu.passenger,
                               reply_markup=await reply.main_menu())
        await bot.send_message(chat_id=self.__data.get('client_id'), text=await form.order_cancel(),
                               reply_markup=await inline.menu_more())


class Unpack:
    def __init__(self, call: types.CallbackQuery, data: dict):
        self.__call = call
        self.__data = data

    async def start(self):
        await self._unpack_call()
        await self._unpack_new_order()
        await self._unpack_driver()
        print(self.__data)
        return self.__data

    async def _unpack_call(self):
        self.__data['order_client_id'] = int(self.__call.data.split("_")[1])
        self.__data['driver_id'] = self.__call.from_user.id
        self.__data['lang'] = await pg.select_language(user_id=self.__call.from_user.id)
        self.__data['message_id'] = self.__call.message.message_id

    async def _unpack_new_order(self):
        self.__data['order_driver_id'], self.__data['client_id'], self.__data['from_town'], location, \
            self.__data['to_town'], self.__data['to_district'], self.__data['to_spot'],  self.__data['to_subspot'], \
            date_time, self.__data['places'],  self.__data['price'], self.__data['cost'], \
            self.__data['phone_client'] = await pg.new_order_driver(order_client_id=self.__data['order_client_id'])
        # self.__data['location'] = json.loads(location)
        self.__data['date_time'] = datetime.datetime.strftime(date_time, "%Y-%m-%d %H:%M:%S")
        self.__data['time'] = datetime.datetime.strftime(date_time, "%H:%M")
        print(self.__data)
        self.__data['lang_client'] = await pg.select_language(user_id=self.__data.get('client_id'))

    async def _unpack_driver(self):
        self.__data['name'], self.__data['phone_driver'], self.__data['car'], self.__data['color'], \
            self.__data['number'], rate = \
            await pg.select_parametrs_driver(driver_id=self.__data.get('driver_id'))
        self.__data['location'] = await pg.route_location(driver_id=self.__data.get('driver_id'))
        Text_lang = Txt.language[self.__data['lang']]
        self.__data['rate'] = float(rate)
        self.__data['car_value'] = Text_lang.car.car[self.__data['car']]


class Condition:
    def __init__(self, data: dict):
        self.__data = data

    async def places_check(self):
        num = self.__data.get('places')
        free_places = await pg.check_places_orders_driver(order_driver_id=self.__data.get('order_driver_id'))
        return free_places >= num

    async def active_check(self):
        return await pg.select_order_client_check(order_client_id=self.__data.get('order_client_id'))

    async def price_check(self):
        wallet = await pg.select_all_wallet(driver_id=self.__data.get('driver_id'))
        order_price = await self.order_price()
        return wallet >= order_price

    async def order_price(self):
        order_price = (await func.percent_price(price=self.__data.get('price'))) * self.__data.get('places')
        return order_price


class NewOrderDriver(StatesGroup):

    @staticmethod
    async def menu_accept_order(call: types.CallbackQuery, state: FSMContext):
        print(call.data)
        unpack = Unpack(call=call, data=await state.get_data())
        await state.set_data(data=await unpack.start())
        condition = Condition(data=await state.get_data())
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            data['order_price'] = await condition.order_price()
            condition_active = await condition.active_check()
            condition_places = await condition.places_check()
            condition_wallet = await condition.price_check()
            print(await condition.active_check())
        if condition_active is True and condition_places is True and condition_wallet is True:
            accept = Accept(call=call, data=await state.get_data())
            await accept.start()
        elif condition_places is False:
            await call.answer(text=Text_lang.alert.driver.places_error, show_alert=True)
        elif condition_wallet is False:
            await call.answer(text=Text_lang.alert.driver.insufficient_funds, show_alert=True)
        elif condition_active is False:
            await call.answer(text=Text_lang.alert.driver.accept_order_late, show_alert=True)
        else:
            await call.answer(text=Text_lang.alert.driver.accept_order_late, show_alert=True)
        await state.set_state("MenuDriver:menu_driver_level1")
        print("accept", await state.get_data())

    @staticmethod
    async def menu_reject_order(call: types.CallbackQuery, state: FSMContext):
        unpack = Unpack(call=call, data=await state.get_data())
        await state.set_data(data=await unpack.start())
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
        condition_active = await pg.select_order_client_check(order_client_id=data.get('order_client_id'))
        if condition_active is True:
            reject = Reject(data=await state.get_data())
            await reject.start()
            await call.answer()
        elif condition_active is False:
            await call.answer(text=Text_lang.alert.driver.accept_order_late, show_alert=True)
        else:
            await call.answer(text=Text_lang.alert.driver.accept_order_late, show_alert=True)
        await state.set_state("MenuDriver:menu_driver_level1")

    @staticmethod
    async def menu_location(call: types.CallbackQuery, state: FSMContext):
        location = await pg.active_location(order_accept_id=int(call.data.split("_")[1]))
        await bot.send_location(chat_id=call.from_user.id, latitude=location['latitude'], longitude=location['longitude'])
        await call.answer()

    def register_handlers_new_order_driver(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_accept_order, lambda x: x.data.startswith("accept"),    state="*")
        dp.register_callback_query_handler(self.menu_reject_order, lambda x: x.data.startswith("reject"),    state="*")
        dp.register_callback_query_handler(self.menu_location, lambda x: x.data.startswith("point"),         state="*")


