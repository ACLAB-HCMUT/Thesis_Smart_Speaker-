
// Import required libraries
#include "WiFi.h"
#include "ESPAsyncWebServer.h"
#include "SPIFFS.h"
#include "DHT20.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "tasks/led_Task.h"  // Include file task led
#include "tasks/mqtt_Task.h"
// Replace with your network credentials
// const char* ssid = PROJECT_WIFI_SSID;
// const char* password = PROJECT_WIFI_PASSWORD;

const char* ssid = "ACLAB";
const char* password = "ACLAB2023";


// Set LED GPIO
const int ledPin = 21;
// Stores LED state

// Task to handle Wi-Fi connection
void wifiTask(void *pvParameters) {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    vTaskDelay(1000 / portTICK_PERIOD_MS);
    Serial.println("Connecting to WiFi..");
  }

  // Print ESP32 Local IP Address
  Serial.println(WiFi.localIP());
  vTaskDelete(NULL);  // Delete the task when done
}

void setup(){
  Serial.begin(115200);  // Initialize Serial communication
  xTaskCreate(wifiTask, "WiFiTask", 4096, NULL, 1, NULL);
  // Create tasks for Wi-Fi and MQTT
  
  createMqttTask();  // Initialize MQTT task
  //createSingleLedTask();
}
void loop(){
  // Nothing to do here, FreeRTOS tasks handle the work
}
