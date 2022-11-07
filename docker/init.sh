#!/bin/sh

# rabbitmq-server -detached
rabbitmqctl wait --timeout 60 /var/lib/rabbitmq/mnesia/rabbitmq.pid
# rabbitmq-plugins enable rabbitmq_mqtt
rabbitmqctl add_user mqtt-test mqtt-test
rabbitmqctl set_permissions -p / mqtt-test '.*' '.*' '.*'
rabbitmqctl set_user_tags mqtt-test management
