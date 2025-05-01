from kafka import KafkaConsumer
import json
import threading

def handle_event(data):
    print("Received Kafka Event:", data)
    # handle logic (e.g., update user history)

def consume():
    consumer = KafkaConsumer(
        'reservation-topic',
        bootstrap_servers='kafka:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id='user-service-group',
        auto_offset_reset='earliest'
    )

    for msg in consumer:
        handle_event(msg.value)

# Start in a background thread
def start_consumer():
    thread = threading.Thread(target=consume)
    thread.daemon = True
    thread.start()
