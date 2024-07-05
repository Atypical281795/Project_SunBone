# Human_detect_v3 - By: lzbqr - 周一 6月 22 2020

#本次更新加入了识别特定人的功能，只识别穿蓝色衣服的人
#录像功能,录像存储在SD卡根目录下的vedio文件夹内，由众多连续的小视频组成，每个小视频时长3秒
#物品检测,可以检测包含人体在内的20种物体
'''
使用说明：
1.在第24行 sensor.set_vflip(1)，修改摄像头安装方式，1/0表示正面或反面
2.使用液晶屏时，在第27行，lcd.rotation(0)，修改液晶屏选装角度，0-3每增加1图像旋转90度。
3.第33行，修改LCD_ON来使用或不适应液晶屏。0不使用，1使用。
4.第35行，修改Vedio_ON来进行录像开关，1开启录像，0关闭录像
'''

import sensor,image,lcd,time,video,os
import KPU as kpu
from machine import UART,Timer
from fpioa_manager import fm
import struct

#摄像头初始化
sensor.reset(freq=24000000, set_regs=True, dual_buff=True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

#修改摄像头安装方式：1/0表示正面或反面
sensor.set_vflip(1)
sensor.run(1)
lcd.init() #LCD初始化
lcd.rotation(2)

clock = time.clock()

#调试开关，打开方便调试，关掉略微增加帧率
#lcd显示开关，1使用显示，0不使用LCD
LCD_ON = 1
#录像开关，1开启录像，0关闭录像
Vedio_ON = 1

#注册与飞控通讯的串口
fm.register(6, fm.fpioa.UART1_RX, force=True)
fm.register(7, fm.fpioa.UART1_TX, force=True)

##########################################编写有关Mavlink协议有关的代码#################################

# 设置MAVlink的几个字节的信息
MAV_system_id = 1
MAV_component_id = 1
packet_sequence = 0
MAV_OPTICAL_FLOW_message_id = 76
MAV_OPTICAL_FLOW_extra_crc = 152

#初始化串口
uart = UART(UART.UART1, 115200, read_buf_len=4096)

# 编写计算校验位的函数
def checksum(data, extra):
    output = 0xFFFF
    for i in range(len(data)):
        tmp = data[i] ^ (output & 0xFF)
        tmp = (tmp ^ (tmp << 4)) & 0xFF
        output = ((output >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)) & 0xFFFF
    tmp = extra ^ (output & 0xFF)
    tmp = (tmp ^ (tmp << 4)) & 0xFF
    output = ((output >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)) & 0xFFFF
    return output

# Mavlink协议打包
def send_optical_flow_packet(x, y,flag):
    global packet_sequence
    temp = struct.pack("<fffffffHBBB",x,y,flag,4,5,100,0,31010,0,0,0)#

    #print(len(temp))
    temp = struct.pack("<bbbbb33s",
                       33,
                       packet_sequence & 0xFF,
                       MAV_system_id,
                       MAV_component_id,
                       MAV_OPTICAL_FLOW_message_id,
                       temp)

    #print(len(temp))
    temp = struct.pack("<b38sh",
                       0xFE,
                       temp,
                       checksum(temp, MAV_OPTICAL_FLOW_extra_crc))

    #print(len(temp))

    print (struct.unpack("<bbbbbbfffffffHBBBh",temp))

    print([hex(x) for x in temp])

    packet_sequence += 1

    uart.write(temp)
    return temp

#模型分类，按照class顺序
classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']

#将模型放在SD卡中。
task = kpu.load("/sd/class.kmodel") #模型SD卡上

#网络参数
anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)

#初始化yolo2网络，识别可信概率为0.7（70%）
a = kpu.init_yolo2(task, 0.7, 0.3, 5, anchor)

