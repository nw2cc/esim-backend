import asyncio

from src.esim.billionConnect import BillionConnect
from src.esim.joyTel import JoyTelWarehouse


async def main():

    # 亿点创建 eSIM 订单
    bc = BillionConnect('HuanYu', '5e545d0680b64a11992b1a26cd932909')
    res = await bc.f040()
    print(res)

    # JoyTel 提交订单
    jtw = JoyTelWarehouse('test001', 'abcdefj')
    res = await jtw.order_submit(
        'test',
        '15666666666',
        'test@qq.com',
        'eSIM-test',
    )
    print(res)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
