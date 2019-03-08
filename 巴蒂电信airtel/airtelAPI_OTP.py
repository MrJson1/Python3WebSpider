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

#解密函数
def des_decrypt(key, content, pad):
    ciphertext = base64.b64decode(content)
    algorithm = algorithms.TripleDES(key[:8].encode())
    cipher = Cipher(algorithm, modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    data = decryptor.update(ciphertext)
    print(data)
    return data.rstrip(pad).decode()

#加密函数一
def sha1_encrypt(content):
    return hashlib.sha1(content.encode()).hexdigest()

#加密函数二
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

#获取加密的key
def get_adsheader():
    localtime = time.localtime(time.time())
    t = str(localtime.tm_year - 1900) + str(localtime.tm_mon - 1) + str(localtime.tm_mday) + \
        str(localtime.tm_hour) + str(localtime.tm_min) + str(localtime.tm_sec) + str(random.randint(0, 1000))
    return (t + str(random.random())).replace('.', '')

#错误函数处理
def error_handler(data):
    """1、Oops! The OTP you have keyed in is invalid. Please try again.
       2、airtel: Prepaid | Postpaid | Broadband | 4G | DTH Services in India
       3、The mobile number or password is incorrect, please try again.
       4、Please enter a valid 10 digit airtel mobile number. Numbers starting with 0,1,3,4 are not valid
       5、Sorry! Your request could not be processed at the moment. Please try again later.
    """
    ErrorDict = {}

    if data:
        if "INVALID_RTN" in str(data):
            JsonData = json.loads(data)
            ErrorMessage = JsonData['message']
            print("ErrorMessage is:",ErrorMessage)
            ErrorDict['errorInfo'] = ErrorMessage
            return ErrorDict

    else:
        check_user_Errorflags = "Oops! The OTP you have keyed in is invalid. Please try again."
        ErrorDict['errorInfo'] = check_user_Errorflags
        return ErrorDict
    pass

#检测用户
def check_user(user):
    #输入预处理,识别OTP长度
    if len(user) == 10:
        adsheader = get_adsheader()
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
        # print("data_encrypt:", data_encrypt)
        res = session.post(url=url, headers=headers, data=data_encrypt, verify=False)
        # print(res)
        # print(res.status_code)
        data = res.text
        ErrorDict = error_handler(data)
        if ErrorDict:
            return ErrorDict

        print("####################################")
        googlecookie = res.headers['googleCookie']
        text = des_decrypt(key=googlecookie, content=data, pad=b'\x04')
        # print("succeed text:", text)
        return text, session

    #识别OTP长度
    else:

        error_dict = {}
        error_dict['errorInfo'] = "Please enter a valid 10 digit airtel mobile number.Numbers starting with 0,1,3,4 are not valid"
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

#发送OTP
def generate_otp(requestkey, session):
    adsheader = get_adsheader()
    url = 'https://www.airtel.in/as/app/wl-service/airtel-digital-profile/rest/customer/authapp/v1/generateotp'
    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'adsHeader': adsheader,
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'googleCookie': 'airtel.com',
        'Host': 'www.airtel.in',
        'Origin': 'https://www.airtel.in',
        'Referer': 'https://www.airtel.in/s/selfcare?normalLogin',
        'User-Agent': UserAgent().random,
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {"requestkey": requestkey}
    data = json.dumps(data, separators=(',', ':'))
    data_encrypt = des_encrypt(key=adsheader, content=data, pad=b'\x04')
    print("OTP  data_encrypt:",data_encrypt)
    res = session.post(url=url, headers=headers, data=data_encrypt, verify=False)
    print(res)
    print(res.text)
    googlecookie = res.headers['googleCookie']

    #分2种情况一种发送OTP没有限制
    try:
        text = des_decrypt(key=googlecookie, content=res.text, pad=b'\x04')
        JsonData = json.loads(text)
        SentResult = JsonData['result']
        print("SentResult :",SentResult)
        print()
        return session

    #发送OTP已经被限制  LIMIT_REACHED_DAY
    except:
        text = des_decrypt(key=googlecookie, content=res.text, pad=b'\x07')
        JsonData = json.loads(text)
        SentResult = JsonData['result']
        print("NOT  SentResult :", SentResult)
        ErrorDict = {}
        prompt = "Sorry! You have reached the maximum limit for requesting an OTP. Please try again later."
        ErrorDict['errorInfo'] = prompt + SentResult
        return ErrorDict

#主界面
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

    if "errorInfo" in checkInfo:
        print("有错误信息：",checkInfo)
        return checkInfo

    # try:
    #     result = checkInfo[0]
    #     if "TRUE" == result:
    #         return "Success"
    # except:
    #     print("其它错误信息异常checkInfo is:", checkInfo)
    # if "keyed in is invalid" in checkInfo:
    #     return checkInfo
    #
    # if "Provided number is not valid RTN" in checkInfo:
    #     return checkInfo

#识别OTP
def validateuserwithotp(otp, session, requestkey):
    resultFalg = {}
    #识别OTP长度
    if len(otp) != 4:
        resultFalg['errorInfo'] = "Please enter a four-digit OTP"
        return resultFalg

    adsheader = get_adsheader()
    url = 'https://www.airtel.in/as/app/wl-service/airtel-digital-profile/rest/customer/authapp/v1/validateuserwithotp'
    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'adsHeader': adsheader,
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'googleCookie': 'airtel.com',
        'Host': 'www.airtel.in',
        'Origin': 'https://www.airtel.in',
        'Referer': 'https://www.airtel.in/s/selfcare?normalLogin',
        'User-Agent': UserAgent().random,
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {"otp":otp,"requestkey":requestkey}
    data = json.dumps(data, separators=(',', ':'))
    data_encrypt = des_encrypt(key=adsheader, content=data, pad=b'\x07')
    print("validateuserwithotp  data_encrypt:",data_encrypt)
    res = session.post(url=url, headers=headers, data=data_encrypt, verify=False)
    print(res)
    googlecookie = res.headers['googleCookie']
    print("validateuserwithotp googlecookie is:", googlecookie)

    #正常情况SUCCESS_AIRTEL
    try:
        text = des_decrypt(key=googlecookie, content=res.text, pad=b'\x02')
        JsonData = json.loads(text)
        print("validateuserwithotp JsonData:", JsonData)
        return session

    # 1、识别失败情况INCORRECT
    # 2、能发送成功但是识别失败情况 {"result":"LIMIT_REACHED_DAY","requestkey":"zuul_886135947853949d46-6f71-4ebd-a952-7b40b8727653"}

    except:
        text = des_decrypt(key=googlecookie, content=res.text, pad=b'\x07')
        JsonData = json.loads(text)
        print("validateuserwithotp failed JsonData:", JsonData)
        resultError = JsonData['result']

        #识别失败情况INCORRECT
        if "INCORRECT" == resultError:
            # resultFalg['errorInfo'] = "validateuserwithotp result is " + resultError
            resultFalg['errorInfo'] = "The mobile number or password is incorrect, please try again."
            return resultFalg

        #能发送成功但是识别失败情况
        prompt = "Sorry! You have reached the maximum limit for requesting an OTP. Please try again later."
        resultFalg['errorInfo'] = prompt + "The send succeeded but the validateuserwithotp failed result:" + resultError
        return resultFalg


def authloginget(session,requestkey):
    adsheader = get_adsheader()
    # adsheader = sha1_encrypt(adsheader)
    # print("adsheader 2:",adsheader)
    url = 'https://www.airtel.in/as/app/wl-service/airtel-digital-profile/rest/customer/authapp/v1/authloginget?'
          # 'requestkey=zuul_886135947066d289f3-fe1d-4772-9ea6-970d462a0f04&_=1551835036118'
    params = {
        'requestkey': requestkey,
        '_': ''
    }
    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'adsHeader': adsheader,
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'googleCookie': 'airtel.com',
        'Host': 'www.airtel.in',
        'Referer': 'https://www.airtel.in/s/selfcare?normalLogin',
        'User-Agent': UserAgent().random,
        'X-Requested-With': 'XMLHttpRequest',
    }

    res = session.get(url=url, headers=headers, params=params, verify=False)
    #错误{"code":"UNAUTHORIZED","message":"UnAuthorized - OTP/Hint Invalid"}
    googlecookie = res.headers['googleCookie']
    text = des_decrypt(key=googlecookie, content=res.text, pad=b'\x02')
    JsonData_ = json.loads(text)
    print(11)
    print(JsonData_)

    #登录
    # adsheader = get_adsheader()
    # adsheader = sha1_encrypt(adsheader)
    # print("adsheader 2:",adsheader)
    url = 'https://www.airtel.in/s/selfcare?normalLogin'
          # 'requestkey=zuul_886135947066d289f3-fe1d-4772-9ea6-970d462a0f04&_=1551835036118'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'www.airtel.in',
        'Referer': 'https://www.airtel.in/s/selfcare?normalLogin',
        'User-Agent': UserAgent().random,
        }

    res = session.get(url=url, headers=headers, verify=False)
    print(22)
    print(res)
    print(res.text)
    # googlecookie = res.headers['googleCookie']
    # text = des_decrypt(key=googlecookie, content=res.text, pad=b'\x02')
    # JsonData_ = json.loads(text)
    # print(JsonData_)
    return session

