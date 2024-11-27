#ifndef MQTT_TX_TASK_H
#define MQTT_TX_TASK_H

#include <PubSubClient.h>

void createMQTT_TX();
void mqtt_txTask(void *pvParameters);

#endif // MQTT_TX_TASK_H