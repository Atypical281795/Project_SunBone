//DFRobotDFPlayerMini函式庫下載：https://github.com/DFRobot/DFRobotDFPlayerMini
#include "DFRobotDFPlayerMini.h"
HardwareSerial myHardwareSerial(1); //ESP32可宣告需要一個硬體序列，軟體序列會出錯
HardwareSerial K210Serial2(2); //ESP32可宣告需要一個硬體序列，軟體序列會出錯
DFRobotDFPlayerMini myDFPlayer;//啟動DFPlayer撥放器
void printDetail(uint8_t type, int value);//宣告播放控制程式

# define ACTIVATED LOW
boolean isPlaying = false;

float sensorVoltage; 
float sensorValue;

void setup()
{
  Serial.begin(115200);
  //啟動mp3連線
  myHardwareSerial.begin(9600, SERIAL_8N1, 13, 12); // Serial的TX,RX
  K210Serial2.begin(115200, SERIAL_8N1, 27, 26);
  delay(300);
  if (!myDFPlayer.begin(myHardwareSerial)) {  //Use softwareSerial to communicate with mp3.
    Serial.println(F("Unable to begin:"));
    Serial.println(F("1.Please recheck the connection!"));
    Serial.println(F("2.Please insert the SD card!"));
    while(true);
  }
  Serial.println(F("MP3 Player online."));
  
  myDFPlayer.setTimeOut(500); //Set serial communictaion time out 500ms
   myDFPlayer.volume(30);  //Set volume value (0~30).
  myDFPlayer.EQ(DFPLAYER_EQ_NORMAL);
}

void loop()
{
  sensorValue = analogRead(34);
  sensorVoltage = (sensorValue/1024*5)*1000;
  Serial.print("sensor voltage = ");
  Serial.print(sensorVoltage);
  Serial.println(" mV");
  if(K210Serial2.available())
  {
    String receivedData = K210Serial2.readStringUntil('\n');
    Serial.println("收到: " + receivedData);
    if (receivedData == "A") 
    {
      Serial.println("test1");
      myDFPlayer.playMp3Folder(1);  //播放mp3內的0001.mp3
      delay(5000);
      myDFPlayer.pause();
    } 
    else if (receivedData == "B") 
    {
      Serial.println("test2");
      myDFPlayer.playMp3Folder(2);  //播放mp3內的0001.mp3
      delay(5000);
      myDFPlayer.pause();
    } 
    else if (receivedData == "C") 
    {
      Serial.println("test3");
      myDFPlayer.playMp3Folder(3);  //播放mp3內的0001.mp3
      delay(5000);
      myDFPlayer.pause();
    } 
    else if (receivedData == "D") 
    {
      Serial.println("test4");
      myDFPlayer.playMp3Folder(4);  //播放mp3內的0001.mp3
      delay(5000);
      myDFPlayer.pause();
    }
  }
  if ((sensorVoltage > 696) &&(sensorVoltage < 795))
  {
    myDFPlayer.play(5);
    delay(5000); 
    myDFPlayer.pause();
  }
  else if((sensorVoltage > 795)||(sensorVoltage == 795))
  {
    myDFPlayer.play(6);
    delay(5000); 
    myDFPlayer.pause();
  }
  delay(100);
}
