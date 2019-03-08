# -*- coding: utf-8 -*-
# @Time    : 2019/02/28 13:57
# @Author  : Haley

import json
from core.network import Req
from core.crypto import Crypto


class Pro(object):
    def __init__(self):
        self.Req = Req()
        self.Req2 = Req()
        self.Crypto = Crypto()

    def init(self):
        url = 'https://www.airtel.in/s/selfcare?normalLogin'
        headers = {
            'Host': 'www.airtel.in',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/72.0.3626.119 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://www.airtel.in/s/selfcare?normalLogin',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.Req.get(url=url, headers=headers)

    def check_user(self, user):
        adsheader = self.Crypto.get_adsheader()
        url = 'https://www.airtel.in/as/app/wl-service/airtel-digital-profile/rest/customer/authapp/v1/checkuser'
        headers = {
            'Host': 'www.airtel.in',
            'Connection': 'keep-alive',
            'Content-Length': '64',
            'Origin': 'https://www.airtel.in',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/72.0.3626.119 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': 'text/plain, */*; q=0.01',
            'googleCookie': 'airtel.com',
            'X-Requested-With': 'XMLHttpRequest',
            'adsHeader': adsheader,
            'Referer': 'https://www.airtel.in/s/selfcare?normalLogin',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        data = {"userid": user, "lob": "Mobility"}
        data = json.dumps(data, separators=(',', ':'))
        data_encrypt = self.Crypto.des_encrypt(key=adsheader, content=data, pad=b'\x08')
        res = self.Req.post(url=url, headers=headers, data=data_encrypt)
        print("res 1111:",res)
        googlecookie = res['headers']['googleCookie']
        text = self.Crypto.des_decrypt(key=googlecookie, content=res['text'], pad=b'\x04')
        return text

    def auth_login(self, requestkey):
        adsheader = self.Crypto.get_adsheader()
        url = 'https://www.airtel.in/as/app/wl-service/airtel-digital-profile/rest/customer/authapp/v1/authlogin'
        headers = {
            'Host': 'www.airtel.in',
            'Connection': 'keep-alive',
            'Origin': 'https://www.airtel.in',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/72.0.3626.119 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': 'text/plain, */*; q=0.01',
            'googleCookie': 'airtel.com',
            'X-Requested-With': 'XMLHttpRequest',
            'adsHeader': adsheader,
            'Referer': 'https://www.airtel.in/s/selfcare?normalLogin',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        data = {"action": "pkmsattempt", "requestkey": requestkey}
        data = json.dumps(data, separators=(',', ':'))
        data_encrypt = self.Crypto.des_encrypt(key=adsheader, content=data, pad=b'\x05')
        res = self.Req.post(url=url, headers=headers, data=data_encrypt)
        googlecookie = res['headers']['googleCookie']
        text = self.Crypto.des_decrypt(key=googlecookie, content=res['text'], pad=b'\x04')
        return text

    def login(self, user, password, requestkey):
        url = 'https://www.airtel.in/as/pkmslogin.form'
        headers = {
            'Host': 'www.airtel.in',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://www.airtel.in',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/72.0.3626.119 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://www.airtel.in/s/selfcare?normalLogin',
            'Accept-Language': 'zh-CN,zh;q=0.9',

        }
        data = {
            'mobileNumber': user,
            'password': password,
            'login-form-type': 'pwd',
            'username': user,
            'requestKey': requestkey,
        }
        res = self.Req.post(url=url, headers=headers, data=data, redirects=True)
        # googlecookie = res['headers']['googleCookie']
        # text = self.Crypto.des_decrypt(key=googlecookie, content=res['text'], pad=b'\x01')
        # print(self.Req.session.cookies.get_dict())
        print(res['text'])
        print(222)
        return res['text']

    def get_prepaid(self, user):
        adsheader = self.Crypto.get_adsheader()
        adsheader = self.Crypto.sha1_encrypt(adsheader)
        url = 'https://www.airtel.in/s/app/wl-service/airtel-usage/rest/prepaid/usage/recharge/v2/details/fetch?'
        params = {'siNumber': user}
        headers = {
            'Host': 'www.airtel.in',
            'Accept': 'application/json, text/plain, */*',
            'googleCookie': 'airtel.com',
            'adsHeader': adsheader,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/72.0.3626.119 Safari/537.36',
            'requesterId': 'WEB',
            'Referer': 'https://www.airtel.in/s/selfcare/prepaid/8861359470/packsAndService',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.Req2.set_cookie(self.Req.session.cookies.get_dict())
        res = self.Req2.get(url=url, headers=headers, params=params)
        print(res)
        googlecookie = res['headers']['googleCookie']
        text = self.Crypto.des_decrypt(key=googlecookie, content=res['text'], pad=b'\x02')
        return text
