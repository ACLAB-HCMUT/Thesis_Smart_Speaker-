#include "fan_Task.h"

// Function to initialize the fan
void setupFan() {
    pinMode(FAN_PIN, OUTPUT);
    analogWrite(FAN_PIN, 0); // Start with the fan off
}

// Function to set the fan speed
void setFanSpeed(uint8_t speed) {
    // Ensure the speed is between 0 and 255
    if (speed > 255) {
        speed = 255;
    }
    analogWrite(FAN_PIN, speed);
}

// Function to turn the fan on
void turnFanOn() {
    analogWrite(FAN_PIN, 150); // Set fan speed to maximum
}

// Function to turn the fan off
void turnFanOff() {
    analogWrite(FAN_PIN, 0); // Set fan speed to 0
}