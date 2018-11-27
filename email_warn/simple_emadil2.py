# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def SendEmail(toAdd, htmlText):
    strFrom = "1214861939@qq.com"
    strTo = toAdd
    msg = MIMEText(htmlText)
    msg['Content-Type'] = 'Text/HTML'
    msg['Subject'] = Header("标题", 'utf-8')
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




if __name__ == "__main__":
    htmlText = "内容错误警告"
    SendEmail("1214861939@qq.com",htmlText)


