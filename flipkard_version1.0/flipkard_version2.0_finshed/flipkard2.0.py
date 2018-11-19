import time
import traceback
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import  expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import  re
from lxml import  etree
from queue import Queue
import boto3

class flipkard:
    def __init__(self):
        self.brower = webdriver.Chrome()

    def login(self, username ,password):
        login_url = 'https://www.flipkart.com/'
        self.brower.get(login_url)
        self.brower.implicitly_wait(2)
        self.brower.find_element_by_class_name('_2zrpKA').send_keys(username)
        self.brower.find_element_by_css_selector(
            'body > div.mCRfo9 > div > div > div > div > div.Km0IJL.col.col-3-5 > div > form > div:nth-child(2) > input').send_keys(
            password)
        self.brower.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div/form/div[3]/button').click()
        time.sleep(2)
        self.brower.execute_script('window.open()')
        # 打开一个新的选项卡
        self.brower.switch_to_window(self.brower.window_handles[1])
        scrap_url = 'https://www.flipkart.com/account/?rd=0&link=home_account'
        self.brower.get(scrap_url)
        try:
            WebDriverWait(self.brower, 20, 0.5).until(lambda driver: self.brower.find_element_by_css_selector(
            'div._1JMKW3').is_displayed())
        except:
            print("请确认您的用户名或者密码是否正确！！！")

        return  username

    #判断用户是否登录成功
    def Islogined(self):
        scrap_url = 'https://www.flipkart.com/account/?rd=0&link=home_account'
        self.brower.get(scrap_url)
        #把Personal Information 的标签作为登录标记
        if self.brower.find_element_by_css_selector("span._10it6k"):
            pass
        else:
            self.login()

    def get_OrderdetailInfo(self):
        self.brower.execute_script('window.open()')
        # 打开一个新的选项卡
        self.brower.switch_to_window(self.brower.window_handles[2])
        url = "https://www.flipkart.com/account/orders"
        self.brower.get(url)
        self.execute_script()
        time.sleep(10)

        #滚动条拉到最下面
        js = "var q=document.documentElement.scrollTop = 10000"
        self.brower.execute_script(js)
        html = self.brower.page_source
        soup = BeautifulSoup(html, "lxml")

        #等待数据全部加载出来
        try:
            #当Back to top 存在的时候
            while soup.select("div._16c-eX._16DdHx > div > span"):
                if len(soup.select('div.F4CVC3')) > 4:
                    self.brower.find_element_by_css_selector("div._16c-eX._16DdHx > div > span").click()


                time.sleep(3)

                self.brower.execute_script(
                    """(function() {var y = document.body.scrollTop;var step = 100;window.scroll(0, y);function f() {if (y < document.body.scrollHeight) {y += step;window.scroll(0, y);setTimeout(f, 50);} else {window.scroll(0, y);document.title += "scroll-done";}}setTimeout(f, 1000);})();""")
                time.sleep(15)
                html = self.brower.page_source
                soup = BeautifulSoup(html, "lxml")
                # wait = WebDriverWait(brower, 200)
                # button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '._2AkmmA._1zypWO')))
                # if brower.find_element_by_css_selector("button._2AkmmA._1zypWO"):
                #     brower.find_element_by_css_selector("button._2AkmmA._1zypWO").click()
                #     wait = WebDriverWait(brower, 5)
                #     if wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_1zypWO'))):
                #         html = brower.page_source
                #         soup = BeautifulSoup(html, "lxml")
                if soup.select("button._2AkmmA._1zypWO"):
                    wait = WebDriverWait(self.brower, 10)
                    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '._2AkmmA._1zypWO')))

                    # if soup.select("button")[1].get_text().strip() == 'Show more orders':
                    if soup.select("button._2AkmmA._1zypWO"):
                        self.brower.find_element_by_css_selector("button._2AkmmA._1zypWO").click()

                        self.brower.execute_script(
                            """(function() {var y = document.body.scrollTop;var step = 100;window.scroll(0, y);function f() {if (y < document.body.scrollHeight) {y += step;window.scroll(0, y);setTimeout(f, 50);} else {window.scroll(0, y);document.title += "scroll-done";}}setTimeout(f, 1000);})();""")
                        time.sleep(10)

                    else:
                        wait = WebDriverWait(self.brower, 5)
                        wait.until(EC.presence_of_element_located((By.CLASS_NAME, '._1zypWO')))
                        html = self.brower.page_source
                        soup = BeautifulSoup(html, "lxml")
                #
                #
                #     if soup.select("div._1zypWO span"):
                #         if soup.select("div._1zypWO span")[0].get_text().strip() == 'No more results to display':
                #             html = brower.page_source
                #             soup = BeautifulSoup(html, "lxml")
                #             break
                js = "var q=document.documentElement.scrollTop = 10000"
                self.brower.execute_script(js)
                break

            if soup.select("button._2AkmmA._1zypWO"):
                self.brower.find_element_by_css_selector('button._2AkmmA._1zypWO').click()
                wait = WebDriverWait(self.brower, 5)
                # wait.until(EC.presence_of_element_located((By.CLASS_NAME, '._1zypWO')))

        except TimeoutException:
            print('Time   Out')

        js = "var q=document.documentElement.scrollTop = 10000"
        self.brower.execute_script(js)
        time.sleep(10)
        html = self.brower.page_source
        soup = BeautifulSoup(html, "lxml")
        #最后判断是否数据全部加载成功
        while soup.select("button._2AkmmA._1zypWO"):
            self.brower.find_element_by_css_selector('button._2AkmmA._1zypWO').click()
            #刷新html，保证拿到的是最新html
            html = self.brower.page_source
            soup = BeautifulSoup(html, "lxml")
        html = self.brower.page_source
        soup = BeautifulSoup(html, "lxml")
        #订单的详细信息，包括ProductInfo，OrderInfo {已经完成的订单，取消的订单}，OrderSum 等信息
        OrderdetailInfo = {}
        ProductInfo = []
        OrderInfo = []

        # 队列收集订单的id
        queue = Queue()
        #用户名用于构建表格使用
        accountname = soup.select("div._2cyQi_")[0].get_text().strip()
        try:
            items = soup.select('div.F4CVC3')
            ordersum = len(items)
            for item in items:
                dict ={}
                orderdict = {}
                try:
                    orderdict["orderId"] = item.select('div.DgI5Zd')[0].get_text().strip()
                except:
                    orderdict["orderId"] = None
                #收集订单的id后面好收集订单的地址
                queue.put(orderdict["orderId"])

                orderdict["orderPrice"] = item.select('div.col-6-12.Gp5Tnb span')[1].get_text().strip()

                #当一个订单存在2个以上产品的时候
                if len(item.select("div._3xiuDJ")) != 1:

                    product_Offers = len(item.select("div._3xiuDJ"))
                    dict["productOffers"]  = product_Offers
                    for item2 in item.select("div._3xiuDJ"):
                        dict["productId"] = orderdict["orderId"]
                        dict["productName"] = item2.select('a._2AkmmA.row.NPoy5u')[0].get_text().strip()
                        dict["productPrice"] = item2.select('div.col-1-12._52MoHd')[0].get_text().strip()
                        dict["productDate"] = item2.select('div.col-3-12._3fG4KG')[0].get_text().strip()  # 产品发货日期
                        product_Status = item2.select('div._3HDMnP')[0].get_text().strip()  # 产品物流状态
                        if product_Status == 'Your item has been delivered':
                            pattern = re.compile('delivered')
                            pattern_res = re.findall(pattern, product_Status)
                            dict["product_Status"] = pattern_res

                        else:
                            dict["product_Status"] = "Cancelled or Returned"
                    #只需要其中的一个状态就可以了，一个订单只有一个状态
                    orderdict["order_Status"] = dict["product_Status"]
                else:

                    #(订单id, 产品名称, 产品价格, 产品发货日期, 产品物流状态, 产品总供给数量)
                    dict["productId"] = orderdict["orderId"]
                    dict["productName"] = item.select('a._2AkmmA.row.NPoy5u')[0].get_text().strip()
                    dict["productPrice"] = item.select('div.col-1-12._52MoHd')[0].get_text().strip()
                    dict["productDate"] = item.select('div.col-3-12._3fG4KG')[0].get_text().strip()  # 产品发货日期
                    dict["productOffers"] = '1'
                    product_Status = item.select('div._3HDMnP')[0].get_text().strip()  # 产品物流状态

                    if product_Status == 'Your item has been delivered':
                        pattern = re.compile('delivered')
                        pattern_res = re.findall(pattern, product_Status)
                        dict["product_Status"] = pattern_res
                        orderdict["order_Status"] = pattern_res

                    else:
                        # 3.If Cancelled, then Refund Description, Refund Status (Completed in this case), Refund to, Refund ID
                        # (如果取消订单,采集退款描述、退款状态、退款订单编号、退款帐号）
                        # 待完善
                        # if product_Status == 'Your item has been cancelled' or product_Status =='Shipment cancelled by you':
                        dict["product_Status"] = "Cancelled or Returned"
                        orderdict["order_Status"] = "Cancelled or Returned"
                # 把空字符串过滤掉方便存储dynamoDB数据库
                for key in dict:
                    if dict[key] == '':
                        dict[key] = None
                ProductInfo.append(dict)

                for key in orderdict:
                    if orderdict[key] == '':
                        orderdict[key] = None
                OrderInfo.append(orderdict)

            OrderdetailInfo["OrderSum"] = ordersum
        except:
            print(traceback.print_exc())
        OrderdetailInfo["ProductInfo"] = ProductInfo
        OrderdetailInfo["OrderInfo"] = OrderInfo
        return OrderdetailInfo,queue,accountname

    #根据抓取出来的订单ID找到订单地址
    def get_SingleOrderAddressInfo(self,orderId):
        #构造采取订单地址的URL
        url_a = 'https://www.flipkart.com/order_details?order_id='
        url_b = '&src=od&link=order_number'
        url = url_a + orderId + url_b

        self.brower.get(url)
        try:
            wait = WebDriverWait(self.brower, 10)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '._2rhtPx')))
        except TimeoutException:
            print('采集订单地址%sTime Out'%orderId)
        address_html = self.brower.page_source
        xpath_html = etree.HTML(address_html)
        address_soup = BeautifulSoup(address_html, "lxml")
        try:
            dict = {}
            # 获取收货人的名字
            try:
                dict["DeliveryName"] = address_soup.select('div._28vuId')[0].get_text().strip()
            except:
                dict["DeliveryName"] =None

            # 获取Phone
            try:
                dict["Phone"] = address_soup.select('span._2KwVbu')[0].get_text().strip()
            except:
                dict["Phone"] =None
            # 获取地址
            try:
                dict["DeliveryAddress"] = xpath_html.xpath("//div[@class='_1oqxSg']/text()")
            except:
                dict["DeliveryAddress"] = None
            return dict
        except:
            print("%s订单地址信息有缺失"%orderId)

    def get_PersonalInfo(self):
        html = self.brower.page_source
        soup = BeautifulSoup(html, "lxml")
        PersonalInfo = {}
        try:
            try:
                PersonalInfo["firstName"] = soup.select("div.Th26Zc   input")[0].attrs['value'].strip()
            except:
                PersonalInfo["firstName"] =None
            try:
                PersonalInfo["lastName"] = soup.select("div.Th26Zc   input")[1].attrs['value'].strip()
            except:
                PersonalInfo["lastName"] =None
            try:

                for item in soup.select("div._2o59RR"):
                    pattern = re.compile('checked')
                    if re.findall(pattern, str(item)):
                        PersonalInfo["gender"] = item.get_text().strip()
            except:
                PersonalInfo["gender"] =None
            try:
                PersonalInfo["emailAddress"] = soup.select("div.Th26Zc input")[2].attrs['value'].strip()
            except:
                PersonalInfo["emailAddress"] =None
            try:
                PersonalInfo["mobileNumber"] = soup.select("div.Th26Zc input")[3].attrs['value'].strip()
            except:
                PersonalInfo["mobileNumber"] =None
        except:
            print(traceback.print_exc())
            print("获取个人信息数据有缺失")

        # 把空字符串过滤掉方便存储dynamoDB数据库
        for key in PersonalInfo:
            if PersonalInfo[key] == '':
                PersonalInfo[key] = None
        return PersonalInfo

    def execute_script(self):
        self.brower.execute_script(""" 
               (function () { 
                   var y = document.body.scrollTop; 
                   var step = 100; 
                   window.scroll(0, y); 
                   function f() { 
                       if (y < document.body.scrollHeight) { 
                           y += step; 
                           window.scroll(0, y); 
                           setTimeout(f, 50); 
                       }
                       else { 
                           window.scroll(0, y); 
                           document.title += "scroll-done"; 
                       } 
                   } 
                   setTimeout(f, 1000); 
               })(); 
               """)
        time.sleep(1)

    def get_AddressInfo(self):
        address_url = 'https://www.flipkart.com/account/addresses'
        self.brower.get(address_url)
        self.execute_script()
        html = self.brower.page_source
        xpath_html = etree.HTML(html)
        ManageAddressInfo = {}
        try:
            for item in xpath_html.xpath('//div[@class="_2HW10N"]'):
                dict = {}
                try:
                    dict["name"] = item.xpath('//p[@class="ZBYhh4"]//span[@class="_2Fw4MM"]/text()')
                except:
                    dict["name"] =None
                try:
                    dict["phoneNumber"] = item.xpath('//p[@class="ZBYhh4"]//span[@class="_3MbGVP _2Fw4MM"]/text()')
                except:
                    dict["phoneNumber"] =  None
                try:
                    dict["pincode"] = item.xpath("//span[@class='_3n0HwW']/text()")
                except:
                    dict["pincode"] =None
                try:
                    dict["addressDetail"] = item.xpath('//div[@class="_2HW10N"]//span[@class="ZBYhh4 _1Zn3iq"]/text()')
                except:
                    dict["addressDetail"] =None

                ManageAddressInfo["addressInfo"] =dict
        except:
            print(traceback.print_exc())
        # 把空字符串过滤掉方便存储dynamoDB数据库
        for key in ManageAddressInfo:
            if ManageAddressInfo[key] == '':
                ManageAddressInfo[key] = None
        return ManageAddressInfo

    def get_NotificationInfo(self):
        notification_url = 'https://www.flipkart.com/account/subscriptions'
        self.brower.get(notification_url)
        time.sleep(2)
        html = self.brower.page_source
        soup = BeautifulSoup(html, "lxml")
        notificationInfo = {}
        try:
            if soup.select("div._3BMEgv  span")[0]:
                notificationInfo['SMS_Notifications'] = soup.select("div._3BMEgv  span")[0].get_text().strip()

        except:
            notificationInfo['SMS_Notifications'] = None
        try:
            if soup.select("div._3BMEgv  span")[2]:
                notificationInfo['Email_Notifications'] = soup.select("div._3BMEgv  span")[2].get_text().strip()

        except:
            notificationInfo['Email_Notifications'] = None

        # 把空字符串过滤掉方便存储dynamoDB数据库
        for key in notificationInfo:
            if notificationInfo[key] == '':
                notificationInfo[key] = None
        return notificationInfo

    def get_PANCardInfo(self):
        PANCardInfo_url ='https://www.flipkart.com/account/pancard'
        self.brower.get(PANCardInfo_url)
        time.sleep(2)
        html = self.brower.page_source
        soup = BeautifulSoup(html, "lxml")
        PANCardInfo = {}
        try:
            PANCardInfo['PanCardNumber'] = soup.select("div.Th26Zc input")[0].attrs['value'].strip()
        except:
            PANCardInfo['PanCardNumber'] = None
        try:
            PANCardInfo['FullName'] = soup.select("div.Th26Zc input")[1].attrs['value'].strip()
        except:
            PANCardInfo['FullName'] = None
        try:
            PANCardInfo['PANImage'] = soup.select("div._2ugmFU label")[0].get_text().strip()
        except:
            PANCardInfo['PANImage'] = None

        # 把空字符串过滤掉方便存储dynamoDB数据库
        for key in PANCardInfo:
            if PANCardInfo[key] == '':
                PANCardInfo[key] = None
        return PANCardInfo

    def get_paymentsWalletInfo(self):
        PANCardInfo_url ='https://www.flipkart.com/account/pancard'
        self.brower.get(PANCardInfo_url)
        time.sleep(2)
        html = self.brower.page_source
        soup = BeautifulSoup(html, "lxml")
        paymentsWalletInfo = {}
        try:
            paymentsWalletInfo['PhonePeWallet'] = soup.select("span._3qs2U5")[0].get_text().strip()
        except:
            paymentsWalletInfo['PhonePeWallet'] = None
        try:
            paymentsWalletInfo['GiftCards'] = soup.select("span._3qs2U5")[1].get_text().strip()
        except:
            paymentsWalletInfo['GiftCards'] = None

        # 把空字符串过滤掉方便存储dynamoDB数据库
        for key in paymentsWalletInfo:
            if paymentsWalletInfo[key] == '':
                paymentsWalletInfo[key] = None

        return paymentsWalletInfo

    def get_SaveCardsInfo(self):
        url = 'https://www.flipkart.com/account/carddetails'
        self.brower.get(url)
        time.sleep(3)
        self.execute_script()
        html = self.brower.page_source
        soup = BeautifulSoup(html, "lxml")
        SaveCardsInfo = {}

        try:
            # nameXpath = soup.select("div._3ny5Jw div span")[0].get_text().strip()
            SaveCardsInfo['CardName'] = soup.select("div._3ny5Jw div span")[0].get_text().strip()
            # if nameXpath =='Yes Bank Debit Card':
            #     #待处理
            #     pass
        except:
            SaveCardsInfo['CardName'] = None


        # 把空字符串过滤掉方便存储dynamoDB数据库
        for key in SaveCardsInfo:
            if SaveCardsInfo[key] == '':
                SaveCardsInfo[key] = None
        return SaveCardsInfo

    def get_ReviewInfo(self):
        url = 'https://www.flipkart.com/account/reviews'
        self.brower.get(url)
        time.sleep(4)
        self.execute_script()
        html = self.brower.page_source
        soup = BeautifulSoup(html, "lxml")
        dict = {}
        try:
            #当评价存在的时候
            if soup.select("div._1zdYIq span")[0].get_text().strip() =="My Reviews":
                dict_item = {}
                for  item  in  soup.select("div._1I6kUh"):
                    try:
                        dict_item["Reviewproductname"] = item.select('div._2jQViS')[0].get_text().strip()
                    except:
                        dict_item["Reviewproductname"] =None
                    try:
                        dict_item["Reviewrating"] = item.select('p._3yYOd2')[0].get_text().strip()
                    except:
                        dict_item["Reviewrating"] = None
                    try:
                        dict_item["Reviewdescription"] = item.select('div._1JIVPz div')[0].get_text().strip()
                    except:
                        dict_item["Reviewdescription"] =None
                    try:
                        dict_item["ReviewDate"] = item.select('p.dNmCY8')[1].get_text().strip()
                    except:
                        dict_item["ReviewDate"] =None

                dict["Totalreviews"] = soup.select('span._3nCce6')[0].get_text().strip()
                # 把空字符串过滤掉方便存储dynamoDB数据库
                for key in dict_item:
                    if dict_item[key] == '':
                        dict_item[key] = None
                dict["ReviewInfo"] = dict_item

            else:
                dict["ReviewInfo"] = "No Reviews & Ratings"
        except:
            pass

        # 把空字符串过滤掉方便存储dynamoDB数据库
        for key in dict:
            if dict[key] == '':
                dict[key] = None
        return dict


    def run(self):
        # 按照网页的数据结构存储数据
        myordersinfo = {}  # my orders
        accountinfo = {}  # ACCOUNT SETTINGS
        paymentsinfo = {}  # PAYMENTS
        mystuffinfo = {}  # MY STUFF

        username = self.login('9597954836','abc@123')


        try:
            # 获取accountinfo 信息
            accountinfo["PersonalInfo"] = self.get_PersonalInfo()
            accountinfo["ManageAddressInfo"] = self.get_AddressInfo()
            accountinfo["notificationInfo"] = self.get_NotificationInfo()
            accountinfo["PANCardInfo"] = self.get_PANCardInfo()
        except:
            print(traceback.print_exc())

        try:
            # 获取paymentsinfo 信息
            paymentsinfo["paymentsWalletInfo"] = self.get_paymentsWalletInfo()
            paymentsinfo["SaveCardsInfo"] = self.get_SaveCardsInfo()
        except:
            print(traceback.print_exc())

        try:
            # 获取mystuffinfo 信息
            mystuffinfo["ReviewInfo"] = self.get_ReviewInfo()
            # mystuffinfo["ReviewInfo"] = None
        except:
            print(traceback.print_exc())

        OrderdetailInfo, queue, accountname = self.get_OrderdetailInfo()
        try:
            #获取myordersinfo 信息
            try:
                while not queue.empty():
                    orderid = queue.get()
                    myordersinfo["OrderAddressInfo"] = self.get_SingleOrderAddressInfo(orderid)
            except:
                myordersinfo["OrderAddressInfo"] = None

            myordersinfo["OrderdetailInfo"] = OrderdetailInfo
        except:
            print(traceback.print_exc())

        finally:
            self.brower.close()
            self.brower.quit()

        return accountname,paymentsinfo,myordersinfo,accountinfo,mystuffinfo,username


    def SaveDB(self, table,accountname,paymentsinfo,myordersinfo,accountinfo,mystuffinfo,username):

            table.put_item(
                Item={
                    'UserId':username,
                    'AccountName':accountname,
                    'PaymentsInfo': paymentsinfo,
                    'MyOrdersInfo': myordersinfo,
                    'AccountInfo': accountinfo,
                    'Mystuffinfo': mystuffinfo,
                }
            )
            print('************************************************************************')
            print("******信息爬取完成，并且数据保存到Flipkar_DB数据库中，需要数据可以在Flipkar_DB数据库查找******")


if __name__ == "__main__":
    print('-----------------信息正在爬取中不要关闭浏览器窗口--------------------')
    flipkard = flipkard()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Flipkar_DB')
    print(time.strftime("%d/%m/%Y"))
    accountname, paymentsinfo, myordersinfo, accountinfo, mystuffinfo,username = flipkard.run()
    print('**************%s信息正在存储中*****************'%accountname)
    flipkard.SaveDB(table,accountname,paymentsinfo,myordersinfo,accountinfo,mystuffinfo,username)

