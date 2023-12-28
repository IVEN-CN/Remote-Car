"""GY25陀螺仪读取角度测试文件"""
import serial
import struct

class GY25:
    def __init__(self, port='/dev/ttyS0', baudrate=9600):
        self.ser = serial.Serial(port, baudrate)
        self.ser.write(bytes.fromhex('A6 01 00 00 00 00 00 01 A7'))  # 设置为角度输出模式

    def read_angle(self):
        while True:
            data = self.ser.read(8)  # 读取8个字节的数据
            if len(data) == 8 and data[0] == 0xa6:  # 检查数据包的头部
                yaw, pitch, roll = struct.unpack('<hhh', data[1:7])  # 解析数据包
                return yaw / 100.0, pitch / 100.0, roll / 100.0  # 返回角度信息

gy25 = GY25()
yaw, pitch, roll = gy25.read_angle()
print('偏航角:', yaw, '俯仰角:', pitch, '滚动角:', roll)