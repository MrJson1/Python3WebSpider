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

class flipkard:
    def __init__(self):
        self.brower = webdriver.Chrome()

    def login(self, username ,password):
        login_url = 'https://www.flipkart.com/'
        self.brower.maximize_window()
        self.brower.get(login_url)
        self.brower.find_element_by_class_name('_2zrpKA').send_keys(username)
        self.brower.find_element_by_css_selector('body > div.mCRfo9 > div > div > div > div > div.Km0IJL.col.col-3-5 > div > form > div:nth-child(2) > input').send_keys(password)
        self.brower.implicitly_wait(1)
        self.brower.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div/form/div[3]/button').click()
        #
        # WebDriverWait(self.brower, 20, 0.5).until(lambda brower: self.brower.find_element_by_css_selector(
        #     'div._2cyQi_').is_displayed())
        scrap_url = 'https://www.flipkart.com/account/?rd=0&link=home_account'
        self.brower.implicitly_wait(2)
        self.brower.get(scrap_url)

        WebDriverWait(self.brower, 20, 0.5).until(lambda driver: self.brower.find_element_by_css_selector(
            'div._1JMKW3').is_displayed())

    def get_OrderdetailInfo(self):
        self.brower.execute_script('window.open()')
        # 打开一个新的选项卡
        self.brower.switch_to_window(self.brower.window_handles[1])
        url = "https://www.flipkart.com/account/orders"
        self.brower.get(url)
        self.brower.execute_script(
            """(function() {var y = document.body.scrollTop;var step = 100;window.scroll(0, y);function f() {if (y < document.body.scrollHeight) {y += step;window.scroll(0, y);setTimeout(f, 50);} else {window.scroll(0, y);document.title += "scroll-done";}}setTimeout(f, 1000);})();""")
        time.sleep(10)
        js = "var q=document.documentElement.scrollTop = 10000"

        self.brower.execute_script(js)
        html = self.brower.page_source
        soup = BeautifulSoup(html, "lxml")
        try:

            while soup.select("div._16c-eX._16DdHx > div > span"):
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
                break

            if soup.select("button._2AkmmA._1zypWO"):
                self.brower.find_element_by_css_selector('button._2AkmmA._1zypWO').click()
                wait = WebDriverWait(self.brower, 5)
                # wait.until(EC.presence_of_element_located((By.CLASS_NAME, '._1zypWO')))
                html = self.brower.page_source
                soup = BeautifulSoup(html, "lxml")
        except TimeoutException:
            print('Time   Out')

        #订单的详细信息，包括ProductInfo，OrderInfo {已经完成的订单，取消的订单}，OrderSum 等信息
        OrderdetailInfo = {}
        ProductInfo = []
        OrderInfo = []
        try:
            items = soup.select('div.F4CVC3')
            ordersum = len(items)
            for item in items:
                dict ={}
                orderdict = {}
                orderdict["orderId"] = item.select('div.DgI5Zd')[0].get_text().strip()
                orderdict["orderPrice"] = item.select('div.col-6-12.Gp5Tnb span')[1].get_text().strip()
                #orderdict_Status

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

                ProductInfo.append(dict)
                OrderInfo.append(orderdict)

            OrderdetailInfo["OrderSum"] = ordersum
        except:
            print(traceback.print_exc())
        OrderdetailInfo["ProductInfo"] = ProductInfo
        OrderdetailInfo["OrderInfo"] = OrderInfo
        return OrderdetailInfo

    def get_SingleOrderAddressInfo(self,orderId):
        self.brower.execute_script('window.open()')
        # 打开一个新的选项卡
        self.brower.switch_to_window(self.brower.window_handles[1])
        url_a = 'https://www.flipkart.com/order_details?order_id='
        url_b = '&src=od&link=order_number'
        url = url_a + orderId + url_b
        self.brower.get(url)
        try:
            wait = WebDriverWait(self.brower, 10)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '._2rhtPx')))
        except TimeoutException:
            print('Time Out')
        address_html = self.brower.page_source
        xpath_html = etree.HTML(address_html)
        address_soup = BeautifulSoup(address_html, "lxml")
        try:
            dict = {}
            # 获取收货人的名字
            dict["DeliveryName"] = address_soup.select('div._28vuId')[0].get_text().strip()
            # 获取Phone
            dict["Phone"] = address_soup.select('span._2KwVbu')[0].get_text().strip()
            # 获取地址
            dict["DeliveryAddress"] = xpath_html.xpath("//div[@class='_1oqxSg']/text()")
            return dict
        except:
            print(traceback.print_exc())

    def get_PersonalInfo(self):
        html = self.brower.page_source
        soup = BeautifulSoup(html, "lxml")
        PersonalInfo = {}
        try:
            PersonalInfo["firstName"] = soup.select("div.Th26Zc   input")[0].attrs['value'].strip()
            PersonalInfo["lastName"] = soup.select("div.Th26Zc   input")[1].attrs['value'].strip()
            #需要做修改
            PersonalInfo["gender"] = soup.select("label._8J-bZE._2FAt1l._1YWe2-._2pmKiA._2tcMoY._1Icwrf span")[0].get_text().strip()

            PersonalInfo["emailAddress"] = soup.select("div.Th26Zc input")[2].attrs['value'].strip()
            PersonalInfo["mobileNumber"] = soup.select("div.Th26Zc input")[3].attrs['value'].strip()
        except:
            print(traceback.print_exc())
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
        soup = BeautifulSoup(html, "lxml")
        xpath_html = etree.parse('html',etree.HTMLParser())
        AddressInfo = {}
        try:
            for item in soup.select('div._2HW10N'):
                dict = {}
                dict["name"] = item.select("p.ZBYhh4  span")[0].get_text().strip()
                dict["phoneNumber"] = item.select("p.ZBYhh4  span")[1].get_text().strip()
                dict["pincode"] = item.select("span._3n0HwW")[0].get_text().strip()
                dict["locality"] = xpath_html.xpath('//*[@id="container"]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/span/text()[1]')
                dict["City/District/Town"] = item.select("h3")[0].get_text().strip()
                dict["state"] = item.select("h3")[0].get_text().strip()
                dict["landmark"] = item.select("h3")[0].get_text().strip()
                dict["alternatePhone"] = item.select("h3")[0].get_text().strip()
                dict["addressType"] = item.select("h3")[0].get_text().strip()
                dict["order"] = item.select("h3")[0].get_text().strip()

                AddressInfo =dict

        except:
            print(traceback.print_exc())
        return AddressInfo

    def get_NotificationInfo(self):
        notification_url = 'https://www.flipkart.com/account/subscriptions'
        self.brower.get(notification_url)
        time.sleep(2)
        html = self.brower.page_source
        soup = BeautifulSoup(html, "lxml")
        notificationInfo = {}
        try:

            notificationInfo['SMS_Notifications'] = soup.select("div._3BMEgv  span")[0].get_text().strip()
            notificationInfo['Email_Notifications'] = soup.select("div._3BMEgv  span")[2].get_text().strip()

        except:
            print(traceback.print_exc())
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
            PANCardInfo['FullName'] = soup.select("div.Th26Zc input")[1].attrs['value'].strip()
            PANCardInfo['PANImage'] = soup.select("div._2ugmFU label")[0].get_text().strip()

        except:
            print(traceback.print_exc())
        return PANCardInfo

    def get_paymentsInfo(self):
        PANCardInfo_url ='https://www.flipkart.com/account/pancard'
        self.brower.get(PANCardInfo_url)
        time.sleep(2)
        html = self.brower.page_source
        soup = BeautifulSoup(html, "lxml")
        paymentsInfo = {}
        try:
            paymentsInfo['PhonePeWallet'] = soup.select("span._3qs2U5")[0].get_text().strip()
            paymentsInfo['GiftCards'] = soup.select("span._3qs2U5")[1].get_text().strip()
        except:
            print(traceback.print_exc())

        return paymentsInfo

    def get_CardsInfo(self):
        url = 'https://www.flipkart.com/account/carddetails'
        self.brower.get(url)
        time.sleep(2)
        html = self.brower.page_source
        soup = BeautifulSoup(html, "lxml")
        CardsInfo = {}
        try:

            nameXpath = soup.select("div._3ny5Jw div span")[0].get_text().strip()
            CardsInfo['CardName'] = nameXpath
            if nameXpath =='Yes Bank Debit Card':
                #待处理
                pass

        except:
            print(traceback.print_exc())

        return CardsInfo

    #待完成
    def get_ReviewInfro(self):

        url = 'https://www.flipkart.com/account/rewards'
        self.brower.get(url)

    def run(self):
        pass

if __name__ == "__main__":
    flipkard = flipkard()
    flipkard.login('9597954836','abc@123')

    # get_OrderdetailInfo = flipkard.get_PersonalInfo()
    # print(get_OrderdetailInfo)
    # AddressInfo = flipkard.get_AddressInfo()
    # print(AddressInfo)
    NotificationInfo = flipkard.get_NotificationInfo()
    print(NotificationInfo)
    # get_CardsInfo = flipkard.get_CardsInfo()
    # print(get_CardsInfo)

