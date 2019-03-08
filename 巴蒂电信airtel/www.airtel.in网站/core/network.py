# -*- coding: utf-8 -*-
# @Time    : 2018/10/18 19:33
# @Author  : zwl

import time
import logging
import requests
from http.cookies import SimpleCookie

import urllib3
urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class Req(object):

    def __init__(self):
        self.headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                      ' Chrome/72.0.3626.119 Safari/537.36',
                        }
        self.session = requests.session()
        self.session.headers.clear()
        self.session.cookies.clear()
        self.session.headers.update(self.headers)

    def set_headers(self, headers):
        self.session.headers.update(headers)

    def set_cookie(self, cookie):
        self.session.cookies.update(cookie)

    def get(self, url, params=None, headers=None, retry=2):

        logger.debug(url)
        logger.debug(params)
        logger.debug(self.session.cookies.get_dict())

        for i in range(retry):
            try:
                if headers:
                    self.set_headers(headers)
                result = self.session.get(url, params=params, timeout=(3, 12), verify=False)
                if result.status_code < 400:
                    if 'Set-Cookie' in result.headers:
                        logger.warning(result.headers['Set-Cookie'])
                        simple_cookie = SimpleCookie(result.headers['Set-Cookie'])
                        for item in simple_cookie:
                            self.session.cookies.update({item: simple_cookie[item].value})
                    logger.debug(self.session.cookies.get_dict())
                    logger.debug(result.content)
                    return {'text': result.text, 'headers': result.headers}
                else:
                    logger.warning("HttpStatusCode %d", result.status_code)
            except requests.exceptions.ConnectTimeout:
                logger.warning('requests.exceptions.ConnectTimeout')
            except requests.exceptions.ReadTimeout:
                logger.warning('requests.exceptions.ReadTimeout')
            except requests.exceptions.Timeout:
                logger.warning('requests.exceptions.Timeout')
            except requests.exceptions.ProxyError:
                logger.warning('requests.exceptions.ProxyError')
            except Exception as e:
                logger.warning('Post Other Exception Occur, err=[%s]', e, exc_info=True)
            time.sleep(2)
        return False

    def post(self, url, data, params=None, headers=None, retry=2, redirects=True):

        logger.debug(url)
        logger.debug(data)
        logger.debug(self.session.headers)

        for i in range(retry):
            try:
                if headers:
                    self.set_headers(headers)
                result = self.session.post(url, params=params, data=data, timeout=(3, 12),
                                           verify=False, allow_redirects=redirects)
                if result.status_code < 400:
                    if 'Set-Cookie' in result.headers:
                        logger.warning(result.headers['Set-Cookie'])
                        simple_cookie = SimpleCookie(result.headers['Set-Cookie'])
                        for item in simple_cookie:
                            self.session.cookies.update({item: simple_cookie[item].value})
                    logger.debug(self.session.cookies.get_dict())
                    logger.debug(result.content)
                    return {'text': result.text, 'headers': result.headers}
                else:
                    logger.warning("HttpStatusCode %d", result.status_code)
            except requests.exceptions.ConnectTimeout:
                logger.warning('requests.exceptions.ConnectTimeout')
            except requests.exceptions.ReadTimeout:
                logger.warning('requests.exceptions.ReadTimeout')
            except requests.exceptions.Timeout:
                logger.warning('requests.exceptions.Timeout')
            except requests.exceptions.ProxyError:
                logger.warning('requests.exceptions.ProxyError')
            except Exception as e:
                logger.warning('Post Other Exception Occur, err=[%s]', e, exc_info=True)
            time.sleep(2)
        return False
