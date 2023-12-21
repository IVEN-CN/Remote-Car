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
import time

class MPU6050:
    def __init__(self):  
        # MPU6050寄存器
        self.PWR_MGMT_1   = 0x6B  # 电源管理寄存器
        self.SMPLRT_DIV   = 0x19  # 采样率分频寄存器
        self.CONFIG       = 0x1A  # 配置寄存器
        self.GYRO_CONFIG  = 0x1B  # 陀螺仪配置寄存器
        self.INT_ENABLE   = 0x38  # 中断使能寄存器

        self.ACCEL_XOUT_H = 0x3B  # 加速度计X轴高位寄存器
        self.ACCEL_YOUT_H = 0x3D  # 加速度计Y轴高位寄存器
        self.ACCEL_ZOUT_H = 0x3F  # 加速度计Z轴高位寄存器
        self.GYRO_XOUT_H  = 0x43  # 陀螺仪X轴高位寄存器
        self.GYRO_YOUT_H  = 0x45  # 陀螺仪Y轴高位寄存器
        self.GYRO_ZOUT_H  = 0x47  # 陀螺仪Z轴高位寄存器

        self.bus = smbus.SMBus(1)  # 或者bus = smbus.SMBus(0)适用于旧版本的板子
        self.Device_Address = 0x68   # MPU6050设备地址

    def MPU_Init(self):
        # 写入采样率分频寄存器
        self.bus.write_byte_data(self.Device_Address, self.SMPLRT_DIV, 7)
        
        # 写入电源管理寄存器
        self.bus.write_byte_data(self.Device_Address, self.PWR_MGMT_1, 1)
        
        # 写入配置寄存器
        self.bus.write_byte_data(self.Device_Address, self.CONFIG, 0)
        
        # 写入陀螺仪配置寄存器
        self.bus.write_byte_data(self.Device_Address, self.GYRO_CONFIG, 24)
        
        # 写入中断使能寄存器
        self.bus.write_byte_data(self.Device_Address, self.INT_ENABLE, 1)

    def read_raw_data(self, addr):
        # 加速度计和陀螺仪的值是16位的
        high = self.bus.read_byte_data(self.Device_Address, addr)
        low = self.bus.read_byte_data(self.Device_Address, addr+1)
        
        # 将高位和低位值拼接起来
        value = ((high << 8) | low)
        
        # 获取mpu6050的有符号值
        if(value > 32768):
            value = value - 65536
        return value

def main_mpu(self: MPU6050):
    """主函数"""
    self.MPU_Init()

    # 读取加速度计数据
    self.acc_x = self.read_raw_data(self.ACCEL_XOUT_H)
    self.acc_y = self.read_raw_data(self.ACCEL_YOUT_H)
    self.acc_z = self.read_raw_data(self.ACCEL_ZOUT_H)
    
    # 读取陀螺仪数据
    self.gyro_x = self.read_raw_data(self.GYRO_XOUT_H)
    self.gyro_y = self.read_raw_data(self.GYRO_YOUT_H)
    self.gyro_z = self.read_raw_data(self.GYRO_ZOUT_H)

    return (self.acc_x, self.acc_y, self.acc_z), (self.gyro_x, self.gyro_y, self.gyro_z)

class Bluetooth:
    """蓝牙连接类"""
    def __init__(self,address='00:00:00:00:00:00'):
        """初始化蓝牙连接"""
        self.serverMACAddress = address  
        self.port = 1
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((self.serverMACAddress, self.port))
    def send(self, data):
        """发送数据"""
        self.sock.send(data)
    def close(self):
        """关闭连接"""
        self.sock.close()

if __name__ == '__main__':
    mpu = MPU6050()
    remote_bluetooth = Bluetooth()
    while True:
        # 读取数据
        imformation = main_mpu(mpu)[1]
        # 发送数据
        remote_bluetooth.send(imformation)