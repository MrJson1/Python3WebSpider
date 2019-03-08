# -*- coding: utf-8 -*-
# @Time    : 2019/02/28 13:57
# @Author  : Haley

import base64
import time
import hashlib
import random
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.backends import default_backend


class Crypto(object):
    def __init__(self):
        self.aes_key = b''
        self.aes_iv = b''
        self.des_key = b'ac709bbbee58f2f43b6ec0667e34df067f96a10d'
        self.des_iv = b''

    def aes_decrypt(self, content):
        content = base64.b64decode(content)
        cipher = Cipher(algorithms.AES(self.aes_key), modes.CBC(self.aes_iv), backend=default_backend())
        decryptor = cipher.decryptor()
        data = decryptor.update(content)
        return data.rstrip(b'\x06').decode()

    def aes_encrypt(self, content):
        if not isinstance(content, bytes):
            content = content.encode()
        content += b'\x07' * (16 - len(content) % 16)
        cipher = Cipher(algorithms.AES(self.aes_key), modes.CBC(self.aes_iv), backend=default_backend())
        encryptor = cipher.encryptor()
        data = encryptor.update(content)
        _data = base64.b64encode(data).decode()
        return _data

    def des_decrypt(self, key, content, pad):
        ciphertext = base64.b64decode(content)
        algorithm = algorithms.TripleDES(key[:8].encode())
        cipher = Cipher(algorithm, modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        data = decryptor.update(ciphertext)
        return data.rstrip(pad).decode()

    def des_encrypt(self, key, content, pad):
        if not isinstance(content, bytes):
            content = content.encode()
        content += pad * (8 - len(content) % 8)
        algorithm = algorithms.TripleDES(key[:8].encode())
        cipher = Cipher(algorithm, modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        data = encryptor.update(content)
        _data = base64.b64encode(data).decode()
        return _data

    def get_adsheader(self):
        localtime = time.localtime(time.time())
        t = str(localtime.tm_year - 1900) + str(localtime.tm_mon-1) + str(localtime.tm_mday) + \
            str(localtime.tm_hour) + str(localtime.tm_min) + str(localtime.tm_sec) + str(random.randint(0, 1000))
        return (t + str(random.random())).replace('.', '')

    def sha1_encrypt(self, content):
        return hashlib.sha1(content.encode()).hexdigest()


# print(Crypto().des_decrypt('db7ac8fa02edb75db90d079e6c2c23b516cab4c8', 'LHX3Kkc+r11UrWyOzQ3xsI4FNtin+g4RE/7KfKNozFHeojXpe1aPUw5tS+FFGMELGB0mTkyzhqaK5a075IAkSwvjYnfTAp8uSO9RH2iosT4avHyB79jDDO/JQBsEDW3cbiARewcu5muCpqdVMg9LsOBqTbO/ddfpm1LqVIXoBao6DOPsPU/SznnMlDdkBakWkYLOoWBVe+RG+KAAPDEiOhoKVNF/pv5QQC8yOZL7OPbYr0mPmKnf8sc/nlbzPXsfObACsXgkD62Wqxq0S3JqX8XYZ42hcRPQdBSltmn+PhTWQ+G5wSVcxihv9ZjFCQu6K07eUYdKJGmk2YrlgkdtMYxjQdApzC70XiHwSZV39OSXNV0jBiSaQoi77p2voVGUafydnoMaad86DOPsPU/Szgn59lj9r9OmrRqNCD8zQcgLN1BdDfFRW9wImaHs0YEc8pohWVh4Toh479HbUmLeY+A7fEH3jOlL/zut3hiAJaHKKMppLWPAkZ3sk1a2vcccl1AYxtHgQBS3P70m5JdIDyeTXneOoxT9W3Y5E269Yivjyk2N69M9k2FW91wOa61S6zTjJ3Rqh0kctGrGxH9qb4sv4Xu55oU3WZxnpYvEFPlyiAMj6dcsZnLHsCc4V4tzCWZxnXS2dsxCg7gYyj4ezaHwXG+HqiITuiOym1d32xm41dlwDN84PzcN0zsoYniGN8z6jKEjR0/CztQfsdotU+ELSka3+ysSOIUnhuqSZgPmIkhY6X0K6T+ddxFRn0qtL77SR8PkeB874kMuPd0oLY+9c6YH2REDMHUzddiGhnE8t7ZRbc0FGmklzayyTtSKqkWb7p7PG0HRkbaoiuDksZAJ02EjXpuQeqCPRXsfSKcczzkDrCTjuQ/WR5dDfT3w5wljVoLBvN3X3Hi1jEpJ3of0U+DkAJGH1TnH/KEkWzU3t9hRvX6KEMdSDM0ftxa8tVR3qM5Udgt2xnkD3NJz3Kq8H3SeioZAs5sm020VDsKwn8O4To3e6TNxMsoreOJdWA5NxOHXQpQIYTip3BYbw8QhPpS+22abxqY5yKM+QcXlTmRgAXavRVHjwt9j6zUhr75p5oCcM8R3u78Sp/iajsxiLH5M89k0GduG5n+3dc/NIPLZtZuaoLQP952RfH08n7eHZqJ8NCUWJIBfLLv3e+TQy64zsfdodXd6M/7svVFdwwUmKtIr9bZqPvB+BIrF/N5pECcYk0gXuJZXJRenEzsESKmzJzj6kYLOoWBVe+RzDX1wkllesj4bMrXoC4h6fSDRqK1oTxgQ6TfcVm4wSO883DRN/5tqR9Xy9TuRcFpYObj8XFvz8u10oVQYndSPkjfNQIoqaOEfuo7m7+xT5tQtqEZxDXS6g+p0KsvsvVWf7nn8FkAwgCEwxRVuY4LCjRpgH5XstVk8ViXAEvW7ZhqebzQw2yvF0o9g6S4HKqLmLpiUYzrnBW8UZotvEmWT7O2+7iSAioxJuffa04P0LkP+uG5s72rk6m6AtVI2te3zwSDUtg6Znu9nShYmudE2Nbhn+caUSklFqX9kb03bgTd0TsX8kV/vnyebRm8a6ADQtz6lGTPYwp/tPkCanqxpA3wIkKrqw92a4qsbUmYVQFfc37pbkZ5eaAVvkI/6NYO/8kfhd3RtPOXgfPqkr3jXe+wUE/zmdGQ="', b'\x02'))
# print(Crypto().sha1_encrypt('2222'))