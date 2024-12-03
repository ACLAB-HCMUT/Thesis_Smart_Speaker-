#ifndef TEMP_TASK_H
#define TEMP_TASK_H

#include <DHT20.h>
#include <Wire.h>
#include "LiquidCrystal_I2C.h"
extern DHT20 dht20; // I2C address
void tempTask(void *pvParameters);
void createTempTask();
float getTemp();
float getMois();

#endif // TEMP_TASK_H