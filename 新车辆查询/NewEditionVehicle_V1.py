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
    rcdlstatus_url = "https://parivahan.gov.in/rcdlstatus/"
    response = session.get(url=rcdlstatus_url,headers=headers,verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    try:
        get_javax_faces_ViewState = soup.select("input")[-1].attrs["value"]
        # img_src = soup.select("img#form_rcdl:j_idt37:j_idt43")[0].attrs["src"]
        # print(get_javax_faces_ViewState)
        # print(img_src)
        return get_javax_faces_ViewState,session
    except:
        print("网站已更新请更新相应的代码,参数获取不对")
        exit(-1)

#错误处理器
def error_handler(soup):
    """
    错误处理情况1、Registration No. does not exist!!! Please check the number. 情况
               2、空指针异常
    :param soup:
    :return:
    """
    #临时dict
    dict = {}
    #返回dict
    error_dict = {}
    #1、Registration No. does not exist!!! Please check the number. 情况
    NotExist_Flag = re.findall('detail:"(.*?)"}\);;', str(soup), re.S)
    if NotExist_Flag:
        dict['errorInfo'] = NotExist_Flag[0]
        error_dict['comments'] = dict
        return error_dict
    #2、空指针异常  NullPointerException
    Exception_Flag = "class java.lang.NullPointerException"
    exception_flag = re.search(Exception_Flag, str(soup), re.S)
    if exception_flag:
        print(soup)
        dict['errorInfo'] = Exception_Flag
        error_dict['comments'] = dict
        return error_dict


#获取车辆的信息
def GetVehicleInfo(soup):
    """
    解析车辆的信息
    :param soup:
    :return:
    """
    #soup预处理数据
    temp = soup.select("update#form_rcdl:pnl_show ")
    # print(temp)
    temp = str(temp).replace('![CDATA[','')
    newsoup = BeautifulSoup(temp, "html.parser")
    # print(newsoup)
    items = newsoup.select("div tr")
    # print(items)
    #返回的数据
    result_dict = {}
    try:
        title = newsoup.select("div.font-bold.top-space.bottom-space.text-capitalize")[0].get_text().strip()
        result_dict[title.split(":")[0]] = title.split(":")[1].lstrip()
    except:
        result_dict["Registering Authority"] = None
    #数据,一行行解析
    try:
        tempLine = items[0].select("td ")
        # print(tempLine)
        Temp = tempLine[0].get_text().strip().replace(' ', '').replace(':', '')
        result_dict[Temp] = tempLine[1].get_text().strip()

        Temp = tempLine[2].get_text().strip().replace(' ', '').replace(':', '')
        result_dict[Temp] = tempLine[3].get_text().strip()
    except:
        result_dict['RegistrationNo'] = None
        result_dict['RegistrationDate'] = None

    try:
        tempLine = items[1].select("td ")
        # print(tempLine)
        Temp = tempLine[0].get_text().strip().replace(' ', '').replace(':', '')
        result_dict[Temp] = tempLine[1].get_text().strip()

        Temp = tempLine[2].get_text().strip().replace(' ', '').replace(':', '')
        result_dict[Temp] = tempLine[3].get_text().strip()
    except:
        result_dict['ChassisNo'] = None
        result_dict['EngineNo'] = None

    try:
        tempLine = items[2].select("td ")
        # print(tempLine)
        Temp = tempLine[0].get_text().strip().replace(' ', '').replace(':', '')
        result_dict[Temp] = tempLine[1].get_text().strip()

    except:
        result_dict['OwnerName'] = None

    try:
        tempLine = items[3].select("td ")
        # print(tempLine)
        Temp = tempLine[0].get_text().strip().replace(' ', '').replace(':', '')
        result_dict[Temp] = tempLine[1].get_text().strip()

        Temp = tempLine[2].get_text().strip().replace(' ', '').replace(':', '')
        result_dict[Temp] = tempLine[3].get_text().strip()
    except:
        result_dict['VehicleClass'] = None
        result_dict['FuelType'] = None

    try:
        tempLine = items[4].select("td ")
        # print(tempLine)
        Temp = tempLine[0].get_text().strip().replace(' ', '').replace(':', '')
        result_dict[Temp] = tempLine[1].get_text().strip()

    except:
        result_dict['Maker/Model'] = None

    try:
        tempLine = items[5].select("td ")
        # print(tempLine)
        Temp = tempLine[0].get_text().strip().replace(' ', '').replace(':', '')
        result_dict[Temp] = tempLine[1].get_text().strip()

        Temp = tempLine[2].get_text().strip().replace(' ', '').replace(':', '')
        result_dict[Temp] = tempLine[3].get_text().strip()
    except:
        result_dict['FitnessUpto'] = None
        result_dict['InsuranceUpto'] = None

    try:
        tempLine = items[6].select("td ")
        # print(tempLine)
        Temp = tempLine[0].get_text().strip().replace(' ', '').replace(':', '')
        result_dict[Temp] = tempLine[1].get_text().strip()

        Temp = tempLine[2].get_text().strip().replace(' ', '').replace(':', '')
        result_dict[Temp] = tempLine[3].get_text().strip()
    except:
        result_dict['FuelNorms'] = None
        result_dict['RoadTaxPaidUpto'] = None

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
def RunVehicleCheckStatus(RegNO1, RegNO2):
    """
    运行主函数
    :param RegNO1:
    :param RegNO2:
    :return:
    """
    # 获取post 请求的参数
    get_javax_faces_ViewState,  session = get_post_parameter()

    #post 请求的头
    headers = {
        'Accept': 'application/xml, text/xml, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Faces-Request': 'partial/ajax',
        'Host': 'parivahan.gov.in',
        'Origin': 'https://parivahan.gov.in',
        'Referer': 'https://parivahan.gov.in/rcdlstatus/',
        'User-Agent': UserAgent().random,
        'X-Requested-With': 'XMLHttpRequest'
    }
    FormData = {
        'javax.faces.partial.ajax':'true',
        'javax.faces.source': 'form_rcdl:j_idt48',
        'javax.faces.partial.execute': '@all',
        'javax.faces.partial.render':'form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl',
        'form_rcdl:j_idt48':'form_rcdl:j_idt48',
        'form_rcdl': 'form_rcdl',
        'form_rcdl:tf_reg_no1': RegNO1,
        'form_rcdl:tf_reg_no2': RegNO2,
        # 'form_rcdl:j_idt34:CaptchaID': get_captcha,
        'javax.faces.ViewState': get_javax_faces_ViewState,
    }

    rcdlstatus_url = "https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml"
    response = session.post(rcdlstatus_url, data=FormData, headers=headers, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    # 错误信息处理
    errorInfo = error_handler(soup)
    if errorInfo:
        return errorInfo

    else:
        result_dict = GetVehicleInfo(soup)
        return result_dict


for i in range(100):
    print("############执行第：", i, "次")
    j = 1
    result_dict = RunVehicleCheckStatus("HR26CU","1222")
    print(result_dict)


