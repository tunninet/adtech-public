# Ad-Consumer

A small Python service that listens to a Kafka topic (`<YOUR_KAFKA_TOPIC>`) and upserts each
user’s latest event into a MongoDB `last_events` collection.

## Overview

1. **Kafka Consumer**: Subscribes to the `<YOUR_KAFKA_TOPIC>` topic via the configured Kafka
   bootstrap server.
2. **MongoDB Upsert**: Whenever we receive `{"user_id": "...", "event": "..."}`, we
   update the `last_events` collection so that `_id == user_id`. This ensures we
   always have the latest event for each user.
3. **Configuration**: Environment variables define Mongo credentials, Kafka server
   details, and the topic name. (The first three variables—`MONGO_USER`, `MONGO_PASS`,
   `MONGO_DB`—are set upstream by the Ansible deploy file.)

---

## Environment Variables

| Variable         | Default                                        | Description                                |
|------------------|------------------------------------------------|--------------------------------------------|
| `MONGO_USER`     | *(set upstream)*                               | MongoDB username.                          |
| `MONGO_PASS`     | *(set upstream)*                               | MongoDB password.                          |
| `MONGO_DB`       | *(set upstream)*                               | MongoDB database name (e.g., `adtech`).    |
| `MONGO_URI`      | *(constructed if unset)*                       | Complete MongoDB connection URI.           |
| `KAFKA_BOOTSTRAP`| `<YOUR_KAFKA_SERVICE>:9092`  | Kafka bootstrap server(s).                 |
| `KAFKA_TOPIC`    | `<YOUR_KAFKA_TOPIC>`                                  | Topic name to consume from.                |
| `KAFKA_GROUP_ID` | `<YOUR_KAFKA_CONSUMER_GROUP>`                              | Consumer group ID.                         |

**Note**: If `MONGO_URI` is not provided, the script uses `MONGO_USER`, `MONGO_PASS`, and
`MONGO_DB` to build a default replicaset URI pointing to:

<YOUR_MONGODB_FQDN>:27017, <YOUR_MONGODB_FQDN_2>:27017, <YOUR_MONGODB_FQDN_3>:27017

and appends `?replicaSet=<YOUR_MONGODB_REPLICA_SET>`.
