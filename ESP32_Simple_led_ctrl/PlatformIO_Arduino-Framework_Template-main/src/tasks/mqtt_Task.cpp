#include "mqtt_Task.h"
#include "led_Task.h"

//* UNBLOCK BELOW TO CONNECT TO ADAFRUIT */
// Adafruit IO MQTT credentials
// const char* mqttServer = "io.adafruit.com";
// const int mqttPort = 1883;
// const char* mqttUser = "";  // Replace with your Adafruit IO username
// const char* mqttKey = "";  // Replace with your Adafruit IO key
// const char* feedName = "";  // Replace with your feed name

WiFiClient wifiClient;
Adafruit_MQTT_Client mqttClient(&wifiClient, mqttServer, mqttPort, mqttUser, mqttKey);
Adafruit_MQTT_Subscribe ledControl = Adafruit_MQTT_Subscribe(&mqttClient, feedName);

// Function to connect to the MQTT broker
void connectToMqtt() {
  int8_t ret;
  while ((ret = mqttClient.connect()) != 0) {  // connect will return 0 for success
    Serial.println(mqttClient.connectErrorString(ret));
    Serial.println("Retrying MQTT connection in 5 seconds...");
    mqttClient.disconnect();
    delay(5000);  // wait 5 seconds
  }
  Serial.println("MQTT Connected!");
}

// Callback function to handle incoming messages
// Updated function signature to accept const char* for topic
void mqttCallback(const char* topic, uint8_t* payload, uint16_t length) {
  char message[length + 1];
  memcpy(message, payload, length);
  message[length] = '\0';  // Null-terminate the string

  Serial.print("Message received: ");
  Serial.println(message);

  // Control the LED based on the message
  if (strcmp(message, "1") == 0) {
    pixels.setPixelColor(0, pixels.Color(0, 0, 255));  // Turn LED on (blue)
    pixels.show();
    Serial.println("LED is ON");
  } else if (strcmp(message, "0") == 0) {
    pixels.setPixelColor(0, pixels.Color(0, 0, 0));  // Turn LED off
    pixels.show();
    Serial.println("LED is OFF");
  } else {
    Serial.println("Invalid payload");
  }
}


// Task to handle MQTT communication
void mqttTask(void *pvParameters) {
  mqttClient.subscribe(&ledControl);

  while (1) {
    if (!mqttClient.connected()) {
      connectToMqtt();  // Connect if disconnected
    }
    //mqttClient.processPackets(100);  // Check for new packets (100ms processing time)
    // Check for new messages
    Adafruit_MQTT_Subscribe *subscription;
    while ((subscription = mqttClient.readSubscription(5000))) {
      if (subscription == &ledControl) {
        mqttCallback(ledControl.topic, (uint8_t *)ledControl.lastread, strlen((char *)ledControl.lastread));
      }
    }

    mqttClient.processPackets(10000);  // Process any remaining packets
    mqttClient.ping();  // Keep the connection alive
    vTaskDelay(100 / portTICK_PERIOD_MS);  // Delay to avoid flooding the server
  }
}


// Function to create the MQTT task
void createMqttTask() {
  xTaskCreate(mqttTask, "MqttTask", 4096, NULL, 2, NULL);
}
