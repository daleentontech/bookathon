import os, pika, json
from dateutil.parser import parse as date_parse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin_api.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from books.models import Book, BookUser, User

broker_url = 'amqps://rdkynmun:Hx6EA_eC60K0Z954hB4_cdKfluyfuL61@beaver.rmq.cloudamqp.com/rdkynmun'

parameters = pika.URLParameters(broker_url)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print("Received in admin")
    data = json.loads(body)
    print(data)

    if properties.content_type == 'book_borrowed':
        book_id = data.get('pk')
        user_id = data.get('borrower')
        is_borrowed = data.get('is_borrowed')
        borrowed_on = data.get('borrowed_on')
        borrowed_on = date_parse(borrowed_on)
        default = {
            "id": book_id,
            "is_borrowed": is_borrowed,
            "borrowed_on": borrowed_on,
        }
        book = Book.objects.get(id=book_id)
        book.is_borrowed = is_borrowed
        book.borrowed_on = borrowed_on
        book.save()

        # Create BookUser to store the borrower and book borrowed
        book_user_data = {
            "user_id": user_id,
            "book_id": book_id,
        }
        book_user = BookUser.objects.create(**book_user_data)
        print(book_user)
    elif properties.content_type == 'user_created':
        data = {
            'id': data.get("id"),
            'email': data.get("email"),
            'first_name': data.get("first_name"),
            'last_name': data.get("last_name")
        }
        user = User.objects.create(**data)
        print(user.email)


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print("Started Consuming")

channel.start_consuming()
channel.close()