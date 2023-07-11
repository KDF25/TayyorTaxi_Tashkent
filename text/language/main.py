from text.language.ru import Ru_language
from text.language.uzb import Uzb_language
# from text.language.ENG import ENG_language

RU = Ru_language()
UZB = Uzb_language()
ENG = Ru_language()


class Text_main:

    choose_language = f"🇺🇿 Tilni tanlang 👇\n" \
                      f"🇷🇺 Выберите язык 👇\n" \
                      f"🇺🇸 Choose language 👇\n"

    language = {"rus": RU, "uzb": UZB, "eng": ENG}

    class menu:
        passenger = [RU.menu.passenger, UZB.menu.passenger, ENG.menu.passenger]
        spot = [RU.menu.spot, UZB.menu.spot, ENG.menu.spot]
        information = [RU.menu.information, UZB.menu.information, ENG.menu.information]
        order = [RU.menu.order, UZB.menu.order, ENG.menu.order]
        driver = [RU.menu.driver, UZB.menu.driver, ENG.menu.driver]
        settings = [RU.menu.settings, UZB.menu.settings, ENG.menu.settings]
        main_menu = [RU.menu.main_menu, UZB.menu.main_menu, ENG.menu.main_menu]
        online = [RU.menu.online, UZB.menu.online, ENG.menu.online]
        personal_cabinet = [RU.menu.personal_cabinet, UZB.menu.personal_cabinet, ENG.menu.personal_cabinet]
        change = [RU.menu.change, UZB.menu.change, ENG.menu.change]

    class information:
        about_us = [RU.information.about_us, UZB.information.about_us, ENG.information.about_us]
        how_to_use = [RU.information.how_to_use, UZB.information.how_to_use, ENG.information.how_to_use]
        feedback = [RU.information.feedback, UZB.information.feedback, ENG.information.feedback]

    class personal_cabinet:
        data = [RU.buttons.personal_cabinet.data.data, UZB.buttons.personal_cabinet.data.data,
                ENG.buttons.personal_cabinet.data.data]
        wallet = [RU.buttons.personal_cabinet.wallet.wallet, UZB.buttons.personal_cabinet.wallet.wallet,
                  ENG.buttons.personal_cabinet.wallet.wallet]

    class settings:
        rus = "🇷🇺 Ru"
        uzb = "🇺🇿 O’z"
        eng = "🇺🇸 Eng"
        language = [rus, uzb, eng]

    class option:
        da = [RU.buttons.common.da, UZB.buttons.common.da, ENG.buttons.common.da]
        no = [RU.buttons.common.no, UZB.buttons.common.no, ENG.buttons.common.no]

    class places:
        places = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        places_dict = {0: '0️⃣', 1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4:  '4️⃣'}

    class money:
        class driver:
            price = [5000, 7000, 9000, 10000, 12000, 15000, 17000, 20000, 23000,
                     25000, 30000, 35000, 40000, 50000, 60000]

        class wallet:
            tax = 1000
            wallet = 50000
            price = [1000, 3000, 5000, 10000, 20000, 40000, 50000, 70000]

    class Admin:
        menu = 'Меню Администратора'

        class buttons:
            stata = "Статистика"
            analise = "Анализ"

    class reminder:
        driver = "⏰ Напоминаем, чтобы снова стать активным, нажмите «🚕 Нужны пассажиры»\n\n" \
                 "⏰ Eslatib oʻtamiz, yana faol boʻlish uchun «🚕 Yoʻlovchilar kerak» tugmasini bosing."


