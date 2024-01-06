"""遥控小车的遥控器
荔枝派读取GY25的数据，通过蓝牙发送给小车

GY25与荔枝派的连接：
GY25的VCC接3.3V
GY25的GND接GND
GY25的RXD接TXD
GY25的TXD接RXD
"""

import bluetooth
from GY25 import GY25

class Bluetooth:
    """蓝牙连接类"""
    def __init__(self,address='00:00:00:00:00:00'):
        """初始化蓝牙连接"""
        self.serverMACAddress = address                         # 蓝牙模块的MAC地址
        self.port = 1                                           # 通信的频道，1是默认的频道
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM) # 创建一个客户端的socket
        self.sock.connect((self.serverMACAddress, self.port))   # 连接到服务器
    def send(self, data):
        """发送数据"""
        self.sock.send(data)
    def close(self):
        """关闭连接"""
        self.sock.close()

if __name__ == '__main__':
    gy = GY25()
    remote_bluetooth = Bluetooth()
    while True:
        # 读取数据
        imformation = gy.read_angle()
        # 发送数据
        remote_bluetooth.send(imformation)