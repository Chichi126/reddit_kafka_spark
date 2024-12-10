# Use an official openjdk base image to ensure Java is available
FROM openjdk:8-jdk-alpine

# Install necessary dependencies like Spark and any other dependencies
RUN apk add --no-cache bash curl


# Set up Spark
ENV SPARK_VERSION 3.5.1
ENV HADOOP_VERSION 3.2

# Download and install Spark
RUN curl -sL "https://archive.apache.org/dist/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz" | tar xz -C /opt && \
ln -s /opt/spark-3.1.2-bin-hadoop3.2 /opt/spark

# Set environment variables
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Expose ports for Spark (default ports)
EXPOSE 7077 8080

# Start Spark master
CMD ["/opt/spark/bin/spark-class", "org.apache.spark.deploy.master.Master"]

