import bluetooth

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
    bluetooth = Bluetooth()
    while True:
        # 发送测试数据
        bluetooth.send('hello')