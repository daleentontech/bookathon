import pika, json
from decouple import config
broker_url = config("BROKER_URL")

parameters = pika.URLParameters(broker_url)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()


def publish(method_frame, body):
    properties = pika.BasicProperties(method_frame)
    channel.basic_publish(
        exchange='',
        routing_key='client',
        body=json.dumps(body).encode('utf-8'),
        properties=properties
    )