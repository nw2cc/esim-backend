import json
import time
import hashlib

from typing import Union, List, Any
from dataclasses import dataclass
from src.libs.httpRequests import HttpRequests
from src.utils import md5


@dataclass
class RSPResponse:
    code: str
    mesg: str
    data: Any


class JoyTelWarehouse:
    customer_url = 'https://api.joytel.vip/customerApi/customerOrder'
    recharge_url = 'https://api.joytel.vip/joyRechargeApi/rechargeOrder'

    def __init__(self, customer_code: str, customer_auth: str):
        self.customer_code = customer_code
        self.customer_auth = customer_auth

    @staticmethod
    def headers():
        return {
            'Content-Type': 'application/json',
        }

    @staticmethod
    def timestamp():
        return int(time.time() * 1000)

    @staticmethod
    def item_list_trans(item_list: List[dict]):
        text = ''
        for item in item_list:
            for value in item.values():
                text += str(value)
        return text

    def auto_graph(self, *content: Union[str, int]):
        text = f'{self.customer_code}{self.customer_auth}' + ''.join(str(n) for n in content)
        sha1 = hashlib.sha1()
        sha1.update(text.encode('utf-8'))
        return sha1.hexdigest()

    async def order_submit(
        self,
        receiver_name: str,
        receiver_phone: str,
        email: str,
        product_code: str,
        quantity: int = 1,
        order_type: int = 3,
        remark: str = '',
    ):
        timestamp = self.timestamp()
        item_list = [
            {
                'productCode': product_code,
                'quantity': quantity,
            }
        ]
        payload = {
            'customerCode': self.customer_code,
            'type': order_type,
            'receiveName': receiver_name,
            'phone': receiver_phone,
            'timestamp': timestamp,
            'autoGraph': self.auto_graph(
                order_type,
                receiver_name,
                receiver_phone,
                timestamp,
                self.item_list_trans(item_list),
            ),
            'itemList': item_list,
            'remark': remark,
            'email': email,
        }
        return await HttpRequests.post(self.customer_url, json.dumps(payload), headers=self.headers())

    async def order_query(self, order_code: str):
        timestamp = self.timestamp()
        payload = {
            'customerCode': self.customer_code,
            'timestamp': timestamp,
            'autoGraph': self.auto_graph(order_code, timestamp),
            'orderCode': order_code,
        }
        return await HttpRequests.post(self.customer_url + '/query', json.dumps(payload), headers=self.headers())

    async def recharge_order_submit(self):
        raise NotImplementedError

    async def recharge_order_query(self):
        raise NotImplementedError


class JoyTelRSP:
    base_url = 'https://esim.joytelecom.com/openapi'

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret

    def __headers(self):
        timestamp = int(time.time() * 1000)
        trans_id = md5(timestamp)
        return {
            'AppId': self.app_id,
            'TransId': trans_id,
            'Timestamp': timestamp,
            'Ciphertext': md5(f'{self.app_id}{trans_id}{timestamp}{self.app_secret}'),
            'Content-Type': 'application/json',
        }

    async def coupon_query(self, coupons: List[str]):
        res = await HttpRequests.post(
            self.base_url + '/openapi/coupon/query',
            {
                'coupons': ','.join(coupons),
            },
            headers=self.__headers(),
        )
        if res:
            return RSPResponse(**res.json)

    async def coupon_redeem(self, coupon: str):
        res = await HttpRequests.post(
            self.base_url + '/openapi/coupon/redeem',
            {
                'coupon': coupon,
                'qrcodeType': 1,
            },
            headers=self.__headers(),
        )
        if res:
            return RSPResponse(**res.json)
