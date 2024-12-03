// led_Task.h

#ifndef LED_TASK_H
#define LED_TASK_H

#include "Arduino.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include <Adafruit_NeoPixel.h>


extern Adafruit_NeoPixel pixels1;
extern Adafruit_NeoPixel pixels2;


void led_handle1(int ledIndex, const char* message);
void led_handle2(int ledIndex, const char* message);


#endif // LED_TASK_H