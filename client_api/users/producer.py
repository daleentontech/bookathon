import pika

broker_url = 'amqps://rdkynmun:Hx6EA_eC60K0Z954hB4_cdKfluyfuL61@beaver.rmq.cloudamqp.com/rdkynmun'

parameters = pika.URLParameters(broker_url)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()


def publish():
    channel.basic_publish(
        exchange='',
        routing_key='admin',
        body=b'Hello from client'
    )