from pika.exchange_type import ExchangeType
from dotenv import load_dotenv
import pika
import os

# Load env fil
load_dotenv()


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

    def _publish_message(self, routing_key, body, **props):
        self._channel.basic_publish(
            exchange=self.EXCHANGE_NAME,
            routing_key=routing_key,
            body=body,
            properties=pika.BasicProperties(**props)
        )

    def publish_update_openuserapp(self, data, routing_key='update_openuserapp'):
        self._publish_message(
            routing_key=str(routing_key),
            body=data,
            props={'content_type': 'application/json'}
        )
