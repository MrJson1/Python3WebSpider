import requests
import json
from bs4 import BeautifulSoup
from http.cookiejar import MozillaCookieJar
import re
from fake_useragent import UserAgent

#保持会话
def getSession():
    session = requests.session()
    session.cookies = MozillaCookieJar()
    return session

#获取网关ID
def getTransactionID():
    session = getSession()

    headers_info = {"Content-Type": "application/json;charset=utf-8",
                    "qt_agency_id": "ac8584d2-a1b7-4b99-a021-2d9a6819226e",
                    "qt_api_key": "822a256d-8192-4803-8598-72b48d1af4c0"}

    Basepan = 'https://preprod.aadhaarapi.com'
    url_pan = Basepan + '/gateway/creditscore/init/'
    # print("url_pan:",url_pan)

    data = {
        "purpose": "01",
        "response_url": "http://139.159.217.146:500/callback/",
        "pdf_report": "N",
        "format": "json"
    }

    data = json.dumps(data)
    # print("data:",data)

    handel_pan_result = session.post(url=url_pan, data=data, headers=headers_info).text
    # print(handel_pan_result)
    trad_id_json = json.loads(handel_pan_result)
    transaction_id = trad_id_json["id"]
    print("transaction_id:", transaction_id)
    return transaction_id,session

#发送OTP
def SendOTP_AND_GetOTP(session,transaction_id,phoneNumber):
    #2、发送OTP
    headrs = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'content-type': 'application/json; charset=UTF-8',
        'x-quagga-gateway-open': 'y',
        'x-quagga-sdk': 'web_sdk_v2.1',
        'x-quagga-source': 'WEB',
    }

    phone_data = {
        'phone': phoneNumber
    }

    data = json.dumps(phone_data)
    Senturl = 'https://preprod.aadhaarapi.com/gateway/auth/creditscore/%s/self' % transaction_id
    print("发送OTP URL的请求",Senturl)
    response = session.post(Senturl, data=data, headers=headrs)
    responseHtml = response.text
    responseData = json.loads(responseHtml)
    # print("responseHtml:",responseData)

    returnDict = {}

    #识别手机号码
    HandleError = Handle_Error(responseData)
    if HandleError:
        dict = {}
        print("识别手机号码 HandleError:",HandleError)
        dict['errorInfo'] = str(HandleError)
        returnDict['comments'] = dict
        return returnDict
    """
    {"id":"7d78ae05-a98e-4669-baf4-9c47f94d2590",
    "email":null,"phone":"6360773973","email_validated":"N","phone_validated":"Y","account_status":"ACTIVE"}
    """
    print("已经发送OTP")

    #3、获取otp,并且验证,实现登录
    OTP = input("请输入OTP:")


    returnDict["OTP"] = OTP
    returnDict["session"] = session
    return returnDict

#实现登录并且获取参数
def Login_And_GetCsrf(transaction_id,OTP,session):
    url = "https://preprod.aadhaarapi.com/gateway/auth/%s/creditscore/login/localotp" % transaction_id
    print("login url:", url)
    path = "/gateway/auth/%s/creditscore/login/localotp" % transaction_id
    print("path:",path)
    headrs = {
        'authority': 'preprod.aadhaarapi.com',
        'method': 'POST',
        'path': path,
        'scheme': 'https',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9',
        'content-type':'application/json; charset=UTF-8',
        'origin':'https://preprod.aadhaarapi.com',
        'user-agent':UserAgent().random,
        'x-quagga-gateway-open':'y',
        'x-quagga-sdk':'web_sdk_v2.1',
        'x-quagga-source':'WEB',
        'x-requested-with':'XMLHttpRequest',
    }

    post_otp = {
        'otp': OTP,
        'phone': phoneNumber,
        'transaction_type':'creditscore'
    }
    post_otp = json.dumps(post_otp)

    res = session.post(url=url, data=post_otp, headers=headrs)
    result = res.text
    print("login 后的结果：",result)
    json_result = json.loads(result)
    #识别OTP
    HandleError = Handle_Error(json_result)
    if HandleError:
        print("识别OTP HandleError:", HandleError)
        exit(-1)

    else:
        redirectURL = json_result["redirectURL"]
        print("redirectURL:", redirectURL)

        base_url = 'https://preprod.aadhaarapi.com'
        logined_url = base_url + redirectURL
        print("logined_url:", logined_url)
        """https://preprod.aadhaarapi.com/gateway/creditscore/fc1c7772-1580-4026-805a-574a4bb519a9"""

        response = session.get(url=logined_url)
        html = response.text
        print(response.url)  # https://preprod.aadhaarapi.com/gateway/creditscore/721be145-0591-4c11-8da9-1991cb3e4c92
        # print("response:", html)
        soup = BeautifulSoup(html, 'html.parser')
        csrf = soup.find_all('input', id='csrf')[0].attrs['value']
        print("csrf:",csrf)
        return csrf, session, path

