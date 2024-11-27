#include "fan_Task.h"

void setupFan() {
    pinMode(FAN_PIN, OUTPUT);
    analogWrite(FAN_PIN, 0);
}


void setFanSpeed(uint8_t speed) {
    if (speed > 255) {
        speed = 255;
    }
    analogWrite(FAN_PIN, speed);
}

void fan_handle(const char* message) {
    if (strcmp(message, "ON") == 0) {
        analogWrite(FAN_PIN, 60);  // Turn fan on
    } else if (strcmp(message, "OFF") == 0) {
        analogWrite(FAN_PIN, 60);  // Turn fan off
    }
}