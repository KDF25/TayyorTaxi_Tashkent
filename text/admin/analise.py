import datetime
from string import Template

from pgsql import pg
from text.function.function import TextFunc
from text.language.main import Text_main

func = TextFunc()
Txt = Text_main()


class FormAnalise:
    def __init__(self):
        self.__data = None
        self.__text = None
        self.__type = None


    async def analise(self, data: dict):
        self.__data = data
        if self.__data['type'] == 'taxi':
            await self._taxi()
        elif self.__data['type'] == 'online':
            await self._online()
        return self.__text

    async def _taxi(self):
        await self._unpack_taxi()
        text = Template('<b>Анализ $timeframe: $date</b>\n\n'
                        '• нажал  Найти водителя  - $passenger\n'
                        '• нажал  Откуда(город) - $from_town\n'
                        '• нажал  Отправил локацию  - $location\n'
                        '• нажал  Куда(город)   - $to_town\n'
                        '• нажал  Количество мест - $place\n'
                        '•        <b>Нет машин</b>      - $no_model\n'
                        '• нажал  Район   - $district\n'
                        '• нажал  Пятак  - $spot\n'
                        '• нажал  Подпятак - $sub_spot\n\n'
                        '• Расстояние/Цена/Время - \n'
                        '$filter_distance | $filter_money | $filter_time\n\n'
                        '• выбрал Водителя - $ordered\n'
                        '• нажал заказать  -  $phone\n'
                        '• отправил телефон - $book\n\n\n'
                        '<b><i>* Нет машин - показывает процент тех, кто дошел до выбора модели, '
                        'но остановился так как не было машин</i></b>')
        self.__text = text.substitute(timeframe=self.__timeframe_text,date=self.__date, passenger=self.__type_app,
                                      from_town=self.__from_town,
                                      filter_distance=self.__filter_distance,
                                      filter_money=self.__filter_money,
                                      filter_time=self.__filter_time,
                                      location=self.__location,
                                      to_town=self.__to_town,
                                      place=self.__places,
                                      no_model=self.__no_model,
                                      district=self.__to_district,
                                      spot=self.__to_spot,
                                      sub_spot=self.__to_sub_spot,
                                      ordered=self.__ordered,
                                      phone=self.__phone,
                                      book=self.__book)

    async def _unpack_taxi(self):
        self.__count = await pg.count_clients()
        self.__date = datetime.date.strftime(datetime.date.today(), "%d.%m.%Y")
        await self._timeframe_taxi()
        await self._unpack_parameters()
        await self._timeframe_text()
        self.__type_app, self.__from_town, self.__location, self.__to_town, self.__places, self.__no_model, \
            self.__to_district,  self.__to_spot,  self.__to_sub_spot, self.__filter_time, self.__filter_money, \
            self.__filter_distance, self.__ordered, self.__phone, self.__book = self.__parameters

    async def _timeframe_taxi(self):
        if self.__data['timeframe'] == 'all':
            self.__parameters = await pg.analise_taxi_all_time()
        else:
            self.__parameters = await pg.analise_taxi_timeframe(days=int(self.__data['timeframe']))

    async def _timeframe_text(self):
        if self.__data['timeframe'] == 'all':
            self.__timeframe_text = 'за все время'
        else:
            self.__timeframe_text = f"за {self.__data['timeframe']} день/дней"

    async def _unpack_parameters(self):
        parameters = []
        for parameter in self.__parameters:
            parameter = f'{parameter[0]}/{self.__count}   ({round(parameter[0] / self.__count * 100, 1)} %)'
            parameters.append(parameter)
        self.__parameters = parameters

    async def _online(self):
        await self._unpack_online()
        text = Template('<b>Анализ $timeframe: $date</b>\n\n'
                        '• нажал На линии       - $online\n'
                        '• нажал  Откуда(город) - $from_town\n'
                        '• нажал  Отправил локацию  - $location\n'
                        '• нажал  Куда(город)   - $to_town\n'
                        '• нажал  Район   - $district\n'
                        '• нажал  Пятак  - $spot\n'
                        '• нажал  Подпятак - $sub_spot\n'
                        '• нажал  Цена     - $price\n'
                        '• нажал  Количество мест - $place\n'
                        '• нажал  Время - $date_time\n'
                        '• нажал  Подтверждение  - $book\n\n'
                        '• Хотел отменить - $cancel\n'
                        '• Отменил        - $delete\n\n')
        self.__text = text.substitute(timeframe=self.__timeframe_text, date=self.__date,
                                      online=self.__online, from_town=self.__from_town,
                                      location=self.__location,
                                      to_town=self.__to_town,
                                      district=self.__to_district,
                                      spot=self.__to_spot,
                                      sub_spot=self.__to_sub_spot,
                                      price=self.__price,
                                      place=self.__place,
                                      book=self.__book,
                                      date_time=self.__date_time,
                                      cancel=self.__cancel, delete=self.__delete)

    async def _unpack_online(self):
        self.__count = await pg.count_drivers()
        self.__date = datetime.date.strftime(datetime.date.today(), "%d.%m.%Y")
        await self._timeframe_online()
        await self._unpack_parameters()
        await self._timeframe_text()
        self.__online, self.__from_town, self.__location, self.__to_town, self.__to_district,  \
            self.__to_spot,  self.__to_sub_spot, self.__price, self.__place, \
            self.__date_time, self.__book, self.__cancel, self.__delete = self.__parameters

    async def _timeframe_online(self):
        if self.__data['timeframe'] == 'all':
            self.__parameters = await pg.analise_online_all_time()
        else:
            self.__parameters = await pg.analise_online_timeframe(days=int(self.__data['timeframe']))