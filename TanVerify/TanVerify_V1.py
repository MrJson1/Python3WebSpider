import  requests
from http.cookiejar import MozillaCookieJar
from fake_useragent import UserAgent
from bs4 import  BeautifulSoup
import re
from urllib.parse import  urlencode


# 保持会话
def get_session():
    session = requests.Session()
    session.cookies = MozillaCookieJar()
    return session

#获取post 请求的参数
def getLoginStepOne_post_parameter():
    #获取会话
    session = get_session()
    headers = {'User-Agent': UserAgent().random}
    url = "https://www1.incometaxindiaefiling.gov.in/e-FilingGS/Services/KnowYourTanVerify.html"
    response = session.get(url=url, headers=headers, timeout=30)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    try:
        #获取requestId
        requestId = soup.select("input#KnowYourTanVerify_requestId")[0].attrs['value']

        #获取KnowYourTanVerify_searchCriteria_state 的dict
        searchCriteria_state = soup.select("select#KnowYourTanVerify_searchCriteria_state option")
        lenth_searchCriteria_state = len(searchCriteria_state)
        # 计数器
        i = 1
        # 返回的dict
        searchCriteria_state_dict = {}
        while i < lenth_searchCriteria_state:
            lenth_searchCriteria_state -= 1
            key = searchCriteria_state[lenth_searchCriteria_state].get_text().strip()
            value = searchCriteria_state[lenth_searchCriteria_state].attrs['value']
            searchCriteria_state_dict[key] = value

        #获取KnowYourTanVerify_searchCriteria_category 的dict
        searchCriteria_category = soup.select("select#KnowYourTanVerify_searchCriteria_category option")
        lenth_searchCriteria_category = len(searchCriteria_category)
        # 计数器
        j = 1
        #返回的dict
        searchCriteria_category_dict = {}
        while j < lenth_searchCriteria_category:
            lenth_searchCriteria_category -= 1
            key = searchCriteria_category[lenth_searchCriteria_category].get_text().strip()
            value = searchCriteria_category[lenth_searchCriteria_category].attrs['value']
            searchCriteria_category_dict[key] = value
            # print(key, value)

        # print(searchCriteria_category_dict)
        return searchCriteria_category_dict,searchCriteria_state_dict,requestId,session
    except:
        print("网站已更新请更新相应的代码,参数获取不对")
        exit(-1)

#判断发送验证码是否成功
def send_verification_successful(html):

    soup = BeautifulSoup(html, "html.parser")
    #判断成功标识
    successful_flag = 'KnowYourTanVerifyOtp_hindi'
    is_verification_succeed_flag = re.search(successful_flag, html, re.S)

    #识别OTP的长度和Name 不能为空
    sendFail_falg = "errorFor"
    sendFail_falg_ = re.search(sendFail_falg, html, re.S)

    if is_verification_succeed_flag:
        # print(is_verification_succeed_flag)
        flag = 1
        return flag

    elif sendFail_falg_:
        print("sendFail_falg_:",sendFail_falg_)
        errorInfo = soup.select("div.error")[0].get_text().strip()
        # print("errorInfo:",errorInfo)
        return errorInfo


#实现第一步发送OTP
def LoginStepOne(CategoryOfDeductor, State, Name, MobileNumber):
    #临时的
    dict = {}
    #返回的
    error_dict = {}

    #获取LoginStepOne post 的参数
    searchCriteria_category_dict, searchCriteria_state_dict, requestId, session = getLoginStepOne_post_parameter()
    try:
        searchCriteria_category = searchCriteria_category_dict[CategoryOfDeductor]
    except:
        dict['errorInfo'] = "Category of Deductor input error"
        error_dict['comments'] = dict
        return error_dict
    try:
        searchCriteria_state = searchCriteria_state_dict[State]
    except:
        dict['errorInfo'] = "State input error"
        error_dict['comments'] = dict
        return error_dict
    # print(searchCriteria_category)
    # print(searchCriteria_state)
    # print(requestId)

    LoginStepOne_Url = 'https://www1.incometaxindiaefiling.gov.in/e-FilingGS/Services/KnowYourTanVerify.html'
    #post 请求的头
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www1.incometaxindiaefiling.gov.in',
        'Origin': 'https://www1.incometaxindiaefiling.gov.in',
        'Pragma': 'no-cache',
        'Referer': 'https://www1.incometaxindiaefiling.gov.in/e-FilingGS/Services/KnowYourTanVerify.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': UserAgent().random

    }

    FormData = {
        'hindi':'',
        'requestId':requestId,
        'pagniationParam.showAdvSearch':'',
        'searchCriteria.searchOption':'name',
        'searchCriteria.category':searchCriteria_category,
        'searchCriteria.state':searchCriteria_state,
        'searchCriteria.name':Name,
        'searchCriteria.tan':'',
        'mobileOfDeductee': MobileNumber
    }

    response = session.post(url=LoginStepOne_Url,data=FormData,headers=headers, timeout=30)
    # print(response.status_code)
    # print(response.text)
    html = response.text
    # print(html)
    #判断是否发送OTP成功,和错误处理
    flag = send_verification_successful(html)
    if flag == 1:
        dict["html"] = html
        dict["session"] = session
        return dict
        # print(verification_succeed_flag)
        # print("执行了第二步")
        # LoginSteptwo(html,session)

    #识别OTP是否有效和判断Name不能为空
    else:
        dict['errorInfo'] = flag
        error_dict['comments'] = dict
        return error_dict


