import requests
import json
import time
import logging
from kafka import KafkaProducer
from random import randint, uniform
import config
import sys
from datetime import datetime

# logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('kafka-producer')

# Generate data
def generate_data(type, city=None):
    if type == 'random':
        return {
            'city': city,
            'temperature': round(uniform(20, 30), 2),  # Random temperature between 20 and 30 degrees Celsius
            'humidity': randint(30, 70),  # Random humidity percentage between 30 and 70
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }

    else:
        r = requests.post(url=config.api_url, headers=config.header, data=config.data)

        if r.ok:
            data = r.json()
            return data
        else:
            return None


# Callback successful
def on_send_success(record_metadata):
    log.info(f"Message sent to {record_metadata.topic} on partition {record_metadata.partition} with offset {record_metadata.offset}")

# Callback failure
def on_send_error(excp):
    log.error('Error sending message', exc_info=excp)

# Serializer
def json_serializer(data):
    return json.dumps(data).encode('utf-8')

# Connect to the Kafka
producer = KafkaProducer(bootstrap_servers=[config.kafka_broker], value_serializer=json_serializer)


if __name__ == "__main__":
    cities = ["Tehran"]

    type  = sys.argv[1]

    if type == 'random':
        while True:
            for city in cities:
                weather_data = generate_data(type, city)
                # Asynchronously send the data and add callbacks
                future = producer.send(config.kafka_topic, weather_data)
                future.add_callback(on_send_success).add_errback(on_send_error)

            time.sleep(1)
    
    if type == 'exchanges':
        while True:
            data = generate_data(type)
            for exchange in data:
                exchange['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                future = producer.send(config.kafka_topic, exchange)
                future.add_callback(on_send_success).add_errback(on_send_error)    

            time.sleep(10)    
