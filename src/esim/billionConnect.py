import json
import datetime

from typing import Any
from dataclasses import dataclass
from src.libs.httpRequests import HttpRequests
from src.utils import md5


@dataclass
class BCResponse:
    tradeCode: str
    tradeData: Any
    tradeMsg: str


class BillionConnect:
    """
    文档地址：https://sale-flow.billionconnect.com/open/interfaceDoc.do
    最后更新：2025-03-06

    F001-获取覆盖国家列表 Obtain list of countries covered
    F002-获取商品 Obtain commodities
    F003-获取商品价格 Obtain commodity price
    F004-获取自提点信息 Obtain self-pick-up site information
    F005-获取物流公司信息 Obtain logistics company information
    F006-创建含卡订单 Create card order
    F007-创建充值订单 Create recharge order
    F008-取消订单 Cancel order
    F009-修改物流信息 Modify logistics information
    F010-查询卡片有效期 Query validity of card
    F011-查询订单信息 Query order information
    F012-查询套餐使用信息 Query data plan usage information
    F013-卡号充值验证 Validate add package iccids
    F014-查询预存款账户余额 Query sale account balance
    F015-查询加速包商品 Query acceleration package commodities
    F016-创建加速包订单 Create acceleration package order
    F017-售后申请 Apply after sale
    F018-取消售后单 Cancel after sale
    F019-修改售后单 Modify after sale
    F020-查询售后单 Query after sale
    F023-日流量查询 Daily flow query
    F040-创建ESIM订单 Create ESIM order
    F041-重新发送ESIM邮件 Resend ESIM email
    F042-查询ESIM服务状态 Query ESIM Profile Status
    F045-结束已激活套餐 Terminate active plan
    F046-查询套餐使用信息 Query data plan usage information
    F051-通过商品ID获取自提点信息 Query self pickup information by sku
    F052-查询eSIM充值商品 Query eSIM recharge commodities
    F054-查询实名认证状态 Query realname authentication status
    """

    url = 'https://apiint-flow.billionconnect.com/Flow/saler/2.0/invoke'

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret

    @staticmethod
    def __payload(trade_type: str, trade_data: dict):
        return json.dumps(
            {
                'tradeType': trade_type,
                'tradeTime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'tradeData': trade_data,
            },
            separators=(',', ':'),
        )

    def __headers(self, payload: str):
        return {
            'x-channel-id': self.app_id,
            'x-sign-value': md5(f'{self.app_secret}{payload}'),
            'x-sign-method': 'md5',
            'Content-Type': 'application/json;charset=UTF-8',
        }

    async def __post(self, payload: str):
        res = await HttpRequests.post(self.url, payload, headers=self.__headers(payload))
        if res:
            return BCResponse(**res.json)

    async def f001(self, sales_method: int = 5, language: int = 1):
        """
        获取覆盖国家列表 Obtain list of countries covered
        """
        return await self.__post(
            self.__payload(
                'F001',
                {
                    'salesMethod': str(sales_method),
                    'language': str(language),
                },
            )
        )

    async def f002(
        self,
        sales_method: int = 5,
        sku_id: str = '',
        network_operator_scope: int = 1,
        language: int = 1,
        country_code: str = '',
    ):
        """
        获取商品 Obtain commodities
        """
        return await self.__post(
            self.__payload(
                'F002',
                {
                    'salesMethod': str(sales_method),
                    'skuId': sku_id,
                    'networkOperatorScope': network_operator_scope,
                    'language': str(language),
                    'countryCode': country_code,
                },
            )
        )

    async def f003(self, sales_method: int = 5):
        """
        获取商品价格 Obtain commodity price
        """
        return await self.__post(
            self.__payload(
                'F003',
                {
                    'salesMethod': str(sales_method),
                },
            )
        )

    async def f004(self):
        """
        F004-获取自提点信息 Obtain self-pick-up site information
        """
        raise NotImplementedError

    async def f005(self):
        """
        F005-获取物流公司信息 Obtain logistics company information
        """
        raise NotImplementedError

    async def f006(self):
        """
        F006-创建含卡订单 Create card order
        """
        raise NotImplementedError

    async def f007(self):
        """
        F007-创建充值订单 Create recharge order
        """
        raise NotImplementedError

    async def f008(self):
        """
        F008-取消订单 Cancel order
        """
        raise NotImplementedError

    async def f009(self):
        """
        F009-修改物流信息 Modify logistics information
        """
        raise NotImplementedError

    async def f010(self):
        """
        F010-查询卡片有效期 Query validity of card
        """
        raise NotImplementedError

    async def f011(self):
        """
        F011-查询订单信息 Query order information
        """
        raise NotImplementedError

    async def f012(self):
        """
        F012-查询套餐使用信息 Query data plan usage information
        """
        raise NotImplementedError

    async def f013(self):
        """
        F013-卡号充值验证 Validate add package iccids
        """
        raise NotImplementedError

    async def f014(self):
        """
        F014-查询预存款账户余额 Query sale account balance
        """
        raise NotImplementedError

    async def f015(self):
        """
        F015-查询加速包商品 Query acceleration package commodities
        """
        raise NotImplementedError

    async def f016(self):
        """
        F016-创建加速包订单 Create acceleration package order
        """
        raise NotImplementedError

    async def f017(self):
        """
        F017-售后申请 Apply after sale
        """
        raise NotImplementedError

    async def f018(self):
        """
        F018-取消售后单 Cancel after sale
        """
        raise NotImplementedError

    async def f019(self):
        """
        F019-修改售后单 Modify after sale
        """
        raise NotImplementedError

    async def f020(self):
        """
        F020-查询售后单 Query after sale
        """
        raise NotImplementedError

    async def f023(self):
        """
        F023-日流量查询 Daily flow query
        """
        raise NotImplementedError

    async def f040(self):
        """
        F040-创建ESIM订单 Create ESIM order
        """
        raise NotImplementedError

    async def f041(self):
        """
        F041-重新发送ESIM邮件 Resend ESIM email
        """
        raise NotImplementedError

    async def f042(self):
        """
        F042-查询ESIM服务状态 Query ESIM Profile Status
        """
        raise NotImplementedError

    async def f045(self):
        """
        F045-结束已激活套餐 Terminate active plan
        """
        raise NotImplementedError

    async def f046(self):
        """
        F046-查询套餐使用信息 Query data plan usage information
        """
        raise NotImplementedError

    async def f051(self):
        """
        F051-通过商品ID获取自提点信息 Query self pickup information by sku
        """
        raise NotImplementedError

    async def f052(self):
        """
        F052-查询eSIM充值商品 Query eSIM recharge commodities
        """
        raise NotImplementedError

    async def f054(self):
        """
        F054-查询实名认证状态 Query realname authentication status
        """
        raise NotImplementedError
