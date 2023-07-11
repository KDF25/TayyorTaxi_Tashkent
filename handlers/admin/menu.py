from contextlib import suppress

from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageToDeleteNotFound

from config import bot
from config import dp
from handlers.admin.is_admin import IsAdmin
from handlers.admin.mailing import Mailing
from handlers.admin.analise import Analise
from keyboards.inline.admin import InlineAdmin
from keyboards.reply.user import Reply
from text.admin.mailing import FormAdmin
from text.language.main import Text_main

form = FormAdmin()
inline = InlineAdmin()
Txt = Text_main()
reply = Reply(language='rus')


class MenuAdmin(StatesGroup):
    menu_admin_level1 = State()

    async def start_admin(self, message: types.Message, state: FSMContext):
        await bot.send_message(chat_id=message.from_user.id, text="Администраторская",
                               reply_markup=await reply.main_menu())
        await bot.send_message(chat_id=message.from_user.id, text="Администраторская",
                               reply_markup=await inline.menu_admin())
        await self.menu_admin_level1.set()

    async def main_menu(self, message: types.Message, state: FSMContext):
        await bot.send_message(chat_id=message.from_user.id, text=Txt.Admin.menu,
                               reply_markup=await inline.menu_admin())
        await self.menu_admin_level1.set()
        print('mm', await state.get_state())

    async def send_statistics(self, call: types.CallbackQuery, state: FSMContext):
        await call.answer()
        with suppress(MessageToDeleteNotFound):
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.from_user.id, text=await form.mailing_st())
        await bot.send_message(chat_id=call.from_user.id, text=Txt.Admin.menu, reply_markup=await inline.menu_admin())

    @staticmethod
    async def menu_mailing(call: types.CallbackQuery, state: FSMContext):
        await Mailing.mailing_level1.set()
        await call.answer()
        await bot.edit_message_text(chat_id=call.from_user.id, text="Кому хотели бы разослать?",
                                    message_id=call.message.message_id, reply_markup=await inline.menu_mailing())
        print('1', await state.get_state())

    @staticmethod
    async def menu_analise(call: types.CallbackQuery, state: FSMContext):
        await Analise.analise_level1.set()
        await call.answer()
        await bot.edit_message_text(chat_id=call.from_user.id, text="Что будем анализировать?",
                                    message_id=call.message.message_id, reply_markup=await inline.menu_analise())
        print('123', await state.get_state())

    def register_handlers_menu_admin(self, dp: Dispatcher):
        dp.register_message_handler(self.start_admin, IsAdmin(), commands="admin", state='*')
        dp.register_message_handler(self.main_menu, IsAdmin(), text=Txt.Admin.menu, state=[*Mailing.states_names])
        dp.register_callback_query_handler(self.menu_mailing, IsAdmin(), text="mail", state=self.menu_admin_level1)
        dp.register_callback_query_handler(self.menu_analise, IsAdmin(), text="analise", state=self.menu_admin_level1)
        dp.register_callback_query_handler(self.menu_analise, IsAdmin(), text="back", state=Analise.analise_level2)
        dp.register_callback_query_handler(self.send_statistics, IsAdmin(), text="statistics", state=self.menu_admin_level1)


