
import requests
import json
import pandas as pd
import kafka
import time

# Initialize Kafka producer and topic
producer = kafka.KafkaProducer(bootstrap_servers=["localhost:9092"])
topic = "mystream"

# Function to fetch data
def get_data():
    """Fetch weather data from the API."""
    response = requests.get("https://api.open-meteo.com/v1/forecast", params={
        "latitude": 52.52,
        "longitude": 13.41,
        "hourly": "temperature_2m",
        "timezone": "Europe/Berlin",
    })
    return response.json()

# Main execution block
while True:
    try:
        data = get_data()
        # Send data to Kafka
        producer.send(topic, json.dumps(data).encode("utf-8"))
        producer.flush()  # Ensure the message is sent immediately
        print("Data sent to Kafka topic:", topic)
    except Exception as e:
        print(f"An error occurred: {e}")
    time.sleep(60)  # Wait for 60 seconds before the next API call


# weather = get_data()
# print(weather)


# if __name__ == "__main__":
#     data = get_data()
#     df = pd.DataFrame(data["hourly"]["temperature_2m"])
#     print(df)