#主函数
def Run_airteLogin_getData(user):
    # 返回dict
    error_dict = {}
    checkInfo = check_user(user)
    print("处理过的checkInfo:",checkInfo)
    Error = check_user_OK(checkInfo)
    #处理错误信息
    if Error:
        error_dict['comments'] = Error
        return error_dict

    #无错误继续下一步
    else:
        res = checkInfo[0]
        session = checkInfo[1]
        requestkey = json.loads(res)['requestkey']
        #发送OTP,判断发送OTP次数是否受到限制
        otpFlag = generate_otp(requestkey,session)
        if "errorInfo" in str(otpFlag):
            error_dict['comments'] = otpFlag
            return error_dict

        # 发送otp成功情况   otpFlag保持会话标识
        else:
            # session = otpFlag
            otp = input("请输入OTP:")
            # 识别OTP
            resultFalg = validateuserwithotp(otp, otpFlag, requestkey)
            if "errorInfo" in str(resultFalg):
                error_dict['comments'] = resultFalg
                return error_dict

            # session = auth_login(requestkey,session)
            session = authloginget(resultFalg, requestkey)
            print("########################################################")
            # session = login_interface(user, otp, requestkey, session)
            resultData = get_prepaidInfo(mobileNumber, session)
            return resultData

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
# mobileNumber = "9108680638"
# mobileNumber = "9108680639"
# mobileNumber = "8861359478"
# mobileNumber = "8861359477"
# mobileNumber = "8861359471"
resultData = Run_airteLogin_getData(mobileNumber)
print("#####################################最后结果")
print(resultData)