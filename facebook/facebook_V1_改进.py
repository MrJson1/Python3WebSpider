import  requests
from http.cookiejar import MozillaCookieJar
from fake_useragent import UserAgent
from bs4 import  BeautifulSoup
import re


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
    facebook_Loginurl = "https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=100"
    response = session.get(url=facebook_Loginurl, headers=headers)
    html = response.text
    # print(html)
    soup = BeautifulSoup(html, "html.parser")
    try:
        jazoest = soup.select("input")[0].attrs['value']
        lsd = soup.select("input")[1].attrs['value']
        lgnrnd = soup.select("input")[14].attrs['value']
        lgnjs = soup.select("input")[15].attrs['value']
        # print("jazoest:",jazoest)
        # print("lsd:",lsd)
        # print("lgnrnd:",lgnrnd)
        # print("lgnjs:",lgnjs)
        return jazoest,lsd,lgnrnd,lgnjs,session
    except:
        print("网站已更新请更新相应的代码,参数获取不对")
        exit(-1)

def handle_FaceLoginError(html):
    pass

#登录
def FacebookLogin(email,password):
    jazoest, lsd, lgnrnd, lgnjs, session = get_post_parameter()
    headers = {
        'authority':'www.facebook.com',
        'method':'POST',
        'path':'/login/device-based/regular/login/?login_attempt=1&lwv=100',
        'scheme':'https',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9',
        'cache-control':'max-age=0',
        'content-type':'application/x-www-form-urlencoded',
        'origin':'https://www.facebook.com',
        'referer':'https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=110',
        'upgrade-insecure-requests':'1',
        'user-agent':UserAgent().random,
    }

    formData = {
        'jazoest': jazoest,
        'lsd': lsd,
        'display': '',
        'enable_profile_selector': '',
        'isprivate': '',
        'legacy_return': '0',
        'profile_selector_ids': '',
        'return_session': '',
        'skip_api_login': '',
        'signed_next': '',
        'trynum': '1',
        'timezone': '-480',
        'lgndim': 'eyJ3IjoxMzY0LCJoIjo3NjgsImF3IjoxMzY0LCJhaCI6NzI0LCJjIjoyNH0=',
        'lgnrnd': lgnrnd,
        'lgnjs': lgnjs,
        'email': email,
        'pass': password,
        'prefill_contact_point': email,
        'prefill_source': 'browser_dropdown',
        'prefill_type': 'password',
        'first_prefill_source': 'browser_dropdown',
        'first_prefill_type': 'contact_point',
        'had_cp_prefilled': 'true',
        'had_password_prefilled': 'true',
        'ab_test_data': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB',

    }
    post_url = 'https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=100'

    response = session.post(url=post_url, data=formData, headers=headers)
    print(response.status_code)
    print(response.text)
    res = session.get(url="https://www.facebook.com/?sk=welcome")
    # print(res.text)
    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    personal_homepage_url = soup.select("div._1k67._cy7  a")[0].attrs['href']
    print(personal_homepage_url)
    #获取cookie
    session.get(personal_homepage_url)
    #获取个人的简介信息
    resultList = getPersonalInfo(session,personal_homepage_url)
    return resultList

