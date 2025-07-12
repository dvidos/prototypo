# consumer/Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY src/ ./src/

WORKDIR /app/src

RUN pip install kafka-python

CMD ["python", "consumer.py"]
