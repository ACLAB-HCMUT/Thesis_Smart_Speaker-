// Import required libraries
#include "ESPAsyncWebServer.h"
#include "SPIFFS.h"
#include "DHT20.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

// Import tasks
#include "tasks/led_Task.h"  
#include "tasks/mqtt_Task.h"
#include "tasks/mqtt_tx_Task.h"
#include "tasks/temp_Task.h"
#include "tasks/wifi_Task.h"

void setup(){
  Serial.begin(115200);  // Initialize Serial communication
  Serial.println("Starting here");

  createWifiTask();  // Initialize Wi-Fi task
  createTempTask();  // Initialize temperature task
  createMqttTask();  // Initialize MQTT task
  createMQTT_TX();  // Initialize MQTT_Tx task
}
void loop(){
  // Nothing to do here, FreeRTOS tasks handle the work
}
