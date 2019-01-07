from PIL import Image
from pytesseract import *
import requests
from bs4 import BeautifulSoup
import random
from http.cookiejar import MozillaCookieJar


headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www1.incometaxindiaefiling.gov.in',
            'Origin': 'https://www1.incometaxindiaefiling.gov.in',
        }


def get_ip():
    str_ip = """196.19.63.157:3128
    196.19.63.156:3128
    179.43.138.94:3128
    192.126.129.94:3128
    196.19.70.196:3128
    196.19.70.152:3128
    196.19.70.248:3128
    192.126.129.110:3128
    196.16.208.116:3128
    45.57.186.76:3128
    196.19.70.227:3128
    196.19.70.169:3128
    192.126.129.126:3128
    179.43.138.210:3128
    196.16.208.88:3128
    196.17.143.198:3128
    192.227.149.135:3128
    179.43.138.7:3128
    45.57.186.169:3128
    196.19.63.76:3128
    196.17.143.223:3128
    45.57.186.59:3128
    196.17.143.145:3128
    192.126.129.15:3128
    192.227.149.231:3128
    196.16.208.246:3128
    196.17.143.97:3128
    196.19.70.99:3128
    196.19.63.210:3128
    192.227.149.229:3128
    196.16.208.223:3128
    196.16.208.111:3128
    45.57.186.217:3128
    192.227.149.37:3128
    196.19.63.92:3128
    179.43.138.98:3128
    45.57.186.161:3128
    196.17.143.233:3128
    45.57.186.179:3128
    192.126.129.224:3128
    196.16.208.83:3128
    192.126.129.181:3128
    192.227.149.166:3128
    196.17.143.220:3128
    179.43.138.195:3128
    179.43.138.155:3128
    196.19.70.182:3128
    196.19.63.253:3128
    192.227.149.179:3128
    196.19.70.20:3128"""
    
    ip_list = str_ip.replace("\n", ",").split(",")
    # print(ip_list)
    
    ip = str(random.choice(ip_list)).strip()
    # print(ip)
    proxy_dict = {
        'http': 'http://%s' % ip,
        'https': 'https://%s' % ip
    }
    
    return proxy_dict


def get_browser():
    session = requests.session()
    session.headers = headers
    session.cookies = MozillaCookieJar()
    return session


def handle_captcha(captcha_url,browser):
    
    captcha = browser.get(captcha_url).content
    
    with open('captcha.jpg', 'wb') as f:
        f.write(captcha)
    
    image = Image.open('captcha.jpg')
    text = pytesseract.image_to_string(image).strip()
    
    # print(text)
    if len(text) == 6:
        
        print("验证码是%s" % text)
        return text
    else:
        print('验证码错误，重新识别')
        
        return 'captchaError'
    
    
def handel_maintenance(res):
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        maintenance_info = soup.select('div.col-md-6 h1')[0].string
        # hours = soup.select('span.hours')[0].string
        # minutes = soup.select('span.minutes')[0].string
        # seconds = soup.select('span.seconds')[0].string
        # print(hours,minutes,seconds)

        # print(maintenance_info)
        return maintenance_info
    except:
        pass
    
    
def get_requestId():
    proxy_dict = get_ip()
    browser = get_browser()
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    url='https://www1.incometaxindiaefiling.gov.in/e-FilingGS/Services/VerifyYourPanGSAuthentication.html'
    
    res = browser.get(url=url,headers=headers,proxies = proxy_dict)
    # res = browser.get(url=url,headers=headers)

    maintenance_info = handel_maintenance(res)
    
    if maintenance_info:
        return maintenance_info,'','',''

    cook = res.headers['Set-Cookie']
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    requestId = soup.find_all('input', id='VerifyYourPanGSAuthentication_requestId')[0].attrs['value']
    capcha_url = soup.select("img.captchaImgBox")[0].attrs['src']
    capcha_url = 'https://www1.incometaxindiaefiling.gov.in'+capcha_url
    text = handle_captcha(capcha_url,browser)
    return requestId,cook,text,browser


