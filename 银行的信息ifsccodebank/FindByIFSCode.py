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

#获取post 请求的参数
def get_post_parameter():
    #获取会话
    session = get_session()
    headers = {'User-Agent': UserAgent().random}
    codebank_url = "https://www.ifsccodebank.com/search-by-IFSC-code.aspx"
    response = session.get(url=codebank_url,headers=headers,verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    try:
        get__VIEWSTATE = soup.select("input#__VIEWSTATE")[0].attrs['value']
        get__VIEWSTATEGENERATOR = soup.select("input#__VIEWSTATEGENERATOR")[0].attrs['value']
        get__EVENTVALIDATION = soup.select("input#__EVENTVALIDATION")[0].attrs['value']
        # print(get__VIEWSTATE)
        # print(get__VIEWSTATEGENERATOR)
        # print(get__EVENTVALIDATION)
        return get__VIEWSTATE,session,get__VIEWSTATEGENERATOR,get__EVENTVALIDATION
    except:
        print("网站已更新请更新相应的代码,参数获取不对")
        exit(-1)

#错误处理器
def error_handler(soup):
    """
    错误处理情况1、There are currently no items found.
    :param soup:
    :return:
    """
    # 临时dict
    dict = {}
    # 返回dict
    error_dict = {}

    flag_Nofound = "There are currently no items found."
    Nofound = re.search(flag_Nofound, str(soup), re.S)
    if Nofound:
        dict['errorInfo'] = flag_Nofound
        error_dict['comments'] = dict
        return error_dict


    # else:
    #     print(soup)
    #     dict['errorInfo'] = "unknown exception"
    #     error_dict['comments'] = dict
    #     return error_dict


#判断成功标识
def RunIsucceed(html):
    flag_succeful = "Bank Details:"
    succeed_flag = re.search(flag_succeful, str(html), re.S)
    if succeed_flag:
        return succeed_flag

#解析IFSC_CODE，获取数据
def  ParseHTML_getData(soup):
    """
    默认多条数据情况只取开始的第一条
    :param soup:
    :return:
    """
    result_dict = {}
    # 左边数据
    Left_items = soup.select("div.imgTwoColumn.floatLEFT tr")
    Left_items_lenth = len(Left_items)
    # print(Left_items_lenth)
    while Left_items_lenth >= 0:
        Left_items_lenth -= 1
        item = Left_items[Left_items_lenth].select("td")
        # print(len(item))
        # print(item)
        key = item[0].get_text().strip().replace(' ', '').replace(':', '')
        result_dict[key] = item[1].get_text().strip()

    # 右边数据
    Right_items = soup.select("div.imgTwoColumn.floatRIGHT tr")
    # print(Right_items)
    Right_items_lenth = len(Right_items)
    # print(Right_items_lenth)
    while Right_items_lenth >= 0:
        Right_items_lenth -= 1
        item = Right_items[Right_items_lenth].select("td")
        # print(len(item))
        # print(item)
        key = item[0].get_text().strip().replace(' ', '').replace(':', '')
        result_dict[key] = item[1].get_text().strip()
    # print(result_dict)

    #数据过滤,处理空值的情况
    for key in result_dict:
        value = result_dict[key]
        if not value:
            result_dict[key] = None

    dict = {}
    success_dict = {}
    dict['successInfo'] = result_dict
    success_dict['comments'] = dict

    return success_dict

# 返回结果
def SearchIFSC_Code(IFSCCode):
    # 获取post 请求的参数
    get__VIEWSTATE, session, get__VIEWSTATEGENERATOR, get__EVENTVALIDATION= get_post_parameter()

    #post 请求的头
    headers = {
        'authority':'www.ifsccodebank.com',
        'method':'POST',
        'path':'/search-by-IFSC-code.aspx',
        'scheme':'https',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.ifsccodebank.com',
        'referer': 'https://www.ifsccodebank.com/search-by-IFSC-code.aspx',
        'upgrade-insecure-requests': '1',
        'user-agent': UserAgent().random

    }
    FormData = {
        '__VIEWSTATE':get__VIEWSTATE,
        '__VIEWSTATEGENERATOR': get__VIEWSTATEGENERATOR,
        '__VIEWSTATEENCRYPTED': '',
        '__EVENTVALIDATION': get__EVENTVALIDATION,
        'ctl00$BC$txtIFSCCode': IFSCCode,
        'ctl00$BC$btnSeach': 'Search',
    }

    url = "https://www.ifsccodebank.com/search-by-IFSC-code.aspx"
    response = session.post(url, data=FormData, headers=headers, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    #判断是否能查询到
    errorInfo = error_handler(soup)
    if errorInfo:
        return errorInfo

    #默认多条数据情况只取开始的第一条
    success_dict = ParseHTML_getData(soup)
    return  success_dict
    # print(success_dict)

# SearchIFSC_Code("SIDB0TREMHO")
result = SearchIFSC_Code("121")
print(result)


