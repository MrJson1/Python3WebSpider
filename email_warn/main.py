# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import  json
from flask import Flask,jsonify
from flask import request

# type=plain 文本格式 默认
# type=html  网页格式
# 暂时不支持image和file格式
# 邮箱支持发送警告给多人
class WarnEmail:
    __mail_user = '' # 登陆邮箱
    __mail_password = '' # 邮箱授权码
    __senderName= '' # 发件人

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


    def SendWarnEmail(self,receiver,  msg, type='plain'):
        if receiver == '':
            return "receiver NO"

        #发送邮箱的配置
        conf = self.load_json("./config")
        mail_host = conf['mail_host']
        mail_port = conf['mail_port']
        sender = self.__mail_user

        type = type.lower()
        if type.__eq__('plain') or type.__eq__('html'):
            message = MIMEText(msg, type, 'utf-8')
        elif type.__eq__('file') or type.__eq__('image'):
            return "暂时不支持file或者image的格式"
        else:
            return False

        try:
            message['From'] = Header(self.__senderName, 'utf-8')
            message['To'] = Header(str(receiver), 'utf-8')
            subject = conf['subject']
            message['Subject'] = Header(subject, 'utf-8')

        except Exception as e:
            print(e)
            return False
        try:
            smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
            smtpObj.login(self.__mail_user, self.__mail_password)
            smtpObj.sendmail(sender, receiver, message.as_string())
            smtpObj.quit()
            return True
        except Exception as e:
            print(e)
            return False

app = Flask(__name__)
@app.route("/getemaildata",methods=['POST'])
def getemaildata():
    try:
        receiver_email = request.get_json("receiver_email")["receiver_email"]
        msg = request.get_json("msg")["msg"]
    except Exception as error:
        return jsonify(returnMag="fail", status=500, returnInfo=("%s :error" % error.args))
    try:
        qq = WarnEmail()
        qq.SendWarnEmail(receiver_email, msg)
        return jsonify(returnMag="success", status=200)
    except:
        return jsonify(returnMag="parameter error", status=400)

if __name__ == "__main__":
    app.run()

