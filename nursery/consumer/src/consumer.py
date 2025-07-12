# consumer/src/consumer.py

from kafka import KafkaConsumer
import json
import logging
import signal
import sys

logging.basicConfig(level=logging.INFO)

TOPIC = "mits.public.events"
BROKER = "kafka:9092"

def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[BROKER],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='event_logger',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    )

    logging.info(f"Listening for messages on topic '{TOPIC}'...")

    def shutdown_handler(sig, frame):
        logging.info("Shutdown signal received. Closing consumer...")
        consumer.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    for message in consumer:
        logging.info(f"Event received: {json.dumps(message.value, indent=2)}")

if __name__ == "__main__":
    main()
