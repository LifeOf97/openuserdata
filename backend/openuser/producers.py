from pika.exchange_type import ExchangeType
import pika
import json
import os


class RabbitMQProducer:

    URL = os.environ.get('RABBITMQ_URL')
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

    def publish_update_openuserapp(self, data, routing_key='update_openuserapp'):
        self._channel.basic_publish(
            exchange=self.EXCHANGE_NAME,
            routing_key=str(routing_key),
            body=json.dumps(data),
            properties=pika.BasicProperties(
                content_type='application/json'
            )
        )
