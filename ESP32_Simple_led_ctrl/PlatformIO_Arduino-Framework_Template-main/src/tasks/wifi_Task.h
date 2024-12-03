// wifi_task.h
#ifndef WIFI_TASK_H
#define WIFI_TASK_H

#include "Arduino.h"
#include <Wire.h>
#include "WiFi.h"

void wifiTask(void *pvParameters);
void createWifiTask();

#endif // WIFI_TASK_H