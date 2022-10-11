from pika.exchange_type import ExchangeType
from pika.channel import Channel
from celery import Celery
import pika
import os
import json


URL = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672')
PARAMS = pika.URLParameters(URL)
PARAMS.socket_timeout = 5
EXCHANGE = ExchangeType.direct
EXCHANGE_NAME = 'openuser'
DEFAULT_QUEUE_NAME = 'open_user_creator'
NEW_CREATOR_KEY = 'new_creator'
DEL_CREATOR_KEY = 'delete_creator'
NEW_OPENUSERAPP_KEY = 'new_openuserapp'
UPDATE_OPENUSERAPP_KEY = 'update_openuserapp'
DEL_OPENUSERAPP_KEY = 'delete_openuserapp'

# Connect to main Celery instance
celery_app = Celery('src', broker=os.environ.get('CELERY_BROKER_REDIS', 'redis://redis:6379/0'))


def main():
    connection = pika.BlockingConnection(parameters=PARAMS)
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type=EXCHANGE, durable=True)

    def callback(ch: Channel, mth, props, body):
        if mth.routing_key == NEW_CREATOR_KEY:
            print(F"Recieved ({mth.routing_key}) message: {json.loads(body)}")
            celery_app.send_task(name='openuser.tasks.new_openusercreator', kwargs={'data': json.loads(body)})

        if mth.routing_key == DEL_CREATOR_KEY:
            print(F"Recieved ({mth.routing_key}) message: {json.loads(body)}")
            celery_app.send_task(name='openuser.tasks.delete_openusercreator', kwargs={'data': json.loads(body)})

        if mth.routing_key == NEW_OPENUSERAPP_KEY:
            print(F"Recieved ({mth.routing_key}) message: {json.loads(body)}")
            celery_app.send_task('openuser.tasks.new_openuserapp', kwargs={'data': json.loads(body)})

        if mth.routing_key == UPDATE_OPENUSERAPP_KEY:
            print(F"Recieved ({mth.routing_key}) message: {json.loads(body)}")
            celery_app.send_task('openuser.tasks.update_openuserapp', kwargs={'data': json.loads(body)})

        if mth.routing_key == DEL_OPENUSERAPP_KEY:
            print(F"Recieved ({mth.routing_key}) message: {json.loads(body)}")
            celery_app.send_task('openuser.tasks.delete_openuserapp', kwargs={'data': json.loads(body)})

        # Always acknowledge message delivery/processed
        ch.basic_ack(delivery_tag=mth.delivery_tag)

    # declare queue
    openusercreator_queue = channel.queue_declare(queue=DEFAULT_QUEUE_NAME, durable=True)

    # bind queue to exchange and consume messages with the provided routing_keys
    channel.queue_bind(
        queue=openusercreator_queue.method.queue,
        exchange=EXCHANGE_NAME,
        routing_key=NEW_CREATOR_KEY
    )
    channel.queue_bind(
        queue=openusercreator_queue.method.queue,
        exchange=EXCHANGE_NAME,
        routing_key=DEL_CREATOR_KEY
    )
    channel.queue_bind(
        queue=openusercreator_queue.method.queue,
        exchange=EXCHANGE_NAME,
        routing_key=NEW_OPENUSERAPP_KEY
    )
    channel.queue_bind(
        queue=openusercreator_queue.method.queue,
        exchange=EXCHANGE_NAME,
        routing_key=UPDATE_OPENUSERAPP_KEY
    )
    channel.queue_bind(
        queue=openusercreator_queue.method.queue,
        exchange=EXCHANGE_NAME,
        routing_key=DEL_OPENUSERAPP_KEY
    )

    channel.basic_consume(queue=openusercreator_queue.method.queue, on_message_callback=callback)

    print(F"Waiting for ({NEW_CREATOR_KEY} | {DEL_CREATOR_KEY} | {NEW_OPENUSERAPP_KEY} | {UPDATE_OPENUSERAPP_KEY}\
| {DEL_OPENUSERAPP_KEY}) messages in ({openusercreator_queue.method.queue}) queue")

    channel.start_consuming()
    connection.close()


if __name__ == '__main__':
    main()