#处理的第一步
def getStepOne_post_parameter(phoneNumber):
    #获取ID
    transaction_id, session = getTransactionID()
    #构建url
    baseUrl = "https://preprod.aadhaarapi.com/gateway/auth/creditscore/"
    suffixUrl = "?&company_display_name=Your%20Company%20Name&color_bg=2C3E50&color_ft=FFFFFF&logo_url=https://akta.org/wp-content/uploads/2015/02/sponsorship-fpo.gif&full_name=SATHISHKUMAR%20%20M%20%20%20%20SATHISH%20KU&address_line=223%20NACHIANNAN%20ANGANNAN%20STREET%20%20RAMANATHAPURAM%20COIMBATORE&state=TN&postal=641045&dob=1986-06-03&pan_number=BUXPS2681D&phone=User%20Contact%20Number"
    gatewayUrl = baseUrl + transaction_id + suffixUrl
    print("gatewayUrl:",gatewayUrl)
    Way_response = session.get(url=gatewayUrl)
    # print("Way_response:",Way_response.text)
    print("##########################################")

    #发送OTP并且获取OTP
    # OTP, session = SendOTP_AND_GetOTP(session,transaction_id,phoneNumber)
    returnDict = SendOTP_AND_GetOTP(session,transaction_id,phoneNumber)
    # print("returnDict:", returnDict)

    #有错误的情况
    if "errorInfo" in str(returnDict):
        # print("eerror:",returnDict)
        return returnDict

    #正常情况
    else:
        OTP = returnDict["OTP"]
        session = returnDict["session"]
        # 实现登录并且获取csrf
        csrf, session, path = Login_And_GetCsrf(transaction_id, OTP, session)

        return_Dict = {}
        return_Dict["csrf"] = csrf
        return_Dict["session"] = session
        return_Dict["transaction_id"] = transaction_id
        return_Dict["path"] = path
        return return_Dict

        # return csrf, session, transaction_id, path

#获取征信值
def GetCreditScoreData(phoneNumber):
    # csrf, session, transaction_id, path = getStepOne_post_parameter(phoneNumber)
    return_Dict = getStepOne_post_parameter(phoneNumber)
    #有错误的情况
    if "errorInfo" in str(return_Dict):
        print(return_Dict)
        return return_Dict

    #正确的情况
    else:
        csrf = return_Dict["csrf"]
        session = return_Dict["session"]
        transaction_id = return_Dict["transaction_id"]
        path = return_Dict["path"]
        baseUrl = "https://preprod.aadhaarapi.com/gateway/creditscore/"
        creditscoreUrl = baseUrl + transaction_id
        print("creditscoreUrl:",creditscoreUrl)
        """https://preprod.aadhaarapi.com/gateway/creditscore/0cb88436-bc0c-402f-a63b-681ccdc69db1"""

        headrs = {
            'authority': 'preprod.aadhaarapi.com',
            'method': 'POST',
            'path': path,
            'scheme': 'https',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.9',
            'content-type':'application/json; charset=UTF-8',
            'csrf-token':csrf,
            'origin':'https://preprod.aadhaarapi.com',
            'referer':'https://preprod.aadhaarapi.com/gateway/creditscore/%s' % transaction_id,
            'user-agent':UserAgent().random,
            'x-quagga-gateway-open':'y',
            'x-quagga-sdk':'web_sdk_v2.1',
            'x-quagga-source':'WEB',
            'x-requested-with':'XMLHttpRequest',
        }

        PayLoadData = {
            "": "Get Credit Score",
            'DOB': "1986-06-03",
            'address_line': "223 NACHIANNAN ANGANNAN STREET  RAMANATHAPURAM COIMBATORE",
            'consent': 'true',
            'customer_panNumber': "BUXPS2681D",
            'full_name': "SATHISHKUMAR  M    SATHISH KU",
            'mobile_phone': phoneNumber,
            'postal': "641045",
            'state': "TN",
            '_csrf': csrf
        }
        FormData = json.dumps(PayLoadData)
        response = session.post(url=creditscoreUrl, headers=headrs, data=FormData)
        returnData = response.text
        returnData = json.loads(returnData)
        print("returnData:",returnData)

        return returnData

#错误处理器
def Handle_Error(responseData):
    #识别手机号Invalid Phone Number
    InvalidFlag = "message"
    Invalid_Flag = re.search(InvalidFlag, str(responseData), re.S)
    if Invalid_Flag:
        HandleError = responseData['message']
        return HandleError


if __name__ == '__main__':
    phoneNumber = "9380453065"
    # phoneNumber = "6360773973"
    return_Dict = GetCreditScoreData(phoneNumber)
    print("最后的结果#####################")
    print(return_Dict)



