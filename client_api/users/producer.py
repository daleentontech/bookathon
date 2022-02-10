import pika, json

broker_url = 'amqps://rdkynmun:Hx6EA_eC60K0Z954hB4_cdKfluyfuL61@beaver.rmq.cloudamqp.com/rdkynmun'

parameters = pika.URLParameters(broker_url)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()


def publish(method_frame, body):
    properties = pika.BasicProperties(method_frame)
    channel.basic_publish(
        exchange='',
        routing_key='admin',
        body=json.dumps(body).encode('utf-8'),
        properties=properties
    )