#include "mqtt_tx_Task.h"
#include "temp_Task.h"

// MQTT server details
const char* mqtt_txServer = "io.adafruit.com";
const int mqtt_txPort = 1883;
const char* mqtt_txUser = "duongwt16";
const char* mqtt_txKey = "aio_qjYd85z1Od2dcJ6cDOlJw12EJzOM";

// Feed names
const char* tx_feedNames[] = {
    "duongwt16/feeds/bedroom.mois",
    "duongwt16/feeds/bedroom.temp"
};

const unsigned long publishInterval = 10000; // 10 seconds
WiFiClient espClient;
Adafruit_MQTT_Client mqtt_txClient(&espClient, mqtt_txServer, mqtt_txPort, mqtt_txUser, mqtt_txKey);

Adafruit_MQTT_Publish moisFeed = Adafruit_MQTT_Publish(&mqtt_txClient, tx_feedNames[0]);
Adafruit_MQTT_Publish tempFeed = Adafruit_MQTT_Publish(&mqtt_txClient, tx_feedNames[1]);

void publishToFeed(Adafruit_MQTT_Publish &feed, const char* payload) {
    if (!feed.publish(payload)) {
        Serial.println("Failed to publish");
    }
}

void reconnect() {
    while (mqtt_txClient.connected() == 0) {
        // Serial.print("Attempting MQTT connection...");
        if (mqtt_txClient.connect()) {
            Serial.println("connected");
        } else {
            Serial.print("failed");
            Serial.print(mqtt_txClient.connectErrorString(mqtt_txClient.connect()));
            Serial.println(" try again in 5 seconds");
            vTaskDelay(5000/portTICK_PERIOD_MS); // Wait 5 seconds before retrying
        }
    }
}

void mqtt_txTask(void *pvParameters) {
    unsigned long lastPublishTime = 0;
    while (true) {
        if (mqtt_txClient.connected() == 0) {
            reconnect();
        }
        mqtt_txClient.processPackets(10000);
        mqtt_txClient.ping();

        float mois = getMois();
        float temp = getTemp();
        
        char moisStr[8];
        char tempStr[8];
        
        dtostrf(mois, 6, 2, moisStr);
        dtostrf(temp, 6, 2, tempStr);
        
        unsigned long currentTime = millis();
        
        if (currentTime - lastPublishTime >= publishInterval) {
            lastPublishTime = currentTime;
            publishToFeed(moisFeed, moisStr);
            publishToFeed(tempFeed, tempStr);
        }
        vTaskDelay(100 / portTICK_PERIOD_MS); // Delay to prevent task from hogging the CPU
    }
}

void createMQTT_TX() {
    xTaskCreate(mqtt_txTask, "MQTT_tx Task", 4096, NULL, 1, NULL);
}