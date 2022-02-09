import pika, json, os, time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin_api.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

broker_url = 'amqps://rdkynmun:Hx6EA_eC60K0Z954hB4_cdKfluyfuL61@beaver.rmq.cloudamqp.com/rdkynmun'

parameters = pika.URLParameters(broker_url)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print("Received in admin")
    print(body)


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print("Started Consuming")

channel.start_consuming()
channel.close()