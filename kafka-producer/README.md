# AdTech Kafka Producer (Kubernetes)

This Python script simulates user events (e.g., page views, clicks, purchases) and streams them to a Kafka topic at regular intervals. It is typically deployed in Kubernetes using an upstream YAML file, rather than run locally.

## How It Works

1. **Random Event Data**  
   - The script generates a random user ID from a predefined list of IDs (1–10).
   - It then randomly picks an event type (`page_view`, `click`, or `purchase`).

2. **Kafka Producer**  
   - Leverages the `kafka-python` library to create a KafkaProducer instance.
   - By default, it uses the address `<YOUR_KAFKA_SERVICE>:9092`.
   - Serializes events to JSON and publishes them to the `<YOUR_KAFKA_TOPIC>` topic.

3. **Continuous Loop**  
   - The script runs indefinitely in a `while True` loop.
   - Every 5 seconds, it sends another event for each user ID.

## Deployment in Kubernetes

1. **Container Image**  
   - The script is packaged in a Docker container (e.g., built from a Dockerfile that installs Python dependencies like `kafka-python`).
   - The container is then stored in a registry accessible to your Kubernetes cluster.

2. **Upstream Deploy File**  
   - You should have a YAML file (e.g., `deploy-producer.yaml`) that defines a Deployment (or similar resource) for this producer.
   - This YAML specifies:
     - The container image to pull from your registry.
     - Environment variables or config maps if needed (e.g., bootstrap server URL).
     - The number of replicas (to scale event production).

3. **Apply the Deployment**  
   - Once you have the deployment file, apply it with:
     ```bash
     kubectl apply -f producer-deploy.yaml -n <your-namespace>
     ```
   - The script then runs as a Pod within Kubernetes, continuously sending events to Kafka.

4. **View Logs**  
   - Check logs to see the producer in action:
     ```bash
     kubectl logs -f deployment/producer-deployment -n <your-namespace>
     ```
   - Replace `producer-deployment` with the actual name from your YAML file if different.

5. **Scaling**  
   - Increase or decrease the number of replicas to manage how many events per second you produce. For example:
     ```bash
     kubectl scale deployment/producer-deployment --replicas=3 -n <your-namespace>
     ```

## Configuration

- **Kafka Address**: If your Kafka is reachable at a different domain or port, update the `bootstrap_servers` in the script or set an environment variable in the deployment YAML.
- **User IDs**: Change the `user_ids` list to match your application’s user base.
- **Event Types**: Add or remove items in the `actions` list to simulate different events.
- **Interval**: Adjust `time.sleep(5)` to control how frequently events are produced.

## Dependencies

- [Python 3.7+](https://www.python.org/downloads/)  
- [kafka-python](https://pypi.org/project/kafka-python/)  
- [six](https://pypi.org/project/six/) (for Python 3.12 compatibility)  

These should be installed in the container image. If you maintain a Dockerfile, ensure it runs:
```bash
pip install kafka-python six
```
(or uses a requirements file with those packages listed).

## Troubleshooting

- **Connection Issues**: Verify the producer can resolve `<YOUR_KAFKA_SERVICE>` and that the Kafka service is running on port 9092.  
- **Serialization Errors**: Check that the consumer is expecting JSON, or adjust the `value_serializer` and consumer accordingly.  
- **Logging**: Increase or decrease the logging level as needed in the `logging.basicConfig(level=logging.INFO)` line.

## License

This script is provided as-is for demonstration purposes. Adapt and extend as needed for your production environment.