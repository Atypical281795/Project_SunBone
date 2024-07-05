import sensor, image, lcd, time
import KPU as kpu
from machine import UART
import gc, sys
from fpioa_manager import fm
#上述模組提供了攝像頭（sensor）、圖像處理（image）、LCD顯示（lcd）、時間管理（time）、KPU運算（kpu）、UART通信（UART）、垃圾回收（gc）、系統功能（sys）和FPIOA管理（fm）的功能。

input_size = (224, 224)
labels = ['raise_arm', 'squat', 'run', 'one_leg', 'other']
anchors = [3.44, 4.31, 2.94, 3.19, 1.19, 3.59, 1.81, 4.12, 2.81, 2.84]
#定義了輸入圖像的尺寸、動作標籤和錨點（anchors）

def lcd_show_except(e):
    import uio
    err_str = uio.StringIO()
    sys.print_exception(e, err_str)
    err_str = err_str.getvalue()
    img = image.Image(size=input_size)
    img.draw_string(0, 10, err_str, scale=1, color=(0xff,0x00,0x00))
    lcd.display(img)
#這個函數用於在LCD上顯示異常信息

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
#通過UART發送檢測結果

def init_uart():
    fm.register(10, fm.fpioa.UART1_TX, force=True)
    fm.register(11, fm.fpioa.UART1_RX, force=True)
    uart = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=256)
    return uart
#配置並初始化UART

def show_action(action, duration=2000):
    lcd.clear(lcd.WHITE)
    img = image.Image(size=(320, 240))
    img.draw_string(90, 110, action, color=(255, 0, 0), scale=2)
    lcd.display(img)
    time.sleep_ms(duration)
#在LCD上顯示當前的動作名稱

def detect_action(task, action_label, duration=10000):
    start_time = time.ticks_ms()
    uart = init_uart()
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

#            if action_label in detected_labels:
#                lcd.draw_string(10, img.height() - 30, "correct", scale=1, color=(0, 255, 0))
#            else:
#                lcd.draw_string(10, img.height() - 30, "mistake", scale=1, color=(255, 0, 0))

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
#執行動作檢測，並在LCD上顯示結果，同時通過UART發送檢測到的對象

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
        kpu.init_yolo2(task, 0.5, 0.3, 5, anchors)  # threshold:[0,1], nms_value: [0, 1]

#        actions = ['raise_arm', 'squat', 'run', 'one_leg']
#        for action in actions:
#           show_action(action)
#            detect_action(task, action)
#        show_action("End")

        actions = ['raise_arm', 'squat', 'run', 'one_leg']
        repeat_times = 50
        for _ in range(repeat_times):
            for action in actions:
                show_action(action)
                detect_action(task, action)
        show_action("End")


    except Exception as e:
        raise e
    finally:
        if task is not None:
            kpu.deinit(task)

if __name__ == "__main__":
    try:
        main(anchors=anchors, labels=labels, model_addr="/sd/model-132194.kmodel")
    except Exception as e:
        sys.print_exception(e)
        lcd_show_except(e)
    finally:
        gc.collect()
#主函數，初始化攝像頭和LCD顯示屏，並加載KPU模型。之後，依次顯示和檢測定義好的動作。如果出現異常，會在LCD上顯示錯誤信息，並進行垃圾回收
