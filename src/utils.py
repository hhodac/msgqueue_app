import json
import dotenv


# MQTT client callback functions
def on_publish(client, userdata, mid):
    """Callback when message is published"""
    print(" [INFO] Published to " + str(mid))


def on_connect(client, userdata, flags, rc):
    """Callback when client connect to broker"""
    if rc == 0:
        print(" [INFO] Connection successful")
    else:
        print(" [ERROR] Connection refused")


def on_subscribe(client, userdata, mid, granted_qos):
    """Callback when client subscribed to a topic"""
    print(" [INFO] Subscribed to " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, message):
    """Callback when client received message from a topic"""
    msg = json.loads(message.payload.decode('utf-8'))
    print(" [INFO] Received %s from topic %s" % (msg, message.topic))


# Configurations
def load_system_config(cfg_file):
    """Load system configuration file"""
    with open(cfg_file, 'r') as f:
        cfg = json.load(f)
    return cfg


def load_env_config(dotenv_file):
    """Load environment secret configuration file"""
    dotenv.load_dotenv(dotenv_file)
