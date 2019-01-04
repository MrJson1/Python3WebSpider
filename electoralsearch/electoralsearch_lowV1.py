import  requests
from http.cookiejar import MozillaCookieJar
from fake_useragent import UserAgent
from bs4 import  BeautifulSoup
from aip import AipOcr
from pytesseract import *
from PIL import Image
from urllib.parse import  urlencode
import json
import re

#获取request 请求的参数
def get_request_parameter():
    # 保持会话
    def get_session():
        session = requests.Session()
        session.cookies = MozillaCookieJar()
        return session
    #获取会话
    session = get_session()
    headers = {'User-Agent': UserAgent().random}
    electoralsearch_url = "https://electoralsearch.in/"
    response = session.get(url=electoralsearch_url, headers=headers, timeout=30)
    html = response.text
    # print(html)
    soup = BeautifulSoup(html, "html.parser")
    try:
        get_reureureired = str(soup.select("script")[-1]).split('return')[-1].split(';')[0].replace('\'', '')
        # print(get_reureureired)
        return get_reureureired,session
    except:
        print("网站已更新请更新相应的代码,参数获取不对")
        exit(-1)

# 获取验证码
def get_captcha_code(session):
    # captcha_link = "https://electoralsearch.in/Home/GetCaptcha?image=true&id=Wed Jan 02 2019 17:04:17 GMT+0800 (中国标准时间)"
    captcha_link = "https://electoralsearch.in/Home/GetCaptcha?image=true&id=Fri Jan 04 2019 10:45:28 GMT+0800 (中国标准时间)"
    headers = {'User-Agent': UserAgent().random}
    response = session.get(url=captcha_link, headers=headers,timeout=30)
    with open("./captchacode.png", "wb") as fn:
        fn.write(response.content)

    img = Image.open("./captchacode.png")
    imgry = img.convert('L')  # 转化为灰度图
    imgry.save('./captchacode.png')


    image = Image.open("./captchacode.png")

    captcha = pytesseract.image_to_string(image)

    # #使用的百度AIP
    # APP_ID = '15179847'
    # API_KEY = 'CvVnnyicDjZHBoBn9itQD9sG'
    # SECEER_KEY = 'nv0hjAgETYSEG1NOykEcRSqdCkf2o7wI'
    #
    # client = AipOcr(APP_ID, API_KEY, SECEER_KEY)
    # def get_file_content(filePath):
    #     with open(filePath, 'rb') as fp:
    #         return fp.read()
    #
    # # 定义参数变量
    # options = {
    #     'detect_direction': 'true',
    #     'language_type': 'CHN_ENG',
    # }
    # filePath = './captchacode.png'
    # # 调用通用文字识别接口
    # result = client.basicGeneral(get_file_content(filePath), options)
    # captcha = result['words_result'][0]['words']
    print(captcha)
    # captcha = input("请输入验证码：")
    return captcha

#是否登录成功标记
def is_SearchSucceed(html,EPIC_No_flag):
    Succee_flag = '"numFound":1'
    succeed_flag = re.search(Succee_flag, html, re.S)
    #EPIC_No_flag 预处理
    EPIC_No_flag = EPIC_No_flag.replace(" ","").upper()
    succeed_flag_2 = re.search(EPIC_No_flag, html, re.S)
    if succeed_flag and succeed_flag_2:
        try:
            result_jsondata = json.loads(html)
            response_docs_dict = result_jsondata['response']['docs'][0]
            # print(response_docs_dict)
            #临时的dict
            dict = {}
            #返回的dict
            result_dict = {}

            # 数据重新处理
            if response_docs_dict:
                try:
                    dict['epic_no'] = str(response_docs_dict['epic_no']).strip()
                except:
                    dict['epic_no'] =None
                try:
                    dict['name'] = str(response_docs_dict['name']).strip()
                except:
                    dict['name'] = None
                try:
                    dict['age'] = str(response_docs_dict['age']).strip()
                except:
                    dict['age'] = None
                try:
                    dict["Father's/Husband's_Name"] = str(response_docs_dict['rln_name']).strip()
                except:
                    dict["Father's/Husband's_Name"] = None
                try:
                    dict['state'] = str(response_docs_dict['state']).strip()
                except:
                    dict['state'] = None
                try:
                    dict['District'] = str(response_docs_dict['district']).strip()
                except:
                    dict['District'] = None
                try:
                    dict['PollingStation'] = str(response_docs_dict['ps_name']).strip()
                except:
                    dict['PollingStation'] = None
                try:
                    dict['AssemblyConstituency'] = str(response_docs_dict['ac_name']).strip()
                except:
                    dict['AssemblyConstituency'] = None
                try:
                    dict['ParliamentaryConstituency'] = str(response_docs_dict['pc_name']).strip()
                except:
                    dict['ParliamentaryConstituency'] = None
                # print(dict)
                successfulInfo_dict = {}
                successfulInfo_dict["successfulInfo"] = dict
                result_dict["comments"] = successfulInfo_dict
                # print(result_dict)
                return result_dict
        except:
            WebsiteUpdateInfo = "网站已经更新返回的数据,请修改succeed_flag代码"

            print(WebsiteUpdateInfo)

