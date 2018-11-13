# coding:utf-8
import time
import traceback
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import csv
from boto3.dynamodb.conditions import Key, Attr
import boto3

class Linkedin:
    def __init__(self):
        self.driver = webdriver.Chrome()
    def login(self, username, password):
        url = 'https://www.linkedin.com/uas/login?session_redirect=&goback=&trk=hb_signin'
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_name('session_key').send_keys(username)
        self.driver.find_element_by_name('session_password').send_keys(password)
        self.driver.find_element_by_name('signin').click()
        self.driver.implicitly_wait(2)

        # #如果跳出有验证手机的按钮执行下行语句跳过手机验证
        # if self.driver.find_element_by_xpath('//*[@id="ember722"]/div[2]/button').click():
        #     self.driver.find_element_by_xpath('//*[@id="ember722"]/div[2]/button').click()

        WebDriverWait(self.driver, 20, 0.5).until(lambda driver: self.driver.find_element_by_css_selector(
            'div#nav-settings__dropdown').is_displayed())

    def get_profile(self):
        self.driver.find_element_by_css_selector('div#nav-settings__dropdown').click()
        time.sleep(3)
        self.driver.find_element_by_css_selector('div#nav-settings__dropdown h3').click()
        time.sleep(3)
        self.driver.execute_script("""(function() {var y = document.body.scrollTop;var step = 100;window.scroll(0, y);function f() {if (y < document.body.scrollHeight) {y += step;window.scroll(0, y);setTimeout(f, 50);} else {window.scroll(0, y);document.title += "scroll-done";}}setTimeout(f, 1000);})();""")
        time.sleep(4)
        html = self.driver.page_source
        soup = BeautifulSoup(html, "lxml")
        ret = {}
        lists_work = []
        list_basalinfo = []
        try:
            try:
                dict = {}
                dict["name"] = soup.select('div.pv-top-card-v2-section__info h1')[0].get_text().strip()
                dict["location"] = soup.select('div.pv-top-card-v2-section__info h3')[0].get_text().strip()
                dict["contest"] = soup.select('header h2 strong')[0].get_text().strip()
                dict["university"] = soup.select('div.pv-top-card-v2-section__links a span')[1].get_text().strip()
                dict["company"] = soup.select('div.pv-top-card-v2-section__links a span')[0].get_text().strip()
                dict["position"] = soup.select('div.pv-top-card-v2-section__info h2')[0].get_text().strip()
                list_basalinfo.append(dict)
            except:
                print(traceback.print_exc())

            ret["basalinfo"] = list_basalinfo

            #当简介人工作信息存在的时候爬取
            if  soup.select("section#experience-section ul li div.pv-entity__summary-info "):

                for item in soup.select("section#experience-section ul li div.pv-entity__summary-info "):

                    dicts = {}
                    try:
                        dicts["position"] = item.select("h3")[0].get_text().strip()
                        for div in item.select("h4"):
                            dicts[div.select("span")[0].get_text().strip()] = div.select("span")[-1].get_text().strip()
                    except:
                        print(traceback.print_exc())
                    lists_work.append(dicts)
            #当简介人的工作信息不存在的时候返回null
            else:
                lists_work.append('null')
        except:
            print(traceback.print_exc())
        ret["work"] = lists_work

        lists_edu = []
        # 当简介人教育信息存在的时候爬取
        if soup.select('section.education-section ul li div.pv-entity__summary-info'):

            for item in soup.select('section.education-section ul li div.pv-entity__summary-info'):
                try:
                    dicts = {}
                    dicts["university"] = item.select("h3")[0].get_text().strip()
                    for div in item.select("p"):
                        dicts[div.select("span")[0].get_text().strip()] = div.select("span")[-1].get_text().strip()
                    lists_edu.append(dicts)
                except:
                    print(traceback.print_exc())
        else:
            # 当简介人的教育信息不存在的时候返回null
            lists_edu.append('null')

        ret["education"] = lists_edu
        return ret

    def get_friends(self):
        url = "http://www.linkedin.com/mynetwork/invite-connect/connections/"
        self.driver.get(url)

        # #有朋友才可以跳转到这个界面，要不会报错
        # WebDriverWait(self.driver, 20, 0.5).until(lambda driver: self.driver.find_element_by_css_selector(
        #     'div.mn-connection-card__details').is_displayed())
        html = self.driver.page_source

        soup = BeautifulSoup(html, "lxml")
        firends_list = []
        # 当简介人朋友信息存在的时候爬取
        if soup.select("div.mn-connection-card__details a"):

            for item in soup.select("div.mn-connection-card__details a"):
                try:
                    ret = {}
                    ret[item.select('span')[0].get_text().strip()] = item.select('span')[1].get_text().strip()
                    ret[item.select('span')[2].get_text().strip()] = item.select('span')[3].get_text().strip()
                    firends_list.append(ret)
                except:
                    pass

            return firends_list
        else:
            # 当简介人的朋友信息不存在的时候返回null
            firends_list.append('null')
            return firends_list


    def run(self):
        ret = {}
        #此登入方式目前只是支持邮箱+密码登入，不支持手机号登入
        self.login("1214861939@qq.com", "15185764374abc")
        ret["profile"] = self.get_profile()
        ret["friends"] = self.get_friends()

        #个人的基本简介
        basalinfo = ret['profile']['basalinfo'][0]
        for key in basalinfo:
            if basalinfo[key] == '':
                basalinfo[key] = 'null'
        #简介人的姓名
        profilename = basalinfo['name']
        #简介人的工作信息
        workinfo = ret['profile']['work'][0]
        for key in workinfo:
            if workinfo[key] == '':
                workinfo[key] = 'null'
        # 简介人的教育信息
        educationinfo = ret['profile']['education'][0]
        for key in educationinfo:
            if educationinfo[key] == '':
                educationinfo[key] = 'null'
        # 简介人的大学
        university = educationinfo['university']
        # 简介人的朋友信息
        friendsinfo = ret['friends']

        # with open("result.json", "w") as file:
        #     file.write((str(ret)))
        # with open("data.csv","w") as file:
        #     file.write(str(ret))
        # datas = str(ret)
        # print(datas)
        self.driver.close()
        return basalinfo,profilename,university,friendsinfo,workinfo,educationinfo

    def SaveDB(self, table,profilename,university,basalinfo,workinfo,educationinfo,friendsinfo):

            table.put_item(
                Item={
                    'ProfileName': profilename,
                    'University': university,
                    'BasalInfo': basalinfo,
                    'WorkInfo': workinfo,
                    'EducationIfo': educationinfo,
                    'Friends': friendsinfo,
                }
            )
            print('************************************************************************')
            print("******信息爬取完成，并且数据保存到Linkedin_DB中，需要数据可以在Linkedin_DB中查找******")

if __name__ == "__main__":
    print('-----------------信息正在爬取中--------------------')
    l = Linkedin()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Linkedin_DB')
    print(time.strftime("%d/%m/%Y"))
    basalinfo, profilename, university, friendsinfo, workinfo, educationinfo = l.run()
    l.SaveDB(table, profilename, university, basalinfo, workinfo, educationinfo, friendsinfo)









