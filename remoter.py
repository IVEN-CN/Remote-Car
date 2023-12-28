"""遥控小车的遥控器
树莓派读取MPU6050的数据，通过蓝牙发送给小车

MPU和树莓派（全志派）的连接方式：
    MPU-6050 VCC连接到树莓派的3.3V
    MPU-6050 GND连接到树莓派的GND
    MPU-6050 SDA连接到树莓派的SDA（GPIO2）
    MPU-6050 SCL连接到树莓派的SCL（GPIO3）
"""

import smbus
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