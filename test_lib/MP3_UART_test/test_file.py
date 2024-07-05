from fpioa_manager import fm
from machine import UART
import time

# 配置UART引脚
fm.register(6, fm.fpioa.UART1_RX, force=True)
fm.register(7, fm.fpioa.UART1_TX, force=True)

# 初始化UART
uart = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)

# 等待一段时间，确保ESP32已经准备就绪
time.sleep(2)

count = 0
while True:
    message = "K210 消息 #{}".format(count)
    uart.write(message + '\n')
    print("发送:", message)

    if uart.any():
        #received_data = uart.read().decode('utf-8').strip()
        print("yo M3?")

    count += 1
    time.sleep(1)  # 每秒发送一次消息
