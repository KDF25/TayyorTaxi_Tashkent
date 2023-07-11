from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.utils.exceptions import MessageNotModified, MessageToDeleteNotFound

from config import dp, bot, storage
from keyboards.inline.driver import InlineDriverData
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.reply.user import Reply

from text.driver.registration import FormRegistration
from pgsql import pg
from typing import Union
from text.language.main import Text_main

Txt = Text_main()


class RegistrationDriver(StatesGroup):
    registration_level1 = State()
    registration_level2 = State()
    registration_level3 = State()
    registration_level4 = State()
    registration_level5 = State()
    registration_level6 = State()
    registration_level7 = State()
    registration_level8 = State()

    def __init__(self):
        self.__state = None
        self.__phone = None
        self.__number = None
        self.__message = None

    async def menu_name(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.registration_level2.set()
        async with state.proxy() as data:
            inline = InlineDriverData(language=data.get('lang'))
            Text_lang = Txt.language[data.get('lang')]
            if isinstance(message, types.Message):
                data['user_id'] = message.from_user.id
                data['username'] = message.from_user.username
                data['name'] = message.text
                await bot.send_message(chat_id=message.from_user.id, text=Text_lang.questions.registration.auto,
                                       reply_markup=await inline.menu_cars())
            elif isinstance(message, types.CallbackQuery):
                print(data)
                with suppress(MessageToDeleteNotFound):
                    await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                                text=Text_lang.questions.registration.auto,
                                                reply_markup=await inline.menu_cars())
                await message.answer()

    async def menu_cars(self, call: types.CallbackQuery, state: FSMContext):
        await self.registration_level3.set()
        async with state.proxy() as data:
            dta = call.data.split('_')
            if dta[0] == "car":
                data['car'] = int(dta[1])
        with suppress(MessageNotModified):
            inline = InlineDriverData(language=data.get('lang'))
            Text_lang = Txt.language[data.get('lang')]
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=Text_lang.questions.registration.color,
                                        reply_markup=await inline.menu_color())

    async def menu_color(self, call: types.CallbackQuery, state: FSMContext):
        await self.registration_level4.set()
        async with state.proxy() as data:
            dta = call.data.split('_')
            inline = InlineDriverData(language=data.get('lang'))
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
            if dta[0] == "color":
                data['color'] = int(dta[1])
                with suppress(MessageNotModified):
                    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                                text=Text_lang.questions.registration.number,
                                                reply_markup=await inline.menu_back())
            elif dta[0] == "back":
                with suppress(MessageToDeleteNotFound):
                    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id - 1)
                await bot.send_message(chat_id=call.from_user.id, text=Text_lang.menu.driver,
                                       reply_markup=await reply.main_menu())
                with suppress(MessageToDeleteNotFound):
                    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
                await bot.send_message(chat_id=call.from_user.id, text=Text_lang.questions.registration.number,
                                       reply_markup=await inline.menu_back())

    async def menu_number(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.registration_level5.set()
        self.__message = message
        self.__state = state
        if isinstance(message, types.Message):
            self.__number = message.text
            await self._number_check()
        elif isinstance(message, types.CallbackQuery):
            await self._number_back()

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
                await self.previous()
                await bot.send_message(chat_id=self.__message.from_user.id, text=Text_lang.alert.phone.alert)
        else:
            await self.previous()
            await bot.send_message(chat_id=self.__message.from_user.id, text=Text_lang.alert.phone.alert)

    async def _number_accept(self):
        async with self.__state.proxy() as data:
            data["number"] = self.__number.upper()
            inline = InlineDriverData(language=data.get('lang'))
            reply = Reply(language=data.get('lang'))
            Text_lang = Txt.language[data.get('lang')]
            await bot.send_message(chat_id=self.__message.from_user.id, text=Text_lang.menu.driver,
                                   reply_markup=await reply.share_phone())
            await bot.send_message(chat_id=self.__message.from_user.id, text=Text_lang.questions.registration.phone,
                                   reply_markup=await inline.menu_back())

    async def _number_back(self):
        async with self.__state.proxy() as data:
            inline = InlineDriverData(language=data.get('lang'))
            reply = Reply(language=data.get('lang'))
            Text_lang = Txt.language[data.get('lang')]
            with suppress(MessageToDeleteNotFound):
                await bot.delete_message(chat_id=self.__message.from_user.id,
                                         message_id=self.__message.message.message_id-1)
            await bot.send_message(chat_id=self.__message.from_user.id, text=Text_lang.menu.driver,
                                   reply_markup=await reply.share_phone())
            with suppress(MessageToDeleteNotFound):
                await bot.delete_message(chat_id=self.__message.from_user.id,
                                         message_id=self.__message.message.message_id)
            await bot.send_message(chat_id=self.__message.from_user.id, text=Text_lang.questions.registration.phone,
                                   reply_markup=await inline.menu_back())
            await self.__message.answer()

    async def menu_phone_text(self, message: types.Message, state: FSMContext):
        self.__message = message
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            self.__phone = message.text.replace(" ", "").replace("+", "").replace("-", "")
            phone_len = len(str(self.__phone))
            phone_start = str(self.__phone)[0:3]
            if phone_len == 12 and phone_start == '998' and self.__phone.isnumeric():
                await self._phone_accept(state=state)
            else:
                await bot.send_message(chat_id=message.from_user.id, text=Text_lang.alert.phone.alert)

    async def menu_phone_contact(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        print(message)
        self.__message = message
        if isinstance(message, types.Message):
            self.__phone = int(message.contact.phone_number)
            await self._phone_accept(state=state)
        elif isinstance(message, types.CallbackQuery):
            await self._phone_back(state=state)

    async def _phone_accept(self, state: FSMContext):
        await self.registration_level6.set()
        async with state.proxy() as data:
            data["phone"] = self.__phone
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
            inline = InlineDriverData(language=data.get('lang'))
            form = FormRegistration(data=data)
            await bot.send_message(chat_id=self.__message.from_user.id, text=Text_lang.menu.driver,
                                   reply_markup=await reply.main_menu())
            await bot.send_message(chat_id=self.__message.from_user.id, text=await form.agreement(),
                                   reply_markup=await inline.menu_agreement(), disable_web_page_preview=True)

    async def _phone_back(self, state: FSMContext):
        await self.registration_level6.set()
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            inline = InlineDriverData(language=data.get('lang'))
            reply = Reply(language=data.get('lang'))
            form = FormRegistration(data=data)
        with suppress(MessageToDeleteNotFound):
            await bot.delete_message(chat_id=self.__message.from_user.id, message_id=self.__message.message.message_id - 1)
        await bot.send_message(chat_id=self.__message.from_user.id, text=Text_lang.menu.driver,
                               reply_markup=await reply.main_menu())
        with suppress(MessageToDeleteNotFound):
            await bot.delete_message(chat_id=self.__message.from_user.id, message_id=self.__message.message.message_id)
        await bot.send_message(chat_id=self.__message.from_user.id, text=await form.agreement(),
                               reply_markup=await inline.menu_agreement(), disable_web_page_preview=True)

    async def menu_registration(self, call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
            form = FormRegistration(data=data)
            await pg.first_rec_driver(driver_id=call.from_user.id, name=data.get("name"), username=data.get('username'),
                                      wallet=Txt.money.wallet.wallet, phone=data.get('phone'), car=data.get("car"),
                                      color=data.get('color'), number=data.get('number'))
        print("ok", await state.get_state())
        with suppress(MessageToDeleteNotFound):
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.from_user.id, text=await form.finish(),
                               reply_markup=await reply.start_driver(), disable_web_page_preview=True)
        # await bot.send_video(chat_id=call.from_user.id, video=video_driver, caption=Text_lang.video.driver)
        await state.set_state("MenuDriver:menu_driver_level1")
        print("ok", await state.get_state())

    def register_handlers_registration(self, dp: Dispatcher):
        dp.register_message_handler(self.menu_name, content_types="text",                                               state=self.registration_level1)
        dp.register_callback_query_handler(self.menu_name, text="back",                                                 state=self.registration_level3)

        dp.register_callback_query_handler(self.menu_cars, lambda x: x.data.startswith("car"),                          state=self.registration_level2)
        dp.register_callback_query_handler(self.menu_cars, text="back",                                                 state=self.registration_level4)

        dp.register_callback_query_handler(self.menu_color, lambda x: x.data.startswith("color"),                       state=self.registration_level3)
        dp.register_callback_query_handler(self.menu_color, text="back",                                                state=self.registration_level5)

        dp.register_message_handler(self.menu_number, content_types="text",                                             state=self.registration_level4)
        dp.register_callback_query_handler(self.menu_number, text="back",                                               state=self.registration_level6)

        dp.register_message_handler(self.menu_phone_text, content_types="text",                                         state=self.registration_level5)
        dp.register_message_handler(self.menu_phone_contact, content_types="contact",                                   state=self.registration_level5)

        dp.register_callback_query_handler(self.menu_registration, text="agree",                                        state=self.registration_level6)

