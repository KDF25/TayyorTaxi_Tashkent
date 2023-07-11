import asyncio
import datetime
import json
from contextlib import suppress
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToDeleteNotFound, BotBlocked

from config import bot
from keyboards.inline.client import InlineClient
from keyboards.inline.driver import InlineDriver
from keyboards.reply.user import Reply
from pgsql import pg
from text.client.client import FormClient
from text.client.new_order import FormNewOrderClient
from text.language.main import Text_main


Txt = Text_main()


class Mailing:

    def __init__(self, data: dict):
        self.__data = data
        self.__language = self.__data.get('lang')
        self.__Text_lang = Txt.language[self.__language]

    async def start(self):
        await self._client()
        try:
            await self._driver()
        except BotBlocked:
            print("block mail")
            await self._block()

    async def _client(self):
        with suppress(MessageNotModified):
            inline = InlineClient(language=self.__language)
            reply = Reply(language=self.__language)
            with suppress(MessageToDeleteNotFound):
                await bot.delete_message(chat_id=self.__data.get('client_id'), message_id=self.__data.get('message_id'))
            await bot.send_message(chat_id=self.__data.get('client_id'), text=self.__Text_lang.menu.passenger,
                                   reply_markup=await reply.main_menu())
            await bot.send_message(chat_id=self.__data.get('client_id'),  text=self.__Text_lang.order.client.passenger,
                                   reply_markup=await inline.menu_more())

    async def _driver(self):
        self.__language_driver = await pg.select_language(user_id=self.__data.get('driver_id'))
        inline = InlineClient(order_client_id=self.__data.get('order_client_id'), language=self.__language_driver)
        form = FormClient(data=self.__data)
        await bot.send_message(chat_id=self.__data.get("driver_id"), reply_markup=await inline.menu_accept_order(),
                               text=await form.order_driver(language=self.__language_driver))

    async def _block(self):
        await asyncio.sleep(120)
        await pg.block_status(user_id=self.__data.get('driver_id'), status=False)
        try:
            await self._close_order()
        except BotBlocked:
            print("block driver block")
            await pg.block_status(user_id=self.__data.get('client_id'), status=False)

    async def _close_order(self):
        print('not_accept')
        reply = Reply(language=self.__language)
        form = FormNewOrderClient(language=self.__language, driver_id=self.__data.get('driver_id'))
        inline = InlineDriver(language=self.__language, order_client_id=self.__data.get('order_client_id'))
        await pg.delay_passenger(order_client_id=self.__data.get('order_client_id'))
        await bot.send_message(chat_id=self.__data.get('client_id'), text=self.__Text_lang.menu.passenger,
                               reply_markup=await reply.main_menu())
        await bot.send_message(chat_id=self.__data.get('client_id'), text=await form.order_cancel(),
                               reply_markup=await inline.menu_more())


class Delay:

    def __init__(self, data: dict):
        self.__data = data
        self.__language = data.get('lang')
        self.__Text_lang = Txt.language[data.get('lang')]

    async def start(self):
        await asyncio.sleep(1200)
        await self._accept_check()

    async def _accept_check(self):
        if await self._check_1() is None and await self._check_1() is not True:
            try:
                await self._close_order()
            except BotBlocked:
                print("block accept check")
                await pg.block_status(user_id=self.__data.get('client_id'), status=False)

    async def _check_1(self):
        return await pg.check_order_accept(order_client_id=self.__data.get('order_client_id'))

    async def _check_2(self):
        return await pg.check_order_accept2(client_id=self.__data.get('client_id'),
                                            from_town=self.__data.get('from_town'),
                                            to_town=self.__data.get('to_town'))

    async def _close_order(self):
        print('not_accept')
        reply = Reply(language=self.__language)
        form = FormNewOrderClient(language=self.__language, driver_id=self.__data.get('driver_id'))
        inline = InlineDriver(language=self.__language, order_client_id=self.__data.get('order_client_id'))
        await pg.delay_passenger(order_client_id=self.__data.get('order_client_id'))
        await bot.send_message(chat_id=self.__data.get('client_id'), text=self.__Text_lang.menu.passenger,
                               reply_markup=await reply.main_menu())
        await bot.send_message(chat_id=self.__data.get('client_id'), text=await form.order_cancel(),
                               reply_markup=await inline.menu_more())


