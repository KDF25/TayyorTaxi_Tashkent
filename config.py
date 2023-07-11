from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from attrs import define, field

from click_api.models.click_data import Click_Data

storage = RedisStorage2(db=3)
scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
scheduler.start()

PGUSER = "postgres"
PASSWORD = "karimov"
token = '5369594012:AAFASOLAQUE_EXLh8Y-qYkpkNagl0h9a0Q8'
ip = 'localhost'

bot = Bot(token=str(token), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

chat_id_our = -1001767085919

@define
class ApiKeys:
    status: bool = True
    testkey: str = "bvgSObj8KMfVKmDr2eXtQouhHu1h6tMSYY5o"
    prod_key: str = "J6moK&R1V46gk5X8%6xWygHwVkF2%Xv5nfxQ"
    merchant_id: str = "634e0e269fd41bc3daf3c022"
    payme_url: str = "https://checkout.paycom.uz/"
    payme_key: bytes = field(default="".encode())

    def __attrs_post_init__(self) -> None:
        key = self.prod_key if self.status is True else self.testkey
        self.payme_key = f"Paycom:{key}".encode()


payme_keys = ApiKeys()
cli_data = Click_Data(service_id=25574, merchant_id=17595, secret_key="0UPkg4pS40", merchant_user_id=28977)
