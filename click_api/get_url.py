from config import cli_data
from pgsql import pg
from click_api.models.insert_order import InsertCreatedOrder


class GetUrl:
    def __init__(self, amount: int, driver_id: int, pay_id: int | str):
        self.amount = amount
        self.driver_id = driver_id
        self.pay_id = pay_id

    async def return_url(self):
        return (f"https://my.click.uz/services/pay?"
                f"service_id={cli_data.service_id}&"
                f"merchant_id={cli_data.merchant_id}&"
                f"amount={self.amount}&"
                f"transaction_param="
                f"{self.pay_id}")

    async def add_order(self):
        return InsertCreatedOrder(
            click_trans_id=0,
            click_paydoc_id=0,
            merchant_trans_id=f"{self.pay_id}",
            amount=self.amount,
            action=0,
            sign_time="",
            canceled=False
        )