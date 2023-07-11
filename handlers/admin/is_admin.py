from aiogram.dispatcher.filters import BoundFilter
from config import bot
from aiogram import types
import typing

chat_id = -1001767085919


class IsAdmin(BoundFilter):
    async def check(self, message: typing.Union[types.Message, types.CallbackQuery]):
        status = (await bot.get_chat_member(user_id=message.from_user.id, chat_id=chat_id)).status
        if status in ["creator", "administrator"]:
            return True


class IsAdminReverse(BoundFilter):
    async def check(self, message: typing.Union[types.Message, types.CallbackQuery]):
        status = (await bot.get_chat_member(user_id=message.from_user.id, chat_id=chat_id)).status
        if status in ["member", "restricted"]:
            return True


class IsAdminOur(BoundFilter):
    async def check(self, message: typing.Union[types.Message, types.CallbackQuery]):
        status = (await bot.get_chat_member(user_id=message.from_user.id, chat_id=chat_id )).status
        if status in ["creator", "administrator"]:
            return True

