#include "wifi_Task.h"

const char* ssid = "DCrab";
const char* password = "zzzzzzzz";

void wifiTask(void *pvParameters) {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    vTaskDelay(1000 / portTICK_PERIOD_MS);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println(WiFi.localIP());
  vTaskDelete(NULL);  // Delete the task when done
}

void createWifiTask() {
  xTaskCreate(wifiTask, "WiFiTask", 4096, NULL, 1, NULL);
}