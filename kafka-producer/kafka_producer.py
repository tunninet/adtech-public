import time
import json
import random
import logging

# workaround for the kafka module due to compatibility in newer python versions
import six
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

producer_id = 'adtech-producer'

producer = KafkaProducer(
    bootstrap_servers=['<YOUR_KAFKA_SERVICE>:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    client_id=producer_id
)

user_ids = [str(i) for i in range(1, 11)]
actions = ["page_view", "click", "purchase"]

logger.info(f"Starting Kafka producer (client_id={producer_id})")

while True:
    for user_id in user_ids:
        event = {"user_id": user_id, "event": random.choice(actions)}
        producer.send('<YOUR_KAFKA_TOPIC>', event)
        logger.info(f"Sent event: {event} as: {producer_id}")
        time.sleep(5)