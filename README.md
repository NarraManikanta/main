# main
Stock data pipeline: A Flask-based web app uploads CSV files to Kafka for real-time processing, including data transformation and storage into an Oracle database.

Project Overview:

This project involves building a data pipeline for processing stock data. The pipeline consists of several components:

Flask Web Application (app.py):
Provides a web interface for users to upload CSV files containing stock data.
Upon receiving a CSV file, it reads the file into a DataFrame and sends each row of the DataFrame to a Kafka topic.
The web application is built using Flask, a Python web framework.

Kafka Producer:
Sends each row of the DataFrame to the Kafka topic.
Utilizes the KafkaProducer from the kafka library.

Kafka Consumer (consumer.py):
Listens to the Kafka topic for incoming messages.
Parses the JSON messages, performs data transformations (e.g., converting dates to datetime format, calculating average price), and inserts the transformed data into an Oracle database.
Utilizes the KafkaConsumer from the kafka library for consuming messages and cx_Oracle for interacting with the Oracle database.

Oracle Database:
Stores the transformed stock data.
Insertions into the database are handled by the Kafka Consumer.

Frontend Interface (index.html):
Provides a simple HTML form for users to upload CSV files.