class Book:

    def __init__(self, data: dict):
        # self.__message = message
        self.__data = data

    async def start(self):
        # await self._unpack_message()
        await self._unpack_driver()
        await self._unpack_order()
        await self._book()
        return self.__data

    # async def _unpack_message(self):
    #     # self.__data["order_driver_id"] = int(self.__call.data.split('_')[1])
    #     self.__data['message_id'] = self.__message.message_id

    async def _unpack_driver(self):
        self.__data['driver_id'], self.__date_time, self.__data['places_driver'], self.__data['price'] = \
            await pg.select_order(order_driver_id=self.__data.get("order_driver_id"))

    async def _unpack_order(self):
        self.__data['cost'] = self.__data.get('price') * self.__data.get('places')
        self.__data['date_time'] = datetime.datetime.strftime(self.__date_time, "%Y-%m-%d %H:%M:%S")
        self.__data['time'] = datetime.datetime.strftime(self.__date_time, "%H:%M")

    async def _book(self):
        self.__data['order_client_id'] = await pg.order_client_rec(order_driver_id=self.__data.get('order_driver_id'),
                                                                   client_id=self.__data.get('client_id'),
                                                                   driver_id=self.__data.get('driver_id'),
                                                                   phone=self.__data.get('phone_client'),
                                                                   from_town=self.__data.get('from_town'),
                                                                   location=self.__data.get('location'),
                                                                   to_district=self.__data.get('to_district'),
                                                                   to_town=self.__data.get('to_town'),
                                                                   to_spot=self.__data.get('to_spot'),
                                                                   to_subspot=self.__data.get('to_subspot'),
                                                                   date_time=self.__data.get('date_time'),
                                                                   places=self.__data.get('places'),
                                                                   price=self.__data.get('price'),
                                                                   cost=self.__data.get('cost'))


class Count:

    def __init__(self, data: dict):
        self.__data = data

    async def subspot(self):
        return await pg.select_count_to_subspots(from_town=self.__data.get('from_town'),
                                                 to_town=self.__data.get('to_town'),
                                                 to_spot=self.__data.get('to_spot'),
                                                 to_subspot=self.__data.get('to_subspot'),
                                                 places=self.__data.get('places'),
                                                 client_id=self.__data.get('client_id'))

    async def spot(self):
        return await pg.select_count_to_spots(from_town=self.__data.get('from_town'), to_town=self.__data.get('to_town'),
                                              to_spot=self.__data.get('to_spot'), places=self.__data.get('places'),
                                              client_id=self.__data.get('client_id'))

    async def district(self):
        return await pg.select_count_to_districts(from_town=self.__data.get('from_town'),
                                                  to_town=self.__data.get('to_town'),
                                                  to_district=self.__data.get('to_district'),
                                                  places=self.__data.get('places'),
                                                  client_id=self.__data.get('client_id'))

    async def town(self):
        return await pg.select_count_to_town(from_town=self.__data.get('from_town'), to_town=self.__data.get('to_town'),
                                             places=self.__data.get('places'), client_id=self.__data.get('client_id'))


