# coding:utf-8

import re
from http.cookiejar import MozillaCookieJar
import requests
from bs4 import BeautifulSoup
import base64
from fake_useragent import UserAgent
import time
import json
import boto3

#保持会话
def get_browser():
    requests.packages.urllib3.disable_warnings()
    session = requests.Session()
    session.cookies = MozillaCookieJar()
    return session

#获取post请求参数
def get_post_parameter(browser):
    login_url = "https://parivahan.gov.in/rcdlstatus/?pur_cd=101"
    headers = {"User-Agent": UserAgent().random}
    response = browser.get(login_url, headers=headers, verify=False)
    soup = BeautifulSoup(response.content.decode(), "html.parser")
    try:
        get_javax_faces_ViewState = soup.select("form#form_rcdl input")[-1]["value"]
        captureVal = soup.select("div table td input")[0]["name"]
        check = soup.select("div.container div div button")[0]["name"]
        # 验证码url
        url = soup.select("table.vahan-captcha.inline-section img")[0]["src"]
        captcha_Url = "https://parivahan.gov.in" + url
        # # print(get_javax_faces_ViewState)
        # print(captureVal)
        # print(check)
        # # print(captcha_Url)
        return get_javax_faces_ViewState, captureVal, check, captcha_Url

    except:
        print("获取参数不对网站已经更新！！！！")
        exit(-1)

#验证码处理器
# def captcha_processer(captcha_Url,browser):
    #调用识别验证码服务器
    # url = "http://127.0.0.1:19952/captcha/v1"
    # def request_1(img_bytes,browser):
    #     captcha_1 = browser.post(url, json={'image': base64.b64encode(img_bytes).decode()}).json()['message']
    #     return captcha_1
    #
    # response_captcha = browser.get(captcha_Url)
    # captcha_bytes = response_captcha.content
    # captcha = request_1(captcha_bytes,browser)
    # print(captcha)
    #
    # return captcha

#登录
def Login_parivahan(number, birthday,report_id):
    browser = get_browser()
    User_Agent = UserAgent().random
    get_javax_faces_ViewState, captureVal, check, captcha_Url = get_post_parameter(browser)
    # captcha = captcha_processer(captcha_Url,browser)
   
    #共同的post url
    post_url = "https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml"
    headers_1 = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Faces-Request": "partial/ajax",
        "Referer": "https://parivahan.gov.in/rcdlstatus/?pur_cd=101",
        "Host": "parivahan.gov.in",
        "Origin": "https://parivahan.gov.in",
        "User-Agent": User_Agent
    }

    formData_1= {
        "form_rcdl": "form_rcdl",
        "form_rcdl: tf_dlNO": number,
        "form_rcdl: tf_dob_input": birthday,
        # "form_rcdl:j_idt33:CaptchaID":captcha,
        "javax.faces.ViewState": get_javax_faces_ViewState,
        "javax.faces.source": captureVal,
        "javax.faces.partial.event": "blur",
        "javax.faces.partial.execute": captureVal,
        "javax.faces.partial.render": captureVal,
        "CLIENT_BEHAVIOR_RENDERING_MODE": "OBSTRUSIVE",
        "javax.faces.behavior.event": "blur",
        "javax.faces.partial.ajax": "true"
    }

    response_1 = browser.post(post_url, data=formData_1, headers=headers_1)

    messages = handle_error(response_1.content.decode(), 0)
    
    
    
    if messages == "success":
        formData_2 = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": check,
            "javax.faces.partial.execute": "@all",
            "javax.faces.partial.render": "form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl",
            check: check,
            "form_rcdl": "form_rcdl",
            "form_rcdl:tf_dlNO": number,
            "form_rcdl:tf_dob_input": birthday,
            "javax.faces.ViewState":get_javax_faces_ViewState,
            # "form_rcdl:j_idt33:CaptchaID":captcha

        }

        headers_2 = {
            "Accept": "application/xml, text/xml, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Faces-Request": "partial/ajax",
            "Referer": "https://parivahan.gov.in/rcdlstatus/?pur_cd=101",
            "Host": "parivahan.gov.in",
            "Origin": "https://parivahan.gov.in",
            "User-Agent": User_Agent
        }

        response_2 = browser.post(post_url, data=formData_2, headers=headers_2)
        if "Details Of Driving License" in response_2.content.decode():
            result = parseHtml(response_2.content.decode())
            return result
        else:
            messages = handle_error(response_2.content.decode(), -1)
            return {"msg": messages}
    else:
        return messages



