from click_api.requests import prepare_pay, complete_pay
from config import dp
from payme_api.handlers import post_requests
from pgsql import pg, loop
from handlers.client.menu import MenuClient
from handlers.client.client import Client
from handlers.client.new_order import NewOrderClient
from handlers.client.active_order import ActiveOrderClient
from handlers.client.on_spot import OnSpotClient
from handlers.client.reminder import ReminderClient
from handlers.client.drivers_rate import DriversRate
from handlers.driver.registration import RegistrationDriver
from handlers.driver.menu import MenuDriver
from handlers.driver.driver import Driver
from handlers.driver.new_order import NewOrderDriver
from handlers.driver.active_order import ActiveOrderDriver
from handlers.driver.on_spot import OnSpotDriver
from handlers.driver.reminder import ReminderDriver
from handlers.driver.personal_cabinet import PersonalCabinet
from aiohttp import web
from handlers.admin.menu import MenuAdmin
from handlers.admin.mailing import Mailing
from handlers.admin.analise import Analise
from catching_errors.catch_errors import register_handlers_error


async def on_startup(dp):
	await pg.sql_start()
	print("бот вышел в онлайн")

app = web.Application()
app.router.add_post(path='/api', handler=post_requests)
app.router.add_post(path='/prepare', handler=prepare_pay)
app.router.add_post(path='/complete', handler=complete_pay)


#
menu_client = MenuClient()
client = Client()
new_order_client = NewOrderClient()
active_order_client = ActiveOrderClient()
on_spot_client = OnSpotClient()
reminder_client = ReminderClient()
drivers_rate = DriversRate()

registration = RegistrationDriver()
menu_driver = MenuDriver()
driver = Driver()
new_order_driver = NewOrderDriver()
active_order_driver = ActiveOrderDriver()
on_spot_driver = OnSpotDriver()
reminder_driver = ReminderDriver()
personal_cabinet = PersonalCabinet()

menu_admin = MenuAdmin()
mailing_admin = Mailing()
analise_admin = Analise()


# register_handlers
menu_client.register_handlers_client_menu(dp=dp)
client.register_handlers_client(dp=dp)
active_order_client.register_handlers_active_order_client(dp=dp)
on_spot_client.register_handlers_on_spot_client(dp=dp)
reminder_client.register_handlers_reminder_client(dp=dp)
drivers_rate.register_handlers_drivers_rate_client(dp=dp)
new_order_client.register_handlers_new_order_client(dp=dp)

registration.register_handlers_registration(dp=dp)
menu_driver.register_handlers_driver_menu(dp=dp)
driver.register_handlers_driver(dp=dp)
new_order_driver.register_handlers_new_order_driver(dp=dp)
active_order_driver.register_handlers_active_order_driver(dp=dp)
on_spot_driver.register_handlers_on_spot_driver(dp=dp)
reminder_driver.register_handlers_reminder_driver(dp=dp)
personal_cabinet.register_handlers_personal_cabinet(dp=dp)

menu_admin.register_handlers_menu_admin(dp=dp)
mailing_admin.register_handlers_mailing(dp=dp)
analise_admin.register_handlers_analise(dp=dp)
register_handlers_error(dp=dp)


def main():
	loop.run_until_complete(on_startup(dp=dp))
	loop.create_task(dp.start_polling())
	web.run_app(app=app, port=6001, loop=loop)


if __name__ == "__main__":
	main()
