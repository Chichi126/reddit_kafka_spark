import pandas
import pyspark
import praw
import requests
import json
import time
import kafka
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Retrieve variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
user_agent = os.getenv("USER_AGENT")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password,
)

producer = kafka.KafkaProducer(bootstrap_servers=["localhost:9092"], 
                               value_serializer=lambda v: json.dumps(v).encode("utf-8"))
topic = "redditstream"


def get_data():
    """
    This function streams comments from the dataengineering subreddit and sends them
    to the kafka topic "redditstream". The function will continue to run until it is
    manually stopped. The function will print each comment to the console and wait
    for 30 seconds before checking for the next comment.

    :return: None
    """
    try:

        subreddit = reddit.subreddit("dataengineering")
        for comment in subreddit.stream.comments():
            data = {
                "id": comment.id,
                "body": comment.body,
                "author": comment.author.name,
                "subreddit": comment.subreddit.display_name
            }
            producer.send(topic, data)
            producer.flush()
            print("**"*100)
            print(f" Comment: {data}") # Print the comment body (comment.body)
            time.sleep(30)  
    except Exception as e:
        print(f"An error occurred: {e}")

get_data()
    