class Ozb_language:

    class start:
        main = "<b>TayyorTaxi | Toshkent-Toshkent viloyati</b> botiga xush kelibsiz! \n\n" \
               "<b>«🚖 Haydovchi topish»</b> tugmasini bosing va sizga qulay haydovchilarni toping!"
        start = "Xush kelibsiz!"

    class menu:
        passenger = "🚖 Haydovchi topish"
        spot = "📍 Men joydaman"
        information = "ℹ Ma’lumot"
        order = "🗓 Faol buyurtmalarim"
        driver = "🙋 Men haydovchiman"
        settings = "⚙ Sozlamalar"
        main_menu = "🏠 Bosh sahifa"
        online = "🚕 Yo’lovchilar kerak"
        personal_cabinet = "🔑 Shaxsiy kabinet"
        change = "🔄 Yo’lovchi bo’lish"

    class information:
        about_us = "ℹ Xizmat haqida"
        how_to_use = "❓ Qanday foydalaniladi"
        feedback = "☎ Aloqa"
        rules = "Xizmat ko'rsatish qoidalari"

    class feedback:
        feedback = "Quyidagi kontaktlar orqali biz bilan bog'lanishingiz mumkin👇\n\n" \
                   "Telegram: @tayyortaxitoshkent_aloqabot"

    class symbol:
        sum = 'so’m'

    class url:
        class client:
            about_us = "https://telegra.ph/Xizmat-haqida-10-13"
            how_to_use = "https://telegra.ph/Qanday-foydalaniladi-10-13"

        class driver:
            how_to_use = "https://telegra.ph/Qanday-foydalaniladi-10-13-2"
            about_us = "https://telegra.ph/Xizmat-haqida-10-13-2"
            rules = "https://telegra.ph/Xizmat-korsatish-shartlari-10-13"

    class buttons:

        class common:
            back = "⬅Ortga"
            cont = "➡Davom etish"
            location = "📍 Mening joylashuvim"
            order = "✅Buyurtma berish"
            phone = "📱Mening raqamim"
            agree = "✅Tasdiqlash"
            yes = "✅To'g'ri"
            da = "✅Ha"
            no = "❌Yo'q"
            on_spot = "✅Ha, men shu yerdaman"

        class passenger:
            choose_more = "➡Yana tanlash"
            location = "📍 Haydovchi yo’lga chiqish joyi"

        class driver:
            route_cancel = "❌Bekor qilish"
            location = "📍 Jo’nash joyi"
            accept = "✅Qabul qilish"
            reject = "❌Rad etish"

        class cancel:
            client = "❌Buyurtmani bekor qilish"
            driver = "❌Bekor qilish"
            driver_ok = "❌Baribir bekor qilish"

        class personal_cabinet:
            class data:
                data = "✍Mening ma’lumotlarim"
                name = "Ismni o'zgartirish"
                phone = "Raqamni o'zgartirish"
                car = "Mashinani o’zgartirish"
                model = "Modelni o’zgartirish"
                number = "Davlat raqamini o’zgartirish"
                color = "Rangini o’zgartirish"

            class wallet:
                wallet = "💳Balans"
                balance = "Balansni to‘ldirish"
                payme = "Payme"
                click = "Click"
                paynet = "Paynet"
                pay = "✅To’lash"

    class questions:

        class passenger:
            from_town = "Qayerdan yo’lga chiqasiz? 👇"
            location = "📍 Joylashuvingizni yuboring, sizga eng yaqin bo’lgan haydovchilarni yo’lga chiqish joylarini topamiz👇"
            from_spot = "🅿️ Kelish joyini belgilang 👇"
            to_town = "Qayoqqa ketyapsiz? 👇"
            to_spot = "🅿️ Kelish joyini belgilang 👇"
            places = "Yo’lovchilar sonini belgilang 👇"
            phone = f"Telefon raqamingizni yuboring 👇\n\n" \
                    f"<b>«📱Mening raqamim»</b> tugmasini bosishingiz mumkin yoki " \
                    f"qo'lda kiritishingiz mumkin: +998** *** ** **"
            auto = "Avtomobil modelini tanlang 👇"
            car = "Quyidagilardan tanlang 👇"

            drivers_rate = "⭐️Safar qanday o'tdi? Iltimos haydovchiga baho bering. " \
                           "Xizmatni siz uchun yaxshiroq qilishga yo’rdam berasiz."

        class driver:
            from_town = "Qayerdan yo’lga chiqasiz? 👇"
            location = "📍 Qayerdan yo’lga chiqasiz? Joylashuvni belgilang 👇"
            from_spot = "🅿️ Kelish joyini belgilang 👇"
            to_town = "Qayoqqa ketyapsiz? 👇"
            to_spot = "🅿️ Kelish joyini belgilang 👇"
            price = "💺 Bir nafar yo’lovchi narxini belgilang 👇"
            places = "Bo’sh joy sonini belgilang 👇"
            time = "⏰ Jo’nash vaqtini belgilang 👇\n\n" \
                   "<i>❗ Faqat kevotgan <b>12 soat</b> ichidagi vaqtni belgilashingiz mumkin</i>"
            accept = "✅ Arizangiz qabul qilindi. Yo’lovchilar aloqaga chiqkanoq siz xabarnoma olasiz.\n\n" \
                     "⚠️Mijozlar uchun faol bo'lishni to'xtatish yoki marshrut parametrlarini o’zgartirish uchun " \
                     "<b>«🚕 Yo’lovchilar kerak»</b> tugmasini bosing"
            change = "Haqiqatan ham yo‘lovchi bo‘lmoqchimisiz?\n\nSizning ma'lumotlaringiz saqlanadi"
            sure = "Haqiqatan ham faoliyatingizni bekor qilmoqchimisiz? " \
                   "Bu marshrutda endi yangi buyurtmalarni olmaysiz."

        class registration:
            name = "Haydovchi bo'lish uchun siz kichik ro'yxatdan o'tishingiz kerak, undan keyin siz faol va " \
                   "<b>💵 50 000</b> so'm bonusga ega haydovchi bo'lasiz!\n\n " \
                   "Ismingizni kiriting 👇\n\n Uni yo’lovchilar korishadi"
            auto = "Avtomobilingiz modelini tanlang 👇"
            number = "<b>Avtomobilning davlat raqamini kiriting ushbu formatda:</b>\n\n" \
                     "01A123BC\n" \
                     "01123ABC\n" \
                     "01H123456\n\n" \
                     "⚠️Ma'lumot xizmatdan tashqari hech qayerga uzatilmaydi faqatgina haydovchi bilan " \
                     "yo'lovchini uchrashuvini osonlashtirish uchun kerak"
            color = "Mashinani rangini tanlang 👇"
            phone = f"Yo’lovchilar bilan ulanish uchun telefon raqamingizni jo’nating 👇\n\n" \
                    f"<b>«📱Mening raqamim»</b> tugmasini bosishingiz mumkin " \
                    f"yoki qo'lda kiritishingiz mumkin: +998 ** *** ** **"
            agreement = "Hammasi to'g'rimi? 👇\n\n<b>«✅To'g'ri»</b>, tugmasini bosish orqali siz xizmat ko'rsatish " \
                        "shartlari bilan tanishganingizni va roziligingizni tasdiqlaysiz - 👉"
            how_to_use = "Qanday foydalaniladi?"
            rules = "Xizmat ko'rsatish qoidalari"

    class personal_cabinet:
        name = "Ismingiz"
        phone = "Telefon"
        car = "Mashina"
        id = "ID"
        wallet = "Balans"
        common = "Asosiy"
        bonus = "Bonus"
        congratulation = "Tabriklaymiz! Xizmatda roʻyxatdan oʻtganingiz uchun sizga 💵 <b>50 000</b> soʻm bonus berildi\n\n" \
                         "<b>❕Bonusdan foydalanish muddati - 20 kun</b>\n\n" \
                         "Avval ma’lumotni ko’rib chiqing 👇"
        online = "Yo’lovchi buyurtmalarini qabul qilishni boshlash uchun «🚕 Yo’lovchilar kerak» tugmasini bosing👇"

    class chain:
        class passenger:
            from_place = "Qayerdan"
            to_place = "Qayoqqa"
            num = "Yo'lovchilar soni"
            distance = "📍 sizdan"

            car_find1 = "Siz uchun "
            car_find2 = "ta mashina mavjud"
            car_not_found = "Afsuski, bu yo'nalishdagi avtomobillar hozirda topilmadi, keyinroq qayta urinib ko'ring."
            car_not_found2 = "Afsuski, bu yo'nalishdagi avtomobillar hozirda topilmadi\n\n" \
                            "<b>🅿️ Sizga eng yaqin ketish nuqtalarda haydovchilar bor</b> 👇"

            driver = "Haydovchi"
            car = "Model"
            places = "Bo’sh joylar"
            price = "1 yo'lovchi uchun narx"
            info = "Sizning ma'lumotlaringiz"
            time = "Jo’nash vaqti"
            phone = "Telefon"
            cost = "Umumiy"
            passenger = "yo'lovchiga"

        class driver:
            from_place = "Qayerdan"
            to_place = "Qayoqqa"
            places = "Bo’sh joylar"
            price = "Umumiy 1️⃣ yo’lovchiga"
            price2 = "1 yo'lovchi"
            time = "Jo’nash vaqti"
            alright = "Hammasi to'g'rimi?"
            onepass = "1 yo'l."
            name = "Ismingiz"
            phone = "Telefon"
            info = "Yo’lovchini ma’lumotlari"
            spot = "📍 Sizning jo’nash joyingiz"
            car = "Mashina"
            cost = 'Umumiy'
            passenger = "yo'lovchiga"

        class personal_cabinet:
            change_name = "Ismni o'zgartirish"
            change_phone = "Raqamni o'zgartirish"
            change_car = "Mashinani o’zgartirish"
            change_param = {'name': change_name, 'phone': change_phone, "car": change_car}
            new_data = "Yangi ma’lumotni kiriting 👇"
            new_data_rec = "Ma’lumot o’zgartirildi."
            payment = "To'ldirish miqdorini belgilang 👇"
            pay_way = "To’lov turini tanlang 👇"
            amount = "To’lov miqdori"

            pay_way2 = "To’lov orqali"
            amount2 = "To’lov miqdori"
            payment2 = '<i>To’lov o’tqazish uchun </i> <b>«✅To’lash»</b> tugmasini bosing 👇'
            accept = '✅To’lov o’tqazildi\n\nBalansingizga kiritilgan miqdor'

    class order:
        active_orders = '<i>Buyurtmangiz holatini <b>«🗓 Faol Buyurtmalar»</b> sahifasida kuzatishingiz mumkin</i>'

        class client:
            passenger = f"Ariza haydovchiga jo’natildi, tasdiqlangandan so’ng sizga bildirishnoma keladi.\n\n" \
                        f"<b>Siz bir nechta haydovchilarga ariza yuborishingiz mumkin, " \
                        f"arizani birinchi bo'lib qabul qilgan kishi bilan yo’lga chiqasiz.</b>\n\n" \
                        f"Yana tanlaysizmi?"
            accept = "✅Ariza haydovchi tomonidan qabul qilindi"
            reject = '❌ Ariza haydovchi tomonidan rad etildi\n\n' \
                     'Boshqa haydovchini tanlashingiz mumkin👇'
            info = "Sizning ma’lumotlaringiz"

        class driver:
            driver = f'✅ Sizning arizangiz qabul qilindi. Yo’lovchilar javob berishlari bilan siz xabarnoma olasiz.\n\n' \
                     f'<i>Buyurtmalar holatini <b>«🗓 Faol Buyurtmalar»</b> sahifasida kuzatishingiz mumkin</i> 👇'
            route_cancel = "❌ Faoliyat bekor qilindi, mijozlar sizni boshqa haydovchilar roʻyxatida koʻrmaydi.\n\n" \
                           "❕Yo'lovchilar uchun yana faol boʻlish uchun <b>«🚕 Yo’ldaman»</b> tugmasini bosing."
            order = "Buyurtma va mijoz ma'lumotlarini olish uchun <b>«✅Qabul qilish»</b> tugmasini bosing."
            order_cost1 = 'Xizmat narxi'
            order_cost2 = "so'mni tashkil etadi, mablag' balansingizdan yechib olinadi."
            accept = "✅ Ariza qabul qilindi, yo’lovchiga buyurtma qabul qilinganligi haqida xabar berdik"
            reject = '❌ Ariza rad etildi'
            info = "Yo’lovchini maʼlumotlari"
            phone_client = "Telefon"
            new_order = "⚡ Yangi yo'lovchi bor!"

    class cancel:
        class client:
            question_order = "Buyurtmani bekor qilmoqchimisiz? Bu harakatni qaytarib bo'lmaydi."
            order = "❌Bekor qilindi."
            delete = "❌ Afsuski, haydovchi arizani bekor qildi"
            cancel = "❌ Ariza haydovchi tomonidan rad etildi"
            new_driver = "Boshqa haydovchi tanlashingiz mumkin 👇"

        class driver:
            passenger = "❌Yo’lovchi arizani bekor qildi, mablag' hamyoningizga qaytariladi"
            driver = "Ishonchingiz komilmi? Agar buyurtma haydovchi tomonidan bekor qilinsa mablag' " \
                     "balansingizga qaytarilmaydi"
            order = "❌Bekor qilindi."

    class alert:
        wallet = "Balansingizda mablag‘ingiz yetarli emas, balansingizni to‘ldiring." \
                                 "🔑 Shaxsiy kabinet —> 💳 Balans —> Balansni to‘ldirish"

        class phone:
            alert = "Qayta urinib ko'ring 😅"

        class driver:
            accept_order_late = "❌ Murojaat boshqa haydovchi tomonidan qabul qilinganligi yoki arizaga " \
                                "sizning tarafingizdan uzoq javob berilganligi sababli avtomatik rad etilgan"
            places_error =  "4 ta joydan ortiq bo’sh joy yo’q"
            places_full = "Mashina to'lgan, biz yo'lovchilarga xabarnoma yubordik"
            insufficient_funds = "Balansingizda mablag‘ingiz yetarli emas, balansingizni to‘ldiring." \
                                 "🔑 Shaxsiy kabinet —> 💳 Balans —> Balansni to‘ldirish"
            insufficient_funds2 = "⚠️Eslatma!\n\n" \
                                  "Keyingi buyurtmani qabul qilish uchun balansingizda yetarli mablag‘ yo‘q, " \
                                  "faol bo‘lish uchun balansingizni to‘ldiring"

    class car:
        car = {1: 'Cobalt', 2: 'Gentra', 3: 'Lacetti', 4: 'Nexia 1', 5: 'Nexia 2',
               6: 'Nexia 3', 7: 'Malibu 1', 8: 'Captiva', 9: 'Malibu 2', 10: 'Matiz',
               11: 'Spark', 12: 'Epica', 13: 'Damas', 14: 'Lada', 15: 'Иномарка'}
        color = {1: 'Oq', 2: 'Qora', 3: 'Kumush', 4: "To'q kulrang", 5: 'Sutli rang', 6: 'Olcha rang',
                 7: 'Sariq', 8: 'Qizil', 9: 'Yashil', 10: "Ko’k", 11: 'Moviy'}

    class active_order:
        no_active_order = "Hozirgi paytda faol buyurtmalaringiz yo’q"

    class rate:
        rate_5 = "😄 Baho uchun rahmat, sizga hammasi yoqgan bo’lsa biz xursandmiz!"
        rate_4 = "😄 Baho uchun rahmat, sizga hammasi yoqgan bo’lsa biz xursandmiz! Biz yaxshiroq harakat qilamiz."
        rate_3 = "😕 Baho uchun rahmat, haydovchi sizning umidlaringizni oqlamagani uchun uzur. " \
                 "Umid qilamizki, keyingi safar faqatgina ijobiy his-tuyg'ular qoldiradi."
        rate_2 = "😐 Baho uchun rahmat, haydovchi sizning umidlaringizni oqlamagani uchun uzur, " \
                 "uning faoliyatini kamaytiramiz."
        rate_1 = "😞 Baho uchun rahmat, haydovchi sizning umidlaringizni oqlamagani uchun uzur, " \
                 "uning faoliyatini kamaytiramiz."
        rate_dict = {1: rate_1, 2: rate_2, 3: rate_3, 4: rate_4, 5: rate_5}

    class on_spot:
        common = "❗ Jo’nash joyiga kelganingizda <b>«📍 Men joydaman»</b> tugmasini bosing"
        client = "📍 Yo'lovchi joyda 👇"
        driver = "📍 Haydovchi joyda 👇"
        on_spot = "📍 Jo’nash joyi 👆"
        inform_driver = "✅ Haydovchiga xabar berdik"
        inform_client = "✅ Yo’lovchilarga xabar berdik"
        time = "Jo’nash vaqti"
        info = "Yo’lovchilar ma’lumoti"
        passenger = "Yo’lovchi"
        phone = "Telefon"
        places = "Yo’lovchilar"

    class option:
        yes = "Bo’r"
        no = "Yo’q"
        da = "Ha"
        option = {0: no, 1: yes}

    class quiz:
        main = "Ayni paytda Paynet orqali to‘lov ulanmagan. \n\n" \
               "<b>Paynet orqali hamyoningizni to'ldirish sizga qulayroq bo'ladimi?</b>👇"
        thanks = "Ma'lumot uchun rahmat, tez orada ushbu to'lov usulini qo'shamiz."
        yes = "✅ Ha, qulayroq"

    class reminder:
        client1 = "📣"
        client2 = "ta dan ortiq haydovchilar bugun sizning yo’nalishingiz boyicha yo’lga chiqishmoqchi. " \
                  "O’zingizga qulay haydovchini topishga ulguring! 👇"
        driver1 = "📣"
        driver2 = "ta dan ortiq yo’lovchilar bugun sizning yo’nalishingiz boyicha yo’lga chiqishmoqchi. " \
                  "Faol bo’lishga ulguring! \n\n" \
                  "Faol bolish uchun <b>«🚕 Yo’lovchilar kerak»</b> tugmasini bosing"