import sensor, image, lcd, time
import KPU as kpu
from machine import UART
import gc, sys
from fpioa_manager import fm
from board import board_info

input_size = (224, 224)
labels = ['raise_arm', 'squat', 'run', 'one_leg', 'other']
anchors = [3.44, 4.31, 2.94, 3.19, 1.19, 3.59, 1.81, 4.12, 2.81, 2.84]

def lcd_show_except(e):
    import uio
    err_str = uio.StringIO()
    sys.print_exception(e, err_str)
    err_str = err_str.getvalue()
    img = image.Image(size=input_size)
    img.draw_string(0, 10, err_str, scale=1, color=(0xff,0x00,0x00))
    lcd.display(img)

class Comm:
    def __init__(self, uart):
        self.uart = uart

    def send_detect_result(self, objects, labels):
        msg = ""
        if objects:
            for obj in objects:
                pos = obj.rect()
                p = obj.value()
                idx = obj.classid()
                label = labels[idx]
                msg += "{}:{}:{}:{}:{}:{:.2f}, ".format(pos[0], pos[1], pos[2], pos[3], idx, p)
            if msg:
                msg = msg[:-2] + "\n"
            self.uart.write(msg.encode())

def init_uart():
    fm.register(6, fm.fpioa.UART1_RX, force=True)
    fm.register(7, fm.fpioa.UART1_TX, force=True)
    uart = UART(UART.UART1, 115200, 8, 0, 0)
    return uart

def send_command(uart, command):
    uart.write(command)
    time.sleep(0.05)  # 減少延遲時間

def show_action(action, duration=2000):
    lcd.clear(lcd.WHITE)
    img = image.Image(size=(320, 240))
    img.draw_string(90, 110, action, color=(255, 0, 0), scale=2)
    lcd.display(img)
    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < duration:
        pass

def detect_action(task, action_label, uart, duration=10000):
    start_time = time.ticks_ms()
    comm = Comm(uart)

    while time.ticks_diff(time.ticks_ms(), start_time) < duration:
        img = sensor.snapshot()
        objects = kpu.run_yolo2(task, img)
        detected_labels = []

        if objects:
            for obj in objects:
                pos = obj.rect()
                img.draw_rectangle(pos)
                detected_labels.append(labels[obj.classid()])

            if "other" in detected_labels:
                img.draw_string(5, img.height() - 230, "############", scale=3, color=(255, 0, 0))
            else:
                img.draw_string(5, img.height() - 230, "############", scale=3, color=(0, 255, 0))
        else:
            img.draw_string(5, img.height() - 35, "############", scale=3, color=(255, 255, 0))

        label_pos_y = img.height() - (len(detected_labels) * 20) - 10
        for label in detected_labels:
            img.draw_string(img.width() - 100, label_pos_y, label, scale=1, color=(0, 255, 0))
            label_pos_y += 20

        lcd.display(img)
        comm.send_detect_result(objects, labels)

def main(anchors, labels=None, model_addr="/sd/m.kmodel", sensor_window=input_size, lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False):
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_windowing(sensor_window)
    sensor.set_hmirror(sensor_hmirror)
    sensor.set_vflip(sensor_vflip)
    sensor.run(1)

    lcd.init(type=1)
    lcd.rotation(lcd_rotation)
    lcd.clear(lcd.WHITE)

    if not labels:
        with open('labels.txt', 'r') as f:
            exec(f.read())
    if not labels:
        print("no labels.txt")
        img = image.Image(size=(320, 240))
        img.draw_string(90, 110, "no labels.txt", color=(255, 0, 0), scale=2)
        lcd.display(img)
        return 1
    try:
        img = image.Image("startup.jpg")
        lcd.display(img)
    except Exception:
        img = image.Image(size=(320, 240))
        img.draw_string(90, 110, "loading model...", color=(255, 255, 255), scale=2)
        lcd.display(img)

    try:
        task = None
        task = kpu.load(model_addr)
        kpu.init_yolo2(task, 0.5, 0.3, 5, anchors)

        uart = init_uart()
        actions = ['raise_arm', 'squat', 'run', 'one_leg']
        repeat_times = 1000

        for _ in range(repeat_times):
            for action in actions:
                show_action(action)
                if action == "raise_arm":
                    send_command(uart, 'A')  # 發送播放指令
                    wait_duration = 35000
                elif action == "squat":
                    send_command(uart, 'B')  # 發送播放指令
                    wait_duration = 29000
                elif action == "run":
                    send_command(uart, 'C')  # 發送播放指令
                    wait_duration = 15000
                elif action == "one_leg":
                    send_command(uart, 'D')  # 發送播放指令
                    wait_duration = 21000

                start_wait = time.ticks_ms()
                while time.ticks_diff(time.ticks_ms(), start_wait) < wait_duration:
                    detect_action(task, action, uart, wait_duration)

        show_action("End")

    except Exception as e:
        raise e
    finally:
        if task is not None:
            kpu.deinit(task)

if __name__ == "__main__":
    try:
        main(anchors=anchors, labels=labels, model_addr="/sd/sunbone.kmodel")
    except Exception as e:
        sys.print_exception(e)
        lcd_show_except(e)
    finally:
        gc.collect()
