import csv
import requests
import pprint
from flask import request
from flask import Flask,jsonify
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

# with open("req.csv","r",encoding="utf-8") as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
#         print(row)

tempp = """"yybs" in dict.keys() """
tem = """len(dict['yybs']) != 0 """
# ywbh id_type id_num name insurance_type begin_date end_date  user_id pay_base
string = """wdmc ywbh entrustdate sbxh nsbz jyje xzbz payopbranch handorgname"""
listTO = string.split(" ")

i = 0
while i < len(listTO):
    tips = " and " + "\""+str(listTO[i]) + "\"" + " in dict.keys()"
    sb = " and len(dict['" + str(listTO[i]) +"']) != 0"
    tempp = tempp + tips
    tem = tem + sb
    i = i + 1

print(tempp)
print(tem)

reqMsg = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
	<S:Body xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
		<wrap:oBOW712711 xmlns:wrap="http://wrapper.trade.tfrunning.com/">
			<transaction>
				<body>
					<request>
						<xfaceTradeDTO>
							<oBOW712711DTO>
								<middHead>
									<wdmc>贵州凯里农村商业银行股份有限公司</wdmc>
									<yybs>003</yybs>
									<mac/>
								</middHead>
								<middBody>
									<stop_date>20211206</stop_date>
									<page_num>10</page_num>
									<branch>2510001</branch>
									<payacctinfo>
										<payer_acct/>
									</payacctinfo>
									<start_num>1</start_num>
									<id_num>522731199612269404</id_num>
									<payacctnum/>
									<id_type/>
									<ywbh>003004810000</ywbh>
									<trans_status/>
									<start_date>20211105</start_date>
									<trans_type/>
									<channel_seq/>
								</middBody>
							</oBOW712711DTO>
						</xfaceTradeDTO>
						<vocationalHeader>
							<postingDateText>0</postingDateText>
							<origExternalTask>712711</origExternalTask>
							<authCode>0</authCode>
							<trackNumber>ITLR20190918030005158651</trackNumber>
							<serviceCode>712711</serviceCode>
							<authorizer/>
							<revwCode>0</revwCode>
							<checker/>
							<tfOrigChannel>ITLR</tfOrigChannel>
							<userId>134835</userId>
							<xipDate>20190918</xipDate>
							<tfChannel>ITLR</tfChannel>
							<tranName>社保(个人)交易明细查询</tranName>
							<externalTask>712711</externalTask>
							<menuCode/>
							<userReferenceNumber>ITLR20190918030005158651</userReferenceNumber>
							<externalBranchCode>2510001</externalBranchCode>
						</vocationalHeader>
					</request>
				</body>
				<header>
					<security>
						<loginUser>ITLR</loginUser>
						<requestIp>11.18.14.93</requestIp>
					</security>
					<signature/>
					<message>
						<sndDt>20190918</sndDt>
						<msgType>OBOW.07127110.01</msgType>
						<reqAppCd>ITLR</reqAppCd>
						<reserve/>
						<msgId>ITLR20190918030005158651</msgId>
						<appCd>OBOW</appCd>
						<sndTm>101225993</sndTm>
						<callTyp>SYN</callTyp>
					</message>
					<version>1.0</version>
				</header>
			</transaction>
		</wrap:oBOW712711>
	</S:Body>
</soapenv:Envelope>"""

headers = {"Content-Type":"text/html; charset = utf-8"}
temp = """<?xml version="1.0" encoding="UTF-8"?>
<transaction>
	<header>
		<version>1.0</version>
		<security>
			<loginUser>134002</loginUser>
			<requestIp>127.0.0.1</requestIp>
		</security>
		<message>
			<msgType>OBOW.007127070.01</msgType>
			<msgId>QNYP20190919000000002379</msgId>
			<sndDt>20190919</sndDt>
			<callTyp>SYN</callTyp>
			<sndTm>210412</sndTm>
			<appCd>OBOW</appCd>
			<reqAppCd>QNYP</reqAppCd>
			<reserve></reserve>
		</message>
	</header>
	<body>
		<request>
			<vocationalHeader>
				<serviceCode>712707</serviceCode>
				<tfOrigChannel>QNYP</tfOrigChannel>
				<tfChannel>QNYP</tfChannel>
				<externalTask>QNYP712707</externalTask>
				<externalBranchCode>2730001</externalBranchCode>
				<userId>V11168</userId>
				<postingDateText>0</postingDateText>
				<xipDate>20190919</xipDate>
				<userReferenceNumber>QNYP20190919000000002379000</userReferenceNumber>
				<trackNumber>QNYP20190919000000002379000</trackNumber>
			</vocationalHeader>
			<xfaceTradeDTO>
				<oBOW712707DTO>
					<middHead>
						<wdmc>黔农云</wdmc>
						<yybs>003</yybs>
					</middHead>
					<middBody>
						<ywbh>003004810000</ywbh>
						<oper_flag>3</oper_flag>
						<id_type>201</id_type>
						<id_num>522132197702223412</id_num>
						<name>冯世成</name>
					</middBody>
				</oBOW712707DTO>
			</xfaceTradeDTO>
		</request>
	</body>
</transaction>
"""
print(temp.replace('\n','').replace('\t',''))

# resMsg = requests.post(url="http://127.0.0.1:5000/OSBSSTB", data=reqMsg.encode(), headers = headers)
# resMsg = requests.post(url="http://10.135.0.33:50000/OSBSSTB", data=reqMsg.encode(), headers = headers)
resMsg = """					<responseDTO>
						<jklx>1</jklx>
						<nsrsbh>12520302429400744T</nsrsbh>
						<zgswskfj_dm>15203026200</zgswskfj_dm>
						<zgswj_dm>15203020000</zgswj_dm>
						<zgswskfjmc>国家税务总局遵义市红花岗区税务局第二税务分局</zgswskfjmc>
						<nsrmc>遵义市老城小学</nsrmc>
						<djxh>10215203000000557146</djxh>
						<swjgmc>国家税务总局遵义市红花岗区税务局</swjgmc>
					</responseDTO>
"""
print(type(resMsg))
print(resMsg)

xh = XMLHandler()
xml.sax.parseString(resMsg, xh)
dict = xh.getDict()
print("解析请求报文：")
pprint.pprint(dict)










