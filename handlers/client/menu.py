from contextlib import suppress
from typing import Union
from config import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified, MessageToDeleteNotFound


from keyboards.reply.user import Reply
from keyboards.inline.client import Start, InlineClient
from text.client.menu import FormMenuClient
from text.client.client import FormClient
from pgsql import pg
from text.language.main import Text_main
from handlers.client.client import Client
from handlers.client.active_order import ActiveOrderClient
from handlers.client.on_spot import OnSpotClient
from handlers.driver.registration import RegistrationDriver
from handlers.driver.menu import MenuDriver


Txt = Text_main()
start = Start()
active = ActiveOrderClient()
on_spot = OnSpotClient()


class MenuClient(StatesGroup):
    registration = State()
    menu_client_level1 = State()
    menu_client_level2 = State()

    def __init__(self):
        self.__reply = None
        self.__Text_lang = None
        self.__exist = None
        self.__new_language = None
        self.__state = None
        self.__message = None

    async def void(self, call: types.CallbackQuery):
        await call.answer()

    # start
    async def command_start(self, message: types.Message, state: FSMContext):
        print(message)
        self.__message = message
        self.__state = state
        # a = 0
        # while a<10000000:
        #     await self._record()
        #     a+=1
        #     if a % 1000 == 0:
        #         print(a)
        await self._check_user_exist()

    async def _check_user_exist(self):
        self.__exist = await pg.exist_client(self.__message.from_user.id)
        exist_lang = await pg.exist_lang(self.__message.from_user.id)
        if self.__exist is True and exist_lang is True:
            await self._user()
        elif self.__exist is False or exist_lang is False:
            await self._new_user()

    async def _user(self):
        await pg.block_status(user_id=self.__message.from_user.id, status=True)
        await self.__state.reset_data()
        await self._check_user_type()

    async def _new_user(self):
        await self.registration.set()
        await bot.send_message(chat_id=self.__message.from_user.id, text=Txt.choose_language,
                               reply_markup=await start.choose_language())
        if self.__exist is False:
            await self._record()

    async def _record(self):
        user_id = self.__message.from_user.id
        name = self.__message.from_user.first_name
        username = self.__message.from_user.username
        await pg.first_rec_client(user_id=user_id, name=name, username=username, status=True)

    async def _check_user_type(self):
        exist = await pg.exist_driver(driver_id=self.__message.from_user.id)
        if exist is True:
            await self._start_driver()
        elif exist is False:
            await self._start_client()

    async def _start_client(self):
        await self._greeting_client()
        await self.menu_client_level1.set()

    async def _start_driver(self):
        await self._greeting_driver()
        await MenuDriver.menu_driver_level1.set()

    async def _greeting_client(self):
        async with self.__state.proxy() as data:
            data['lang'] = await pg.select_language(user_id=self.__message.from_user.id)
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
        await bot.send_message(chat_id=self.__message.from_user.id, text=Text_lang.start.start,
                               reply_markup=await reply.start_client())

    async def _greeting_driver(self):
        async with self.__state.proxy() as data:
            data['lang'] = await pg.select_language(user_id=self.__message.from_user.id)
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
        await bot.send_message(chat_id=self.__message.from_user.id, text=Text_lang.start.start,
                               reply_markup=await reply.start_driver())

    # language
    async def menu_choose_language(self, call: types.callback_query, state: FSMContext):
        await call.answer()
        language = call.data
        user_id = call.from_user.id
        await pg.update_language(language=language, user_id=user_id)
        async with state.proxy() as data:
            data['lang'] = language
            reply = Reply(language=language)
            form = FormMenuClient(language=language)
            # Text_lang = Txt.language[data.get('lang')]
        # await bot.send_video(chat_id=call.from_user.id, video=video_client, caption=Text_lang.video.client)
        with suppress(MessageToDeleteNotFound):
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id, text=await form.main(),
                               reply_markup=await reply.start_client(), disable_web_page_preview=True)
        print(data)
        await call.answer()
        await self.menu_client_level1.set()

    # main menu
    async def main_menu(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            await state.set_data(data={"lang": data.get('lang')})
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=Text_lang.menu.main_menu,
                                   reply_markup=await reply.start_client())
            await self.menu_client_level1.set()

    # settings
    @staticmethod
    async def menu_setting(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=Text_lang.menu.settings,
                                   reply_markup=await reply.setting())

    async def menu_change_language(self, message: types.Message, state: FSMContext):
        self.__message = message
        await self._change_language()
        async with state.proxy() as data:
            data['lang'] = self.__new_language
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=Text_lang.menu.main_menu,
                                   reply_markup=await reply.start_client())

    async def _change_language(self):
        new_language = self.__message.text
        user_id = self.__message.from_user.id
        if new_language == "🇷🇺 Ru":
            self.__new_language = 'rus'
        elif new_language == "🇺🇿 Уз (кир)":
            self.__new_language = 'uzb'
        elif new_language == "🇺🇿 Uz (lat)":
            self.__new_language = 'ozb'
        await pg.update_language(language=self.__new_language, user_id=user_id)

    @staticmethod
    async def menu_information(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=Text_lang.menu.information,
                                   reply_markup=await reply.information())

    @staticmethod
    async def menu_about_us(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            form = FormMenuClient(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=await form.about_us(),
                                   disable_web_page_preview=False)

    @staticmethod
    async def menu_how_to_use(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            form = FormMenuClient(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=await form.how_to_use(),
                                   disable_web_page_preview=False)

    @staticmethod
    async def menu_feedback(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            await bot.send_message(chat_id=message.from_user.id, text=Text_lang.feedback.feedback)

    @staticmethod
    async def menu_passenger(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            question = Text_lang.questions.passenger.from_town
            await state.set_data(data={"lang": data.get('lang')})
            reply = Reply(language=data.get('lang'))
            inline = InlineClient(language=data.get('lang'), condition=False)
            form = FormClient(data=await state.get_data(), question=question)
            if isinstance(message, types.Message):
                await bot.send_message(chat_id=message.from_user.id,  text=Text_lang.menu.passenger,
                                       reply_markup=await reply.main_menu())
                await bot.send_message(chat_id=message.from_user.id, reply_markup=await inline.menu_towns(),
                                       text=await form.main_text())
                data['row_id'] = await pg.insert_analise_client(user_id=message.from_user.id)
            elif isinstance(message, types.CallbackQuery):
                # async with state.proxy() as data:
                data.pop("from_town")
                data.pop("from_town_value")
                with suppress(MessageToDeleteNotFound):
                    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
                await bot.send_message(chat_id=message.from_user.id, text=Text_lang.menu.passenger,
                                       reply_markup=await reply.main_menu())
                with suppress(MessageToDeleteNotFound):
                    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id-1)
                await bot.send_message(chat_id=message.from_user.id, reply_markup=await inline.menu_towns(),
                                       text=await form.main_text())
                # with suppress(MessageNotModified):
                #     await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                #                                 text=await form.main_text(), reply_markup=await inline.menu_towns())
                await message.answer()
        await Client.client_level1.set()
        print(await state.get_state(), await state.get_data())

    # driver
    async def menu_driver(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            self.__message = message
            self.__state = state
            self.__Text_lang = Txt.language[data.get('lang')]
            self.__reply = Reply(language=data.get('lang'))
            await state.set_data(data={"lang": data.get('lang')})
            await self._check_registration()

    async def _check_registration(self):
        exist = await pg.exist_driver(driver_id=self.__message.from_user.id)
        if exist is True:
            await self._start_driver()
        elif exist is False:
            await self._registration()

    async def _registration(self):
        if isinstance(self.__message, types.Message):
            await bot.send_message(chat_id=self.__message.from_user.id, reply_markup=await self.__reply.main_menu(),
                                   text=self.__Text_lang.questions.registration.name)
        elif isinstance(self.__message, types.CallbackQuery):
            with suppress(MessageNotModified):
                await bot.edit_message_text(chat_id=self.__message.from_user.id,
                                            message_id=self.__message.message.message_id,
                                            text=self.__Text_lang.questions.registration.name)
        await RegistrationDriver.registration_level1.set()

    @staticmethod
    async def menu_allactive_order(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['client_id'] = message.from_user.id
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
        await bot.send_message(chat_id=message.from_user.id, text=Text_lang.menu.order,
                               reply_markup=await reply.main_menu())
        await active.active_order_check(data=data)
        await ActiveOrderClient.active_order_client.set()

    @staticmethod
    async def menu_on_spot(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['client_id'] = message.from_user.id
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
        await bot.send_message(chat_id=message.from_user.id, text=Text_lang.menu.spot,
                               reply_markup=await reply.main_menu())
        await on_spot.on_spot_check(data=data)
        await OnSpotClient.on_spot.set()



    # register_handler
    def register_handlers_client_menu(self, dp: Dispatcher):
        dp.register_message_handler(self.command_start, commands="start",                                               state='*')
        dp.register_callback_query_handler(self.void, text='void',                                                      state="*")
        dp.register_callback_query_handler(self.menu_choose_language, text=['rus', 'ozb', 'uzb'],                       state=self.registration)
        dp.register_message_handler(self.main_menu, text=Txt.menu.main_menu,
                                    state=[*MenuClient.states_names] + [*Client.states_names] +
                                          [*RegistrationDriver.states_names] + [*ActiveOrderClient.states_names] +
                                          [*OnSpotClient.states_names])

        dp.register_message_handler(self.menu_setting, text=Txt.menu.settings, state=self.menu_client_level1)
        dp.register_message_handler(self.menu_change_language, text=Txt.settings.language,
                                    state=self.menu_client_level1)

        dp.register_message_handler(self.menu_information, text=Txt.menu.information, state=self.menu_client_level1)
        dp.register_message_handler(self.menu_about_us, text=Txt.information.about_us, state=self.menu_client_level1)
        dp.register_message_handler(self.menu_how_to_use, text=Txt.information.how_to_use,
                                    state=self.menu_client_level1)
        dp.register_message_handler(self.menu_feedback, text=Txt.information.feedback, state=self.menu_client_level1)
        # переход в клиентскую часть из водителя
        dp.register_message_handler(self.main_menu, text=Txt.option.da, state=MenuDriver.menu_driver_level1)

        # переход в пассажирскую ветку
        dp.register_message_handler(self.menu_passenger, text=Txt.menu.passenger, state=self.menu_client_level1)
        dp.register_callback_query_handler(self.menu_passenger, text="back", state=Client.client_level2)

        # переход в клиентскую часть
        dp.register_message_handler(self.menu_driver, text=Txt.menu.driver, state=self.menu_client_level1)
        dp.register_callback_query_handler(self.menu_driver, text="back", state=RegistrationDriver.registration_level2)

        # активные ордера
        dp.register_message_handler(self.menu_allactive_order, text=Txt.menu.order, state=self.menu_client_level1)

        # я на месте
        dp.register_message_handler(self.menu_on_spot, text=Txt.menu.spot, state=self.menu_client_level1)




