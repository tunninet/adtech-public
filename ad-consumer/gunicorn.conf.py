import threading  # Used for creating and managing threads
import logging  # Provides logging capabilities
from consumer import start_kafka_consumer  # Imports the function to start the Kafka consumer

# Function that runs after a Gunicorn worker is initialized
def post_worker_init(worker):
    # Log the initialization of the Kafka consumer thread
    logging.info("[gunicorn.conf] post_worker_init: starting Kafka consumer thread...")
    
    # Create a new thread to run the Kafka consumer
    # Setting daemon=True ensures the thread will not block program exit
    t = threading.Thread(target=start_kafka_consumer, daemon=True)
    
    # Start the Kafka consumer thread
    t.start()