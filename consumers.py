from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
import json
import pyspark

# MongoDB Database and Collection
database = "reddit_db"
collection = "dataengineering"

# Load MongoDB credentials from config.json
with open("config.json") as f:
    config = json.load(f)

mongodb_username = config["mongodb_username"]
mongodb_password = config["mongodb_password"]

# MongoDB URI
uri = f"mongodb+srv://{mongodb_username}:{mongodb_password}@amdari-cluster.ynzr6.mongodb.net/"

# Kafka Configuration
broker = "localhost:9092"
topic = "mystream"

# Create Spark Session
spark = SparkSession.builder \
    .appName("Kafka-to-MongoDB-Streaming") \
    .config("spark.mongodb.write.connection.uri", uri) \
    .config("spark.mongodb.write.database", database) \
    .config("spark.mongodb.write.collection", collection) \
    .getOrCreate()

# Define Schema for Kafka messages
schema = StructType([
    StructField("id", StringType(), True),
    StructField("body", StringType(), True),
    StructField("subreddit", StringType(), True)
])

# Read Stream from Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", broker) \
    .option("startingOffsets", "earliest") \
    .option("subscribe", topic) \
    .load()

# Fixing schema extraction
parsed_df = kafka_df.selectExpr("CAST(value AS STRING)").select(
    "value"
).rdd.map(lambda x: json.loads(x["value"])).toDF(schema)

parsed_df.printSchema()

# Write Stream to MongoDB
query = parsed_df.writeStream \
    .outputMode("append") \
    .format("mongodb") \
    .option("checkpointLocation", "checkpoint") \
    .start()

# Wait for termination
query.awaitTermination()




