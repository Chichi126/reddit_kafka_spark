import kafka
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "redditstream",
    auto_offset_reset='earliest',
    bootstrap_servers=["localhost:9092"],
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

for comment in consumer:
    print(comment.value)