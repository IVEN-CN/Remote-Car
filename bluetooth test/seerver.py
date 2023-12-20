# server.py
"""一个简单了蓝牙服务器，接收另一个蓝牙客户端的信号"""
import bluetooth

server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_sock.bind(("",port))
server_sock.listen(1)

client_sock,address = server_sock.accept() # 接收客户端的连接请求，返回客户端socket和地址
print("Accepted connection from ",address)

def recv_all(sock):
    """接收所有数据"""
    BUFF_SIZE = 1024 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE) # 一次最多接收BUFF_SIZE字节,part是接收到的数据
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return int(data, 2)

data = recv_all(client_sock) # 1024是每次接收的最大字节数,data是接收到的数据
print(f"received [{data}]")

client_sock.close()
server_sock.close()