class Client(StatesGroup):

    client_level1 = State()
    client_level2 = State()
    client_level3 = State()
    client_level4 = State()
    client_level5 = State()
    client_level6 = State()

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

    def __init__(self):
        self.__call = None
        self.__state = None
        self.__number = None
        self.__message = None

    async def menu_location(self, call: types.CallbackQuery, state: FSMContext):
        await self.client_level2.set()
        async with state.proxy() as data:
            dta = call.data.split('_')
            if dta[0] == "town":
                data['client_id'] = int(call.from_user.id)
                data["from_town"] = int(dta[1])
                data["from_town_value"] = await pg.id_to_town(sub_id=data.get("from_town"), language=data.get('lang'))
                await pg.update_from_town_client(row_id=data.get('row_id'), from_town=data.get('from_town'))
            elif dta[0] == "back":
                data.pop("location")
            Text_lang = Txt.language[data.get('lang')]
            question = Text_lang.questions.passenger.location
            form = FormClient(question=question, data=data)
            inline = InlineClient(language=data.get('lang'))
            reply = Reply(language=data.get('lang'))
        with suppress(MessageToDeleteNotFound):
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.from_user.id, text=Text_lang.menu.passenger,
                               reply_markup=await reply.share_location())
        with suppress(MessageToDeleteNotFound):
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
        await bot.send_message(chat_id=call.from_user.id, text=await form.main_text(),
                               reply_markup=await inline.menu_back())
        print(1, data)
        await call.answer()

    async def menu_to_town(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.client_level3.set()
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            question = Text_lang.questions.passenger.to_town
            form = FormClient(question=question, data=data)
            inline = InlineClient(language=data.get('lang'))
            reply = Reply(language=data.get('lang'))
            if isinstance(message, types.Message):
                data['location'] = {'latitude': float(message.location.latitude), 'longitude': message.location.longitude}
                await pg.update_location_client(row_id=data.get('row_id'))
                await bot.send_message(chat_id=message.chat.id, text=Text_lang.menu.passenger,
                                       reply_markup=await reply.main_menu())
                await bot.send_message(chat_id=message.from_user.id, reply_markup=await inline.menu_towns(),
                                       text=await form.main_text())
            elif isinstance(message, types.CallbackQuery):
                data.pop("to_town")
                data.pop("to_town_value")
                with suppress(MessageNotModified):
                    await message.answer()
                    await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                                text=await form.main_text(), reply_markup=await inline.menu_towns())

            print(2, data)

    async def menu_places(self, call: types.CallbackQuery, state: FSMContext):
        await self.client_level4.set()
        async with state.proxy() as data:
            dta = call.data.split('_')
            if dta[0] == "town":
                data["to_town"] = int(dta[1])
                data["to_town_value"] = await pg.id_to_town(sub_id=data.get("to_town"), language=data.get('lang'))
                await pg.update_to_town_client(row_id=data.get('row_id'), to_town=data.get('to_town'))
            elif dta[0] == "back":
                data.pop("places")
        with suppress(MessageNotModified):
            Text_lang = Txt.language[data.get('lang')]
            question = Text_lang.questions.passenger.places
            form = FormClient(question=question, data=data)
            inline = InlineClient(language=data.get('lang'))
            await call.answer()
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.main_text(), reply_markup=await inline.menu_places())
        print(3, data)

    async def menu_share_phone(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as self.__data:
            dta = call.data.split('_')
            if dta[0] == "places":
                self.__data["places"] = int(dta[1])
                await pg.update_places_client(row_id=self.__data.get('row_id'), places=self.__data.get('places'))
            else:
                self.__data.pop("to_district")
                self.__data.pop("to_district_value")
                self.__data.pop("to_spot")
                self.__data.pop("to_spot_value")
            with suppress(MessageNotModified):
                await self._count_check()
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            text=self.__text, reply_markup=self.__markup)
        print(4, self.__data)

    async def _count_check(self):
        await self._common()
        await self._choose_count()

    async def _common(self):
        self.__Text_lang = Txt.language[self.__data.get('lang')]
        self.__form = FormClient(question=self.__Text_lang.questions.passenger.to_spot, data=self.__data)
        self.__inline = InlineClient(data=self.__data, language=self.__data.get('lang'))
        self.__reply = Reply(language=self.__data.get('lang'))

    async def _choose_count(self):
        await self._count()
        if self.__count != 0 and self.__data.get('to_town') != 1:
            await self._var_1()
            await self._town_level1.set()
        elif self.__count != 0 and self.__data.get('to_town') == 1:
            await self._var_3()
            await self._city_level1.set()
        elif self.__count == 0:
            await self.client_level5.set()
            await self._var_2()

    async def _var_1(self):
        self.__data.pop("to_spot")
        self.__data.pop("to_spot_value")
        self.__text = await self.__form.main_text()
        self.__markup = await self.__inline.menu_spots()

    async def _var_2(self):
        self.__text = self.__Text_lang.chain.passenger.car_not_found
        self.__markup = await self.__inline.menu_back()
        await pg.update_no_model_client(row_id=self.__data.get('row_id'))

    async def _var_3(self):
        self.__data.pop("to_district")
        self.__data.pop("to_district_value")
        self.__text = await self.__form.main_text()
        self.__markup = await self.__inline.menu_districts()

    async def _count(self):
        self.__count = await pg.select_count_to_town(from_town=self.__data.get('from_town'),
                                                     to_town=self.__data.get('to_town'),
                                                     places=self.__data.get('places'),
                                                     client_id=self.__data.get('client_id'))

    async def menu_to_spot(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            dta = call.data.split('_')
            if dta[0] == "district":
                await self.next()
                data["to_district"] = int(dta[1])
                data["to_district_value"] = await pg.id_to_district(sub_id=data.get("to_district"),
                                                                    language=data.get('lang'))
                await pg.update_to_district_client(row_id=data.get('row_id'), to_district=data.get('to_district'))
            else:
                await self.previous()
                data.pop("to_spot")
                data.pop("to_spot_value")
            with suppress(MessageNotModified):
                Text_lang = Txt.language[data.get('lang')]
                question = Text_lang.questions.passenger.to_spot
                form = FormClient(question=question, data=data)
                inline = InlineClient(data=data, language=data.get('lang'))
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            text=await form.main_text(), reply_markup=await inline.menu_spots())
        print("5**", data)

    async def menu_to_sub_spot(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            dta = call.data.split('_')
            if dta[0] == "spot":
                await self.next()
                data["to_spot"] = int(dta[1])
                data["to_spot_value"] = await pg.id_to_spot(sub_id=data.get("to_spot"), language=data.get('lang'))
                await pg.update_to_spot_client(row_id=data.get('row_id'), to_spot=data.get('to_spot'))
            else:
                await self.previous()
                data.pop("to_subspot")
                data.pop("to_subspot_value")
            with suppress(MessageNotModified):
                Text_lang = Txt.language[data.get('lang')]
                question = Text_lang.questions.passenger.to_spot
                form = FormClient(question=question, data=data)
                inline = InlineClient(data=data, language=data.get('lang'))
                await call.answer()
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            text=await form.main_text(), reply_markup=await inline.menu_sub_spots())
        print(6, data)

    async def menu_list(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            dta = call.data.split('_')
            if dta[0] == "subspot":
                await self.next()
                data["to_subspot"] = int(dta[1])
                data["to_subspot_value"] = await pg.id_to_sub_spot(sub_id=data.get("to_subspot"),
                                                                   language=data.get('lang'))
                await pg.update_to_subspot_client(row_id=data.get('row_id'), to_subspot=data.get('to_subspot'))
                Text_lang = Txt.language[data.get('lang')]
                question = Text_lang.questions.passenger.car
                form = FormClient(question=question, data=data)
                inline = InlineClient(data=data, language=data.get('lang'))
                with suppress(MessageNotModified):
                    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                                text=await form.main_text(), reply_markup=await inline.menu_list())
            else:
                await self.previous()
                Text_lang = Txt.language[data.get('lang')]
                question = Text_lang.questions.passenger.car
                form = FormClient(question=question, data=data)
                inline = InlineClient(data=data, language=data.get('lang'))
                with suppress(MessageToDeleteNotFound):
                    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
                await bot.send_message(chat_id=call.from_user.id,  text=await form.main_text(),
                                       reply_markup=await inline.menu_list())
        print(7, data)
        await call.answer()

    @staticmethod
    async def menu_sort_time(call: types.CallbackQuery, state: FSMContext):
        await call.answer()
        async with state.proxy() as data:
            with suppress(MessageNotModified):
                Text_lang = Txt.language[data.get('lang')]
                question = Text_lang.questions.passenger.car
                form = FormClient(question=question, data=data)
                inline = InlineClient(data=data, language=data.get('lang'), condition=call.data)
                await pg.update_filters1_client(row_id=data.get('row_id'))
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            text=await form.main_text(), reply_markup=await inline.menu_list())

    @staticmethod
    async def menu_sort_distance(call: types.CallbackQuery, state: FSMContext):
        await call.answer()
        async with state.proxy() as data:
            with suppress(MessageNotModified):
                Text_lang = Txt.language[data.get('lang')]
                question = Text_lang.questions.passenger.car
                form = FormClient(question=question, data=data)
                inline = InlineClient(data=data, language=data.get('lang'), condition=call.data)
                await pg.update_filters3_client(row_id=data.get('row_id'))
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            text=await form.main_text(), reply_markup=await inline.menu_list())

    @staticmethod
    async def menu_sort_money(call: types.CallbackQuery, state: FSMContext):
        await call.answer()
        async with state.proxy() as data:
            with suppress(MessageNotModified):
                Text_lang = Txt.language[data.get('lang')]
                question = Text_lang.questions.passenger.car
                form = FormClient(question=question, data=data)
                inline = InlineClient(data=data, language=data.get('lang'), condition=call.data)
                await pg.update_filters2_client(row_id=data.get('row_id'))
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            text=await form.main_text(), reply_markup=await inline.menu_list())

    async def menu_order(self, call: types.CallbackQuery, state: FSMContext):
        await call.answer()
        async with state.proxy() as self.__data:
            dta = call.data.split('_')
            if dta[0] == "order":
                await self.next()
                self.__data["order_driver_id"] = int(dta[1])
                Text_lang = Txt.language[self.__data.get('lang')]
                inline = InlineClient(language=self.__data.get('lang'), order_driver_id=self.__data.get("order_driver_id"))
                reply = Reply(language=self.__data.get('lang'))
                form = FormClient(data=self.__data)
                with suppress(MessageNotModified):
                    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                                text=await form.order_passenger(), reply_markup=await inline.menu_order())
            else:
                await self.previous()
                Text_lang = Txt.language[self.__data.get('lang')]
                inline = InlineClient(language=self.__data.get('lang'), order_driver_id=self.__data.get("order_driver_id"))
                reply = Reply(language=self.__data.get('lang'))
                form = FormClient(data=self.__data)
                with suppress(MessageToDeleteNotFound):
                    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
                await bot.send_message(chat_id=call.message.chat.id, text=Text_lang.menu.passenger,
                                       reply_markup=await reply.main_menu())
                with suppress(MessageToDeleteNotFound):
                    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
                await bot.send_message(chat_id=call.from_user.id, text=await form.order_passenger(),
                                       reply_markup=await inline.menu_order())
        print(8, self.__data)

    @staticmethod
    async def menu_location_driver(call: types.CallbackQuery, state: FSMContext):
        await call.answer()
        async with state.proxy() as data:
            location = await pg.driver_location(order_driver_id=data.get('order_driver_id'))
            await bot.send_location(chat_id=call.from_user.id, latitude=location['latitude'], longitude=location['longitude'])

    async def menu_booking(self, call: types.CallbackQuery, state: FSMContext):
        await self.next()
        await call.answer()
        async with state.proxy() as self.__data:
            print(222, self.__data)
            dta = call.data.split('_')
            Text_lang = Txt.language[self.__data.get('lang')]
            reply = Reply(language=self.__data.get('lang'))
            inline = InlineClient(language=self.__data.get('lang'))
            if dta[0] == 'book':
                self.__data['order_driver_id'] = int(dta[1])
                await pg.update_ordered_client(row_id=self.__data.get('row_id'))
            if self.__data.get('phone_client') is None:
                with suppress(MessageToDeleteNotFound):
                    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
                await bot.send_message(chat_id=call.message.chat.id, text=Text_lang.menu.passenger,
                                       reply_markup=await reply.share_phone())
                with suppress(MessageToDeleteNotFound):
                    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
                message_1 = await bot.send_message(chat_id=call.from_user.id, text=Text_lang.questions.passenger.phone,
                                                   reply_markup=await inline.menu_share_phone())
                self.__data['message_id'] = message_1.message_id
            else:
                with suppress(MessageToDeleteNotFound):
                    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
                await self._book(state=state)

    async def menu_phone_text(self, message: types.Message, state: FSMContext):
        self.__message = message
        async with state.proxy() as data:
            try:
                Text_lang = Txt.language[data.get('lang')]
                self.__number = int(message.text.replace(" ", ""))
                number_len = len(str(self.__number))
                number_start = str(self.__number)[0:3]
                if number_len == 12 and number_start == '998':
                    await self._book(state=state)
                else:
                    await bot.send_message(chat_id=message.from_user.id, text=Text_lang.alert.phone.alert)
            except ValueError:
                await bot.send_message(chat_id=message.from_user.id, text=Text_lang.alert.phone.alert)

    async def menu_phone_contact(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        self.__message = message
        self.__number = int(message.contact.phone_number)
        await self._book(state=state)

    async def _book(self, state: FSMContext):
        await self.next()
        async with state.proxy() as self.__data:
            if self.__data.get('phone_client') is None:
                self.__data['phone_client'] = self.__number
                await pg.update_phone_client(row_id=self.__data.get('row_id'))
        await pg.update_book_client(row_id=self.__data.get('row_id'))
        book = Book(data=await state.get_data())
        await state.set_data(data=await book.start())
        mailing = Mailing(data=await state.get_data())
        delay = Delay(data=await state.get_data())
        await mailing.start()
        await delay.start()

    async def menu_more(self, call: types.CallbackQuery, state: FSMContext):
        print('menu_more')
        count = Count(data=await state.get_data())
        if await count.subspot() != 0:
            print('subspot', await count.subspot())
            await self.previous()
            await self.previous()
            await self.menu_list(call=call, state=state)
        elif await count.spot() != 0:
            print('spot', await count.spot())
            await self.previous()
            await self.previous()
            await self.previous()
            await self.menu_to_sub_spot(call=call, state=state)
        elif await count.district() != 0:
            print('district', await count.district())
            await self.previous()
            await self.previous()
            await self.previous()
            await self.previous()
            await self.menu_to_spot(call=call, state=state)
        else:
            print('no_car')
            await self.previous()
            await self.previous()
            await self.previous()
            await self.previous()
            await self.previous()
            await self.menu_share_phone(call=call, state=state)

    @staticmethod
    async def default(call: types.CallbackQuery, state: FSMContext):
        print(await state.get_state(), call.data)

    def register_handlers_client(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_location, lambda x: x.data.startswith("town"),                     state=self.client_level1)
        dp.register_callback_query_handler(self.menu_location, text="back",                                             state=self.client_level3)

        dp.register_message_handler(self.menu_to_town, content_types='location',                                        state=self.client_level2)
        dp.register_callback_query_handler(self.menu_to_town, text="back",                                              state=self.client_level4)

        dp.register_callback_query_handler(self.menu_places, lambda x: x.data.startswith("town"),                       state=self.client_level3)
        dp.register_callback_query_handler(self.menu_places, text="back",                                               state=[self._city_level1, self._town_level1, self.client_level5])

        dp.register_callback_query_handler(self.menu_share_phone, lambda x: x.data.startswith("places"),                state=self.client_level4)
        dp.register_callback_query_handler(self.menu_share_phone, text="back",                                          state=[self._city_level2, self._town_level2])

        dp.register_callback_query_handler(self.menu_to_spot, lambda x: x.data.startswith("district"),                  state=self._city_level1)
        dp.register_callback_query_handler(self.menu_to_spot, text="back",                                              state=self._city_level3)

        dp.register_callback_query_handler(self.menu_to_sub_spot, lambda x: x.data.startswith("spot"),                  state=[self._city_level2, self._town_level1])#6
        dp.register_callback_query_handler(self.menu_to_sub_spot, text="back",                                          state=[self._city_level4, self._town_level3])#8

        dp.register_callback_query_handler(self.menu_list, lambda x: x.data.startswith("subspot"),                      state=[self._city_level3, self._town_level2])#7
        dp.register_callback_query_handler(self.menu_list, text="back",                                                 state=[self._city_level5, self._town_level4])#9

        dp.register_callback_query_handler(self.menu_sort_time, text="sort_time",                                       state=[self._city_level4, self._town_level3])#8
        dp.register_callback_query_handler(self.menu_sort_distance, text="sort_distance",                               state=[self._city_level4, self._town_level3])#8
        dp.register_callback_query_handler(self.menu_sort_money, text="sort_money",                                     state=[self._city_level4, self._town_level3])#8

        dp.register_callback_query_handler(self.menu_order, lambda x: x.data.startswith("order"),                       state=[self._city_level4, self._town_level3])
        dp.register_callback_query_handler(self.menu_order, text="back",                                                state=[self._city_level6, self._town_level5])

        dp.register_callback_query_handler(self.menu_location_driver, lambda x: x.data.startswith("location"),          state=[self._city_level5, self._town_level4])  # 8

        dp.register_callback_query_handler(self.menu_booking, lambda x: x.data.startswith("book"),                      state=[self._city_level5, self._town_level4])

        dp.register_message_handler(self.menu_phone_text, content_types=["text"],                                       state=[self._city_level6, self._town_level5])
        dp.register_message_handler(self.menu_phone_contact, content_types=["contact"],                                 state=[self._city_level6, self._town_level5])

        dp.register_callback_query_handler(self.menu_more, text="back",                                                 state=[self._city_level7, self._town_level6])

        # dp.register_callback_query_handler(self.menu_new_order, lambda x: x.data.startswith("passenger"), state='*')
        # dp.register_callback_query_handler(self.default, lambda x: x.data.startswith(""), state='*')



