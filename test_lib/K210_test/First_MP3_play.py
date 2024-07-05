from machine import UART
from board import board_info
from fpioa_manager import fm
import time


fm.register(6, fm.fpioa.UART1_RX, force=True)
fm.register(7, fm.fpioa.UART1_TX, force=True)

uart = UART(UART.UART1, 115200, 8, 0, 0)

def send_command(command):
    uart.write(command)
    time.sleep(0.1)

while (True):
    send_command('A')  # 發送播放指令
    time.sleep(35)      # 停止5秒
    send_command('B')  # 發送播放指令
    time.sleep(29)      # 停止5秒
    send_command('C')  # 發送播放指令
    time.sleep(15)      # 停止5秒
    send_command('D')  # 發送停止指令
    time.sleep(21)     # 停止5秒
