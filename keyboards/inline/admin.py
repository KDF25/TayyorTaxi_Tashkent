from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from text.language.main import Text_main

Txt = Text_main()


class InlineAdmin:

    @staticmethod
    async def menu_admin():
        markup = InlineKeyboardMarkup(row_width=2)
        b_client = InlineKeyboardButton(text="Статистика", callback_data="statistics")
        b_driver = InlineKeyboardButton(text="Анализ", callback_data="analise")
        b_all = InlineKeyboardButton(text="Рассылка", callback_data="mail")
        markup.add(b_client, b_driver).add(b_all)
        return markup

    @staticmethod
    async def menu_mailing():
        markup = InlineKeyboardMarkup(row_width=2)
        b_client = InlineKeyboardButton(text="Клиенты", callback_data="mail_client")
        b_driver = InlineKeyboardButton(text="Водители", callback_data="mail_driver")
        b_all = InlineKeyboardButton(text="Все пользователи", callback_data="mail_all")
        markup.add(b_client, b_driver).add(b_all)
        return markup

    @staticmethod
    async def menu_send():
        markup = InlineKeyboardMarkup(row_width=1)
        b_yes = InlineKeyboardButton(text="✅ Да", callback_data="yes")
        b_cancel = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
        markup.add(b_yes, b_cancel)
        return markup

    @staticmethod
    async def menu_analise():
        markup = InlineKeyboardMarkup(row_width=2)
        b1 = InlineKeyboardButton(text="Такси", callback_data="analise_taxi")
        b2 = InlineKeyboardButton(text="На линии", callback_data="analise_online")
        markup.add(b1, b2)
        return markup

    @staticmethod
    async def menu_analise_timeframe():
        markup = InlineKeyboardMarkup(row_width=3)
        b1 = InlineKeyboardButton(text="1 день", callback_data="day_1")
        b2 = InlineKeyboardButton(text="7 дней", callback_data="day_7")
        b3 = InlineKeyboardButton(text="Месяц", callback_data="day_30")
        b4 = InlineKeyboardButton(text="Все время", callback_data="day_all")
        b5 = InlineKeyboardButton(text="⬅Назад", callback_data="back")
        markup.add(b1, b2, b3).add(b4).add(b5)
        return markup