// led_Task.cpp
#include "led_Task.h"

Adafruit_NeoPixel pixels(4, 8, NEO_GRB + NEO_KHZ800);
// Task để xử lý input từ Serial để điều khiển LED
void led_handle(int ledIndex, const char* message) {
  if (strcmp(message, "ON") == 0) {
    pixels.setPixelColor(ledIndex, pixels.Color(255, 255, 255));
  } else if (strcmp(message, "OFF") == 0) {
    pixels.setPixelColor(ledIndex, pixels.Color(0, 0, 0));
  }
  pixels.show();
}
