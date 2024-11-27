#include "temp_Task.h"
DHT20 dht20; // I2C address
float current_temp = 0.0;
float current_mois = 0.0;

void setup_dht() {
  Wire.begin(11,12);
  dht20.begin();
}

void tempTask(void *pvParameters) {
    setup_dht();
    while (1) {
        if (dht20.read() == 0) { // Check if reading is successful
            current_temp = dht20.getTemperature();
            current_mois = dht20.getHumidity();
            Serial.print("Temperature: ");
            Serial.println(current_temp);
            Serial.print("Humidity: ");
            Serial.println(current_mois);
        }
        vTaskDelay(10000 / portTICK_PERIOD_MS);
    }
}

float getTemp() {
    return current_temp;
}

float getMois() {
    return current_mois;
}

void createTempTask() {
  xTaskCreate(tempTask, "TempTask", 2048*3, NULL, 1, NULL);
}