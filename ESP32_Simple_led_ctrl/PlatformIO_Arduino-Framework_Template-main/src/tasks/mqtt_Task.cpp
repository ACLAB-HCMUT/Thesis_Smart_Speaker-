#include "mqtt_Task.h"
#include "led_Task.h"
#include "fan_Task.h"
// Adafruit IO MQTT 
const char* mqttServer = "io.adafruit.com";
const int mqttPort = 1883;
const char* mqttUser = "duongwt16";
const char* mqttKey = "aio_rpEG821XN1vVIRtdJ7ZEMhBsEldc";


// Feed names
const char* feedNames[] = {
    "duongwt16/feeds/led1",
    "duongwt16/feeds/led2",  
    "duongwt16/feeds/fan"
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
    delay(1000);
  }
  Serial.println("MQTT Connected!");
}

// Callback to handle feed messages based on topic
void handleFeedMessage(const char* topic, const char* message) {
  if (strcmp(topic, feedNames[0]) == 0) {
    // Handle LED feed
    // if (strcmp(message, "ON") == 0) {
    //   pixels.setPixelColor(0, pixels.Color(0, 0, 255));  // LED on
    // } else if (strcmp(message, "OFF") == 0) {
    //   pixels.setPixelColor(0, pixels.Color(0, 0, 0));    // LED off
    // }
    // pixels.show();
    led_handle(0, message);
  } else if (strcmp(topic, feedNames[1]) == 0) {
    // Handle second LED feed (or any other function for different feed)
    // Add control logic for the second feed here
    // Handle LED feed
    // if (strcmp(message, "ON") == 0) {
    //   pixels.setPixelColor(1, pixels.Color(0, 255, 0));  // LED on
    // } else if (strcmp(message, "OFF") == 0) {
    //   pixels.setPixelColor(1, pixels.Color(0, 0, 0));    // LED off
    // }
    // pixels.show();
    led_handle(1, message);
  } else if (strcmp(topic, feedNames[2]) == 0) {
    // Handle fan feed
    if (strcmp(message, "ON") == 0) {
      turnFanOn();  // Turn fan on
    } else if (strcmp(message, "OFF") == 0) {
      turnFanOff();  // Turn fan off
    }
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
  xTaskCreate(mqttTask, "MqttTask", 4096, NULL, 2, NULL);
}
