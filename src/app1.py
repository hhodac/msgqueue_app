import os
import sys
import json
import time
import random
import argparse
from datetime import datetime

import paho.mqtt.client as mqtt

from utils import load_env_config, load_system_config


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, default="app1",
                        help='name of application')
    parser.add_argument('--env_cfg', type=str, default='.env',
                        help='path to environment configuration file')
    parser.add_argument('--sys_cfg', type=str, default='config.json',
                        help='path to system configuration file')
    opt = parser.parse_args()
    return opt


def main(opt):
    # Initialisation
    load_env_config(opt['env_cfg'])
    sys_cfg = load_system_config(opt['sys_cfg'])

    client_name = opt['name']
    username = os.environ['MQTT_USERNAME']
    password = os.environ['MQTT_PASSWORD']
    vhost = sys_cfg['vhost']
    host = sys_cfg['host']
    port = sys_cfg['port']

    topic_publish = "app1/randint"
    a, b = [1, 100]
    t1, t2 = [1, 30]

    # Client connect to broker
    client = mqtt.Client(client_name, True, protocol=mqtt.MQTTv311)
    client.username_pw_set(vhost + ":" + username, password)
    print(" [INFO] App name: %s" % client_name)
    print(" [INFO] Connected to %s:%d" % (sys_cfg['host'], sys_cfg['port']))
    client.connect(host=host, port=port, keepalive=60)

    # Publish to broker
    print(" [INFO] `%s` publishing to topic `%s`" % (client_name, topic_publish))
    while True:
        i = random.randint(a, b)
        t = datetime.now().strftime("%H:%M:%S")
        msg = {
            "time": t,
            "value": i,
        }
        client.publish(topic_publish, json.dumps(msg), qos=0)
        print(" [x] Sent %s to %s" % (msg, topic_publish))
        # sleep
        n = random.randint(t1, t2)
        time.sleep(n)


if __name__ == "__main__":
    opt = parse_opt()
    try:
        main(vars(opt))
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
