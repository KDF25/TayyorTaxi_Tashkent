class Ru_language:

    class start:
        main = "Добро пожаловать в телеграм-бот <b>TayyorTaxi | Toshkent-Toshkent viloyati</b> \n\n" \
               "Жмите <b>«🚖 Найти водителя»</b> и находите водителей по своему маршруту!"
        start = "Добро пожаловать!"

    class menu:
        passenger = "🚖 Найти водителя"
        spot = "📍 Я на месте"
        information = "ℹ Информация"
        order = "🗓 Активные заказы"
        driver = "🙋 Я водитель"
        settings = "⚙ Настройки"
        main_menu = "🏠 Главное меню"
        online = "🚕 Нужны пассажиры"
        personal_cabinet = "🔑 Личный кабинет"
        change = "🔄 Стать пассажиром"

    class information:
        about_us = "ℹ О сервисе"
        how_to_use = "❓ Как использовать"
        feedback = "☎ Обратная связь"
        rules = "Правила сервиса"

    class feedback:
        feedback = "Связаться с нами вы можете по следующим контактам👇\n\n" \
                   "Телеграм: @tayyortaxitosh_aloqabot"

    class symbol:
        sum = 'сум'

    class url:
        class client:
            about_us = "https://telegra.ph/O-servise-10-13"
            how_to_use = "https://telegra.ph/Kak-ispolzovat-10-13"

        class driver:
            how_to_use = "https://telegra.ph/Kak-ispolzovat-10-13-2"
            about_us = "https://telegra.ph/O-servise-10-13-2"
            rules = "https://telegra.ph/Pravila-servisa-10-13"

    class buttons:

        class common:
            back = "⬅Назад"
            cont = "➡Продолжить"
            location = "📍 Моё местоположение"
            order = "✅Заказать"
            phone = "📱Мой номер"
            agree = "✅Подтвердить"
            yes = "✅Верно"
            da = "✅Да"
            no = "❌Нет"
            on_spot = "✅Да, я на месте"

        class passenger:
            choose_more = "➡Выбрать еще"
            location = "📍 Место выезда водителя"

        class driver:
            route_cancel = "❌Отменить активность"
            location = "📍 Место выезда"
            accept = "✅Принять"
            reject = "❌Отклонить"

        class cancel:
            client = "❌Отменить заказ"
            driver = "❌Отменить поездку"
            driver_ok = "❌Все равно отменить"

        class personal_cabinet:
            class data:
                data = "✍Мои данные"
                name = "Изменить имя"
                phone = "Изменить номер"
                car = "Изменить авто"
                model = "Изменить модель"
                number = "Изменить гос.номер"
                color = "Изменить цвет"

            class wallet:
                wallet = "💳Кошелёк"
                balance = "Пополнить баланс"
                payme = "Payme"
                click = "Click"
                paynet = "Paynet"
                pay = "✅Оплатить"

    class questions:

        class passenger:
            from_town = "Откуда вы поедете? 👇"
            location = "📍 Отправьте вашу локацию, мы подберём водителей с ближайшими точками выезда👇"
            from_spot = "🅿️ Выберите место выезда 👇"
            to_town = "Куда вы поедете? 👇"
            to_spot = "🅿️ Выберите место прибытия 👇"
            places = "Укажите количество пассажиров 👇"
            phone = f'Отправьте номер для связи 👇\n\n' \
                    f'Можно нажать <b>«Мой номер»</b> или ввести вручную по шаблону: +998 ** *** ** **'
            auto = "Выберите модель авто 👇"
            car = "Выберите из нижеследующих 👇"

            drivers_rate = "⭐️Как прошла поездка? Пожалуйста, оцените водителя, это поможет " \
                           "сделать наш сервис лучше для клиентов."

        class driver:
            from_town = "Откуда вы поедете 👇"
            location = "📍 Откуда выезжаете? Отправьте локацию 👇"
            from_spot = "🅿️ Выберите место выезда 👇"
            to_town = "Куда вы направляетесь? 👇"
            to_spot = "🅿️ Выберите место прибытия 👇"
            price = "Укажите цену за 💺1 пассажира 👇"
            places = "Укажите количество свободных мест 👇"
            time = "⏰ Укажите время выезда 👇\n\n" \
                   "<i>❗ Можно указать только ближайшие <b>12 часов</b> </i>"
            accept = "✅ Ваша заявка принята. Как только клиенты откликнутся, вы получите уведомление.\n\n" \
                     "⚠️Чтобы перестать быть активным для клиентов или поменять параметры маршрута, " \
                     "перейдите во вкладку <b>«🚕 Нужны пассажиры»</b>"
            change = "Вы уверены, что хотите перейти в клиентскую часть?\n\nВаши данные будут сохранены за вами"
            sure = "Вы уверены, что хотите отменить вашу активность? " \
                   "Вы больше не будете получать новые заказы по данному маршруту."

        class registration:
            name = "Чтобы стать водителем нужно пройти небольшую регистрацию, после чего вы станете " \
                   "активным и получите бонусные 💵 <b>50 000</b> сум\n\n" \
                   "Для начала введите ваше имя 👇\n\n" \
                   "<i>Его будут видеть клиенты</i>"
            auto = "Выберите модель вашего авто 👇"
            number = "<b>Введите гос.номер машины без пробелов в формате:</b>\n\n" \
                     "01A123BC\n" \
                     "01123ABC\n" \
                     "01H123456\n\n" \
                     "⚠️Информация не передается за пределами данного сервиса и служит " \
                     "только для облегчения встречи водителя с пассажиром"
            color = "Выберите цвет вашего авто 👇"
            phone = f'Отправьте номер для связи с клиентами 👇\n\n' \
                    f'Можно нажать <b>«Мой номер»</b> или ввести вручную по шаблону: +998 ** *** ** **'
            agreement = 'Все верно? 👇\n\nНажимая кнопку <b>«✅Верно»</b>, вы подтверждаете, ' \
                        'что ознакомились и согласились с правилами сервиса - 👉'
            rules = "Правила сервиса"
            how_to_use = "Как использовать"

    class personal_cabinet:
        name = "Имя"
        phone = "Номер"
        car = "Авто"
        id = "ID"
        wallet = "Баланс"
        common = "Основной"
        bonus = "Бонусный"
        congratulation = "Поздравляем! Мы начислили вам бонусные 💵 <b>50 000</b> сум за регистрацию в сервисе\n\n" \
                         "<b>❕Время использования бонуса - 20 дней</b>\n\n" \
                         "Для начала ознакомьтесь 👇"
        online = "Чтобы начать принимать заказы клиентов, нажмите <b>«🚕 Нужны пассажиры»</b> 👇"

    class chain:
        class passenger:
            from_place = "Откуда"
            to_place = "Куда"
            num = "Пассажиры"
            distance = "📍 От вас"

            car_find1 = "Для вас было подобрано "
            car_find2 = "машин"
            car_not_found = "К сожалению машин по этому маршруту на данный момент не найдено, попробуйте позже"
            car_not_found2 = "К сожалению машин по этому маршруту на данный момент не найдено\n\n" \
                            "<b>🅿️ Есть водители в ближайших к вам точках выезда</b> 👇"

            driver = "Водитель"
            car = "Модель"
            places = "Свободно мест"
            price = "Цена за 1 пассажира"
            info = "Ваши данные"
            phone = "Телефон"
            time = "Выезд в"
            cost = "Всего за"
            passenger = "пассажира"

        class driver:
            from_place = "Откуда"
            to_place = "Куда"
            places = "Свободно мест"
            price = "Цена за 1️⃣ пассажира"
            price2 = "1 пассажир"
            time = "Выезд в"
            alright = "Все верно?"
            onepass = '1 пас.'
            name = "Имя"
            phone = "Телефон"
            info = "Данные клиента"
            spot = "📍 Ваше место выезда"
            car = "Модель"
            cost = "Всего за"
            passenger = "пассажира"

        class personal_cabinet:
            change_name = "Изменить имя"
            change_phone = "Изменить номер"
            change_car = "Изменить авто"
            change_param = {'name': change_name, 'phone': change_phone, "car": change_car}
            new_data = "Введите новые данные 👇"
            new_data_rec = "Данные успешно обновлены."
            payment = "Укажите сумму пополнения 👇"
            pay_way = "Выберите способ оплаты 👇"
            amount = "Сумма пополнения"

            pay_way2 = "Оплата через "
            amount2 = "Сумма к оплате"
            payment2 = '<i>Чтобы произвести оплату нажмите на кнопку</i> <b>«✅Оплатить»</b> 👇'
            accept = '✅Оплата подтверждена\n\nНа баланс зачислено'

    class order:
        active_orders = '<i>Следить за статусом заказа вы можете во вкладке <b>«🗓 Активные заказы»</b></i>'

        class client:
            passenger = f"Запрос отправлен водителю, как только он" \
                        f"будет подтвержден, вы получите уведомление\n\n" \
                        f"<b>Вы можете отправить заявку сразу нескольким водителям, " \
                        f"а поездка будет с тем, кто примет её первым.\n\n</b>" \
                        f"Выбрать еще водителей?"
            accept = "✅Заявка принята водителем"
            reject = 'Заявка отклонена'
            info = "Ваши данные"

        class driver:
            driver = f'Ваша заявка принята. Как только клиенты откликнутся, вы получите уведомление.\n\n' \
                     f'<i>За статусом заказов вы можете следить во вкладке <b>«🗓 Активные заказы»</b></i> 👇'
            route_cancel = "❌Активность отменена, клиенты больше не будут видеть вас в списке водителей.\n\n" \
                           "❕Чтобы снова стать активным для клиентов перейдите во вкладку <b>«🚕 На линии»</b>"
            order = 'Чтобы получить заказ и данные клиента нажмите <b>«✅Принять»</b>.'
            order_cost1 = 'Стоимость услуги'
            order_cost2 = 'сум средства будут списаны с вашего кошелька.'
            accept = "✅ Заявка принята, мы уведомили пассажира о принятии заказа"
            reject = '❌ Заказ отклонён'
            info = "Данные пассажира"
            phone_client = "Телефон"
            new_order = "⚡ Есть пассажир!"

    class cancel:
        class client:
            question_order = "Вы уверены, что хотите отменить заказ? Это действие необратимое."
            order = "❌Заказ отменен"
            delete = "❌ К сожалению, водитель отменил поездку"
            cancel = "❌ Запрос был отклонен водителем"
            new_driver = "Вы можете выбрать другого водителя 👇"

        class driver:
            passenger = '❌Пассажир отменил поездку, средства возвращены на ваш кошелек'
            driver = "Вы уверены? Средства не вернутся на ваш счет если заказ отменен водителем"
            order = "❌Заказ отменен"

    class alert:
        wallet = "<b>⚠️У вас недостаточно средств на балансе чтобы стать активным!</b>\n\n " \
                 "Пополните кошелек:\n\n " \
                 "🔑 Личный кабинет --> 💳 Кошелёк --> Пополнить баланс"

        class phone:
            alert = "Давайте попробуем еще раз 😅"

        class driver:
            accept_order_late = "❌ Заявка была отклонена по причине принятия заявки другим водителем " \
                                "либо из-за долгого ответа на заявку вами"
            places_error = "❗ У вас недостаточно мест в салоне"
            places_full = "Машина заполнена, мы разослали уведомления пассажирам"
            insufficient_funds = "У вас недостаточно средств в кошельке, пополните баланс." \
                                 "🔑Личный кабинет --> 💳Кошелёк --> Пополните баланс"
            insufficient_funds2 = "<b>⚠️Напоминаем!</b>\n\nУ вас недостаточно средств в кошельке " \
                                  "чтобы принять следующий заказ, пополните баланс чтобы стать активным\n\n" \
                                  "🔑 Личный кабинет --> 💳 Кошелёк --> Пополнить баланс"

    class car:
        car = {1: 'Cobalt', 2: 'Gentra', 3: 'Lacetti', 4: 'Nexia 1', 5: 'Nexia 2',
               6: 'Nexia 3', 7: 'Malibu 1', 8: 'Captiva', 9: 'Malibu 2', 10: 'Matiz',
               11: 'Spark', 12: 'Epica', 13: 'Damas', 14: 'Lada', 15: 'Иномарка'}
        color = {1: 'Белый', 2: 'Черный', 3: 'Серебристый', 4: 'Темно-серый', 5: 'Молочный', 6: 'Вишневый',
                 7: 'Желтый', 8: 'Красный', 9: 'Зеленый', 10: 'Синий', 11: 'Голубой'}

    class active_order:
        no_active_order = "На данный момент у вас нет активных заказов"

    class rate:
        rate_5 = "😄 Спасибо за оценку, рады что вам все понравилось!"
        rate_4 = "😄 Спасибо за оценку, мы рады что все прошло хорошо! Будем стараться лучше."
        rate_3 = "😕 Спасибо за оценку, жаль что водитель не оправдал ваших ожиданий, надеемся что следующая поездка " \
                 "оставит только положительные эмоции."
        rate_2 = "😐 Спасибо за оценку, жаль что водитель не оправдал ваших ожиданий, мы снизим его активность на " \
                 "некоторое время."
        rate_1 = "😞 Спасибо за оценку, жаль что водитель не оправдал ваших ожиданий, мы снизим его активность до " \
                 "выяснения обстоятельств, после чего возможно заблокируем данного водителя в нашем сервисе."
        rate_dict = {1: rate_1, 2: rate_2, 3: rate_3, 4: rate_4, 5: rate_5}

    class on_spot:
        common = "❗ Нажмите <b>«📍 Я на месте»</b> когда будете в указанной точке"
        client = "📍 Пассажир на месте 👇"
        driver = "📍 Водитель на месте👇"
        on_spot = "📍 Место выезда 👆"
        inform_driver = "✅ Мы уведомили водителя"
        inform_client = "✅ Мы уведомили клиента"
        time = "Выезд в"
        info = "Данные клиентов"
        passenger = "Пассажир"
        phone = "Телефон"
        places = "Пассажиры"

    class option:
        yes = "Есть"
        no = "Нет"
        da = "Да"
        option = {0: no, 1:yes}

    class quiz:
        main = "На данный момент оплата через Paynet не подключена.\n\n" \
               "<b>Вам будет удобнее пополнять кошелёк через Paynet?</b>👇"
        thanks = "Спасибо за информацию, в скором времени добавим данный метод оплаты."
        yes = "✅ Да, удобнее"

    class reminder:
        client1 = "📣 Свыше"
        client2 = "водителей собираются сегодня ехать по вашему направлению. " \
                "Успейте найти подходящего именно для вашей поездки! 👇"
        driver1 = "📣 Свыше"
        driver2 = "пассажиров собираются сегодня ехать по вашему направлению. " \
                  "Успейте стать активным, чтобы найти подходящих именно для вас! \n\n" \
                  "Жмите <b>«🚕 Нужны пассажиры»</b> чтобы стать активным 👇"
