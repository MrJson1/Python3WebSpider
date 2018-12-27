import  requests
from http.cookiejar import MozillaCookieJar
from fake_useragent import UserAgent
from bs4 import  BeautifulSoup
from pytesseract import *
from PIL import Image

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
    vehiclesearchstatus_url = "https://vahan.nic.in/nrservices/faces/user/jsp/SearchStatus.jsp"
    response = session.get(url=vehiclesearchstatus_url,headers=headers,verify=False)
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    # print(soup)
    try:
        vehiclesearchstatus = soup.select("input")[2].attrs["value"]
        get_vehiclesearchstatus_j_id_jsp_1224339130_11 = soup.select("input")[4].attrs["value"]
        get_javax_faces_ViewState = soup.select("input")[1].attrs["value"]

        # print(vehiclesearchstatus)
        # print(get_vehiclesearchstatus_j_id_jsp_1224339130_11)
        # print(get_javax_faces_ViewState)
        return vehiclesearchstatus,get_vehiclesearchstatus_j_id_jsp_1224339130_11,get_javax_faces_ViewState,session
    except:
        print("网站已更新请更新相应的代码,参数获取不对")
        exit(-1)

# 获取验证码
def get_captcha_code(session):
    captcha_link = "https://vahan.nic.in/nrservices/cap_img.jsp"
    headers = {'User-Agent': UserAgent().random}

    response = session.get(url=captcha_link, headers=headers,verify=False)
    with open("./captcha_code.png", "wb") as fn:
        fn.write(response.content)

    def get_bin_table(threshold=160):
        """
        获取灰度转二值的映射table
        :param threshold:
        :return:
        """
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)

        return table

    def depoint(img):  # input: gray image
        pixdata = img.load()
        w, h = img.size
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                count = 0
                if pixdata[x, y - 1] > 245:
                    count = count + 1
                if pixdata[x, y + 1] > 245:
                    count = count + 1
                if pixdata[x - 1, y] > 245:
                    count = count + 1
                if pixdata[x + 1, y] > 245:
                    count = count + 1
                if count > 2:
                    pixdata[x, y] = 255
        return img

    def denoise_processor(img):
        imgry = img.convert('L')  # 转化为灰度图
        imgry.save('1-hui.png')
        table = get_bin_table()
        out = imgry.point(table, '1')
        for x in range(1, weight - 1):
            for y in range(1, height - 1):
                nearDots = 0
                if not out.getpixel((x - 1, y)):  # 左
                    nearDots += 1
                if not out.getpixel((x + 1, y)):  # 右
                    nearDots += 1
                if not out.getpixel((x, y - 1)):  # 下
                    nearDots += 1
                if not out.getpixel((x, y + 1)):  # 上
                    nearDots += 1
                if not out.getpixel((x - 1, y + 1)):  # 左上
                    nearDots += 1
                if not out.getpixel((x - 1, y - 1)):  # 左下
                    nearDots += 1
                if not out.getpixel((x + 1, y + 1)):  # 右上
                    nearDots += 1
                if not out.getpixel((x + 1, y - 1)):  # 右下
                    nearDots += 1
                if nearDots < 4:
                    out.putpixel((x, y), 1)
                for i in range(height):  # 清除边框
                    out.putpixel((0, i), 1)
                    out.putpixel((weight - 1, i), 1)
                for j in range(weight):
                    out.putpixel((j, 0), 1)
                    out.putpixel((j, height - 1), 1)
        return out

    image = Image.open("./captcha_code.png")
    weight, height = image.size
    out = depoint(image)
    out = denoise_processor(out)
    out.save('./captcha_code1.png')

    captcha = pytesseract.image_to_string(Image.open('./captcha_code1.png'))
    captcha = captcha.replace(' ', '').replace('|','l').replace(']','J')
    print(captcha)
    # print(len(captcha))
    # captcha = input("请输入验证码：")
    return captcha

#错误处理器
def error_handler(soup):
    if soup.select("span#vehiclesearchstatus:msg"):
        errorInfo = soup.select("#vehiclesearchstatus:msg")[0].get_text().strip()
        print(errorInfo)
        return errorInfo
        # if errorInfo=="Either Vehicle No is wrong or Vehicle Details are not digitized.":
        #     return errorInfo
        # elif errorInfo=="Verification Code Mismatch":
        #     return errorInfo

