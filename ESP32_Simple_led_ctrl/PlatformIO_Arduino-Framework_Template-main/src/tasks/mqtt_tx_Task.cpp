#include "mqtt_tx_Task.h"
#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

// MQTT server details
const char* mqtt_txServer = "io.adafruit.com";
const int mqtt_txPort = 1883;
const char* mqtt_txUser = "duongwt16";
const char* mqtt_txKey = "aio_mJMS46fQhBxlvwgBfbgKyTfcy8cT";

// Feed names
const char* tx_feedNames[] = {
    "duongwt16/feeds/bedroom.mois",
    "duongwt16/feeds/bedroom.temp",
    "duongwt16/feeds/living-room.mois",
    "duongwt16/feeds/living-room.temp"
};

const unsigned long publishInterval = 10000; // 5 seconds
WiFiClient espClient;
PubSubClient mqtt_txClient(espClient);

void publishToFeed(const char* topic, const char* payload) {
    if (mqtt_txClient.connected()) {
        mqtt_txClient.publish(topic, payload);
    } else {
        Serial.println("MQTT client not connected");
    }
}

void reconnect() {
    while (!mqtt_txClient.connected()) {
        // Serial.print("Attempting MQTT connection...");
        if (mqtt_txClient.connect("ESP32Client", mqtt_txUser, mqtt_txKey)) {
            //Serial.println("connected");
        } else {
            // Serial.print("failed, rc=");
            // Serial.print(mqtt_txClient.state());
            //Serial.println(" try again in 5 seconds");
            delay(1000);
        }
    }
}

void mqtt_txTask(void *pvParameters) {
    unsigned long lastPublishTime = 0;
    while (true) {
        if (!mqtt_txClient.connected()) {
            reconnect();
        }
        mqtt_txClient.loop();

        float mois = 30 + static_cast<float>(rand()) / (static_cast<float>(RAND_MAX / (80 - 30)));
        float temp = 20 + static_cast<float>(rand()) / (static_cast<float>(RAND_MAX / (37 - 20)));
        
        char moisStr[8];
        char tempStr[8];
        
        dtostrf(mois, 6, 2, moisStr);
        dtostrf(temp, 6, 2, tempStr);
        
        unsigned long currentTime = millis();
        
        if (currentTime - lastPublishTime >= publishInterval) {
            lastPublishTime = currentTime;
            for (int i = 0; i < sizeof(tx_feedNames) / sizeof(tx_feedNames[0]); i++) {
                if (strstr(tx_feedNames[i], "mois") != NULL) {
                    publishToFeed(tx_feedNames[i], moisStr);
                } else if (strstr(tx_feedNames[i], "temp") != NULL) {
                    publishToFeed(tx_feedNames[i], tempStr);
                }
            }
        }
        vTaskDelay(100 / portTICK_PERIOD_MS); // Delay to prevent task from hogging the CPU
    }
}

void setup_mqtt_tx() {
    mqtt_txClient.setServer(mqtt_txServer, mqtt_txPort);
    xTaskCreate(mqtt_txTask, "MQTT_tx Task", 4096, NULL, 1, NULL);
}