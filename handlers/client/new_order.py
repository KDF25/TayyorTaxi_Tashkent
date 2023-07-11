import json

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot
from handlers.client.client import Client
from pgsql import pg
from text.function.function import TextFunc
from text.language.main import Text_main

Txt = Text_main()
func = TextFunc()


class Unpack:

    def __init__(self, call: types.CallbackQuery, data: dict):
        self.__call = call
        self.__data = data

    async def start(self):
        await self._unpack_call()
        await self._unpack_new_order()
        await self._unpack_spots()
        return self.__data

    async def _unpack_call(self):
        self.__data['lang'] = await pg.select_language(user_id=int(self.__call.from_user.id))
        self.__data['client_id'] = int(self.__call.from_user.id)
        self.__data['order_client_id'] = int(self.__call.data.split('_')[1])
        self.__data['row_id'] = await pg.insert_analise_client(user_id=int(self.__call.from_user.id))

    async def _unpack_new_order(self):
        self.__data['phone_client'], self.__data['from_town'], location, self.__data['to_town'],  \
            self.__data['to_district'], self.__data['to_spot'],  self.__data['to_subspot'], date_time, \
            self.__data['places'] = await pg.new_order_client(order_client_id=self.__data.get('order_client_id'))
        self.__data['location'] = json.loads(location)

    async def _unpack_spots(self):
        self.__data['from_town_value'] = await pg.id_to_town(language=self.__data.get('lang'), sub_id=self.__data.get('from_town'))
        self.__data['to_town_value'] = await pg.id_to_town(language=self.__data.get('lang'), sub_id=self.__data.get('to_town'))
        self.__data['to_spot_value'] = await pg.id_to_spot(language=self.__data.get('lang'), sub_id=self.__data.get('to_spot'))
        self.__data['to_subspot_value'] = await pg.id_to_sub_spot(language=self.__data.get('lang'), sub_id=self.__data.get('to_subspot'))

    async def state(self):
        if self.__data.get('to_district') is not None:
            return "Client:_city_level5"
        else:
            return "Client:_town_level4"


class NewOrderClient(StatesGroup):
    new_order_client = State()

    @staticmethod
    async def menu_new_order(call: types.CallbackQuery, state: FSMContext):
        client = Client()
        unpack = Unpack(call=call, data=await state.get_data())
        await state.set_data(data=await unpack.start())
        await state.set_state(state=await unpack.state())
        await client.menu_more(call=call, state=state)

    @staticmethod
    async def menu_location(call: types.CallbackQuery, state: FSMContext):
        location = await pg.active_location(order_accept_id=int(call.data.split("_")[1]))
        await bot.send_location(chat_id=call.from_user.id, latitude=location['latitude'],
                                longitude=location['longitude'])
        await call.answer()

    def register_handlers_new_order_client(self, dp: Dispatcher):
        dp.register_callback_query_handler(self.menu_new_order, lambda x: x.data.startswith("passenger"), state='*')
        dp.register_callback_query_handler(self.menu_location, lambda x: x.data.startswith("point"), state="*")
