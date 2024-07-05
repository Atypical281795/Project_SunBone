#include <HardwareSerial.h>
#include "DFRobotDFPlayerMini.h"

HardwareSerial myHardwareSerial(1); //ESP32可宣告需要一個硬體序列，軟體序列會出錯
HardwareSerial SerialPort(2); // 使用UART2
DFRobotDFPlayerMini myDFPlayer;//啟動DFPlayer撥放器
char data;

void setup() {
  //ESP32_UART端口設定//
  Serial.begin(115200);  // 用于调试输出
  SerialPort.begin(115200, SERIAL_8N1, 16, 17); // RX:16, TX:17
  myHardwareSerial.begin(9600, SERIAL_8N1, 12, 13); // Serial的TX,RX
  ////
  Serial.println("Initializing DFPlayer ... (May take 1-2 seconds)");
  myDFPlayer.begin(myHardwareSerial);//將DFPlayer播放器宣告在HardwareSerial控制
  delay(500);
  myDFPlayer.volume(10);  //設定聲音大小（0-30）

  // 等待串口监视器连接
  while (!Serial) {
    ;
  }
  Serial.println("ESP32 准备就绪");
}

void loop() {
    data = SerialPort.read();
  if(SerialPort.available())
  {
    switch(data)
    {
      case 'A':
        Serial.println("test1");
        myDFPlayer.playMp3Folder(1);  //播放mp3內的0001.mp3 3秒鐘
        delay(15000);
        myDFPlayer.pause();
        break;
      case 'B':
        Serial.println("test2");
        myDFPlayer.playMp3Folder(2);  //播放mp3內的0001.mp3 3秒鐘
        delay(15000);
        myDFPlayer.pause();
        break;
      case 'C':
        Serial.println("test3");
        myDFPlayer.playMp3Folder(3);  //播放mp3內的0001.mp3 3秒鐘
        delay(15000);
        myDFPlayer.pause();
        break;
      case 'D':
        Serial.println("test4");
        myDFPlayer.playMp3Folder(4);  //播放mp3內的0001.mp3 3秒鐘
        delay(15000);
        myDFPlayer.pause();
        break;
    }
  }
  if (SerialPort.available()) {
    String receivedData = SerialPort.readStringUntil('\n');
    Serial.println("收到: " + receivedData);
    SerialPort.println("ESP32收到: " + receivedData);
  }
  
  
  // 定期发送消息以保持连接活跃
  static unsigned long lastSendTime = 0;
  if (millis() - lastSendTime > 5000) {  // 每5秒
    SerialPort.println("ESP32 心跳");
    lastSendTime = millis();
  }
}