#错误处理器
def error_handler(html):
    """
    #错误信息处理 1、没有查询到数据,账号无效情况（Number of Record(s) Found: 0），2、发生了意外错误，3、账号无效，4、识别码错误和其他错误
    :param html:
    :return:
    """

    #临时dict
    dict = {}
    #返回dict
    error_dict = {}
    #1、没有查询到数据
    NotFound_flag = '"numFound":0'
    error_flag = re.search(NotFound_flag, html, re.S)
    if error_flag:
        NotFound = "Number of Record(s) Found: 0"
        dict['errorInfo'] = NotFound
        error_dict['comments'] = dict
        return error_dict

    #2、发生了意外错误
    unexpected_flag = "An unexpected error has occurred. Please contact the system administrator"
    error_flag = re.search(unexpected_flag, html, re.S)
    if error_flag:
        dict['errorInfo'] = unexpected_flag
        error_dict['comments'] = dict
        return error_dict

    #3、账号无效,默认实现numFound_flag 0和1 之外的判断为账号无效
    valid_flag = '"numFound"'
    ValidFlag = re.search(valid_flag,html, re.S)
    if ValidFlag:
        numFound_jsondata = json.loads(html)
        numFound_flag = numFound_jsondata["response"]["numFound"]
        print("numFound_flag:",numFound_flag)
        if numFound_flag != 1 or numFound_flag !=0:
            flag = "Please Enter valid Epic No."
            dict['errorInfo'] = flag
            error_dict['comments'] = dict
            return error_dict

    #4、Wrong Captcha and Other errors
    dict['errorInfo'] = html
    error_dict['comments'] = dict
    return error_dict

#返回结果
def RunElectoralSearch(EPIC_No,State=""):
    account_dict = {}
    #输入预处理
    if EPIC_No=="" and State =="":
        account_dict["comments"] = "Need Your EPIC_No"
        return account_dict
    else:
        # 获取get 参数
        get_reureureired, session = get_request_parameter()

        # post 请求的头
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'electoralsearch.in',
            'Referer': 'https://electoralsearch.in/',
            'User-Agent': UserAgent().random
        }

        # 构造Request URL
        base_url = "https://electoralsearch.in/Home/searchVoter?"
        params = {
            'epic_no': EPIC_No,
            'page_no': '1',
            'results_per_page': '10',
            'reureureired': get_reureureired,
            'search_type': 'epic',
            'state': State,
            'txtCaptcha': get_captcha_code(session)
        }
        electoralsearch_url = base_url + urlencode(params)
        print(electoralsearch_url)

        response = session.get(electoralsearch_url, headers=headers, timeout=30)
        result_html = response.text
        # print("result_html:",result_html)
        # 判断登录成功标记
        result_dict = is_SearchSucceed(result_html,EPIC_No)
        if result_dict:
            return result_dict

        else:
            # 错误信息处理
            error_dict = error_handler(result_html)
            return error_dict


for i in range(1, 50):
    try:
        result_dict = RunElectoralSearch(EPIC_No="Sje0997320")
        print("最后的结果：",result_dict)
        if "NRB0399436" in str(result_dict):
            print(9999)
    except:
        pass