#获取信息单个功能,并且返回列表
def getSingleInfoList(session,WorkUrl):
    print("WorkUrl:", WorkUrl)
    res = session.get(WorkUrl)
    WorkHtml_ = res.text
    #获取的数据需要去除注释的JS
    WorkHtml = WorkHtml_.replace('<!--', '').replace('-->', '')
    WorkSoup = BeautifulSoup(WorkHtml, "html.parser")
    temp = WorkSoup.select("div._4qm1")
    lenth_Work = len(temp)
    print("lenth_Workeducation:", lenth_Work)
    WorkedList = []
    # 计数器
    i = 0
    while i < lenth_Work:
        dict = {}
        lenth_Work -= 1
        # 获取标题
        title = temp[lenth_Work].select("span")[0].get_text().strip()
        # print("title:", title)
        # 获取一个标题中全部的信息
        useful = str(temp[lenth_Work].get_text().strip())
        # 获取小标题
        usefulSmallTitle = temp[lenth_Work].select("div._2lzr._50f5._50f7")
        # 获取小标题里面的内容
        usefulSmallTitleDetail = temp[lenth_Work].select("div.fsm.fwn.fcg")
        # 存储数据
        DetailDict = {}

        # 计算器
        j = 0
        lenth_usefulSmallTitle = len(usefulSmallTitle)
        # print("lenth_usefulSmallTitle:", lenth_usefulSmallTitle)
        if lenth_usefulSmallTitle > 0:

            while j < lenth_usefulSmallTitle:
                lenth_usefulSmallTitle -= 1
                SmallTitle = usefulSmallTitle[lenth_usefulSmallTitle].get_text().strip()
                SmallTitleDetail = usefulSmallTitleDetail[lenth_usefulSmallTitle].get_text().strip()
                # print("SmallTitle:", SmallTitle)
                # print("SmallTitleDetail", SmallTitleDetail)
                DetailDict[SmallTitle] = SmallTitleDetail
                dict[title] = DetailDict
            WorkedList.append(dict)
        else:
            uselessRedact = temp[lenth_Work].select("a")[-1].get_text().strip()
            # print(uselessRedact)
            returnUseful = useful.replace(uselessRedact, "").replace(title, "")
            # print(returnUseful)
            # 数据存储
            dict[title] = returnUseful
            WorkedList.append(dict)

    return WorkedList

#获取生活纪事信息单个功能,并且返回列表
def getSingYearOverviewsleInfoList(session,WorkUrl):
    print("WorkUrl:", WorkUrl)
    res = session.get(WorkUrl)
    WorkHtml_ = res.text
    #获取的数据需要去除注释的JS
    WorkHtml = WorkHtml_.replace('<!--', '').replace('-->', '')
    WorkSoup = BeautifulSoup(WorkHtml, "html.parser")
    temp = WorkSoup.select("div._4qm1")
    WorkSoup_ = BeautifulSoup(str(temp), "html.parser")

    yearList = WorkSoup_.select("span._50f8._2iem")
    yearListDetail = WorkSoup_.select("div._4bl9")
    lenth_Work = len(yearList)
    # print("lenth_Work:", lenth_Work)
    WorkedList = []
    # 计数器
    i = 0
    while i < lenth_Work:
        dict = {}
        lenth_Work -= 1
        # 获取年份
        year = yearList[lenth_Work].get_text().strip()
        # print("year:", year)
        # 获取一个年份详细信息
        yearDetail = yearListDetail[lenth_Work].get_text().strip()
        # print("yearDetail:", yearDetail)
        dict[year] = yearDetail
        WorkedList.append(dict)

    # print(WorkedList)
    return WorkedList

#获取你生活过的地方信息单个功能,并且返回列表
def getSingleWhereLivedInfoList(session,WorkUrl):
    print("WorkUrl:", WorkUrl)
    res = session.get(WorkUrl)
    WorkHtml_ = res.text
    #获取的数据需要去除注释的JS
    WorkHtml = WorkHtml_.replace('<!--', '').replace('-->', '')
    WorkSoup = BeautifulSoup(WorkHtml, "html.parser")
    temp = WorkSoup.select("div._4qm1")
    lenth_Work = len(temp)
    # print(temp)
    WorkedList = []
    # 计数器
    i = 0
    while i < lenth_Work:
        DataDict = {}
        dict = {}
        lenth_Work -= 1
        # 获取标题
        title = temp[lenth_Work].select("span")[0].get_text().strip()
        # print("title:", title)
        titleInfoList = temp[lenth_Work].select("span._2iel._50f7 a")
        titleInfoDetailList = temp[lenth_Work].select("div.fsm.fwn.fcg")
        lenth = len(titleInfoList)
        # 计数器
        j = 0
        while j < lenth:
            lenth -= 1
            temp_ = titleInfoList[lenth].get_text().strip()
            dict[temp_] = titleInfoDetailList[lenth].get_text().strip()
        # print(dict)
        DataDict[title] = dict
        # print(DataDict)
        WorkedList.append(DataDict)

    return WorkedList

