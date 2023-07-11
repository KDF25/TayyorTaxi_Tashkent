import math



# async def distance(self, location_client: dict, location_driver: dict):
#     lat1, lon1 = location_client['latitude'], location_client['longitude']
#     lat2, lon2 = location_driver['latitude'], location_driver['longitude']
#     distance = int((3958 * 3.1415926 * math.sqrt(
#         (lat2 - lat1) * (lat2 - lat1) + math.cos(lat2 / 57.29578) * math.cos(lat1 / 57.29578) *
#         (lon2 - lon1) * (lon2 - lon1)) / 180) * 1.609344 * 1000)
#     return await self.distance_to_str(distance=distance)

# lat1, lon1 =  41.343764,  69.312397
# lat2, lon2 =  41.334462,  69.314137
# distance = int((3958 * 3.1415926 * math.sqrt(
#         (lat2 - lat1) * (lat2 - lat1) + math.cos(lat2 / 57.29578) * math.cos(lat1 / 57.29578) *
#         (lon2 - lon1) * (lon2 - lon1)) / 180) * 1.609344 * 1000)
# print(distance)
import random

for i in range(55, 0, -5):
    print(i)