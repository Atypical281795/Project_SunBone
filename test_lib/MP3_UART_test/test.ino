#include <HardwareSerial.h>

HardwareSerial SerialPort(2); // 使用UART2

void setup() {
  Serial.begin(115200);  // 用于调试输出
  SerialPort.begin(115200, SERIAL_8N1, 16, 17); // RX:16, TX:17
  
  // 等待串口监视器连接
  while (!Serial) {
    ;
  }
  Serial.println("ESP32 准备就绪");
}

void loop() {
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