#获取公司的详细信息
def getCompanyInfo(html):

    soup = BeautifulSoup(html, "html.parser")

    title = soup.select("table.grid caption")[0].get_text().strip()
    print("title:", title)
    title_ = soup.select("table.grid div label")[0].get_text().strip()
    print("title_:", title_)

    labels = soup.select("table.grid div.label ")
    fields = soup.select("table.grid div.field ")

    # 处理labels 的值（左边的数据）
    labelsList = []
    lenth_labels = len(labels)
    # 计算器
    i = 0
    while i < lenth_labels:
        lenth_labels -= 1
        label = labels[lenth_labels].get_text().strip()
        # print(label)
        # 把多余的title_ 去除
        if title_ != label:
            labelsList.append(label)

        if title_ == label:
            print("把多余的title_ 去除的下标：", lenth_labels)

    #list 倒序处理
    labelsList.reverse()
    # 处理fields 的值（右边的数据）,并且数据入字典
    lenth_fields = len(fields)
    # print("lenth_fields:", lenth_fields)
    # 计算器
    j = 0
    # 临时的dict
    TANDetails = {}
    TANAOCode = {}

    while j < lenth_fields:
        lenth_fields -= 1
        # print(lenth_fields)
        field = fields[lenth_fields].get_text().strip()
        # 7作为分割的标识
        if lenth_fields > 7:
            TANAOCode[labelsList[lenth_fields]] = field

        if lenth_fields <= 7:
            TANDetails[labelsList[lenth_fields]] = field

    TANDetailsDict = {}
    TANAOCodeDict = {}
    TANDetailsDict[title] = TANDetails
    TANAOCodeDict[title_] = TANAOCode
    TAN_name = TANDetails['Name']
    # print(TANDetailsDict)
    # print(TANAOCodeDict)
    resultList = []
    resultList.append(TANDetailsDict)
    resultList.append(TANAOCodeDict)

    #临时的dict
    dict = {}
    dict[TAN_name] = resultList

    #返回的dict
    resultDict = {}
    resultDict["TAN_name"] = dict

    return resultDict

#获取单个url公司的信息
def getSingleInfo(url,session):
    #识别单个url 的标识
    flag = "KnowYourTanDetails.html"
    Single_flag = re.search(flag, url, re.S)
    if Single_flag:
        print("Singleurl:",url)
        response = session.get(url)
        resHtml = response.text
        resultDict = getCompanyInfo(resHtml)
        return  resultDict

#错误处理器
def Handle_Error(html):
    #1、No records found.情况
    soup = BeautifulSoup(html, "html.parser")
    #临时的
    dict = {}
    #返回的
    error_dict = {}

    # 1、No records found.情况
    #错误标识actionErrors
    Errorflag = 'actionErrors'
    Error_flag = re.search(Errorflag, html, re.S)
    if Error_flag:

        try:
            handErrors = soup.select("div#actionErrors")[0].get_text().strip()
        except:
            handErrors = Error_flag
        # print("handErrors:", handErrors)
        dict['errorInfo'] = handErrors
        error_dict['comments'] = dict
        print("error_dict:",error_dict)
        return error_dict

    #2、OTP验证码错误,错误标识actionMessages
    OTPflag = "actionMessages"
    OTP_flag = re.search(OTPflag, html, re.S)
    if OTP_flag:
        try:
            OTPErrors = soup.select("div#actionMessages")[0].get_text().strip()
        except:
            OTPErrors = OTP_flag

        dict['errorInfo'] = OTPErrors
        error_dict['comments'] = dict
        print("error_dict:", error_dict)
        return error_dict

def getMobileOTP():
    MobileOTP = input("请输入手机验证码OTP：")
    print("len(MobileOTP):",len(MobileOTP))
    if len(MobileOTP) ==6:
        return MobileOTP

    else:
        print("Invalid OTP. Please retry")
        getMobileOTP()


