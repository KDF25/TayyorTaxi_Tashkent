import datetime
from string import Template

from pgsql import pg
from text.function.function import TextFunc
from text.language.main import Text_main

func = TextFunc()
Txt = Text_main()


class FormAdmin:

    async def every_day_client(self, language: str, num: int):
        Text_lang = Txt.language[language]
        text = Template("$text1 <b>$num</b> $text2")
        text = text.substitute(text1=Text_lang.reminder.client1, text2=Text_lang.reminder.client2, num=num)
        return text

    async def every_day_driver(self, language: str, num: int):
        Text_lang = Txt.language[language]
        text = Template("$text1 <b>$num</b> $text2")
        text = text.substitute(text1=Text_lang.reminder.driver1, text2=Text_lang.reminder.driver2, num=num)
        return text

    async def client(self, num: int):
        text = f"🇺🇿📣 <b>{num}</b> ta dan ortiq haydovchilar bugun sizning yo’nalishingiz boyicha yo’lga chiqishmoqchi. " \
             f"O’zingizga qulay haydovchini topishga ulguring! 👇 \n\n" \
             f"🇷🇺📣 Свыше <b>{num}</b> водителей собираются сегодня ехать по вашему направлению. " \
             f"Успейте найти подходящего именно для вашей поездки! 👇"
        return text

    async def driver(self, num: int):
        text = f'🇺🇿📣 <b>{num}</b> ta dan ortiq yo’lovchilar bugun sizning yo’nalishingiz boyicha yo’lga chiqishmoqchi. ' \
               f'Faol bo’lishga ulguring! \n\n Faol bolish uchun «🚕 Yo’lovchilar kerak» tugmasini bosing 👇\n\n ' \
               f'🇷🇺📣 Свыше <b>{num}</b> пассажиров собираются сегодня ехать по вашему направлению. ' \
               f'Успейте стать активным, чтобы найти подходящих именно для вас! \n\n ' \
               f'Жмите «🚕 Нужны пассажиры» чтобы стать активным 👇'
        return text


    async def left_days(self, language: str, days: int, wallet: int, date):
        Text_lang = Txt.language[language]
        date = datetime.datetime.strftime(date, "%d.%m.%y")
        wallet = await func.int_to_str(num=wallet)
        day = ''
        if language == 'rus':
            day = 'день' if days == 1 else 'дней'
        text = Template("$text1 <b>$wallet $sum</b>"
                        "$text2 <b>$days $day</b>"
                        "$text3: $date $text4")
        text = text.substitute(text1=Text_lang.mailing.left_days.text1, wallet=wallet, sum=Text_lang.symbol.sum,
                               text2=Text_lang.mailing.left_days.text2, days=days, day=day,
                               text3=Text_lang.mailing.left_days.text3, date=date,
                               text4=Text_lang.mailing.left_days.text4)
        return text

    async def mail_end(self, users: str):
        count = await pg.get_users_unblock(users=users)
        text = Template('Рассылка завершена. Доставлено — $nonblock пользователям. '
                        'Бот заблокирован — $block пользователями')
        text = text.substitute(nonblock=count[0][0], block=count[1][0])
        return text

    async def mailing_choose(self, users: str):
        if users == 'client':
            self.__type = 'Клиенты'
        elif users == 'driver':
            self.__type = 'Водители'
        elif users == 'all':
            self.__type = 'Все пользователи'
        await self.mailing()
        return self.__text

    async def mailing(self):
        text = Template("<b>$type</b>\n\n"
                        "$start_mailing")
        self.__text = text.substitute(type=self.__type,
                                      start_mailing="Отправьте сообщение которое хотели бы разослать!")

    async def mailing_st(self):
        date = datetime.date.strftime(datetime.date.today(), "%d.%m.%Y")

        new_users = await func.int_to_str(num=await pg.new_users())
        new_drivers = await func.int_to_str(num=await pg.new_drivers())
        all_users = await func.int_to_str(num=await pg.all_users())
        all_drivers = await func.int_to_str(num=await pg.all_drivers())

        all_payment = await func.int_to_str(num=(await pg.all_payment())[0])
        all_payment_max = await func.int_to_str(num=(await pg.all_payment())[1])
        all_payment_min = await func.int_to_str(num=(await pg.all_payment())[2])
        all_payment_count = await func.int_to_str(num=(await pg.all_payment())[3])

        new_payment = await func.int_to_str(num=(await pg.new_payment())[0])
        new_payment_max = await func.int_to_str(num=(await pg.new_payment())[1])
        new_payment_min = await func.int_to_str(num=(await pg.new_payment())[2])
        new_payment_count = await func.int_to_str(num=(await pg.new_payment())[3])

        all_order_success = await func.int_to_str(num=(await pg.all_orders_success()))
        new_order_success = await func.int_to_str(num=(await pg.new_orders_success()))
        all_order_cancel_driver= await func.int_to_str(num=(await pg.all_order_cancel_driver()))
        new_order_cancel_driver = await func.int_to_str(num=(await pg.new_order_cancel_driver()))
        all_order_cancel_client = await func.int_to_str(num=(await pg.all_order_cancel_client()))
        new_order_cancel_client = await func.int_to_str(num=(await pg.new_order_cancel_client()))
        cancel_by_client_max = await func.int_to_str(num=(await pg.cancel_by_client())[0])
        cancel_by_client_min = await func.int_to_str(num=(await pg.cancel_by_client())[1])
        cancel_by_client_avg = await func.int_to_str(num=(await pg.cancel_by_client())[2])

        cancel_by_driver_max = await func.int_to_str(num=(await pg.cancel_by_driver())[0])
        cancel_by_driver_min = await func.int_to_str(num=(await pg.cancel_by_driver())[1])
        cancel_by_driver_avg = await func.int_to_str(num=(await pg.cancel_by_driver())[2])

        payment_type = await pg.all_payment_type()
        Click = await func.int_to_str(num=payment_type[0][0])
        Payme = await func.int_to_str(num=payment_type[1][0])
        Paynet = await func.int_to_str(num=payment_type[2][0])

        text = Template("Сводка: $date\n\n"

                        "Новые пользователи — <b>$new_users</b>\n"
                        "Новые водители — <b>$new_drivers</b>\n"
                        "Общее количество пользователей — <b>$all_users</b>\n"
                        "Общее количество водителей — <b>$all_drivers</b>\n\n"
                        "———————————————\n\n"
                        "Сумма пополнения сегодня — <b>$new_payment</b> сум\n"
                        "Общая сумма пополнения — <b>$all_payment</b> сум\n\n"
                        "———————————————\n\n"
                        "✅ Новые успешные заказы: — $new_order_success\n\n"
                        "✅ В общем успешных заказов: — $all_order_success\n\n"
                        "❌ Новые отменённые заказы:\n"
                        "Клиентом: — $new_order_cancel_client\n"
                        "Водителем: — $new_order_cancel_driver\n\n"
                        "❌ В общем отменённых заказов:\n"
                        "Клиентом: — $all_order_cancel_client\n"
                        "Водителем: — $all_order_cancel_driver\n\n"
                        "———————————————\n\n"
                        "Сумма пополнения сегодня:\n"
                        "• максимум — $new_payment_max сум\n"
                        "• минимум — $new_payment_min сум\n"
                        "• <b>кол-во пополнений — $new_payment_count</b>\n\n"
                        "За все время:\n"
                        "• максимум — $all_payment_max сум\n"
                        "• минимум — $all_payment_min сум\n"
                        "• <b>кол-во пополнений — $all_payment_count</b>\n\n"
                        "Метод оплаты:\n"
                        "• Click — $Click\n"
                        "• Payme — $Payme\n"
                        "• Paynet — $Paynet\n\n"
                        "———————————————\n\n"
                        "⛔️Отмена заказа 1 пользователем:\n"
                        "Клиент:\n"
                        "• максимум отклонено — $cancel_by_client_max\n"
                        "• минимум — $cancel_by_client_min\n"
                        "• среднее — $cancel_by_client_avg\n\n"
                        "Водитель:\n"
                        "• максимум отклонено — $cancel_by_driver_max\n"
                        "• минимум — $cancel_by_driver_min\n"
                        "• среднее — $cancel_by_driver_avg\n")
        text = text.substitute(date=date,
                               new_users=new_users,
                               new_drivers=new_drivers,
                               all_users=all_users,
                               all_drivers=all_drivers,

                               all_payment=all_payment,
                               all_payment_max=all_payment_max,
                               all_payment_min=all_payment_min,
                               all_payment_count=all_payment_count,

                               new_payment=new_payment,
                               new_payment_max=new_payment_max,
                               new_payment_min=new_payment_min,
                               new_payment_count=new_payment_count,

                               all_order_success=all_order_success,

                               new_order_success=new_order_success,

                               all_order_cancel_driver=all_order_cancel_driver,

                               new_order_cancel_driver=new_order_cancel_driver,

                               all_order_cancel_client=all_order_cancel_client,

                               new_order_cancel_client=new_order_cancel_client,

                               Click=Click, Payme=Payme, Paynet=Paynet,

                               cancel_by_client_max=cancel_by_client_max,
                               cancel_by_client_min=cancel_by_client_min,
                               cancel_by_client_avg=cancel_by_client_avg,

                               cancel_by_driver_max=cancel_by_driver_max,
                               cancel_by_driver_min=cancel_by_driver_min,
                               cancel_by_driver_avg=cancel_by_driver_avg)
        # print(text)
        return text

