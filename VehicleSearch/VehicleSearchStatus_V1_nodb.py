import  requests
from http.cookiejar import MozillaCookieJar
from fake_useragent import UserAgent
from bs4 import  BeautifulSoup
from pytesseract import *
from PIL import Image
import boto3
import pymysql
import  json
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random

# 保持会话
def get_session():
    requests.packages.urllib3.disable_warnings()
    session = requests.Session()
    session.cookies = MozillaCookieJar()
    return session

#获取post 请求的参数
def get_post_parameter():
    #获取会话
    try:
        session = get_session()
        headers = {'User-Agent': UserAgent().random}
        vehiclesearchstatus_url = "https://vahan.nic.in/nrservices/faces/user/jsp/SearchStatus.jsp"
        response = session.get(url=vehiclesearchstatus_url,headers=headers,verify=False,timeout = 100)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
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
            
    except:
        SendEmail("2357673823@qq.com", "carinfo进程被卡住")


# 获取验证码
def get_captcha_code(session):
    try:
        captcha_link = "https://vahan.nic.in/nrservices/cap_img.jsp"
        headers = {'User-Agent': UserAgent().random}
        response = session.get(url=captcha_link, headers=headers,verify=False,timeout=100)
        new_filename = str(random.randint(1, 4))
        with open("./captcha_code%s.png"% new_filename, "wb") as fn:
            fn.write(response.content)
        image = Image.open("./captcha_code%s.png" % new_filename)
        captcha = pytesseract.image_to_string(image)
        captcha = captcha.replace(' ', '').replace('|', 'l').replace(']', 'J')
        print(captcha)
        # print(captcha)
        # print(len(captcha))
        # captcha = input("请输入验证码：")
        # 判断验证码是否有效(预处理提高执行效率)
        if len(captcha) != 6:
            print("重新识别")
            get_captcha_code(session)
        else:
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
                
            # image = Image.open("./captcha_code.png%s"% new_filename)
            weight, height = image.size
            out = depoint(image)
            out = denoise_processor(out)
            out.save('./captcha_code1%s.png'% new_filename)
            
            captcha = pytesseract.image_to_string(Image.open('./captcha_code1%s.png'% new_filename))
            captcha = captcha.replace(' ', '').replace('|','l').replace(']','J')
            # print(captcha)
            return captcha
        # print(captcha)
        # print(len(captcha))
        # captcha = input("请输入验证码：")
        # 判断验证码是否有效(预处理提高执行效率)
        # if len(captcha) == 6:
        #     return captcha
        # else:
        #     get_captcha_code(session)
    except:
        SendEmail("2357673823@qq.com", "carinfo验证码被卡住")


#错误处理器
def error_handler(soup):
    try:
        errorInfo = soup.select("#vehiclesearchstatus:msg")[0].get_text().strip()
        if errorInfo=="Either Vehicle No is wrong or Vehicle Details are not digitized.":
            return errorInfo
        elif errorInfo == "Verification Code Mismatch":
            
            return errorInfo
        else:
            return errorInfo
        
    except:
        pass
        
# if soup.select("span#vehiclesearchstatus:msg"):
    #     errorInfo = soup.select("#vehiclesearchstatus:msg")[0].get_text().strip()
    #     # print(errorInfo)
    #     # return errorInfo
    #
    #     if errorInfo=="Either Vehicle No is wrong or Vehicle Details are not digitized.":
    #
    #         return errorInfo
    #
    #     if errorInfo=="Verification Code Mismatch":
    #         return errorInfo
    #
    #     else:
    #         return "fail"





