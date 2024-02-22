from kafka import KafkaConsumer, TopicPartition
import cx_Oracle
import json
from dateutil import parser


def convert_date(date_value):
    try:
        #convertung the date string to datatime value
        date_datetime = parser.parse(date_value)
    except Exception as e:
        print('Invalid DaateFormat filling with default date printing default date 1/1/1900')
        date_datetime = parser.parse('01/01/1900')
        
    return date_datetime


def avg_price(open,high,low,close):
    try:
        #finding the average price of the stock
        average_price = float((open+high+low+close)/4)
    except Exception as e:
        print('error occured while calculating the average price assigining 0')
        average_price = 0
    return average_price



def consume():
    # Kafka Consumer details
    bootstrap_servers = '<your_bootstap_server>'
    topic = '<your_topic_name>'
    group_id = 'stock_data_consumer_group' 

    # Oracle Database settings
    oracle_connection_string = '<username>/<password>@localhost:<port>/<SID>'

    # Create a Kafka consumer
    consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers, group_id=group_id,
                            auto_offset_reset='earliest', enable_auto_commit=False)

    # Connect to Oracle Database
    connection = cx_Oracle.connect(oracle_connection_string)
    cursor = connection.cursor()

    # Main loop to consume messages from Kafka
    try:
        for message in consumer:
            try:
                data = json.loads(message.value.decode('utf-8'))

                # Extracting relevant data fields
                temp_date = data.get('date')
                date = convert_date(temp_date)
                open_price = data.get('open')
                high_price = data.get('high')
                low_price = data.get('low')
                close_price = data.get('close')
                volume = data.get('volume')
                name = data.get('Name')  
                average = avg_price(open_price,high_price,low_price,close_price)


                # Insert data into Oracle Database
                cursor.execute("INSERT INTO STOCKMARKET_DATA (\"Date\", \"Open\", \"High\", \"Low\", \"Close\", \"Volume\", \"Name\", \"AVERAGE_STOCK_PRICE\") VALUES (:1, :2, :3, :4, :5, :6, :7, :8)",
                            (date, open_price, high_price, low_price, close_price, volume, name, average))
                connection.commit()

                print("Data inserted into Oracle DB:", data)

                # Commit the offset to mark the message as consumed
                consumer.commit()
                
                #breaking the loop after storing a row in database
                break

            except json.decoder.JSONDecodeError:
                print('Error: Invalid JSON data')
            except Exception as e:
                print('Error:', e)

    finally:
        consumer.close()
        cursor.close()
        connection.close()


