from confluent_kafka import Consumer, KafkaError
from queue import Queue
import threading
from stripe_integration import process_message


kafka_conf = {'bootstrap.servers': 'localhost:9092', 'group.id': 'my_group', 'auto.offset.reset': 'earliest'}
consumer = Consumer(kafka_conf)
consumer.subscribe(['customer_changes'])

message_queue = Queue()

print("Consumer started")

def process_messages():
    while True:
        if not message_queue.empty():
            msg = message_queue.get()
            process_message(msg)
            message_queue.task_done()


def receive_messages():
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break
            message_queue.put(msg)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

receive_thread = threading.Thread(target=receive_messages)
process_thread = threading.Thread(target=process_messages)

receive_thread.start()
process_thread.start()

receive_thread.join()
process_thread.join()
