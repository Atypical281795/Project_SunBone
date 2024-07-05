#include "DFRobotDFPlayerMini.h"

HardwareSerial myHardwareSerial(1); //ESP32可宣告需要一個硬體序列，軟體序列會出錯
DFRobotDFPlayerMini myDFPlayer;//啟動DFPlayer撥放器

void setup()
{
  //啟動mp3連線
  myHardwareSerial.begin(9600, SERIAL_8N1, 12, 13); // Serial的TX,RX
  //實際上只用到TX傳送指令，因此RX可不接（接收player狀態）
  Serial.println("Initializing DFPlayer ... (May take 1-2 seconds)");
  myDFPlayer.begin(myHardwareSerial);//將DFPlayer播放器宣告在HardwareSerial控制
  delay(500);
  myDFPlayer.volume(30);  //設定聲音大小（0-30）
}

void loop()
{
  Serial.println("test1");
  myDFPlayer.playMp3Folder(1);  //播放mp3內的0001.mp3 3秒鐘
  delay(15000);
  myDFPlayer.pause();
}