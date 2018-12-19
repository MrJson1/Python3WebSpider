import  requests
from http.cookiejar import MozillaCookieJar
from fake_useragent import UserAgent
from bs4 import  BeautifulSoup
from aip import AipOcr
from pytesseract import *
from PIL import Image


# 保持会话
def get_session():
    session = requests.Session()
    session.cookies = MozillaCookieJar()
    return session

#获取post 请求的参数
def get_post_parameter():
    #获取会话
    session = get_session()
    headers = {'User-Agent': UserAgent().random}
    SearchldCard_url = "http://ceodelhi.gov.in/OnlineErms/ElectorSearchIdCard.aspx"
    response = session.get(url=SearchldCard_url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    try:
        __VIEWSTATEGENERATOR = soup.select("#__VIEWSTATEGENERATOR")[0].attrs["value"]
        __VIEWSTATE = soup.select("#__VIEWSTATE")[0].attrs["value"]
        __EVENTVALIDATION = soup.select("#__EVENTVALIDATION")[0].attrs["value"]
        # print(__VIEWSTATEGENERATOR)
        # print(__VIEWSTATE)
        # print(__EVENTVALIDATION)
        return __VIEWSTATEGENERATOR, __VIEWSTATE, __EVENTVALIDATION,session
    except:
        print("网站已更新请更新相应的代码,参数获取不对")
        exit(-1)

# 获取验证码
def get_captcha_code(session):
    captcha_link = "http://ceodelhi.gov.in/OnlineErms/CapchaControlImage.aspx"
    headers = {'User-Agent': UserAgent().random}
    response = session.get(url=captcha_link, headers=headers)
    with open("./captchacode.png", "wb") as fn:
        fn.write(response.content)

    img = Image.open("./captchacode.png")
    imgry = img.convert('L')  # 转化为灰度图
    imgry.save('./captchacode.png')

    #使用的百度AIP
    APP_ID = '15179847'
    API_KEY = 'CvVnnyicDjZHBoBn9itQD9sG'
    SECEER_KEY = 'nv0hjAgETYSEG1NOykEcRSqdCkf2o7wI'

    client = AipOcr(APP_ID, API_KEY, SECEER_KEY)
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    # 定义参数变量
    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
    }
    filePath = './captchacode.png'
    # 调用通用文字识别接口
    result = client.basicGeneral(get_file_content(filePath), options)
    captcha = result['words_result'][0]['words']
    # print(captcha)
    # captcha = input("请输入验证码：")
    # print(captcha)
    return captcha

#错误处理器
def error_handler(soup):
    if soup.select("#ctl00_ContentPlaceHolder1_LabelError"):
        errorInfo = soup.select("#ctl00_ContentPlaceHolder1_LabelError")[0].get_text().strip()
        # print(errorInfo)
        if errorInfo=="No records found.":
            return errorInfo
        elif errorInfo=="Capcha code not matched..":
            return errorInfo
    else:
        pass

# 返回结果
def RunSearchldCard(Voterid):
    # 返回的字典
    result_dict = {}
    if Voterid=="":
        result_dict["resultInfo"] = "Need Your Voters' Photo Identity Card No"
        return result_dict
    # 获取post 请求的参数
    __VIEWSTATEGENERATOR, __VIEWSTATE, __EVENTVALIDATION ,session= get_post_parameter()
    #post 请求的头
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://ceodelhi.gov.in/OnlineErms/ElectorSearchIdCard.aspx',
        'User-Agent': UserAgent().random,
        'Host': 'ceodelhi.gov.in',
        'Origin': 'http://ceodelhi.gov.in',
        'Upgrade-Insecure-Requests': '1'
    }
    postData = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': __VIEWSTATE,
        '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
        '__VIEWSTATEENCRYPTED': '',
        '__EVENTVALIDATION': __EVENTVALIDATION,
        'ctl00$ContentPlaceHolder1$TextBoxIDCardNo': Voterid,
        'ctl00$ContentPlaceHolder1$TextBoxcaptacha': get_captcha_code(session),
        'ctl00$ContentPlaceHolder1$ButtonSearch': 'Search'
    }

    SearchldCard_url = "http://ceodelhi.gov.in/OnlineErms/ElectorSearchIdCard.aspx"
    response = session.post(SearchldCard_url, data=postData, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    # print(soup)

    #错误信息处理
    errorInfo = error_handler(soup)
    # print(errorInfo)
    if errorInfo:
        result_dict["resultInfo"] = errorInfo
        return result_dict

    else:
        try:
            result_dict[soup.select("th")[5].get_text().strip()] = str(
                soup.select("table")[20].select("tr td")[5].get_text().strip()).replace(' ', '')
        except:
            result_dict["Voters' Address"] = None
        try:
            result_dict[soup.select("th")[6].get_text().strip()] = soup.select("table")[20].select("tr td")[
                6].get_text().strip()
        except:
            result_dict["Voters' Name"] = None
        # result_dict[soup.select("th")[7].get_text().strip()] = soup.select("table")[20].select("tr td")[7].get_text().strip()
        try:
            result_dict[soup.select("th")[8].get_text().strip()] = soup.select("table")[20].select("tr td")[
                8].get_text().strip()
        except:
            result_dict["Relation Name"] = None
        try:
            result_dict[soup.select("th")[9].get_text().strip()] = soup.select("table")[20].select("tr td")[
                9].get_text().strip()
        except:
            result_dict["Age"] = None
        try:
            result_dict[soup.select("th")[10].get_text().strip()] = soup.select("table")[20].select("tr td")[
                10].get_text().strip()
        except:
            result_dict["Sex"] = None
        try:
            result_dict[soup.select("th")[11].get_text().strip()] = soup.select("table")[20].select("tr td")[
                11].get_text().strip()
        except:
            result_dict["ID Card No"] = None
        return result_dict

result_dict = RunSearchldCard(Voterid="SJE0997320")
print(result_dict)





