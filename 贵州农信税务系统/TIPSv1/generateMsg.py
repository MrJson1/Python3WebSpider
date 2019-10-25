# _*_conding:utf-8_*_
import xml.sax.handler
import pprint
import xml.dom.minidom as Dom

#解析请求报文
class XMLHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.buffer = ""
        self.mapping = {}

    def startElement(self, name, attributes):
        self.buffer = ""

    def characters(self, data):
        self.buffer += data

    def endElement(self, name):
        self.mapping[name] = self.buffer.replace(' ','').replace('\n','').replace('\t','')

    def getDict(self):
        return self.mapping

req_data =  """							<responseDTO>
								<zjrq>20180324</zjrq>
								<zjsj>112548</zjsj>
								<zjlsh>OBOW2019011511264754166290880</zjlsh>
								<jgdh></jgdh>
								<jygy>126921</jygy>
								<taxorgcode>25201220000</taxorgcode>
								<taxorgname>息烽县地税局</taxorgname>
								<trano>48624125</trano>
								<trecode>2301100000</trecode>
								<trename>息烽国库</trename>
								<payeebankno>011701000014</payeebankno>
								<payeeacct>2109010001201300500031</payeeacct>
								<payeename>贵阳市息烽县支库</payeename>
								<payopbkcode>402701012108</payopbkcode>
								<payopbkname></payopbkname>
								<handorgname>贵州青蓝紫富硒茶业有限公司</handorgname>
								<jyje>502.25</jyje>
								<taxvouno>352016181200001006</taxvouno>
								<billdate>20181227</billdate>
								<taxpaycode>91520122709600177P</taxpaycode>
								<taxpayname>贵州息烽温泉矿产资源开发有限公司</taxpayname>
								<corpcode></corpcode>
								<budgettype>1</budgettype>
								<trimsign>0</trimsign>
								<printvousign>1</printvousign>
								<detailnum>2</detailnum>
								</responseDTO>
		    """

xh = XMLHandler()
xml.sax.parseString(req_data, xh)
dict = xh.getDict()
# print("请求报文：")
pprint.pprint(dict)

temp = """        # response>xfaceTradeDTO>responseDTO>total_num
        total_num_node = doc.createElement("total_num")
        total_num_value = doc.createTextNode("1")
        if not serviceCodeFlag:
            total_num_value = doc.createTextNode("")
        total_num_node.appendChild(total_num_value)
        xresponseDTO_node.appendChild(total_num_node)"""

# temp2 = """            # response>xfaceTradeDTO>responseDTO>insuranceInfo>social_sec_branch
#             social_sec_branch_node = doc.createElement("social_sec_branch")
#             social_sec_branch_value = doc.createTextNode("5200000201522731")
#             social_sec_branch_node.appendChild(social_sec_branch_value)
#             insuranceInfo_node.appendChild(social_sec_branch_node)"""

temp2 = """            # response>xfaceTradeDTO>responseDTO>list>social_sec_branch
            social_sec_branch_node = doc.createElement("social_sec_branch")
            social_sec_branch_value = doc.createTextNode("5200000201522731")
            social_sec_branch_node.appendChild(social_sec_branch_value)
            insuranceInfo_node.appendChild(social_sec_branch_node)"""

for key in dict.keys():
    temp_key = dict[key]
    print(temp.replace("total_num",key).replace("1",temp_key))
    print()
#
# for key in dict.keys():
#     temp_key = dict[key]
#     print(temp2.replace("social_sec_branch",key).replace("5200000201522731",temp_key))
#     print()
# reqMsg = "1231111789"
# lenReq = reqMsg[0:8]
# print(lenReq)
# print(reqMsg.lstrip(lenReq))
# print(reqMsg)
# data = """<?xml version="1.0" encoding="UTF-8"?>
# <transaction><body><request><xfaceTradeDTO><oBOW712301DTO><middHead><wdmc>贵州乌当农村商业银行股份有限公司百宜支行</wdmc><yybs>003</yybs><mac></mac></middHead><middBody><nsrsbh>520123G73270120</nsrsbh><gdslxbz>2</gdslxbz><ywbh>003004211000</ywbh></middBody></oBOW712301DTO></xfaceTradeDTO><vocationalHeader><postingDateText>0</postingDateText><origExternalTask>712301</origExternalTask><authCode></authCode><trackNumber>ITLR20191012030007749225</trackNumber><serviceCode>712301</serviceCode><authorizer></authorizer><revwCode></revwCode><checker></checker><tfOrigChannel>ITLR</tfOrigChannel><userId>123165</userId><xipDate>20191012</xipDate><tfChannel>ITLR</tfChannel><tranName>社保费(单位)欠费信息查询</tranName><externalTask>712301</externalTask><menuCode></menuCode><userReferenceNumber>ITLR20191012030007749225</userReferenceNumber><externalBranchCode>2030012</externalBranchCode></vocationalHeader></request></body><header><security><loginUser>ITLR</loginUser><requestIp>11.18.14.95</requestIp></security><signature></signature><message><sndDt>20191012</sndDt><msgType>OBOW.07123010.01</msgType><reqAppCd>ITLR</reqAppCd><reserve></reserve><msgId>ITLR20191012030007749225</msgId><appCd>OBOW</appCd><sndTm>135908765</sndTm><callTyp>SYN</callTyp></message><version>1.0</version></header></transaction>"""
# # print("returnData:"+returnData)
# length = len(data.encode('utf-8'))
# slen = '%08d' % length
# data = slen + data
# print(data)
# print(slen)







