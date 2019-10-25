import socket
import threading


client = socket.socket()
# client.connect(('11.18.16.50', 9109))
client.connect(('127.0.0.1', 8888))

def recv_data():
    while True:
        data = client.recv(10240)
        print("客服端：")
        print(data.decode())


username = input("输入你的请求报文：")
client.send(username.encode())


thread = threading.Thread(target=recv_data, daemon=True)
thread.start()

while True:
    reqMsg = input('')
    client.send(reqMsg.encode())


