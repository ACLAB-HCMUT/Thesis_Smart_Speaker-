// led_Task.cpp

#include "led_Task.h"
Adafruit_NeoPixel pixels(1, 45, NEO_GRB + NEO_KHZ800);
// Task để xử lý input từ Serial để điều khiển LED
void ledTask(void *pvParameters) {
  int ledPin = *((int *) pvParameters);  // Lấy giá trị ledPin từ pvParameters
  while(1) {
    if (Serial.available() > 0) {
      char input = Serial.read();  // Đọc ký tự từ Serial
      if (input == '1') {
        //digitalWrite(ledPin, HIGH);  // Bật đèn LED
        pixels.setPixelColor(0,pixels.Color(0, 0, 255));
        pixels.show();
        Serial.println("LED is ON");
      } 
      else if (input == '0') {
        //digitalWrite(ledPin, LOW);   // Tắt đèn LED
        pixels.setPixelColor(0,pixels.Color(0, 0, 0));
        pixels.show();
        Serial.println("LED is OFF");
      } else {
        Serial.println("Invalid input! Enter '1' to turn ON, '0' to turn OFF");
      }
    }
    vTaskDelay(100 / portTICK_PERIOD_MS);  // Độ trễ để giảm tải hệ thống
  }
}

// Hàm tạo task
void createLedTask(int ledPin) {
  // Tạo task nhận input từ Serial với tham số ledPin
  xTaskCreate(ledTask, "LedTask", 2048, &ledPin, 1, NULL);
}