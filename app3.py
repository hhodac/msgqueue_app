import os
import sys
import json
import argparse

from tabulate import tabulate
import pandas as pd
import paho.mqtt.client as mqtt

from utils import load_env_config, load_system_config


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, default="app3",
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
        print(" [x] From %s received %s" % (message.topic, msg))
        print("Average values per %s" % message.topic[10:])
        if message.topic == topic_subscribe1:
            table_stat1.append(msg)
            df = pd.DataFrame(table_stat1)
        if message.topic == topic_subscribe2:
            table_stat2.append(msg)
            df = pd.DataFrame(table_stat2)
        if message.topic == topic_subscribe3:
            table_stat3.append(msg)
            df = pd.DataFrame(table_stat3)
        print(tabulate(df, headers="keys", tablefmt='psql'), "\n")

    # Initialisation
    load_env_config(opt['env_cfg'])
    sys_cfg = load_system_config(opt['sys_cfg'])

    client_name = opt['name']
    username = os.environ['MQTT-USERNAME']
    password = os.environ['MQTT-PASSWORD']
    vhost = sys_cfg['vhost']
    host = sys_cfg['host']
    port = sys_cfg['port']

    topic_subscribe1 = "app2/stat_1m"
    topic_subscribe2 = "app2/stat_5m"
    topic_subscribe3 = "app2/stat_30m"

    # Client connect to broker
    client = mqtt.Client(client_name, True, protocol=mqtt.MQTTv311)
    client.username_pw_set(vhost + ":" + username, password)
    client.on_message = on_message
    print(" [INFO] App name: %s" % client_name)
    print(" [INFO] Connected to %s:%d" % (sys_cfg['host'], sys_cfg['port']))
    client.connect(host=host, port=port, keepalive=60)

    # Subscribe to topic
    table_stat1 = []
    table_stat2 = []
    table_stat3 = []
    for topic in [topic_subscribe1, topic_subscribe2, topic_subscribe3]:
        client.subscribe(topic)
        print(" [INFO] `%s` subscribing to topic `%s`" % (client_name, topic))

    client.loop_forever()


if __name__ == "__main__":
    opt = parse_opt()
    try:
        main(vars(opt))
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
