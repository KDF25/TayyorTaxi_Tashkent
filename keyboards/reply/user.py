from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from text.language.main import Text_main

Txt = Text_main()


class Reply:
    def __init__(self, language: str):
        self.__language = language
        self.__Text_lang = Txt.language[language]
        self.__main_menu = KeyboardButton(text=self.__Text_lang.menu.main_menu)

    async def start_client(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        b1 = KeyboardButton(text=self.__Text_lang.menu.passenger)
        b2 = KeyboardButton(text=self.__Text_lang.menu.spot)
        b3 = KeyboardButton(text=self.__Text_lang.menu.information)
        b4 = KeyboardButton(text=self.__Text_lang.menu.order)
        b5 = KeyboardButton(text=self.__Text_lang.menu.driver)
        b6 = KeyboardButton(text=self.__Text_lang.menu.settings)
        markup.add(b1, b2, b3, b4, b5, b6)
        return markup

    async def main_menu(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(self.__main_menu)
        return markup

    async def start_driver(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        b = KeyboardButton(text=self.__Text_lang.menu.spot)
        b1 = KeyboardButton(text=self.__Text_lang.menu.online)
        b2 = KeyboardButton(text=self.__Text_lang.menu.order)
        b3 = KeyboardButton(text=self.__Text_lang.menu.personal_cabinet)
        b4 = KeyboardButton(text=self.__Text_lang.menu.information)
        b5 = KeyboardButton(text=self.__Text_lang.menu.settings)
        b6 = KeyboardButton(text=self.__Text_lang.menu.change)
        markup.add(b, b1).add(b2, b3, b4, b5).add(b6)
        return markup

    async def setting(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        b1 = KeyboardButton(text=Txt.settings.ozb)
        b2 = KeyboardButton(text=Txt.settings.rus)
        b3 = KeyboardButton(text=Txt.settings.uzb)
        markup.add(b1, b2, b3).add(self.__main_menu)
        return markup

    async def information(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        b1 = KeyboardButton(text=self.__Text_lang.information.about_us)
        b2 = KeyboardButton(text=self.__Text_lang.information.how_to_use)
        b3 = KeyboardButton(text=self.__Text_lang.information.feedback)
        markup.add(b1, b2).add(b3).add(self.__main_menu)
        return markup

    async def share_phone(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        b1 = KeyboardButton(text=self.__Text_lang.buttons.common.phone, request_contact=True)
        markup.add(b1, self.__main_menu)
        return markup

    async def share_location(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        b1 = KeyboardButton(text=self.__Text_lang.buttons.common.location, request_location=True)
        markup.add(b1, self.__main_menu)
        return markup

    async def change(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        b1 = KeyboardButton(text=self.__Text_lang.buttons.common.da)
        b2 = KeyboardButton(text=self.__Text_lang.buttons.common.no)
        markup.add(b1, b2, self.__main_menu)
        return markup

    async def personal_cabinet(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        b1 = KeyboardButton(text=self.__Text_lang.buttons.personal_cabinet.data.data)
        b2 = KeyboardButton(text=self.__Text_lang.buttons.personal_cabinet.wallet.wallet)
        markup.add(b1, b2, self.__main_menu)
        return markup

