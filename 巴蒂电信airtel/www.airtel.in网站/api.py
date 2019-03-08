# -*- coding: utf-8 -*-
# @Time    : 2018/10/18 19:33
# @Author  : zwl

import logging
import json
from core.protocol import Pro

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


class Api(object):

    def __init__(self):
        self.pro = Pro()

    def login(self, user, password):
        res = self.pro.check_user(user)
        requestkey = json.loads(res)['requestkey']
        print("requestkey:",requestkey)
        self.pro.auth_login(requestkey)
        return self.pro.login(user, password, requestkey)

    def spider(self, user):
        return self.pro.get_prepaid(user)


api = Api()
# api.login('8861359470', 'qwertyui1')
api.login('8861359470', 'qwertyui12')
print("11111")
print(api.spider('8861359470'))