import datetime
import math

from pgsql import pg
from text.language.main import Text_main

Txt = Text_main()


class TextFunc:

    @staticmethod
    async def int_to_str(num: int):
        new_num = ""
        num = str(num)
        num_len = len(num)
        for i in range(0, num_len, 3):
            if i < num_len - 3:
                part = num[num_len - 3 - i:num_len - i:]
                new_num = f"{part} {new_num}"
        new_num_len = len(new_num.replace(" ", ""))
        if new_num_len < num_len:
            new_num = f"{num[0:num_len - new_num_len]} {new_num}"
        return new_num

    @staticmethod
    async def percent_price(price: int):
        tax = int(price * 10 / 100)
        tax = math.ceil(tax / 500) * 500
        tax = tax if tax < 9000 else 9000
        return tax

    @staticmethod
    async def distance_to_str(distance: float):
        if distance < 1000:
            distance = f"{int(distance)} м"
        elif distance % 1000 == 0:
            distance = f"{int(distance / 1000)} км"
        else:
            distance = f"{round(distance/1000, 1)} км"
        return distance

    @staticmethod
    async def new_rate(rates):
        N = 50
        n = 20
        P = 0
        S = 0
        for i in rates:
            P += N * i[0]
            S += N
            N -= 1
        x = N - n if N > n else N
        for j in range(N, x - 1, -1):
            P += N * 5
            S += N
            N -= 1
        return round(P / S, 1)

    # @staticmethod
    async def distance(self, location_client: dict, location_driver: dict):
        lat1, lon1 = location_client['latitude'], location_client['longitude']
        lat2, lon2 = location_driver['latitude'], location_driver['longitude']
        distance = int((3958 * 3.1415926 * math.sqrt(
            (lat2 - lat1) * (lat2 - lat1) + math.cos(lat2 / 57.29578) * math.cos(lat1 / 57.29578) *
            (lon2 - lon1) * (lon2 - lon1)) / 180) * 1.609344 * 1000)
        return await self.distance_to_str(distance=distance)


