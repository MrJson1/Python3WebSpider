import  requests
from http.cookiejar import MozillaCookieJar
from fake_useragent import UserAgent
from bs4 import  BeautifulSoup
from pytesseract import *
from PIL import Image
import re


# 保持会话
def get_session():
    session = requests.Session()
    session.cookies = MozillaCookieJar()
    return session

# 获取验证码和ViewState
def get_captcha_and_ViewState(session):
    login_url = "https://www.tdscpc.gov.in/app/tapn/tdstcscredit.xhtml"
    #随机头
    User_Agent = UserAgent().random
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.tdscpc.gov.in',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': User_Agent,

    }
    response_html = session.get(url=login_url, headers=headers,  timeout=30)
    html = response_html.text
    soup = BeautifulSoup(html, "html.parser")
    try:
        #获取图片的url
        img_url = soup.select("img")[1].attrs["src"]
        base_url = "https://www.tdscpc.gov.in"
        captcha_url = base_url + img_url


        #获取javax.faces.ViewState 值
        get_javax_faces_ViewState = soup.select("input#javax.faces.ViewState")[1].attrs["value"]
        print("captcha_url:", captcha_url)
        # print("get_javax_faces_ViewState:",get_javax_faces_ViewState)

        response = session.get(url=captcha_url, headers=headers, timeout=30)
        with open("./captchacode.png", "wb") as fn:
            fn.write(response.content)

        image = Image.open("./captchacode.png")
        captcha = pytesseract.image_to_string(image)
        print("captcha image_to_string:",captcha)
        captcha = input("请输入验证码：")
        print(captcha)
        return captcha, get_javax_faces_ViewState
    except:
        print("网站已经更新！！！！！！！")

#登录界面预处理(主要处理验证码)
def login_preproccess():
    session = get_session()
    captcha, get_javax_faces_ViewState = get_captcha_and_ViewState(session)
    User_Agent = UserAgent().random
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.tdscpc.gov.in',
        'Origin':'https://www.tdscpc.gov.in',
        'Referer':'https://www.tdscpc.gov.in/app/tapn/tdstcscredit.xhtml',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': User_Agent,
    }
    login_preproccess_formData = {
        'captcha':captcha,
        'clickProceed': 'Proceed',
        'captchaForm_SUBMIT': '1',
        'javax.faces.ViewState':get_javax_faces_ViewState
    }
    login_preproccess_posturl = "https://www.tdscpc.gov.in/app/tapn/tdstcscredit.xhtml"
    preproccess_response = session.post(url=login_preproccess_posturl,headers=headers,data=login_preproccess_formData, tiemout = 30)
    preproccess_html = preproccess_response.text
    html = is_presucceful(preproccess_html)

    #如果存在说明预处理成功
    if html:
        soup = BeautifulSoup(html, "html.parser")
        # print("soup:",soup)
        #获取第二个post请求参数
        renderForm = soup.select("input#renderForm")[0].attrs["value"]
        currQtr = soup.select("input#currQtr")[0].attrs["value"]
        returnType = soup.select("select#returnType")[0].attrs["size"]
        renderPage = soup.select("input#renderPage")[0].attrs["value"]
        hidField = soup.select("input#hidField")[0].attrs["value"]
        tapTdsTcsCredit_SUBMIT = soup.select("input")[-8].attrs["value"]
        clickGo = soup.select("input#clickGo")[0].attrs["value"]
        get_login_javax_faces_ViewState = soup.select("input#javax.faces.ViewState")[0].attrs["value"]
        # print("get_login_javax_faces_ViewState:", get_login_javax_faces_ViewState)
        # print("renderForm:", renderForm)
        # print("currQtr", currQtr)
        # print("returnType:",returnType, "renderPage:",renderPage, "hidField:",hidField)
        # print("tapTdsTcsCredit_SUBMIT:",tapTdsTcsCredit_SUBMIT)
        # print("clickGo",clickGo)

        return renderForm,currQtr,returnType,renderPage,hidField,session,tapTdsTcsCredit_SUBMIT,get_login_javax_faces_ViewState,clickGo,html
    else:
        print("验证码识别错误:Text entered does not match with image data")
        exit(-1)

#预处理是否成功
def is_presucceful(html):
    #验证码识别成功标识
    flag_presucceful = "PAN of Deductee"
    succeed_flag = re.search(flag_presucceful, html, re.S)
    if succeed_flag:
        print("预处理成功")
        return html
    print("login_preproccess预处理失败")