def handel_errorinfo(html):
    
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        pan_error = soup.find_all(errorfor='VerifyYourPanGSAuthentication_pan')[0].string.strip()
        return 'Invalid PAN. Please retry.'
    except:
        pass
    
    try:
        fullnameError = soup.find_all(errorfor='VerifyYourPanGSAuthentication_fullName')[0].string.strip()
        
        return 'Please enter Full Name.'
    except:
        pass
    
    try:
        captcha_error = soup.find_all(errorfor='VerifyYourPanGSAuthentication_captchaCode')[0].string.strip()
        
        return 'Invalid Code. Please enter the code as appearing in the Image.'
    except:
        pass
    
    
    return "success"
    
    
def main_pan_processing(pan, fullName, dateofBirth, status,report_id):
    # 处理验证码
    # 获取requestid
    requestId,cook,text,browser= get_requestId()
    # print(requestId)
    # requestId 有两个意思，其中一个是表示网站维护的错误信息
    if 'e-Filing website is under maintenance' in requestId:
        return requestId

    if text == 'captchaError':
        return 'captchaError'
    
    Status = {
        "Individual": 'P',
        "Hindu Un-divided Family": 'H',
        "Association Of Persons": 'A',
        "Body Of Individuals": 'B',
        "Company": 'C',
        "Government": 'G',
        "Artificial Juridical Person": 'J',
        "Local Authority": 'L',
        "Firm": 'F',
        "Trust": 'T',

    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Referer': 'https://www1.incometaxindiaefiling.gov.in/e-FilingGS/Services/VerifyYourPanGSAuthentication.html',
        'Cookie': cook,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    
        'Content-Type': 'application/x-www-form-urlencoded',
    
        'Host': 'www1.incometaxindiaefiling.gov.in',
        'Origin': 'https://www1.incometaxindiaefiling.gov.in',
        'Upgrade-Insecure-Requests': '1',
    }
    
    post_data = {
        'requestId':requestId,
        'pan':pan,
        'fullName':fullName,
        'dateOfBirth':dateofBirth,
        'status':Status[status],
        'captchaCode':text
    }
    
    proxy_dict = get_ip()

    url = 'https://www1.incometaxindiaefiling.gov.in/e-FilingGS/Services/VerifyYourPanGSAuthentication.html'
    # html = browser.post(url=url, headers=headers, data=post_data).text

    html = browser.post(url=url, headers=headers, data=post_data,proxies=proxy_dict).text
    # print(html)
    # 处理错误信息
    validInfo = handel_errorinfo(html)
    # print(111111)
    # print(validInfo)
    # print(22222)

    if validInfo == 'Please enter Full Name.':
        return validInfo

    if validInfo == 'Invalid PAN. Please retry.':
        return validInfo
    if validInfo == 'Invalid Code. Please enter the code as appearing in the Image.':
        return 'captchaError'

    if validInfo == 'success':
    
        soup = BeautifulSoup(html, 'html.parser')
        result = soup.select("ul.nonclickBulletedList li span")[0].get_text()
    
        # print(result)
        # if result=='No record found for the given PAN.':
        #     return result
        #
        # if result=='PAN is Active and the details are	matching with PAN database.':
        #
        #     return result
        # if result=='PAN is Active but the details are not matching with PAN database.':
        #     return result
        
        return result
        
        
def main():
    stop = 0
    # pan = 'AKTPM7533P'
    # pan = 'BSJPK4547H'
    # fullName = 'Ayush Kumar'
    #
    #
    # dateofBirth = '19/05/1992'
    # status = 'Individual'
    
    pan = 'DPJPK8650H'

    # fullName = 'GAURAV KUMAR'
    a = 'GAURAV'
    b = ' '
    c = 'KUMAR'
    fullName  = a +b+c

    dateofBirth = '01/02/1996'

    status = 'Individual'
    
    # pan = 'OPJPK865OH'
    # fullName = 'GAURAV KUMAR ANEK PAL SIMGH'
    # dateofBirth = '01/02/1996'
    # status = 'Individual'

    report_id = '20180904062108124275'
    
    

    result = main_pan_processing(pan, fullName, dateofBirth, status,report_id)
    print(result)
    # 如果是验证码错
    if result=="captchaError":
        main()
    
    # 如果是pan卡号码错

    elif result=="Invalid PAN. Please retry.":
        # return result
        pass

    elif result == 'Please enter Full Name.':
        pass
    
    elif 'e-Filing website is under maintenance' in result:
        print(result)
    else:
        print(result)
    
if __name__ == '__main__':
    main()