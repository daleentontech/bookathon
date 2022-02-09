import pika, json, os, time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "client_api.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from books.models import Book

broker_url = 'amqps://rdkynmun:Hx6EA_eC60K0Z954hB4_cdKfluyfuL61@beaver.rmq.cloudamqp.com/rdkynmun'

parameters = pika.URLParameters(broker_url)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='client')


def callback(ch, method, properties, body):
    print("Received in client")
    data = json.loads(body)
    print(data)

    if properties.content_type == 'book_created':
        Book.objects.create(**data)
        print("Book created")
    elif properties.content_type == 'book_deleted':
        Book.objects.filter(id=data).first().delete()
        print("Book deleted")


channel.basic_consume(queue='client', on_message_callback=callback, auto_ack=True)

print("Started Consuming")

channel.start_consuming()
channel.close()
