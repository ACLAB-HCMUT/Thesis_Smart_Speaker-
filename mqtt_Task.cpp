#include "mqtt_Task.h"
#include "led_Task.h"
#include "fan_Task.h"
#include "PubSubClient.h"
#include "Wire.h"
// Adafruit IO MQTT 
const char* mqttServer = "172.30.201.231";
const int mqttPort = 1883;
// extern const char* ssid;
// extern const char* password;
// **********************************************************//

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;



void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Feel free to add more if statements to control more GPIOs with MQTT

  // If a message is received on the topic esp32/output, you check if the message is either "on" or "off". 
  // Changes the output state according to the message
  if (String(topic) == "esp32/output") {
    Serial.print("Changing output to ");
    if(messageTemp == "on"){
      Serial.println("on");
      pixels.setPixelColor(0, pixels.Color(0, 0, 255));  // LED on
      pixels.show();
    }
    else if(messageTemp == "off"){
      Serial.println("off");
      pixels.setPixelColor(0, pixels.Color(0, 0, 0));  // LED off
      pixels.show();
    }
  }
}
void setup_wifi(){
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
}
void reconnect() {
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        if (client.connect("YoloUnoClient")) {
            Serial.println("connected");
            client.subscribe("esp32/output");
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}
void mqttTask(void *pvParameters) {
  setup_wifi();
  while (1) {
    if (!client.connected()) {
      reconnect();
    }
    client.loop();
  }
}

void serialInputTask(void *pvParameters) {
  while (1) {
    if (Serial.available() > 0) {
      String input = Serial.readStringUntil('\n');
      input.trim();
      if (input == "on" || input == "off") {
        client.publish("esp32/output", input.c_str());
      } else {
        Serial.println("Invalid input. Please enter 'on' or 'off'.");
      }
    }
    vTaskDelay(100 / portTICK_PERIOD_MS);
  }
}

// Create MQTT task
void createMqttTask() {
  xTaskCreate(mqttTask, "MqttTask", 8192, NULL, 2, NULL);
  xTaskCreate(serialInputTask, "SerialInputTask", 4096, NULL, 1, NULL);
}
