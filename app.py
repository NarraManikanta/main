from flask import Flask, render_template, request, redirect, url_for
from kafka import KafkaProducer
import json
from consumer import *
import pandas as pd

app = Flask(__name__)

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers='<your_bootstap_server>')

def send_dataframe_to_kafka(df, topic):
    print(df.shape)
    for index, row in df.iterrows():
        json_data = row.to_json()
        print('json_data',json_data)
        producer.send(topic, value=json_data.encode('utf-8'))
        consume()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Read CSV file into DataFrame
            df = pd.read_csv(file)
            # Send DataFrame rows to Kafka topic
            send_dataframe_to_kafka(df, '<your_topic_name>')
            return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
