from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ThreadPool
from multiprocessing import Manager
import socket
from datetime import datetime
import requests

#发消息给所有连接的客户端
def send_data(proxy_dict, proxy_queue):
    while True:
        data = proxy_queue.get()     #从队列中拿要发给客户的消息
        print('Response即将发送的响应报文:', data.decode())
        for conn in proxy_dict.values():
            conn.send(data)

def worker_thread(conn,reqMsg, proxy_queue, lenReq):
    while True:
        recv_data = conn.recv(8 * 1024)
        if recv_data:
            time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            # data = "{name} {time} \n {data}".format(name=reqMsg, time=time, data = recv_data.decode())
            data = "{name} {data}".format(name=reqMsg, data=recv_data.decode())
            print("worker_thread:" + data)
            print(time)
            print(int(len(data.encode('utf-8'))))
            resMsg = requests.post(url="http://127.0.0.1:8000/OSBSSTB", data=data)
            proxy_queue.put(resMsg)
        else:
            conn.close()
            break

def worker_process(server, proxy_dict, proxy_queue):
    thread_pool = ThreadPool( cpu_count()*2 )   #通常分配2倍CPU个数的线程
    while True:
        conn, _ = server.accept()    #生成对等套接字
        reqMsg = conn.recv(10240).decode()   #客户上传的数据
        print("reqMsg请求报文:" + reqMsg)
        #报文头长度
        lenReq = reqMsg[0:8]
        if (lenReq.isdigit()):
            reqMsg = reqMsg.lstrip(lenReq)
        # 获取完整的请求报文
        reqSize = int(lenReq)
        #即将发送的报文长度
        reqlength = int(len(reqMsg.encode('utf-8')))
        while (reqSize == reqlength):
            print("reqMsg请求完整报文:" + reqMsg)
            resMsg = requests.post(url="http://127.0.0.1:8000/OSBSSTB", data=reqMsg.encode())
            #返回报文长度
            length = len(resMsg.text.encode('utf-8'))
            slen = '%08d' % length

            resMsg = (slen + resMsg.text).encode()
            proxy_dict[resMsg] = conn
            proxy_queue.put(resMsg)                #把数据丢到队列中去
            break
        else:
            # 异步提交
            thread_pool.apply_async(worker_thread, args=(conn,reqMsg, proxy_queue, lenReq))


if __name__ == '__main__':

    server = socket.socket()
    server.bind(('', 8888))
    server.listen(1000)

    mgr = Manager()
    proxy_dict = mgr.dict()    #保存连接的客户端， 名字当做键，对等套接字当做值
    proxy_queue = mgr.Queue()  #消息队列

    n = cpu_count()
    process_pool = Pool(n)

    for i in range(n-1):
        process_pool.apply_async(worker_process, args=(server, proxy_dict, proxy_queue))
    process_pool.apply_async(send_data, args=(proxy_dict, proxy_queue))

    process_pool.close()
    process_pool.join()