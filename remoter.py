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
from GY25 import calculate_angle
import threading
import time

if __name__ == '__main__':
    gy = GY25()
    remote_bluetooth = Bluetooth()
    time.sleep(1)
    remote_bluetooth.oled.clear()
    def main():
        global yaw, pitch, roll, angle
        while True:
            try:
                # 读取数据,yaw:航向角，pitch:俯仰角，roll:滚动角
                yaw, pitch, roll = gy.read_angle()
            except:
                continue

            # 姿态解算
            angle = calculate_angle(pitch, roll)

            # region处理数据
            if angle < 10:
                # 静置波动，小车静止
                sign = 0
            elif 10 <= angle < 45 and pitch < 0:
                # 轻微前倾，小车缓慢前进
                sign = 1
            elif  angle >= 45 and pitch < 0:
                # 前倾，小车加速前进
                sign = 2
            elif 10 <= angle < 45 and pitch > 0:
                # 轻微后倾，小车缓慢后退
                sign = 3
            elif angle >= 45 and pitch > 0:
                # 后倾，小车加速后退
                sign = 4
            elif angle >= 10 and roll < 0 and pitch < 0:
                # 左前倾，小车左前方移动
                sign = 5
            elif 10 <= angle < 45 and roll < 0:
                # 左倾，小车左移
                sign = 6
            elif 10 <= angle < 45 and roll > 0 and pitch < 0:
                # 右前倾，小车右前方移栋
                sign = 7
            elif 10 <= angle < 45 and roll > 0:
                # 右倾，小车右移
                sign = 8
            elif angle >= 45 and roll < 0:
                # 大幅度左倾，笑着左方向自转
                sign = 9
            elif angle >= 45 and roll > 0:
                # 大幅度右倾，小车右方向自转
                sign = 10
            elif angle >= 10 and roll < 0 and pitch > 0:
                # 左后倾，小车左后方移动
                sign = 11
            elif angle >= 10 and roll > 0 and pitch > 0:
                # 右后倾，小车右后方移动
                sign = 12
            else:
                # 其他情况，小车静止
                sign = 0
            # endregion

            # 发送信号
            remote_bluetooth.send(sign)
    
    def write_():
        time.sleep(0.01)
        remote_bluetooth.oled.write_text(f' yaw: {yaw}\n pitch:{pitch}\n roll:{roll}\n angle:{angle}')

    threading.Thread(target=main).start()
    threading.Thread(target=write_,daemon=True).start()