#获取联系方式和基本信息单个功能,并且返回列表
def getSingleContactInfoList(session,WorkUrl):
    print("WorkUrl:", WorkUrl)
    res = session.get(WorkUrl)
    WorkHtml_ = res.text
    #获取的数据需要去除注释的JS
    WorkHtml = WorkHtml_.replace('<!--', '').replace('-->', '')
    WorkSoup = BeautifulSoup(WorkHtml, "html.parser")
    temp = WorkSoup.select("div._4qm1")
    # print(temp)
    lenth_Work = len(temp)
    print("lenth_Work:", lenth_Work)
    WorkedList = []
    # 计数器
    i = 0
    while i < lenth_Work:
        lenth_Work -= 1
        # 获取标题
        title = temp[lenth_Work].select("span")[0].get_text().strip()
        # print("title:", title)
        # 获取左边标题中全部的信息
        LeftSmallTitle = temp[lenth_Work].select("span._50f4._5kx5")
        LeftLenth = len(LeftSmallTitle)
        # print("LeftSmallTitle:",LeftSmallTitle)
        # 获取右边边标题中全部的信息
        RightSmallTitle = temp[lenth_Work].select("span._2iem")
        RightLenth = len(RightSmallTitle)
        # print("RightSmallTitle:",RightSmallTitle)
        # print(LeftLenth)
        # print(RightLenth)
        TitleDataDict = {}
        # 存储数据
        DataDict = {}
        # 计数器
        j = 0
        while j < LeftLenth:
            # 排除左边的数据大于右边数据长度的情况（例如：联系方式）
            LeftLenth -= 1
            RightLenth -= 1
            if RightLenth >= 0:
                LeftData = LeftSmallTitle[LeftLenth].get_text().strip()
                RightData = RightSmallTitle[LeftLenth].get_text().strip()
                DataDict[LeftData] = RightData
        # print(DataDict)
        TitleDataDict[title] = DataDict
        # print(TitleDataDict)
        WorkedList.append(TitleDataDict)

    return WorkedList