def handle_error(html, index):
    
    strs = re.findall("CDATA\[(.*?)\]\]>", html, re.S)[index]
    if index == 0:
        soup = BeautifulSoup(strs, "html.parser")
        try:
            msg = soup.select("div.ui-messages")[0].get_text().strip()
            if not msg:
                return "success"
        except:
            pass
        try:
            messages = soup.select("span.ui-messages-error-summary")[0].get_text().strip()
            return messages
        except:
            return strs
    else:
        try:
            messages = re.findall('detail:"(.*?)"}\);;', strs, re.S)[0]
            return messages
        except:
            return strs


def parseHtml(html):

    strs = re.findall("CDATA\[(.*?)\]\]>", html, re.S)[-2]
    ret = {}
    soup = BeautifulSoup(strs, "html.parser")
    try:
        strs = re.findall("CDATA\[(.*?)\]\]>", html, re.S)[0]
        soup1 = BeautifulSoup(strs, "html.parser")
        msg = soup1.select("div.ui-messages-error.ui-corner-all ul li")[0].get_text().strip()
    except:
        msg = False
        
    if msg:
        return {"msg": "No DL Details Found"}
    
    try:
        detail = soup.select("div.font-bold.top-space.bottom-space.text-capitalize.center-position.text-underline")[0].get_text().strip().split(":")[-1].strip()
    except:
        return {"msg": "No DL Details Found"}
    
    ret["DrivingLicense"] = detail
    
    try:
        item = soup.select("table.table.table-responsive.table-striped.table-condensed.table-bordered")[0]
        try:
            currentStatue = item.select("tr")[0].select("td")[-1].get_text().strip()
        except:
            currentStatue = None
        try:
            name = item.select("tr")[1].select("td")[-1].get_text().strip()
        except:
            name = None
        try:
            issue = item.select("tr")[2].select("td")[-1].get_text().strip()
        except:
            issue = None
        try:
            transaction = item.select("tr")[3].select("td")[-1].get_text().strip()
        except:
            transaction = None
        ret["CurrentStatus"] = currentStatue
        ret["HolderName"] = name
        ret["DateOfIssue"] = issue
        ret["LastTransactionAt"] = transaction

    except:
        pass

    try:
        itemDetails = soup.select("table.table.table-responsive.table-striped.table-condensed.table-bordered")[1]
        try:
            froms = itemDetails.select("tr")[0].select("td")[1].get_text().strip()
            if ":" in froms:
                froms = froms.split(":")[-1].strip()
        except:
            froms = None
        try:
            to = itemDetails.select("tr")[0].select("td")[2].get_text().strip()
            if ":" in to:
                to = to.split(":")[-1].strip()
        except:
            to = None
        ret['Non-Transport'] = {"Form": froms, "To": to}

        try:
            froms2 = itemDetails.select("tr")[1].select("td")[1].get_text().strip()
            if ":" in froms2:
                froms2 = froms2.split(":")[-1].strip()
        except:
            froms2 = None
        try:
            to2 = itemDetails.select("tr")[1].select("td")[2].get_text().strip()
            if ":" in to2:
                to2 = to2.split(":")[-1].strip()
        except:
            to2 = None
        ret['Transport'] = {"Form": froms2, "To": to2}

    except:
        pass

    try:
        itemDetails2 = soup.select("table.table.table-responsive.table-striped.table-condensed.table-bordered")[2]

        try:
            hazardous = itemDetails2.select("tr")[0].select("td")[1].get_text().strip()
        except:
            hazardous = None
        try:
            hill = itemDetails2.select("tr")[0].select("td")[3].get_text().strip()
        except:
            hill = None

        ret["HazardousValidTill"] = hazardous
        ret["HillValidTill"] = hill

    except:
        pass

    try:
        keyList = []
        for item in soup.select("div.ui-datatable-tablewrapper table tr th"):
            keyList.append(item.get_text().strip())
        lists = []
        for item in soup.select("div.ui-datatable-tablewrapper table tr.ui-widget-content"):
            listsTemp = []
            index = 0
            for td in item.select("td"):

                try:
                    listsTemp.append({keyList[index]: td.get_text().strip()})
                except:
                    listsTemp.append({keyList[index]: None})
                index += 1
            lists.append(listsTemp)
        ret["ClassOfVehicleDetails"] = lists
    except:
        ret["ClassOfVehicleDetails"] = None

    result_dict2 = {}
    result_dict2['data'] = ret
    result_dict2['msg'] = "success"

    return result_dict2
    