#返回结果预处理
def go_results_preproccess(html,financialYear_,quarter_,Salary_):
    """
    判断输入的数据是否有效
    :param html:
    :param financialYear_:
    :param quarter_:
    :param Salary_:
    :return:error_dict or success_dict

    """
    soup = BeautifulSoup(html, "html.parser")

    #临时dict
    dict = {}
    #返回dict
    error_dict = {}

    # 获取财政年度集合
    _financialYear_ = soup.select("select#financialYear option")
    # print(_financialYear_)
    # print(len(_financialYear_))
    length_financialYear = len(_financialYear_)
    length_financialYear -= 1
    # 财政年度选择list
    selectFinancialYearList = []
    while 0 < length_financialYear:
        #财政年度集合
        selectFinancialYearList.append(_financialYear_[length_financialYear].get_text().strip())
        length_financialYear -= 1
    # print("selectFinancialYearList:",selectFinancialYearList)

    #1、判断传入的财政年度查询是否有效(这里只是初步的判断，因为正则匹配是完全匹配,不过后面的error_processor已经
    #弥补了这个不足，例如传入的是financialYear_ = "2018-1",下面的判断就不足 )
    flag = str(selectFinancialYearList)
    selectFinancialYearList_succeed_flag = re.search(financialYear_, flag, re.S)

    if selectFinancialYearList_succeed_flag:
        financialYear = financialYear_.split("-")[0]
        currYear = "20" + financialYear_.split("-")[1]

        try:
            quarter_dict = {}
            quarter = soup.select("select#quarter option")
            quarter_dict[quarter[1].get_text().strip()] = quarter[1].attrs["value"]
            quarter_dict[quarter[2].get_text().strip()] = quarter[2].attrs["value"]
            quarter_dict[quarter[3].get_text().strip()] = quarter[3].attrs["value"]
            quarter_dict[quarter[4].get_text().strip()] = quarter[4].attrs["value"]
            quarter = quarter_dict[quarter_]

            #2、判断quarter_ 是否有效
            if quarter:

                Salary_list = []
                returnType = soup.select("select#returnType option")
                Salary_list.append(returnType[1].get_text().strip())
                Salary_list.append(returnType[2].get_text().strip())
                # print(returnType)
                print("Salary_list:",Salary_list)

                #3、判断Salary_ 输入是否有效
                if Salary_ in Salary_list:
                    salary = Salary_

                    #全部有效输入就返回
                    success_dict = {}
                    dict["financialYear"] = financialYear
                    dict["currYear"] = currYear
                    dict["quarter"] = quarter
                    dict["salary"] = salary
                    success_dict["successfulInfo"] = dict
                    # return financialYear,currYear,quarter,salary
                    return success_dict
                else:
                    dict['errorInfo'] = "salary: Validation Error: Value is not valid"
                    error_dict['comments'] = dict
                    return error_dict


            # quarter_无效情况
            else:
                dict['errorInfo'] = "quarter: Validation Error: Value is not valid"
                error_dict['comments'] = dict
                return error_dict

        #如果报错采用quarter_默认方式
        except:
            quarter_List = ["Q1","Q2","Q3","Q4"]
            if quarter_ in quarter_List:
                quarter = str(int(quarter_[1]) + 2)

                Salary_list = []
                returnType = soup.select("select#returnType option")
                Salary_list.append(returnType[1].get_text().strip())
                Salary_list.append(returnType[2].get_text().strip())
                # print(returnType)
                # print("Salary_list:", Salary_list)

                # 3、判断Salary_ 输入是否有效
                if Salary_ in Salary_list:
                    salary = Salary_

                    #全部有效输入就返回
                    success_dict = {}
                    dict["financialYear"] = financialYear
                    dict["currYear"] = currYear
                    dict["quarter"] = quarter
                    dict["salary"] = salary
                    success_dict["successfulInfo"] = dict
                    # return financialYear,currYear,quarter,salary
                    return success_dict
                else:
                    dict['errorInfo'] = "salary: Validation Error: Value is not valid"
                    error_dict['comments'] = dict
                    return error_dict

            # quarter_无效情况
            else:
                dict['errorInfo'] = "quarter: Validation Error: Value is not valid"
                error_dict['comments'] = dict
                return error_dict


    #财政年度无效情况
    dict['errorInfo'] = "financialYear: Validation Error: Value is not valid"
    error_dict['comments'] = dict
    return error_dict

