# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import  json
from flask import Flask,jsonify
from flask import request
import  random
import  re
import time
from email_V1.connect import session
from email_V1.email_modules import email_info
import codecs
import pymysql
import pandas as pd
import csv
from email.utils import formataddr

#主要处理邮箱系统的类
"""
0、倒入config配置文件
1、初始化邮箱的配置和mysql连接
2、生成4位验证码
3、构建当前时间和4位随机数的request_id
4、验证邮箱的是否有效
5、存储邮箱操作的信息函数（每一次的请求都保存）
6、发送验证邮箱同时返回验证码
7、发邮箱
8、查询公司薪水的信息
9、查询公司地址的信息
10、根据用户提供的域名查询公司的全部相关信息（返回查询到的公司信息，暂时不做任何处理，后续判断方便）
"""
class EmailSystem:
    __mail_user = '' # 登陆邮箱
    __mail_password = '' # 邮箱授权码
    __senderName= '' # 发件人

    #倒入config配置文件
    def load_json(self, path):
        try:
            with open(path) as json_file:
                data = json.load(json_file)
        except Exception as e:
            print('ERROR: no such file like ' + path)
            print(e)
            exit(-1)
        else:
            return data

    def __init__(self):
        conf = self.load_json("./config")
        self.__mail_user=conf['mail_user']
        self.__mail_password=conf['mail_password']
        self.__senderName=conf['senderName']
        self.subject = conf['subject']
        self.mail_host = conf['mail_host']
        self.mail_port = conf['mail_port']
        self.time = time
        #连接数据库
        self.db = pymysql.connect(
            host=conf['host'],
            user=conf['user'],
            passwd=conf['passwd'],
            database=conf['database'],
        )
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()

    #生成4位验证码
    def random_captcha(self):
        # 用来保存生成的随机数或字母
        list = ""
        # range(x)生成x个随机数的验证码
        for i in range(4):
            # 跟随循环生成一个0-4之间的随机数来决定生成的是大小写字母还是数字
            j = random.randrange(0, 4)
            # 随机产生的数字是1时，生成数字
            if j == 1:
                a = random.randrange(0, 10)
                list = list + str(a)
            # 随机产生的数字是2时，生成大写字母
            elif j == 2:
                a = chr(random.randrange(65, 91))
                list = list + a
            # 随机产生的数字是除了1和2时，生成小写字母
            else:
                a = chr(random.randrange(97, 123))
                list = list + a
        return list

    #构建当前时间和4位随机数的request_id
    def set_request_id(self):
        strandom = ""
        for i in range(4):
            #ord(char)函数将char类型的单字符转换成ASCII码值
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            strandom += ch
        request_id = str(self.time.time()).split(".")[0] + str(self.time.time()).split(".")[1] + strandom
        return request_id

    #验证邮箱的是否有效
    def validate(self,receiveremail):
        if len(receiveremail) > 7:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", receiveremail) != None:
                return "邮箱格式正确"
            else:
                return "邮箱格式错误！！"
        else:
            return "邮箱格式错误！！"

    #存储邮箱操作的信息函数
    def add_emailinfo(self,request_id, email, status_code):
        emailinfo = [
            email_info(request_id=request_id,
                       email=email,
                       status_code=status_code,
                       ),
        ]
        session.add_all(emailinfo)
        session.commit()

    #发送验证邮箱同时返回验证码
    def SendvalidateEmail(self,receiveremail):
        #发送邮件的验证信息
        validateCode = self.random_captcha()
        msg = "您的验证码为："  + validateCode
        self.SendEmail(receiveremail,msg)
        #返回方便后续验证验证码是否有效
        return validateCode

    #发邮箱
    def SendEmail(self,receiveremail, msg):
        #邮箱的发送内容
        message = MIMEText(msg)
        #邮箱的格式
        message['Content-Type'] = 'Text/HTML'
        try:
            #发送人
            message['From'] = formataddr([self.__senderName,self.__mail_user])
            #收件人
            message['To'] = formataddr(["元丁科技服务用户",receiveremail])
            #发送邮箱标题
            message['Subject'] = Header(self.subject, 'utf-8').encode()
        except Exception as e:
            print(e)
            return "邮箱函数有问题！！！"
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, self.mail_port)
            smtpObj.login(self.__mail_user, self.__mail_password)
            smtpObj.sendmail(self.__mail_user, receiveremail, message.as_string())
            smtpObj.quit()
            return True
        except Exception as e:
            print(e)
            return "邮箱发送失败！！！！"

    #查询公司薪水的信息
    def querycompanySalary(self,sql):
        responseSalaryInfo = []
        # 当公司薪水的信息存在时
        try:
            self.cursor.execute(sql)
            # 获取公司全部薪水的信息
            companySalaryInfo = self.cursor.fetchall()
            responseSalaryInfo.append(companySalaryInfo)
        except:
            companySalaryInfo = None
            responseSalaryInfo.append(companySalaryInfo)

        #返回查询的信息
        return responseSalaryInfo

    #查询公司地址的信息
    def querycompanylocation(self,sql):
        responselocationInfo = []
        # 当公司的信息存在时
        try:
            self.cursor.execute(sql)
            # 获取公司全部薪水的信息
            locationInfo= self.cursor.fetchall()
            responselocationInfo.append(locationInfo)
        except:
            locationInfo = None
            responselocationInfo.append(locationInfo)

        # 返回查询的信息
        return responselocationInfo

    #根据用户提供的域名查询公司的全部相关信息
    def querycompanyInfo(self,email):
        responseInfo = {}
        SQL_companyinfo = "select * from companyinfo where Website = '%s' " % (email)

        #当companyinfo_id存在返回公司的信息
        try:
            #执行sql
            self.cursor.execute(SQL_companyinfo)
            #获取公司的id
            companyinfo_id = self.cursor.fetchone()[0]
            #获取公司的基本信息
            self.cursor.execute(SQL_companyinfo)

            companyinfo_brief = self.cursor.fetchall()
            responseInfo["companyinfo_brief"] = companyinfo_brief

            #获取companySalary 的基本信息
            SQL_companySalary = "select * from companySalary2 WHERE  companyinfo_id= %s" % (companyinfo_id)
            responseSalaryInfo = self.querycompanySalary(SQL_companySalary)
            responseInfo["companySalaryInfo"] = responseSalaryInfo

            # 获取companylocation 的基本信息
            SQL_companylocation = "select * from companylocation2 WHERE  companyinfo_id= %s" % (companyinfo_id)
            responselocationInfo = self.querycompanylocation(SQL_companylocation)
            responseInfo["companylocationInfo"] = responselocationInfo

            #返回查询到的公司信息，暂时不做任何处理，后续判断方便
            return responseInfo
        except:
            return None

