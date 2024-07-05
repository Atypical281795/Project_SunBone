#include "DFRobotDFPlayerMini.h"
HardwareSerial myHardwareSerial(1); // ESP32硬件串行1
DFRobotDFPlayerMini myDFPlayer;

void setup()
{
  Serial.begin(115200);
  myHardwareSerial.begin(9600, SERIAL_8N2, 12, 13); // Serial的TX,RX
  Serial.println("Initializing DFPlayer ... (May take 1-2 seconds)");

  while (myDFPlayer.begin(myHardwareSerial)==false) {
    Serial.println("Unable to begin: ");
    Serial.println("1. Please recheck the connection!");
    Serial.println("2. Please insert the SD card!");
    Serial.begin(115200);
    myHardwareSerial.begin(9600, SERIAL_8N2, 12, 13); // Serial的TX,RX
    if(myDFPlayer.begin(myHardwareSerial)==true)
      break;
  }
  Serial.println("DFPlayer Mini online.");
  
  myDFPlayer.volume(30);  // 设置声音大小（0-30）
}

void loop()
{
  Serial.println("Playing track 0001 from mp3 folder");
  myDFPlayer.playMp3Folder(1);  // 播放mp3内的0001.mp3
  delay(15000); // 延迟15秒
  myDFPlayer.pause();
  delay(5000); // 延迟5秒
}
