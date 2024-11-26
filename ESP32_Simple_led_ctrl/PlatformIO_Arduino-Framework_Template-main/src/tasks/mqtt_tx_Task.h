#ifndef MQTT_TX_TASK_H
#define MQTT_TX_TASK_H

#include <PubSubClient.h>

void setup_mqtt_tx();
void mqtt_txTask(void *pvParameters);

#endif // MQTT_TX_TASK_H