#获取数据
def LoginAndGetData(CategoryOfDeductor, State, Name, MobileNumber):
    #输入数据预处理是否有效
    LoginStepOneDict = LoginStepOne(CategoryOfDeductor, State, Name, MobileNumber)
    #错误标识
    errorflag = "errorInfo"
    error_flag = re.search(errorflag, str(LoginStepOneDict), re.S)
    # print(error_flag)
    #错误信息直接返回
    if error_flag:
        return LoginStepOneDict
    else:
        html = LoginStepOneDict["html"]
        session = LoginStepOneDict["session"]
        soup = BeautifulSoup(html, "html.parser")
        list = []
        try:
            LoginSteptwo_requestId = soup.select("input#KnowYourTanVerifyOtp_requestId")[0].attrs['value']
            list.append(LoginSteptwo_requestId)
        except:
            print("获取LoginSteptwo_requestId值有错误,网站已经更新")
            exit(-1)
        # print("LoginSteptwo_requestId:", LoginSteptwo_requestId)

        # 实现第二步
        MobileOTP = getMobileOTP()

        # MobileOTP = input("请输入手机验证码OTP：")

        LoginSteptwo_requestId = list[0]
        print("LoginSteptwo_requestId:", LoginSteptwo_requestId)

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www1.incometaxindiaefiling.gov.in',
            'Origin': 'https://www1.incometaxindiaefiling.gov.in',
            'Referer': 'https://www1.incometaxindiaefiling.gov.in/e-FilingGS/Services/KnowYourTanVerify.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': UserAgent().random

        }

        FormData = {
            'requestId': LoginSteptwo_requestId,
            'hindi': '',
            'mobilePin': MobileOTP,
        }

        LoginSteptwo_url = 'https://www1.incometaxindiaefiling.gov.in/e-FilingGS/Services/KnowYourTanVerifyOtp.html'
        Two_response = session.post(url=LoginSteptwo_url, headers=headers, data=FormData,
                                    timeout=30)
        html = Two_response.text
        print("html:", html)

        # 判断OTP是否识别正确
        error_dict = Handle_Error(html)
        if error_dict:
            return error_dict

        else:
            # 多个公司信息返回的list
            MultipleInfoList = []

            soup = BeautifulSoup(html, "html.parser")
            Two_response_url = Two_response.url
            print("Two_response_url:", Two_response_url)

            # 处理错误的情况
            Hand_response = session.get(url=Two_response_url)
            Hand_html = Hand_response.text
            print("Hand_html", Hand_html)
            error_dict = Handle_Error(Hand_html)
            if error_dict:
                return error_dict

            else:
                # 通过Two_response_url判断页面是否有多个公司数据

                # 单个信息的处理
                resultDict = getSingleInfo(Two_response_url, session)
                if resultDict:
                    # print(resultDict)
                    return resultDict

                # 多个信息处理
                else:
                    reportsTopDiv = soup.select("div.reportsTopDiv td a")
                    # 获取总页数
                    pages = reportsTopDiv[-1].get_text().strip()
                    pageNum = int(pages)
                    print("pageNum:", pageNum)

                    # 如果有多个页面url处理
                    while pageNum > 0:
                        # 构建下一页的url
                        """
                        原本的代码是：document.forms[0].action= action + "?requestId="+varRandNum+'&pagniationParam.pageNum='+i;
                        分析requestId是随机的不是必须的参数，构建的时候忽略
                        """
                        base_url = 'https://www1.incometaxindiaefiling.gov.in/e-FilingGS/Services/KnowYourTanPagination.html?'
                        params = {
                            'pagniationParam.pageNum': pageNum
                        }
                        pagesNextUrl = base_url + urlencode(params)
                        print("pagesNextUrl:", pagesNextUrl)
                        print("正在抓取第", pageNum, "页")
                        pageNum -= 1

                        response = session.get(pagesNextUrl)
                        response_html = response.text
                        # print("response_html:",response_html)
                        soup_html = BeautifulSoup(response_html, "html.parser")
                        reportsTopDiv_ = soup_html.select("div.reportsTopDiv td a")

                        # 去除页数的值
                        reportsTopDiv_lenth = len(reportsTopDiv_) - 1
                        # print(reportsTopDiv_)
                        # print(reportsTopDiv_lenth)
                        # 计数器
                        j = 0
                        while j < reportsTopDiv_lenth:
                            reportsTopDiv_lenth -= 1
                            base_href = reportsTopDiv_[reportsTopDiv_lenth].attrs['href']
                            base = 'https://www1.incometaxindiaefiling.gov.in'
                            company_url = base + base_href
                            print("company_url:", company_url)

                            res = session.get(company_url)
                            resHtml = res.text
                            resultDict = getCompanyInfo(resHtml)
                            print("最后返回的结果是：#################################")
                            print("resultDict:", resultDict)
                            print("##########################################")
                            MultipleInfoList.append(resultDict)

                    return MultipleInfoList




CategoryOfDeductor = 'Company/Firms/AOP/BOI/AJP/AOP(Trust) and Branches'
State = 'DELHI'
# State = 'ASSAM'
Name = 'SAPIENT'
# Name = 'SAPIENT (INDIA) PVT. LTD.'
# MobileNumber = '6360773973'
MobileNumber = '9380453065'
result = LoginAndGetData(CategoryOfDeductor, State, Name, MobileNumber)
print("最最最后的结果是################")
print(result)
# print(len(result))






