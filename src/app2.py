import os
import sys
import json
import time
import argparse
from cache import Cache

import paho.mqtt.client as mqtt

from utils import load_env_config, load_system_config, on_connect


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, default="app2",
                        help='name of application')
    parser.add_argument('--env_cfg', type=str, default='.env',
                        help='path to environment configuration file')
    parser.add_argument('--sys_cfg', type=str, default='config.json',
                        help='path to system configuration file')
    opt = parser.parse_args()
    return opt


def main(opt):
    def on_message(client, userdata, message):
        msg = json.loads(message.payload.decode('utf-8'))
        client_topic_1m.update(msg)
        client_topic_5m.update(msg)
        client_topic_30m.update(msg)
        print(" [x] Received %s from %s" % (msg, message.topic))

    # Initialisation
    load_env_config(opt['env_cfg'])
    sys_cfg = load_system_config(opt['sys_cfg'])

    client_name = opt['name']
    username = os.environ['MQTT_USERNAME']
    password = os.environ['MQTT_PASSWORD']
    vhost = sys_cfg['vhost']
    host = sys_cfg['host']
    port = sys_cfg['port']

    topic_subscribe = "app1/randint"
    topic_publish1 = "app2/stat_1m"
    topic_publish2 = "app2/stat_5m"
    topic_publish3 = "app2/stat_30m"

    # Client connect to broker
    client = mqtt.Client(client_name, True, protocol=mqtt.MQTTv311)
    client.username_pw_set(vhost + ":" + username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    print(" [INFO] App name: %s" % client_name)
    print(" [INFO] Connected to %s:%d" % (sys_cfg['host'], sys_cfg['port']))
    client.connect(host=host, port=port, keepalive=60)

    # Subscribe to topic
    client.subscribe(topic_subscribe)
    client.loop_start()
    print(" [INFO] Subscribed to topic %s" % topic_subscribe)

    # Map client to topic publish
    client_topic_1m = Cache(client, topic_publish1)
    client_topic_5m = Cache(client, topic_publish2)
    client_topic_30m = Cache(client, topic_publish3)

    cnt = 0
    while True:
        time.sleep(60)
        cnt += 1
        client_topic_1m.publish()
        if cnt % 5 == 0:
            client_topic_5m.publish()
        if cnt % 30 == 0:
            client_topic_30m.publish()


if __name__ == "__main__":
    opt = parse_opt()
    try:
        main(vars(opt))
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
