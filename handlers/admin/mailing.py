import asyncio
import random
from contextlib import suppress

from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import BotBlocked, Unauthorized, MessageNotModified

from config import bot
from config import dp, scheduler
from keyboards.inline.admin import InlineAdmin
from pgsql import pg
from text.admin.mailing import FormAdmin
from text.language.main import Text_main

Txt = Text_main()
form = FormAdmin()
inline = InlineAdmin()


async def left_5_days(dp: Dispatcher):
    drivers = await pg.time_reminder(days=5)
    for driver_id, wallet, date, language in drivers:
        text = await form.left_days(language=language, days=5, wallet=wallet, date=date)
        try:
            await bot.send_message(chat_id=driver_id, text=text)
        except BotBlocked:
            await pg.block_status(user_id=driver_id, status=False)


async def left_1_days(dp: Dispatcher):
    drivers = await pg.time_reminder(days=1)
    for driver_id, wallet, date, language in drivers:
        text = await form.left_days(language=language, days=1, wallet=wallet, date=date)
        try:
            await bot.send_message(chat_id=driver_id, text=text)
        except BotBlocked:
            await pg.block_status(user_id=driver_id, status=False)


async def bonus_end(dp: Dispatcher):
    await pg.bonus_end()


async def every_day_client(dp: Dispatcher):
    users = await pg.every_day_client()
    num = random.randint(15, 30)
    for user_id in users:
        # language = await pg.select_language(user_id=user_id[0])
        # text = await form.every_day_client(language=language, num=num)
        text = await form.client(num=num)
        try:
            await bot.send_message(chat_id=user_id[0], text=text)
            await asyncio.sleep(delay=0.05)
        except BotBlocked:
            await pg.block_status(user_id=user_id[0], status=False)


async def every_day_driver(dp: Dispatcher):
    users = await pg.every_day_driver()
    num = random.randint(50, 150)
    for user_id in users:
        # language = await pg.select_language(user_id=user_id[0])
        # text = await form.every_day_driver(language=language, num=num)
        text = await form.driver(num=num)
        try:
            await bot.send_message(chat_id=user_id[0], text=text)
            await asyncio.sleep(delay=0.05)
        except BotBlocked:
            await pg.block_status(user_id=user_id[0], status=False)


scheduler.add_job(left_5_days, 'cron', day_of_week='mon-sun', hour=10, minute=00, args=(dp,))
scheduler.add_job(left_1_days, 'cron', day_of_week='mon-sun', hour=10, minute=00, args=(dp,))
scheduler.add_job(bonus_end, 'cron', day_of_week='mon-sun', hour=00, minute=00, args=(dp,))

scheduler.add_job(every_day_client, 'cron', day_of_week='mon', hour=23, minute=2, args=(dp,))
scheduler.add_job(every_day_driver, 'cron', day_of_week='mon', hour=23, minute=2, args=(dp,))

scheduler.add_job(every_day_client, 'cron', day_of_week='fri', hour=7, minute=00, args=(dp,))
scheduler.add_job(every_day_driver, 'cron', day_of_week='fri', hour=7, minute=00, args=(dp,))

scheduler.add_job(every_day_client, 'cron', day_of_week='wed', hour=16, minute=00, args=(dp,))
scheduler.add_job(every_day_driver, 'cron', day_of_week='wed', hour=16, minute=00, args=(dp,))


class Mailing(StatesGroup):
    mailing_level1 = State()
    mailing_level2 = State()
    mailing_level3 = State()

    async def menu_choose(self, call: types.CallbackQuery, state: FSMContext):
        # print('2', await state.get_state())
        await self.next()
        async with state.proxy() as data:
            data["type"] = call.data.split('_')[1]
        text = await form.mailing_choose(users=data.get("type"))
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text)

    async def menu_check(self, message: types.Message, state: FSMContext):
        await self.next()
        async with state.proxy() as data:
            data["message_id"] = message.message_id
        await bot.copy_message(chat_id=message.from_user.id, message_id=message.message_id,
                               from_chat_id=message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id, text="Все верно?",
                               reply_markup=await inline.menu_send())

    async def menu_send(self, call: types.CallbackQuery, state: FSMContext):
        self.__call = call
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Рассылка началась')
        async with state.proxy() as self.__data:
            await self._mail_send()

    async def _mail_send(self):
        users = await pg.get_users(users=self.__data.get('type'))
        index = 0
        for user in users:
            try:
                await bot.copy_message(chat_id=[*user][0], message_id=self.__data.get("message_id"),
                                       from_chat_id=self.__call.from_user.id)
                await asyncio.sleep(delay=0.05)
                index += 1
                if index % 100 == 0:
                    with suppress(MessageNotModified):
                        await bot.edit_message_text(chat_id=self.__call.from_user.id,
                                                    message_id=self.__call.message.message_id,
                                                    text=f'Разослано {index} пользователям')
            except (BotBlocked, Unauthorized):
                await pg.block_status(user_id=[*user][0], status=False)
        else:
            await bot.delete_message(chat_id=self.__call.from_user.id, message_id=self.__call.message.message_id)
            await bot.send_message(chat_id=self.__call.from_user.id,
                                   text=await form.mail_end(users=self.__data.get('type')))

    async def menu_cancel(self, call: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.from_user.id, text="Рассылка отменена")

    def register_handlers_mailing(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_choose, lambda x: x.data and x.data.startswith("mail"), state=self.mailing_level1)
        dp.register_message_handler(self.menu_check, content_types=["text", "photo", "video"], state=self.mailing_level2)
        dp.register_callback_query_handler(self.menu_send, text="yes", state=self.mailing_level3)
        dp.register_callback_query_handler(self.menu_cancel, text="cancel", state=self.mailing_level3)