#登录
def login_go(dedtpan,dedtan,financialYear_,quarter_,Type_of_Return):
    """
    实现点击go查询数据功能
    :param dedtpan:
    :param dedtan:
    :param financialYear_:
    :param quarter_:
    :param Type_of_Return:
    :return: 成功的dict or 失败的dict
    """

    # 接收login_post参数
    renderForm, currQtr, returnType, renderPage, hidField, session, tapTdsTcsCredit_SUBMIT, get_login_javax_faces_ViewState, clickGo, html = login_preproccess()

    # 判断输入的数据是否有效,预处理 并且取得financialYear,currYear,quarter,salary
    preproccess_dict = go_results_preproccess(html, financialYear_, quarter_, Type_of_Return)
    print("preproccess_dict:",preproccess_dict)

    #预处理成功的情况
    if "successfulInfo" in preproccess_dict:
        financialYear = preproccess_dict['successfulInfo']['financialYear']
        currYear = preproccess_dict['successfulInfo']['currYear']
        quarter = preproccess_dict['successfulInfo']['quarter']
        # salary = preproccess_dict['successfulInfo']['salary']

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www.tdscpc.gov.in',
            'Origin': 'https://www.tdscpc.gov.in',
            'Referer': 'https://www.tdscpc.gov.in/app/tapn/tdstcscredit.xhtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': UserAgent().random
        }

        formData = {
            'dedtpan': dedtpan,
            'renderForm': renderForm,
            'dedtan': dedtan,
            'financialYear': financialYear,
            'currYear': currYear,
            'quarter': quarter,
            'currQtr': currQtr,
            'returnType': returnType,
            'clickGo': clickGo,
            'renderPage': renderPage,
            'hidField': hidField,
            'tapTdsTcsCredit_SUBMIT': tapTdsTcsCredit_SUBMIT,
            'javax.faces.ViewState': get_login_javax_faces_ViewState
        }

        post_url = "https://www.tdscpc.gov.in/app/tapn/tdstcscredit.xhtml"
        response = session.post(url=post_url, headers=headers, data=formData, timeout =30)
        html = response.text
        # print("html:", html)
        #错误处理器
        error_dict = error_processor(html)
        if error_dict:
            print("错误处理器处理完了:",error_dict)
            return error_dict

        #无错误信息的情况
        else:
            soup = BeautifulSoup(html, "html.parser")
            title = soup.select("h3.w990")[0].get_text().strip()
            print("title:", title)

            # 临时的dict
            dict = {}
            try:
                temp_0 =soup.select("table")[-1].select("td")[0].get_text().strip()
                dict[soup.select("table")[-1].select("th")[0].get_text().strip()] = temp_0
            except:
                dict['PAN'] = None
            try:
                temp_1 = soup.select("table")[-1].select("td")[1].get_text().strip()
                dict[soup.select("table")[-1].select("th")[1].get_text().strip()] = temp_1
            except:
                dict['TAN'] = None
            try:
                # Financial Year
                dict[soup.select("table")[-1].select("th")[2].get_text().strip()] = financialYear_
            except:
                dict['Financial Year'] = None
            try:
                # Quarter
                dict[soup.select("table")[-1].select("th")[3].get_text().strip()] = quarter_
            except:
                dict['Quarter'] = None
            try:
                # Type of Return
                dict[soup.select("table")[-1].select("th")[4].get_text().strip()] = Type_of_Return
            except:
                dict['Type of Return'] = None
            try:
                temp_5 = soup.select("table")[-1].select("td")[5].get_text().strip()
                dict[soup.select("table")[-1].select("th")[5].get_text().strip()] = temp_5
            except:
                dict['Count of Records Present'] = None
            try:
                temp_6 = soup.select("table")[-1].select("td")[6].get_text().strip()
                dict[soup.select("table")[-1].select("th")[6].get_text().strip()] = temp_6
            except:
                dict['Remarks (whether quarterly TDS / TCS statement filed)'] = None
            try:
                temp_7 = soup.select("table")[-1].select("td")[7].get_text().strip()
                dict[soup.select("table")[-1].select("th")[7].get_text().strip()] = temp_7
            except:
                dict['Details Viewed On'] = None

            temporary_dict = {}
            # 返回的结果dict
            success_dict = {}
            temporary_dict["successfulInfo"] = dict
            success_dict['comments'] = temporary_dict
            print(success_dict)
            return success_dict


    else:
        return preproccess_dict

    # 判断验证码是否正确
    # if login_preproccess():

    # #否则验证码错误
    # else:
    #     # 临时dict
    #     dict = {}
    #     # 返回dict
    #     error_dict = {}
    #     dict['errorInfo'] = "Text entered does not match with image data"
    #     error_dict['comments'] = dict
    #     return error_dict

#login_go 错误处理器
def error_processor(html):
    """
    错误处理器目前只是处理3个问题：
    1、dedtpan 无效的情况
    2、dedtan  无效的情况
    3、弥补go_results_preproccess 函数在判断financialYear_ 的缺陷
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, "html.parser")
    #临时dict
    dict = {}
    #返回dict
    error_dict = {}
    #错误标注
    err_Summary_flag = soup.select("ul#err_Summary")
    print("err_Summary_flag:",err_Summary_flag)

    if err_Summary_flag:
        err_Summary = soup.select("ul#err_Summary li span")[0].get_text().strip()
        dict['errorInfo'] = err_Summary
        error_dict['comments'] = dict
        return error_dict

dedtpan ="AIRPD1318B"
dedtan = "BLRH00723C"
financialYear_ = "2018-19"
quarter = "Q1"
Type_of_Return = "Salary"
login_go(dedtpan,dedtan,financialYear_,quarter,Type_of_Return)
