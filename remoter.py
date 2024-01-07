"""遥控小车的遥控器
荔枝派读取GY25的数据，通过蓝牙发送给小车

GY25与荔枝派的连接：
GY25的VCC接3.3V
GY25的GND接GND
GY25的RXD接TXD
GY25的TXD接RXD
"""

from bt import Bluetooth
from GY25 import GY25


if __name__ == '__main__':
    gy = GY25()
    remote_bluetooth = Bluetooth()
    while True:
        # 读取数据
        imformation = gy.read_angle()
        # 发送数据
        remote_bluetooth.send(imformation)