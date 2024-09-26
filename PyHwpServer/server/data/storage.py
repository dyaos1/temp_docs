from typing import Any
from threading import Thread
import json
from kafka import KafkaConsumer
from util.small_utils import none_check
from config import load_config, ConfigPydanticModel


CONFIG: ConfigPydanticModel = load_config()

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args: Any, **kwargs: Any) :
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    

class Storage(metaclass=SingletonMeta):
    def __init__(self):
        
        host = none_check(CONFIG.server.kafka.host, 'localhost')
        port = none_check(CONFIG.server.kafka.port, 9092)
        str_type = none_check(CONFIG.server.kafka.str_type, 'utf-8')
        topic = none_check(CONFIG.server.kafka.topic, 'topic')
        self.occupation = False
        self.threads: list[Thread] = []
        self.consumer = KafkaConsumer(topic,
                            group_id='group',
                            bootstrap_servers=[f'{host}:{port}'],
                            auto_offset_reset='earliest', 
                            enable_auto_commit=False,
                            value_deserializer=lambda m: json.loads(m.decode(str_type)),
                        )
        self.stop_command = False

    def set_occupied(self):
        self.occupation = True

    def set_unoccupied(self):
        self.occupation = False

    def is_occupied(self):
        return self.occupation
    
    def append_thread(self, thread: Thread):
        self.threads.append(thread)

    def refresh_thread(self):
        self.threads = [t for t in self.threads if t.is_alive()]
    
    def is_thread_working(self):
        self.refresh_thread()
        return True if len(self.threads) > 0 else False
    
    