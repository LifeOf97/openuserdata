from pika.exchange_type import ExchangeType
from pika.channel import Channel
import pika
import os
import json
from tasks import update_openusercreators


URL = os.environ.get('RABBITMQ_URL')
PARAMS = pika.URLParameters(URL)
PARAMS.socket_timeout = 5
EXCHANGE = ExchangeType.direct
EXCHANGE_NAME = 'openuser'
DEFAULT_QUEUE_NAME = 'open_user_creator'
NEW_CREATOR_KEY = 'new_creator'
CREATE_OPENUSERAPP_KEY = 'create_openuserapp'


connection = pika.BlockingConnection(parameters=PARAMS)
channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type=EXCHANGE, durable=True)


def callback(ch: Channel, mth, props, body):
    if mth.routing_key == NEW_CREATOR_KEY:
        print(F"Recieved ({mth.routing_key}) message: {json.loads(body)}")
        # execute a celery task
        update_openusercreators(data=body)
    elif mth.routing_key == CREATE_OPENUSERAPP_KEY:
        print(F"Recieved ({mth.routing_key}) message: {json.loads(body)}")
        # execute a celery task
        # create_openuserapp(data=body)

    # acknowledge message delivery
    ch.basic_ack(delivery_tag=mth.delivery_tag)


# declare queue
openusercreator_queue = channel.queue_declare(queue=DEFAULT_QUEUE_NAME, durable=True)

# bind queue to exchange and consume messages with NEW_CREATOR_KEY routing_key
channel.queue_bind(queue=openusercreator_queue.method.queue, exchange=EXCHANGE_NAME, routing_key=NEW_CREATOR_KEY)

# bind queue to exchange and consume messages with CREATE_OPENUSERAPP_KEY routing_key
channel.queue_bind(queue=openusercreator_queue.method.queue, exchange=EXCHANGE_NAME, routing_key=CREATE_OPENUSERAPP_KEY)

channel.basic_consume(queue=openusercreator_queue.method.queue, on_message_callback=callback)

print(F"Waiting for ({NEW_CREATOR_KEY}|{CREATE_OPENUSERAPP_KEY}) messages in ({openusercreator_queue.method.queue}) queue")

channel.start_consuming()
connection.close()
