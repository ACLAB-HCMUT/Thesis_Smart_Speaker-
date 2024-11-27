#ifndef FAN_TASK_H
#define FAN_TASK_H

#include <Arduino.h>

// Pin definitions
#define FAN_PIN 8

// Function prototypes
void setupFan();
void setFanSpeed(uint8_t speed);
void fan_handle(const char* message);

#endif // FAN_TASK_H