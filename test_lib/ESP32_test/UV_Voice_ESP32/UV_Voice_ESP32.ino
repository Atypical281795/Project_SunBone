#include "DFRobotDFPlayerMini.h"

HardwareSerial myHardwareSerial(1); //ESP32可宣告需要一個硬體序列，軟體序列會出錯
DFRobotDFPlayerMini myDFPlayer; //啟動DFPlayer撥放器

void setup() {
  Serial.begin(115200);

  //啟動mp3連線
  myHardwareSerial.begin(9600, SERIAL_8N1, 27, 25); // Serial的TX,RX
  Serial.println("Initializing DFPlayer ... (May take 1-2 seconds)");

  if (!myDFPlayer.begin(myHardwareSerial)) { //將DFPlayer播放器宣告在HardwareSerial控制
    Serial.println("Unable to begin:");
    Serial.println("1.Please recheck the connection!");
    Serial.println("2.Please insert the SD card!");
    while (true);
  }
  Serial.println("DFPlayer Mini online.");

  myDFPlayer.volume(30);  //設定聲音大小（0-30）
}

void loop() {
  static int currentTrack = 1; // 用於追踪當前播放的曲目
  static unsigned long lastChangeTime = 0; // 用於計時

  // 每隔5秒切換到下一個曲目
  if (millis() - lastChangeTime > 5000) {
    myDFPlayer.playMp3Folder(currentTrack);  //播放mp3內的指定曲目
    Serial.print("Playing track: ");
    Serial.println(currentTrack);
    
    currentTrack++; // 切換到下一個曲目
    lastChangeTime = millis(); // 重置計時器

    // 如果曲目超過了SD卡中的數量（假設最多有10首曲目）
    if (currentTrack > 10) {
      currentTrack = 1; // 重新從第一首曲目開始
    }
  }
}