# def run():
#     result = Login_parivahan("MH1920090018951", "09-06-1987")
#     # result = Login_parivahan("MH0420090034322", "23-10-1987")
#     # result = Login_parivahan("P09072004330411", "08-02-1984")
#     print(result)

stop_exec = 0
i = 0
while stop_exec < 1:
    try:
        time.sleep(2)
        i = i + 1
        print(i)
        # try:
        # print(1111)
        time.sleep(0.5)
        aws_access_key_id = 'AKIAIMYPHVRMHZ76PSOA'
        aws_secret_access_key = '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'
        dynamodb = boto3.resource(service_name='dynamodb', aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key, region_name='ap-south-1')
        sqs = boto3.resource(service_name='sqs', aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key, region_name='ap-south-1')
        queue = sqs.get_queue_by_name(QueueName='driving_license_request')
        sqs_msg = queue.receive_messages(MaxNumberOfMessages=1)[0]
        
        try:
            report_info = json.loads(sqs_msg.body)
            report_info_json = json.dumps(report_info)
        except:
            report_info = {}
            report_info['report_id'] = 'empty'
        if report_info['report_id'] != 'empty':
            # print(report_info)
            report_id = report_info['report_id']
            print(report_id)
            # print("x0")
            callbackURL = report_info['callbackurl']
            # print(report_id)
            # print(callbackURL)
            license_no = report_info['driving_license_number'].strip().replace(" ",'').upper()
            print(license_no)
            date_of_birth = report_info['date_of_birth'].strip().replace(" ",'').replace("/","-")
            
            month = {"jan":"01","feb":"02","mar":"03","apr":"04","may":"05","jun":"06","jul":"07","aug":"08","sept":"09","oct":"10","nov":"11","dec":"12"}
            s0 = date_of_birth.split("-")[0].lower()
            s = date_of_birth.split("-")[1].lower()
            s1 = date_of_birth.split("-")[2].lower()
    
            num = month[s]
    
            date_of_birth = s0 + "-" + num + "-" + s1
            # print(license_no)
            # print(date_of_birth)
            # print(55555555555)
            stop = 0
            while stop < 5:
                stop = stop + 1
                try:
                    # print(Vehicle_No)
                    result_dict = Login_parivahan(license_no,date_of_birth,report_id)
                    # print(result_dict)
                    
                    # print(1111111)
                    result = result_dict['msg']
                    print(result)
                    # print(result)
                    report = {}
                    
                    # print("x2")
                    if "No DL Details Found" in result:
                        stop = 31
                        report['comments'] = "No DL Details Found"
                    
                    elif result =="success":
                        # print(result)
                        # s = result_dict["data"]
                        stop = 31
                        report['comments'] = result_dict["data"]
                    
                    # elif result==None:
                    #     print()
                    #     stop =31
                    #     report['comments'] = "No DL Details Found"
            
                except:
                    pass
                
            date_of_birth0 = report_info['date_of_birth']
            report['report_id'] = report_id
            report['callbackURL'] = callbackURL
            report['date_of_birth'] = date_of_birth0
            report['driving_license_number'] = license_no
            print(report)
            time.sleep(1)
            
    except:
        time.sleep(2)
    