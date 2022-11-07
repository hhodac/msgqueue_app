# Switchdin Challenge

Topic: Python Software Engineer (Embedded, Data Science)

# Application Description

Environment setup:
* MQTT message broker: RabbitMQ
* Publish/Subscribe library: paho-mqtt

System overview:
![System overview](figures/system_overview.png)

## Local setup
Initialise RabbitMQ server:
```
# Starting server
rabbitmq-server

# Enabling plugin
rabbitmq-plugins enable rabbitmq_mqtt

# Setup users and authentication
rabbitmqctl add_user mqtt-test mqtt-test
rabbitmqctl set_permissions -p / mqtt-test ".*" ".*" ".*"
rabbitmqctl set_user_tags mqtt-test management
```

Generate hidden environment file *(secret keys)*
* File name: `.env`
* File content:
```
MQTT-USERNAME = "mqtt-test"
MQTT-PASSWORD = "mqtt-test"
```

## Docker setup
```
docker pull rabbitmq
```

## App1
Generates a random number between [1 and 100] every [1 to 30] seconds and publishes to broker with topic named `app1/randint`.

Run app:
```
python src/app1.py
```
## App2
Subscribes to topic `app1/randint` and compute average every [1, 5, 30] minutes,
and publishes accordingly to broker with topics named `app2/stat_1m`, `app2/stat_5m`, `app2/stat_30m`.

Run app:
```
python src/app2.py
```

## App3
Subscribes to topics `app2/stat_1m`, `app2/stat_5m`, `app2/stat_30m`, and prints out tabular view in console accordingly.

Run app:
```
python src/app3.py
```

# Demo
![demo](figures/demo.gif)

# Project timeline records
* Self-study & research: 1 day
* Implementation: 1 day
    * [x] Design: 30 minutes
    * [x] Coding: 2 hours
    * [x] Testing (local): 1 hour
    * [ ] Deployment: 2 hour
    * [ ] Testing (deploy): 1 hour
    * [x] Documentation: 1 hour

# References
1. RabbitMQ:
    * [cli guide](https://www.rabbitmq.com/cli.html)
    * [MQTT Plugin](https://www.rabbitmq.com/mqtt.html)
    * [Tutorials](https://www.rabbitmq.com/getstarted.html)
2. Paho MQTT:
    * [Installation and usage](https://pypi.org/project/paho-mqtt/)
    * [Documentations](https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php)
    * [Tutorials](http://www.steves-internet-guide.com/into-mqtt-python-client/)