# 返回结果
def RunVehicleSearch(Vehicle_No,report_id):
    # 获取post 请求的参数
    print("y1")
    vehiclesearchstatus, get_vehiclesearchstatus_j_id_jsp_1224339130_11, get_javax_faces_ViewState, session = get_post_parameter()
    # 返回的字典
    print("y2")
    result_dict = {}
    get_captcha = get_captcha_code(session)
    print("y3")
    #输入账号判断是否有效
    if Vehicle_No=="":
        result_dict["comments"] = "Need Your Vehicle No"
        print("y4")
        return result_dict

    #判断验证码是否有效(预处理提高执行效率)
    # elif len(get_captcha) !=6:
    #     result_dict["resultInfo"] = "Verification Code Mismatch"
    #     print("y6")
    #     return result_dict
    
    
    print("y7")
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
    print("y8")
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
    
    print("y9")
    try:
        Search_url = "https://vahan.nic.in/nrservices/faces/user/jsp/SearchStatus.jsp"
        response = session.post(Search_url, data=postData, headers=headers, verify=False,timeout=100)
        print("y10")
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        print("y11")
        # print(soup)
        #错误信息处理
        errorInfo = error_handler(soup)
        print("y12")
        # print(errorInfo)
        
        if errorInfo:
            result_dict["comments"] = errorInfo
            
            print("y13")
            return result_dict
    except:
        SendEmail("2357673823@qq.com", "carinfo进程被卡住：reportid:%s" % (report_id))
        
    else:
        print("y14")
        try:
            title = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_31")[0].get_text().strip()
            print("y15")
                # print(title)
            if "details found at" in title:
            # if "Registration No" in title:
                print("验证码识别准确")
                #获取数据
                try:
                    result_dict["licenseAddress"] =title
                except:
                    
                    result_dict["licenseAddress"] = None
                try:
                    result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_34")[0].get_text().strip().replace(' ','').replace(':','')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_35")[0].get_text().strip()
                except:
                    result_dict['RegistrationNo'] = None
                try:
                    result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_39")[0].get_text().strip().replace(' ','').replace(':','')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_40")[0].get_text().strip()
                except:
                    result_dict['ChassisNo'] = None
                try:
                    result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_44")[0].get_text().strip().replace(' ','').replace(':','')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_45")[0].get_text().strip()
                except:
                    result_dict['OwnerName'] = None
                try:
                    result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_47")[0].get_text().strip().replace(' ','').replace(':','')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_48")[0].get_text().strip()
                except:
                    result_dict['VehicleClass'] = None
                try:
                    result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_52")[0].get_text().strip().replace(' ','').replace(':','')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_53")[0].get_text().strip()
                except:
                    result_dict['Maker/Model'] = None
                try:
                    result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_55")[0].get_text().strip().replace(' ','').replace(':','')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_56")[0].get_text().strip()
                except:
                    result_dict['FitnessUpto'] = None
                try:
                    result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_60")[0].get_text().strip().replace(' ','').replace(':','')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_61")[0].get_text().strip()
                except:
                    result_dict['PollutionNorms'] = None
                try:
                    result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_65")[0].get_text().strip().replace(' ','').replace(':','')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_66")[0].get_text().strip()
                except:
                    result_dict["Financier'sName"] = None
                #右边数据
                try:
                    result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_36")[0].get_text().strip().replace(' ','').replace(':','')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_37")[0].get_text().strip()
                except:
                    result_dict['RegistrationDate'] = None
                try:
                    result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_41")[0].get_text().strip().replace(' ','').replace(':','')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_42")[0].get_text().strip()
                except:
                    result_dict['EngineNo'] = None
                try:
                    result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_49")[0].get_text().strip().replace(' ','').replace(':','')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_50")[0].get_text().strip()
                except:
                    result_dict['Fuel'] = None
                try:
                    result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_57")[0].get_text().strip().replace(' ','').replace(':','')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_58")[0].get_text().strip()
                except:
                    result_dict['InsuranceUpto'] = None
                try:
                    result_dict[soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_62")[0].get_text().strip().replace(' ','').replace(':','')] = soup.select("#vehiclesearchstatus:j_id_jsp_1224339130_63")[0].get_text().strip()
                except:
                    result_dict['Status'] = None
                    
                result_dict2 ={}
                result_dict2['report'] = result_dict
                result_dict2['comments'] = "success"
                
                return result_dict2
            
            else:
                result_dict['comments'] = None
                htmlText = 'carinfo没有抓取到title异常报告%s'%report_id
                
                SendEmail("2357673823@qq.com",htmlText)
                
        except:
            result_dict['comments'] = None
            




def SendEmail(toAdd, htmlText):
    strFrom = "1214861939@qq.com"
    strTo = toAdd
    msg = MIMEText(htmlText)
    msg['Content-Type'] = 'Text/HTML'
    msg['Subject'] = Header("carinfo错误报告", 'utf-8')
    msg['To'] = strTo
    msg['From'] = strFrom
    try:
        smtpServer = smtplib.SMTP_SSL('smtp.qq.com', '465')
        smtpServer.ehlo()
        smtpServer.login('1214861939@qq.com', 'clleujeyfpbzhhbi')
        smtpServer.sendmail(strFrom, strTo, msg.as_string())
        smtpServer.close()
    except Exception as e:
        print('Exception: send email failed', e)
        return 'failed to send mail'
        






if __name__ == '__main__':
        try:
            time.sleep(0.5)
            aws_access_key_id = 'AKIAIMYPHVRMHZ76PSOA'
            aws_secret_access_key = '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'
            dynamodb = boto3.resource(service_name='dynamodb',aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,region_name='ap-south-1')
            sqs = boto3.resource(service_name='sqs',aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,region_name='ap-south-1')
            queue = sqs.get_queue_by_name(QueueName='vehicle')
            sqs_msg = queue.receive_messages(MaxNumberOfMessages=1)[0]
            
            try:
                report_info=json.loads(sqs_msg.body)
                report_info_json=json.dumps(report_info)
            except:
                report_info={}
                report_info['report_id']='empty'
            if report_info['report_id'] != 'empty':
                report_id = report_info['report_id']
                print("x0")
                callbackURL = report_info['callbackURL']
                print(report_id)
                try:
                    regist_no = report_info['regist_no'].strip()
                except:
                    regist_no = ''
                if ' ' in regist_no: 
                    part_a = regist_no.split(' ',2)[0]
                    part_b = regist_no.split(' ',2)[1]
                    print(part_a)
                    print(part_b)
                else:
                    part_a=regist_no[0:6]
                    part_b=regist_no[6:10]
                    print(part_a)
                    print(part_b)
                print("x1")
                stop = 0
                while stop < 30:
                    stop = stop + 1
                    try:
                        Vehicle_No = part_a + part_b
                        print(Vehicle_No)
                        result_dict = RunVehicleSearch(Vehicle_No,report_id)
                        print(result_dict)
                        # print(result_dict)
                        result = result_dict['comments']
                        # print(result)
                        
                        print("x2")
                        if result =="Need Your Vehicle No":
                            print(111111111111)
                            stop = 31
                            result_dict['comments'] = result
                            report={}
                            report["licenseAddress"]=None
                            report['RegistrationNo']=regist_no
                            report['ChassisNo']=None
                            report['OwnerName']=None
                            report['VehicleClass']=None
                            report['Maker/Model']=None
                            report['FitnessUpto']=None
                            report['PollutionNorms']=None
                            report["Financier'sName"]=None
                            report['RegistrationDate']=None
                            report['EngineNo']=None
                            report['Fuel']=None
                            report['InsuranceUpto']=None
                            report['Status']=result
                            result_dict['report']=report
                            
                        elif result =="Please input correct Vehicle No":
                            print(2222222222)
                            stop = 31
                            report={}
                            result_dict['comments'] = result
                            report["licenseAddress"]=None
                            report['RegistrationNo']=regist_no
                            report['ChassisNo']=None
                            report['OwnerName']=None
                            report['VehicleClass']=None
                            report['Maker/Model']=None
                            report['FitnessUpto']=None
                            report['PollutionNorms']=None
                            report["Financier'sName"]=None
                            report['RegistrationDate']=None
                            report['EngineNo']=None
                            report['Fuel']=None
                            report['InsuranceUpto']=None
                            report['Status']=result
                            result_dict['report']=report
                        elif result =="Either Vehicle No is wrong or Vehicle Details are not digitized.":
                            print(333333333)
                            stop = 31
                            
                            result_dict['comments'] = result
                            report={}
                            report["licenseAddress"]=None
                            report['RegistrationNo']=regist_no
                            report['ChassisNo']=None
                            report['OwnerName']=None
                            report['VehicleClass']=None
                            report['Maker/Model']=None
                            report['FitnessUpto']=None
                            report['PollutionNorms']=None
                            report["Financier'sName"]=None
                            report['RegistrationDate']=None
                            report['EngineNo']=None
                            report['Fuel']=None
                            report['InsuranceUpto']=None
                            report['Status']=result
                            result_dict['report']=report
                            
                        elif result == "Verification Code Mismatch" or result=='Enter captcha Value':
                            
                            if stop == 30:
                                result_dict['comments'] = None
                        elif result == None:
                            stop = 31
                            result_dict['comments'] = "No information was queried"
                            
                        else:
                            print(555555)
                            stop = 31
                            pass
                        
                        
                    except:
                        pass
                    
                    
                # print(result_dict)
                report=result_dict['report']
                report['report_id']=report_id
                report['callbackURL']=callbackURL
                report['regist_no']=regist_no
                time.sleep(1)
                print("x3")
                print(result_dict)
        except:

            time.sleep(2)
            pass















