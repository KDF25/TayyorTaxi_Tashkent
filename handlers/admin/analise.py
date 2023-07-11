from contextlib import suppress

from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified

from config import bot
from config import dp
from handlers.admin.is_admin import IsAdmin, IsAdminOur
from handlers.admin.mailing import Mailing
from keyboards.inline.admin import InlineAdmin
from keyboards.reply.user import Reply
from text.admin.analise import FormAnalise
from text.language.main import Text_main

form = FormAnalise()
inline = InlineAdmin()
Txt = Text_main()
chat_id = -740338582
reply = Reply(language='rus')


class Analise(StatesGroup):

    analise_level1 = State()
    analise_level2 = State()
    analise_level3 = State()

    async def send_analise_type(self, call: types.CallbackQuery, state: FSMContext):
        print(call.data)
        await self.analise_level2.set()
        async with state.proxy() as data:
            data['type'] = call.data.split('_')[1]
        with suppress(MessageNotModified):
            await bot.edit_message_text(chat_id=call.from_user.id, text="За какое время?",
                                        message_id=call.message.message_id,
                                        reply_markup=await inline.menu_analise_timeframe())
            await call.answer()

    async def send_analise_timeframe(self, call: types.CallbackQuery, state: FSMContext):
        print(call.data)
        async with state.proxy() as data:
            data['timeframe'] = call.data.split('_')[1]
        with suppress(MessageNotModified):
            await bot.edit_message_text(chat_id=call.from_user.id, text=await form.analise(data=data),
                                        message_id=call.message.message_id)
            await call.answer()

    def register_handlers_analise(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.send_analise_type, IsAdminOur(), lambda x: x.data.startswith("analise"),
                                           state=self.analise_level1)
        dp.register_callback_query_handler(self.send_analise_timeframe, IsAdminOur(),
                                           lambda x: x.data.startswith("day"), state=self.analise_level2)


