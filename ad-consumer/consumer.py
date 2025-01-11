# consumer.py
import os
import json
import logging
import sys

# workaround for the kafka module due to compatibility in newer python versions
import six
if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaConsumer
import pymongo

logging.basicConfig(level=logging.INFO)

# Read env
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_DB   = os.getenv("MONGO_DB")

mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    # Build default replicaset URI if none provided
    hosts = (
      "<YOUR_MONGODB_FQDN_1>:27017,"
      "<YOUR_MONGODB_FQDN_2>:27017,"
      "<YOUR_MONGODB_FQDN_3>:27017"
    )
    mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{hosts}/{MONGO_DB}?replicaSet=<YOUR_MONGODB_REPLICA_SET>"

logging.info(f"[ad-consumer] Connecting to Mongo at: {mongo_uri}")
client = pymongo.MongoClient(mongo_uri)
db = client[MONGO_DB]
last_events = db["last_events"]

try:
    client.admin.command("ping")
    logging.info("[ad-consumer] Pinged MongoDB successfully!")
except Exception:
    logging.exception("[ad-consumer] Could not ping MongoDB!")

bootstrap = os.getenv("KAFKA_BOOTSTRAP", "<YOUR_KAFKA_SERVICE>:9092")
topic     = os.getenv("KAFKA_TOPIC",     "<YOUR_KAFKA_TOPIC>")
group_id  = os.getenv("KAFKA_GROUP_ID",  "<YOUR_KAFKA_CONSUMER_GROUP>")

logging.info(f"[ad-consumer] Bootstrapping from: {bootstrap}, topic={topic}, group={group_id}")

def main():
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[bootstrap],
        group_id=group_id,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    logging.info("[ad-consumer] Starting consumer loop...")

    for msg in consumer:
        val = msg.value
        user_id = val.get("user_id", "").strip()
        event   = val.get("event",    "page_view").strip()

        if not user_id:
            logging.warning(f"[ad-consumer] Missing user_id in message!? {val}")
            continue

        logging.info(f"[ad-consumer] Upserting (updating or inserting) user={user_id}, event={event}")
        # Upsert into DB
        last_events.update_one(
            {"_id": user_id},
            {"$set": {"event": event}},
            upsert=True
        )

if __name__ == "__main__":
    main()
