import threading
import socket
import requests

global reqMsg
#接收数据
def recv(client_socket, ip_port):
    reqMsg = ""
    reqSize = 1024
    #计数器
    i = 0
    while True:
        client_text = client_socket.recv(1024)
        if client_text:
            print("计算器i:", i)
            print("[requestInfo]", ip_port,":",client_text)
            lenReq = client_text[0:8]
            if (lenReq.isdigit()) and i == 0:
                reqMsg = client_text.lstrip(lenReq)
                # 获取完整的请求报文
                reqSize = int(lenReq)
            else:
                reqMsg = reqMsg + client_text

            i += 1
            #即将发送的报文长度
            # reqlength = int(len(reqMsg.encode('utf-8')))
            reqlength = int(len(reqMsg))
            if (reqSize == reqlength):
                print("reqMsg请求完整报文:", str(reqMsg,encoding="UTF-8"))
                resMsg = requests.post(url="http://127.0.0.1:8000/OSBSSTB", data=reqMsg)
                # 返回报文长度
                length = len(resMsg.text.encode('utf-8'))
                slen = '%08d' % length
                resMsg = (slen + resMsg.text).encode()
                print('Response即将发送的响应报文:', resMsg.decode())
                client_socket.send(resMsg)
                reqMsg = ""
                reqSize = 1024
                i = 0
        else:
            client_socket.close()
            break

#程序主入口
def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #设置端口复用
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    tcp_socket.bind(('', 8888))
    tcp_socket.listen(100)
    while True:
        client_socket, ip_port =tcp_socket.accept()
        t1 = threading.Thread(target=recv, args=(client_socket, ip_port))
        #设置线程守护
        t1.setDaemon(True)
        t1.start()

if __name__ == '__main__':
    main()

