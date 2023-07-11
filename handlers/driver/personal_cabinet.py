from contextlib import suppress
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageNotModified
# from payme_api.get_check import GetCheck
# from click_api.get_url import GetUrl
from click_api.get_url import GetUrl
from config import bot
from handlers.driver.driver import Driver
from keyboards.inline.driver import InlinePersonalCabinet
from keyboards.reply.user import Reply
from payme_api.get_check import GetCheck
from pgsql import pg
# from datetime_now.datetime_now import dt_now

from text.driver.personal_data import FormPersonalData
from text.language.main import Text_main

Txt = Text_main()

driver = Driver()


class PersonalCabinet(StatesGroup):
    personal_cabinet = State()

    change_data = State()
    _change_name = State()
    _change_phone = State()
    _change_auto = State()

    _change_model = State()
    _change_color = State()
    _change_number = State()

    wallet_level1 = State()
    wallet_level2 = State()
    wallet_level3 = State()
    wallet_level4 = State()
    wallet_level5 = State()

    def __init__(self):
        self.__number = None
        self.__state = None
        self.__phone = None
        self.__message = None

    async def menu_personal_data(self, message:  Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.change_data.set()
        if isinstance(message, types.Message):
            driver_id = message.from_user.id
            name, phone_driver, car, color, number, rate = await pg.select_parametrs_driver(driver_id=driver_id)
            async with state.proxy() as data:
                data['driver_id'] = driver_id
                data['name'] = name
                data['phone_driver'] = phone_driver
                data['car'] = car
                data['color'] = color
                data['number'] = number
                Text_lang = Txt.language[data.get('lang')]
                reply = Reply(language=data.get('lang'))
                form = FormPersonalData(data=data)
                inline = InlinePersonalCabinet(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=Text_lang.buttons.personal_cabinet.data.data,
                                   reply_markup=await reply.main_menu())
            await bot.send_message(chat_id=message.from_user.id, text=await form.personal_data_form(),
                                   reply_markup=await inline.menu_personal_data())
        elif isinstance(message, types.CallbackQuery):
            async with state.proxy() as data:
                inline = InlinePersonalCabinet(language=data.get('lang'))
                form = FormPersonalData(data=data)
            with suppress(MessageNotModified):
                await bot.edit_message_text(chat_id=message.from_user.id, reply_markup=await inline.menu_personal_data(),
                                            message_id=message.message.message_id, text=await form.personal_data_form())
                await message.answer()

    async def menu_auto(self, call: types.CallbackQuery, state: FSMContext):
        await self._change_auto.set()
        async with state.proxy() as data:
            inline = InlinePersonalCabinet(language=data.get('lang'))
            form = FormPersonalData(data=data)
            with suppress(MessageNotModified):
                await bot.edit_message_text(chat_id=call.from_user.id, text=await form.change_car(),
                                            message_id=call.message.message_id, reply_markup=await inline.menu_auto())
                await call.answer()

    async def menu_model(self, call: types.CallbackQuery, state: FSMContext):
        await self._change_model.set()
        async with state.proxy() as data:
            inline = InlinePersonalCabinet(language=data.get('lang'))
            form = FormPersonalData(data=data)
            with suppress(MessageNotModified):
                await bot.edit_message_text(chat_id=call.from_user.id, text=await form.change_car(),
                                            message_id=call.message.message_id, reply_markup=await inline.menu_model())
                await call.answer()

    async def menu_new_model(self, call: types.CallbackQuery, state: FSMContext):
        await self.personal_cabinet.set()
        async with state.proxy() as data:
            data['car'] = int(call.data.split('_')[1])
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
            await pg.update_drivers_car(driver_id=data.get('driver_id'), car=data.get('car'))
            with suppress(MessageToDeleteNotFound):
                await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await bot.send_message(chat_id=call.from_user.id, reply_markup=await reply.personal_cabinet(),
                                   text=Text_lang.chain.personal_cabinet.new_data_rec)

    async def menu_color(self, call: types.CallbackQuery, state: FSMContext):
        await self._change_color.set()
        async with state.proxy() as data:
            inline = InlinePersonalCabinet(language=data.get('lang'))
            form = FormPersonalData(data=data)
            with suppress(MessageNotModified):
                await bot.edit_message_text(chat_id=call.from_user.id, text=await form.change_car(),
                                            message_id=call.message.message_id, reply_markup=await inline.menu_color())
                await call.answer()

    async def menu_new_color(self, call: types.CallbackQuery, state: FSMContext):
        await self.personal_cabinet.set()
        async with state.proxy() as data:
            data['color'] = int(call.data.split('_')[1])
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
            await pg.update_drivers_color(driver_id=data.get('driver_id'), color=data.get('color'))
            with suppress(MessageToDeleteNotFound):
                await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await bot.send_message(chat_id=call.from_user.id, reply_markup=await reply.personal_cabinet(),
                                   text=Text_lang.chain.personal_cabinet.new_data_rec)

    async def menu_number(self, call: types.CallbackQuery, state: FSMContext):
        await self._change_number.set()
        async with state.proxy() as data:
            form = FormPersonalData(data=data)
            with suppress(MessageNotModified):
                await bot.edit_message_text(chat_id=call.from_user.id, text=await form.change_number(),
                                            message_id=call.message.message_id)
                await call.answer()

    async def menu_new_number(self, message: types.Message, state: FSMContext):
        await self.personal_cabinet.set()
        self.__message = message
        self.__state = state
        self.__number = message.text
        await self._number_check()

    async def _number_check(self):
        async with self.__state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
        if self.__number[0:2].isnumeric() and (len(self.__number) == 8 or len(self.__number) == 9):
            if len(self.__number) == 8 and self.__number[2:5].isnumeric() and self.__number[6:].isalpha():
                await self._number_accept()
            elif len(self.__number) == 8 and self.__number[3:6].isnumeric() \
                    and self.__number[7:].isalpha() and self.__number[2].isalpha():
                await self._number_accept()
            elif len(self.__number) == 9 and self.__number[2].isalpha() and self.__number[4:].isnumeric():
                await self._number_accept()
            else:
                await self._change_number.set()
                await bot.send_message(chat_id=self.__message.from_user.id, text=Text_lang.alert.phone.alert)
        else:
            await self._change_number.set()
            await bot.send_message(chat_id=self.__message.from_user.id, text=Text_lang.alert.phone.alert)

    async def _number_accept(self):
        async with self.__state.proxy() as data:
            data["number"] = self.__number.upper()
            reply = Reply(language=data.get('lang'))
            Text_lang = Txt.language[data.get('lang')]
            await pg.update_drivers_number(driver_id=data.get('driver_id'), number=data.get('number'))
            await bot.send_message(chat_id=self.__message.from_user.id, reply_markup=await reply.personal_cabinet(),
                                   text=Text_lang.chain.personal_cabinet.new_data_rec)

    async def menu_name(self, call: types.CallbackQuery, state: FSMContext):
        await self._change_name.set()
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            with suppress(MessageNotModified):
                await bot.edit_message_text(chat_id=call.from_user.id,  text=Text_lang.chain.personal_cabinet.new_data,
                                            message_id=call.message.message_id)
                await call.answer()

    async def menu_new_name(self, message: types.Message, state: FSMContext):
        await self.personal_cabinet.set()
        async with state.proxy() as data:
            data['name'] = message.text
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
            await pg.update_drivers_name(driver_id=data.get('driver_id'), name=data.get('name'))
            # await pg.update_route_driver_name(driver_id=data.get('driver_id'), name=data.get('name'))
            with suppress(MessageToDeleteNotFound):
                await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id-1)
            await bot.send_message(chat_id=message.from_user.id, text=Text_lang.chain.personal_cabinet.new_data_rec,
                                   reply_markup=await reply.personal_cabinet())

    async def menu_phone(self, call: types.CallbackQuery, state: FSMContext):
        await self._change_phone.set()
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
            with suppress(MessageToDeleteNotFound):
                await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await bot.send_message(chat_id=call.from_user.id, text=Text_lang.chain.personal_cabinet.new_data,
                                   reply_markup=await reply.share_phone())
        print(data)

    async def menu_phone_text(self, message: types.Message, state: FSMContext):
        self.__message = message
        self.__state = state
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            self.__phone = message.text.replace(" ", "").replace("+", "").replace("-", "")
            phone_len = len(str(self.__phone))
            phone_start = str(self.__phone)[0:3]
            if phone_len == 12 and phone_start == '998' and self.__phone.isnumeric():
                await self._phone_accept()
            else:
                await bot.send_message(chat_id=message.from_user.id, text=Text_lang.alert.phone.alert)

    async def menu_phone_contact(self, message: types.Message, state: FSMContext):
        self.__message = message
        self.__state = state
        self.__phone = int(message.contact.phone_number)
        await self._phone_accept()

    async def _phone_accept(self):
        await self.personal_cabinet.set()
        async with self.__state.proxy() as data:
            data["phone"] = int(self.__phone)
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
            await pg.update_drivers_phone(driver_id=data.get('driver_id'), phone=data.get('phone'))
            # await pg.update_route_driver_phone(driver_id=data.get('driver_id'), phone=data.get('phone'))
            # await pg.update_orders_accepted_phone(driver_id=data.get('driver_id'), phone=data.get('phone'))
        await bot.send_message(chat_id=self.__message.from_user.id, text=Text_lang.chain.personal_cabinet.new_data_rec,
                               reply_markup=await reply.personal_cabinet())

    # wallet

    async def menu_wallet(self, message:  Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.wallet_level1.set()
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            driver_id = message.from_user.id
            wallet = await pg.select_wallets(driver_id=driver_id)
            data['driver_id'] = driver_id
            data['wallet'] = [i for i in wallet]
            form = FormPersonalData(data=data)
            inline = InlinePersonalCabinet(language=data.get('lang'))
            reply = Reply(language=data.get('lang'))
            if isinstance(message, types.Message):
                await bot.send_message(chat_id=message.from_user.id, reply_markup=await reply.main_menu(),
                                       text=Text_lang.buttons.personal_cabinet.wallet.wallet)
                await bot.send_message(chat_id=message.from_user.id, text=await form.wallet_form(),
                                       reply_markup=await inline.menu_balance())
            elif isinstance(message, types.CallbackQuery):
                with suppress(MessageNotModified):
                    await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                                text=await form.wallet_form(), reply_markup=await inline.menu_balance())
                    await message.answer()
        print(data)

    async def menu_amount(self, call: types.CallbackQuery, state: FSMContext):
        await self.wallet_level2.set()
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            inline = InlinePersonalCabinet(language=data.get('lang'))
        with suppress(MessageNotModified):
            await bot.edit_message_text(chat_id=call.from_user.id, text=Text_lang.chain.personal_cabinet.payment,
                                        message_id=call.message.message_id, reply_markup=await inline.menu_cash())
            await call.answer()

    async def menu_pay_way(self, call: types.CallbackQuery, state: FSMContext):
        await self.wallet_level3.set()
        async with state.proxy() as data:
            dta = call.data.split('_')
            if dta[0] == 'cash':
                data['cash'] = int(call.data.split('_')[1])
            form = FormPersonalData(data=data)
            inline = InlinePersonalCabinet(language=data.get('lang'))
        with suppress(MessageNotModified):
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.pay_way_form(), reply_markup=await inline.menu_pay_way())
            await call.answer()

    async def menu_payme(self, call: types.CallbackQuery, state: FSMContext):
        await self.wallet_level4.set()
        async with state.proxy() as data:
            if call.data == 'Payme':
                data['type'] = call.data
            form = FormPersonalData(data=data)
            pay_id = await pg.wallet_pay(driver_id=call.from_user.id,
                                         cash=data["cash"], type_of_payment='Payme', status=False)
            check = GetCheck(amount=data["cash"], driver_id=call.from_user.id, pay_id=pay_id)
            await pg.start_order_from_check(check=await check.rec_check_to_database())
        inline = InlinePersonalCabinet(language=data.get('lang'), url=await check.return_url())
        with suppress(MessageNotModified):
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.payment_form(), reply_markup=await inline.payme_url())

    async def menu_click(self, call: types.CallbackQuery, state: FSMContext):
        await self.wallet_level4.set()
        async with state.proxy() as data:
            if call.data == 'Click':
                data['type'] = call.data
            form = FormPersonalData(data=data)
            pay_id = await pg.wallet_pay(driver_id=call.from_user.id,
                                         cash=data["cash"], type_of_payment="Click", status=False)
            geturl = GetUrl(driver_id=call.from_user.id, amount=data["cash"], pay_id=pay_id)
            inline = InlinePersonalCabinet(language=data.get('lang'), url=await geturl.return_url())
            await pg.add_click_order(order=await geturl.add_order())
        text = await form.payment_form()
        with suppress(MessageNotModified):
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                        reply_markup=await inline.click_url())

    async def menu_paynet(self, call: types.CallbackQuery, state: FSMContext):
        await self.wallet_level4.set()
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            inline = InlinePersonalCabinet(language=data.get('lang'))
        with suppress(MessageNotModified):
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=Text_lang.quiz.main, reply_markup=await inline.menu_quiz())
            await call.answer()

    async def menu_quiz(self, call: types.CallbackQuery, state: FSMContext):
        await self.wallet_level3.set()
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            form = FormPersonalData(data=data)
            inline = InlinePersonalCabinet(language=data.get('lang'))
            if await pg.exist_quiz(driver_id=call.from_user.id) is False:
                await pg.add_quiz(driver_id=call.from_user.id)
        with suppress(MessageNotModified):
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=await form.pay_way_form(), reply_markup=await inline.menu_pay_way())
            await call.answer(text=Text_lang.quiz.thanks, show_alert=True)

    def register_handlers_personal_cabinet(self, dp: Dispatcher):
        # personal data
        dp.register_message_handler(self.menu_personal_data, text=Txt.personal_cabinet.data,                            state=self.personal_cabinet)
        dp.register_callback_query_handler(self.menu_personal_data, text="back",                                        state=[self._change_auto, self._change_name, self._change_phone])

        dp.register_callback_query_handler(self.menu_name, text="name",                                                 state=self.change_data)
        dp.register_message_handler(self.menu_new_name, content_types="text",                                           state=self._change_name)

        dp.register_callback_query_handler(self.menu_auto, text="auto",                                                 state=self.change_data)
        dp.register_callback_query_handler(self.menu_auto, text="back",                                                 state=[self._change_model, self._change_color, self._change_number])

        dp.register_callback_query_handler(self.menu_model, text="model",                                               state=self._change_auto)
        dp.register_callback_query_handler(self.menu_new_model, lambda x: x.data.startswith("car"),                     state=self._change_model)
        dp.register_callback_query_handler(self.menu_color, text="colors",                                              state=self._change_auto)
        dp.register_callback_query_handler(self.menu_new_color, lambda x: x.data.startswith("color"),                   state=self._change_color)
        dp.register_callback_query_handler(self.menu_number, text="number",                                             state=self._change_auto)
        dp.register_message_handler(self.menu_new_number, content_types="text",                                         state=self._change_number)

        dp.register_callback_query_handler(self.menu_phone, text="phone",                                               state=self.change_data)

        dp.register_message_handler(self.menu_phone_text, content_types="text",                                         state=self._change_phone)
        dp.register_message_handler(self.menu_phone_contact, content_types="contact",                                   state=self._change_phone)

        # wallet
        dp.register_message_handler(self.menu_wallet, text=Txt.personal_cabinet.wallet,                                 state=self.personal_cabinet)
        dp.register_callback_query_handler(self.menu_wallet, text="back",                                               state=self.wallet_level2)

        dp.register_callback_query_handler(self.menu_amount, lambda x: x.data and x.data.startswith("balance"),         state=self.wallet_level1)
        dp.register_callback_query_handler(self.menu_amount, text="back",                                               state=self.wallet_level3)

        dp.register_callback_query_handler(self.menu_pay_way, lambda x: x.data.startswith("cash"),                      state=self.wallet_level2)
        dp.register_callback_query_handler(self.menu_pay_way, text="back",                                              state=self.wallet_level4)

        dp.register_callback_query_handler(self.menu_payme, text='Payme',                                               state=self.wallet_level3)
        dp.register_callback_query_handler(self.menu_click, text='Click',                                               state=self.wallet_level3)
        dp.register_callback_query_handler(self.menu_paynet, text='Paynet',                                             state=self.wallet_level3)
        dp.register_callback_query_handler(self.menu_quiz, text="quizback",                                             state=self.wallet_level4)








