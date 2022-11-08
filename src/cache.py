import json
from datetime import datetime
from statistics import mean


class Cache:
    def __init__(self, client, publish_topic):
        self.client = client
        self.publish_topic = publish_topic
        self.time_start = datetime.now().strftime("%H:%M:%S")
        self.records = []

    def update(self, t_value):
        """Update records array"""
        self.records.append(t_value)

    def get_mean(self):
        """Compute and round mean of records"""
        values = [r['value'] for r in self.records]
        return round(mean(values), 4)

    def clear(self):
        """Clear cache"""
        self.records = []

    def publish(self):
        """Publish message to topic"""
        if len(self.records) > 0:
            mean_value = self.get_mean()
            t0 = self.time_start
            t1 = datetime.now().strftime("%H:%M:%S")
            msg = {
                "time_from": t0,
                "time_to": t1,
                "value": mean_value,
            }
            self.client.publish(self.publish_topic, json.dumps(msg), qos=0)
            print(" [x] Sent %s to %s" % (msg, self.publish_topic))
            self.time_start = t1
        self.clear()