# 返回结果
def RunVehicleSearch(Vehicle_No):
    # 获取post 请求的参数
    vehiclesearchstatus, get_vehiclesearchstatus_j_id_jsp_1224339130_11, get_javax_faces_ViewState, session = get_post_parameter()
    # 返回的字典
    result_dict = {}
    get_captcha = get_captcha_code(session)

    #输入账号判断是否有效
    if Vehicle_No=="":
        result_dict["resultAccountErrorInfo"] = "Need Your Vehicle No"
        return result_dict
    #判断验证码是否有效(预处理提高执行效率)
    elif  len(get_captcha) !=6:
        result_dict["resultInfo"] = "Verification Code Mismatch"
        return result_dict

    #post 请求的头
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://vahan.nic.in/nrservices/faces/user/jsp/SearchStatus.jsp',
        'User-Agent': UserAgent().random,
        'Host': 'vahan.nic.in',
        'Origin': 'https://vahan.nic.in',
        'Upgrade-Insecure-Requests': '1'
    }
    postData = {
        'vehiclesearchstatus':'vehiclesearchstatus',
        'vehiclesearchstatus:j_id_jsp_1224339130_2': '',
        'vehiclesearchstatus:j_id_jsp_1224339130_11': get_vehiclesearchstatus_j_id_jsp_1224339130_11,
        'vehiclesearchstatus:regn_no1_exact':Vehicle_No,
        # 'vehiclesearchstatus:regn_no2_exact':Vehicle_No2,
        'vehiclesearchstatus:txt_ALPHA_NUMERIC': get_captcha,
        'vehiclesearchstatus:j_id_jsp_1224339130_28': 'Search Vehicle',
        'javax.faces.ViewState': get_javax_faces_ViewState,
        'ctl00$ContentPlaceHolder1$ButtonSearch': 'Search'
    }

    Search_url = "https://vahan.nic.in/nrservices/faces/user/jsp/SearchStatus.jsp"
    response = session.post(Search_url, data=postData, headers=headers, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    # print(soup)
    #错误信息处理
    errorInfo = error_handler(soup)
    print(errorInfo)

    if errorInfo:
        result_dict["resultInfo"] = errorInfo
        return result_dict

    else:
        try:
            title = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_31")[0].get_text().strip()
            print("title:",title)
            print(soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_66")[0].get_text().strip(),"OK")
        except:
            title = None
        # 获取数据
        try:
            result_dict["licenseAddress"] = title
        except:

            result_dict["licenseAddress"] = None
        try:
            result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_34")[0].get_text().strip().replace(' ',
                                                                                                                 '').replace(
                ':', '')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_35")[0].get_text().strip()
        except:
            result_dict['RegistrationNo'] = None
        try:
            result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_39")[0].get_text().strip().replace(' ',
                                                                                                                 '').replace(
                ':', '')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_40")[0].get_text().strip()
        except:
            result_dict['ChassisNo'] = None
        try:
            result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_44")[0].get_text().strip().replace(' ',
                                                                                                                 '').replace(
                ':', '')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_45")[0].get_text().strip()
        except:
            result_dict['OwnerName'] = None
        try:
            result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_47")[0].get_text().strip().replace(' ',
                                                                                                                 '').replace(
                ':', '')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_48")[0].get_text().strip()
        except:
            result_dict['VehicleClass'] = None
        try:
            result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_52")[0].get_text().strip().replace(' ',
                                                                                                                 '').replace(
                ':', '')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_53")[0].get_text().strip()
        except:
            result_dict['Maker/Model'] = None
        try:
            result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_55")[0].get_text().strip().replace(' ',
                                                                                                                 '').replace(
                ':', '')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_56")[0].get_text().strip()
        except:
            result_dict['FitnessUpto'] = None
        try:
            result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_60")[0].get_text().strip().replace(' ',
                                                                                                                 '').replace(
                ':', '')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_61")[0].get_text().strip()
        except:
            result_dict['PollutionNorms'] = None
        try:
            if soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_66")[0].get_text().strip():
                result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_65")[0].get_text().strip().replace(' ',
                                                                                                                     '').replace(
                    ':', '')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_66")[0].get_text().strip()
            else:
                result_dict[
                    soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_65")[0].get_text().strip().replace(' ',
                                                                                                             '').replace(
                        ':', '')] = None

        except:
            result_dict["Financier'sName"] = None
        # 右边数据
        try:
            result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_36")[0].get_text().strip().replace(' ',
                                                                                                                 '').replace(
                ':', '')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_37")[0].get_text().strip()
        except:
            result_dict['RegistrationDate'] = None
        try:
            result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_41")[0].get_text().strip().replace(' ',
                                                                                                                 '').replace(
                ':', '')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_42")[0].get_text().strip()
        except:
            result_dict['EngineNo'] = None
        try:
            result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_49")[0].get_text().strip().replace(' ',
                                                                                                                 '').replace(
                ':', '')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_50")[0].get_text().strip()
        except:
            result_dict['Fuel'] = None
        try:
            result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_57")[0].get_text().strip().replace(' ',
                                                                                                                 '').replace(
                ':', '')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_58")[0].get_text().strip()
        except:
            result_dict['InsuranceUpto'] = None
        try:
            result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_62")[0].get_text().strip().replace(' ',
                                                                                                                 '').replace(
                ':', '')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_63")[0].get_text().strip()
        except:
            result_dict['Status'] = None
        # dict = {}
        # dict[title] = result_dict
        return result_dict


# for i in range(10):
#     print("############执行第：",i,"次")
#     j = 1
#     result_dict = RunVehicleSearch("MH06T", "7161")
#     print(result_dict)

result_dict = RunVehicleSearch("MH06T7161")
print(result_dict)








