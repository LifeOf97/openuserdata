# This rabbitmq producer is currently not in use
from pika.exchange_type import ExchangeType
import pika
import json
import os


class RabbitMQProducer:

    URL = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672')
    PARAMS = pika.URLParameters(URL)
    PARAMS.socket_timeout = 5
    EXCHANGE = ExchangeType.direct
    EXCHANGE_NAME = 'openuser'

    def __init__(self):
        self._connection = pika.BlockingConnection(parameters=self.PARAMS)
        self._channel = self._connection.channel()
        self._channel.exchange_declare(
            exchange=self.EXCHANGE_NAME,
            exchange_type=self.EXCHANGE,
            durable=True
        )

    def publish_message(self, data: dict, routing_key: str):
        """
        Method to publish messages to rabbitmq message broker exchange for consumers
        listening for messages with the specified routing_key.

        data: dict = the message to send
        routing_key: str = the routing key to send this message with
        """
        self._channel.basic_publish(
            exchange=self.EXCHANGE_NAME,
            routing_key=str(routing_key),
            body=json.dumps(data),
            properties=pika.BasicProperties(content_type='application/json')
        )
        self._connection.close()
