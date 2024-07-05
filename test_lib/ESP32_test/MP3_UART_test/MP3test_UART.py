from fpioa_manager import fm
from board import board_info
from machine import UART
import time

# 配置UART引脚
fm.register(6, fm.fpioa.UART1_RX, force=True)
fm.register(7, fm.fpioa.UART1_TX, force=True)

# 初始化UART
uart = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)

# 等待一段时间，确保ESP32已经准备就绪
time.sleep(2)

def send_command(command):
    uart.write(command)
    time.sleep(0.1)

count = 0
while True:
    message = "K210 消息 #{}".format(count)
    uart.write(message + '\n')
    print("发送:", message)
    count += 1
    time.sleep(1)  # 每秒发送一次消息

    send_command('A')  # 發送播放指令
    time.sleep(10)      # 停止5秒
    send_command('B')  # 發送播放指令
    time.sleep(10)      # 停止5秒
    send_command('C')  # 發送播放指令
    time.sleep(10)      # 停止5秒
    send_command('D')  # 發送停止指令
    time.sleep(10)      # 停止5秒
