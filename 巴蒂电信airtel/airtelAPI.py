import  json
import  time
import random
import base64
import time
import hashlib
import random
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.backends import default_backend
import  requests
from http.cookiejar import MozillaCookieJar
from fake_useragent import UserAgent
from bs4 import  BeautifulSoup
import re

# 保持会话
def get_session():
    requests.packages.urllib3.disable_warnings()
    session = requests.Session()
    session.cookies = MozillaCookieJar()
    return session

def des_decrypt(key, content, pad):
    ciphertext = base64.b64decode(content)
    algorithm = algorithms.TripleDES(key[:8].encode())
    cipher = Cipher(algorithm, modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    data = decryptor.update(ciphertext)
    print(data)
    return data.rstrip(pad).decode()

def sha1_encrypt(content):
    return hashlib.sha1(content.encode()).hexdigest()

def des_encrypt(key, content, pad):
    if not isinstance(content, bytes):
        content = content.encode()
    content += pad * (8 - len(content) % 8)
    algorithm = algorithms.TripleDES(key[:8].encode())
    cipher = Cipher(algorithm, modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    data = encryptor.update(content)
    _data = base64.b64encode(data).decode()
    return _data

def get_adsheader():
    localtime = time.localtime(time.time())
    t = str(localtime.tm_year - 1900) + str(localtime.tm_mon - 1) + str(localtime.tm_mday) + \
        str(localtime.tm_hour) + str(localtime.tm_min) + str(localtime.tm_sec) + str(random.randint(0, 1000))
    return (t + str(random.random())).replace('.', '')

def error_handler(data):
    """1、Oops! The OTP you have keyed in is invalid. Please try again.
       2、airtel: Prepaid | Postpaid | Broadband | 4G | DTH Services in India
       3、The mobile number or password is incorrect, please try again.
       4、Please enter a valid 10 digit airtel mobile number. Numbers starting with 0,1,3,4 are not valid
       5、Sorry! Your request could not be processed at the moment. Please try again later.
    """

    if data:
        if "INVALID_RTN" in str(data):
            JsonData = json.loads(data)
            ErrorMessage = JsonData['message']
            print("ErrorMessage is:",ErrorMessage)
            return ErrorMessage

    else:
        check_user_Errorflags = "Oops! The OTP you have keyed in is invalid. Please try again."
        return check_user_Errorflags
    pass

def check_user(user):
    #输入预处理,识别OTP长度
    if len(user) == 10:
        adsheader = get_adsheader()
        print("adsheader is:", adsheader)
        session = get_session()
        url = 'https://www.airtel.in/as/app/wl-service/airtel-digital-profile/rest/customer/authapp/v1/checkuser'
        headers = {
            'Host': 'www.airtel.in',
            'Connection': 'keep-alive',
            'Content-Length': '64',
            'Origin': 'https://www.airtel.in',
            'User-Agent': UserAgent().random,
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
        data_encrypt = des_encrypt(key=adsheader, content=data, pad=b'\x08')
        print("data_encrypt:", data_encrypt)
        res = session.post(url=url, headers=headers, data=data_encrypt, verify=False)
        # print(res)
        print(res.status_code)
        data = res.text
        print("data:", data)
        check_user_Errorflags = error_handler(data)
        if check_user_Errorflags:
            return check_user_Errorflags

        print("####################################")
        # Rerror = session.get("https://www.airtel.in/common/paymentBank/index.html")
        # print(Rerror.text)
        googlecookie = res.headers['googleCookie']
        print("googlecookie is:",googlecookie)
        text = des_decrypt(key=googlecookie, content=data, pad=b'\x04')
        return text, session

    #识别OTP长度
    else:
        dict = {}
        error_dict = {}
        dict['errorInfo'] = "Please enter a valid 10 digit airtel mobile number.Numbers starting with 0,1,3,4 are not valid"
        error_dict['comments'] = dict
        return error_dict

def auth_login(requestkey, session):
    adsheader = get_adsheader()

    url = 'https://www.airtel.in/as/app/wl-service/airtel-digital-profile/rest/customer/authapp/v1/authlogin'
    headers = {
        'Host': 'www.airtel.in',
        'Connection': 'keep-alive',
        'Origin': 'https://www.airtel.in',
        'User-Agent': UserAgent().random,
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
    data_encrypt = des_encrypt(key=adsheader, content=data, pad=b'\x05')
    res = session.post(url=url, headers=headers, data=data_encrypt, verify=False)
    # googlecookie = res.headers['googleCookie']
    # text = des_decrypt(key=googlecookie, content=res.text, pad=b'\x04')
    return session

def login_interface(user, password, requestkey,session):
    url = 'https://www.airtel.in/as/pkmslogin.form'
    headers = {
        'Host': 'www.airtel.in',
        'Cache-Control': 'max-age=0',
        'Origin': 'https://www.airtel.in',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': UserAgent().random,
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

    res = session.post(url=url, headers=headers, data=data, verify=False)
    # result = res.text
    # print(result)
    return session

#检测check_user 是否OK
def check_user_OK(checkInfo):
    print("checkInfo is:", checkInfo)
    if "keyed in is invalid" in checkInfo:
        return checkInfo

    if "Provided number is not valid RTN" in checkInfo:
        return checkInfo

def Run_airteLogin( user, password):
    checkInfo = check_user(user)
    print("checkInfo:",checkInfo)
    Error = check_user_OK(checkInfo)
    if Error:
        return Error

    else:
        res = checkInfo[0]
        session = checkInfo[1]
        # res, session = check_user(user)
        requestkey = json.loads(res)['requestkey']
        # print("requestkey:", requestkey)
        # session = auth_login(requestkey,session)
        session = login_interface(user, password, requestkey, session)
        return  session

#获取预付费的信息
def get_prepaidInfo(user, session):

    adsheader = get_adsheader()
    adsheader = sha1_encrypt(adsheader)
    # print("adsheader 2:",adsheader)
    url = 'https://www.airtel.in/s/app/wl-service/airtel-usage/rest/prepaid/usage/recharge/v2/details/fetch?'
    params = {'siNumber': user}
    headers = {
        'Host': 'www.airtel.in',
        'Accept': 'application/json, text/plain, */*',
        'googleCookie': 'airtel.com',
        'adsHeader': adsheader,
        'User-Agent': UserAgent().random,
        'requesterId': 'WEB',
        'Referer': 'https://www.airtel.in/s/selfcare/prepaid/%s/packsAndService'%(user),
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    res = session.get(url=url, headers=headers, params=params)
    # print(res)
    googlecookie = res.headers['googleCookie']
    text = des_decrypt(key=googlecookie, content=res.text, pad=b'\x02')
    JsonData_ = json.loads(text)
    # print("JsonData is:",JsonData_)
    #解析数据
    # dict = {}
    # dict["balance"] = JsonData['rechargeOverview']['balance']
    # tempData = JsonData['rechargeOverview']['prepaidValidity']
    # dict["INCOMINGSTOPSIN"] = str(tempData['validityDays']) + " " + tempData['validityDaysUnit']
    # tempData = JsonData['usageOverview']['prepaidUsages']
    # dict["Internet"] = str(tempData[0]['available']) + " " + tempData[0]['unit']
    # dict["Talk"] = str(tempData[1]['available']) + " " + tempData[1]['unit']
    # dict["SMS"] = str(tempData[2]['available']) + " " + tempData[2]['unit']

    #主要的部分
    adsheader = get_adsheader()
    adsheader = sha1_encrypt(adsheader)
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'adsHeader': adsheader,
        'Connection': 'keep-alive',
        'googleCookie': 'airtel.com',
        'Host': 'www.airtel.in',
        'User-Agent': UserAgent().random,
        'requesterId': 'WEB',
        'Referer': 'https://www.airtel.in/s/selfcare/prepaid/%s/packsAndService'%(user),
    }
    url = "https://www.airtel.in/s/app/wl-service/airtel-digital-profile/rest/customer/profile/v1/product/detail/fetch?"
    params = {
        'lob':'MOBILITY',
        'siNumber':user,
        'skipCrmDetails':'true'
    }

    device_response = session.get(url=url, params=params, headers = headers, verify=False)
    googlecookie = device_response.headers['googleCookie']
    text = des_decrypt(key=googlecookie, content=device_response.text, pad=b'\x06')
    JsonData = json.loads(text)

    for key in JsonData_:
        # print(JsonData_[key])
        JsonData[key] = JsonData_[key]

    return JsonData



mobileNumber = "8861359470"
# mobileNumber = "8861359479"
password = "qwertyui12"
session = Run_airteLogin(mobileNumber, password)
text = get_prepaidInfo(mobileNumber,session)
print("最后的结果##################3")
print(text)
