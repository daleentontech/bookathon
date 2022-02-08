import pika

broker_url = 'amqps://rdkynmun:Hx6EA_eC60K0Z954hB4_cdKfluyfuL61@beaver.rmq.cloudamqp.com/rdkynmun'

parameters = pika.URLParameters(broker_url)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='books')


def callback(ch, method, properties, body):
    print("Received in admin")
    print(body)


channel.basic_consume(queue='books', on_message_callback=callback)

print("Started Consuming")

channel.start_consuming()
channel.close()