#实例化flask
app = Flask(__name__)

global_var = [0]#定义一个全局变量，存validateCode相应的值

global_emailvar = [0]#定义一个全局变量，存emaile相应的值

#下面的4个方法是辅助设置全局变量的方法，也可以使用session来处理这个问题，在这里我没有使用，下面是新学习到用法
def set_var(var):#设置全局变量
    global_var[0] = var
    return "validateCode  set success"

def get_var():#获取全局变量
    return global_var[0]

def set_emailvar(var):#设置全局变量
    global_emailvar[0] = var
    return "email  set success"

def get_emailvar():#获取全局变量
    return global_emailvar[0]

#获取邮箱地址，发送验证邮箱
@app.route("/getemaildata",methods=['POST'])
def getemaildata():
    try:
        try:
            # 获取json 数据
            receiver_email = request.get_json("receiver_email")["receiver_email"]
        except :
            # 403  parameter error,服务器拒绝请求
            return jsonify(returnMag="parameter error", status=403)

        try:
            emailsystem = EmailSystem()
            validateinfo = emailsystem.validate(receiver_email)
            if validateinfo == "邮箱格式正确":
                # 调用发送验证邮箱同时返回验证码函数方法
                validateCode = emailsystem.SendvalidateEmail(receiver_email)

                # 设置全局变量
                set_var(validateCode)
                set_emailvar(receiver_email)

                return jsonify(returnMag="SendvalidateEmail Success,请查收邮箱并且到/validatedata    路由下验证", status=200)
            else:
                # 400 服务器不理解请求的语法（邮箱格式错误）
                return jsonify(returnMag=validateinfo, status=400)
        except:

            return jsonify(returnMag="parameter error", status=400)
    except Exception as error:
        #500  服务器遇到错误无法完成请求
        return jsonify(returnMag="fail", status=500, returnInfo=("%s :error" % error.args))


#验证邮箱并且发送公司邮件功能
@app.route("/validatedata",methods=['post'])
def validateData():
    try:
        try:
            validatedata = request.get_json("validatedata")["validatedata"]
        except:
            return jsonify(returnMag="parameter error", status=403)
        emailSystem = EmailSystem()
        request_id = emailSystem.set_request_id()

        validateCode = get_var()
        # 邮箱验证成功执行
        if validatedata == validateCode:
            receiver_email = get_emailvar()
            responseInfo = emailSystem.querycompanyInfo(receiver_email)
            print(responseInfo)

            # 判断有公司的信息就发送邮件否则就不发送邮件,dict 不能直接发送，需要对查询出来的数据进行处理
            if responseInfo == None:
                # 204 找不到请求的数据
                status_code = 204
                returnMag = "validatedata Success 但是没有公司的相关信息"
                emailSystem.add_emailinfo(request_id, receiver_email, status_code)
                return jsonify(returnMag=returnMag, status=200)
            else:
                status_code = 200
                try:
                    # 对信息进行一下处理
                    response_Info = "查询到的如下信息：" + "\n" + \
                                    "companyinfo_brief:" + str(responseInfo["companyinfo_brief"]) + "\n" + \
                                    "companySalaryInfo:" + str(responseInfo["companySalaryInfo"]) + "\n" + \
                                    "companylocationInfo" + str(responseInfo["companylocationInfo"]) + "\n" + \
                                    "表格对应的关系是：" + "\n" + \
                                    "companyinfo_brief(companyinfo_id,companyinfo_overview_url,companyName, Website, Headquarters, size, Founded,Type, Industry, Revenue, Competitors, rate)" + "\n" + \
                                    "companySalary(companySalary_id,companySalary_overview_url, salaries,companyinfo_id)" + "\n" + \
                                    "companylocation(companylocation_id, companyIocation_sum, companylocation_overview_url,companyinfo_id)"

                    # 发送邮件
                    emailSystem.SendEmail(receiver_email, response_Info)
                    returnMag = "validatedata Success 公司的相关信息已经发送到%s邮箱请查收" % (receiver_email)

                    # 把此次的操作数据和请求状态保存到数据库中
                    emailSystem.add_emailinfo(request_id, receiver_email, status_code)
                    return jsonify(returnMag=returnMag, status=200)
                except:
                    return jsonify(returnMag="validatedata Success  邮箱发送失败！！！！", status=200)
        else:
            return jsonify(returnMag="validatedata Fail", status=403)
    except Exception as error:
        #500  服务器遇到错误无法完成请求
        return jsonify(returnMag="fail", status=500, returnInfo=("%s :error" % error.args))


if __name__ == "__main__":
    app.run(host='0.0.0.0')

