import time
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
from MPU6050 import MPU6050

# 初始化OLED显示屏
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
disp.begin()
disp.clear()
disp.display()

# 创建一个空白的图像用于绘制
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# 获取绘图对象以便在图像上绘制
draw = ImageDraw.Draw(image)

# 初始化MPU6050
mpu6050 = MPU6050(0x68)

while True:
    # 清除图像内容
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # 读取陀螺仪数据
    accel_data = mpu6050.get_accel_data()
    gyro_data = mpu6050.get_gyro_data()

    # 在图像上绘制陀螺仪数据
    draw.text((0, 0), 'Accel: {0}'.format(accel_data), font=ImageFont.load_default(), fill=255)
    draw.text((0, 10), 'Gyro: {0}'.format(gyro_data), font=ImageFont.load_default(), fill=255)

    # 显示图像
    disp.image(image)
    disp.display()

    # 等待一段时间
    time.sleep(0.1)