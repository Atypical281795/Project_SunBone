#include "DFRobotDFPlayerMini.h"

int ultra; // 紫外線感測數據
unsigned long startMillis; // 計時開始時間
const unsigned long thresholdTime = 10000; // 門檻時間 10 秒 (10000 毫秒)
bool isAboveThreshold = false; // 是否超過門檻時間
HardwareSerial myHardwareSerial(1); // ESP32 硬體序列

DFRobotDFPlayerMini myDFPlayer; // 啟動 DFPlayer 播放器

void setup() {
  Serial.begin(9600);

  // 初始化紫外線感測引腳
  pinMode(14, OUTPUT);
  digitalWrite(14, HIGH);

  // 啟動 MP3 連線
  myHardwareSerial.begin(9600, SERIAL_8N1, 12, 13); // Serial 的 TX, RX
  Serial.println("Initializing DFPlayer ... (May take 1-2 seconds)");
  myDFPlayer.begin(myHardwareSerial); // 將 DFPlayer 播放器宣告在 HardwareSerial 控制
  delay(500);
  myDFPlayer.volume(30); // 設定聲音大小（0-30）
}

void loop() {
  ultra = analogRead(14) / 4;
  Serial.println(ultra);
  delay(500);

  if (ultra > 600) {
    if (!isAboveThreshold) {
      startMillis = millis(); // 記錄開始時間
      isAboveThreshold = true;
    }
    if (millis() - startMillis >= thresholdTime) {
      Serial.println("紫外線過量");
      myDFPlayer.playMp3Folder(1); // 播放 mp3 內的 0001.mp3
      delay(15000); // 播放 15 秒
      myDFPlayer.pause();
      isAboveThreshold = false; // 重置標誌
    }
  } else {
    isAboveThreshold = false; // 重置標誌
  }
}