#获取主页的简介信息
def getPersonalInfo(session,base_url):
    #返回的list
    resultList = []
    #简介
    portionUrl = '/about'
    about_url = base_url + portionUrl
    response = session.get(about_url)
    oerview_html = response.text
    #获取的数据需要去除注释的JS
    html = oerview_html.replace('<!--', '').replace('-->', '')
    soup = BeautifulSoup(html,"html.parser")
    # print(soup)
    #获取所有的左边标题
    Titles = re.findall(r'sectionTitles:\[(.+?)\]', oerview_html)[0]
    TitleList = Titles.split(",")

    #概览
    overviewDict =  {}
    overviewList = []
    oerviewTitle = TitleList[0].replace('"','')
    print(oerviewTitle)

    #获取左边概览的列表
    LeftList = soup.select("div._6a._5u5j._6b")
    lenth_LeftList = len(LeftList)
    # print("左边概览的列表长度:",LeftList)
    #计数器
    i = 0
    while i < lenth_LeftList:
        lenth_LeftList -= 1
        #获取多余的信息
        useless = LeftList[lenth_LeftList].select("div._5wn5._2kin._50f3")[0].get_text().strip()
        # print(useless)
        #获取所有的信息
        uesful = LeftList[lenth_LeftList].get_text().strip()
        # print(uesful)
        #过滤信息
        uesfulInfo = str(uesful).replace(useless, '').replace("\n", '')
        # print(uesfulInfo)
        overviewList.append(uesfulInfo)

    #获取家庭成员的个数
    familyNO = soup.select("span._c24._2iem")[0].get_text().strip()
    overviewList.append(familyNO)

    #获取右边概览的列表
    tempHtml = soup.select("div.hidden_elem")[-1]
    # print(tempHtml)
    items = tempHtml.select("div span div")
    lenth_items = len(items)
    # print(lenth_items)
    # print(items)
    # 计算器
    k = lenth_items / 2
    j = -1

    while k > 0:
        j += 2
        tempItme = items[j].get_text().strip()
        # print(tempItme)
        overviewList.append(tempItme)
        k -= 1
    print("########################################")
    overviewDict[oerviewTitle] = overviewList
    # print(overviewDict)
    resultList.append(overviewDict)
    print("##################################")


    #工作与学历
    WorkEducationDict = {}
    WorkeducationTitle = TitleList[1].replace('"','')
    print(WorkeducationTitle)

    portionUrl = '/about?section=education'
    WorkEducationUrl = base_url + portionUrl
    WorkedList = getSingleInfoList(session,WorkEducationUrl)
    WorkEducationDict[WorkeducationTitle] = WorkedList
    # print(WorkEducationDict)
    resultList.append(WorkEducationDict)
    print("##################################")


    #你生活过的地方
    WhereLivedDict ={}
    WhereLivedTitle = TitleList[2].replace('"', '')
    print(WhereLivedTitle)

    portionUrl = '/about?section=living'
    WhereLivedUrl = base_url + portionUrl
    WorkedList = getSingleWhereLivedInfoList(session,WhereLivedUrl)
    WhereLivedDict[WhereLivedTitle] = WorkedList
    # print(WhereLivedDict)
    resultList.append(WhereLivedDict)
    print("##################################")


    #联系方式和基本信息
    ContactBasicDict = {}
    ContactBasicTitle = TitleList[3].replace('"', '')
    print(ContactBasicTitle)

    portionUrl = '/about?section=contact-info'
    contactUrl = base_url + portionUrl
    WorkedList = getSingleContactInfoList(session,contactUrl)
    ContactBasicDict[ContactBasicTitle] = WorkedList
    # print(ContactBasicDict)
    resultList.append(ContactBasicDict)
    print("##################################")


    #家庭成员与感情状况
    FamilyDict = {}
    FamilyTitle = TitleList[4].replace('"', '')
    print(FamilyTitle)

    portionUrl = '/about?section=relationship'
    relationshipUrl = base_url + portionUrl
    WorkedList = getSingleInfoList(session,relationshipUrl)
    FamilyDict[FamilyTitle] = WorkedList
    # print(FamilyDict)
    resultList.append(FamilyDict)
    print("##################################")


    #你的详细资料
    DetailsDict = {}
    DetailsTitle = TitleList[5].replace('"', '')
    print(DetailsTitle)

    portionUrl = '/about?section=bio'
    bioUrl = base_url + portionUrl
    WorkedList = getSingleInfoList(session,bioUrl)
    DetailsDict[DetailsTitle] = WorkedList
    # print(DetailsDict)
    resultList.append(DetailsDict)
    print("##################################")


    #生活纪事
    ChronicleDict = {}
    ChronicleTitle = TitleList[6].replace('"', '')
    print(ChronicleTitle)
    year_overviewsUrl = "https://www.facebook.com/lang.song.180072/about?section=year-overviews"
    WorkedList = getSingYearOverviewsleInfoList(session,year_overviewsUrl)
    ChronicleDict[ChronicleTitle] = WorkedList
    # print(ChronicleDict)
    resultList.append(ChronicleDict)
    print("##################################")

    return resultList

resultList = FacebookLogin("13765159785","SL13985191033")
# resultList = FacebookLogin("18485592160","15185764374abc")
print(resultList)



