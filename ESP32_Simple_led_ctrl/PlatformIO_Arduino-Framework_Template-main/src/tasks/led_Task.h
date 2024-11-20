// led_Task.h

#ifndef LED_TASK_H
#define LED_TASK_H

#include "Arduino.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include <Adafruit_NeoPixel.h>


extern Adafruit_NeoPixel pixels;
// Hàm khởi tạo task nhận input từ Serial để điều khiển LED
void led_handle(int ledIndex, const char* message);
#endif // LED_TASK_H
