from kafka import KafkaConsumer
import json
import threading
import logging

# Set up logging for better debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_event(data):
    logger.info(f"Received Kafka Event: {data}")
    # Handle logic (e.g., update user history)

def consume():
    try:
        consumer = KafkaConsumer(
            'reservation-topic',
            bootstrap_servers='devops-project-kafka-1:9092',  # Correct Kafka container name
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='user-service-group',
            auto_offset_reset='earliest'
        )

        for msg in consumer:
            handle_event(msg.value)
    except Exception as e:
        logger.error(f"Error while consuming messages: {e}")

# Start in a background thread
def start_consumer():
    thread = threading.Thread(target=consume)
    thread.daemon = True
    thread.start()

# Call start_consumer to initialize the background thread
if __name__ == '__main__':
    start_consumer()
