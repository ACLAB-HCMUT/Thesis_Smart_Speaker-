// led_Task.cpp
#include "led_Task.h"

Adafruit_NeoPixel pixels1(4, 8 , NEO_GRB + NEO_KHZ800); // D5-D6
Adafruit_NeoPixel pixels2(4, 10, NEO_GRB + NEO_KHZ800); // D7-D8


void led_handle1(int ledIndex, const char* message) {
  if (strcmp(message, "ON") == 0) {
    pixels1.setPixelColor(ledIndex, pixels1.Color(255, 255, 255));
  } else if (strcmp(message, "OFF") == 0) {
    pixels1.setPixelColor(ledIndex, pixels1.Color(0, 0, 0));
  }
  pixels1.show();
}

void led_handle2(int ledIndex, const char* message) {
  if (strcmp(message, "ON") == 0) {
    pixels2.setPixelColor(ledIndex, pixels2.Color(255, 255, 255));
  } else if (strcmp(message, "OFF") == 0) {
    pixels2.setPixelColor(ledIndex, pixels2.Color(0, 0, 0));
  }
  pixels2.show();
}
