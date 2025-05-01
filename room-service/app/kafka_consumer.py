from kafka import KafkaConsumer
import json
import threading
import time
from kafka.errors import NoBrokersAvailable

def handle_event(data):
    print("Received Kafka Event in Room Service:", data)
    # handle your business logic, e.g., update room availability

def consume():
    while True:
        try:
            consumer = KafkaConsumer(
                'reservation-topic',
                bootstrap_servers='kafka:9092',
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                group_id='room-service-group',
                auto_offset_reset='earliest'
            )
            break  # Connected successfully, exit the retry loop
        except NoBrokersAvailable:
            print("Kafka not available yet. Retrying in 5 seconds...")
            time.sleep(5)

    for msg in consumer:
        handle_event(msg.value)

# Start consumer in a background thread
def start_consumer():
    thread = threading.Thread(target=consume)
    thread.daemon = True
    thread.start()
