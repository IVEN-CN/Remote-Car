# client.py
"""一个简单的蓝牙客户端，向另一个蓝牙服务器发送信号"""
import bluetooth

serverMACAddress = '00:00:00:00:00:00'  # 请替换为你的蓝牙设备的MAC地址
port = 1
sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((serverMACAddress, port))

sock.send(b'2')

sock.close()