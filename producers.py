import praw
import json
import time
from confluent_kafka import Producer
from dotenv import load_dotenv
import os

load_dotenv()

# Reddit credentials
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT"),
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
)

# Kafka configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'reddit_producer'
}

producer = Producer(conf)
topic = "redditstream"

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def get_data():
    try:
        subreddit = reddit.subreddit("politics")
        for comment in subreddit.stream.comments():
            data = {
                "id": comment.id,
                "body": comment.body,
                "author": comment.author.name,
                "subreddit": comment.subreddit.display_name
            }
            
            producer.produce(
                topic,
                value=json.dumps(data).encode('utf-8'),
                callback=delivery_report
            )
            producer.poll(0)  # Trigger delivery reports
            
            print("**"*100)
            print(f" Comment: {data}")
            time.sleep(3)
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        producer.flush()

if __name__ == "__main__":
    get_data()