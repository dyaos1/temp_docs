from kafka import KafkaProducer
from kafka.errors import KafkaError
from util import none_check
import json
from config import load_config, ConfigPydanticModel

CONFIG: ConfigPydanticModel = load_config()

class Producer():
    def __init__(self):
        host = none_check(CONFIG.server.kafka.host, 'localhost')
        port = none_check(CONFIG.server.kafka.port, 9092)
        str_type = none_check(CONFIG.server.kafka.str_type, 'utf-8')
        self.topic = none_check(CONFIG.server.kafka.topic, 'topic')

        self.producer = KafkaProducer(
            bootstrap_servers=[f'{host}:{port}'], 
            value_serializer=lambda m: json.dumps(m).encode(f'{str_type}'))

    def send_message(self, message: dict[str, str]):
        self.producer.send(self.topic, message)
        self.producer.flush()
        self.producer.close()