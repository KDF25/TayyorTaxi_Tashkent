from contextlib import suppress
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageToDeleteNotFound
from handlers.driver.personal_cabinet import PersonalCabinet
from config import bot

from keyboards.inline.driver import InlineDriver
from keyboards.reply.user import Reply
from text.driver.menu import FormMenuDriver
from text.driver.driver import FormDriver, FormDriverCancel
from pgsql import pg
from handlers.driver.driver import Driver
from handlers.driver.active_order import ActiveOrderDriver
from handlers.driver.on_spot import OnSpotDriver

from text.language.main import Text_main

Txt = Text_main()
active = ActiveOrderDriver()
on_spot = OnSpotDriver()


class MenuDriver(StatesGroup):
    menu_driver_level1 = State()
    menu_driver_level2 = State()
    menu_driver_level3 = State()
    menu_driver_level4 = State()
    menu_driver_level5 = State()
    menu_driver_level6 = State()
    menu_driver_level7 = State()
    menu_driver_level8 = State()

    def __init__(self):
        self.__message = None
        self.__id = None

    async def main_menu_driver(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            await state.set_data(data={"lang": data.get('lang')})
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=Text_lang.menu.main_menu,
                                   reply_markup=await reply.start_driver())
            await self.menu_driver_level1.set()

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
                                   reply_markup=await reply.start_driver())

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
            form = FormMenuDriver(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=await form.about_us(),
                                   disable_web_page_preview=False)

    @staticmethod
    async def menu_how_to_use(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            form = FormMenuDriver(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=await form.how_to_use(),
                                   disable_web_page_preview=False)

    @staticmethod
    async def menu_feedback(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            await bot.send_message(chat_id=message.from_user.id, text=Text_lang.feedback.feedback)

    @staticmethod
    async def menu_change(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            await state.set_data(data={"lang": data.get('lang')})
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
            await bot.send_message(chat_id=message.from_user.id, text=Text_lang.questions.driver.change,
                                   reply_markup=await reply.change())

    async def menu_online(self, message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        self.__id = message.from_user.id
        async with state.proxy() as self.__data:
            await state.set_data(data={"lang": self.__data.get('lang')})
            await self._route_exist()
            await self._wallet_check()
            reply = Reply(language=self.__data.get('lang'))
            print('online', self.__data)
            if isinstance(message, types.Message):
                if self.__condition is True:
                    self.__data['row_id'] = await pg.insert_analise_driver(driver_id=self.__id)
                    await bot.send_message(chat_id=message.from_user.id, text=self.__Text_lang.menu.online,
                                           reply_markup=await reply.main_menu())
                    await bot.send_message(chat_id=message.from_user.id, reply_markup=self.__markup, text=self.__text)
                else:
                    await bot.send_message(chat_id=message.from_user.id, text=self.__Text_lang.alert.wallet,
                                           reply_markup=await reply.main_menu())
            elif isinstance(message, types.CallbackQuery):
                with suppress(MessageToDeleteNotFound):
                    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
                await bot.send_message(chat_id=message.from_user.id, text=self.__Text_lang.menu.online,
                                       reply_markup=await reply.main_menu())
                with suppress(MessageToDeleteNotFound):
                    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id - 1)
                await bot.send_message(chat_id=message.from_user.id, reply_markup=self.__markup, text=self.__text)
                await message.answer()
            await Driver.driver_level1.set()

    async def _route_exist(self):
        exist = await pg.route_exist(driver_id=self.__id)
        self.__Text_lang = Txt.language[self.__data.get('lang')]
        inline = InlineDriver(language=self.__data.get('lang'), condition=False)
        if exist is False:
            self.__data.pop("from_town")
            self.__data.pop("from_town_value")
            question = self.__Text_lang.questions.driver.from_town
            form = FormDriver(data=self.__data, question=question)
            self.__text = await form.main_text()
            self.__markup = await inline.menu_towns()
        elif exist is True:
            form = FormDriverCancel(language=self.__data.get('lang'), driver_id=self.__id)
            self.__text = await form.order()
            self.__markup = await inline.menu_route_cancel()

    async def _wallet_check(self):
        wallet = await pg.select_all_wallet(driver_id=self.__id)
        self.__condition = bool(wallet > Txt.money.wallet.tax)

    @staticmethod
    async def menu_active_order(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            data['driver_id'] = message.from_user.id
            reply = Reply(language=data.get('lang'))
        await bot.send_message(chat_id=message.from_user.id, text=Text_lang.menu.order,
                               reply_markup=await reply.main_menu())
        await active.active_order_check(data=data)
        await ActiveOrderDriver.active_order_driver.set()

    @staticmethod
    async def menu_on_spot(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            Text_lang = Txt.language[data.get('lang')]
            data['driver_id'] = message.from_user.id
            reply = Reply(language=data.get('lang'))
        await bot.send_message(chat_id=message.from_user.id, text=Text_lang.menu.spot,
                               reply_markup=await reply.main_menu())
        await on_spot.on_spot_check(data=data)
        await OnSpotDriver.on_spot_driver.set()

    @staticmethod
    async def menu_personal_cabinet(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
        async with state.proxy() as data:
            await state.set_data(data={"lang": data.get('lang')})
            Text_lang = Txt.language[data.get('lang')]
            reply = Reply(language=data.get('lang'))
        if isinstance(message, types.Message):
            await bot.send_message(chat_id=message.from_user.id, text=Text_lang.menu.personal_cabinet,
                                   reply_markup=await reply.personal_cabinet())
        elif isinstance(message, types.CallbackQuery):
            with suppress(MessageToDeleteNotFound):
                await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
            await bot.send_message(chat_id=message.from_user.id, text=Text_lang.menu.personal_cabinet,
                                   reply_markup=await reply.personal_cabinet())
        await PersonalCabinet.personal_cabinet.set()

    def register_handlers_driver_menu(self, dp: Dispatcher):
        dp.register_message_handler(self.menu_change, text=Txt.menu.change,                                             state=self.menu_driver_level1)
        dp.register_message_handler(self.main_menu_driver, text=Txt.menu.main_menu, state=[*Driver.states_names] +
                                                                                          [*MenuDriver.states_names] +
                                                                                          [*ActiveOrderDriver.states_names] +
                                                                                          [*PersonalCabinet.states_names] +
                                                                                          [*OnSpotDriver.states_names])

        dp.register_message_handler(self.main_menu_driver, text=Txt.option.no,                                          state=self.menu_driver_level1)
        dp.register_message_handler(self.menu_setting, text=Txt.menu.settings,                                          state=[*MenuDriver.states_names])
        dp.register_message_handler(self.menu_change_language, text=Txt.settings.language,                              state=self.menu_driver_level1)

        dp.register_message_handler(self.menu_information, text=Txt.menu.information,                                   state=[*MenuDriver.states_names])
        dp.register_message_handler(self.menu_about_us, text=Txt.information.about_us,                                  state=[*MenuDriver.states_names])
        dp.register_message_handler(self.menu_how_to_use, text=Txt.information.how_to_use,                              state=[*MenuDriver.states_names])
        dp.register_message_handler(self.menu_feedback, text=Txt.information.feedback,                                  state=[*MenuDriver.states_names])

        # переход в ветку на линиии
        dp.register_message_handler(self.menu_online, text=Txt.menu.online,                                             state=self.menu_driver_level1)
        dp.register_callback_query_handler(self.menu_online, text='back',                                               state=[Driver.driver_level2,
                                                                                                                               Driver.route_cancel])
        # # переход в ветку активные заказы
        dp.register_message_handler(self.menu_active_order, text=Txt.menu.order,                                        state=self.menu_driver_level1)

        # # переход в ветку я на месте
        dp.register_message_handler(self.menu_on_spot, text=Txt.menu.spot,                                              state=self.menu_driver_level1)

        # переход в ветку ЛК
        dp.register_message_handler(self.menu_personal_cabinet, text=Txt.menu.personal_cabinet,                         state=self.menu_driver_level1)
        dp.register_callback_query_handler(self.menu_personal_cabinet, text='back',                                     state=[PersonalCabinet.wallet_level1,
                                                                                                                               PersonalCabinet.change_data])

