from flask import request
from flask import Flask,jsonify
import xml.sax.handler
import pprint
import xml.dom.minidom as Dom
from datetime import datetime

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

#响应报文模板
def writexml(dict):
    doc = Dom.Document()
    #SOAP-ENV:Envelope报文头模拟
    root = doc.createElement("SOAP-ENV:Envelope")
    root.setAttribute("xmlns:SOAP-ENV", "http://schemas.xmlsoap.org/soap/envelope/")
    root.setAttribute("xmlns:SOAP-ENC", "http://schemas.xmlsoap.org/soap/encoding/")
    root.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.setAttribute("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    root.setAttribute("xmlns:tns", "http://wrapper.trade.tfrunning.com/")
    root.setAttribute("xmlns:wsdl", "http://schemas.xmlsoap.org/wsdl/")
    root.setAttribute("xmlns:soap", "http://schemas.xmlsoap.org/wsdl/soap/")
    doc.appendChild(root)
    #响应报文结构
    SOAP_Body = doc.createElement("SOAP-ENV:Body")
    SOAP_Body.setAttribute("SOAP-ENV:encodingStyle","http://schemas.xmlsoap.org/soap/encoding/")
    root.appendChild(SOAP_Body)
    #需要适配
    root_node =doc.createElement("tns:oBOW712736Response")
    SOAP_Body.appendChild(root_node)

    transaction_node = doc.createElement("transaction")
    root_node.appendChild(transaction_node)
    header = doc.createElement("header")
    body = doc.createElement("body")
    transaction_node.appendChild(header)
    transaction_node.appendChild(body)

    # signature
    signature_node = doc.createElement("signature")
    signature_value = doc.createTextNode("")
    signature_node.appendChild(signature_value)
    header.appendChild(signature_node)

    # version
    version_node = doc.createElement("version")
    version_value = doc.createTextNode("1.0")
    version_node.appendChild(version_value)
    header.appendChild(version_node)

    # message
    message_node = doc.createElement("message")
    header.appendChild(message_node)

    # message>callTyp
    callTyp_node = doc.createElement("callTyp")
    callTyp_value = doc.createTextNode("")
    callTyp_node.appendChild(callTyp_value)
    message_node.appendChild(callTyp_node)

    # message>msgRef
    msgRef_node = doc.createElement("msgRef")
    msgRef_value = doc.createTextNode("")
    msgRef_node.appendChild(msgRef_value)
    message_node.appendChild(msgRef_node)

    # message>msgType
    msgType_node = doc.createElement("msgType")
    msgType_value = doc.createTextNode("")
    msgType_node.appendChild(msgType_value)
    message_node.appendChild(msgType_node)

    # message>reserve
    reserve_node = doc.createElement("reserve")
    reserve_value = doc.createTextNode("")
    reserve_node.appendChild(reserve_value)
    message_node.appendChild(reserve_node)

    # status
    status_node = doc.createElement("status")
    header.appendChild(status_node)

    # status>appCd
    appCd_node = doc.createElement("appCd")
    appCd_value = doc.createTextNode("")
    appCd_node.appendChild(appCd_value)
    status_node.appendChild(appCd_node)

    # status>desc
    desc_node = doc.createElement("desc")
    desc_value = doc.createTextNode("")
    desc_node.appendChild(desc_value)
    status_node.appendChild(desc_node)

    # status>retCd
    retCd_node = doc.createElement("retCd")
    retCd_value = doc.createTextNode("")
    retCd_node.appendChild(retCd_value)
    status_node.appendChild(retCd_node)

    # status>wrapperFailDetailMessage
    wrapperFailDetailMessage_node = doc.createElement("wrapperFailDetailMessage")
    wrapperFailDetailMessage_value = doc.createTextNode("")
    wrapperFailDetailMessage_node.appendChild(wrapperFailDetailMessage_value)
    status_node.appendChild(wrapperFailDetailMessage_node)

    #response
    response_node = doc.createElement("response")
    body.appendChild(response_node)

    # response>xfaceTradeDTO
    xfaceTradeDTO_node = doc.createElement("xfaceTradeDTO")
    response_node.appendChild(xfaceTradeDTO_node)

    # response>xfaceTradeDTO>responseDTO
    xresponseDTO_node = doc.createElement("responseDTO")
    xfaceTradeDTO_node.appendChild(xresponseDTO_node)

    # response>xfaceTradeDTO>responseDTO>qycxjgwjm
    qycxjgwjm_node = doc.createElement("qycxjgwjm")
    qycxjgwjm_value = doc.createTextNode("")
    qycxjgwjm_node.appendChild(qycxjgwjm_value)
    xresponseDTO_node.appendChild(qycxjgwjm_node)

    # response>xfaceTradeDTO>responseDTO>qycxjgwjlj
    qycxjgwjlj_node = doc.createElement("qycxjgwjlj")
    qycxjgwjlj_value = doc.createTextNode("")
    qycxjgwjlj_node.appendChild(qycxjgwjlj_value)
    xresponseDTO_node.appendChild(qycxjgwjlj_node)

    # pprint.pprint(doc.toxml("utf-8"))
    returnXml = doc.toprettyxml(indent="\t", newl="\n")
    # print(returnXml)
    file_name = "./http/" + dict['msgType'] + ".xml"
    f = open(file_name, "w")
    f.write(doc.toprettyxml(indent="\t", newl="\n"))
    f.close()
    return returnXml

#响应报文 SSTB场景
def fixed_writexml_SSTB(dict, tnsdict, Msgtype):
    # 根据不同交易处理响应报文
    serviceCode = dict["serviceCode"]
    doc = Dom.Document()
    serviceCodeFlag = False

    #根据类型不同处理响应报文头部
    if Msgtype == "HS":
        # SOAP-ENV:Envelope报文头模拟
        root = doc.createElement("SOAP-ENV:Envelope")
        root.setAttribute("xmlns:SOAP-ENV", "http://schemas.xmlsoap.org/soap/envelope/")
        root.setAttribute("xmlns:SOAP-ENC", "http://schemas.xmlsoap.org/soap/encoding/")
        root.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.setAttribute("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
        root.setAttribute("xmlns:tns", "http://wrapper.trade.tfrunning.com/")
        root.setAttribute("xmlns:wsdl", "http://schemas.xmlsoap.org/wsdl/")
        root.setAttribute("xmlns:soap", "http://schemas.xmlsoap.org/wsdl/soap/")
        doc.appendChild(root)
        # 响应报文结构
        SOAP_Body = doc.createElement("SOAP-ENV:Body")
        SOAP_Body.setAttribute("SOAP-ENV:encodingStyle", "http://schemas.xmlsoap.org/soap/encoding/")
        root.appendChild(SOAP_Body)
        # 适配tns
        root_node = doc.createElement(tnsdict['tns'])
        SOAP_Body.appendChild(root_node)

        transaction_node = doc.createElement("transaction")
        root_node.appendChild(transaction_node)

    else:
        #报文头模拟
        transaction_node = doc.createElement("transaction")
        transaction_node.setAttribute("xmlns:SOAP-ENV", "http://schemas.xmlsoap.org/soap/envelope/")
        transaction_node.setAttribute("xmlns:SOAP-ENC", "http://schemas.xmlsoap.org/soap/encoding/")
        transaction_node.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        transaction_node.setAttribute("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
        transaction_node.setAttribute("xmlns:tns", "http://wrapper.trade.tfrunning.com/")
        transaction_node.setAttribute("xmlns:wsdl", "http://schemas.xmlsoap.org/wsdl/")
        transaction_node.setAttribute("xmlns:soap", "http://schemas.xmlsoap.org/wsdl/soap/")
        doc.appendChild(transaction_node)

    header = doc.createElement("header")
    body = doc.createElement("body")
    transaction_node.appendChild(header)
    transaction_node.appendChild(body)

    # signature
    signature_node = doc.createElement("signature")
    signature_value = doc.createTextNode("")
    if "signature" in dict.keys():
        signature_value = doc.createTextNode(dict['signature'])
    signature_node.appendChild(signature_value)
    header.appendChild(signature_node)

    # version
    version_node = doc.createElement("version")
    if "version" in dict.keys():
        version_value = doc.createTextNode(dict['version'])
        version_node.appendChild(version_value)
    header.appendChild(version_node)

    # message
    message_node = doc.createElement("message")
    header.appendChild(message_node)

    # message>callTyp
    callTyp_node = doc.createElement("callTyp")
    callTyp_value = doc.createTextNode(dict['callTyp'])
    callTyp_node.appendChild(callTyp_value)
    message_node.appendChild(callTyp_node)

    # message>msgRef
    msgRef_node = doc.createElement("msgRef")
    msgRef_value = doc.createTextNode(dict['msgId'])
    msgRef_node.appendChild(msgRef_value)
    message_node.appendChild(msgRef_node)

    # message>msgType
    msgType_node = doc.createElement("msgType")
    msgType_value = doc.createTextNode(dict['msgType'])
    msgType_node.appendChild(msgType_value)
    message_node.appendChild(msgType_node)

    # message>reserve
    reserve_node = doc.createElement("reserve")
    reserve_value = doc.createTextNode(dict['reserve'])
    reserve_node.appendChild(reserve_value)
    message_node.appendChild(reserve_node)

    # status
    status_node = doc.createElement("status")
    header.appendChild(status_node)

    # status>appCd
    appCd_node = doc.createElement("appCd")
    appCd_value = doc.createTextNode(dict['appCd'])
    appCd_node.appendChild(appCd_value)
    status_node.appendChild(appCd_node)

    # status>desc
    desc_node = doc.createElement("desc")
    desc_value = doc.createTextNode("交易成功")  # 默认交易成功
    if serviceCode == "712708":
        desc_value = doc.createTextNode("协议明细查询成功")
    if serviceCode == "712709":
        desc_value = doc.createTextNode("凭证打印查询成功")
    if serviceCode == "712713":
        desc_value = doc.createTextNode("现金调账成功")
    if serviceCode == "712717":
        desc_value = doc.createTextNode("查询成功")
    if serviceCode == "712718":
        desc_value = doc.createTextNode("缴费文件上传提交成功，后台正在入库，请关注进度")

    # status>retCd
    retCd_node = doc.createElement("retCd")
    retCd_value = doc.createTextNode("00000")

    # response
    response_node = doc.createElement("response")
    body.appendChild(response_node)

    # response>xfaceTradeDTO
    xfaceTradeDTO_node = doc.createElement("xfaceTradeDTO")
    response_node.appendChild(xfaceTradeDTO_node)

    # response>xfaceTradeDTO>responseDTO
    xresponseDTO_node = doc.createElement("responseDTO")
    xfaceTradeDTO_node.appendChild(xresponseDTO_node)

    # 实现查询自然人的参保缴费信息的功能
    if serviceCode == "712701":
        # 检查必填关键字段
        if "yybs" in dict.keys() and "ywbh" in dict.keys() and "id_type" in dict.keys() and "id_num" in dict.keys() and "name" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0 and len(dict['ywbh']) != 0 and len(dict['id_type']) != 0 and len(
                    dict['id_num']) != 0 and len(dict['name']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>reg_order
        reg_order_node = doc.createElement("reg_order")
        reg_order_value = doc.createTextNode("20125200910013638666")
        if not serviceCodeFlag:
            reg_order_value = doc.createTextNode("")
        reg_order_node.appendChild(reg_order_value)
        xresponseDTO_node.appendChild(reg_order_node)

        # response>xfaceTradeDTO>responseDTO>det_num
        det_num_node = doc.createElement("det_num")
        det_num_value = doc.createTextNode("1")
        if not serviceCodeFlag:
            det_num_value = doc.createTextNode("")
        det_num_node.appendChild(det_num_value)
        xresponseDTO_node.appendChild(det_num_node)

        if serviceCodeFlag:
            # response>xfaceTradeDTO>responseDTO>insuranceInfo
            insuranceInfo_node = doc.createElement("insuranceInfo")
            xresponseDTO_node.appendChild(insuranceInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>social_sec_branch
            social_sec_branch_node = doc.createElement("social_sec_branch")
            social_sec_branch_value = doc.createTextNode("5200000201522731")
            social_sec_branch_node.appendChild(social_sec_branch_value)
            insuranceInfo_node.appendChild(social_sec_branch_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>user_id
            user_id_node = doc.createElement("user_id")
            user_id_value = doc.createTextNode("28258950")
            user_id_node.appendChild(user_id_value)
            insuranceInfo_node.appendChild(user_id_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_org_code
            tax_org_code_node = doc.createElement("tax_org_code")
            tax_org_code_value = doc.createTextNode("15227310000")
            tax_org_code_node.appendChild(tax_org_code_value)
            insuranceInfo_node.appendChild(tax_org_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_type
            pay_type_node = doc.createElement("pay_type")
            pay_type_value = doc.createTextNode("0")
            pay_type_node.appendChild(pay_type_value)
            insuranceInfo_node.appendChild(pay_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>sub_det_num
            sub_det_num_node = doc.createElement("sub_det_num")
            sub_det_num_value = doc.createTextNode("1")
            sub_det_num_node.appendChild(sub_det_num_value)
            insuranceInfo_node.appendChild(sub_det_num_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo
            insuranceTypeInfo_node = doc.createElement("insuranceTypeInfo")
            insuranceInfo_node.appendChild(insuranceTypeInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>begin_date
            begin_date_node = doc.createElement("begin_date")
            begin_date_value = doc.createTextNode("201210")
            begin_date_node.appendChild(begin_date_value)
            insuranceTypeInfo_node.appendChild(begin_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>end_date
            end_date_node = doc.createElement("end_date")
            end_date_value = doc.createTextNode("999912")
            end_date_node.appendChild(end_date_value)
            insuranceTypeInfo_node.appendChild(end_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>project_code
            project_code_node = doc.createElement("project_code")
            project_code_value = doc.createTextNode("10210")
            project_code_node.appendChild(project_code_value)
            insuranceTypeInfo_node.appendChild(project_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>project_name
            project_name_node = doc.createElement("project_name")
            project_name_value = doc.createTextNode("城乡居民基本养老保险费")
            project_name_node.appendChild(project_name_value)
            insuranceTypeInfo_node.appendChild(project_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>item_code
            item_code_node = doc.createElement("item_code")
            item_code_value = doc.createTextNode("102100100")
            item_code_node.appendChild(item_code_value)
            insuranceTypeInfo_node.appendChild(item_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>item_name
            item_name_node = doc.createElement("item_name")
            item_name_value = doc.createTextNode("城乡居民基本养老保险费")
            item_name_node.appendChild(item_name_value)
            insuranceTypeInfo_node.appendChild(item_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>sub_item_code
            sub_item_code_node = doc.createElement("sub_item_code")
            sub_item_code_value = doc.createTextNode("000000000")
            sub_item_code_node.appendChild(sub_item_code_value)
            insuranceTypeInfo_node.appendChild(sub_item_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>sub_item_name
            sub_item_name_node = doc.createElement("sub_item_name")
            sub_item_name_value = doc.createTextNode("000000000")
            sub_item_name_node.appendChild(sub_item_name_value)
            insuranceTypeInfo_node.appendChild(sub_item_name_node)

    # 实现获取城乡居民的社保缴费信息或者缴费档次信息的功能
    elif serviceCode == "712702":
        # 检查必填关键字段
        if "yybs" in dict.keys() and "ywbh" in dict.keys() and "id_type" in dict.keys() \
                and "id_num" in dict.keys() and "name" in dict.keys() and "insurance_type" in dict.keys() \
                and "pay_year" in dict.keys() and "user_id" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0 and len(dict['ywbh']) != 0 and len(dict['id_type']) != 0 \
                    and len(dict['id_num']) != 0 and len(dict['name']) != 0 and len(dict['insurance_type']) != 0 \
                    and len(dict['pay_year']) != 0 and len(dict['user_id']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("未查到批次信息记录，请确认字段是否输入正确")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>switch_date
        switch_date_node = doc.createElement("switch_date")
        switch_date_value = doc.createTextNode("20190916")
        if not serviceCodeFlag:
            switch_date_value = doc.createTextNode("")
        switch_date_node.appendChild(switch_date_value)
        xresponseDTO_node.appendChild(switch_date_node)

        # response>xfaceTradeDTO>responseDTO>tax_serial
        tax_serial_node = doc.createElement("tax_serial")
        tax_serial_value = doc.createTextNode("10012949")
        if not serviceCodeFlag:
            tax_serial_value = doc.createTextNode("")
        tax_serial_node.appendChild(tax_serial_value)
        xresponseDTO_node.appendChild(tax_serial_node)

        # response>xfaceTradeDTO>responseDTO>reg_order
        reg_order_node = doc.createElement("reg_order")
        reg_order_value = doc.createTextNode("20125200910013638666")
        if not serviceCodeFlag:
            reg_order_value = doc.createTextNode("")
        reg_order_node.appendChild(reg_order_value)
        xresponseDTO_node.appendChild(reg_order_node)

        # response>xfaceTradeDTO>responseDTO>total_num
        total_num_node = doc.createElement("total_num")
        total_num_value = doc.createTextNode("1")
        if not serviceCodeFlag:
            total_num_value = doc.createTextNode("")
        total_num_node.appendChild(total_num_value)
        xresponseDTO_node.appendChild(total_num_node)

        # response>xfaceTradeDTO>responseDTO>total_amt
        total_amt_node = doc.createElement("total_amt")
        total_amt_value = doc.createTextNode("100.00")
        if not serviceCodeFlag:
            total_amt_value = doc.createTextNode("")
        total_amt_node.appendChild(total_amt_value)
        xresponseDTO_node.appendChild(total_amt_node)

        # response>xfaceTradeDTO>responseDTO>settle_bank_acct
        settle_bank_acct_node = doc.createElement("settle_bank_acct")
        settle_bank_acct_value = doc.createTextNode("264000123140600005024159")
        if not serviceCodeFlag:
            settle_bank_acct_value = doc.createTextNode("")
        settle_bank_acct_node.appendChild(settle_bank_acct_value)
        xresponseDTO_node.appendChild(settle_bank_acct_node)

        # response>xfaceTradeDTO>responseDTO>settle_bank_name
        settle_bank_name_node = doc.createElement("settle_bank_name")
        settle_bank_name_value = doc.createTextNode("待报解社会保险费")
        if not serviceCodeFlag:
            settle_bank_name_value = doc.createTextNode("")
        settle_bank_name_node.appendChild(settle_bank_name_value)
        xresponseDTO_node.appendChild(settle_bank_name_node)

        if serviceCodeFlag:
            # response>xfaceTradeDTO>responseDTO>insuranceInfo
            insuranceInfo_node = doc.createElement("insuranceInfo")
            xresponseDTO_node.appendChild(insuranceInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>social_sec_branch
            social_sec_branch_node = doc.createElement("social_sec_branch")
            social_sec_branch_value = doc.createTextNode("5200000201522731")
            if not serviceCodeFlag:
                social_sec_branch_value = doc.createTextNode("")
            social_sec_branch_node.appendChild(social_sec_branch_value)
            insuranceInfo_node.appendChild(social_sec_branch_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>social_sec_serial
            social_sec_serial_node = doc.createElement("social_sec_serial")
            social_sec_serial_value = doc.createTextNode("07f88ad61e6e4b1b90391dbc2a5440e6")
            if not serviceCodeFlag:
                social_sec_serial_value = doc.createTextNode("")
            social_sec_serial_node.appendChild(social_sec_serial_value)
            insuranceInfo_node.appendChild(social_sec_serial_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>detail_serial
            detail_serial_node = doc.createElement("detail_serial")
            detail_serial_value = doc.createTextNode("887b3eef01874f3b9806cb0d7a4fbffb")
            if not serviceCodeFlag:
                detail_serial_value = doc.createTextNode("")
            detail_serial_node.appendChild(detail_serial_value)
            insuranceInfo_node.appendChild(detail_serial_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>user_id
            user_id_node = doc.createElement("user_id")
            user_id_value = doc.createTextNode("28258950")
            if not serviceCodeFlag:
                user_id_value = doc.createTextNode("")
            user_id_node.appendChild(user_id_value)
            insuranceInfo_node.appendChild(user_id_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_org_code
            tax_org_code_node = doc.createElement("tax_org_code")
            tax_org_code_value = doc.createTextNode("15227310000")
            if not serviceCodeFlag:
                tax_org_code_value = doc.createTextNode("")
            tax_org_code_node.appendChild(tax_org_code_value)
            insuranceInfo_node.appendChild(tax_org_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_branch_code
            tax_branch_code_node = doc.createElement("tax_branch_code")
            tax_branch_code_value = doc.createTextNode("15227316200")
            if not serviceCodeFlag:
                tax_branch_code_value = doc.createTextNode("")
            tax_branch_code_node.appendChild(tax_branch_code_value)
            insuranceInfo_node.appendChild(tax_branch_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>begin_date
            begin_date_node = doc.createElement("begin_date")
            begin_date_value = doc.createTextNode("201901")
            if not serviceCodeFlag:
                begin_date_value = doc.createTextNode("")
            begin_date_node.appendChild(begin_date_value)
            insuranceInfo_node.appendChild(begin_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>end_date
            end_date_node = doc.createElement("end_date")
            end_date_value = doc.createTextNode("201912")
            if not serviceCodeFlag:
                end_date_value = doc.createTextNode("")
            end_date_node.appendChild(end_date_value)
            insuranceInfo_node.appendChild(end_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>project_code
            project_code_node = doc.createElement("project_code")
            project_code_value = doc.createTextNode("10210")
            if not serviceCodeFlag:
                project_code_value = doc.createTextNode("")
            project_code_node.appendChild(project_code_value)
            insuranceInfo_node.appendChild(project_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>project_name
            project_name_node = doc.createElement("project_name")
            project_name_value = doc.createTextNode("城乡居民基本养老保险费")
            if not serviceCodeFlag:
                project_name_value = doc.createTextNode("")
            project_name_node.appendChild(project_name_value)
            insuranceInfo_node.appendChild(project_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>items_code
            items_code_node = doc.createElement("items_code")
            items_code_value = doc.createTextNode("102100100")
            if not serviceCodeFlag:
                items_code_value = doc.createTextNode("")
            items_code_node.appendChild(items_code_value)
            insuranceInfo_node.appendChild(items_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>items_name
            items_name_node = doc.createElement("items_name")
            items_name_value = doc.createTextNode("城乡居民基本养老保险费")
            if not serviceCodeFlag:
                items_name_value = doc.createTextNode("")
            items_name_node.appendChild(items_name_value)
            insuranceInfo_node.appendChild(items_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>sub_item_code
            sub_item_code_node = doc.createElement("sub_item_code")
            sub_item_code_value = doc.createTextNode("000000000")
            if not serviceCodeFlag:
                sub_item_code_value = doc.createTextNode("")
            sub_item_code_node.appendChild(sub_item_code_value)
            insuranceInfo_node.appendChild(sub_item_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>sub_item_name
            sub_item_name_node = doc.createElement("sub_item_name")
            sub_item_name_value = doc.createTextNode("000000000")
            if not serviceCodeFlag:
                sub_item_name_value = doc.createTextNode("")
            sub_item_name_node.appendChild(sub_item_name_value)
            insuranceInfo_node.appendChild(sub_item_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_amt
            pay_amt_node = doc.createElement("pay_amt")
            pay_amt_value = doc.createTextNode("100.00")
            if not serviceCodeFlag:
                pay_amt_value = doc.createTextNode("")
            pay_amt_node.appendChild(pay_amt_value)
            insuranceInfo_node.appendChild(pay_amt_node)

    # 实现获取灵活就业人员的待缴费信息或者缴费档次信息的功能
    elif serviceCode == "712703":
        # 检查必填关键字段  yybs ywbh  id_type id_num name insurance_type begin_date end_date  user_id pay_base
        if "yybs" in dict.keys() and "ywbh" in dict.keys() and "" in dict.keys() and "id_type" in dict.keys() \
                and "id_num" in dict.keys() and "name" in dict.keys() and "insurance_type" in dict.keys() \
                and "begin_date" in dict.keys() and "end_date" in dict.keys() and "user_id" in dict.keys() \
                and "pay_base" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0 and len(dict['ywbh']) != 0 and len(dict['']) != 0 and len(
                    dict['id_type']) != 0 and len(dict['id_num']) != 0 and len(dict['name']) != 0 and len(
                    dict['insurance_type']) != 0 \
                    and len(dict['begin_date']) != 0 and len(dict['end_date']) != 0 and len(dict['user_id']) != 0 \
                    and len(dict['pay_base']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("未查到批次信息记录，请确认字段是否输入正确")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>jfjgwjm
        jfjgwjm_node = doc.createElement("jfjgwjm")
        jfjgwjm_value = doc.createTextNode("202111296901055120190919173001.txt")
        if not serviceCodeFlag:
            jfjgwjm_value = doc.createTextNode("")
        jfjgwjm_node.appendChild(jfjgwjm_value)
        xresponseDTO_node.appendChild(jfjgwjm_node)

        # response>xfaceTradeDTO>responseDTO>jfjgwjlj
        jfjgwjlj_node = doc.createElement("jfjgwjlj")
        jfjgwjlj_value = doc.createTextNode("/OBOW/SSTB/PLJFJG")
        if not serviceCodeFlag:
            jfjgwjlj_value = doc.createTextNode("")
        jfjgwjlj_node.appendChild(jfjgwjlj_value)
        xresponseDTO_node.appendChild(jfjgwjlj_node)

    # 实现个人银行缴费撤销的功能
    elif serviceCode == "712706":
        # 检查必填关键字段 ywbh ori_switch_date ori_tax_serial
        if "yybs" in dict.keys() and "ywbh" in dict.keys() and "ori_switch_date" in dict.keys() and "ori_tax_serial" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0 and len(dict['ywbh']) != 0 and len(dict['ori_switch_date']) != 0 and len(
                    dict['ori_tax_serial']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>host_date
        host_date_node = doc.createElement("host_date")
        host_date_value = doc.createTextNode("20211206")
        if not serviceCodeFlag:
            host_date_value = doc.createTextNode("")
        host_date_node.appendChild(host_date_value)
        xresponseDTO_node.appendChild(host_date_node)

        # response>xfaceTradeDTO>responseDTO>host_time
        host_time_node = doc.createElement("host_time")
        host_time_value = doc.createTextNode("101715")
        if not serviceCodeFlag:
            host_time_value = doc.createTextNode("")
        host_time_node.appendChild(host_time_value)
        xresponseDTO_node.appendChild(host_time_node)

        # response>xfaceTradeDTO>responseDTO>host_serial
        host_serial_node = doc.createElement("host_serial")
        host_serial_value = doc.createTextNode("OBOW2019091809452173969139368")
        if not serviceCodeFlag:
            host_serial_value = doc.createTextNode("")
        host_serial_node.appendChild(host_serial_value)
        xresponseDTO_node.appendChild(host_serial_node)

    # 实现个人委托扣款缴费协议维护的功能
    elif serviceCode == "712707":
        # 检查必填关键字段 ywbh oper_flag id_type id_num name
        if "yybs" in dict.keys() and "ywbh" in dict.keys() and "oper_flag" in dict.keys() and "id_type" in dict.keys() \
                and "id_num" in dict.keys() and "name" in dict.keys():
            #oper_flag 为2时签约字段判断
            if dict["oper_flag"] == '2':
                if "payer_acct" in dict.keys() and "acct_name" in dict.keys() and "acct_type" in dict.keys() and "open_inst" in dict.keys():
                    if len(dict['payer_acct']) != 0 and len(dict['acct_name']) != 0 and len(dict['acct_type']) != 0 and len(dict['open_inst']) != 0:
                        serviceCodeFlag = True
            #解约状态
            if dict["oper_flag"] == '3':
                if len(dict['yybs']) != 0 and len(dict['ywbh']) != 0 and len(dict['oper_flag']) != 0\
                        and len(dict['id_type']) != 0  and len(dict['id_num']) != 0 and len(dict['name']) != 0:
                    serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("操作标志非法！必填字段不能为空请确认，提示oper_flag 只能为2或者3")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>protocol_no
        protocol_no_node = doc.createElement("protocol_no")
        protocol_no_value = doc.createTextNode("4027010029992019092369155647")
        if not serviceCodeFlag:
            protocol_no_value = doc.createTextNode("")
        protocol_no_node.appendChild(protocol_no_value)
        xresponseDTO_node.appendChild(protocol_no_node)

        # response>xfaceTradeDTO>responseDTO>payer_open_bank
        payer_open_bank_node = doc.createElement("payer_open_bank")
        payer_open_bank_value = doc.createTextNode("314701012069")
        if not serviceCodeFlag:
            payer_open_bank_value = doc.createTextNode("")
        payer_open_bank_node.appendChild(payer_open_bank_value)
        xresponseDTO_node.appendChild(payer_open_bank_node)

        # response>xfaceTradeDTO>responseDTO>payer_open_bank_name
        payer_open_bank_name_node = doc.createElement("payer_open_bank_name")
        payer_open_bank_name_value = doc.createTextNode("贵州花溪农村商业银行股份有限公司")
        if not serviceCodeFlag:
            payer_open_bank_name_value = doc.createTextNode("")
        payer_open_bank_name_node.appendChild(payer_open_bank_name_value)
        xresponseDTO_node.appendChild(payer_open_bank_name_node)

        # response>xfaceTradeDTO>responseDTO>sign_status
        sign_status_node = doc.createElement("sign_status")
        sign_status_value = doc.createTextNode("1")   #解约
        if dict["oper_flag"] == '2':
            sign_status_value = doc.createTextNode("0")
        if not serviceCodeFlag:
            sign_status_value = doc.createTextNode("")
        sign_status_node.appendChild(sign_status_value)
        xresponseDTO_node.appendChild(sign_status_node)

    # 实现个人委托扣款缴费协议查询的功能
    elif serviceCode == "712708":
        # 检查必填关键字段 ywbh
        if "yybs" in dict.keys() and "ywbh" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0 and len(dict['ywbh']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>tot_num
        tot_num_node = doc.createElement("tot_num")
        tot_num_value = doc.createTextNode("1")
        if not serviceCodeFlag:
            tot_num_value = doc.createTextNode("")
        tot_num_node.appendChild(tot_num_value)
        xresponseDTO_node.appendChild(tot_num_node)

        # response>xfaceTradeDTO>responseDTO>det_num
        det_num_node = doc.createElement("det_num")
        det_num_value = doc.createTextNode("1")
        if not serviceCodeFlag:
            det_num_value = doc.createTextNode("")
        det_num_node.appendChild(det_num_value)
        xresponseDTO_node.appendChild(det_num_node)

        if serviceCodeFlag:
            # response>xfaceTradeDTO>responseDTO>insuranceInfo
            insuranceInfo_node = doc.createElement("insuranceInfo")
            xresponseDTO_node.appendChild(insuranceInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>id_type
            id_type_node = doc.createElement("id_type")
            id_type_value = doc.createTextNode("201")
            if not serviceCodeFlag:
                id_type_value = doc.createTextNode("")
            id_type_node.appendChild(id_type_value)
            insuranceInfo_node.appendChild(id_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>id_num
            id_num_node = doc.createElement("id_num")
            id_num_value = doc.createTextNode("522132197702223412")
            if not serviceCodeFlag:
                id_num_value = doc.createTextNode("")
            id_num_node.appendChild(id_num_value)
            insuranceInfo_node.appendChild(id_num_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>name
            name_node = doc.createElement("name")
            name_value = doc.createTextNode("冯世成")
            if not serviceCodeFlag:
                name_value = doc.createTextNode("")
            name_node.appendChild(name_value)
            insuranceInfo_node.appendChild(name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payer_acct
            payer_acct_node = doc.createElement("payer_acct")
            payer_acct_value = doc.createTextNode("6217790001900003480")
            if not serviceCodeFlag:
                payer_acct_value = doc.createTextNode("")
            payer_acct_node.appendChild(payer_acct_value)
            insuranceInfo_node.appendChild(payer_acct_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payer_acct_name
            payer_acct_name_node = doc.createElement("payer_acct_name")
            payer_acct_name_value = doc.createTextNode("冯世成")
            if not serviceCodeFlag:
                payer_acct_name_value = doc.createTextNode("")
            payer_acct_name_node.appendChild(payer_acct_name_value)
            insuranceInfo_node.appendChild(payer_acct_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payer_acct_type
            payer_acct_type_node = doc.createElement("payer_acct_type")
            payer_acct_type_value = doc.createTextNode("1")
            if not serviceCodeFlag:
                payer_acct_type_value = doc.createTextNode("")
            payer_acct_type_node.appendChild(payer_acct_type_value)
            insuranceInfo_node.appendChild(payer_acct_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>open_inst
            open_inst_node = doc.createElement("open_inst")
            open_inst_value = doc.createTextNode("2060001")
            if not serviceCodeFlag:
                open_inst_value = doc.createTextNode("")
            open_inst_node.appendChild(open_inst_value)
            insuranceInfo_node.appendChild(open_inst_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payer_open_bank
            payer_open_bank_node = doc.createElement("payer_open_bank")
            payer_open_bank_value = doc.createTextNode("314701012069")
            if not serviceCodeFlag:
                payer_open_bank_value = doc.createTextNode("")
            payer_open_bank_node.appendChild(payer_open_bank_value)
            insuranceInfo_node.appendChild(payer_open_bank_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payer_open_bank_name
            payer_open_bank_name_node = doc.createElement("payer_open_bank_name")
            payer_open_bank_name_value = doc.createTextNode("贵州花溪农村商业银行股份有限公司")
            if not serviceCodeFlag:
                payer_open_bank_name_value = doc.createTextNode("")
            payer_open_bank_name_node.appendChild(payer_open_bank_name_value)
            insuranceInfo_node.appendChild(payer_open_bank_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>reg_pltdate
            reg_pltdate_node = doc.createElement("reg_pltdate")
            reg_pltdate_value = doc.createTextNode("20211208")
            if not serviceCodeFlag:
                reg_pltdate_value = doc.createTextNode("")
            reg_pltdate_node.appendChild(reg_pltdate_value)
            insuranceInfo_node.appendChild(reg_pltdate_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>reg_date
            reg_date_node = doc.createElement("reg_date")
            reg_date_value = doc.createTextNode("20190923")
            if not serviceCodeFlag:
                reg_date_value = doc.createTextNode("")
            reg_date_node.appendChild(reg_date_value)
            insuranceInfo_node.appendChild(reg_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>reg_time
            reg_time_node = doc.createElement("reg_time")
            reg_time_value = doc.createTextNode("134834")
            if not serviceCodeFlag:
                reg_time_value = doc.createTextNode("")
            reg_time_node.appendChild(reg_time_value)
            insuranceInfo_node.appendChild(reg_time_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>branch
            branch_node = doc.createElement("branch")
            branch_value = doc.createTextNode("2060001")
            if not serviceCodeFlag:
                branch_value = doc.createTextNode("")
            branch_node.appendChild(branch_value)
            insuranceInfo_node.appendChild(branch_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>teller
            teller_node = doc.createElement("teller")
            teller_value = doc.createTextNode("V12122")
            if not serviceCodeFlag:
                teller_value = doc.createTextNode("")
            teller_node.appendChild(teller_value)
            insuranceInfo_node.appendChild(teller_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>maintain_pltdate
            maintain_pltdate_node = doc.createElement("maintain_pltdate")
            maintain_pltdate_value = doc.createTextNode("")
            if not serviceCodeFlag:
                maintain_pltdate_value = doc.createTextNode("")
            maintain_pltdate_node.appendChild(maintain_pltdate_value)
            insuranceInfo_node.appendChild(maintain_pltdate_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>maintain_date
            maintain_date_node = doc.createElement("maintain_date")
            maintain_date_value = doc.createTextNode("")
            if not serviceCodeFlag:
                maintain_date_value = doc.createTextNode("")
            maintain_date_node.appendChild(maintain_date_value)
            insuranceInfo_node.appendChild(maintain_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>maintain_time
            maintain_time_node = doc.createElement("maintain_time")
            maintain_time_value = doc.createTextNode("")
            if not serviceCodeFlag:
                maintain_time_value = doc.createTextNode("")
            maintain_time_node.appendChild(maintain_time_value)
            insuranceInfo_node.appendChild(maintain_time_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>maintain_branch
            maintain_branch_node = doc.createElement("maintain_branch")
            maintain_branch_value = doc.createTextNode("")
            if not serviceCodeFlag:
                maintain_branch_value = doc.createTextNode("")
            maintain_branch_node.appendChild(maintain_branch_value)
            insuranceInfo_node.appendChild(maintain_branch_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>maintain_teller
            maintain_teller_node = doc.createElement("maintain_teller")
            maintain_teller_value = doc.createTextNode("")
            if not serviceCodeFlag:
                maintain_teller_value = doc.createTextNode("")
            maintain_teller_node.appendChild(maintain_teller_value)
            insuranceInfo_node.appendChild(maintain_teller_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>sign_status
            sign_status_node = doc.createElement("sign_status")
            sign_status_value = doc.createTextNode("0")
            if not serviceCodeFlag:
                sign_status_value = doc.createTextNode("")
            sign_status_node.appendChild(sign_status_value)
            insuranceInfo_node.appendChild(sign_status_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>protocol_no
            protocol_no_node = doc.createElement("protocol_no")
            protocol_no_value = doc.createTextNode("4027010029992019092369155761")
            if not serviceCodeFlag:
                protocol_no_value = doc.createTextNode("")
            protocol_no_node.appendChild(protocol_no_value)
            insuranceInfo_node.appendChild(protocol_no_node)

    # 实现个人缴费凭证信息查询的功能
    elif serviceCode == "712709":
        # 检查必填关键字段 ywbh
        if "yybs" in dict.keys() and "ywbh" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0 and len(dict['ywbh']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>tot_num
        tot_num_node = doc.createElement("tot_num")
        tot_num_value = doc.createTextNode("1")
        if not serviceCodeFlag:
            tot_num_value = doc.createTextNode("")
        tot_num_node.appendChild(tot_num_value)
        xresponseDTO_node.appendChild(tot_num_node)

        # response>xfaceTradeDTO>responseDTO>det_num
        det_num_node = doc.createElement("det_num")
        det_num_value = doc.createTextNode("1")
        if not serviceCodeFlag:
            det_num_value = doc.createTextNode("")
        det_num_node.appendChild(det_num_value)
        xresponseDTO_node.appendChild(det_num_node)

        if serviceCodeFlag:
            # response>xfaceTradeDTO>responseDTO>insuranceInfo
            insuranceInfo_node = doc.createElement("insuranceInfo")
            xresponseDTO_node.appendChild(insuranceInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>plt_date
            plt_date_node = doc.createElement("plt_date")
            plt_date_value = doc.createTextNode("20211206")
            if not serviceCodeFlag:
                plt_date_value = doc.createTextNode("")
            plt_date_node.appendChild(plt_date_value)
            insuranceInfo_node.appendChild(plt_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>switch_date
            switch_date_node = doc.createElement("switch_date")
            switch_date_value = doc.createTextNode("20190918")
            if not serviceCodeFlag:
                switch_date_value = doc.createTextNode("")
            switch_date_node.appendChild(switch_date_value)
            insuranceInfo_node.appendChild(switch_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_serial
            tax_serial_node = doc.createElement("tax_serial")
            tax_serial_value = doc.createTextNode("10013028")
            if not serviceCodeFlag:
                tax_serial_value = doc.createTextNode("")
            tax_serial_node.appendChild(tax_serial_value)
            insuranceInfo_node.appendChild(tax_serial_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>trans_serial
            trans_serial_node = doc.createElement("trans_serial")
            trans_serial_value = doc.createTextNode("69139360")
            if not serviceCodeFlag:
                trans_serial_value = doc.createTextNode("")
            trans_serial_node.appendChild(trans_serial_value)
            insuranceInfo_node.appendChild(trans_serial_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>trans_type
            trans_type_node = doc.createElement("trans_type")
            trans_type_value = doc.createTextNode("03")
            if not serviceCodeFlag:
                trans_type_value = doc.createTextNode("")
            trans_type_node.appendChild(trans_type_value)
            insuranceInfo_node.appendChild(trans_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_type
            pay_type_node = doc.createElement("pay_type")
            pay_type_value = doc.createTextNode("0")
            if not serviceCodeFlag:
                pay_type_value = doc.createTextNode("")
            pay_type_node.appendChild(pay_type_value)
            insuranceInfo_node.appendChild(pay_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>branch
            branch_node = doc.createElement("branch")
            branch_value = doc.createTextNode("2510001")
            if not serviceCodeFlag:
                branch_value = doc.createTextNode("")
            branch_node.appendChild(branch_value)
            insuranceInfo_node.appendChild(branch_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>teller
            teller_node = doc.createElement("teller")
            teller_value = doc.createTextNode("134835")
            if not serviceCodeFlag:
                teller_value = doc.createTextNode("")
            teller_node.appendChild(teller_value)
            insuranceInfo_node.appendChild(teller_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>sys_time
            sys_time_node = doc.createElement("sys_time")
            sys_time_value = doc.createTextNode("094245")
            if not serviceCodeFlag:
                sys_time_value = doc.createTextNode("")
            sys_time_node.appendChild(sys_time_value)
            insuranceInfo_node.appendChild(sys_time_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cash_transfer_flag
            cash_transfer_flag_node = doc.createElement("cash_transfer_flag")
            cash_transfer_flag_value = doc.createTextNode("1")
            if not serviceCodeFlag:
                cash_transfer_flag_value = doc.createTextNode("")
            cash_transfer_flag_node.appendChild(cash_transfer_flag_value)
            insuranceInfo_node.appendChild(cash_transfer_flag_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_base
            pay_base_node = doc.createElement("pay_base")
            pay_base_value = doc.createTextNode("")
            if not serviceCodeFlag:
                pay_base_value = doc.createTextNode("")
            pay_base_node.appendChild(pay_base_value)
            insuranceInfo_node.appendChild(pay_base_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>trans_amt
            trans_amt_node = doc.createElement("trans_amt")
            trans_amt_value = doc.createTextNode("300.00")
            if not serviceCodeFlag:
                trans_amt_value = doc.createTextNode("")
            trans_amt_node.appendChild(trans_amt_value)
            insuranceInfo_node.appendChild(trans_amt_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payer_acct
            payer_acct_node = doc.createElement("payer_acct")
            payer_acct_value = doc.createTextNode("251000120119900005024724")
            if not serviceCodeFlag:
                payer_acct_value = doc.createTextNode("")
            payer_acct_node.appendChild(payer_acct_value)
            insuranceInfo_node.appendChild(payer_acct_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payer_acct_name
            payer_acct_name_node = doc.createElement("payer_acct_name")
            payer_acct_name_value = doc.createTextNode("凯里")
            if not serviceCodeFlag:
                payer_acct_name_value = doc.createTextNode("")
            payer_acct_name_node.appendChild(payer_acct_name_value)
            insuranceInfo_node.appendChild(payer_acct_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payer_open_inst
            payer_open_inst_node = doc.createElement("payer_open_inst")
            payer_open_inst_value = doc.createTextNode("2510001")
            if not serviceCodeFlag:
                payer_open_inst_value = doc.createTextNode("")
            payer_open_inst_node.appendChild(payer_open_inst_value)
            insuranceInfo_node.appendChild(payer_open_inst_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insurance_type
            insurance_type_node = doc.createElement("insurance_type")
            insurance_type_value = doc.createTextNode("10210")
            if not serviceCodeFlag:
                insurance_type_value = doc.createTextNode("")
            insurance_type_node.appendChild(insurance_type_value)
            insuranceInfo_node.appendChild(insurance_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>id_type
            id_type_node = doc.createElement("id_type")
            id_type_value = doc.createTextNode("201")
            if not serviceCodeFlag:
                id_type_value = doc.createTextNode("")
            id_type_node.appendChild(id_type_value)
            insuranceInfo_node.appendChild(id_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>id_num
            id_num_node = doc.createElement("id_num")
            id_num_value = doc.createTextNode("522731199612269404")
            if not serviceCodeFlag:
                id_num_value = doc.createTextNode("")
            id_num_node.appendChild(id_num_value)
            insuranceInfo_node.appendChild(id_num_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insured_name
            insured_name_node = doc.createElement("insured_name")
            insured_name_value = doc.createTextNode("王冬叶")
            if not serviceCodeFlag:
                insured_name_value = doc.createTextNode("")
            insured_name_node.appendChild(insured_name_value)
            insuranceInfo_node.appendChild(insured_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>user_id
            user_id_node = doc.createElement("user_id")
            user_id_value = doc.createTextNode("26073488")
            if not serviceCodeFlag:
                user_id_value = doc.createTextNode("")
            user_id_node.appendChild(user_id_value)
            insuranceInfo_node.appendChild(user_id_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>reg_order
            reg_order_node = doc.createElement("reg_order")
            reg_order_value = doc.createTextNode("20125200910000373928")
            if not serviceCodeFlag:
                reg_order_value = doc.createTextNode("")
            reg_order_node.appendChild(reg_order_value)
            insuranceInfo_node.appendChild(reg_order_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payee_acct_name
            payee_acct_name_node = doc.createElement("payee_acct_name")
            payee_acct_name_value = doc.createTextNode("待报解预算收入")
            if not serviceCodeFlag:
                payee_acct_name_value = doc.createTextNode("")
            payee_acct_name_node.appendChild(payee_acct_name_value)
            insuranceInfo_node.appendChild(payee_acct_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payee_acct
            payee_acct_node = doc.createElement("payee_acct")
            payee_acct_value = doc.createTextNode("264000123140600005024159")
            if not serviceCodeFlag:
                payee_acct_value = doc.createTextNode("")
            payee_acct_node.appendChild(payee_acct_value)
            insuranceInfo_node.appendChild(payee_acct_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_year
            pay_year_node = doc.createElement("pay_year")
            pay_year_value = doc.createTextNode("2019")
            if not serviceCodeFlag:
                pay_year_value = doc.createTextNode("")
            pay_year_node.appendChild(pay_year_value)
            insuranceInfo_node.appendChild(pay_year_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>begin_date
            begin_date_node = doc.createElement("begin_date")
            begin_date_value = doc.createTextNode("")
            if not serviceCodeFlag:
                begin_date_value = doc.createTextNode("")
            begin_date_node.appendChild(begin_date_value)
            insuranceInfo_node.appendChild(begin_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>end_date
            end_date_node = doc.createElement("end_date")
            end_date_value = doc.createTextNode("")
            if not serviceCodeFlag:
                end_date_value = doc.createTextNode("")
            end_date_node.appendChild(end_date_value)
            insuranceInfo_node.appendChild(end_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>send_serial
            send_serial_node = doc.createElement("send_serial")
            send_serial_value = doc.createTextNode("40220211206069139360")
            if not serviceCodeFlag:
                send_serial_value = doc.createTextNode("")
            send_serial_node.appendChild(send_serial_value)
            insuranceInfo_node.appendChild(send_serial_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_ticket_num
            tax_ticket_num_node = doc.createElement("tax_ticket_num")
            tax_ticket_num_value = doc.createTextNode("")
            if not serviceCodeFlag:
                tax_ticket_num_value = doc.createTextNode("")
            tax_ticket_num_node.appendChild(tax_ticket_num_value)
            insuranceInfo_node.appendChild(tax_ticket_num_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_pay_code
            tax_pay_code_node = doc.createElement("tax_pay_code")
            tax_pay_code_value = doc.createTextNode("522731199612269404")
            if not serviceCodeFlag:
                tax_pay_code_value = doc.createTextNode("")
            tax_pay_code_node.appendChild(tax_pay_code_value)
            insuranceInfo_node.appendChild(tax_pay_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_pay_name
            tax_pay_name_node = doc.createElement("tax_pay_name")
            tax_pay_name_value = doc.createTextNode("王冬叶")
            if not serviceCodeFlag:
                tax_pay_name_value = doc.createTextNode("")
            tax_pay_name_node.appendChild(tax_pay_name_value)
            insuranceInfo_node.appendChild(tax_pay_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_org_code
            tax_org_code_node = doc.createElement("tax_org_code")
            tax_org_code_value = doc.createTextNode("15227310000")
            if not serviceCodeFlag:
                tax_org_code_value = doc.createTextNode("")
            tax_org_code_node.appendChild(tax_org_code_value)
            insuranceInfo_node.appendChild(tax_org_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_org_name
            tax_org_name_node = doc.createElement("tax_org_name")
            tax_org_name_value = doc.createTextNode("国家税务总局遵义市红花岗区税务局")
            if not serviceCodeFlag:
                tax_org_name_value = doc.createTextNode("")
            tax_org_name_node.appendChild(tax_org_name_value)
            insuranceInfo_node.appendChild(tax_org_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>protocol_no
            protocol_no_node = doc.createElement("protocol_no")
            protocol_no_value = doc.createTextNode("")
            if not serviceCodeFlag:
                protocol_no_value = doc.createTextNode("")
            protocol_no_node.appendChild(protocol_no_value)
            insuranceInfo_node.appendChild(protocol_no_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>invoice_date
            invoice_date_node = doc.createElement("invoice_date")
            invoice_date_value = doc.createTextNode("")
            if not serviceCodeFlag:
                invoice_date_value = doc.createTextNode("")
            invoice_date_node.appendChild(invoice_date_value)
            insuranceInfo_node.appendChild(invoice_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>bank_no
            bank_no_node = doc.createElement("bank_no")
            bank_no_value = doc.createTextNode("402701002999")
            if not serviceCodeFlag:
                bank_no_value = doc.createTextNode("")
            bank_no_node.appendChild(bank_no_value)
            insuranceInfo_node.appendChild(bank_no_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>settle_bank_code
            settle_bank_code_node = doc.createElement("settle_bank_code")
            settle_bank_code_value = doc.createTextNode("402701002999")
            if not serviceCodeFlag:
                settle_bank_code_value = doc.createTextNode("")
            settle_bank_code_node.appendChild(settle_bank_code_value)
            insuranceInfo_node.appendChild(settle_bank_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>settle_bank_name
            settle_bank_name_node = doc.createElement("settle_bank_name")
            settle_bank_name_value = doc.createTextNode("待报解社会保险费")
            if not serviceCodeFlag:
                settle_bank_name_value = doc.createTextNode("")
            settle_bank_name_node.appendChild(settle_bank_name_value)
            insuranceInfo_node.appendChild(settle_bank_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>settle_bank_acct
            settle_bank_acct_node = doc.createElement("settle_bank_acct")
            settle_bank_acct_value = doc.createTextNode("264000123140600005024159")
            if not serviceCodeFlag:
                settle_bank_acct_value = doc.createTextNode("")
            settle_bank_acct_node.appendChild(settle_bank_acct_value)
            insuranceInfo_node.appendChild(settle_bank_acct_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>host_date
            host_date_node = doc.createElement("host_date")
            host_date_value = doc.createTextNode("20211206")
            if not serviceCodeFlag:
                host_date_value = doc.createTextNode("")
            host_date_node.appendChild(host_date_value)
            insuranceInfo_node.appendChild(host_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>host_serial
            host_serial_node = doc.createElement("host_serial")
            host_serial_value = doc.createTextNode("OBOW2019091809424529269139360")
            if not serviceCodeFlag:
                host_serial_value = doc.createTextNode("")
            host_serial_node.appendChild(host_serial_value)
            insuranceInfo_node.appendChild(host_serial_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>channel_date
            channel_date_node = doc.createElement("channel_date")
            channel_date_value = doc.createTextNode("20190918")
            if not serviceCodeFlag:
                channel_date_value = doc.createTextNode("")
            channel_date_node.appendChild(channel_date_value)
            insuranceInfo_node.appendChild(channel_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>channel_seq
            channel_seq_node = doc.createElement("channel_seq")
            channel_seq_value = doc.createTextNode("ITLR20190918030005158637")
            if not serviceCodeFlag:
                channel_seq_value = doc.createTextNode("")
            channel_seq_node.appendChild(channel_seq_value)
            insuranceInfo_node.appendChild(channel_seq_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>channel_time
            channel_time_node = doc.createElement("channel_time")
            channel_time_value = doc.createTextNode("101151")
            if not serviceCodeFlag:
                channel_time_value = doc.createTextNode("")
            channel_time_node.appendChild(channel_time_value)
            insuranceInfo_node.appendChild(channel_time_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>xtgzh
            xtgzh_node = doc.createElement("xtgzh")
            xtgzh_value = doc.createTextNode("ITLR20190918030005158637")
            if not serviceCodeFlag:
                xtgzh_value = doc.createTextNode("")
            xtgzh_node.appendChild(xtgzh_value)
            insuranceInfo_node.appendChild(xtgzh_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>fkzhlx
            fkzhlx_node = doc.createElement("fkzhlx")
            fkzhlx_value = doc.createTextNode("3")
            if not serviceCodeFlag:
                fkzhlx_value = doc.createTextNode("")
            fkzhlx_node.appendChild(fkzhlx_value)
            insuranceInfo_node.appendChild(fkzhlx_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>jyqd
            jyqd_node = doc.createElement("jyqd")
            jyqd_value = doc.createTextNode("ITLR")
            if not serviceCodeFlag:
                jyqd_value = doc.createTextNode("")
            jyqd_node.appendChild(jyqd_value)
            insuranceInfo_node.appendChild(jyqd_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>dycs
            dycs_node = doc.createElement("dycs")
            dycs_value = doc.createTextNode("1")
            if not serviceCodeFlag:
                dycs_value = doc.createTextNode("")
            dycs_node.appendChild(dycs_value)
            insuranceInfo_node.appendChild(dycs_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxdycs
            cxdycs_node = doc.createElement("cxdycs")
            cxdycs_value = doc.createTextNode("1")
            if not serviceCodeFlag:
                cxdycs_value = doc.createTextNode("")
            cxdycs_node.appendChild(cxdycs_value)
            insuranceInfo_node.appendChild(cxdycs_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxjg
            cxjg_node = doc.createElement("cxjg")
            cxjg_value = doc.createTextNode("2510001")
            if not serviceCodeFlag:
                cxjg_value = doc.createTextNode("")
            cxjg_node.appendChild(cxjg_value)
            insuranceInfo_node.appendChild(cxjg_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxgy
            cxgy_node = doc.createElement("cxgy")
            cxgy_value = doc.createTextNode("134835")
            if not serviceCodeFlag:
                cxgy_value = doc.createTextNode("")
            cxgy_node.appendChild(cxgy_value)
            insuranceInfo_node.appendChild(cxgy_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxsqgy
            cxsqgy_node = doc.createElement("cxsqgy")
            cxsqgy_value = doc.createTextNode("108082")
            if not serviceCodeFlag:
                cxsqgy_value = doc.createTextNode("")
            cxsqgy_node.appendChild(cxsqgy_value)
            insuranceInfo_node.appendChild(cxsqgy_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>sub_det_num
            sub_det_num_node = doc.createElement("sub_det_num")
            sub_det_num_value = doc.createTextNode("1")
            if not serviceCodeFlag:
                sub_det_num_value = doc.createTextNode("")
            sub_det_num_node.appendChild(sub_det_num_value)
            insuranceInfo_node.appendChild(sub_det_num_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo
            insuranceTypeInfo_node = doc.createElement("insuranceTypeInfo")
            insuranceInfo_node.appendChild(insuranceTypeInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>social_sec_branch
            social_sec_branch_node = doc.createElement("social_sec_branch")
            social_sec_branch_value = doc.createTextNode("5200000201522731")
            if not serviceCodeFlag:
                social_sec_branch_value = doc.createTextNode("")
            social_sec_branch_node.appendChild(social_sec_branch_value)
            insuranceTypeInfo_node.appendChild(social_sec_branch_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>social_sec_serial
            social_sec_serial_node = doc.createElement("social_sec_serial")
            social_sec_serial_value = doc.createTextNode("d84caca54f6841c18ccb4e0473f72717")
            if not serviceCodeFlag:
                social_sec_serial_value = doc.createTextNode("")
            social_sec_serial_node.appendChild(social_sec_serial_value)
            insuranceTypeInfo_node.appendChild(social_sec_serial_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>detail_serial
            detail_serial_node = doc.createElement("detail_serial")
            detail_serial_value = doc.createTextNode("d4e12b9d5a0a4945a7921e38937dad48")
            if not serviceCodeFlag:
                detail_serial_value = doc.createTextNode("")
            detail_serial_node.appendChild(detail_serial_value)
            insuranceTypeInfo_node.appendChild(detail_serial_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>user_id
            user_id_node = doc.createElement("user_id")
            user_id_value = doc.createTextNode("26073488")
            if not serviceCodeFlag:
                user_id_value = doc.createTextNode("")
            user_id_node.appendChild(user_id_value)
            insuranceTypeInfo_node.appendChild(user_id_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_org_code
            tax_org_code_node = doc.createElement("tax_org_code")
            tax_org_code_value = doc.createTextNode("15227310000")
            if not serviceCodeFlag:
                tax_org_code_value = doc.createTextNode("")
            tax_org_code_node.appendChild(tax_org_code_value)
            insuranceTypeInfo_node.appendChild(tax_org_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_branch_code
            tax_branch_code_node = doc.createElement("tax_branch_code")
            tax_branch_code_value = doc.createTextNode("15227316200")
            if not serviceCodeFlag:
                tax_branch_code_value = doc.createTextNode("")
            tax_branch_code_node.appendChild(tax_branch_code_value)
            insuranceTypeInfo_node.appendChild(tax_branch_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>begin_date
            begin_date_node = doc.createElement("begin_date")
            begin_date_value = doc.createTextNode("201901")
            if not serviceCodeFlag:
                begin_date_value = doc.createTextNode("")
            begin_date_node.appendChild(begin_date_value)
            insuranceTypeInfo_node.appendChild(begin_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>end_date
            end_date_node = doc.createElement("end_date")
            end_date_value = doc.createTextNode("201912")
            if not serviceCodeFlag:
                end_date_value = doc.createTextNode("")
            end_date_node.appendChild(end_date_value)
            insuranceTypeInfo_node.appendChild(end_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>project_code
            project_code_node = doc.createElement("project_code")
            project_code_value = doc.createTextNode("10210")
            if not serviceCodeFlag:
                project_code_value = doc.createTextNode("")
            project_code_node.appendChild(project_code_value)
            insuranceTypeInfo_node.appendChild(project_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>project_name
            project_name_node = doc.createElement("project_name")
            project_name_value = doc.createTextNode("城乡居民基本养老保险费")
            if not serviceCodeFlag:
                project_name_value = doc.createTextNode("")
            project_name_node.appendChild(project_name_value)
            insuranceTypeInfo_node.appendChild(project_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>items_code
            items_code_node = doc.createElement("items_code")
            items_code_value = doc.createTextNode("102100100")
            if not serviceCodeFlag:
                items_code_value = doc.createTextNode("")
            items_code_node.appendChild(items_code_value)
            insuranceTypeInfo_node.appendChild(items_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>items_name
            items_name_node = doc.createElement("items_name")
            items_name_value = doc.createTextNode("城乡居民基本养老保险费")
            if not serviceCodeFlag:
                items_name_value = doc.createTextNode("")
            items_name_node.appendChild(items_name_value)
            insuranceTypeInfo_node.appendChild(items_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>sub_item_code
            sub_item_code_node = doc.createElement("sub_item_code")
            sub_item_code_value = doc.createTextNode("000000000")
            if not serviceCodeFlag:
                sub_item_code_value = doc.createTextNode("")
            sub_item_code_node.appendChild(sub_item_code_value)
            insuranceTypeInfo_node.appendChild(sub_item_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>sub_item_name
            sub_item_name_node = doc.createElement("sub_item_name")
            sub_item_name_value = doc.createTextNode("000000000")
            if not serviceCodeFlag:
                sub_item_name_value = doc.createTextNode("")
            sub_item_name_node.appendChild(sub_item_name_value)
            insuranceTypeInfo_node.appendChild(sub_item_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_rate
            pay_rate_node = doc.createElement("pay_rate")
            pay_rate_value = doc.createTextNode("")
            if not serviceCodeFlag:
                pay_rate_value = doc.createTextNode("")
            pay_rate_node.appendChild(pay_rate_value)
            insuranceTypeInfo_node.appendChild(pay_rate_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_base
            pay_base_node = doc.createElement("pay_base")
            pay_base_value = doc.createTextNode("")
            if not serviceCodeFlag:
                pay_base_value = doc.createTextNode("")
            pay_base_node.appendChild(pay_base_value)
            insuranceTypeInfo_node.appendChild(pay_base_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_amt
            pay_amt_node = doc.createElement("pay_amt")
            pay_amt_value = doc.createTextNode("300.00")
            if not serviceCodeFlag:
                pay_amt_value = doc.createTextNode("")
            pay_amt_node.appendChild(pay_amt_value)
            insuranceTypeInfo_node.appendChild(pay_amt_node)


    # 实现查询并返回个人缴费明细信息的功能
    elif serviceCode == "712711":
        # 检查必填关键字段 ywbh
        if "yybs" in dict.keys() and "ywbh" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0 and len(dict['ywbh']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>tot_num
        tot_num_node = doc.createElement("tot_num")
        tot_num_value = doc.createTextNode("2")
        if not serviceCodeFlag:
            tot_num_value = doc.createTextNode("")
        tot_num_node.appendChild(tot_num_value)
        xresponseDTO_node.appendChild(tot_num_node)

        # response>xfaceTradeDTO>responseDTO>tot_amt
        tot_amt_node = doc.createElement("tot_amt")
        tot_amt_value = doc.createTextNode("600.00")
        if not serviceCodeFlag:
            tot_amt_value = doc.createTextNode("")
        tot_amt_node.appendChild(tot_amt_value)
        xresponseDTO_node.appendChild(tot_amt_node)

        # response>xfaceTradeDTO>responseDTO>det_num
        det_num_node = doc.createElement("det_num")
        det_num_value = doc.createTextNode("2")
        if not serviceCodeFlag:
            det_num_value = doc.createTextNode("")
        det_num_node.appendChild(det_num_value)
        xresponseDTO_node.appendChild(det_num_node)

        if serviceCodeFlag:
            #第一条记录
            # response>xfaceTradeDTO>responseDTO>insuranceInfo
            insuranceInfo_node = doc.createElement("insuranceInfo")
            xresponseDTO_node.appendChild(insuranceInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>plt_date
            plt_date_node = doc.createElement("plt_date")
            plt_date_value = doc.createTextNode("20211206")
            plt_date_node.appendChild(plt_date_value)
            insuranceInfo_node.appendChild(plt_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>switch_date
            switch_date_node = doc.createElement("switch_date")
            switch_date_value = doc.createTextNode("20190918")
            switch_date_node.appendChild(switch_date_value)
            insuranceInfo_node.appendChild(switch_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_serial
            tax_serial_node = doc.createElement("tax_serial")
            tax_serial_value = doc.createTextNode("10013021")
            tax_serial_node.appendChild(tax_serial_value)
            insuranceInfo_node.appendChild(tax_serial_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>trans_serial
            trans_serial_node = doc.createElement("trans_serial")
            trans_serial_value = doc.createTextNode("69139222")
            trans_serial_node.appendChild(trans_serial_value)
            insuranceInfo_node.appendChild(trans_serial_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>trans_type
            trans_type_node = doc.createElement("trans_type")
            trans_type_value = doc.createTextNode("03")
            trans_type_node.appendChild(trans_type_value)
            insuranceInfo_node.appendChild(trans_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_type
            pay_type_node = doc.createElement("pay_type")
            pay_type_value = doc.createTextNode("0")
            pay_type_node.appendChild(pay_type_value)
            insuranceInfo_node.appendChild(pay_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>branch
            branch_node = doc.createElement("branch")
            branch_value = doc.createTextNode("2510001")
            branch_node.appendChild(branch_value)
            insuranceInfo_node.appendChild(branch_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>teller
            teller_node = doc.createElement("teller")
            teller_value = doc.createTextNode("134835")
            teller_node.appendChild(teller_value)
            insuranceInfo_node.appendChild(teller_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>sys_time
            sys_time_node = doc.createElement("sys_time")
            sys_time_value = doc.createTextNode("090744")
            sys_time_node.appendChild(sys_time_value)
            insuranceInfo_node.appendChild(sys_time_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cash_transfer_flag
            cash_transfer_flag_node = doc.createElement("cash_transfer_flag")
            cash_transfer_flag_value = doc.createTextNode("1")
            cash_transfer_flag_node.appendChild(cash_transfer_flag_value)
            insuranceInfo_node.appendChild(cash_transfer_flag_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_base
            pay_base_node = doc.createElement("pay_base")
            pay_base_value = doc.createTextNode("")
            pay_base_node.appendChild(pay_base_value)
            insuranceInfo_node.appendChild(pay_base_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>trans_amt
            trans_amt_node = doc.createElement("trans_amt")
            trans_amt_value = doc.createTextNode("300.00")
            trans_amt_node.appendChild(trans_amt_value)
            insuranceInfo_node.appendChild(trans_amt_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payer_acct
            payer_acct_node = doc.createElement("payer_acct")
            payer_acct_value = doc.createTextNode("251000120119900005024724")
            payer_acct_node.appendChild(payer_acct_value)
            insuranceInfo_node.appendChild(payer_acct_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payer_acct_name
            payer_acct_name_node = doc.createElement("payer_acct_name")
            payer_acct_name_value = doc.createTextNode("凯里")
            payer_acct_name_node.appendChild(payer_acct_name_value)
            insuranceInfo_node.appendChild(payer_acct_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payer_open_inst
            payer_open_inst_node = doc.createElement("payer_open_inst")
            payer_open_inst_value = doc.createTextNode("2510001")
            payer_open_inst_node.appendChild(payer_open_inst_value)
            insuranceInfo_node.appendChild(payer_open_inst_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insurance_type
            insurance_type_node = doc.createElement("insurance_type")
            insurance_type_value = doc.createTextNode("10210")
            insurance_type_node.appendChild(insurance_type_value)
            insuranceInfo_node.appendChild(insurance_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>id_type
            id_type_node = doc.createElement("id_type")
            id_type_value = doc.createTextNode("201")
            id_type_node.appendChild(id_type_value)
            insuranceInfo_node.appendChild(id_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>id_num
            id_num_node = doc.createElement("id_num")
            id_num_value = doc.createTextNode("522731199612269404")
            id_num_node.appendChild(id_num_value)
            insuranceInfo_node.appendChild(id_num_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insured_name
            insured_name_node = doc.createElement("insured_name")
            insured_name_value = doc.createTextNode("王冬叶")
            insured_name_node.appendChild(insured_name_value)
            insuranceInfo_node.appendChild(insured_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>user_id
            user_id_node = doc.createElement("user_id")
            user_id_value = doc.createTextNode("26073488")
            user_id_node.appendChild(user_id_value)
            insuranceInfo_node.appendChild(user_id_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>reg_order
            reg_order_node = doc.createElement("reg_order")
            reg_order_value = doc.createTextNode("20125200910000373928")
            reg_order_node.appendChild(reg_order_value)
            insuranceInfo_node.appendChild(reg_order_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payee_acct_name
            payee_acct_name_node = doc.createElement("payee_acct_name")
            payee_acct_name_value = doc.createTextNode("待报解预算收入")
            payee_acct_name_node.appendChild(payee_acct_name_value)
            insuranceInfo_node.appendChild(payee_acct_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payee_acct
            payee_acct_node = doc.createElement("payee_acct")
            payee_acct_value = doc.createTextNode("264000123140600005024159")
            payee_acct_node.appendChild(payee_acct_value)
            insuranceInfo_node.appendChild(payee_acct_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_year
            pay_year_node = doc.createElement("pay_year")
            pay_year_value = doc.createTextNode("2019")
            pay_year_node.appendChild(pay_year_value)
            insuranceInfo_node.appendChild(pay_year_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>begin_date
            begin_date_node = doc.createElement("begin_date")
            begin_date_value = doc.createTextNode("")
            begin_date_node.appendChild(begin_date_value)
            insuranceInfo_node.appendChild(begin_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>end_date
            end_date_node = doc.createElement("end_date")
            end_date_value = doc.createTextNode("")
            end_date_node.appendChild(end_date_value)
            insuranceInfo_node.appendChild(end_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>send_serial
            send_serial_node = doc.createElement("send_serial")
            send_serial_value = doc.createTextNode("40220211206069139222")
            send_serial_node.appendChild(send_serial_value)
            insuranceInfo_node.appendChild(send_serial_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_ticket_num
            tax_ticket_num_node = doc.createElement("tax_ticket_num")
            tax_ticket_num_value = doc.createTextNode("")
            tax_ticket_num_node.appendChild(tax_ticket_num_value)
            insuranceInfo_node.appendChild(tax_ticket_num_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_pay_code
            tax_pay_code_node = doc.createElement("tax_pay_code")
            tax_pay_code_value = doc.createTextNode("522731199612269404")
            tax_pay_code_node.appendChild(tax_pay_code_value)
            insuranceInfo_node.appendChild(tax_pay_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_pay_name
            tax_pay_name_node = doc.createElement("tax_pay_name")
            tax_pay_name_value = doc.createTextNode("王冬叶")
            tax_pay_name_node.appendChild(tax_pay_name_value)
            insuranceInfo_node.appendChild(tax_pay_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_org_code
            tax_org_code_node = doc.createElement("tax_org_code")
            tax_org_code_value = doc.createTextNode("15227310000")
            tax_org_code_node.appendChild(tax_org_code_value)
            insuranceInfo_node.appendChild(tax_org_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_org_name
            tax_org_name_node = doc.createElement("tax_org_name")
            tax_org_name_value = doc.createTextNode("国家税务总局遵义市红花岗区税务局")
            tax_org_name_node.appendChild(tax_org_name_value)
            insuranceInfo_node.appendChild(tax_org_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>protocol_no
            protocol_no_node = doc.createElement("protocol_no")
            protocol_no_value = doc.createTextNode("")
            protocol_no_node.appendChild(protocol_no_value)
            insuranceInfo_node.appendChild(protocol_no_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>invoice_date
            invoice_date_node = doc.createElement("invoice_date")
            invoice_date_value = doc.createTextNode("")
            invoice_date_node.appendChild(invoice_date_value)
            insuranceInfo_node.appendChild(invoice_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>bank_no
            bank_no_node = doc.createElement("bank_no")
            bank_no_value = doc.createTextNode("402701002999")
            bank_no_node.appendChild(bank_no_value)
            insuranceInfo_node.appendChild(bank_no_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>settle_bank_code
            settle_bank_code_node = doc.createElement("settle_bank_code")
            settle_bank_code_value = doc.createTextNode("402701002999")
            settle_bank_code_node.appendChild(settle_bank_code_value)
            insuranceInfo_node.appendChild(settle_bank_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>settle_bank_name
            settle_bank_name_node = doc.createElement("settle_bank_name")
            settle_bank_name_value = doc.createTextNode("待报解社会保险费")
            settle_bank_name_node.appendChild(settle_bank_name_value)
            insuranceInfo_node.appendChild(settle_bank_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>settle_bank_acct
            settle_bank_acct_node = doc.createElement("settle_bank_acct")
            settle_bank_acct_value = doc.createTextNode("264000123140600005024159")
            settle_bank_acct_node.appendChild(settle_bank_acct_value)
            insuranceInfo_node.appendChild(settle_bank_acct_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>host_date
            host_date_node = doc.createElement("host_date")
            host_date_value = doc.createTextNode("20211206")
            host_date_node.appendChild(host_date_value)
            insuranceInfo_node.appendChild(host_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>host_serial
            host_serial_node = doc.createElement("host_serial")
            host_serial_value = doc.createTextNode("OBOW2019091809074472769139222")
            host_serial_node.appendChild(host_serial_value)
            insuranceInfo_node.appendChild(host_serial_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>check_status
            check_status_node = doc.createElement("check_status")
            check_status_value = doc.createTextNode("9")
            check_status_node.appendChild(check_status_value)
            insuranceInfo_node.appendChild(check_status_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>send_flag
            send_flag_node = doc.createElement("send_flag")
            send_flag_value = doc.createTextNode("9")
            send_flag_node.appendChild(send_flag_value)
            insuranceInfo_node.appendChild(send_flag_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>trans_status
            trans_status_node = doc.createElement("trans_status")
            trans_status_value = doc.createTextNode("8")
            trans_status_node.appendChild(trans_status_value)
            insuranceInfo_node.appendChild(trans_status_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>channel_date
            channel_date_node = doc.createElement("channel_date")
            channel_date_value = doc.createTextNode("20190918")
            channel_date_node.appendChild(channel_date_value)
            insuranceInfo_node.appendChild(channel_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>channel_seq
            channel_seq_node = doc.createElement("channel_seq")
            channel_seq_value = doc.createTextNode("ITLR20190918030005157921")
            channel_seq_node.appendChild(channel_seq_value)
            insuranceInfo_node.appendChild(channel_seq_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>channel_time
            channel_time_node = doc.createElement("channel_time")
            channel_time_value = doc.createTextNode("093651")
            channel_time_node.appendChild(channel_time_value)
            insuranceInfo_node.appendChild(channel_time_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>xtgzh
            xtgzh_node = doc.createElement("xtgzh")
            xtgzh_value = doc.createTextNode("ITLR20190918030005157921")
            xtgzh_node.appendChild(xtgzh_value)
            insuranceInfo_node.appendChild(xtgzh_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>fkzhlx
            fkzhlx_node = doc.createElement("fkzhlx")
            fkzhlx_value = doc.createTextNode("3")
            fkzhlx_node.appendChild(fkzhlx_value)
            insuranceInfo_node.appendChild(fkzhlx_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>jyqd
            jyqd_node = doc.createElement("jyqd")
            jyqd_value = doc.createTextNode("ITLR")
            jyqd_node.appendChild(jyqd_value)
            insuranceInfo_node.appendChild(jyqd_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>respmsg
            respmsg_node = doc.createElement("respmsg")
            respmsg_value = doc.createTextNode("撤销成功")
            respmsg_node.appendChild(respmsg_value)
            insuranceInfo_node.appendChild(respmsg_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxjg
            cxjg_node = doc.createElement("cxjg")
            cxjg_value = doc.createTextNode("2510001")
            cxjg_node.appendChild(cxjg_value)
            insuranceInfo_node.appendChild(cxjg_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxgy
            cxgy_node = doc.createElement("cxgy")
            cxgy_value = doc.createTextNode("134835")
            cxgy_node.appendChild(cxgy_value)
            insuranceInfo_node.appendChild(cxgy_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxsqgy
            cxsqgy_node = doc.createElement("cxsqgy")
            cxsqgy_value = doc.createTextNode("108082")
            cxsqgy_node.appendChild(cxsqgy_value)
            insuranceInfo_node.appendChild(cxsqgy_node)

            # 第二条记录
            # response>xfaceTradeDTO>responseDTO>insuranceInfo
            insuranceInfo_node = doc.createElement("insuranceInfo")
            xresponseDTO_node.appendChild(insuranceInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>plt_date
            plt_date_node = doc.createElement("plt_date")
            plt_date_value = doc.createTextNode("20211206")
            plt_date_node.appendChild(plt_date_value)
            insuranceInfo_node.appendChild(plt_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>switch_date
            switch_date_node = doc.createElement("switch_date")
            switch_date_value = doc.createTextNode("20190918")
            switch_date_node.appendChild(switch_date_value)
            insuranceInfo_node.appendChild(switch_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_serial
            tax_serial_node = doc.createElement("tax_serial")
            tax_serial_value = doc.createTextNode("10013028")
            tax_serial_node.appendChild(tax_serial_value)
            insuranceInfo_node.appendChild(tax_serial_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>trans_serial
            trans_serial_node = doc.createElement("trans_serial")
            trans_serial_value = doc.createTextNode("69139360")
            trans_serial_node.appendChild(trans_serial_value)
            insuranceInfo_node.appendChild(trans_serial_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>trans_type
            trans_type_node = doc.createElement("trans_type")
            trans_type_value = doc.createTextNode("03")
            trans_type_node.appendChild(trans_type_value)
            insuranceInfo_node.appendChild(trans_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_type
            pay_type_node = doc.createElement("pay_type")
            pay_type_value = doc.createTextNode("0")
            pay_type_node.appendChild(pay_type_value)
            insuranceInfo_node.appendChild(pay_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>branch
            branch_node = doc.createElement("branch")
            branch_value = doc.createTextNode("2510001")
            branch_node.appendChild(branch_value)
            insuranceInfo_node.appendChild(branch_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>teller
            teller_node = doc.createElement("teller")
            teller_value = doc.createTextNode("134835")
            teller_node.appendChild(teller_value)
            insuranceInfo_node.appendChild(teller_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>sys_time
            sys_time_node = doc.createElement("sys_time")
            sys_time_value = doc.createTextNode("094245")
            sys_time_node.appendChild(sys_time_value)
            insuranceInfo_node.appendChild(sys_time_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cash_transfer_flag
            cash_transfer_flag_node = doc.createElement("cash_transfer_flag")
            cash_transfer_flag_value = doc.createTextNode("1")
            cash_transfer_flag_node.appendChild(cash_transfer_flag_value)
            insuranceInfo_node.appendChild(cash_transfer_flag_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_base
            pay_base_node = doc.createElement("pay_base")
            pay_base_value = doc.createTextNode("")
            pay_base_node.appendChild(pay_base_value)
            insuranceInfo_node.appendChild(pay_base_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>trans_amt
            trans_amt_node = doc.createElement("trans_amt")
            trans_amt_value = doc.createTextNode("300.00")
            trans_amt_node.appendChild(trans_amt_value)
            insuranceInfo_node.appendChild(trans_amt_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payer_acct
            payer_acct_node = doc.createElement("payer_acct")
            payer_acct_value = doc.createTextNode("251000120119900005024724")
            payer_acct_node.appendChild(payer_acct_value)
            insuranceInfo_node.appendChild(payer_acct_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payer_acct_name
            payer_acct_name_node = doc.createElement("payer_acct_name")
            payer_acct_name_value = doc.createTextNode("凯里")
            payer_acct_name_node.appendChild(payer_acct_name_value)
            insuranceInfo_node.appendChild(payer_acct_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payer_open_inst
            payer_open_inst_node = doc.createElement("payer_open_inst")
            payer_open_inst_value = doc.createTextNode("2510001")
            payer_open_inst_node.appendChild(payer_open_inst_value)
            insuranceInfo_node.appendChild(payer_open_inst_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insurance_type
            insurance_type_node = doc.createElement("insurance_type")
            insurance_type_value = doc.createTextNode("10210")
            insurance_type_node.appendChild(insurance_type_value)
            insuranceInfo_node.appendChild(insurance_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>id_type
            id_type_node = doc.createElement("id_type")
            id_type_value = doc.createTextNode("201")
            id_type_node.appendChild(id_type_value)
            insuranceInfo_node.appendChild(id_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>id_num
            id_num_node = doc.createElement("id_num")
            id_num_value = doc.createTextNode("522731199612269404")
            id_num_node.appendChild(id_num_value)
            insuranceInfo_node.appendChild(id_num_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insured_name
            insured_name_node = doc.createElement("insured_name")
            insured_name_value = doc.createTextNode("王冬叶")
            insured_name_node.appendChild(insured_name_value)
            insuranceInfo_node.appendChild(insured_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>user_id
            user_id_node = doc.createElement("user_id")
            user_id_value = doc.createTextNode("26073488")
            user_id_node.appendChild(user_id_value)
            insuranceInfo_node.appendChild(user_id_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>reg_order
            reg_order_node = doc.createElement("reg_order")
            reg_order_value = doc.createTextNode("20125200910000373928")
            reg_order_node.appendChild(reg_order_value)
            insuranceInfo_node.appendChild(reg_order_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payee_acct_name
            payee_acct_name_node = doc.createElement("payee_acct_name")
            payee_acct_name_value = doc.createTextNode("待报解预算收入")
            payee_acct_name_node.appendChild(payee_acct_name_value)
            insuranceInfo_node.appendChild(payee_acct_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>payee_acct
            payee_acct_node = doc.createElement("payee_acct")
            payee_acct_value = doc.createTextNode("264000123140600005024159")
            payee_acct_node.appendChild(payee_acct_value)
            insuranceInfo_node.appendChild(payee_acct_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_year
            pay_year_node = doc.createElement("pay_year")
            pay_year_value = doc.createTextNode("2019")
            pay_year_node.appendChild(pay_year_value)
            insuranceInfo_node.appendChild(pay_year_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>begin_date
            begin_date_node = doc.createElement("begin_date")
            begin_date_value = doc.createTextNode("")
            begin_date_node.appendChild(begin_date_value)
            insuranceInfo_node.appendChild(begin_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>end_date
            end_date_node = doc.createElement("end_date")
            end_date_value = doc.createTextNode("")
            end_date_node.appendChild(end_date_value)
            insuranceInfo_node.appendChild(end_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>send_serial
            send_serial_node = doc.createElement("send_serial")
            send_serial_value = doc.createTextNode("40220211206069139360")
            send_serial_node.appendChild(send_serial_value)
            insuranceInfo_node.appendChild(send_serial_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_ticket_num
            tax_ticket_num_node = doc.createElement("tax_ticket_num")
            tax_ticket_num_value = doc.createTextNode("")
            tax_ticket_num_node.appendChild(tax_ticket_num_value)
            insuranceInfo_node.appendChild(tax_ticket_num_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_pay_code
            tax_pay_code_node = doc.createElement("tax_pay_code")
            tax_pay_code_value = doc.createTextNode("522731199612269404")
            tax_pay_code_node.appendChild(tax_pay_code_value)
            insuranceInfo_node.appendChild(tax_pay_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_pay_name
            tax_pay_name_node = doc.createElement("tax_pay_name")
            tax_pay_name_value = doc.createTextNode("王冬叶")
            tax_pay_name_node.appendChild(tax_pay_name_value)
            insuranceInfo_node.appendChild(tax_pay_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_org_code
            tax_org_code_node = doc.createElement("tax_org_code")
            tax_org_code_value = doc.createTextNode("15227310000")
            tax_org_code_node.appendChild(tax_org_code_value)
            insuranceInfo_node.appendChild(tax_org_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_org_name
            tax_org_name_node = doc.createElement("tax_org_name")
            tax_org_name_value = doc.createTextNode("国家税务总局遵义市红花岗区税务局")
            tax_org_name_node.appendChild(tax_org_name_value)
            insuranceInfo_node.appendChild(tax_org_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>protocol_no
            protocol_no_node = doc.createElement("protocol_no")
            protocol_no_value = doc.createTextNode("")
            protocol_no_node.appendChild(protocol_no_value)
            insuranceInfo_node.appendChild(protocol_no_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>invoice_date
            invoice_date_node = doc.createElement("invoice_date")
            invoice_date_value = doc.createTextNode("")
            invoice_date_node.appendChild(invoice_date_value)
            insuranceInfo_node.appendChild(invoice_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>bank_no
            bank_no_node = doc.createElement("bank_no")
            bank_no_value = doc.createTextNode("402701002999")
            bank_no_node.appendChild(bank_no_value)
            insuranceInfo_node.appendChild(bank_no_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>settle_bank_code
            settle_bank_code_node = doc.createElement("settle_bank_code")
            settle_bank_code_value = doc.createTextNode("402701002999")
            settle_bank_code_node.appendChild(settle_bank_code_value)
            insuranceInfo_node.appendChild(settle_bank_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>settle_bank_name
            settle_bank_name_node = doc.createElement("settle_bank_name")
            settle_bank_name_value = doc.createTextNode("待报解社会保险费")
            settle_bank_name_node.appendChild(settle_bank_name_value)
            insuranceInfo_node.appendChild(settle_bank_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>settle_bank_acct
            settle_bank_acct_node = doc.createElement("settle_bank_acct")
            settle_bank_acct_value = doc.createTextNode("264000123140600005024159")
            settle_bank_acct_node.appendChild(settle_bank_acct_value)
            insuranceInfo_node.appendChild(settle_bank_acct_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>host_date
            host_date_node = doc.createElement("host_date")
            host_date_value = doc.createTextNode("20211206")
            host_date_node.appendChild(host_date_value)
            insuranceInfo_node.appendChild(host_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>host_serial
            host_serial_node = doc.createElement("host_serial")
            host_serial_value = doc.createTextNode("OBOW2019091809424529269139360")
            host_serial_node.appendChild(host_serial_value)
            insuranceInfo_node.appendChild(host_serial_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>check_status
            check_status_node = doc.createElement("check_status")
            check_status_value = doc.createTextNode("9")
            check_status_node.appendChild(check_status_value)
            insuranceInfo_node.appendChild(check_status_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>send_flag
            send_flag_node = doc.createElement("send_flag")
            send_flag_value = doc.createTextNode("9")
            send_flag_node.appendChild(send_flag_value)
            insuranceInfo_node.appendChild(send_flag_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>trans_status
            trans_status_node = doc.createElement("trans_status")
            trans_status_value = doc.createTextNode("8")
            trans_status_node.appendChild(trans_status_value)
            insuranceInfo_node.appendChild(trans_status_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>channel_date
            channel_date_node = doc.createElement("channel_date")
            channel_date_value = doc.createTextNode("20190918")
            channel_date_node.appendChild(channel_date_value)
            insuranceInfo_node.appendChild(channel_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>channel_seq
            channel_seq_node = doc.createElement("channel_seq")
            channel_seq_value = doc.createTextNode("ITLR20190918030005158637")
            channel_seq_node.appendChild(channel_seq_value)
            insuranceInfo_node.appendChild(channel_seq_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>channel_time
            channel_time_node = doc.createElement("channel_time")
            channel_time_value = doc.createTextNode("101151")
            channel_time_node.appendChild(channel_time_value)
            insuranceInfo_node.appendChild(channel_time_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>xtgzh
            xtgzh_node = doc.createElement("xtgzh")
            xtgzh_value = doc.createTextNode("ITLR20190918030005158637")
            xtgzh_node.appendChild(xtgzh_value)
            insuranceInfo_node.appendChild(xtgzh_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>fkzhlx
            fkzhlx_node = doc.createElement("fkzhlx")
            fkzhlx_value = doc.createTextNode("3")
            fkzhlx_node.appendChild(fkzhlx_value)
            insuranceInfo_node.appendChild(fkzhlx_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>jyqd
            jyqd_node = doc.createElement("jyqd")
            jyqd_value = doc.createTextNode("ITLR")
            jyqd_node.appendChild(jyqd_value)
            insuranceInfo_node.appendChild(jyqd_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>respmsg
            respmsg_node = doc.createElement("respmsg")
            respmsg_value = doc.createTextNode("撤销成功")
            respmsg_node.appendChild(respmsg_value)
            insuranceInfo_node.appendChild(respmsg_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxjg
            cxjg_node = doc.createElement("cxjg")
            cxjg_value = doc.createTextNode("2510001")
            cxjg_node.appendChild(cxjg_value)
            insuranceInfo_node.appendChild(cxjg_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxgy
            cxgy_node = doc.createElement("cxgy")
            cxgy_value = doc.createTextNode("134835")
            cxgy_node.appendChild(cxgy_value)
            insuranceInfo_node.appendChild(cxgy_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxsqgy
            cxsqgy_node = doc.createElement("cxsqgy")
            cxsqgy_value = doc.createTextNode("108082")
            cxsqgy_node.appendChild(cxsqgy_value)
            insuranceInfo_node.appendChild(cxsqgy_node)

    # 实现上核心冲正对账差错银行多缴费的功能
    elif serviceCode == "712713":
        # 检查必填关键字段 ywbh ori_check_date ori_host_serial
        if "yybs" in dict.keys() and "ywbh" in dict.keys() and "ori_check_date" in dict.keys() and "ori_host_serial" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0 and len(dict['ywbh']) != 0 and len(dict['ori_check_date']) != 0 and len(
                    dict['ori_host_serial']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>host_adj_date
        host_adj_date_node = doc.createElement("host_adj_date")
        host_adj_date_value = doc.createTextNode("20181231")
        if not serviceCodeFlag:
            host_adj_date_value = doc.createTextNode("")
        host_adj_date_node.appendChild(host_adj_date_value)
        xresponseDTO_node.appendChild(host_adj_date_node)

        # response>xfaceTradeDTO>responseDTO>host_adj_serial
        host_adj_serial_node = doc.createElement("host_adj_serial")
        host_adj_serial_value = doc.createTextNode("OBOW2019050914502043568594501")
        if not serviceCodeFlag:
            host_adj_serial_value = doc.createTextNode("")
        host_adj_serial_node.appendChild(host_adj_serial_value)
        xresponseDTO_node.appendChild(host_adj_serial_node)

        # response>xfaceTradeDTO>responseDTO>adjust_cashacc
        adjust_cashacc_node = doc.createElement("adjust_cashacc")
        adjust_cashacc_value = doc.createTextNode("287000122419999009999998")
        if not serviceCodeFlag:
            adjust_cashacc_value = doc.createTextNode("")
        adjust_cashacc_node.appendChild(adjust_cashacc_value)
        xresponseDTO_node.appendChild(adjust_cashacc_node)

    # 实现查询个人委托扣款批量签约批次信息的功能
    elif serviceCode == "712716":
        # 检查必填关键字段 ywbh wdmc
        if "yybs" in dict.keys() and "ywbh" in dict.keys() and "wdmc" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0 and len(dict['ywbh']) != 0 and len(dict['wdmc']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>zbs
        zbs_node = doc.createElement("zbs")
        zbs_value = doc.createTextNode("3")
        if not serviceCodeFlag:
            zbs_value = doc.createTextNode("")
        zbs_node.appendChild(zbs_value)
        xresponseDTO_node.appendChild(zbs_node)

        # response>xfaceTradeDTO>responseDTO>mxbs
        mxbs_node = doc.createElement("mxbs")
        mxbs_value = doc.createTextNode("3")
        if not serviceCodeFlag:
            mxbs_value = doc.createTextNode("")
        mxbs_node.appendChild(mxbs_value)
        xresponseDTO_node.appendChild(mxbs_node)

        #第一条记录
        if serviceCodeFlag:
            # response>xfaceTradeDTO>responseDTO>insuranceInfo
            list_node = doc.createElement("list")
            xresponseDTO_node.appendChild(list_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>ptrq
            ptrq_node = doc.createElement("ptrq")
            ptrq_value = doc.createTextNode("20190101")
            ptrq_node.appendChild(ptrq_value)
            list_node.appendChild(ptrq_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pch
            pch_node = doc.createElement("pch")
            pch_value = doc.createTextNode("2019010168336407")
            pch_node.appendChild(pch_value)
            list_node.appendChild(pch_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>jyzt
            jyzt_node = doc.createElement("jyzt")
            jyzt_value = doc.createTextNode("0")
            jyzt_node.appendChild(jyzt_value)
            list_node.appendChild(jyzt_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>xyxx
            xyxx_node = doc.createElement("xyxx")
            xyxx_value = doc.createTextNode("批转联签约全部处理完成")
            xyxx_node.appendChild(xyxx_value)
            list_node.appendChild(xyxx_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>qywjm
            qywjm_node = doc.createElement("qywjm")
            qywjm_value = doc.createTextNode("10109120190403151649.txt")
            qywjm_node.appendChild(qywjm_value)
            list_node.appendChild(qywjm_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>fqjg
            fqjg_node = doc.createElement("fqjg")
            fqjg_value = doc.createTextNode("2870001")
            fqjg_node.appendChild(fqjg_value)
            list_node.appendChild(fqjg_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>fqgy
            fqgy_node = doc.createElement("fqgy")
            fqgy_value = doc.createTextNode("101091")
            fqgy_node.appendChild(fqgy_value)
            list_node.appendChild(fqgy_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>fqqd
            fqqd_node = doc.createElement("fqqd")
            fqqd_value = doc.createTextNode("ITLR")
            fqqd_node.appendChild(fqqd_value)
            list_node.appendChild(fqqd_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>xtrq
            xtrq_node = doc.createElement("xtrq")
            xtrq_value = doc.createTextNode("20190403")
            xtrq_node.appendChild(xtrq_value)
            list_node.appendChild(xtrq_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>xtsj
            xtsj_node = doc.createElement("xtsj")
            xtsj_value = doc.createTextNode("150418")
            xtsj_node.appendChild(xtsj_value)
            list_node.appendChild(xtsj_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>rkzbs
            rkzbs_node = doc.createElement("rkzbs")
            rkzbs_value = doc.createTextNode("1")
            rkzbs_node.appendChild(rkzbs_value)
            list_node.appendChild(rkzbs_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>qycgzbs
            qycgzbs_node = doc.createElement("qycgzbs")
            qycgzbs_value = doc.createTextNode("0")
            qycgzbs_node.appendChild(qycgzbs_value)
            list_node.appendChild(qycgzbs_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>qysbzbs
            qysbzbs_node = doc.createElement("qysbzbs")
            qysbzbs_value = doc.createTextNode("1")
            qysbzbs_node.appendChild(qysbzbs_value)
            list_node.appendChild(qysbzbs_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxxtrq
            cxxtrq_node = doc.createElement("cxxtrq")
            cxxtrq_value = doc.createTextNode("")
            cxxtrq_node.appendChild(cxxtrq_value)
            list_node.appendChild(cxxtrq_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxxtsj
            cxxtsj_node = doc.createElement("cxxtsj")
            cxxtsj_value = doc.createTextNode("")
            cxxtsj_node.appendChild(cxxtsj_value)
            list_node.appendChild(cxxtsj_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxfqjg
            cxfqjg_node = doc.createElement("cxfqjg")
            cxfqjg_value = doc.createTextNode("")
            cxfqjg_node.appendChild(cxfqjg_value)
            list_node.appendChild(cxfqjg_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxfqgy
            cxfqgy_node = doc.createElement("cxfqgy")
            cxfqgy_value = doc.createTextNode("")
            cxfqgy_node.appendChild(cxfqgy_value)
            list_node.appendChild(cxfqgy_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxsqgy
            cxsqgy_node = doc.createElement("cxsqgy")
            cxsqgy_value = doc.createTextNode("")
            cxsqgy_node.appendChild(cxsqgy_value)
            list_node.appendChild(cxsqgy_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxfqqd
            cxfqqd_node = doc.createElement("cxfqqd")
            cxfqqd_value = doc.createTextNode("")
            cxfqqd_node.appendChild(cxfqqd_value)
            list_node.appendChild(cxfqqd_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxcgzbs
            cxcgzbs_node = doc.createElement("cxcgzbs")
            cxcgzbs_value = doc.createTextNode("0")
            cxcgzbs_node.appendChild(cxcgzbs_value)
            list_node.appendChild(cxcgzbs_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxsbzbs
            cxsbzbs_node = doc.createElement("cxsbzbs")
            cxsbzbs_value = doc.createTextNode("0")
            cxsbzbs_node.appendChild(cxsbzbs_value)
            list_node.appendChild(cxsbzbs_node)

        #第二条记录
        if serviceCodeFlag:
            # response>xfaceTradeDTO>responseDTO>insuranceInfo
            list_node = doc.createElement("list")
            xresponseDTO_node.appendChild(list_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>ptrq
            ptrq_node = doc.createElement("ptrq")
            ptrq_value = doc.createTextNode("20190101")
            ptrq_node.appendChild(ptrq_value)
            list_node.appendChild(ptrq_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pch
            pch_node = doc.createElement("pch")
            pch_value = doc.createTextNode("2019010168336701")
            pch_node.appendChild(pch_value)
            list_node.appendChild(pch_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>jyzt
            jyzt_node = doc.createElement("jyzt")
            jyzt_value = doc.createTextNode("0")
            jyzt_node.appendChild(jyzt_value)
            list_node.appendChild(jyzt_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>xyxx
            xyxx_node = doc.createElement("xyxx")
            xyxx_value = doc.createTextNode("批转联签约全部处理完成")
            xyxx_node.appendChild(xyxx_value)
            list_node.appendChild(xyxx_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>qywjm
            qywjm_node = doc.createElement("qywjm")
            qywjm_value = doc.createTextNode("10109120190403154337.txt")
            qywjm_node.appendChild(qywjm_value)
            list_node.appendChild(qywjm_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>fqjg
            fqjg_node = doc.createElement("fqjg")
            fqjg_value = doc.createTextNode("2870001")
            fqjg_node.appendChild(fqjg_value)
            list_node.appendChild(fqjg_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>fqgy
            fqgy_node = doc.createElement("fqgy")
            fqgy_value = doc.createTextNode("101091")
            fqgy_node.appendChild(fqgy_value)
            list_node.appendChild(fqgy_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>fqqd
            fqqd_node = doc.createElement("fqqd")
            fqqd_value = doc.createTextNode("ITLR")
            fqqd_node.appendChild(fqqd_value)
            list_node.appendChild(fqqd_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>xtrq
            xtrq_node = doc.createElement("xtrq")
            xtrq_value = doc.createTextNode("20190403")
            xtrq_node.appendChild(xtrq_value)
            list_node.appendChild(xtrq_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>xtsj
            xtsj_node = doc.createElement("xtsj")
            xtsj_value = doc.createTextNode("153106")
            xtsj_node.appendChild(xtsj_value)
            list_node.appendChild(xtsj_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>rkzbs
            rkzbs_node = doc.createElement("rkzbs")
            rkzbs_value = doc.createTextNode("3")
            rkzbs_node.appendChild(rkzbs_value)
            list_node.appendChild(rkzbs_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>qycgzbs
            qycgzbs_node = doc.createElement("qycgzbs")
            qycgzbs_value = doc.createTextNode("0")
            qycgzbs_node.appendChild(qycgzbs_value)
            list_node.appendChild(qycgzbs_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>qysbzbs
            qysbzbs_node = doc.createElement("qysbzbs")
            qysbzbs_value = doc.createTextNode("3")
            qysbzbs_node.appendChild(qysbzbs_value)
            list_node.appendChild(qysbzbs_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxxtrq
            cxxtrq_node = doc.createElement("cxxtrq")
            cxxtrq_value = doc.createTextNode("")
            cxxtrq_node.appendChild(cxxtrq_value)
            list_node.appendChild(cxxtrq_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxxtsj
            cxxtsj_node = doc.createElement("cxxtsj")
            cxxtsj_value = doc.createTextNode("")
            cxxtsj_node.appendChild(cxxtsj_value)
            list_node.appendChild(cxxtsj_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxfqjg
            cxfqjg_node = doc.createElement("cxfqjg")
            cxfqjg_value = doc.createTextNode("")
            cxfqjg_node.appendChild(cxfqjg_value)
            list_node.appendChild(cxfqjg_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxfqgy
            cxfqgy_node = doc.createElement("cxfqgy")
            cxfqgy_value = doc.createTextNode("")
            cxfqgy_node.appendChild(cxfqgy_value)
            list_node.appendChild(cxfqgy_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxsqgy
            cxsqgy_node = doc.createElement("cxsqgy")
            cxsqgy_value = doc.createTextNode("")
            cxsqgy_node.appendChild(cxsqgy_value)
            list_node.appendChild(cxsqgy_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxfqqd
            cxfqqd_node = doc.createElement("cxfqqd")
            cxfqqd_value = doc.createTextNode("")
            cxfqqd_node.appendChild(cxfqqd_value)
            list_node.appendChild(cxfqqd_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxcgzbs
            cxcgzbs_node = doc.createElement("cxcgzbs")
            cxcgzbs_value = doc.createTextNode("0")
            cxcgzbs_node.appendChild(cxcgzbs_value)
            list_node.appendChild(cxcgzbs_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxsbzbs
            cxsbzbs_node = doc.createElement("cxsbzbs")
            cxsbzbs_value = doc.createTextNode("0")
            cxsbzbs_node.appendChild(cxsbzbs_value)
            list_node.appendChild(cxsbzbs_node)

        #第三条记录
        if serviceCodeFlag:
            # response>xfaceTradeDTO>responseDTO>insuranceInfo
            list_node = doc.createElement("list")
            xresponseDTO_node.appendChild(list_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>ptrq
            ptrq_node = doc.createElement("ptrq")
            ptrq_value = doc.createTextNode("20190101")
            ptrq_node.appendChild(ptrq_value)
            list_node.appendChild(ptrq_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pch
            pch_node = doc.createElement("pch")
            pch_value = doc.createTextNode("2019010168336731")
            pch_node.appendChild(pch_value)
            list_node.appendChild(pch_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>jyzt
            jyzt_node = doc.createElement("jyzt")
            jyzt_value = doc.createTextNode("0")
            jyzt_node.appendChild(jyzt_value)
            list_node.appendChild(jyzt_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>xyxx
            xyxx_node = doc.createElement("xyxx")
            xyxx_value = doc.createTextNode("批转联签约全部处理完成")
            xyxx_node.appendChild(xyxx_value)
            list_node.appendChild(xyxx_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>qywjm
            qywjm_node = doc.createElement("qywjm")
            qywjm_value = doc.createTextNode("10109120190403154557.txt")
            qywjm_node.appendChild(qywjm_value)
            list_node.appendChild(qywjm_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>fqjg
            fqjg_node = doc.createElement("fqjg")
            fqjg_value = doc.createTextNode("2870001")
            fqjg_node.appendChild(fqjg_value)
            list_node.appendChild(fqjg_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>fqgy
            fqgy_node = doc.createElement("fqgy")
            fqgy_value = doc.createTextNode("101091")
            fqgy_node.appendChild(fqgy_value)
            list_node.appendChild(fqgy_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>fqqd
            fqqd_node = doc.createElement("fqqd")
            fqqd_value = doc.createTextNode("ITLR")
            fqqd_node.appendChild(fqqd_value)
            list_node.appendChild(fqqd_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>xtrq
            xtrq_node = doc.createElement("xtrq")
            xtrq_value = doc.createTextNode("20190403")
            xtrq_node.appendChild(xtrq_value)
            list_node.appendChild(xtrq_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>xtsj
            xtsj_node = doc.createElement("xtsj")
            xtsj_value = doc.createTextNode("153325")
            xtsj_node.appendChild(xtsj_value)
            list_node.appendChild(xtsj_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>rkzbs
            rkzbs_node = doc.createElement("rkzbs")
            rkzbs_value = doc.createTextNode("1")
            rkzbs_node.appendChild(rkzbs_value)
            list_node.appendChild(rkzbs_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>qycgzbs
            qycgzbs_node = doc.createElement("qycgzbs")
            qycgzbs_value = doc.createTextNode("0")
            qycgzbs_node.appendChild(qycgzbs_value)
            list_node.appendChild(qycgzbs_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>qysbzbs
            qysbzbs_node = doc.createElement("qysbzbs")
            qysbzbs_value = doc.createTextNode("1")
            qysbzbs_node.appendChild(qysbzbs_value)
            list_node.appendChild(qysbzbs_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxxtrq
            cxxtrq_node = doc.createElement("cxxtrq")
            cxxtrq_value = doc.createTextNode("")
            cxxtrq_node.appendChild(cxxtrq_value)
            list_node.appendChild(cxxtrq_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxxtsj
            cxxtsj_node = doc.createElement("cxxtsj")
            cxxtsj_value = doc.createTextNode("")
            cxxtsj_node.appendChild(cxxtsj_value)
            list_node.appendChild(cxxtsj_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxfqjg
            cxfqjg_node = doc.createElement("cxfqjg")
            cxfqjg_value = doc.createTextNode("")
            cxfqjg_node.appendChild(cxfqjg_value)
            list_node.appendChild(cxfqjg_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxfqgy
            cxfqgy_node = doc.createElement("cxfqgy")
            cxfqgy_value = doc.createTextNode("")
            cxfqgy_node.appendChild(cxfqgy_value)
            list_node.appendChild(cxfqgy_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxsqgy
            cxsqgy_node = doc.createElement("cxsqgy")
            cxsqgy_value = doc.createTextNode("")
            cxsqgy_node.appendChild(cxsqgy_value)
            list_node.appendChild(cxsqgy_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxfqqd
            cxfqqd_node = doc.createElement("cxfqqd")
            cxfqqd_value = doc.createTextNode("")
            cxfqqd_node.appendChild(cxfqqd_value)
            list_node.appendChild(cxfqqd_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxcgzbs
            cxcgzbs_node = doc.createElement("cxcgzbs")
            cxcgzbs_value = doc.createTextNode("0")
            cxcgzbs_node.appendChild(cxcgzbs_value)
            list_node.appendChild(cxcgzbs_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>cxsbzbs
            cxsbzbs_node = doc.createElement("cxsbzbs")
            cxsbzbs_value = doc.createTextNode("0")
            cxsbzbs_node.appendChild(cxsbzbs_value)
            list_node.appendChild(cxsbzbs_node)

    # 实现查询对账统计信息的功能
    elif serviceCode == "712717":
        # 检查必填关键字段 ywbh wdmc
        if "yybs" in dict.keys() and "ywbh" in dict.keys() and "wdmc" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0 and len(dict['ywbh']) != 0 and len(dict['wdmc']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>tot_num
        tot_num_node = doc.createElement("tot_num")
        tot_num_value = doc.createTextNode("1")
        if not serviceCodeFlag:
            tot_num_value = doc.createTextNode("")
        tot_num_node.appendChild(tot_num_value)
        xresponseDTO_node.appendChild(tot_num_node)

        # response>xfaceTradeDTO>responseDTO>det_num
        det_num_node = doc.createElement("det_num")
        det_num_value = doc.createTextNode("1")
        if not serviceCodeFlag:
            det_num_value = doc.createTextNode("")
        det_num_node.appendChild(det_num_value)
        xresponseDTO_node.appendChild(det_num_node)

        if serviceCodeFlag:
            # response>xfaceTradeDTO>responseDTO>insuranceInfo
            insuranceInfo_node = doc.createElement("insuranceInfo")
            xresponseDTO_node.appendChild(insuranceInfo_node)

            # response>xfaceTradeDTO>responseDTO>check_date
            check_date_node = doc.createElement("check_date")
            check_date_value = doc.createTextNode("20190814")
            if not serviceCodeFlag:
                check_date_value = doc.createTextNode("")
            check_date_node.appendChild(check_date_value)
            insuranceInfo_node.appendChild(check_date_node)

            # response>xfaceTradeDTO>responseDTO>tot_suc_num
            tot_suc_num_node = doc.createElement("tot_suc_num")
            tot_suc_num_value = doc.createTextNode("2")
            if not serviceCodeFlag:
                tot_suc_num_value = doc.createTextNode("")
            tot_suc_num_node.appendChild(tot_suc_num_value)
            insuranceInfo_node.appendChild(tot_suc_num_node)

            # response>xfaceTradeDTO>responseDTO>tot_suc_amt
            tot_suc_amt_node = doc.createElement("tot_suc_amt")
            tot_suc_amt_value = doc.createTextNode("320.00")
            if not serviceCodeFlag:
                tot_suc_amt_value = doc.createTextNode("")
            tot_suc_amt_node.appendChild(tot_suc_amt_value)
            insuranceInfo_node.appendChild(tot_suc_amt_node)

            # response>xfaceTradeDTO>responseDTO>send_flag
            send_flag_node = doc.createElement("send_flag")
            send_flag_value = doc.createTextNode("0")
            if not serviceCodeFlag:
                send_flag_value = doc.createTextNode("")
            send_flag_node.appendChild(send_flag_value)
            insuranceInfo_node.appendChild(send_flag_node)

            # response>xfaceTradeDTO>responseDTO>branch
            branch_node = doc.createElement("branch")
            branch_value = doc.createTextNode("")
            if not serviceCodeFlag:
                branch_value = doc.createTextNode("")
            branch_node.appendChild(branch_value)
            insuranceInfo_node.appendChild(branch_node)

            # response>xfaceTradeDTO>responseDTO>settle_acct
            settle_acct_node = doc.createElement("settle_acct")
            settle_acct_value = doc.createTextNode("264000123140600005024159")
            if not serviceCodeFlag:
                settle_acct_value = doc.createTextNode("")
            settle_acct_node.appendChild(settle_acct_value)
            insuranceInfo_node.appendChild(settle_acct_node)

            # response>xfaceTradeDTO>responseDTO>settle_acct_name
            settle_acct_name_node = doc.createElement("settle_acct_name")
            settle_acct_name_value = doc.createTextNode("待报解预算收入")
            if not serviceCodeFlag:
                settle_acct_name_value = doc.createTextNode("")
            settle_acct_name_node.appendChild(settle_acct_name_value)
            insuranceInfo_node.appendChild(settle_acct_name_node)

            # response>xfaceTradeDTO>responseDTO>settle_branch
            settle_branch_node = doc.createElement("settle_branch")
            settle_branch_value = doc.createTextNode("2019005")
            if not serviceCodeFlag:
                settle_branch_value = doc.createTextNode("")
            settle_branch_node.appendChild(settle_branch_value)
            insuranceInfo_node.appendChild(settle_branch_node)

            # response>xfaceTradeDTO>responseDTO>tax_org_code
            tax_org_code_node = doc.createElement("tax_org_code")
            tax_org_code_value = doc.createTextNode("15226310000")
            if not serviceCodeFlag:
                tax_org_code_value = doc.createTextNode("")
            tax_org_code_node.appendChild(tax_org_code_value)
            insuranceInfo_node.appendChild(tax_org_code_node)

            # response>xfaceTradeDTO>responseDTO>tax_org_name
            tax_org_name_node = doc.createElement("tax_org_name")
            tax_org_name_value = doc.createTextNode("国家税务总局黎平县税务局")
            if not serviceCodeFlag:
                tax_org_name_value = doc.createTextNode("")
            tax_org_name_node.appendChild(tax_org_name_value)
            insuranceInfo_node.appendChild(tax_org_name_node)

    # 实现批量缴费的功能
    elif serviceCode == "712718":
        # 检查必填关键字段 ywbh jflx
        if "yybs" in dict.keys() and "ywbh" in dict.keys() and "jflx" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0 and len(dict['ywbh']) != 0 and len(dict['jflx']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>pch
        pch_node = doc.createElement("pch")
        pch_value = doc.createTextNode("2021120769143339")
        if not serviceCodeFlag:
            pch_value = doc.createTextNode("")
        pch_node.appendChild(pch_value)
        xresponseDTO_node.appendChild(pch_node)

    # 个人委托扣款批量签约批次撤销明细导出服务
    elif serviceCode == "712736":
        # 检查必填关键字段
        if "yybs" in dict.keys() and "ywbh" in dict.keys() and "pch" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0 and len(dict['ywbh']) != 0 and len(dict['pch']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("未查到批次信息记录，请确认字段是否输入正确")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>qycxjgwjm
        qycxjgwjm_node = doc.createElement("qycxjgwjm")
        qycxjgwjm_value = doc.createTextNode("201812216747608420190916135340.txt")
        if not serviceCodeFlag:
            qycxjgwjm_value = doc.createTextNode("")
        qycxjgwjm_node.appendChild(qycxjgwjm_value)
        xresponseDTO_node.appendChild(qycxjgwjm_node)

        # response>xfaceTradeDTO>responseDTO>qycxjgwjlj
        qycxjgwjlj_node = doc.createElement("qycxjgwjlj")
        qycxjgwjlj_value = doc.createTextNode("/OBOW/SSTB/PLQYCXJG")
        if not serviceCodeFlag:
            qycxjgwjlj_value = doc.createTextNode("")
        qycxjgwjlj_node.appendChild(qycxjgwjlj_value)
        xresponseDTO_node.appendChild(qycxjgwjlj_node)

    # 实现批量缴费明细导出的功能
    elif serviceCode == "712733":
        # 检查必填关键字段
        if "yybs" in dict.keys() and "ywbh" in dict.keys() and "pch" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0 and len(dict['ywbh']) != 0 and len(dict['pch']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("未查到批次信息记录，请确认字段是否输入正确")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>jfjgwjm
        jfjgwjm_node = doc.createElement("jfjgwjm")
        jfjgwjm_value = doc.createTextNode("202111296901055120190919173001.txt")
        if not serviceCodeFlag:
            jfjgwjm_value = doc.createTextNode("")
        jfjgwjm_node.appendChild(jfjgwjm_value)
        xresponseDTO_node.appendChild(jfjgwjm_node)

        # response>xfaceTradeDTO>responseDTO>jfjgwjlj
        jfjgwjlj_node = doc.createElement("jfjgwjlj")
        jfjgwjlj_value = doc.createTextNode("/OBOW/SSTB/PLJFJG")
        if not serviceCodeFlag:
            jfjgwjlj_value = doc.createTextNode("")
        jfjgwjlj_node.appendChild(jfjgwjlj_value)
        xresponseDTO_node.appendChild(jfjgwjlj_node)

    # 实现批量缴费撤销凭证打印次数增加的功能
    elif serviceCode == "712738":
        # 检查必填关键字段 ywbh pch
        if "yybs" in dict.keys() and "ywbh" in dict.keys() and "pch" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0 and len(dict['ywbh']) != 0 and len(dict['pch']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

    else:
        desc_value = doc.createTextNode("未配置报文")

    # status>desc
    desc_node.appendChild(desc_value)
    status_node.appendChild(desc_node)

    # status>retCd
    retCd_node.appendChild(retCd_value)
    status_node.appendChild(retCd_node)

    # status>wrapperFailDetailMessage
    wrapperFailDetailMessage_node = doc.createElement("wrapperFailDetailMessage")
    wrapperFailDetailMessage_value = doc.createTextNode("")
    wrapperFailDetailMessage_node.appendChild(wrapperFailDetailMessage_value)
    status_node.appendChild(wrapperFailDetailMessage_node)

    # pprint.pprint(doc.toxml("utf-8"))
    returnXml = doc.toxml("utf-8")
    # returnXml = doc.toprettyxml(indent="\t", newl="\n")
    # # returnXml = doc.toxml("utf-8")
    # # print("returnXml:" + returnXml)
    # file_name = "./http/" + dict['msgType'] + ".xml"
    # if Msgtype == "HS":
    #     file_name = "./http/" + dict['msgType'] + "HS" + ".xml"
    # f = open(file_name, "w")
    # f.write(returnXml.decode())
    # f.close()
    return returnXml

#响应报文 TIPS场景
def fixed_writexml_TIPS(dict, tnsdict, Msgtype):

    # 根据不同交易处理响应报文
    serviceCode = dict["serviceCode"]
    doc = Dom.Document()
    serviceCodeFlag = False

    #根据类型不同处理响应报文头部
    if Msgtype == "HS":
        # SOAP-ENV:Envelope报文头模拟
        root = doc.createElement("SOAP-ENV:Envelope")
        root.setAttribute("xmlns:SOAP-ENV", "http://schemas.xmlsoap.org/soap/envelope/")
        root.setAttribute("xmlns:SOAP-ENC", "http://schemas.xmlsoap.org/soap/encoding/")
        root.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.setAttribute("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
        root.setAttribute("xmlns:tns", "http://wrapper.trade.tfrunning.com/")
        root.setAttribute("xmlns:wsdl", "http://schemas.xmlsoap.org/wsdl/")
        root.setAttribute("xmlns:soap", "http://schemas.xmlsoap.org/wsdl/soap/")
        doc.appendChild(root)
        # 响应报文结构
        SOAP_Body = doc.createElement("SOAP-ENV:Body")
        SOAP_Body.setAttribute("SOAP-ENV:encodingStyle", "http://schemas.xmlsoap.org/soap/encoding/")
        root.appendChild(SOAP_Body)
        # 适配tns
        root_node = doc.createElement(tnsdict['tns'])
        SOAP_Body.appendChild(root_node)

        transaction_node = doc.createElement("transaction")
        root_node.appendChild(transaction_node)

    else:
        #报文头模拟
        transaction_node = doc.createElement("transaction")
        transaction_node.setAttribute("xmlns:SOAP-ENV", "http://schemas.xmlsoap.org/soap/envelope/")
        transaction_node.setAttribute("xmlns:SOAP-ENC", "http://schemas.xmlsoap.org/soap/encoding/")
        transaction_node.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        transaction_node.setAttribute("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
        transaction_node.setAttribute("xmlns:tns", "http://wrapper.trade.tfrunning.com/")
        transaction_node.setAttribute("xmlns:wsdl", "http://schemas.xmlsoap.org/wsdl/")
        transaction_node.setAttribute("xmlns:soap", "http://schemas.xmlsoap.org/wsdl/soap/")
        doc.appendChild(transaction_node)

    header = doc.createElement("header")
    body = doc.createElement("body")
    transaction_node.appendChild(header)
    transaction_node.appendChild(body)

    # signature
    signature_node = doc.createElement("signature")
    signature_value = doc.createTextNode("")
    if "signature" in dict.keys():
        signature_value = doc.createTextNode(dict['signature'])
    signature_node.appendChild(signature_value)
    header.appendChild(signature_node)

    # version
    version_node = doc.createElement("version")
    if "version" in dict.keys():
        version_value = doc.createTextNode(dict['version'])
        version_node.appendChild(version_value)
    header.appendChild(version_node)

    # message
    message_node = doc.createElement("message")
    header.appendChild(message_node)

    # message>callTyp
    callTyp_node = doc.createElement("callTyp")
    callTyp_value = doc.createTextNode(dict['callTyp'])
    callTyp_node.appendChild(callTyp_value)
    message_node.appendChild(callTyp_node)

    # message>msgRef
    msgRef_node = doc.createElement("msgRef")
    msgRef_value = doc.createTextNode(dict['msgId'])
    msgRef_node.appendChild(msgRef_value)
    message_node.appendChild(msgRef_node)

    # message>msgType
    msgType_node = doc.createElement("msgType")
    msgType_value = doc.createTextNode(dict['msgType'])
    msgType_node.appendChild(msgType_value)
    message_node.appendChild(msgType_node)

    # message>reserve
    reserve_node = doc.createElement("reserve")
    reserve_value = doc.createTextNode(dict['reserve'])
    reserve_node.appendChild(reserve_value)
    message_node.appendChild(reserve_node)

    # status
    status_node = doc.createElement("status")
    header.appendChild(status_node)

    # status>appCd
    appCd_node = doc.createElement("appCd")
    appCd_value = doc.createTextNode(dict['appCd'])
    appCd_node.appendChild(appCd_value)
    status_node.appendChild(appCd_node)

    # status>desc
    desc_node = doc.createElement("desc")
    desc_value = doc.createTextNode("交易成功")  # 默认交易成功
    if serviceCode == "712316":
        desc_value = doc.createTextNode("验证或撤销成功")

    # status>retCd
    retCd_node = doc.createElement("retCd")
    retCd_value = doc.createTextNode("00000")

    # response
    response_node = doc.createElement("response")
    body.appendChild(response_node)

    # response>xfaceTradeDTO
    xfaceTradeDTO_node = doc.createElement("xfaceTradeDTO")
    response_node.appendChild(xfaceTradeDTO_node)

    # response>xfaceTradeDTO>responseDTO
    xresponseDTO_node = doc.createElement("responseDTO")
    xfaceTradeDTO_node.appendChild(xresponseDTO_node)

    #财税银交易
    #实现纳税人基本信息查询功能。任何渠道、柜员都可以发起
    if serviceCode == "712301":
        # 检查必填关键字段 wdmc ywbh gdslxbz nsrsbh
        if "yybs" in dict.keys()  and "wdmc" in dict.keys() and "ywbh" in dict.keys() and "gdslxbz" in dict.keys() \
                and "nsrsbh" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0  and len(dict['wdmc']) != 0 and len(dict['ywbh']) != 0 and len(dict['gdslxbz']) != 0 \
                    and len(dict['nsrsbh']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>jklx
        jklx_node = doc.createElement("jklx")
        jklx_value = doc.createTextNode("1")
        if not serviceCodeFlag:
            jklx_value = doc.createTextNode("")
        jklx_node.appendChild(jklx_value)
        xresponseDTO_node.appendChild(jklx_node)

        # response>xfaceTradeDTO>responseDTO>nsrsbh
        nsrsbh_node = doc.createElement("nsrsbh")
        nsrsbh_value = doc.createTextNode("12520302429400744T")
        if not serviceCodeFlag:
            nsrsbh_value = doc.createTextNode("")
        nsrsbh_node.appendChild(nsrsbh_value)
        xresponseDTO_node.appendChild(nsrsbh_node)

        # response>xfaceTradeDTO>responseDTO>zgswskfj_dm
        zgswskfj_dm_node = doc.createElement("zgswskfj_dm")
        zgswskfj_dm_value = doc.createTextNode("15203026200")
        if not serviceCodeFlag:
            zgswskfj_dm_value = doc.createTextNode("")
        zgswskfj_dm_node.appendChild(zgswskfj_dm_value)
        xresponseDTO_node.appendChild(zgswskfj_dm_node)

        # response>xfaceTradeDTO>responseDTO>zgswj_dm
        zgswj_dm_node = doc.createElement("zgswj_dm")
        zgswj_dm_value = doc.createTextNode("15203020000")
        if not serviceCodeFlag:
            zgswj_dm_value = doc.createTextNode("")
        zgswj_dm_node.appendChild(zgswj_dm_value)
        xresponseDTO_node.appendChild(zgswj_dm_node)

        # response>xfaceTradeDTO>responseDTO>zgswskfjmc
        zgswskfjmc_node = doc.createElement("zgswskfjmc")
        zgswskfjmc_value = doc.createTextNode("国家税务总局遵义市红花岗区税务局第二税务分局")
        if not serviceCodeFlag:
            zgswskfjmc_value = doc.createTextNode("")
        zgswskfjmc_node.appendChild(zgswskfjmc_value)
        xresponseDTO_node.appendChild(zgswskfjmc_node)

        # response>xfaceTradeDTO>responseDTO>nsrmc
        nsrmc_node = doc.createElement("nsrmc")
        nsrmc_value = doc.createTextNode("遵义市老城小学")
        if not serviceCodeFlag:
            nsrmc_value = doc.createTextNode("")
        nsrmc_node.appendChild(nsrmc_value)
        xresponseDTO_node.appendChild(nsrmc_node)

        # response>xfaceTradeDTO>responseDTO>djxh
        djxh_node = doc.createElement("djxh")
        djxh_value = doc.createTextNode("10215203000000557146")
        if not serviceCodeFlag:
            djxh_value = doc.createTextNode("")
        djxh_node.appendChild(djxh_value)
        xresponseDTO_node.appendChild(djxh_node)

        # response>xfaceTradeDTO>responseDTO>swjgmc
        swjgmc_node = doc.createElement("swjgmc")
        swjgmc_value = doc.createTextNode("国家税务总局遵义市红花岗区税务局")
        if not serviceCodeFlag:
            swjgmc_value = doc.createTextNode("")
        swjgmc_node.appendChild(swjgmc_value)
        xresponseDTO_node.appendChild(swjgmc_node)


    #实现银行端查询单位参保登记信息查询功能。任何渠道、柜员都可以发起
    elif serviceCode == "712305":
        # 检查必填关键字段 wdmc ywbh djxh
        if "yybs" in dict.keys()  and "wdmc" in dict.keys() and "ywbh" in dict.keys() and "djxh" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0  and len(dict['wdmc']) != 0 and len(dict['ywbh']) != 0 and len(dict['djxh']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>zgswjgDm
        zgswjgDm_node = doc.createElement("zgswjgDm")
        zgswjgDm_value = doc.createTextNode("15203020000")
        if not serviceCodeFlag:
            zgswjgDm_value = doc.createTextNode("")
        zgswjgDm_node.appendChild(zgswjgDm_value)
        xresponseDTO_node.appendChild(zgswjgDm_node)

        # response>xfaceTradeDTO>responseDTO>zgswjgMc
        zgswjgMc_node = doc.createElement("zgswjgMc")
        zgswjgMc_value = doc.createTextNode("国家税务总局遵义市红花岗区税务局")
        if not serviceCodeFlag:
            zgswjgMc_value = doc.createTextNode("")
        zgswjgMc_node.appendChild(zgswjgMc_value)
        xresponseDTO_node.appendChild(zgswjgMc_node)

        # response>xfaceTradeDTO>responseDTO>zgswksDm
        zgswksDm_node = doc.createElement("zgswksDm")
        zgswksDm_value = doc.createTextNode("15203026200")
        if not serviceCodeFlag:
            zgswksDm_value = doc.createTextNode("")
        zgswksDm_node.appendChild(zgswksDm_value)
        xresponseDTO_node.appendChild(zgswksDm_node)

        # response>xfaceTradeDTO>responseDTO>zgswksMc
        zgswksMc_node = doc.createElement("zgswksMc")
        zgswksMc_value = doc.createTextNode("国家税务总局遵义市红花岗区税务局第二税务分局")
        if not serviceCodeFlag:
            zgswksMc_value = doc.createTextNode("")
        zgswksMc_node.appendChild(zgswksMc_value)
        xresponseDTO_node.appendChild(zgswksMc_node)


        # response>xfaceTradeDTO>responseDTO>jfrztDm
        jfrztDm_node = doc.createElement("jfrztDm")
        jfrztDm_value = doc.createTextNode("03")
        if not serviceCodeFlag:
            jfrztDm_value = doc.createTextNode("")
        jfrztDm_node.appendChild(jfrztDm_value)
        xresponseDTO_node.appendChild(jfrztDm_node)

        # response>xfaceTradeDTO>responseDTO>dbcbxxbs
        dbcbxxbs_node = doc.createElement("dbcbxxbs")
        dbcbxxbs_value = doc.createTextNode("1")
        if not serviceCodeFlag:
            dbcbxxbs_value = doc.createTextNode("")
        dbcbxxbs_node.appendChild(dbcbxxbs_value)
        xresponseDTO_node.appendChild(dbcbxxbs_node)


        if serviceCodeFlag:
            # response>xfaceTradeDTO>responseDTO>dwCbxxList
            dwCbxxList_node = doc.createElement("dwCbxxList")
            xresponseDTO_node.appendChild(dwCbxxList_node)

            # response>xfaceTradeDTO>responseDTO>dwCbxxList>DwCbxxDTO
            DwCbxxDTO_node = doc.createElement("DwCbxxDTO")
            dwCbxxList_node.appendChild(DwCbxxDTO_node)

            # response>xfaceTradeDTO>responseDTO>list>yxbz
            yxbz_node = doc.createElement("yxbz")
            yxbz_value = doc.createTextNode("Y")
            yxbz_node.appendChild(yxbz_value)
            DwCbxxDTO_node.appendChild(yxbz_node)

            # response>xfaceTradeDTO>responseDTO>list>sbjbjgDm
            sbjbjgDm_node = doc.createElement("sbjbjgDm")
            sbjbjgDm_value = doc.createTextNode("5200002202520302")
            sbjbjgDm_node.appendChild(sbjbjgDm_value)
            DwCbxxDTO_node.appendChild(sbjbjgDm_node)

            # response>xfaceTradeDTO>responseDTO>list>sbjbjgMc
            sbjbjgMc_node = doc.createElement("sbjbjgMc")
            sbjbjgMc_value = doc.createTextNode("红花岗区(机关养老保险及职业年金)")
            sbjbjgMc_node.appendChild(sbjbjgMc_value)
            DwCbxxDTO_node.appendChild(sbjbjgMc_node)

            # response>xfaceTradeDTO>responseDTO>list>dwsbbm
            dwsbbm_node = doc.createElement("dwsbbm")
            dwsbbm_value = doc.createTextNode("52030222961")
            dwsbbm_node.appendChild(dwsbbm_value)
            DwCbxxDTO_node.appendChild(dwsbbm_node)

            # response>xfaceTradeDTO>responseDTO>list>xzqhDm
            xzqhDm_node = doc.createElement("xzqhDm")
            xzqhDm_value = doc.createTextNode("520302")
            xzqhDm_node.appendChild(xzqhDm_value)
            DwCbxxDTO_node.appendChild(xzqhDm_node)

            # response>xfaceTradeDTO>responseDTO>list>xzqhMc
            xzqhMc_node = doc.createElement("xzqhMc")
            xzqhMc_value = doc.createTextNode("红花岗区")
            xzqhMc_node.appendChild(xzqhMc_value)
            DwCbxxDTO_node.appendChild(xzqhMc_node)

            # response>xfaceTradeDTO>responseDTO>list>lxrxm
            lxrxm_node = doc.createElement("lxrxm")
            lxrxm_value = doc.createTextNode("唐勇")
            lxrxm_node.appendChild(lxrxm_value)
            DwCbxxDTO_node.appendChild(lxrxm_node)

            # response>xfaceTradeDTO>responseDTO>list>lxdh
            lxdh_node = doc.createElement("lxdh")
            lxdh_value = doc.createTextNode("0851-28258298")
            lxdh_node.appendChild(lxdh_value)
            DwCbxxDTO_node.appendChild(lxdh_node)

            # response>xfaceTradeDTO>responseDTO>list>lxdz
            lxdz_node = doc.createElement("lxdz")
            lxdz_value = doc.createTextNode("遵义市玉屏路7号")
            lxdz_node.appendChild(lxdz_value)
            DwCbxxDTO_node.appendChild(lxdz_node)

            # response>xfaceTradeDTO>responseDTO>list>yzbm
            yzbm_node = doc.createElement("yzbm")
            yzbm_value = doc.createTextNode("563000")
            yzbm_node.appendChild(yzbm_value)
            DwCbxxDTO_node.appendChild(yzbm_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbztDm
            dwcbztDm_node = doc.createElement("dwcbztDm")
            dwcbztDm_value = doc.createTextNode("1")
            dwcbztDm_node.appendChild(dwcbztDm_value)
            DwCbxxDTO_node.appendChild(dwcbztDm_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbztMc
            dwcbztMc_node = doc.createElement("dwcbztMc")
            dwcbztMc_value = doc.createTextNode("正常参保")
            dwcbztMc_node.appendChild(dwcbztMc_value)
            DwCbxxDTO_node.appendChild(dwcbztMc_node)

            # response>xfaceTradeDTO>responseDTO>list>tsdwlbDm
            tsdwlbDm_node = doc.createElement("tsdwlbDm")
            tsdwlbDm_value = doc.createTextNode("")
            tsdwlbDm_node.appendChild(tsdwlbDm_value)
            DwCbxxDTO_node.appendChild(tsdwlbDm_node)

            # response>xfaceTradeDTO>responseDTO>list>tsdwlbMc
            tsdwlbMc_node = doc.createElement("tsdwlbMc")
            tsdwlbMc_value = doc.createTextNode("")
            tsdwlbMc_node.appendChild(tsdwlbMc_value)
            DwCbxxDTO_node.appendChild(tsdwlbMc_node)

            # response>xfaceTradeDTO>responseDTO>list>djzclxDm
            djzclxDm_node = doc.createElement("djzclxDm")
            djzclxDm_value = doc.createTextNode("")
            djzclxDm_node.appendChild(djzclxDm_value)
            DwCbxxDTO_node.appendChild(djzclxDm_node)

            # response>xfaceTradeDTO>responseDTO>list>djzclxMc
            djzclxMc_node = doc.createElement("djzclxMc")
            djzclxMc_value = doc.createTextNode("")
            djzclxMc_node.appendChild(djzclxMc_value)
            DwCbxxDTO_node.appendChild(djzclxMc_node)

            # response>xfaceTradeDTO>responseDTO>list>sshyDm
            sshyDm_node = doc.createElement("sshyDm")
            sshyDm_value = doc.createTextNode("8321")
            sshyDm_node.appendChild(sshyDm_value)
            DwCbxxDTO_node.appendChild(sshyDm_node)

            # response>xfaceTradeDTO>responseDTO>list>sshyMc
            sshyMc_node = doc.createElement("sshyMc")
            sshyMc_value = doc.createTextNode("普通小学教育")
            sshyMc_node.appendChild(sshyMc_value)
            DwCbxxDTO_node.appendChild(sshyMc_node)

            # response>xfaceTradeDTO>responseDTO>list>cbxzbs
            cbxzbs_node = doc.createElement("cbxzbs")
            cbxzbs_value = doc.createTextNode("4")
            cbxzbs_node.appendChild(cbxzbs_value)
            DwCbxxDTO_node.appendChild(cbxzbs_node)

            # response>xfaceTradeDTO>responseDTO>dwCbxxList>DwCbxxDTO>dwCbxzlist>DwCbxxDTO
            dwCbxzlist_node = doc.createElement("dwCbxzlist")
            DwCbxxDTO_node.appendChild(dwCbxzlist_node)

            #第一条数据
            DwCbxzDTO_node = doc.createElement("DwCbxzDTO")
            dwCbxzlist_node.appendChild(DwCbxzDTO_node)

            # response>xfaceTradeDTO>responseDTO>list>zsxmDm
            zsxmDm_node = doc.createElement("zsxmDm")
            zsxmDm_value = doc.createTextNode("10291")
            zsxmDm_node.appendChild(zsxmDm_value)
            DwCbxzDTO_node.appendChild(zsxmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>zspmDm
            zspmDm_node = doc.createElement("zspmDm")
            zspmDm_value = doc.createTextNode("102910002")
            zspmDm_node.appendChild(zspmDm_value)
            DwCbxzDTO_node.appendChild(zspmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>zszmDm
            zszmDm_node = doc.createElement("zszmDm")
            zszmDm_value = doc.createTextNode("")
            zszmDm_node.appendChild(zszmDm_value)
            DwCbxzDTO_node.appendChild(zszmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>tcqBm
            tcqBm_node = doc.createElement("tcqBm")
            tcqBm_value = doc.createTextNode("520302")
            tcqBm_node.appendChild(tcqBm_value)
            DwCbxzDTO_node.appendChild(tcqBm_node)

            # response>xfaceTradeDTO>responseDTO>list>tcqMc
            tcqMc_node = doc.createElement("tcqMc")
            tcqMc_value = doc.createTextNode("红花岗区")
            tcqMc_node.appendChild(tcqMc_value)
            DwCbxzDTO_node.appendChild(tcqMc_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbjfztDm
            dwcbjfztDm_node = doc.createElement("dwcbjfztDm")
            dwcbjfztDm_value = doc.createTextNode("1")
            dwcbjfztDm_node.appendChild(dwcbjfztDm_value)
            DwCbxzDTO_node.appendChild(dwcbjfztDm_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbjfztMc
            dwcbjfztMc_node = doc.createElement("dwcbjfztMc")
            dwcbjfztMc_value = doc.createTextNode("正常参保")
            dwcbjfztMc_node.appendChild(dwcbjfztMc_value)
            DwCbxzDTO_node.appendChild(dwcbjfztMc_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbtslbDm
            dwcbtslbDm_node = doc.createElement("dwcbtslbDm")
            dwcbtslbDm_value = doc.createTextNode("")
            dwcbtslbDm_node.appendChild(dwcbtslbDm_value)
            DwCbxzDTO_node.appendChild(dwcbtslbDm_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbtslbMc
            dwcbtslbMc_node = doc.createElement("dwcbtslbMc")
            dwcbtslbMc_value = doc.createTextNode("")
            dwcbtslbMc_node.appendChild(dwcbtslbMc_value)
            DwCbxzDTO_node.appendChild(dwcbtslbMc_node)

            # response>xfaceTradeDTO>responseDTO>list>jsbzDm
            jsbzDm_node = doc.createElement("jsbzDm")
            jsbzDm_value = doc.createTextNode("N")
            jsbzDm_node.appendChild(jsbzDm_value)
            DwCbxzDTO_node.appendChild(jsbzDm_node)

            # response>xfaceTradeDTO>responseDTO>list>ksjfyf
            ksjfyf_node = doc.createElement("ksjfyf")
            ksjfyf_value = doc.createTextNode("2014-10")
            ksjfyf_node.appendChild(ksjfyf_value)
            DwCbxzDTO_node.appendChild(ksjfyf_node)

            # response>xfaceTradeDTO>responseDTO>list>tzjfyf
            tzjfyf_node = doc.createElement("tzjfyf")
            tzjfyf_value = doc.createTextNode("9999-12")
            tzjfyf_node.appendChild(tzjfyf_value)
            DwCbxzDTO_node.appendChild(tzjfyf_node)

            # response>xfaceTradeDTO>responseDTO>list>pmname
            pmname_node = doc.createElement("pmname")
            pmname_value = doc.createTextNode("")
            pmname_node.appendChild(pmname_value)
            DwCbxzDTO_node.appendChild(pmname_node)

            #第二条数据
            DwCbxzDTO_node = doc.createElement("DwCbxzDTO")
            dwCbxzlist_node.appendChild(DwCbxzDTO_node)

            # response>xfaceTradeDTO>responseDTO>list>zsxmDm
            zsxmDm_node = doc.createElement("zsxmDm")
            zsxmDm_value = doc.createTextNode("10211")
            zsxmDm_node.appendChild(zsxmDm_value)
            DwCbxzDTO_node.appendChild(zsxmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>zspmDm
            zspmDm_node = doc.createElement("zspmDm")
            zspmDm_value = doc.createTextNode("102110101")
            zspmDm_node.appendChild(zspmDm_value)
            DwCbxzDTO_node.appendChild(zspmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>zszmDm
            zszmDm_node = doc.createElement("zszmDm")
            zszmDm_value = doc.createTextNode("")
            zszmDm_node.appendChild(zszmDm_value)
            DwCbxzDTO_node.appendChild(zszmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>tcqBm
            tcqBm_node = doc.createElement("tcqBm")
            tcqBm_value = doc.createTextNode("520302")
            tcqBm_node.appendChild(tcqBm_value)
            DwCbxzDTO_node.appendChild(tcqBm_node)

            # response>xfaceTradeDTO>responseDTO>list>tcqMc
            tcqMc_node = doc.createElement("tcqMc")
            tcqMc_value = doc.createTextNode("红花岗区")
            tcqMc_node.appendChild(tcqMc_value)
            DwCbxzDTO_node.appendChild(tcqMc_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbjfztDm
            dwcbjfztDm_node = doc.createElement("dwcbjfztDm")
            dwcbjfztDm_value = doc.createTextNode("1")
            dwcbjfztDm_node.appendChild(dwcbjfztDm_value)
            DwCbxzDTO_node.appendChild(dwcbjfztDm_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbjfztMc
            dwcbjfztMc_node = doc.createElement("dwcbjfztMc")
            dwcbjfztMc_value = doc.createTextNode("正常参保")
            dwcbjfztMc_node.appendChild(dwcbjfztMc_value)
            DwCbxzDTO_node.appendChild(dwcbjfztMc_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbtslbDm
            dwcbtslbDm_node = doc.createElement("dwcbtslbDm")
            dwcbtslbDm_value = doc.createTextNode("")
            dwcbtslbDm_node.appendChild(dwcbtslbDm_value)
            DwCbxzDTO_node.appendChild(dwcbtslbDm_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbtslbMc
            dwcbtslbMc_node = doc.createElement("dwcbtslbMc")
            dwcbtslbMc_value = doc.createTextNode("")
            dwcbtslbMc_node.appendChild(dwcbtslbMc_value)
            DwCbxzDTO_node.appendChild(dwcbtslbMc_node)

            # response>xfaceTradeDTO>responseDTO>list>jsbzDm
            jsbzDm_node = doc.createElement("jsbzDm")
            jsbzDm_value = doc.createTextNode("N")
            jsbzDm_node.appendChild(jsbzDm_value)
            DwCbxzDTO_node.appendChild(jsbzDm_node)

            # response>xfaceTradeDTO>responseDTO>list>ksjfyf
            ksjfyf_node = doc.createElement("ksjfyf")
            ksjfyf_value = doc.createTextNode("2014-10")
            ksjfyf_node.appendChild(ksjfyf_value)
            DwCbxzDTO_node.appendChild(ksjfyf_node)

            # response>xfaceTradeDTO>responseDTO>list>tzjfyf
            tzjfyf_node = doc.createElement("tzjfyf")
            tzjfyf_value = doc.createTextNode("9999-12")
            tzjfyf_node.appendChild(tzjfyf_value)
            DwCbxzDTO_node.appendChild(tzjfyf_node)

            # response>xfaceTradeDTO>responseDTO>list>pmname
            pmname_node = doc.createElement("pmname")
            pmname_value = doc.createTextNode("")
            pmname_node.appendChild(pmname_value)
            DwCbxzDTO_node.appendChild(pmname_node)

            #第三条数据
            DwCbxzDTO_node = doc.createElement("DwCbxzDTO")
            dwCbxzlist_node.appendChild(DwCbxzDTO_node)

            # response>xfaceTradeDTO>responseDTO>list>zsxmDm
            zsxmDm_node = doc.createElement("zsxmDm")
            zsxmDm_value = doc.createTextNode("10291")
            zsxmDm_node.appendChild(zsxmDm_value)
            DwCbxzDTO_node.appendChild(zsxmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>zspmDm
            zspmDm_node = doc.createElement("zspmDm")
            zspmDm_value = doc.createTextNode("102910001")
            zspmDm_node.appendChild(zspmDm_value)
            DwCbxzDTO_node.appendChild(zspmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>zszmDm
            zszmDm_node = doc.createElement("zszmDm")
            zszmDm_value = doc.createTextNode("")
            zszmDm_node.appendChild(zszmDm_value)
            DwCbxzDTO_node.appendChild(zszmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>tcqBm
            tcqBm_node = doc.createElement("tcqBm")
            tcqBm_value = doc.createTextNode("520302")
            tcqBm_node.appendChild(tcqBm_value)
            DwCbxzDTO_node.appendChild(tcqBm_node)

            # response>xfaceTradeDTO>responseDTO>list>tcqMc
            tcqMc_node = doc.createElement("tcqMc")
            tcqMc_value = doc.createTextNode("红花岗区")
            tcqMc_node.appendChild(tcqMc_value)
            DwCbxzDTO_node.appendChild(tcqMc_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbjfztDm
            dwcbjfztDm_node = doc.createElement("dwcbjfztDm")
            dwcbjfztDm_value = doc.createTextNode("1")
            dwcbjfztDm_node.appendChild(dwcbjfztDm_value)
            DwCbxzDTO_node.appendChild(dwcbjfztDm_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbjfztMc
            dwcbjfztMc_node = doc.createElement("dwcbjfztMc")
            dwcbjfztMc_value = doc.createTextNode("正常参保")
            dwcbjfztMc_node.appendChild(dwcbjfztMc_value)
            DwCbxzDTO_node.appendChild(dwcbjfztMc_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbtslbDm
            dwcbtslbDm_node = doc.createElement("dwcbtslbDm")
            dwcbtslbDm_value = doc.createTextNode("")
            dwcbtslbDm_node.appendChild(dwcbtslbDm_value)
            DwCbxzDTO_node.appendChild(dwcbtslbDm_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbtslbMc
            dwcbtslbMc_node = doc.createElement("dwcbtslbMc")
            dwcbtslbMc_value = doc.createTextNode("")
            dwcbtslbMc_node.appendChild(dwcbtslbMc_value)
            DwCbxzDTO_node.appendChild(dwcbtslbMc_node)

            # response>xfaceTradeDTO>responseDTO>list>jsbzDm
            jsbzDm_node = doc.createElement("jsbzDm")
            jsbzDm_value = doc.createTextNode("N")
            jsbzDm_node.appendChild(jsbzDm_value)
            DwCbxzDTO_node.appendChild(jsbzDm_node)

            # response>xfaceTradeDTO>responseDTO>list>ksjfyf
            ksjfyf_node = doc.createElement("ksjfyf")
            ksjfyf_value = doc.createTextNode("2014-10")
            ksjfyf_node.appendChild(ksjfyf_value)
            DwCbxzDTO_node.appendChild(ksjfyf_node)

            # response>xfaceTradeDTO>responseDTO>list>tzjfyf
            tzjfyf_node = doc.createElement("tzjfyf")
            tzjfyf_value = doc.createTextNode("9999-12")
            tzjfyf_node.appendChild(tzjfyf_value)
            DwCbxzDTO_node.appendChild(tzjfyf_node)

            # response>xfaceTradeDTO>responseDTO>list>pmname
            pmname_node = doc.createElement("pmname")
            pmname_value = doc.createTextNode("")
            pmname_node.appendChild(pmname_value)
            DwCbxzDTO_node.appendChild(pmname_node)

            #第四条数据
            DwCbxzDTO_node = doc.createElement("DwCbxzDTO")
            dwCbxzlist_node.appendChild(DwCbxzDTO_node)

            # response>xfaceTradeDTO>responseDTO>list>zsxmDm
            zsxmDm_node = doc.createElement("zsxmDm")
            zsxmDm_value = doc.createTextNode("10211")
            zsxmDm_node.appendChild(zsxmDm_value)
            DwCbxzDTO_node.appendChild(zsxmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>zspmDm
            zspmDm_node = doc.createElement("zspmDm")
            zspmDm_value = doc.createTextNode("102110102")
            zspmDm_node.appendChild(zspmDm_value)
            DwCbxzDTO_node.appendChild(zspmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>zszmDm
            zszmDm_node = doc.createElement("zszmDm")
            zszmDm_value = doc.createTextNode("")
            zszmDm_node.appendChild(zszmDm_value)
            DwCbxzDTO_node.appendChild(zszmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>tcqBm
            tcqBm_node = doc.createElement("tcqBm")
            tcqBm_value = doc.createTextNode("520302")
            tcqBm_node.appendChild(tcqBm_value)
            DwCbxzDTO_node.appendChild(tcqBm_node)

            # response>xfaceTradeDTO>responseDTO>list>tcqMc
            tcqMc_node = doc.createElement("tcqMc")
            tcqMc_value = doc.createTextNode("红花岗区")
            tcqMc_node.appendChild(tcqMc_value)
            DwCbxzDTO_node.appendChild(tcqMc_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbjfztDm
            dwcbjfztDm_node = doc.createElement("dwcbjfztDm")
            dwcbjfztDm_value = doc.createTextNode("1")
            dwcbjfztDm_node.appendChild(dwcbjfztDm_value)
            DwCbxzDTO_node.appendChild(dwcbjfztDm_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbjfztMc
            dwcbjfztMc_node = doc.createElement("dwcbjfztMc")
            dwcbjfztMc_value = doc.createTextNode("正常参保")
            dwcbjfztMc_node.appendChild(dwcbjfztMc_value)
            DwCbxzDTO_node.appendChild(dwcbjfztMc_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbtslbDm
            dwcbtslbDm_node = doc.createElement("dwcbtslbDm")
            dwcbtslbDm_value = doc.createTextNode("")
            dwcbtslbDm_node.appendChild(dwcbtslbDm_value)
            DwCbxzDTO_node.appendChild(dwcbtslbDm_node)

            # response>xfaceTradeDTO>responseDTO>list>dwcbtslbMc
            dwcbtslbMc_node = doc.createElement("dwcbtslbMc")
            dwcbtslbMc_value = doc.createTextNode("")
            dwcbtslbMc_node.appendChild(dwcbtslbMc_value)
            DwCbxzDTO_node.appendChild(dwcbtslbMc_node)

            # response>xfaceTradeDTO>responseDTO>list>jsbzDm
            jsbzDm_node = doc.createElement("jsbzDm")
            jsbzDm_value = doc.createTextNode("N")
            jsbzDm_node.appendChild(jsbzDm_value)
            DwCbxzDTO_node.appendChild(jsbzDm_node)

            # response>xfaceTradeDTO>responseDTO>list>ksjfyf
            ksjfyf_node = doc.createElement("ksjfyf")
            ksjfyf_value = doc.createTextNode("2014-10")
            ksjfyf_node.appendChild(ksjfyf_value)
            DwCbxzDTO_node.appendChild(ksjfyf_node)

            # response>xfaceTradeDTO>responseDTO>list>tzjfyf
            tzjfyf_node = doc.createElement("tzjfyf")
            tzjfyf_value = doc.createTextNode("9999-12")
            tzjfyf_node.appendChild(tzjfyf_value)
            DwCbxzDTO_node.appendChild(tzjfyf_node)

            # response>xfaceTradeDTO>responseDTO>list>pmname
            pmname_node = doc.createElement("pmname")
            pmname_value = doc.createTextNode("")
            pmname_node.appendChild(pmname_value)
            DwCbxzDTO_node.appendChild(pmname_node)

    #实现银行端查询社保费单位欠费信息的功能。任何渠道、柜员都可以发起
    elif serviceCode == "712306":
        # 检查必填关键字段 wdmc ywbh djxh zgswskfjdm
        if "yybs" in dict.keys()  and "wdmc" in dict.keys() and "ywbh" in dict.keys() and "djxh" in dict.keys() and "zgswskfjdm" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0  and len(dict['wdmc']) != 0 and len(dict['ywbh']) != 0 and len(dict['djxh']) != 0 and len(dict['zgswskfjdm']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>qfzbs
        qfzbs_node = doc.createElement("qfzbs")
        qfzbs_value = doc.createTextNode("6")
        if not serviceCodeFlag:
            qfzbs_value = doc.createTextNode("")
        qfzbs_node.appendChild(qfzbs_value)
        xresponseDTO_node.appendChild(qfzbs_node)

        if serviceCodeFlag:
            # response>xfaceTradeDTO>responseDTO>ZSSbfQsxxGrid>
            ZSSbfQsxxGrid_node = doc.createElement("ZSSbfQsxxGrid")
            xresponseDTO_node.appendChild(ZSSbfQsxxGrid_node)

            #第一个数据
            ZSSbfQsxxGridlb_node = doc.createElement("ZSSbfQsxxGridlb")
            ZSSbfQsxxGrid_node.appendChild(ZSSbfQsxxGridlb_node)

            # response>xfaceTradeDTO>responseDTO>list>hsjg
            hsjg_node = doc.createElement("hsjg")
            hsjg_value = doc.createTextNode("15203020000")
            hsjg_node.appendChild(hsjg_value)
            ZSSbfQsxxGridlb_node.appendChild(hsjg_node)

            # response>xfaceTradeDTO>responseDTO>list>nsrsbh
            nsrsbh_node = doc.createElement("nsrsbh")
            nsrsbh_value = doc.createTextNode("12520302429400744T")
            nsrsbh_node.appendChild(nsrsbh_value)
            ZSSbfQsxxGridlb_node.appendChild(nsrsbh_node)

            # response>xfaceTradeDTO>responseDTO>list>nsrmc
            nsrmc_node = doc.createElement("nsrmc")
            nsrmc_value = doc.createTextNode("遵义市老城小学")
            nsrmc_node.appendChild(nsrmc_value)
            ZSSbfQsxxGridlb_node.appendChild(nsrmc_node)

            # response>xfaceTradeDTO>responseDTO>list>djxh
            djxh_node = doc.createElement("djxh")
            djxh_value = doc.createTextNode("10215203000000557146")
            djxh_node.appendChild(djxh_value)
            ZSSbfQsxxGridlb_node.appendChild(djxh_node)

            # response>xfaceTradeDTO>responseDTO>list>yzpzxh
            yzpzxh_node = doc.createElement("yzpzxh")
            yzpzxh_value = doc.createTextNode("10015218000000002931")
            yzpzxh_node.appendChild(yzpzxh_value)
            ZSSbfQsxxGridlb_node.appendChild(yzpzxh_node)

            # response>xfaceTradeDTO>responseDTO>list>sbbm
            sbbm_node = doc.createElement("sbbm")
            sbbm_value = doc.createTextNode("52030222961")
            sbbm_node.appendChild(sbbm_value)
            ZSSbfQsxxGridlb_node.appendChild(sbbm_node)

            # response>xfaceTradeDTO>responseDTO>list>sbjbjgDm
            sbjbjgDm_node = doc.createElement("sbjbjgDm")
            sbjbjgDm_value = doc.createTextNode("5200002202520302")
            sbjbjgDm_node.appendChild(sbjbjgDm_value)
            ZSSbfQsxxGridlb_node.appendChild(sbjbjgDm_node)

            # response>xfaceTradeDTO>responseDTO>list>skssqq
            skssqq_node = doc.createElement("skssqq")
            skssqq_value = doc.createTextNode("2018-11-01")
            skssqq_node.appendChild(skssqq_value)
            ZSSbfQsxxGridlb_node.appendChild(skssqq_node)

            # response>xfaceTradeDTO>responseDTO>list>skssqz
            skssqz_node = doc.createElement("skssqz")
            skssqz_value = doc.createTextNode("2018-11-30")
            skssqz_node.appendChild(skssqz_value)
            ZSSbfQsxxGridlb_node.appendChild(skssqz_node)

            # response>xfaceTradeDTO>responseDTO>list>zsxmDm
            zsxmDm_node = doc.createElement("zsxmDm")
            zsxmDm_value = doc.createTextNode("10211")
            zsxmDm_node.appendChild(zsxmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(zsxmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>zspmDm
            zspmDm_node = doc.createElement("zspmDm")
            zspmDm_value = doc.createTextNode("102110101")
            zspmDm_node.appendChild(zspmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(zspmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>yskmDm
            yskmDm_node = doc.createElement("yskmDm")
            yskmDm_value = doc.createTextNode("1021101")
            yskmDm_node.appendChild(yskmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(yskmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>ysfpblDm
            ysfpblDm_node = doc.createElement("ysfpblDm")
            ysfpblDm_value = doc.createTextNode("15240001")
            ysfpblDm_node.appendChild(ysfpblDm_value)
            ZSSbfQsxxGridlb_node.appendChild(ysfpblDm_node)

            # response>xfaceTradeDTO>responseDTO>list>skgkDm
            skgkDm_node = doc.createElement("skgkDm")
            skgkDm_value = doc.createTextNode("1520302001")
            skgkDm_node.appendChild(skgkDm_value)
            ZSSbfQsxxGridlb_node.appendChild(skgkDm_node)

            # response>xfaceTradeDTO>responseDTO>list>qfje
            qfje_node = doc.createElement("qfje")
            qfje_value = doc.createTextNode("25819.6")
            qfje_node.appendChild(qfje_value)
            ZSSbfQsxxGridlb_node.appendChild(qfje_node)

            # response>xfaceTradeDTO>responseDTO>list>zsuuid
            zsuuid_node = doc.createElement("zsuuid")
            zsuuid_value = doc.createTextNode("1507BCB362541EB4A78FE97981C32AB8")
            zsuuid_node.appendChild(zsuuid_value)
            ZSSbfQsxxGridlb_node.appendChild(zsuuid_node)

            # response>xfaceTradeDTO>responseDTO>list>yzpzmxxh
            yzpzmxxh_node = doc.createElement("yzpzmxxh")
            yzpzmxxh_value = doc.createTextNode("3")
            yzpzmxxh_node.appendChild(yzpzmxxh_value)
            ZSSbfQsxxGridlb_node.appendChild(yzpzmxxh_node)

            # response>xfaceTradeDTO>responseDTO>list>jkqx
            jkqx_node = doc.createElement("jkqx")
            jkqx_value = doc.createTextNode("2018-11-30")
            jkqx_node.appendChild(jkqx_value)
            ZSSbfQsxxGridlb_node.appendChild(jkqx_node)

            # response>xfaceTradeDTO>responseDTO>list>pmname
            pmname_node = doc.createElement("pmname")
            pmname_value = doc.createTextNode("机关事业单位基本养老保险费收入（单位缴纳）")
            pmname_node.appendChild(pmname_value)
            ZSSbfQsxxGridlb_node.appendChild(pmname_node)

            #第二个数据
            ZSSbfQsxxGridlb_node = doc.createElement("ZSSbfQsxxGridlb")
            ZSSbfQsxxGrid_node.appendChild(ZSSbfQsxxGridlb_node)

            # response>xfaceTradeDTO>responseDTO>list>hsjg
            hsjg_node = doc.createElement("hsjg")
            hsjg_value = doc.createTextNode("15203020000")
            hsjg_node.appendChild(hsjg_value)
            ZSSbfQsxxGridlb_node.appendChild(hsjg_node)

            # response>xfaceTradeDTO>responseDTO>list>nsrsbh
            nsrsbh_node = doc.createElement("nsrsbh")
            nsrsbh_value = doc.createTextNode("12520302429400744T")
            nsrsbh_node.appendChild(nsrsbh_value)
            ZSSbfQsxxGridlb_node.appendChild(nsrsbh_node)

            # response>xfaceTradeDTO>responseDTO>list>nsrmc
            nsrmc_node = doc.createElement("nsrmc")
            nsrmc_value = doc.createTextNode("遵义市老城小学")
            nsrmc_node.appendChild(nsrmc_value)
            ZSSbfQsxxGridlb_node.appendChild(nsrmc_node)

            # response>xfaceTradeDTO>responseDTO>list>djxh
            djxh_node = doc.createElement("djxh")
            djxh_value = doc.createTextNode("10215203000000557146")
            djxh_node.appendChild(djxh_value)
            ZSSbfQsxxGridlb_node.appendChild(djxh_node)

            # response>xfaceTradeDTO>responseDTO>list>yzpzxh
            yzpzxh_node = doc.createElement("yzpzxh")
            yzpzxh_value = doc.createTextNode("10015218000000002931")
            yzpzxh_node.appendChild(yzpzxh_value)
            ZSSbfQsxxGridlb_node.appendChild(yzpzxh_node)

            # response>xfaceTradeDTO>responseDTO>list>sbbm
            sbbm_node = doc.createElement("sbbm")
            sbbm_value = doc.createTextNode("52030222961")
            sbbm_node.appendChild(sbbm_value)
            ZSSbfQsxxGridlb_node.appendChild(sbbm_node)

            # response>xfaceTradeDTO>responseDTO>list>sbjbjgDm
            sbjbjgDm_node = doc.createElement("sbjbjgDm")
            sbjbjgDm_value = doc.createTextNode("5200002202520302")
            sbjbjgDm_node.appendChild(sbjbjgDm_value)
            ZSSbfQsxxGridlb_node.appendChild(sbjbjgDm_node)

            # response>xfaceTradeDTO>responseDTO>list>skssqq
            skssqq_node = doc.createElement("skssqq")
            skssqq_value = doc.createTextNode("2018-11-01")
            skssqq_node.appendChild(skssqq_value)
            ZSSbfQsxxGridlb_node.appendChild(skssqq_node)

            # response>xfaceTradeDTO>responseDTO>list>skssqz
            skssqz_node = doc.createElement("skssqz")
            skssqz_value = doc.createTextNode("2018-11-30")
            skssqz_node.appendChild(skssqz_value)
            ZSSbfQsxxGridlb_node.appendChild(skssqz_node)

            # response>xfaceTradeDTO>responseDTO>list>zsxmDm
            zsxmDm_node = doc.createElement("zsxmDm")
            zsxmDm_value = doc.createTextNode("10211")
            zsxmDm_node.appendChild(zsxmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(zsxmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>zspmDm
            zspmDm_node = doc.createElement("zspmDm")
            zspmDm_value = doc.createTextNode("102110102")
            zspmDm_node.appendChild(zspmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(zspmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>yskmDm
            yskmDm_node = doc.createElement("yskmDm")
            yskmDm_value = doc.createTextNode("1021101")
            yskmDm_node.appendChild(yskmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(yskmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>ysfpblDm
            ysfpblDm_node = doc.createElement("ysfpblDm")
            ysfpblDm_value = doc.createTextNode("15240001")
            ysfpblDm_node.appendChild(ysfpblDm_value)
            ZSSbfQsxxGridlb_node.appendChild(ysfpblDm_node)

            # response>xfaceTradeDTO>responseDTO>list>skgkDm
            skgkDm_node = doc.createElement("skgkDm")
            skgkDm_value = doc.createTextNode("1520302001")
            skgkDm_node.appendChild(skgkDm_value)
            ZSSbfQsxxGridlb_node.appendChild(skgkDm_node)

            # response>xfaceTradeDTO>responseDTO>list>qfje
            qfje_node = doc.createElement("qfje")
            qfje_value = doc.createTextNode("10327.84")
            qfje_node.appendChild(qfje_value)
            ZSSbfQsxxGridlb_node.appendChild(qfje_node)

            # response>xfaceTradeDTO>responseDTO>list>zsuuid
            zsuuid_node = doc.createElement("zsuuid")
            zsuuid_value = doc.createTextNode("64BD1FEC29A5EC076C30F082CACC5C6A")
            zsuuid_node.appendChild(zsuuid_value)
            ZSSbfQsxxGridlb_node.appendChild(zsuuid_node)

            # response>xfaceTradeDTO>responseDTO>list>yzpzmxxh
            yzpzmxxh_node = doc.createElement("yzpzmxxh")
            yzpzmxxh_value = doc.createTextNode("4")
            yzpzmxxh_node.appendChild(yzpzmxxh_value)
            ZSSbfQsxxGridlb_node.appendChild(yzpzmxxh_node)

            # response>xfaceTradeDTO>responseDTO>list>jkqx
            jkqx_node = doc.createElement("jkqx")
            jkqx_value = doc.createTextNode("2018-11-30")
            jkqx_node.appendChild(jkqx_value)
            ZSSbfQsxxGridlb_node.appendChild(jkqx_node)

            # response>xfaceTradeDTO>responseDTO>list>pmname
            pmname_node = doc.createElement("pmname")
            pmname_value = doc.createTextNode("机关事业单位基本养老保险费收入（单位缴纳）")
            pmname_node.appendChild(pmname_value)
            ZSSbfQsxxGridlb_node.appendChild(pmname_node)

            #第三个数据
            ZSSbfQsxxGridlb_node = doc.createElement("ZSSbfQsxxGridlb")
            ZSSbfQsxxGrid_node.appendChild(ZSSbfQsxxGridlb_node)

            # response>xfaceTradeDTO>responseDTO>list>hsjg
            hsjg_node = doc.createElement("hsjg")
            hsjg_value = doc.createTextNode("15203020000")
            hsjg_node.appendChild(hsjg_value)
            ZSSbfQsxxGridlb_node.appendChild(hsjg_node)

            # response>xfaceTradeDTO>responseDTO>list>nsrsbh
            nsrsbh_node = doc.createElement("nsrsbh")
            nsrsbh_value = doc.createTextNode("12520302429400744T")
            nsrsbh_node.appendChild(nsrsbh_value)
            ZSSbfQsxxGridlb_node.appendChild(nsrsbh_node)

            # response>xfaceTradeDTO>responseDTO>list>nsrmc
            nsrmc_node = doc.createElement("nsrmc")
            nsrmc_value = doc.createTextNode("遵义市老城小学")
            nsrmc_node.appendChild(nsrmc_value)
            ZSSbfQsxxGridlb_node.appendChild(nsrmc_node)

            # response>xfaceTradeDTO>responseDTO>list>djxh
            djxh_node = doc.createElement("djxh")
            djxh_value = doc.createTextNode("10215203000000557146")
            djxh_node.appendChild(djxh_value)
            ZSSbfQsxxGridlb_node.appendChild(djxh_node)

            # response>xfaceTradeDTO>responseDTO>list>yzpzxh
            yzpzxh_node = doc.createElement("yzpzxh")
            yzpzxh_value = doc.createTextNode("10015218000000002931")
            yzpzxh_node.appendChild(yzpzxh_value)
            ZSSbfQsxxGridlb_node.appendChild(yzpzxh_node)

            # response>xfaceTradeDTO>responseDTO>list>sbbm
            sbbm_node = doc.createElement("sbbm")
            sbbm_value = doc.createTextNode("52030222961")
            sbbm_node.appendChild(sbbm_value)
            ZSSbfQsxxGridlb_node.appendChild(sbbm_node)

            # response>xfaceTradeDTO>responseDTO>list>sbjbjgDm
            sbjbjgDm_node = doc.createElement("sbjbjgDm")
            sbjbjgDm_value = doc.createTextNode("5200002202520302")
            sbjbjgDm_node.appendChild(sbjbjgDm_value)
            ZSSbfQsxxGridlb_node.appendChild(sbjbjgDm_node)

            # response>xfaceTradeDTO>responseDTO>list>skssqq
            skssqq_node = doc.createElement("skssqq")
            skssqq_value = doc.createTextNode("2018-11-01")
            skssqq_node.appendChild(skssqq_value)
            ZSSbfQsxxGridlb_node.appendChild(skssqq_node)

            # response>xfaceTradeDTO>responseDTO>list>skssqz
            skssqz_node = doc.createElement("skssqz")
            skssqz_value = doc.createTextNode("2018-11-30")
            skssqz_node.appendChild(skssqz_value)
            ZSSbfQsxxGridlb_node.appendChild(skssqz_node)

            # response>xfaceTradeDTO>responseDTO>list>zsxmDm
            zsxmDm_node = doc.createElement("zsxmDm")
            zsxmDm_value = doc.createTextNode("10291")
            zsxmDm_node.appendChild(zsxmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(zsxmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>zspmDm
            zspmDm_node = doc.createElement("zspmDm")
            zspmDm_value = doc.createTextNode("102910002")
            zspmDm_node.appendChild(zspmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(zspmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>yskmDm
            yskmDm_node = doc.createElement("yskmDm")
            yskmDm_value = doc.createTextNode("102119902")
            yskmDm_node.appendChild(yskmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(yskmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>ysfpblDm
            ysfpblDm_node = doc.createElement("ysfpblDm")
            ysfpblDm_value = doc.createTextNode("15240001")
            ysfpblDm_node.appendChild(ysfpblDm_value)
            ZSSbfQsxxGridlb_node.appendChild(ysfpblDm_node)

            # response>xfaceTradeDTO>responseDTO>list>skgkDm
            skgkDm_node = doc.createElement("skgkDm")
            skgkDm_value = doc.createTextNode("1520302001")
            skgkDm_node.appendChild(skgkDm_value)
            ZSSbfQsxxGridlb_node.appendChild(skgkDm_node)

            # response>xfaceTradeDTO>responseDTO>list>qfje
            qfje_node = doc.createElement("qfje")
            qfje_value = doc.createTextNode("5163.92")
            qfje_node.appendChild(qfje_value)
            ZSSbfQsxxGridlb_node.appendChild(qfje_node)

            # response>xfaceTradeDTO>responseDTO>list>zsuuid
            zsuuid_node = doc.createElement("zsuuid")
            zsuuid_value = doc.createTextNode("44708020DF555DD59D2065196E78429C")
            zsuuid_node.appendChild(zsuuid_value)
            ZSSbfQsxxGridlb_node.appendChild(zsuuid_node)

            # response>xfaceTradeDTO>responseDTO>list>yzpzmxxh
            yzpzmxxh_node = doc.createElement("yzpzmxxh")
            yzpzmxxh_value = doc.createTextNode("1")
            yzpzmxxh_node.appendChild(yzpzmxxh_value)
            ZSSbfQsxxGridlb_node.appendChild(yzpzmxxh_node)

            # response>xfaceTradeDTO>responseDTO>list>jkqx
            jkqx_node = doc.createElement("jkqx")
            jkqx_value = doc.createTextNode("2018-11-30")
            jkqx_node.appendChild(jkqx_value)
            ZSSbfQsxxGridlb_node.appendChild(jkqx_node)

            # response>xfaceTradeDTO>responseDTO>list>pmname
            pmname_node = doc.createElement("pmname")
            pmname_value = doc.createTextNode("机关事业单位职业年金（个人缴费）")
            pmname_node.appendChild(pmname_value)
            ZSSbfQsxxGridlb_node.appendChild(pmname_node)

            #第四个数据
            ZSSbfQsxxGridlb_node = doc.createElement("ZSSbfQsxxGridlb")
            ZSSbfQsxxGrid_node.appendChild(ZSSbfQsxxGridlb_node)

            # response>xfaceTradeDTO>responseDTO>list>hsjg
            hsjg_node = doc.createElement("hsjg")
            hsjg_value = doc.createTextNode("15203020000")
            hsjg_node.appendChild(hsjg_value)
            ZSSbfQsxxGridlb_node.appendChild(hsjg_node)

            # response>xfaceTradeDTO>responseDTO>list>nsrsbh
            nsrsbh_node = doc.createElement("nsrsbh")
            nsrsbh_value = doc.createTextNode("12520302429400744T")
            nsrsbh_node.appendChild(nsrsbh_value)
            ZSSbfQsxxGridlb_node.appendChild(nsrsbh_node)

            # response>xfaceTradeDTO>responseDTO>list>nsrmc
            nsrmc_node = doc.createElement("nsrmc")
            nsrmc_value = doc.createTextNode("遵义市老城小学")
            nsrmc_node.appendChild(nsrmc_value)
            ZSSbfQsxxGridlb_node.appendChild(nsrmc_node)

            # response>xfaceTradeDTO>responseDTO>list>djxh
            djxh_node = doc.createElement("djxh")
            djxh_value = doc.createTextNode("10215203000000557146")
            djxh_node.appendChild(djxh_value)
            ZSSbfQsxxGridlb_node.appendChild(djxh_node)

            # response>xfaceTradeDTO>responseDTO>list>yzpzxh
            yzpzxh_node = doc.createElement("yzpzxh")
            yzpzxh_value = doc.createTextNode("10015218000000002931")
            yzpzxh_node.appendChild(yzpzxh_value)
            ZSSbfQsxxGridlb_node.appendChild(yzpzxh_node)

            # response>xfaceTradeDTO>responseDTO>list>sbbm
            sbbm_node = doc.createElement("sbbm")
            sbbm_value = doc.createTextNode("52030222961")
            sbbm_node.appendChild(sbbm_value)
            ZSSbfQsxxGridlb_node.appendChild(sbbm_node)

            # response>xfaceTradeDTO>responseDTO>list>sbjbjgDm
            sbjbjgDm_node = doc.createElement("sbjbjgDm")
            sbjbjgDm_value = doc.createTextNode("5200002202520302")
            sbjbjgDm_node.appendChild(sbjbjgDm_value)
            ZSSbfQsxxGridlb_node.appendChild(sbjbjgDm_node)

            # response>xfaceTradeDTO>responseDTO>list>skssqq
            skssqq_node = doc.createElement("skssqq")
            skssqq_value = doc.createTextNode("2018-11-01")
            skssqq_node.appendChild(skssqq_value)
            ZSSbfQsxxGridlb_node.appendChild(skssqq_node)

            # response>xfaceTradeDTO>responseDTO>list>skssqz
            skssqz_node = doc.createElement("skssqz")
            skssqz_value = doc.createTextNode("2018-11-30")
            skssqz_node.appendChild(skssqz_value)
            ZSSbfQsxxGridlb_node.appendChild(skssqz_node)

            # response>xfaceTradeDTO>responseDTO>list>zsxmDm
            zsxmDm_node = doc.createElement("zsxmDm")
            zsxmDm_value = doc.createTextNode("10291")
            zsxmDm_node.appendChild(zsxmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(zsxmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>zspmDm
            zspmDm_node = doc.createElement("zspmDm")
            zspmDm_value = doc.createTextNode("102910001")
            zspmDm_node.appendChild(zspmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(zspmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>yskmDm
            yskmDm_node = doc.createElement("yskmDm")
            yskmDm_value = doc.createTextNode("102119902")
            yskmDm_node.appendChild(yskmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(yskmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>ysfpblDm
            ysfpblDm_node = doc.createElement("ysfpblDm")
            ysfpblDm_value = doc.createTextNode("15240001")
            ysfpblDm_node.appendChild(ysfpblDm_value)
            ZSSbfQsxxGridlb_node.appendChild(ysfpblDm_node)

            # response>xfaceTradeDTO>responseDTO>list>skgkDm
            skgkDm_node = doc.createElement("skgkDm")
            skgkDm_value = doc.createTextNode("1520302001")
            skgkDm_node.appendChild(skgkDm_value)
            ZSSbfQsxxGridlb_node.appendChild(skgkDm_node)

            # response>xfaceTradeDTO>responseDTO>list>qfje
            qfje_node = doc.createElement("qfje")
            qfje_value = doc.createTextNode("10327.84")
            qfje_node.appendChild(qfje_value)
            ZSSbfQsxxGridlb_node.appendChild(qfje_node)

            # response>xfaceTradeDTO>responseDTO>list>zsuuid
            zsuuid_node = doc.createElement("zsuuid")
            zsuuid_value = doc.createTextNode("EE50E3F700AC53A55140CBDC68FBA012")
            zsuuid_node.appendChild(zsuuid_value)
            ZSSbfQsxxGridlb_node.appendChild(zsuuid_node)

            # response>xfaceTradeDTO>responseDTO>list>yzpzmxxh
            yzpzmxxh_node = doc.createElement("yzpzmxxh")
            yzpzmxxh_value = doc.createTextNode("2")
            yzpzmxxh_node.appendChild(yzpzmxxh_value)
            ZSSbfQsxxGridlb_node.appendChild(yzpzmxxh_node)

            # response>xfaceTradeDTO>responseDTO>list>jkqx
            jkqx_node = doc.createElement("jkqx")
            jkqx_value = doc.createTextNode("2018-11-30")
            jkqx_node.appendChild(jkqx_value)
            ZSSbfQsxxGridlb_node.appendChild(jkqx_node)

            # response>xfaceTradeDTO>responseDTO>list>pmname
            pmname_node = doc.createElement("pmname")
            pmname_value = doc.createTextNode("机关事业单位职业年金（单位缴费）")
            pmname_node.appendChild(pmname_value)
            ZSSbfQsxxGridlb_node.appendChild(pmname_node)

            #第五个数据
            ZSSbfQsxxGridlb_node = doc.createElement("ZSSbfQsxxGridlb")
            ZSSbfQsxxGrid_node.appendChild(ZSSbfQsxxGridlb_node)

            # response>xfaceTradeDTO>responseDTO>list>hsjg
            hsjg_node = doc.createElement("hsjg")
            hsjg_value = doc.createTextNode("15203020000")
            hsjg_node.appendChild(hsjg_value)
            ZSSbfQsxxGridlb_node.appendChild(hsjg_node)

            # response>xfaceTradeDTO>responseDTO>list>nsrsbh
            nsrsbh_node = doc.createElement("nsrsbh")
            nsrsbh_value = doc.createTextNode("12520302429400744T")
            nsrsbh_node.appendChild(nsrsbh_value)
            ZSSbfQsxxGridlb_node.appendChild(nsrsbh_node)

            # response>xfaceTradeDTO>responseDTO>list>nsrmc
            nsrmc_node = doc.createElement("nsrmc")
            nsrmc_value = doc.createTextNode("遵义市老城小学")
            nsrmc_node.appendChild(nsrmc_value)
            ZSSbfQsxxGridlb_node.appendChild(nsrmc_node)

            # response>xfaceTradeDTO>responseDTO>list>djxh
            djxh_node = doc.createElement("djxh")
            djxh_value = doc.createTextNode("10215203000000557146")
            djxh_node.appendChild(djxh_value)
            ZSSbfQsxxGridlb_node.appendChild(djxh_node)

            # response>xfaceTradeDTO>responseDTO>list>yzpzxh
            yzpzxh_node = doc.createElement("yzpzxh")
            yzpzxh_value = doc.createTextNode("10015218000000002930")
            yzpzxh_node.appendChild(yzpzxh_value)
            ZSSbfQsxxGridlb_node.appendChild(yzpzxh_node)

            # response>xfaceTradeDTO>responseDTO>list>sbbm
            sbbm_node = doc.createElement("sbbm")
            sbbm_value = doc.createTextNode("52030222961")
            sbbm_node.appendChild(sbbm_value)
            ZSSbfQsxxGridlb_node.appendChild(sbbm_node)

            # response>xfaceTradeDTO>responseDTO>list>sbjbjgDm
            sbjbjgDm_node = doc.createElement("sbjbjgDm")
            sbjbjgDm_value = doc.createTextNode("5200002202520302")
            sbjbjgDm_node.appendChild(sbjbjgDm_value)
            ZSSbfQsxxGridlb_node.appendChild(sbjbjgDm_node)

            # response>xfaceTradeDTO>responseDTO>list>skssqq
            skssqq_node = doc.createElement("skssqq")
            skssqq_value = doc.createTextNode("2018-10-01")
            skssqq_node.appendChild(skssqq_value)
            ZSSbfQsxxGridlb_node.appendChild(skssqq_node)

            # response>xfaceTradeDTO>responseDTO>list>skssqz
            skssqz_node = doc.createElement("skssqz")
            skssqz_value = doc.createTextNode("2018-10-31")
            skssqz_node.appendChild(skssqz_value)
            ZSSbfQsxxGridlb_node.appendChild(skssqz_node)

            # response>xfaceTradeDTO>responseDTO>list>zsxmDm
            zsxmDm_node = doc.createElement("zsxmDm")
            zsxmDm_value = doc.createTextNode("10291")
            zsxmDm_node.appendChild(zsxmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(zsxmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>zspmDm
            zspmDm_node = doc.createElement("zspmDm")
            zspmDm_value = doc.createTextNode("102910002")
            zspmDm_node.appendChild(zspmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(zspmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>yskmDm
            yskmDm_node = doc.createElement("yskmDm")
            yskmDm_value = doc.createTextNode("102119902")
            yskmDm_node.appendChild(yskmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(yskmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>ysfpblDm
            ysfpblDm_node = doc.createElement("ysfpblDm")
            ysfpblDm_value = doc.createTextNode("15240001")
            ysfpblDm_node.appendChild(ysfpblDm_value)
            ZSSbfQsxxGridlb_node.appendChild(ysfpblDm_node)

            # response>xfaceTradeDTO>responseDTO>list>skgkDm
            skgkDm_node = doc.createElement("skgkDm")
            skgkDm_value = doc.createTextNode("1520302001")
            skgkDm_node.appendChild(skgkDm_value)
            ZSSbfQsxxGridlb_node.appendChild(skgkDm_node)

            # response>xfaceTradeDTO>responseDTO>list>qfje
            qfje_node = doc.createElement("qfje")
            qfje_value = doc.createTextNode("5163.92")
            qfje_node.appendChild(qfje_value)
            ZSSbfQsxxGridlb_node.appendChild(qfje_node)

            # response>xfaceTradeDTO>responseDTO>list>zsuuid
            zsuuid_node = doc.createElement("zsuuid")
            zsuuid_value = doc.createTextNode("F404784FC8CFE899064D6FB61AE8DB9F")
            zsuuid_node.appendChild(zsuuid_value)
            ZSSbfQsxxGridlb_node.appendChild(zsuuid_node)

            # response>xfaceTradeDTO>responseDTO>list>yzpzmxxh
            yzpzmxxh_node = doc.createElement("yzpzmxxh")
            yzpzmxxh_value = doc.createTextNode("1")
            yzpzmxxh_node.appendChild(yzpzmxxh_value)
            ZSSbfQsxxGridlb_node.appendChild(yzpzmxxh_node)

            # response>xfaceTradeDTO>responseDTO>list>jkqx
            jkqx_node = doc.createElement("jkqx")
            jkqx_value = doc.createTextNode("2018-10-31")
            jkqx_node.appendChild(jkqx_value)
            ZSSbfQsxxGridlb_node.appendChild(jkqx_node)

            # response>xfaceTradeDTO>responseDTO>list>pmname
            pmname_node = doc.createElement("pmname")
            pmname_value = doc.createTextNode("机关事业单位职业年金（个人缴费）")
            pmname_node.appendChild(pmname_value)
            ZSSbfQsxxGridlb_node.appendChild(pmname_node)

            #第六个数据
            ZSSbfQsxxGridlb_node = doc.createElement("ZSSbfQsxxGridlb")
            ZSSbfQsxxGrid_node.appendChild(ZSSbfQsxxGridlb_node)

            # response>xfaceTradeDTO>responseDTO>list>hsjg
            hsjg_node = doc.createElement("hsjg")
            hsjg_value = doc.createTextNode("15203020000")
            hsjg_node.appendChild(hsjg_value)
            ZSSbfQsxxGridlb_node.appendChild(hsjg_node)

            # response>xfaceTradeDTO>responseDTO>list>nsrsbh
            nsrsbh_node = doc.createElement("nsrsbh")
            nsrsbh_value = doc.createTextNode("12520302429400744T")
            nsrsbh_node.appendChild(nsrsbh_value)
            ZSSbfQsxxGridlb_node.appendChild(nsrsbh_node)

            # response>xfaceTradeDTO>responseDTO>list>nsrmc
            nsrmc_node = doc.createElement("nsrmc")
            nsrmc_value = doc.createTextNode("遵义市老城小学")
            nsrmc_node.appendChild(nsrmc_value)
            ZSSbfQsxxGridlb_node.appendChild(nsrmc_node)

            # response>xfaceTradeDTO>responseDTO>list>djxh
            djxh_node = doc.createElement("djxh")
            djxh_value = doc.createTextNode("10215203000000557146")
            djxh_node.appendChild(djxh_value)
            ZSSbfQsxxGridlb_node.appendChild(djxh_node)

            # response>xfaceTradeDTO>responseDTO>list>yzpzxh
            yzpzxh_node = doc.createElement("yzpzxh")
            yzpzxh_value = doc.createTextNode("10015218000000002930")
            yzpzxh_node.appendChild(yzpzxh_value)
            ZSSbfQsxxGridlb_node.appendChild(yzpzxh_node)

            # response>xfaceTradeDTO>responseDTO>list>sbbm
            sbbm_node = doc.createElement("sbbm")
            sbbm_value = doc.createTextNode("52030222961")
            sbbm_node.appendChild(sbbm_value)
            ZSSbfQsxxGridlb_node.appendChild(sbbm_node)

            # response>xfaceTradeDTO>responseDTO>list>sbjbjgDm
            sbjbjgDm_node = doc.createElement("sbjbjgDm")
            sbjbjgDm_value = doc.createTextNode("5200002202520302")
            sbjbjgDm_node.appendChild(sbjbjgDm_value)
            ZSSbfQsxxGridlb_node.appendChild(sbjbjgDm_node)

            # response>xfaceTradeDTO>responseDTO>list>skssqq
            skssqq_node = doc.createElement("skssqq")
            skssqq_value = doc.createTextNode("2018-10-01")
            skssqq_node.appendChild(skssqq_value)
            ZSSbfQsxxGridlb_node.appendChild(skssqq_node)

            # response>xfaceTradeDTO>responseDTO>list>skssqz
            skssqz_node = doc.createElement("skssqz")
            skssqz_value = doc.createTextNode("2018-10-31")
            skssqz_node.appendChild(skssqz_value)
            ZSSbfQsxxGridlb_node.appendChild(skssqz_node)

            # response>xfaceTradeDTO>responseDTO>list>zsxmDm
            zsxmDm_node = doc.createElement("zsxmDm")
            zsxmDm_value = doc.createTextNode("10291")
            zsxmDm_node.appendChild(zsxmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(zsxmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>zspmDm
            zspmDm_node = doc.createElement("zspmDm")
            zspmDm_value = doc.createTextNode("102910001")
            zspmDm_node.appendChild(zspmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(zspmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>yskmDm
            yskmDm_node = doc.createElement("yskmDm")
            yskmDm_value = doc.createTextNode("102119902")
            yskmDm_node.appendChild(yskmDm_value)
            ZSSbfQsxxGridlb_node.appendChild(yskmDm_node)

            # response>xfaceTradeDTO>responseDTO>list>ysfpblDm
            ysfpblDm_node = doc.createElement("ysfpblDm")
            ysfpblDm_value = doc.createTextNode("15240001")
            ysfpblDm_node.appendChild(ysfpblDm_value)
            ZSSbfQsxxGridlb_node.appendChild(ysfpblDm_node)

            # response>xfaceTradeDTO>responseDTO>list>skgkDm
            skgkDm_node = doc.createElement("skgkDm")
            skgkDm_value = doc.createTextNode("1520302001")
            skgkDm_node.appendChild(skgkDm_value)
            ZSSbfQsxxGridlb_node.appendChild(skgkDm_node)

            # response>xfaceTradeDTO>responseDTO>list>qfje
            qfje_node = doc.createElement("qfje")
            qfje_value = doc.createTextNode("10327.84")
            qfje_node.appendChild(qfje_value)
            ZSSbfQsxxGridlb_node.appendChild(qfje_node)

            # response>xfaceTradeDTO>responseDTO>list>zsuuid
            zsuuid_node = doc.createElement("zsuuid")
            zsuuid_value = doc.createTextNode("FDE4AD6557FE24FB19691B25162A44C1")
            zsuuid_node.appendChild(zsuuid_value)
            ZSSbfQsxxGridlb_node.appendChild(zsuuid_node)

            # response>xfaceTradeDTO>responseDTO>list>yzpzmxxh
            yzpzmxxh_node = doc.createElement("yzpzmxxh")
            yzpzmxxh_value = doc.createTextNode("2")
            yzpzmxxh_node.appendChild(yzpzmxxh_value)
            ZSSbfQsxxGridlb_node.appendChild(yzpzmxxh_node)

            # response>xfaceTradeDTO>responseDTO>list>jkqx
            jkqx_node = doc.createElement("jkqx")
            jkqx_value = doc.createTextNode("2018-10-31")
            jkqx_node.appendChild(jkqx_value)
            ZSSbfQsxxGridlb_node.appendChild(jkqx_node)

            # response>xfaceTradeDTO>responseDTO>list>pmname
            pmname_node = doc.createElement("pmname")
            pmname_value = doc.createTextNode("机关事业单位职业年金（单位缴费）")
            pmname_node.appendChild(pmname_value)
            ZSSbfQsxxGridlb_node.appendChild(pmname_node)





    #实现银行端社保费单位打印缴款凭证功能。任何渠道、柜员都可以发起
    elif serviceCode == "712308":
        # 检查必填关键字段 wdmc ywbh djxh yzpzxh mxbs yzpzmxxh zsuuid kkje znjtsjscs
        if "yybs" in dict.keys()  and "wdmc" in dict.keys() and "ywbh" in dict.keys() and "djxh" in dict.keys() \
                and "yzpzxh" in dict.keys() and "mxbs" in dict.keys() and "yzpzmxxh" in dict.keys() and "zsuuid" in dict.keys() \
                and "kkje" in dict.keys() and "znjtsjscs" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0  and len(dict['wdmc']) != 0 and len(dict['ywbh']) != 0 and len(dict['djxh']) != 0 \
                    and len(dict['yzpzxh']) != 0 and len(dict['mxbs']) != 0 and len(dict['yzpzmxxh']) != 0 and len(dict['zsuuid']) != 0 \
                    and len(dict['kkje']) != 0 and len(dict['znjtsjscs']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>reg_order
        reg_order_node = doc.createElement("reg_order")
        reg_order_value = doc.createTextNode("20125200910013638666")
        if not serviceCodeFlag:
            reg_order_value = doc.createTextNode("")
        reg_order_node.appendChild(reg_order_value)
        xresponseDTO_node.appendChild(reg_order_node)

        # response>xfaceTradeDTO>responseDTO>det_num
        det_num_node = doc.createElement("det_num")
        det_num_value = doc.createTextNode("1")
        if not serviceCodeFlag:
            det_num_value = doc.createTextNode("")
        det_num_node.appendChild(det_num_value)
        xresponseDTO_node.appendChild(det_num_node)


        if serviceCodeFlag:
            # response>xfaceTradeDTO>responseDTO>insuranceInfo
            insuranceInfo_node = doc.createElement("insuranceInfo")
            xresponseDTO_node.appendChild(insuranceInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>social_sec_branch
            social_sec_branch_node = doc.createElement("social_sec_branch")
            social_sec_branch_value = doc.createTextNode("5200000201522731")
            social_sec_branch_node.appendChild(social_sec_branch_value)
            insuranceInfo_node.appendChild(social_sec_branch_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>user_id
            user_id_node = doc.createElement("user_id")
            user_id_value = doc.createTextNode("28258950")
            user_id_node.appendChild(user_id_value)
            insuranceInfo_node.appendChild(user_id_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_org_code
            tax_org_code_node = doc.createElement("tax_org_code")
            tax_org_code_value = doc.createTextNode("15227310000")
            tax_org_code_node.appendChild(tax_org_code_value)
            insuranceInfo_node.appendChild(tax_org_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_type
            pay_type_node = doc.createElement("pay_type")
            pay_type_value = doc.createTextNode("0")
            pay_type_node.appendChild(pay_type_value)
            insuranceInfo_node.appendChild(pay_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>sub_det_num
            sub_det_num_node = doc.createElement("sub_det_num")
            sub_det_num_value = doc.createTextNode("1")
            sub_det_num_node.appendChild(sub_det_num_value)
            insuranceInfo_node.appendChild(sub_det_num_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo
            insuranceTypeInfo_node = doc.createElement("insuranceTypeInfo")
            insuranceInfo_node.appendChild(insuranceTypeInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>begin_date
            begin_date_node = doc.createElement("begin_date")
            begin_date_value = doc.createTextNode("201210")
            begin_date_node.appendChild(begin_date_value)
            insuranceTypeInfo_node.appendChild(begin_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>end_date
            end_date_node = doc.createElement("end_date")
            end_date_value = doc.createTextNode("999912")
            end_date_node.appendChild(end_date_value)
            insuranceTypeInfo_node.appendChild(end_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>project_code
            project_code_node = doc.createElement("project_code")
            project_code_value = doc.createTextNode("10210")
            project_code_node.appendChild(project_code_value)
            insuranceTypeInfo_node.appendChild(project_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>project_name
            project_name_node = doc.createElement("project_name")
            project_name_value = doc.createTextNode("城乡居民基本养老保险费")
            project_name_node.appendChild(project_name_value)
            insuranceTypeInfo_node.appendChild(project_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>item_code
            item_code_node = doc.createElement("item_code")
            item_code_value = doc.createTextNode("102100100")
            item_code_node.appendChild(item_code_value)
            insuranceTypeInfo_node.appendChild(item_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>item_name
            item_name_node = doc.createElement("item_name")
            item_name_value = doc.createTextNode("城乡居民基本养老保险费")
            item_name_node.appendChild(item_name_value)
            insuranceTypeInfo_node.appendChild(item_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>sub_item_code
            sub_item_code_node = doc.createElement("sub_item_code")
            sub_item_code_value = doc.createTextNode("000000000")
            sub_item_code_node.appendChild(sub_item_code_value)
            insuranceTypeInfo_node.appendChild(sub_item_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>sub_item_name
            sub_item_name_node = doc.createElement("sub_item_name")
            sub_item_name_value = doc.createTextNode("000000000")
            sub_item_name_node.appendChild(sub_item_name_value)
            insuranceTypeInfo_node.appendChild(sub_item_name_node)

    #实现行内渠道到中间业务征收机构代码与名称查询功能
    elif serviceCode == "712314":
        # 检查必填关键字段 wdmc ywbh intbankcd
        if "yybs" in dict.keys()  and "wdmc" in dict.keys() and "ywbh" in dict.keys() and "taxorgcode" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0  and len(dict['wdmc']) != 0 and len(dict['ywbh']) != 0 and len(dict['taxorgcode']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>taxorgname
        taxorgname_node = doc.createElement("taxorgname")
        taxorgname_value = doc.createTextNode("安顺市平坝县地方税务局")
        if not serviceCodeFlag:
            taxorgname_value = doc.createTextNode("")
        taxorgname_node.appendChild(taxorgname_value)
        xresponseDTO_node.appendChild(taxorgname_node)

        # response>xfaceTradeDTO>responseDTO>trecode
        trecode_node = doc.createElement("trecode")
        trecode_value = doc.createTextNode("2303000000")
        if not serviceCodeFlag:
            trecode_value = doc.createTextNode("")
        trecode_node.appendChild(trecode_value)
        xresponseDTO_node.appendChild(trecode_node)

        # response>xfaceTradeDTO>responseDTO>trename
        trename_node = doc.createElement("trename")
        trename_value = doc.createTextNode("国家金库安顺市中心支库")
        if not serviceCodeFlag:
            trename_value = doc.createTextNode("")
        trename_node.appendChild(trename_value)
        xresponseDTO_node.appendChild(trename_node)

        # response>xfaceTradeDTO>responseDTO>payeeacct
        payeeacct_node = doc.createElement("payeeacct")
        payeeacct_value = doc.createTextNode("230300000003371002")
        if not serviceCodeFlag:
            payeeacct_value = doc.createTextNode("")
        payeeacct_node.appendChild(payeeacct_value)
        xresponseDTO_node.appendChild(payeeacct_node)

        # response>xfaceTradeDTO>responseDTO>payeename
        payeename_node = doc.createElement("payeename")
        payeename_value = doc.createTextNode("暂收款")
        if not serviceCodeFlag:
            payeename_value = doc.createTextNode("")
        payeename_node.appendChild(payeename_value)
        xresponseDTO_node.appendChild(payeename_node)

    #实现行内渠道到中间业务TIPS前置查询机构与网点开户行信息的功能
    elif serviceCode == "712315":
        # 检查必填关键字段 wdmc ywbh intbankcd
        if "yybs" in dict.keys()  and "wdmc" in dict.keys() and "ywbh" in dict.keys() and "intbankcd" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0  and len(dict['wdmc']) != 0 and len(dict['ywbh']) != 0 and len(dict['intbankcd']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>fixdbnkcd
        fixdbnkcd_node = doc.createElement("fixdbnkcd")
        fixdbnkcd_value = doc.createTextNode("314702082876")
        if not serviceCodeFlag:
            fixdbnkcd_value = doc.createTextNode("")
        fixdbnkcd_node.appendChild(fixdbnkcd_value)
        xresponseDTO_node.appendChild(fixdbnkcd_node)

        # response>xfaceTradeDTO>responseDTO>bankname
        bankname_node = doc.createElement("bankname")
        bankname_value = doc.createTextNode("六盘水农村商业银行股份有限公司")
        if not serviceCodeFlag:
            bankname_value = doc.createTextNode("")
        bankname_node.appendChild(bankname_value)
        xresponseDTO_node.appendChild(bankname_node)

        # response>xfaceTradeDTO>responseDTO>paybkcode
        paybkcode_node = doc.createElement("paybkcode")
        paybkcode_value = doc.createTextNode("314702082876")
        if not serviceCodeFlag:
            paybkcode_value = doc.createTextNode("")
        paybkcode_node.appendChild(paybkcode_value)
        xresponseDTO_node.appendChild(paybkcode_node)

        # response>xfaceTradeDTO>responseDTO>paybkname
        paybkname_node = doc.createElement("paybkname")
        paybkname_value = doc.createTextNode("六盘水农村商业银行股份有限公司")
        if not serviceCodeFlag:
            paybkname_value = doc.createTextNode("")
        paybkname_node.appendChild(paybkname_value)
        xresponseDTO_node.appendChild(paybkname_node)

    #实现行内渠道到中间业务TIPS三方协议验证、撤销、修改、删除功能。
    # （1）已验证、已撤销的协议不可以修改、删除。
    # （2）修改后自动提交验证
    elif serviceCode == "712316":
        # 检查必填关键字段 wdmc ywbh czbz protocolno
        if "yybs" in dict.keys()  and "wdmc" in dict.keys() and "ywbh" in dict.keys() and "czbz" in dict.keys() and "protocolno" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0  and len(dict['wdmc']) != 0 and len(dict['ywbh']) != 0 and len(dict['czbz']) != 0 and len(dict['protocolno']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")


        if serviceCodeFlag:
            # response>xfaceTradeDTO>responseDTO>insuranceInfo
            protocolno_node = doc.createElement("protocolno")
            xresponseDTO_node.appendChild(protocolno_node)

    #实现行内渠道到中间业务TIPS前置查询三方协议明细功能。非省联社管理机构只能查询接收机构是本机构的
    elif serviceCode == "712317":
        # 检查必填关键字段 wdmc ywbh
        if "yybs" in dict.keys()  and "wdmc" in dict.keys() and "ywbh" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0  and len(dict['wdmc']) != 0 and len(dict['ywbh']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>zbs
        zbs_node = doc.createElement("zbs")
        zbs_value = doc.createTextNode("2")
        if not serviceCodeFlag:
            zbs_value = doc.createTextNode("")
        zbs_node.appendChild(zbs_value)
        xresponseDTO_node.appendChild(zbs_node)

        # response>xfaceTradeDTO>responseDTO>jymxs
        jymxs_node = doc.createElement("jymxs")
        jymxs_value = doc.createTextNode("2")
        if not serviceCodeFlag:
            jymxs_value = doc.createTextNode("")
        jymxs_node.appendChild(jymxs_value)
        xresponseDTO_node.appendChild(jymxs_node)


        if serviceCodeFlag:
            #第一个数据
            # response>xfaceTradeDTO>responseDTO>list
            list_node = doc.createElement("list")
            xresponseDTO_node.appendChild(list_node)

            # response>xfaceTradeDTO>responseDTO>list>protocolno
            protocolno_node = doc.createElement("protocolno")
            protocolno_value = doc.createTextNode("2520422000020181200017")
            protocolno_node.appendChild(protocolno_value)
            list_node.appendChild(protocolno_node)

            # response>xfaceTradeDTO>responseDTO>list>taxorgcode
            taxorgcode_node = doc.createElement("taxorgcode")
            taxorgcode_value = doc.createTextNode("25204220000")
            taxorgcode_node.appendChild(taxorgcode_value)
            list_node.appendChild(taxorgcode_node)

            # response>xfaceTradeDTO>responseDTO>list>taxorgname
            taxorgname_node = doc.createElement("taxorgname")
            taxorgname_value = doc.createTextNode("安顺市普定县地方税务局")
            taxorgname_node.appendChild(taxorgname_value)
            list_node.appendChild(taxorgname_node)

            # response>xfaceTradeDTO>responseDTO>list>paybkcode
            paybkcode_node = doc.createElement("paybkcode")
            paybkcode_value = doc.createTextNode("402711832357")
            paybkcode_node.appendChild(paybkcode_value)
            list_node.appendChild(paybkcode_node)

            # response>xfaceTradeDTO>responseDTO>list>paybkname
            paybkname_node = doc.createElement("paybkname")
            paybkname_value = doc.createTextNode("")
            paybkname_node.appendChild(paybkname_value)
            list_node.appendChild(paybkname_node)

            # response>xfaceTradeDTO>responseDTO>list>payacct
            payacct_node = doc.createElement("payacct")
            payacct_value = doc.createTextNode("820000000000860797")
            payacct_node.appendChild(payacct_value)
            list_node.appendChild(payacct_node)

            # response>xfaceTradeDTO>responseDTO>list>taxpaycode
            taxpaycode_node = doc.createElement("taxpaycode")
            taxpaycode_value = doc.createTextNode("91520422MA6DYQ276J")
            taxpaycode_node.appendChild(taxpaycode_value)
            list_node.appendChild(taxpaycode_node)

            # response>xfaceTradeDTO>responseDTO>list>payopbkcode
            payopbkcode_node = doc.createElement("payopbkcode")
            payopbkcode_value = doc.createTextNode("402711834359")
            payopbkcode_node.appendChild(payopbkcode_value)
            list_node.appendChild(payopbkcode_node)

            # response>xfaceTradeDTO>responseDTO>list>payopbkname
            payopbkname_node = doc.createElement("payopbkname")
            payopbkname_value = doc.createTextNode("普定县农村信用合作联社鸡场信用社")
            payopbkname_node.appendChild(payopbkname_value)
            list_node.appendChild(payopbkname_node)

            # response>xfaceTradeDTO>responseDTO>list>taxpayname
            taxpayname_node = doc.createElement("taxpayname")
            taxpayname_value = doc.createTextNode("普定县鸡场坡苗阿朵加工厂")
            taxpayname_node.appendChild(taxpayname_value)
            list_node.appendChild(taxpayname_node)

            # response>xfaceTradeDTO>responseDTO>list>handorgname
            handorgname_node = doc.createElement("handorgname")
            handorgname_value = doc.createTextNode("普定县鸡场坡苗阿朵加工厂")
            handorgname_node.appendChild(handorgname_value)
            list_node.appendChild(handorgname_node)

            # response>xfaceTradeDTO>responseDTO>list>khh
            khh_node = doc.createElement("khh")
            khh_value = doc.createTextNode("")
            khh_node.appendChild(khh_value)
            list_node.appendChild(khh_node)

            # response>xfaceTradeDTO>responseDTO>list>xyzt
            xyzt_node = doc.createElement("xyzt")
            xyzt_value = doc.createTextNode("1")
            xyzt_node.appendChild(xyzt_value)
            list_node.appendChild(xyzt_node)

            # response>xfaceTradeDTO>responseDTO>list>byzd
            byzd_node = doc.createElement("byzd")
            byzd_value = doc.createTextNode("2350012")
            byzd_node.appendChild(byzd_value)
            list_node.appendChild(byzd_node)

            # response>xfaceTradeDTO>responseDTO>list>gxdjrq
            gxdjrq_node = doc.createElement("gxdjrq")
            gxdjrq_value = doc.createTextNode("20181231")
            gxdjrq_node.appendChild(gxdjrq_value)
            list_node.appendChild(gxdjrq_node)

            # response>xfaceTradeDTO>responseDTO>list>djjgdh
            djjgdh_node = doc.createElement("djjgdh")
            djjgdh_value = doc.createTextNode("2350012")
            djjgdh_node.appendChild(djjgdh_value)
            list_node.appendChild(djjgdh_node)

            # response>xfaceTradeDTO>responseDTO>list>djjygy
            djjygy_node = doc.createElement("djjygy")
            djjygy_value = doc.createTextNode("155511")
            djjygy_node.appendChild(djjygy_value)
            list_node.appendChild(djjygy_node)

            # response>xfaceTradeDTO>responseDTO>list>xgrq
            xgrq_node = doc.createElement("xgrq")
            xgrq_value = doc.createTextNode("")
            xgrq_node.appendChild(xgrq_value)
            list_node.appendChild(xgrq_node)

            # response>xfaceTradeDTO>responseDTO>list>xgjgdh
            xgjgdh_node = doc.createElement("xgjgdh")
            xgjgdh_value = doc.createTextNode("")
            xgjgdh_node.appendChild(xgjgdh_value)
            list_node.appendChild(xgjgdh_node)

            # response>xfaceTradeDTO>responseDTO>list>xgjygy
            xgjygy_node = doc.createElement("xgjygy")
            xgjygy_value = doc.createTextNode("")
            xgjygy_node.appendChild(xgjygy_value)
            list_node.appendChild(xgjygy_node)

            # response>xfaceTradeDTO>responseDTO>list>fkzhlx
            fkzhlx_node = doc.createElement("fkzhlx")
            fkzhlx_value = doc.createTextNode("0")
            fkzhlx_node.appendChild(fkzhlx_value)
            list_node.appendChild(fkzhlx_node)

            # response>xfaceTradeDTO>responseDTO>list>djzddh
            djzddh_node = doc.createElement("djzddh")
            djzddh_value = doc.createTextNode("ITLR")
            djzddh_node.appendChild(djzddh_value)
            list_node.appendChild(djzddh_node)

            # response>xfaceTradeDTO>responseDTO>list>xgzddh
            xgzddh_node = doc.createElement("xgzddh")
            xgzddh_value = doc.createTextNode("")
            xgzddh_node.appendChild(xgzddh_value)
            list_node.appendChild(xgzddh_node)

            #第二个数据
            # response>xfaceTradeDTO>responseDTO>list
            list_node = doc.createElement("list")
            xresponseDTO_node.appendChild(list_node)

            # response>xfaceTradeDTO>responseDTO>list>protocolno
            protocolno_node = doc.createElement("protocolno")
            protocolno_value = doc.createTextNode("1520422000020181200017")
            protocolno_node.appendChild(protocolno_value)
            list_node.appendChild(protocolno_node)

            # response>xfaceTradeDTO>responseDTO>list>taxorgcode
            taxorgcode_node = doc.createElement("taxorgcode")
            taxorgcode_value = doc.createTextNode("15204220000")
            taxorgcode_node.appendChild(taxorgcode_value)
            list_node.appendChild(taxorgcode_node)

            # response>xfaceTradeDTO>responseDTO>list>taxorgname
            taxorgname_node = doc.createElement("taxorgname")
            taxorgname_value = doc.createTextNode("安顺市普定县地方税务局")
            taxorgname_node.appendChild(taxorgname_value)
            list_node.appendChild(taxorgname_node)

            # response>xfaceTradeDTO>responseDTO>list>paybkcode
            paybkcode_node = doc.createElement("paybkcode")
            paybkcode_value = doc.createTextNode("402711832357")
            paybkcode_node.appendChild(paybkcode_value)
            list_node.appendChild(paybkcode_node)

            # response>xfaceTradeDTO>responseDTO>list>paybkname
            paybkname_node = doc.createElement("paybkname")
            paybkname_value = doc.createTextNode("")
            paybkname_node.appendChild(paybkname_value)
            list_node.appendChild(paybkname_node)

            # response>xfaceTradeDTO>responseDTO>list>payacct
            payacct_node = doc.createElement("payacct")
            payacct_value = doc.createTextNode("820000000000860797")
            payacct_node.appendChild(payacct_value)
            list_node.appendChild(payacct_node)

            # response>xfaceTradeDTO>responseDTO>list>taxpaycode
            taxpaycode_node = doc.createElement("taxpaycode")
            taxpaycode_value = doc.createTextNode("91520422MA6DYQ276J")
            taxpaycode_node.appendChild(taxpaycode_value)
            list_node.appendChild(taxpaycode_node)

            # response>xfaceTradeDTO>responseDTO>list>payopbkcode
            payopbkcode_node = doc.createElement("payopbkcode")
            payopbkcode_value = doc.createTextNode("402711834359")
            payopbkcode_node.appendChild(payopbkcode_value)
            list_node.appendChild(payopbkcode_node)

            # response>xfaceTradeDTO>responseDTO>list>payopbkname
            payopbkname_node = doc.createElement("payopbkname")
            payopbkname_value = doc.createTextNode("普定县农村信用合作联社鸡场信用社")
            payopbkname_node.appendChild(payopbkname_value)
            list_node.appendChild(payopbkname_node)

            # response>xfaceTradeDTO>responseDTO>list>taxpayname
            taxpayname_node = doc.createElement("taxpayname")
            taxpayname_value = doc.createTextNode("普定县鸡场坡苗阿朵加工厂")
            taxpayname_node.appendChild(taxpayname_value)
            list_node.appendChild(taxpayname_node)

            # response>xfaceTradeDTO>responseDTO>list>handorgname
            handorgname_node = doc.createElement("handorgname")
            handorgname_value = doc.createTextNode("普定县鸡场坡苗阿朵加工厂")
            handorgname_node.appendChild(handorgname_value)
            list_node.appendChild(handorgname_node)

            # response>xfaceTradeDTO>responseDTO>list>khh
            khh_node = doc.createElement("khh")
            khh_value = doc.createTextNode("")
            khh_node.appendChild(khh_value)
            list_node.appendChild(khh_node)

            # response>xfaceTradeDTO>responseDTO>list>xyzt
            xyzt_node = doc.createElement("xyzt")
            xyzt_value = doc.createTextNode("A")
            xyzt_node.appendChild(xyzt_value)
            list_node.appendChild(xyzt_node)

            # response>xfaceTradeDTO>responseDTO>list>byzd
            byzd_node = doc.createElement("byzd")
            byzd_value = doc.createTextNode("2030012")
            byzd_node.appendChild(byzd_value)
            list_node.appendChild(byzd_node)

            # response>xfaceTradeDTO>responseDTO>list>gxdjrq
            gxdjrq_node = doc.createElement("gxdjrq")
            gxdjrq_value = doc.createTextNode("20181231")
            gxdjrq_node.appendChild(gxdjrq_value)
            list_node.appendChild(gxdjrq_node)

            # response>xfaceTradeDTO>responseDTO>list>djjgdh
            djjgdh_node = doc.createElement("djjgdh")
            djjgdh_value = doc.createTextNode("2030012")
            djjgdh_node.appendChild(djjgdh_value)
            list_node.appendChild(djjgdh_node)

            # response>xfaceTradeDTO>responseDTO>list>djjygy
            djjygy_node = doc.createElement("djjygy")
            djjygy_value = doc.createTextNode("155511")
            djjygy_node.appendChild(djjygy_value)
            list_node.appendChild(djjygy_node)

            # response>xfaceTradeDTO>responseDTO>list>xgrq
            xgrq_node = doc.createElement("xgrq")
            xgrq_value = doc.createTextNode("")
            xgrq_node.appendChild(xgrq_value)
            list_node.appendChild(xgrq_node)

            # response>xfaceTradeDTO>responseDTO>list>xgjgdh
            xgjgdh_node = doc.createElement("xgjgdh")
            xgjgdh_value = doc.createTextNode("")
            xgjgdh_node.appendChild(xgjgdh_value)
            list_node.appendChild(xgjgdh_node)

            # response>xfaceTradeDTO>responseDTO>list>xgjygy
            xgjygy_node = doc.createElement("xgjygy")
            xgjygy_value = doc.createTextNode("")
            xgjygy_node.appendChild(xgjygy_value)
            list_node.appendChild(xgjygy_node)

            # response>xfaceTradeDTO>responseDTO>list>fkzhlx
            fkzhlx_node = doc.createElement("fkzhlx")
            fkzhlx_value = doc.createTextNode("0")
            fkzhlx_node.appendChild(fkzhlx_value)
            list_node.appendChild(fkzhlx_node)

            # response>xfaceTradeDTO>responseDTO>list>djzddh
            djzddh_node = doc.createElement("djzddh")
            djzddh_value = doc.createTextNode("ITLR")
            djzddh_node.appendChild(djzddh_value)
            list_node.appendChild(djzddh_node)

            # response>xfaceTradeDTO>responseDTO>list>xgzddh
            xgzddh_node = doc.createElement("xgzddh")
            xgzddh_value = doc.createTextNode("")
            xgzddh_node.appendChild(xgzddh_value)
            list_node.appendChild(xgzddh_node)

    #实现行内渠道到中间业务TIPS前置查询对账差错明细功能
    elif serviceCode == "712324":
        # 检查必填关键字段 wdmc ywbh
        if "yybs" in dict.keys()  and "wdmc" in dict.keys() and "ywbh" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0  and len(dict['wdmc']) != 0 and len(dict['ywbh']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>reg_order
        reg_order_node = doc.createElement("reg_order")
        reg_order_value = doc.createTextNode("20125200910013638666")
        if not serviceCodeFlag:
            reg_order_value = doc.createTextNode("")
        reg_order_node.appendChild(reg_order_value)
        xresponseDTO_node.appendChild(reg_order_node)

        # response>xfaceTradeDTO>responseDTO>det_num
        det_num_node = doc.createElement("det_num")
        det_num_value = doc.createTextNode("1")
        if not serviceCodeFlag:
            det_num_value = doc.createTextNode("")
        det_num_node.appendChild(det_num_value)
        xresponseDTO_node.appendChild(det_num_node)


        if serviceCodeFlag:
            # response>xfaceTradeDTO>responseDTO>insuranceInfo
            insuranceInfo_node = doc.createElement("insuranceInfo")
            xresponseDTO_node.appendChild(insuranceInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>social_sec_branch
            social_sec_branch_node = doc.createElement("social_sec_branch")
            social_sec_branch_value = doc.createTextNode("5200000201522731")
            social_sec_branch_node.appendChild(social_sec_branch_value)
            insuranceInfo_node.appendChild(social_sec_branch_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>user_id
            user_id_node = doc.createElement("user_id")
            user_id_value = doc.createTextNode("28258950")
            user_id_node.appendChild(user_id_value)
            insuranceInfo_node.appendChild(user_id_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_org_code
            tax_org_code_node = doc.createElement("tax_org_code")
            tax_org_code_value = doc.createTextNode("15227310000")
            tax_org_code_node.appendChild(tax_org_code_value)
            insuranceInfo_node.appendChild(tax_org_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_type
            pay_type_node = doc.createElement("pay_type")
            pay_type_value = doc.createTextNode("0")
            pay_type_node.appendChild(pay_type_value)
            insuranceInfo_node.appendChild(pay_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>sub_det_num
            sub_det_num_node = doc.createElement("sub_det_num")
            sub_det_num_value = doc.createTextNode("1")
            sub_det_num_node.appendChild(sub_det_num_value)
            insuranceInfo_node.appendChild(sub_det_num_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo
            insuranceTypeInfo_node = doc.createElement("insuranceTypeInfo")
            insuranceInfo_node.appendChild(insuranceTypeInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>begin_date
            begin_date_node = doc.createElement("begin_date")
            begin_date_value = doc.createTextNode("201210")
            begin_date_node.appendChild(begin_date_value)
            insuranceTypeInfo_node.appendChild(begin_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>end_date
            end_date_node = doc.createElement("end_date")
            end_date_value = doc.createTextNode("999912")
            end_date_node.appendChild(end_date_value)
            insuranceTypeInfo_node.appendChild(end_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>project_code
            project_code_node = doc.createElement("project_code")
            project_code_value = doc.createTextNode("10210")
            project_code_node.appendChild(project_code_value)
            insuranceTypeInfo_node.appendChild(project_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>project_name
            project_name_node = doc.createElement("project_name")
            project_name_value = doc.createTextNode("城乡居民基本养老保险费")
            project_name_node.appendChild(project_name_value)
            insuranceTypeInfo_node.appendChild(project_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>item_code
            item_code_node = doc.createElement("item_code")
            item_code_value = doc.createTextNode("102100100")
            item_code_node.appendChild(item_code_value)
            insuranceTypeInfo_node.appendChild(item_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>item_name
            item_name_node = doc.createElement("item_name")
            item_name_value = doc.createTextNode("城乡居民基本养老保险费")
            item_name_node.appendChild(item_name_value)
            insuranceTypeInfo_node.appendChild(item_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>sub_item_code
            sub_item_code_node = doc.createElement("sub_item_code")
            sub_item_code_value = doc.createTextNode("000000000")
            sub_item_code_node.appendChild(sub_item_code_value)
            insuranceTypeInfo_node.appendChild(sub_item_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>sub_item_name
            sub_item_name_node = doc.createElement("sub_item_name")
            sub_item_name_value = doc.createTextNode("000000000")
            sub_item_name_node.appendChild(sub_item_name_value)
            insuranceTypeInfo_node.appendChild(sub_item_name_node)

    #实现行内渠道到中间业务TIPS前置银行不平调账功能
    elif serviceCode == "712325":
        # 检查必填关键字段 wdmc ywbh orizwrq orizjlsh
        if "yybs" in dict.keys()  and "wdmc" in dict.keys() and "ywbh" in dict.keys() and "orizwrq" in dict.keys() \
                and "orizjlsh" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0  and len(dict['wdmc']) != 0 and len(dict['ywbh']) != 0 \
                    and len(dict['orizwrq']) != 0 and len(dict['orizjlsh']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>reg_order
        reg_order_node = doc.createElement("reg_order")
        reg_order_value = doc.createTextNode("20125200910013638666")
        if not serviceCodeFlag:
            reg_order_value = doc.createTextNode("")
        reg_order_node.appendChild(reg_order_value)
        xresponseDTO_node.appendChild(reg_order_node)

        # response>xfaceTradeDTO>responseDTO>det_num
        det_num_node = doc.createElement("det_num")
        det_num_value = doc.createTextNode("1")
        if not serviceCodeFlag:
            det_num_value = doc.createTextNode("")
        det_num_node.appendChild(det_num_value)
        xresponseDTO_node.appendChild(det_num_node)


        if serviceCodeFlag:
            # response>xfaceTradeDTO>responseDTO>insuranceInfo
            insuranceInfo_node = doc.createElement("insuranceInfo")
            xresponseDTO_node.appendChild(insuranceInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>social_sec_branch
            social_sec_branch_node = doc.createElement("social_sec_branch")
            social_sec_branch_value = doc.createTextNode("5200000201522731")
            social_sec_branch_node.appendChild(social_sec_branch_value)
            insuranceInfo_node.appendChild(social_sec_branch_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>user_id
            user_id_node = doc.createElement("user_id")
            user_id_value = doc.createTextNode("28258950")
            user_id_node.appendChild(user_id_value)
            insuranceInfo_node.appendChild(user_id_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_org_code
            tax_org_code_node = doc.createElement("tax_org_code")
            tax_org_code_value = doc.createTextNode("15227310000")
            tax_org_code_node.appendChild(tax_org_code_value)
            insuranceInfo_node.appendChild(tax_org_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_type
            pay_type_node = doc.createElement("pay_type")
            pay_type_value = doc.createTextNode("0")
            pay_type_node.appendChild(pay_type_value)
            insuranceInfo_node.appendChild(pay_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>sub_det_num
            sub_det_num_node = doc.createElement("sub_det_num")
            sub_det_num_value = doc.createTextNode("1")
            sub_det_num_node.appendChild(sub_det_num_value)
            insuranceInfo_node.appendChild(sub_det_num_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo
            insuranceTypeInfo_node = doc.createElement("insuranceTypeInfo")
            insuranceInfo_node.appendChild(insuranceTypeInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>begin_date
            begin_date_node = doc.createElement("begin_date")
            begin_date_value = doc.createTextNode("201210")
            begin_date_node.appendChild(begin_date_value)
            insuranceTypeInfo_node.appendChild(begin_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>end_date
            end_date_node = doc.createElement("end_date")
            end_date_value = doc.createTextNode("999912")
            end_date_node.appendChild(end_date_value)
            insuranceTypeInfo_node.appendChild(end_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>project_code
            project_code_node = doc.createElement("project_code")
            project_code_value = doc.createTextNode("10210")
            project_code_node.appendChild(project_code_value)
            insuranceTypeInfo_node.appendChild(project_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>project_name
            project_name_node = doc.createElement("project_name")
            project_name_value = doc.createTextNode("城乡居民基本养老保险费")
            project_name_node.appendChild(project_name_value)
            insuranceTypeInfo_node.appendChild(project_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>item_code
            item_code_node = doc.createElement("item_code")
            item_code_value = doc.createTextNode("102100100")
            item_code_node.appendChild(item_code_value)
            insuranceTypeInfo_node.appendChild(item_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>item_name
            item_name_node = doc.createElement("item_name")
            item_name_value = doc.createTextNode("城乡居民基本养老保险费")
            item_name_node.appendChild(item_name_value)
            insuranceTypeInfo_node.appendChild(item_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>sub_item_code
            sub_item_code_node = doc.createElement("sub_item_code")
            sub_item_code_value = doc.createTextNode("000000000")
            sub_item_code_node.appendChild(sub_item_code_value)
            insuranceTypeInfo_node.appendChild(sub_item_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>sub_item_name
            sub_item_name_node = doc.createElement("sub_item_name")
            sub_item_name_value = doc.createTextNode("000000000")
            sub_item_name_node.appendChild(sub_item_name_value)
            insuranceTypeInfo_node.appendChild(sub_item_name_node)

    #实现行内渠道到中间业务TIPS前置增加差错记录打印次数功能
    elif serviceCode == "712326":
        # 检查必填关键字段 wdmc ywbh orizjlsh
        if "yybs" in dict.keys()  and "wdmc" in dict.keys() and "ywbh" in dict.keys() and "orizjlsh" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0  and len(dict['wdmc']) != 0 and len(dict['ywbh']) != 0 and len(dict['orizjlsh']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>reg_order
        reg_order_node = doc.createElement("reg_order")
        reg_order_value = doc.createTextNode("20125200910013638666")
        if not serviceCodeFlag:
            reg_order_value = doc.createTextNode("")
        reg_order_node.appendChild(reg_order_value)
        xresponseDTO_node.appendChild(reg_order_node)

        # response>xfaceTradeDTO>responseDTO>det_num
        det_num_node = doc.createElement("det_num")
        det_num_value = doc.createTextNode("1")
        if not serviceCodeFlag:
            det_num_value = doc.createTextNode("")
        det_num_node.appendChild(det_num_value)
        xresponseDTO_node.appendChild(det_num_node)


        if serviceCodeFlag:
            # response>xfaceTradeDTO>responseDTO>insuranceInfo
            insuranceInfo_node = doc.createElement("insuranceInfo")
            xresponseDTO_node.appendChild(insuranceInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>social_sec_branch
            social_sec_branch_node = doc.createElement("social_sec_branch")
            social_sec_branch_value = doc.createTextNode("5200000201522731")
            social_sec_branch_node.appendChild(social_sec_branch_value)
            insuranceInfo_node.appendChild(social_sec_branch_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>user_id
            user_id_node = doc.createElement("user_id")
            user_id_value = doc.createTextNode("28258950")
            user_id_node.appendChild(user_id_value)
            insuranceInfo_node.appendChild(user_id_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_org_code
            tax_org_code_node = doc.createElement("tax_org_code")
            tax_org_code_value = doc.createTextNode("15227310000")
            tax_org_code_node.appendChild(tax_org_code_value)
            insuranceInfo_node.appendChild(tax_org_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_type
            pay_type_node = doc.createElement("pay_type")
            pay_type_value = doc.createTextNode("0")
            pay_type_node.appendChild(pay_type_value)
            insuranceInfo_node.appendChild(pay_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>sub_det_num
            sub_det_num_node = doc.createElement("sub_det_num")
            sub_det_num_value = doc.createTextNode("1")
            sub_det_num_node.appendChild(sub_det_num_value)
            insuranceInfo_node.appendChild(sub_det_num_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo
            insuranceTypeInfo_node = doc.createElement("insuranceTypeInfo")
            insuranceInfo_node.appendChild(insuranceTypeInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>begin_date
            begin_date_node = doc.createElement("begin_date")
            begin_date_value = doc.createTextNode("201210")
            begin_date_node.appendChild(begin_date_value)
            insuranceTypeInfo_node.appendChild(begin_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>end_date
            end_date_node = doc.createElement("end_date")
            end_date_value = doc.createTextNode("999912")
            end_date_node.appendChild(end_date_value)
            insuranceTypeInfo_node.appendChild(end_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>project_code
            project_code_node = doc.createElement("project_code")
            project_code_value = doc.createTextNode("10210")
            project_code_node.appendChild(project_code_value)
            insuranceTypeInfo_node.appendChild(project_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>project_name
            project_name_node = doc.createElement("project_name")
            project_name_value = doc.createTextNode("城乡居民基本养老保险费")
            project_name_node.appendChild(project_name_value)
            insuranceTypeInfo_node.appendChild(project_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>item_code
            item_code_node = doc.createElement("item_code")
            item_code_value = doc.createTextNode("102100100")
            item_code_node.appendChild(item_code_value)
            insuranceTypeInfo_node.appendChild(item_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>item_name
            item_name_node = doc.createElement("item_name")
            item_name_value = doc.createTextNode("城乡居民基本养老保险费")
            item_name_node.appendChild(item_name_value)
            insuranceTypeInfo_node.appendChild(item_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>sub_item_code
            sub_item_code_node = doc.createElement("sub_item_code")
            sub_item_code_value = doc.createTextNode("000000000")
            sub_item_code_node.appendChild(sub_item_code_value)
            insuranceTypeInfo_node.appendChild(sub_item_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>sub_item_name
            sub_item_name_node = doc.createElement("sub_item_name")
            sub_item_name_value = doc.createTextNode("000000000")
            sub_item_name_node.appendChild(sub_item_name_value)
            insuranceTypeInfo_node.appendChild(sub_item_name_node)

    #实现行内渠道到中间业务TIPS前置查询网点现金账户功能
    elif serviceCode == "712327":
        # 检查必填关键字段 wdmc ywbh jgdh
        if "yybs" in dict.keys()  and "wdmc" in dict.keys() and "ywbh" in dict.keys() and "jgdh" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0  and len(dict['wdmc']) != 0 and len(dict['ywbh']) != 0 and len(dict['jgdh']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>reg_order
        reg_order_node = doc.createElement("reg_order")
        reg_order_value = doc.createTextNode("20125200910013638666")
        if not serviceCodeFlag:
            reg_order_value = doc.createTextNode("")
        reg_order_node.appendChild(reg_order_value)
        xresponseDTO_node.appendChild(reg_order_node)

        # response>xfaceTradeDTO>responseDTO>det_num
        det_num_node = doc.createElement("det_num")
        det_num_value = doc.createTextNode("1")
        if not serviceCodeFlag:
            det_num_value = doc.createTextNode("")
        det_num_node.appendChild(det_num_value)
        xresponseDTO_node.appendChild(det_num_node)


        if serviceCodeFlag:
            # response>xfaceTradeDTO>responseDTO>insuranceInfo
            insuranceInfo_node = doc.createElement("insuranceInfo")
            xresponseDTO_node.appendChild(insuranceInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>social_sec_branch
            social_sec_branch_node = doc.createElement("social_sec_branch")
            social_sec_branch_value = doc.createTextNode("5200000201522731")
            social_sec_branch_node.appendChild(social_sec_branch_value)
            insuranceInfo_node.appendChild(social_sec_branch_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>user_id
            user_id_node = doc.createElement("user_id")
            user_id_value = doc.createTextNode("28258950")
            user_id_node.appendChild(user_id_value)
            insuranceInfo_node.appendChild(user_id_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>tax_org_code
            tax_org_code_node = doc.createElement("tax_org_code")
            tax_org_code_value = doc.createTextNode("15227310000")
            tax_org_code_node.appendChild(tax_org_code_value)
            insuranceInfo_node.appendChild(tax_org_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>pay_type
            pay_type_node = doc.createElement("pay_type")
            pay_type_value = doc.createTextNode("0")
            pay_type_node.appendChild(pay_type_value)
            insuranceInfo_node.appendChild(pay_type_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>sub_det_num
            sub_det_num_node = doc.createElement("sub_det_num")
            sub_det_num_value = doc.createTextNode("1")
            sub_det_num_node.appendChild(sub_det_num_value)
            insuranceInfo_node.appendChild(sub_det_num_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo
            insuranceTypeInfo_node = doc.createElement("insuranceTypeInfo")
            insuranceInfo_node.appendChild(insuranceTypeInfo_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>begin_date
            begin_date_node = doc.createElement("begin_date")
            begin_date_value = doc.createTextNode("201210")
            begin_date_node.appendChild(begin_date_value)
            insuranceTypeInfo_node.appendChild(begin_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>end_date
            end_date_node = doc.createElement("end_date")
            end_date_value = doc.createTextNode("999912")
            end_date_node.appendChild(end_date_value)
            insuranceTypeInfo_node.appendChild(end_date_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>project_code
            project_code_node = doc.createElement("project_code")
            project_code_value = doc.createTextNode("10210")
            project_code_node.appendChild(project_code_value)
            insuranceTypeInfo_node.appendChild(project_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>project_name
            project_name_node = doc.createElement("project_name")
            project_name_value = doc.createTextNode("城乡居民基本养老保险费")
            project_name_node.appendChild(project_name_value)
            insuranceTypeInfo_node.appendChild(project_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>item_code
            item_code_node = doc.createElement("item_code")
            item_code_value = doc.createTextNode("102100100")
            item_code_node.appendChild(item_code_value)
            insuranceTypeInfo_node.appendChild(item_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>item_name
            item_name_node = doc.createElement("item_name")
            item_name_value = doc.createTextNode("城乡居民基本养老保险费")
            item_name_node.appendChild(item_name_value)
            insuranceTypeInfo_node.appendChild(item_name_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>sub_item_code
            sub_item_code_node = doc.createElement("sub_item_code")
            sub_item_code_value = doc.createTextNode("000000000")
            sub_item_code_node.appendChild(sub_item_code_value)
            insuranceTypeInfo_node.appendChild(sub_item_code_node)

            # response>xfaceTradeDTO>responseDTO>insuranceInfo>insuranceTypeInfo_node>sub_item_name
            sub_item_name_node = doc.createElement("sub_item_name")
            sub_item_name_value = doc.createTextNode("000000000")
            sub_item_name_node.appendChild(sub_item_name_value)
            insuranceTypeInfo_node.appendChild(sub_item_name_node)

    #实现行内渠道到中间业务TIPS前置查询国库资金汇划明细功能。
    # 备注：
    # 网点、非省联社管理机构：只能查询本联社的汇划信息；
    # 省联社管理机构：可以查询所有
    elif serviceCode == "712329":
        # 检查必填关键字段 wdmc ywbh
        if "yybs" in dict.keys()  and "wdmc" in dict.keys() and "ywbh" in dict.keys():
            # 值不能为空
            if len(dict['yybs']) != 0  and len(dict['wdmc']) != 0 and len(dict['ywbh']) != 0:
                serviceCodeFlag = True

        # status>desc
        if not serviceCodeFlag:
            desc_value = doc.createTextNode("必填字段不能为空请确认")

        # status>retCd
        if not serviceCodeFlag:
            retCd_value = doc.createTextNode("131419")

        # response>xfaceTradeDTO>responseDTO>jymxs
        jymxs_node = doc.createElement("jymxs")
        jymxs_value = doc.createTextNode("3")
        if not serviceCodeFlag:
            jymxs_value = doc.createTextNode("")
        jymxs_node.appendChild(jymxs_value)
        xresponseDTO_node.appendChild(jymxs_node)

        # response>xfaceTradeDTO>responseDTO>zbs
        zbs_node = doc.createElement("zbs")
        zbs_value = doc.createTextNode("3")
        if not serviceCodeFlag:
            zbs_value = doc.createTextNode("")
        zbs_node.appendChild(zbs_value)
        xresponseDTO_node.appendChild(zbs_node)


        if serviceCodeFlag:
            #第一个数据
            # response>xfaceTradeDTO>responseDTO>list
            list_node = doc.createElement("list")
            xresponseDTO_node.appendChild(list_node)

            # response>xfaceTradeDTO>responseDTO>list>chkdate
            chkdate_node = doc.createElement("chkdate")
            chkdate_value = doc.createTextNode("20190619")
            chkdate_node.appendChild(chkdate_value)
            list_node.appendChild(chkdate_node)

            # response>xfaceTradeDTO>responseDTO>list>chkacctord
            chkacctord_node = doc.createElement("chkacctord")
            chkacctord_value = doc.createTextNode("1001")
            chkacctord_node.appendChild(chkacctord_value)
            list_node.appendChild(chkacctord_node)

            # response>xfaceTradeDTO>responseDTO>list>paybkcode
            paybkcode_node = doc.createElement("paybkcode")
            paybkcode_value = doc.createTextNode("314701012036")
            paybkcode_node.appendChild(paybkcode_value)
            list_node.appendChild(paybkcode_node)

            # response>xfaceTradeDTO>responseDTO>list>paybkname
            paybkname_node = doc.createElement("paybkname")
            paybkname_value = doc.createTextNode("贵州乌当农村商业银行股份有限公司")
            paybkname_node.appendChild(paybkname_value)
            list_node.appendChild(paybkname_node)

            # response>xfaceTradeDTO>responseDTO>list>payeebankno
            payeebankno_node = doc.createElement("payeebankno")
            payeebankno_value = doc.createTextNode("011701000014")
            payeebankno_node.appendChild(payeebankno_value)
            list_node.appendChild(payeebankno_node)

            # response>xfaceTradeDTO>responseDTO>list>payopbkcode
            payopbkcode_node = doc.createElement("payopbkcode")
            payopbkcode_value = doc.createTextNode("314701012036")
            payopbkcode_node.appendChild(payopbkcode_value)
            list_node.appendChild(payopbkcode_node)

            # response>xfaceTradeDTO>responseDTO>list>payopbkname
            payopbkname_node = doc.createElement("payopbkname")
            payopbkname_value = doc.createTextNode("贵州乌当农村商业银行股份有限公司")
            payopbkname_node.appendChild(payopbkname_value)
            list_node.appendChild(payopbkname_node)

            # response>xfaceTradeDTO>responseDTO>list>payacct
            payacct_node = doc.createElement("payacct")
            payacct_value = doc.createTextNode("2039010001201300500010")
            payacct_node.appendChild(payacct_value)
            list_node.appendChild(payacct_node)

            # response>xfaceTradeDTO>responseDTO>list>payeeopbankno
            payeeopbankno_node = doc.createElement("payeeopbankno")
            payeeopbankno_value = doc.createTextNode("011701000014")
            payeeopbankno_node.appendChild(payeeopbankno_value)
            list_node.appendChild(payeeopbankno_node)

            # response>xfaceTradeDTO>responseDTO>list>payeeacct
            payeeacct_node = doc.createElement("payeeacct")
            payeeacct_value = doc.createTextNode("230000000002371002")
            payeeacct_node.appendChild(payeeacct_value)
            list_node.appendChild(payeeacct_node)

            # response>xfaceTradeDTO>responseDTO>list>payeebankname
            payeebankname_node = doc.createElement("payeebankname")
            payeebankname_value = doc.createTextNode("暂收款")
            payeebankname_node.appendChild(payeebankname_value)
            list_node.appendChild(payeebankname_node)

            # response>xfaceTradeDTO>responseDTO>list>chkaccttype
            chkaccttype_node = doc.createElement("chkaccttype")
            chkaccttype_value = doc.createTextNode("1")
            chkaccttype_node.appendChild(chkaccttype_value)
            list_node.appendChild(chkaccttype_node)

            # response>xfaceTradeDTO>responseDTO>list>allnum
            allnum_node = doc.createElement("allnum")
            allnum_value = doc.createTextNode("0")
            allnum_node.appendChild(allnum_value)
            list_node.appendChild(allnum_node)

            # response>xfaceTradeDTO>responseDTO>list>allamt
            allamt_node = doc.createElement("allamt")
            allamt_value = doc.createTextNode("0.00")
            allamt_node.appendChild(allamt_value)
            list_node.appendChild(allamt_node)

            # response>xfaceTradeDTO>responseDTO>list>jybs
            jybs_node = doc.createElement("jybs")
            jybs_value = doc.createTextNode("0")
            jybs_node.appendChild(jybs_value)
            list_node.appendChild(jybs_node)

            # response>xfaceTradeDTO>responseDTO>list>jyje
            jyje_node = doc.createElement("jyje")
            jyje_value = doc.createTextNode("0.00")
            jyje_node.appendChild(jyje_value)
            list_node.appendChild(jyje_node)

            # response>xfaceTradeDTO>responseDTO>list>addword
            addword_node = doc.createElement("addword")
            addword_value = doc.createTextNode("20190619|1001|314701012036|011701000014|0|0.00|")
            addword_node.appendChild(addword_value)
            list_node.appendChild(addword_node)

            # response>xfaceTradeDTO>responseDTO>list>jyrq
            jyrq_node = doc.createElement("jyrq")
            jyrq_value = doc.createTextNode("20190620")
            jyrq_node.appendChild(jyrq_value)
            list_node.appendChild(jyrq_node)

            # response>xfaceTradeDTO>responseDTO>list>jysj
            jysj_node = doc.createElement("jysj")
            jysj_value = doc.createTextNode("112911")
            jysj_node.appendChild(jysj_value)
            list_node.appendChild(jysj_node)

            # response>xfaceTradeDTO>responseDTO>list>zjrq
            zjrq_node = doc.createElement("zjrq")
            zjrq_value = doc.createTextNode("")
            zjrq_node.appendChild(zjrq_value)
            list_node.appendChild(zjrq_node)

            # response>xfaceTradeDTO>responseDTO>list>zjsj
            zjsj_node = doc.createElement("zjsj")
            zjsj_value = doc.createTextNode("")
            zjsj_node.appendChild(zjsj_value)
            list_node.appendChild(zjsj_node)

            # response>xfaceTradeDTO>responseDTO>list>zjlsh
            zjlsh_node = doc.createElement("zjlsh")
            zjlsh_value = doc.createTextNode("")
            zjlsh_node.appendChild(zjlsh_value)
            list_node.appendChild(zjlsh_node)

            # response>xfaceTradeDTO>responseDTO>list>jyzt
            jyzt_node = doc.createElement("jyzt")
            jyzt_value = doc.createTextNode("1")
            jyzt_node.appendChild(jyzt_value)
            list_node.appendChild(jyzt_node)

            # response>xfaceTradeDTO>responseDTO>list>xym
            xym_node = doc.createElement("xym")
            xym_value = doc.createTextNode("0")
            xym_node.appendChild(xym_value)
            list_node.appendChild(xym_node)

            # response>xfaceTradeDTO>responseDTO>list>xyxx
            xyxx_node = doc.createElement("xyxx")
            xyxx_value = doc.createTextNode("实时汇划数据初始成功")
            xyxx_node.appendChild(xyxx_value)
            list_node.appendChild(xyxx_node)

            # response>xfaceTradeDTO>responseDTO>list>channelseq
            channelseq_node = doc.createElement("channelseq")
            channelseq_value = doc.createTextNode("OBOW20190620112911068740439")
            channelseq_node.appendChild(channelseq_value)
            list_node.appendChild(channelseq_node)

            # response>xfaceTradeDTO>responseDTO>list>xtgzh
            xtgzh_node = doc.createElement("xtgzh")
            xtgzh_value = doc.createTextNode("OBOW20190620112911068740439")
            xtgzh_node.appendChild(xtgzh_value)
            list_node.appendChild(xtgzh_node)

            # response>xfaceTradeDTO>responseDTO>list>trecode
            trecode_node = doc.createElement("trecode")
            trecode_value = doc.createTextNode("2301050000")
            trecode_node.appendChild(trecode_value)
            list_node.appendChild(trecode_node)

            # response>xfaceTradeDTO>responseDTO>list>jyjg
            jyjg_node = doc.createElement("jyjg")
            jyjg_value = doc.createTextNode("2030001")
            jyjg_node.appendChild(jyjg_value)
            list_node.appendChild(jyjg_node)

            # response>xfaceTradeDTO>responseDTO>list>jgmc
            jgmc_node = doc.createElement("jgmc")
            jgmc_value = doc.createTextNode("贵州乌当农村商业银行股份有限公司")
            jgmc_node.appendChild(jgmc_value)
            list_node.appendChild(jgmc_node)


            #第二个数据
            # response>xfaceTradeDTO>responseDTO>list
            list_node = doc.createElement("list")
            xresponseDTO_node.appendChild(list_node)

            # response>xfaceTradeDTO>responseDTO>list>chkdate
            chkdate_node = doc.createElement("chkdate")
            chkdate_value = doc.createTextNode("20190618")
            chkdate_node.appendChild(chkdate_value)
            list_node.appendChild(chkdate_node)

            # response>xfaceTradeDTO>responseDTO>list>chkacctord
            chkacctord_node = doc.createElement("chkacctord")
            chkacctord_value = doc.createTextNode("1001")
            chkacctord_node.appendChild(chkacctord_value)
            list_node.appendChild(chkacctord_node)

            # response>xfaceTradeDTO>responseDTO>list>paybkcode
            paybkcode_node = doc.createElement("paybkcode")
            paybkcode_value = doc.createTextNode("314701012036")
            paybkcode_node.appendChild(paybkcode_value)
            list_node.appendChild(paybkcode_node)

            # response>xfaceTradeDTO>responseDTO>list>paybkname
            paybkname_node = doc.createElement("paybkname")
            paybkname_value = doc.createTextNode("贵州乌当农村商业银行股份有限公司")
            paybkname_node.appendChild(paybkname_value)
            list_node.appendChild(paybkname_node)

            # response>xfaceTradeDTO>responseDTO>list>payeebankno
            payeebankno_node = doc.createElement("payeebankno")
            payeebankno_value = doc.createTextNode("011701000014")
            payeebankno_node.appendChild(payeebankno_value)
            list_node.appendChild(payeebankno_node)

            # response>xfaceTradeDTO>responseDTO>list>payopbkcode
            payopbkcode_node = doc.createElement("payopbkcode")
            payopbkcode_value = doc.createTextNode("314701012036")
            payopbkcode_node.appendChild(payopbkcode_value)
            list_node.appendChild(payopbkcode_node)

            # response>xfaceTradeDTO>responseDTO>list>payopbkname
            payopbkname_node = doc.createElement("payopbkname")
            payopbkname_value = doc.createTextNode("贵州乌当农村商业银行股份有限公司")
            payopbkname_node.appendChild(payopbkname_value)
            list_node.appendChild(payopbkname_node)

            # response>xfaceTradeDTO>responseDTO>list>payacct
            payacct_node = doc.createElement("payacct")
            payacct_value = doc.createTextNode("2039010001201300500010")
            payacct_node.appendChild(payacct_value)
            list_node.appendChild(payacct_node)

            # response>xfaceTradeDTO>responseDTO>list>payeeopbankno
            payeeopbankno_node = doc.createElement("payeeopbankno")
            payeeopbankno_value = doc.createTextNode("011701000014")
            payeeopbankno_node.appendChild(payeeopbankno_value)
            list_node.appendChild(payeeopbankno_node)

            # response>xfaceTradeDTO>responseDTO>list>payeeacct
            payeeacct_node = doc.createElement("payeeacct")
            payeeacct_value = doc.createTextNode("230000000002371002")
            payeeacct_node.appendChild(payeeacct_value)
            list_node.appendChild(payeeacct_node)

            # response>xfaceTradeDTO>responseDTO>list>payeebankname
            payeebankname_node = doc.createElement("payeebankname")
            payeebankname_value = doc.createTextNode("暂收款")
            payeebankname_node.appendChild(payeebankname_value)
            list_node.appendChild(payeebankname_node)

            # response>xfaceTradeDTO>responseDTO>list>chkaccttype
            chkaccttype_node = doc.createElement("chkaccttype")
            chkaccttype_value = doc.createTextNode("1")
            chkaccttype_node.appendChild(chkaccttype_value)
            list_node.appendChild(chkaccttype_node)

            # response>xfaceTradeDTO>responseDTO>list>allnum
            allnum_node = doc.createElement("allnum")
            allnum_value = doc.createTextNode("0")
            allnum_node.appendChild(allnum_value)
            list_node.appendChild(allnum_node)

            # response>xfaceTradeDTO>responseDTO>list>allamt
            allamt_node = doc.createElement("allamt")
            allamt_value = doc.createTextNode("0.00")
            allamt_node.appendChild(allamt_value)
            list_node.appendChild(allamt_node)

            # response>xfaceTradeDTO>responseDTO>list>jybs
            jybs_node = doc.createElement("jybs")
            jybs_value = doc.createTextNode("0")
            jybs_node.appendChild(jybs_value)
            list_node.appendChild(jybs_node)

            # response>xfaceTradeDTO>responseDTO>list>jyje
            jyje_node = doc.createElement("jyje")
            jyje_value = doc.createTextNode("0.00")
            jyje_node.appendChild(jyje_value)
            list_node.appendChild(jyje_node)

            # response>xfaceTradeDTO>responseDTO>list>addword
            addword_node = doc.createElement("addword")
            addword_value = doc.createTextNode("20190618|1001|314701012036|011701000014|0|0.00|")
            addword_node.appendChild(addword_value)
            list_node.appendChild(addword_node)

            # response>xfaceTradeDTO>responseDTO>list>jyrq
            jyrq_node = doc.createElement("jyrq")
            jyrq_value = doc.createTextNode("20190619")
            jyrq_node.appendChild(jyrq_value)
            list_node.appendChild(jyrq_node)

            # response>xfaceTradeDTO>responseDTO>list>jysj
            jysj_node = doc.createElement("jysj")
            jysj_value = doc.createTextNode("021520")
            jysj_node.appendChild(jysj_value)
            list_node.appendChild(jysj_node)

            # response>xfaceTradeDTO>responseDTO>list>zjrq
            zjrq_node = doc.createElement("zjrq")
            zjrq_value = doc.createTextNode("")
            zjrq_node.appendChild(zjrq_value)
            list_node.appendChild(zjrq_node)

            # response>xfaceTradeDTO>responseDTO>list>zjsj
            zjsj_node = doc.createElement("zjsj")
            zjsj_value = doc.createTextNode("")
            zjsj_node.appendChild(zjsj_value)
            list_node.appendChild(zjsj_node)

            # response>xfaceTradeDTO>responseDTO>list>zjlsh
            zjlsh_node = doc.createElement("zjlsh")
            zjlsh_value = doc.createTextNode("")
            zjlsh_node.appendChild(zjlsh_value)
            list_node.appendChild(zjlsh_node)

            # response>xfaceTradeDTO>responseDTO>list>jyzt
            jyzt_node = doc.createElement("jyzt")
            jyzt_value = doc.createTextNode("1")
            jyzt_node.appendChild(jyzt_value)
            list_node.appendChild(jyzt_node)

            # response>xfaceTradeDTO>responseDTO>list>xym
            xym_node = doc.createElement("xym")
            xym_value = doc.createTextNode("0")
            xym_node.appendChild(xym_value)
            list_node.appendChild(xym_node)

            # response>xfaceTradeDTO>responseDTO>list>xyxx
            xyxx_node = doc.createElement("xyxx")
            xyxx_value = doc.createTextNode("实时汇划数据初始成功")
            xyxx_node.appendChild(xyxx_value)
            list_node.appendChild(xyxx_node)

            # response>xfaceTradeDTO>responseDTO>list>channelseq
            channelseq_node = doc.createElement("channelseq")
            channelseq_value = doc.createTextNode("OBOW20190619021520068735448")
            channelseq_node.appendChild(channelseq_value)
            list_node.appendChild(channelseq_node)

            # response>xfaceTradeDTO>responseDTO>list>xtgzh
            xtgzh_node = doc.createElement("xtgzh")
            xtgzh_value = doc.createTextNode("OBOW20190619021520068735448")
            xtgzh_node.appendChild(xtgzh_value)
            list_node.appendChild(xtgzh_node)

            # response>xfaceTradeDTO>responseDTO>list>trecode
            trecode_node = doc.createElement("trecode")
            trecode_value = doc.createTextNode("2301050000")
            trecode_node.appendChild(trecode_value)
            list_node.appendChild(trecode_node)

            # response>xfaceTradeDTO>responseDTO>list>jyjg
            jyjg_node = doc.createElement("jyjg")
            jyjg_value = doc.createTextNode("2030001")
            jyjg_node.appendChild(jyjg_value)
            list_node.appendChild(jyjg_node)

            # response>xfaceTradeDTO>responseDTO>list>jgmc
            jgmc_node = doc.createElement("jgmc")
            jgmc_value = doc.createTextNode("贵州乌当农村商业银行股份有限公司")
            jgmc_node.appendChild(jgmc_value)
            list_node.appendChild(jgmc_node)

            #第三个数据
            # response>xfaceTradeDTO>responseDTO>list
            list_node = doc.createElement("list")
            xresponseDTO_node.appendChild(list_node)

            # response>xfaceTradeDTO>responseDTO>list>chkdate
            chkdate_node = doc.createElement("chkdate")
            chkdate_value = doc.createTextNode("20190617")
            chkdate_node.appendChild(chkdate_value)
            list_node.appendChild(chkdate_node)

            # response>xfaceTradeDTO>responseDTO>list>chkacctord
            chkacctord_node = doc.createElement("chkacctord")
            chkacctord_value = doc.createTextNode("1001")
            chkacctord_node.appendChild(chkacctord_value)
            list_node.appendChild(chkacctord_node)

            # response>xfaceTradeDTO>responseDTO>list>paybkcode
            paybkcode_node = doc.createElement("paybkcode")
            paybkcode_value = doc.createTextNode("314701012036")
            paybkcode_node.appendChild(paybkcode_value)
            list_node.appendChild(paybkcode_node)

            # response>xfaceTradeDTO>responseDTO>list>paybkname
            paybkname_node = doc.createElement("paybkname")
            paybkname_value = doc.createTextNode("贵州乌当农村商业银行股份有限公司")
            paybkname_node.appendChild(paybkname_value)
            list_node.appendChild(paybkname_node)

            # response>xfaceTradeDTO>responseDTO>list>payeebankno
            payeebankno_node = doc.createElement("payeebankno")
            payeebankno_value = doc.createTextNode("011701000014")
            payeebankno_node.appendChild(payeebankno_value)
            list_node.appendChild(payeebankno_node)

            # response>xfaceTradeDTO>responseDTO>list>payopbkcode
            payopbkcode_node = doc.createElement("payopbkcode")
            payopbkcode_value = doc.createTextNode("314701012036")
            payopbkcode_node.appendChild(payopbkcode_value)
            list_node.appendChild(payopbkcode_node)

            # response>xfaceTradeDTO>responseDTO>list>payopbkname
            payopbkname_node = doc.createElement("payopbkname")
            payopbkname_value = doc.createTextNode("贵州乌当农村商业银行股份有限公司")
            payopbkname_node.appendChild(payopbkname_value)
            list_node.appendChild(payopbkname_node)

            # response>xfaceTradeDTO>responseDTO>list>payacct
            payacct_node = doc.createElement("payacct")
            payacct_value = doc.createTextNode("2039010001201300500010")
            payacct_node.appendChild(payacct_value)
            list_node.appendChild(payacct_node)

            # response>xfaceTradeDTO>responseDTO>list>payeeopbankno
            payeeopbankno_node = doc.createElement("payeeopbankno")
            payeeopbankno_value = doc.createTextNode("011701000014")
            payeeopbankno_node.appendChild(payeeopbankno_value)
            list_node.appendChild(payeeopbankno_node)

            # response>xfaceTradeDTO>responseDTO>list>payeeacct
            payeeacct_node = doc.createElement("payeeacct")
            payeeacct_value = doc.createTextNode("230000000002371002")
            payeeacct_node.appendChild(payeeacct_value)
            list_node.appendChild(payeeacct_node)

            # response>xfaceTradeDTO>responseDTO>list>payeebankname
            payeebankname_node = doc.createElement("payeebankname")
            payeebankname_value = doc.createTextNode("暂收款")
            payeebankname_node.appendChild(payeebankname_value)
            list_node.appendChild(payeebankname_node)

            # response>xfaceTradeDTO>responseDTO>list>chkaccttype
            chkaccttype_node = doc.createElement("chkaccttype")
            chkaccttype_value = doc.createTextNode("1")
            chkaccttype_node.appendChild(chkaccttype_value)
            list_node.appendChild(chkaccttype_node)

            # response>xfaceTradeDTO>responseDTO>list>allnum
            allnum_node = doc.createElement("allnum")
            allnum_value = doc.createTextNode("0")
            allnum_node.appendChild(allnum_value)
            list_node.appendChild(allnum_node)

            # response>xfaceTradeDTO>responseDTO>list>allamt
            allamt_node = doc.createElement("allamt")
            allamt_value = doc.createTextNode("0.00")
            allamt_node.appendChild(allamt_value)
            list_node.appendChild(allamt_node)

            # response>xfaceTradeDTO>responseDTO>list>jybs
            jybs_node = doc.createElement("jybs")
            jybs_value = doc.createTextNode("0")
            jybs_node.appendChild(jybs_value)
            list_node.appendChild(jybs_node)

            # response>xfaceTradeDTO>responseDTO>list>jyje
            jyje_node = doc.createElement("jyje")
            jyje_value = doc.createTextNode("0.00")
            jyje_node.appendChild(jyje_value)
            list_node.appendChild(jyje_node)

            # response>xfaceTradeDTO>responseDTO>list>addword
            addword_node = doc.createElement("addword")
            addword_value = doc.createTextNode("20190617|1001|314701012036|011701000014|0|0.00|")
            addword_node.appendChild(addword_value)
            list_node.appendChild(addword_node)

            # response>xfaceTradeDTO>responseDTO>list>jyrq
            jyrq_node = doc.createElement("jyrq")
            jyrq_value = doc.createTextNode("20190617")
            jyrq_node.appendChild(jyrq_value)
            list_node.appendChild(jyrq_node)

            # response>xfaceTradeDTO>responseDTO>list>jysj
            jysj_node = doc.createElement("jysj")
            jysj_value = doc.createTextNode("211917")
            jysj_node.appendChild(jysj_value)
            list_node.appendChild(jysj_node)

            # response>xfaceTradeDTO>responseDTO>list>zjrq
            zjrq_node = doc.createElement("zjrq")
            zjrq_value = doc.createTextNode("")
            zjrq_node.appendChild(zjrq_value)
            list_node.appendChild(zjrq_node)

            # response>xfaceTradeDTO>responseDTO>list>zjsj
            zjsj_node = doc.createElement("zjsj")
            zjsj_value = doc.createTextNode("")
            zjsj_node.appendChild(zjsj_value)
            list_node.appendChild(zjsj_node)

            # response>xfaceTradeDTO>responseDTO>list>zjlsh
            zjlsh_node = doc.createElement("zjlsh")
            zjlsh_value = doc.createTextNode("")
            zjlsh_node.appendChild(zjlsh_value)
            list_node.appendChild(zjlsh_node)

            # response>xfaceTradeDTO>responseDTO>list>jyzt
            jyzt_node = doc.createElement("jyzt")
            jyzt_value = doc.createTextNode("1")
            jyzt_node.appendChild(jyzt_value)
            list_node.appendChild(jyzt_node)

            # response>xfaceTradeDTO>responseDTO>list>xym
            xym_node = doc.createElement("xym")
            xym_value = doc.createTextNode("0")
            xym_node.appendChild(xym_value)
            list_node.appendChild(xym_node)

            # response>xfaceTradeDTO>responseDTO>list>xyxx
            xyxx_node = doc.createElement("xyxx")
            xyxx_value = doc.createTextNode("实时汇划数据初始成功")
            xyxx_node.appendChild(xyxx_value)
            list_node.appendChild(xyxx_node)

            # response>xfaceTradeDTO>responseDTO>list>channelseq
            channelseq_node = doc.createElement("channelseq")
            channelseq_value = doc.createTextNode("OBOW20190618211917068731092")
            channelseq_node.appendChild(channelseq_value)
            list_node.appendChild(channelseq_node)

            # response>xfaceTradeDTO>responseDTO>list>xtgzh
            xtgzh_node = doc.createElement("xtgzh")
            xtgzh_value = doc.createTextNode("OBOW20190618211917068731092")
            xtgzh_node.appendChild(xtgzh_value)
            list_node.appendChild(xtgzh_node)

            # response>xfaceTradeDTO>responseDTO>list>trecode
            trecode_node = doc.createElement("trecode")
            trecode_value = doc.createTextNode("2301050000")
            trecode_node.appendChild(trecode_value)
            list_node.appendChild(trecode_node)

            # response>xfaceTradeDTO>responseDTO>list>jyjg
            jyjg_node = doc.createElement("jyjg")
            jyjg_value = doc.createTextNode("2030001")
            jyjg_node.appendChild(jyjg_value)
            list_node.appendChild(jyjg_node)

            # response>xfaceTradeDTO>responseDTO>list>jgmc
            jgmc_node = doc.createElement("jgmc")
            jgmc_value = doc.createTextNode("贵州乌当农村商业银行股份有限公司")
            jgmc_node.appendChild(jgmc_value)
            list_node.appendChild(jgmc_node)


    else:
        desc_value = doc.createTextNode("未配置报文")

    # status>desc
    desc_node.appendChild(desc_value)
    status_node.appendChild(desc_node)

    # status>retCd
    retCd_node.appendChild(retCd_value)
    status_node.appendChild(retCd_node)

    # status>wrapperFailDetailMessage
    wrapperFailDetailMessage_node = doc.createElement("wrapperFailDetailMessage")
    wrapperFailDetailMessage_value = doc.createTextNode("")
    wrapperFailDetailMessage_node.appendChild(wrapperFailDetailMessage_value)
    status_node.appendChild(wrapperFailDetailMessage_node)

    # pprint.pprint(doc.toxml("utf-8"))
    returnXml = doc.toxml("utf-8")
    # returnXml = doc.toprettyxml(indent="\t", newl="\n")
    # # returnXml = doc.toxml("utf-8")
    # # print("returnXml:" + returnXml)
    # file_name = "./http/" + dict['msgType'] + ".xml"
    # if Msgtype == "HS":
    #     file_name = "./http/" + dict['msgType'] + "HS" + ".xml"
    # f = open(file_name, "w")
    # f.write(returnXml.decode())
    # f.close()
    return returnXml



#检查OSBSSTB报文格式是否符合
def CheckReqMsgAndResMsg(dict):
    flag = False
    #暂时考虑2中场景的报文格式计为赞同格式和恒生格式报文
    try:
        if "soapenv:Body" in dict.keys():
            #场景请求报文类型转换和响应报文类型   恒生格式报文
            if "msgType" in dict.keys():
                msgType = dict["msgType"]
                list = msgType.split('.')
                if list[0] == "OBOW" :
                    if len(list[1]) == 8:
                        temp = list[1] + '0'
                        res = str((int(temp) + 1)).zfill(9)
                    else:
                        res = str((int(list[1]) + 1)).zfill(9)
                    dict["msgType"] = msgType.replace(list[1],res)
                    flag = True
        else:
            #赞同格式报文
            flag = True

        return flag
    except:
        return flag

app = Flask(__name__)

@app.route('/OSBSSTB', methods=['GET', 'POST'])
def osbsstb():
    if(request.method == 'GET'):
        return jsonify(returnMag="请确认请求方式，当前为get请求", status=204)
    else:
        try:
            #解析报文
            req_data = request.get_data()
            time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            print(time + "-->请求报文：" + req_data.decode())
            xh = XMLHandler()
            xml.sax.parseString(req_data, xh)
            dict = xh.getDict()
            print("解析请求报文：")
            pprint.pprint(dict)
            tnsdict = {}
            Msgtype = "ZT"

            #恒生格式报文
            if "soapenv:Body" in dict.keys() or "soapenv:Envelope" in dict.keys():
                Msgtype = "HS"
                # 场景请求报文类型转换和响应报文类型
                if "msgType" in dict.keys():
                    msgType = dict["msgType"]
                    list = msgType.split('.')
                    if list[0] == "OBOW":
                        if len(list[1]) == 8:
                            temp = list[1] + '0'
                            res = str((int(temp) + 1)).zfill(9)
                        else:
                            res = str((int(list[1]) + 1)).zfill(9)
                        dict["msgType"] = msgType.replace(list[1], res)

                for key in dict.keys():
                    if "wrap" in key:
                        wrap = key.split(':')[1]
                        tnsdict['tns'] = "tns:" + wrap + "Response"
                        break

            responsexml = fixed_writexml_SSTB(dict, tnsdict, Msgtype)
            # pprint.pprint(responsexml)
            time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            print(time + "-->响应报文：" + responsexml.decode())
            return responsexml.decode(),{'Content-Type': 'application/xml'}


        except:
            time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            print(time + "-->响应报文：报文类型解析失败")
            return "报文类型解析失败", {'Content-Type': 'application/xml'}

@app.route('/OSBTIPS', methods=['GET', 'POST'])
def osbtips():
    if(request.method == 'GET'):
        return jsonify(returnMag="请确认请求方式，当前为get请求", status=204)
    else:
        try:
            #解析报文
            req_data = request.get_data()
            print("请求报文：" + req_data.decode())
            xh = XMLHandler()
            xml.sax.parseString(req_data, xh)
            dict = xh.getDict()
            print("解析请求报文：")
            pprint.pprint(dict)
            tnsdict = {}
            Msgtype = "ZT"

            #恒生格式报文
            if "soapenv:Body" in dict.keys() or "soapenv:Envelope" in dict.keys():
                Msgtype = "HS"
                # 场景请求报文类型转换和响应报文类型
                if "msgType" in dict.keys():
                    msgType = dict["msgType"]
                    list = msgType.split('.')
                    if list[0] == "OBOW":
                        if len(list[1]) == 8:
                            temp = list[1] + '0'
                            res = str((int(temp) + 1)).zfill(9)
                        else:
                            res = str((int(list[1]) + 1)).zfill(9)
                        dict["msgType"] = msgType.replace(list[1], res)

                for key in dict.keys():
                    if "wrap" in key:
                        wrap = key.split(':')[1]
                        tnsdict['tns'] = "tns:" + wrap + "Response"
                        break

            responsexml = fixed_writexml_TIPS(dict, tnsdict, Msgtype)
            # pprint.pprint(responsexml)
            print("响应报文：" + responsexml.decode())
            return responsexml.decode(),{'Content-Type': 'application/xml'}


        except:
            return "报文类型解析失败", {'Content-Type': 'application/xml'}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port= 8000)
