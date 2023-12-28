"""GY25陀螺仪读取角度测试文件"""
import serial
import struct

class GY25:
    def __init__(self, port='/dev/ttyS0', baudrate=115200):
        self.ser = serial.Serial(port, baudrate)
        self.ser.write(bytes.fromhex('A5'))  # 设置为角度输出模式
        self.ser.write(bytes.fromhex('52')) 

    def read_angle(self):
        while True:
            data = self.ser.read(8)  # 读取8个字节的数据
            if len(data) == 8 and data[0] == 0xAA:  # 检查数据包的头部
                yaw, pitch, roll = struct.unpack('<hhh', data[1:7])  # 解析数据包，<hhh表示3个16位整数
                # 分别对应yaw、pitch、roll，数据类型为小端字节序，即低位在前，高位在后
                return yaw / 100.0, pitch / 100.0, roll / 100.0  # 返回角度信息
            
if __name__ == '__main__':
    gy25 = GY25()
    yaw, pitch, roll = gy25.read_angle()
    print('偏航角:', yaw, '俯仰角:', pitch, '滚动角:', roll)