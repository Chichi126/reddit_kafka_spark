# reddit_kafka_spark

![](https://github.com/Chichi126/reddit_kafka_spark/blob/715b029dac1eba80683ff188a70f4d668800966c/Screenshot%202024-12-16%20at%209.59.01%20AM.png)



## Project Overview

This project uses Apache Spark to stream data from a Kafka topic to a MongoDB database. The streaming data is ingested, processed, and stored in MongoDB, verified and 
accessed for analytics or downstream applications. 

Docker Compose is used to manage and deploy all the required services in a streamlined manner

## Step 1: Prerequisites

Tools Required:

Docker and Docker Compose

Apache Kafka and Confluent components

Apache Spark

MongoDB Atlas or a local MongoDB instance

VSCode or a similar IDE for development and verification

## Configurations Needed:

MongoDB Atlas URI (or local MongoDB connection string)

Kafka topic name and bootstrap server

Spark dependencies for Kafka and MongoDB connectors

Python development environment with PySpark installed


## Step 2: Setting Up Docker Compose

Docker Compose was used to spin up Kafka, Spark, and MongoDB services. Here's an outline of the configuration:

##### Kafka Setup:

Zookeeper and Kafka brokers were defined in the docker-compose.yml file.

A Kafka topic was pre-configured using a Confluent control center or command-line tools.

##### MongoDB Setup:

MongoDB was set up in Docker with a mapped volume to persist data.

Authentication and networking settings were properly configured for external clients to access.

##### Spark Setup:

Spark master and worker nodes were defined with proper networking.

Spark image was pulled with the necessary connectors for Kafka and MongoDB pre-installed.

## Step 3: Writing the Streaming Application

The Python application reads data from Kafka, processes it using Spark, and writes it to MongoDB. 

#### Key components:

*Kafka Integration:*

Spark reads the data stream from Kafka using the Kafka-Spark connector.

The Kafka topic is subscribed to, and data is read in JSON format.

*Data Transformation:*

The data stream is processed using PySpark DataFrame APIs.

Schema definitions ensure proper parsing of JSON data.

*Writing to MongoDB:*

Data is written to MongoDB using the MongoDB-Spark connector.

Each micro-batch is appended to a specified database and collection.

#### Step 4: Verifying MongoDB Data

*Accessing MongoDB Locally:*

MongoDB was accessed locally through the Docker container for verification.

The mongo CLI or Compass UI was used to inspect the created database and collection.

Mongo CLI bash 

  * mongo "< your URI >" (to connect to the cluster)
    
  * show dbs (to display the databases present in the cluster)
    
  * use dbs  (TO enter into that particular database)
    
  * show collections (to display all the collections <tables> inside the database)
    
  * db.dataengineering.find().pretty()


Data replication can also be confirmed using MongoDB Atlas.

By using Compass connected to the Atlas cluster using the URI provided in the application configuration.


Verification in VSCode using the MongoDB Extension:

The MongoDB VSCode extension can connect to both local and cloud MongoDB instances.

Install the Vscode extension then click on connect

click on the view enter your uri including your password and username and enter

*Queries were executed to verify the inserted data.*

Basic queries were run using the MongoDB shell or VSCode extension to ensure data integrity.

Query Example:

* db.dataengineering.find().limit(5);*

