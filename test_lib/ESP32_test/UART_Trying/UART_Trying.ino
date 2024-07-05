#include "DFRobotDFPlayerMini.h"

HardwareSerial myHardwareSerial(1); //ESP32可宣告需要一個硬體序列，軟體序列會出錯
HardwareSerial K210Serial(2); //ESP32可宣告需要一個硬體序列，軟體序列會出錯
DFRobotDFPlayerMini myDFPlayer;//啟動DFPlayer撥放器
String data;

void setup()
{
  //啟動mp3連線
  K210Serial.begin(115200, SERIAL_8N1, 16, 17);
  myHardwareSerial.begin(9600, SERIAL_8N1, 12, 13); 
  //實際上只用到TX傳送指令，因此RX可不接（接收player狀態）
  myDFPlayer.begin(myHardwareSerial);//將DFPlayer播放器宣告在HardwareSerial控制
  delay(500);
  myDFPlayer.volume(15);  //設定聲音大小（0-30）
}

void loop()
{
  data = K210Serial.readString();
  if(K210Serial.available())
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
      case 'E':
        Serial.println("pause");
        myDFPlayer.pause();
        break;
    }
  }
}