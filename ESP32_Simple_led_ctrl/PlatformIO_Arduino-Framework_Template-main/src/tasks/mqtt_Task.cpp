#include "mqtt_Task.h"
#include "led_Task.h"
#include "fan_Task.h"

// Adafruit IO MQTT 
const char* mqttServer = "io.adafruit.com";
const int mqttPort = 1883;
const char* mqttUser = "duongwt16";
const char* mqttKey = "aio_jhVF48MzfamQgz6wSIwMH0rqIXYm";


// Feed names
const char* feedNames[] = {
    "duongwt16/feeds/bedroom.main-light",
    "duongwt16/feeds/bedroom.sub-light",  
    "duongwt16/feeds/bedroom.fan",
    "duongwt16/feeds/living-room.main-light",
    "duongwt16/feeds/living-room.sub-light",  
    "duongwt16/feeds/living-room.fan"
};

// Feed subscriptions array
const int numFeeds = sizeof(feedNames) / sizeof(feedNames[0]);
Adafruit_MQTT_Subscribe* feeds[numFeeds];
WiFiClient wifiClient;
Adafruit_MQTT_Client mqttClient(&wifiClient, mqttServer, mqttPort, mqttUser, mqttKey);

// Function to initialize feeds
void setupFeeds() {
  for (int i = 0; i < numFeeds; i++) {
    feeds[i] = new Adafruit_MQTT_Subscribe(&mqttClient, feedNames[i]);
    mqttClient.subscribe(feeds[i]);
  }
}

// MQTT connection function
void connectToMqtt() {
  while (mqttClient.connect() != 0) {
    Serial.println("Failed to connect to MQTT, retrying...");
    delay(3000);
  }
  Serial.println("MQTT Connected!");
}
 
// Callback to handle feed messages based on topic
void handleFeedMessage(const char* topic, const char* message) {
  if (strcmp(topic, feedNames[0]) == 0) {
    led_handle1(0, message);
  } else if (strcmp(topic, feedNames[1]) == 0) {
    led_handle1(1, message);
  } else if (strcmp(topic, feedNames[2]) == 0) {
    fan_handle(message);
  } else if (strcmp(topic, feedNames[3]) == 0) {
    led_handle2(0, message);
  } else if (strcmp(topic, feedNames[4]) == 0) {
    led_handle2(1, message);
  } else if (strcmp(topic, feedNames[5]) == 0) {
    fan_handle(message);
  }
  Serial.printf(" %s: %s\n", topic, message);
}

// MQTT task for handling multiple feeds
void mqttTask(void *pvParameters) {
  setupFeeds();  // Initialize and subscribe to feeds
  while (1) {
    if (!mqttClient.connected()) {
      connectToMqtt();
    }
    // Read and process each feed subscription
    Adafruit_MQTT_Subscribe *subscription;
    if ((subscription = mqttClient.readSubscription(10))) {
      for (int i = 0; i < numFeeds; i++) {
        if (subscription == feeds[i]) {
          handleFeedMessage(feeds[i]->topic, (char *)feeds[i]->lastread);
        }
      }
    }
    mqttClient.processPackets(10);
    mqttClient.ping();
    vTaskDelay(10 / portTICK_PERIOD_MS);
  }
}

// Create MQTT task
void createMqttTask() {
  xTaskCreate(mqttTask, "MqttTask", 4096, NULL, 1, NULL);
}