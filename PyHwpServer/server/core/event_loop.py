import threading, time
from server.data import Storage
from .coinitializer import CoInitializer
import time
from config import load_config

TIME = load_config().server.interval.loop

def run_task_consumer():
    data_store = Storage()
    data_store.set_occupied()

    message_pack = data_store.consumer.poll(timeout_ms=3000)

    if not message_pack:
        print(f"No payload, timed out after {TIME} seconds.")
        time.sleep(TIME)

    else:
        for tp, messages in message_pack.items():
            for message in messages:

                sub_thread = CoInitializer(message.value["payload"])
                sub_thread.start()
                sub_thread.join()

                # 메시지를 수동 커밋
                data_store.consumer.commit()
                print("Message processed and committed")

    data_store.set_unoccupied()


def run_event_loop():
    data_store = Storage()

    while not data_store.stop_command:
        print(f"Thread is Working: {data_store.is_occupied()}")
        if data_store.is_occupied() == False:
            thread = threading.Thread(target=run_task_consumer)
            thread.start()
            
        else:
            pass
        
        time.sleep(TIME)