import json, threading, typing
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from kafka import KafkaConsumer
from server.core import run_event_loop, Producer
from server.data import Storage

app = FastAPI()
consumer = KafkaConsumer('topic',
                            group_id='group',
                            bootstrap_servers=['localhost:9092'],
                            auto_offset_reset='earliest', 
                            enable_auto_commit=False,
                            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
                        )
def datastore():
    return Storage()


class Payload(BaseModel):
    payload: str


@app.post("/")
def post_payload(payload: Payload):
    producer = Producer()
    producer.send_message(payload.model_dump())
    return payload


@app.get("/run")
async def run_consuming(data_store: typing.Annotated[Storage, Depends(datastore)]):
    data_store.stop_command = False
    if not data_store.is_thread_working():
        thread = threading.Thread(target=run_event_loop)
        thread.start()
        data_store.append_thread(thread)
        return {"status": "consumer app started successfully!"}
    else:
        return {"status": f"oops! app is already running!: {len(data_store.threads)} threads running"}


@app.get("/stop")
async def stop_consuming(data_store: typing.Annotated[Storage, Depends(datastore)]):
    if data_store.is_thread_working():
        data_store.stop_command = True
        data_store.threads = []
        return {"status": f"app stopped"}
    else:
        return {"status": "app is not running now"}
