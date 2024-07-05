#include <HardwareSerial.h>
#include "DFRobotDFPlayerMini.h"

HardwareSerial myHardwareSerial(1); //ESP32可宣告需要一個硬體序列，軟體序列會出錯
HardwareSerial SerialPort(2); // 使用UART2
DFRobotDFPlayerMini myDFPlayer;//啟動DFPlayer播放器

void setup() 
{
  //ESP32_UART端口設定//
  Serial.begin(115200);  // 用于调试输出
  SerialPort.begin(115200, SERIAL_8N1, 3, 1); // RX:3, TX:1
  myHardwareSerial.begin(9600, SERIAL_8N1, 16, 17); // Serial的TX,RX
  ////
  Serial.println("Initializing DFPlayer ... (May take 1-2 seconds)");
  if (!myDFPlayer.begin(myHardwareSerial)) {  //將DFPlayer播放器宣告在HardwareSerial控制
    Serial.println("DFPlayer Mini initialization failed!");
    while(true);
  }
  delay(500);
  myDFPlayer.volume(10);  //設定聲音大小（0-30）
  Serial.println("ESP32 准备就绪");
}

void loop() 
{
  static unsigned long lastPlayTime = 0;
  static bool isPlaying = false;

  if (SerialPort.available()) 
  {
    String receivedData = SerialPort.readStringUntil('\n');
    Serial.println("收到: " + receivedData);
    if (receivedData == "A") 
    {
      Serial.println("test1");
      myDFPlayer.playMp3Folder(1);  //播放mp3內的0001.mp3
      lastPlayTime = millis();
      isPlaying = true;
    } 
    else if (receivedData == "B") 
    {
      Serial.println("test2");
      myDFPlayer.playMp3Folder(2);  //播放mp3內的0001.mp3
      lastPlayTime = millis();
      isPlaying = true;
    } 
    else if (receivedData == "C") 
    {
      Serial.println("test3");
      myDFPlayer.playMp3Folder(3);  //播放mp3內的0001.mp3
      lastPlayTime = millis();
      isPlaying = true;
    } 
    else if (receivedData == "D") 
    {
      Serial.println("test4");
      myDFPlayer.playMp3Folder(4);  //播放mp3內的0001.mp3
      lastPlayTime = millis();
      isPlaying = true;
    }
  }

  if (isPlaying && millis() - lastPlayTime >= 15000) {
    myDFPlayer.pause();
    isPlaying = false;
  }
}