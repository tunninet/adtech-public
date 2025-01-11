FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY kafka_producer.py kafka_producer.py

CMD ["python", "kafka_producer.py"]