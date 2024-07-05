from machine import UART
import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()
# 初始化UART，假設使用UART1
uart = UART(UART.UART1, 115200, 8, 1)

def send_command(command):
    uart.write(command)
    time.sleep(0.1)

while (True):
    clock.tick()
    img = sensor.snapshot()
    print(clock.fps())
    send_command('A')  # 發送播放指令
    time.sleep(10)     # 播放10秒
    send_command('B')  # 發送播放指令
    time.sleep(10)     # 播放10秒
    send_command('C')  # 發送播放指令
    time.sleep(10)     # 播放10秒
    send_command('D')  # 發送停止指令
    time.sleep(10)      # 停止10秒
