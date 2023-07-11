import datetime
from contextlib import suppress
from typing import Union
import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToDeleteNotFound, BotBlocked

from config import bot
from datetime_now import dt_now
from keyboards.inline.driver import InlineDriver
from keyboards.reply.user import Reply
from pgsql import pg
from text.driver.driver import FormDriver
from text.language.main import Text_main

Txt = Text_main()


class Delay:
    def __init__(self, data: dict):
        self.__data = data

    async def start(self):
        now = dt_now.now()
        date_time = datetime.datetime.strptime(self.__data.get('date_time'), "%Y-%m-%d %H:%M:%S")
        sec = (date_time - now).total_seconds()
        await asyncio.sleep(sec)
        await self._check_route()

    async def _check_route(self):
        if await pg.route_exist(driver_id=self.__data.get('driver_id')) is False:
            try:
                await bot.send_message(chat_id=self.__data.get('driver_id'), text=Txt.reminder.driver)
            except BotBlocked:
                await pg.block_status(user_id=self.__data.get('driver_id'), status=False)


class Driver(StatesGroup):
    driver_level1 = State()
    driver_level2 = State()
    driver_level3 = State()
    driver_level4 = State()
    driver_level5 = State()
    driver_level6 = State()
    driver_level7 = State()
    driver_level8 = State()
    driver_level9 = State()
    driver_level10 = State()

    route_cancel = State()

    _city_level1 = State()
    _city_level2 = State()
    _city_level3 = State()
    _city_level4 = State()
    _city_level5 = State()
    _city_level6 = State()
    _city_level7 = State()

    _town_level1 = State()
    _town_level2 = State()
    _town_level3 = State()
    _town_level4 = State()
    _town_level5 = State()
    _town_level6 = State()
    _town_level7 = State()

    def __init__(self):
        self.__call = None
        self.__number = None
        self.__message = None

    @staticmethod
    async def menu_cancel_location(call: types.CallbackQuery):
        location = await pg.route_location(driver_id=call.from_user.id)
        await bot.send_location(chat_id=call.from_user.id, latitude=location['latitude'], longitude=location['longitude'])
        await call.answer()

    async def menu_cancel_start(self, call: types.CallbackQuery, state: FSMContext):
        await self.route_cancel.set()
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            inline = InlineDriver(language=data.get('lang'))
            await pg.update_cancel_driver(row_id=data.get('row_id'))
        with suppress(MessageNotModified):
            await bot.edit_message_text(chat_id=call.from_user.id, reply_markup=await inline.menu_route_choose(),
                                        text=Text_lang.questions.driver.sure, message_id=call.message.message_id)

    @staticmethod
    async def menu_cancel_finish(call: types.CallbackQuery, state: FSMContext):
        await state.set_state("MenuDriver:menu_driver_level1")
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            if call.data == 'yes':
                text = Text_lang.order.driver.route_cancel
                await pg.route_cancel(driver_id=call.from_user.id)
                await pg.update_delete_driver(row_id=data.get('row_id'))
            elif call.data == 'no':
                text = Text_lang.menu.main_menu
        with suppress(MessageToDeleteNotFound):
            reply = Reply(language=data.get('lang'))
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=await reply.start_driver())

    async def menu_location(self, call: types.CallbackQuery, state: FSMContext):
        await self.driver_level2.set()
        async with state.proxy() as data:
            dta = call.data.split('_')
            if dta[0] == "town" or dta[0] == "city":
                data['driver_id'] = int(call.from_user.id)
                data["from_town"] = int(dta[1])
                data["from_town_value"] = await pg.id_to_town(sub_id=data.get("from_town"), language=data.get('lang'))
                await pg.update_from_town_driver(row_id=data.get('row_id'), from_town=data.get('from_town'))
            elif dta[0] == "back":
                data.pop("location")
            Text_lang = Txt.language[data.get('lang')]
            question = Text_lang.questions.driver.location
            form = FormDriver(question=question, data=data)
            inline = InlineDriver(sub_id=data.get("from_town"), language=data.get('lang'))
            reply = Reply(language=data.get('lang'))
        with suppress(MessageToDeleteNotFound):
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.from_user.id, text=Text_lang.menu.online,
                               reply_markup=await reply.share_location())
        with suppress(MessageToDeleteNotFound):
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
        await bot.send_message(chat_id=call.from_user.id, text=await form.main_text(),
                               reply_markup=await inline.menu_back())

        print(data)
        await call.answer()

    async def menu_to_town(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.driver_level3.set()
        # print(message.location)
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            question = Text_lang.questions.driver.to_town
            form = FormDriver(question=question, data=data)
            inline = InlineDriver(language=data.get('lang'))
            reply = Reply(language=data.get('lang'))
            if isinstance(message, types.Message):
                data['location'] = {'latitude': float(message.location.latitude), 'longitude': message.location.longitude}
                await pg.update_location_driver(row_id=data.get('row_id'))
                await bot.send_message(chat_id=message.chat.id, text=Text_lang.menu.online,
                                       reply_markup=await reply.main_menu())
                await bot.send_message(chat_id=message.from_user.id, reply_markup=await inline.menu_towns(),
                                       text=await form.main_text())
            elif isinstance(message, types.CallbackQuery):
                data.pop("to_town")
                data.pop("to_town_value")
                with suppress(MessageNotModified):
                    await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                                text=await form.main_text(), reply_markup=await inline.menu_towns())
                print(data)

    async def menu(self, call: types.CallbackQuery, state: FSMContext):
        dta = call.data.split('_')
        # if dta[0] == "city":
        #     await self._city_level1.set()
        #     await self.menu_city_district(call=call, state=state)
        if dta[0] == "town":
            await self._town_level1.set()
            await self.menu_town_spot(call=call, state=state)

    async def menu_city_district(self, call: types.CallbackQuery, state: FSMContext):
        await self._city_level1.set()
        async with state.proxy() as data:
            dta = call.data.split('_')
            if dta[0] == "city":
                data["to_town"] = int(dta[1])
                data["to_town_value"] = await pg.id_to_town(sub_id=data.get("to_town"), language=data.get('lang'))
                await pg.update_to_town_driver(row_id=data.get('row_id'), to_town=data.get('to_town'))
            elif dta[0] == "back":
                data.pop("to_district")
                data.pop("to_district_value")
        with suppress(MessageNotModified):
            Text_lang = Txt.language[data.get('lang')]
            question = Text_lang.questions.driver.to_spot
            form = FormDriver(question=question, data=data)
            inline = InlineDriver(sub_id=data.get("to_town"), language=data.get('lang'))
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.main_text(), reply_markup=await inline.menu_districts())
        print(data)
        await call.answer()

    async def menu_city_spot(self, call: types.CallbackQuery, state: FSMContext):
        await self._city_level2.set()
        async with state.proxy() as data:
            dta = call.data.split('_')
            if dta[0] == "district":
                data["to_district"] = int(dta[1])
                data["to_district_value"] = await pg.id_to_district(sub_id=data.get("to_district"),
                                                                    language=data.get('lang'))
                await pg.update_to_district_driver(row_id=data.get('row_id'), to_district=data.get('to_district'))
            elif dta[0] == "back":
                data.pop("to_spot")
                data.pop("to_spot_value")
        with suppress(MessageNotModified):
            Text_lang = Txt.language[data.get('lang')]
            question = Text_lang.questions.driver.to_spot
            form = FormDriver(question=question, data=data)
            inline = InlineDriver(sub_id=data.get("to_district"), language=data.get('lang'))
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.main_text(), reply_markup=await inline.menu_spots_city())
        print(data)
        await call.answer()

    async def menu_town_spot(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            dta = call.data.split('_')
            if dta[0] == "town":
                await self.next()
                data["to_town"] = int(dta[1])
                data["to_town_value"] = await pg.id_to_town(sub_id=data.get("to_town"), language=data.get('lang'))
                await pg.update_to_town_driver(row_id=data.get('row_id'), to_town=data.get('to_town'))
            elif dta[0] == "back":
                await self.previous()
                data.pop("to_spot")
                data.pop("to_spot_value")
        with suppress(MessageNotModified):
            Text_lang = Txt.language[data.get('lang')]
            question = Text_lang.questions.driver.to_spot
            form = FormDriver(question=question, data=data)
            inline = InlineDriver(sub_id=data.get("to_town"), language=data.get('lang'))
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.main_text(), reply_markup=await inline.menu_spots())
        print(data)
        await call.answer()

    async def menu_to_sub_spot(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            dta = call.data.split('_')
            if dta[0] == "spot":
                await self.next()
                data["to_spot"] = int(dta[1])
                data["to_spot_value"] = await pg.id_to_spot(sub_id=data.get("to_spot"), language=data.get('lang'))
                await pg.update_to_spot_driver(row_id=data.get('row_id'), to_spot=data.get('to_spot'))
            elif dta[0] == "back":
                await self.previous()
                data.pop("to_subspot")
                data.pop("to_subspot_value")
        with suppress(MessageNotModified):
            Text_lang = Txt.language[data.get('lang')]
            question = Text_lang.questions.driver.to_spot
            form = FormDriver(question=question, data=data)
            inline = InlineDriver(sub_id=data.get("to_spot"), district=data.get('to_district'),
                                  language=data.get('lang'))
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.main_text(), reply_markup=await inline.menu_sub_spots())
        print(data)
        await call.answer()

    async def menu_price(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            dta = call.data.split('_')
            if dta[0] == "subspot":
                await self.next()
                data["to_subspot"] = int(dta[1])
                data["to_subspot_value"] = await pg.id_to_sub_spot(sub_id=data.get("to_subspot"),
                                                                   language=data.get('lang'))
                await pg.update_to_subspot_driver(row_id=data.get('row_id'), to_subspot=data.get('to_subspot'))
            elif dta[0] == "back":
                await self.previous()
        with suppress(MessageNotModified):
            Text_lang = Txt.language[data.get('lang')]
            question = Text_lang.questions.driver.price
            inline = InlineDriver(language=data.get('lang'))
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=question, reply_markup=await inline.menu_price())
        print(data)
        await call.answer()

    async def menu_places(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            dta = call.data.split('_')
            if dta[0] == "price":
                await self.next()
                data["price"] = int(dta[1])
                await pg.update_price_driver(row_id=data.get('row_id'), price=data.get('price'))
            elif dta[0] == "back":
                await self.previous()
        with suppress(MessageNotModified):
            Text_lang = Txt.language[data.get('lang')]
            question = Text_lang.questions.driver.places
            form = FormDriver(question=question, data=data)
            inline = InlineDriver(language=data.get('lang'))
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.main_text(), reply_markup=await inline.menu_places())
        print(data)
        await call.answer()

    async def menu_time(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            dta = call.data.split('_')
            if dta[0] == "places":
                await self.next()
                data["places"] = int(dta[1])
                await pg.update_places_driver(row_id=data.get('row_id'), places=data.get('places'))
            elif dta[0] == "back":
                await self.previous()
        with suppress(MessageNotModified):
            Text_lang = Txt.language[data.get('lang')]
            question = Text_lang.questions.driver.time
            inline = InlineDriver(language=data.get('lang'))
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=question, reply_markup=await inline.menu_time())
        print(data)
        await call.answer()

    async def menu_accept(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            dta = call.data.split('_')
            if dta[0] == "time":
                await self.next()
                data["date_time"] = dta[1]
                await pg.update_datetime_driver(row_id=data.get('row_id'), date_time=data.get('date_time'))
            elif dta[0] == "back":
                await self.previous()
        with suppress(MessageNotModified):
            form = FormDriver(data=data)
            inline = InlineDriver(language=data.get('lang'))
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.order(), reply_markup=await inline.menu_book())
        print(data)
        await call.answer()

    @staticmethod
    async def menu_location_send(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            location = data['location']
        await bot.send_location(chat_id=call.from_user.id, latitude=location['latitude'], longitude=location['longitude'])
        await call.answer()

    async def menu_book(self, call: types.CallbackQuery, state: FSMContext):
        self.__call = call
        async with state.proxy() as self.__data:
            await pg.update_book_driver(row_id=self.__data.get('row_id'))
            await self._booking()
            await self._mailing_driver()
            await state.set_state("MenuDriver:menu_driver_level1")
            await state.set_data(data={"lang": self.__data.get('lang')})
            delay = Delay(data=self.__data)
            await delay.start()

    async def _booking(self):
        await pg.order_driver_rec(driver_id=self.__data.get('driver_id'),
                                  from_town=self.__data.get('from_town'),
                                  location=self.__data.get('location'),
                                  to_district=self.__data.get('to_district'),
                                  to_town=self.__data.get('to_town'),
                                  to_spot=self.__data.get('to_spot'),
                                  to_subspot=self.__data.get('to_subspot'),
                                  date_time=self.__data.get('date_time'),
                                  places=self.__data.get('places'),
                                  price=self.__data.get('price'))

    async def _mailing_driver(self):
        Text_lang = Txt.language[self.__data.get('lang')]
        reply = Reply(self.__data.get('lang'))
        with suppress(MessageToDeleteNotFound):
            await bot.delete_message(chat_id=self.__call.from_user.id, message_id=self.__call.message.message_id)
        await bot.send_message(chat_id=self.__call.message.chat.id, text=Text_lang.questions.driver.accept,
                               reply_markup=await reply.start_driver())

    # async def default(self, call: types.CallbackQuery, state: FSMContext):
    #     print(await state.get_state(), call.data)

    def register_handlers_driver(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_cancel_location, text='location',                                  state=self.driver_level1)
        dp.register_callback_query_handler(self.menu_cancel_start, text='cancel',                                       state=self.driver_level1)
        dp.register_callback_query_handler(self.menu_cancel_finish, text=['yes', 'no'],                                 state=self.route_cancel)

        dp.register_callback_query_handler(self.menu_location, lambda x: x.data.startswith("town"),                     state=self.driver_level1)
        dp.register_callback_query_handler(self.menu_location, lambda x: x.data.startswith("city"),                     state=self.driver_level1)
        dp.register_callback_query_handler(self.menu_location, text="back",                                             state=self.driver_level3)

        dp.register_message_handler(self.menu_to_town, content_types='location',                                        state=self.driver_level2)
        dp.register_callback_query_handler(self.menu_to_town, text="back",                                              state=[self._city_level1, self._town_level2])#3

        dp.register_callback_query_handler(self.menu, lambda x: x.data.startswith("town"),                              state=self.driver_level3)

        dp.register_callback_query_handler(self.menu_city_district, lambda x: x.data.startswith("city"),                state=self.driver_level3)
        dp.register_callback_query_handler(self.menu_city_district, text="back",                                        state=self._city_level2)

        dp.register_callback_query_handler(self.menu_city_spot, lambda x: x.data.startswith("district"),                state=self._city_level1)
        dp.register_callback_query_handler(self.menu_city_spot, text="back",                                            state=self._city_level3)

        dp.register_callback_query_handler(self.menu_town_spot, text="back",                                            state=self._town_level3)#5

        dp.register_callback_query_handler(self.menu_to_sub_spot, lambda x: x.data.startswith("spot"),                  state=[self._city_level2, self._town_level2])#4
        dp.register_callback_query_handler(self.menu_to_sub_spot, text="back",                                          state=[self._city_level4, self._town_level4])#6

        dp.register_callback_query_handler(self.menu_price, lambda x: x.data.startswith("subspot"),                     state=[self._city_level3, self._town_level3])#5
        dp.register_callback_query_handler(self.menu_price, text="back",                                                state=[self._city_level5, self._town_level5])#7

        dp.register_callback_query_handler(self.menu_places, lambda x: x.data.startswith("price"),                      state=[self._city_level4, self._town_level4])#6
        dp.register_callback_query_handler(self.menu_places, text="back",                                               state=[self._city_level6, self._town_level6])#8

        dp.register_callback_query_handler(self.menu_time, lambda x: x.data.startswith("places"),                       state=[self._city_level5, self._town_level5])#7
        dp.register_callback_query_handler(self.menu_time, text="back",                                                 state=[self._city_level7, self._town_level7])#9

        dp.register_callback_query_handler(self.menu_accept, lambda x: x.data.startswith("time"),                       state=[self._city_level6, self._town_level6])#8

        dp.register_callback_query_handler(self.menu_location_send, lambda x: x.data.startswith("location"),            state=[self._city_level7, self._town_level7])
        dp.register_callback_query_handler(self.menu_book, text="book",                                                 state=[self._city_level7, self._town_level7])#9


        # dp.register_callback_query_handler(self.default, lambda x: x.data and x.data.startswith(""), state="*")


