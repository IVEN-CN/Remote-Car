import bluetooth
import wiringpi as wp       # 引入香橙派的wireingpi库
from wiringpi import GPIO   # 引入香橙派的GPIO库
from GY25 import OLED
import serial

class Bluetooth:
    """蓝牙连接类"""
    def __init__(self,address='00:00:00:00:00:00', ifserial=False):
        self.oled = OLED(3, 0x3C)
        self.ifserial = ifserial
        self.oled.write_text('connecting...')
        """初始化蓝牙连接"""
        while True:
            try:
                self.serverMACAddress = address                         # 蓝牙模块的MAC地址
                self.port = 1                                           # 通信的频道，1是默认的频道
                self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM) # 创建一个客户端的socket
                self.sock.connect((self.serverMACAddress, self.port))   # 连接到服务器
                break
            except:
                continue
        if self.ifserial:
            while True:
                try:
                    self.ser = serial.Serial(port='/dev/rfcomm0', baudrate=9600)
                    break
                except:
                    continue
        self.oled.clear()
        self.oled.write_text('connecting success!!')

        self.led = LED(25)                                      # 初始化LED指示灯

    def send(self, data):
        """发送数据"""
        self.led.on()
        if self.ifserial == False:
            self.sock.send(data)
        else:
            self.ser.write(data)
        self.led.off()
        
    def read(self):
        """读取数据"""
        if self.ifserial == False:
            return self.sock.recv(1024)                            # 一次最多读取1024字节
        else:
            return self.ser.read(1024)
    
    def close(self):
        """关闭连接"""
        if self.ifserial == False:
            self.sock.close()
        else:
            self.ser.close()

class LED:
    def __init__(self, pin):
        """香橙派的LED指示灯
        pin：香橙派的引脚wpi编号，与LED的正极连接"""
        self.pin = pin
        wp.wiringPiSetupPhys()
        wp.pinMode(self.pin, GPIO.OUTPUT)

    def on(self):
        wp.digitalWrite(self.pin, GPIO.HIGH)

    def off(self):
        wp.digitalWrite(self.pin, GPIO.LOW)

    def blinl(self):
        wp.digitalWrite(self.pin, GPIO.HIGH)
        wp.delay(100)
        wp.digitalWrite(self.pin, GPIO.LOW)
        wp.delay(100)

if __name__ == '__main__':
    bluetooth = Bluetooth()
    while True:
        # 发送测试数据
        bluetooth.send('hello')