# python 3.6

import random
import time
import json

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "ustoilet_isdworks!"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(5)
        json_msg = [
            {"toilet_id": 3, "avail_num": 3, "people_num": 5,
                "cub_status": [[3, True], [0, False], [1, True]]},
            {"toilet_id": 4, "avail_num": 3, "people_num": 5,
                "cub_status": [[3, True], [0, False], [1, True]]},
            {"toilet_id": 5, "avail_num": 3, "people_num": 5,
                "cub_status": [[3, True], [0, False], [1, True]]}
        ]
        for package in json_msg:
            result = client.publish(topic, json.dumps(package))
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{json_msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