#创建视频录制对象,录制帧率25帧
if(Vedio_ON):
    vedio_flag=0
    dir_name=os.listdir()
    print(dir_name)
    for i_name in dir_name:
        if i_name == 'vedio':
            vedio_flag=1
    if vedio_flag==0:
        os.mkdir('vedio')
    dir_name=os.listdir()
    print(dir_name)
    i_frame=0
    j_video=1
    v_rec= video.open("/sd/vedio/capture1.avi", record=1, interval=40000, quality=50)

#红色阈值[0],绿色阈值[1],蓝色阈值[2]
rgb_thresholds =[
                (0, 100, 39, 127, 25, 127),
                (0, 80, -70, -10, -0, 30),
                (43, 0, -128, 127, -128, -28)]

while(True):
    clock.tick()
    img = sensor.snapshot()
    res = kpu.run_yolo2(task, img) #运行yolo2网络
    blobs = img.find_blobs([rgb_thresholds[2]])
    a=[0,0,0,0,0,0,0,0]
    if blobs:
        for b in blobs:
            a[7]=b.area()
            if a[7]>a[6]:
                a[6]=a[7]
                a[0:4]=b.rect()
                a[4]=b.cx()
                a[5]=b.cy()
        img.draw_rectangle(a[0:4])
        img.draw_cross(a[4], a[5])
    fps =clock.fps()
    if(LCD_ON):
        #显示帧率
        img.draw_string(2,2, ("%2.1ffps" %(fps)), color=(230,0,0), scale=2)
        #画坐标轴
        img.draw_arrow(int(img.width()/80),int(img.height()/2),int(img.width()-int(img.width()/80)),int(img.height()/2),150,5)
        img.draw_arrow(int(img.width()/2),int(img.height()-int(img.height()/80)),int(img.width()/2),int(img.height()/80),150,5)
        if res:
            for i in res:
                class_type=classes[i.classid()]
                if (class_type=='person'):
                    #计算码中心坐标
                    x=int(i.x()+i.w()/2)
                    y=int(i.y()+i.h()/2)
                    if (abs(x-int(a[4]))<20) and (abs(y-int(a[5]))<30):
                        #框住目标
                        img.draw_rectangle(i.rect(), color = (0, 255, 0),thickness = 2, fill = False)
                        img.draw_cross(x,y,200,10,5)
                        #显示中心点坐标
                        img.draw_string(x+2,y+2, ("(%2.1f,%2.1f)" %((x-(img.width()/2)),((img.height()/2)-y))), color=(230,0,0), scale=2, mono_space=0)
                        #显示标签和置信度
                        img.draw_string(2, 15, classes[i.classid()], color=(230,0,0), scale=2, mono_space=0)
                        img.draw_string(2, 30, "%2.3f"%i.value(), color=(230,0,0), scale=2, mono_space=0)
                        #给飞控发送mavlink帧
                        send_optical_flow_packet((x-(img.width()/2)),((img.height()/2)-y),1)
                    else:
                        send_optical_flow_packet(0,0,0)
                else:
                    send_optical_flow_packet(0,0,0)
        else:
            send_optical_flow_packet(0,0,0)
        lcd.display(img)
    else :
        print(fps)
        if res:
            for i in res:
                a=classes[i.classid()]
                if (a=='person'):
                    #计算码中心坐标，并画出中心点
                    x=int(i.x()+i.w()/2)
                    y=int(i.y()+i.h()/2)
                    #给飞控发送mavlink帧
                    send_optical_flow_packet((x-(img.width()/2)),((img.height()/2)-y),1)
                else:
                    send_optical_flow_packet(0,0,0)
        else:
            send_optical_flow_packet(0,0,0)
    if(Vedio_ON):
        tim = time.ticks_ms()
        img_len = v_rec.record(img)
        print("record",j_video,i_frame,time.ticks_ms() - tim)
        i_frame += 1
        if i_frame == 75:
            print("finish:",j_video)
            j_video+=1
            v_rec.record_finish()
            i_frame=0
            v_rec = video.open("/sd/vedio/capture"+str(j_video)+".avi", record=1, interval=40000, quality=50)
    del a[:]
