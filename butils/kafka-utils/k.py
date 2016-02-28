import threading, logging, time, collections

from kafka.client import KafkaClient
from kafka.consumer.simple import SimpleConsumer
from kafka.producer.simple import SimpleProducer

msg_size = 524288

class Producer(threading.Thread):
    daemon = True
    big_msg = "Hello master wayne" * 10

    def run(self):
        client = KafkaClient("localhost:9092")
        producer = SimpleProducer(client)
        self.sent = 0

        while True:
            producer.send_messages('topic.test.min.v1', self.big_msg)
            time.sleep(0.005)
            self.sent += 1


class Consumer(threading.Thread):
    daemon = True

    def run(self):
        client = KafkaClient("localhost:9092")

        consumer = SimpleConsumer(client, "test-group", "topic.test.min.v1",
            max_buffer_size = None,
        )

        self.valid = 0
        self.invalid = 0

        m_len=len("Hello master wayne" * 10)

        consumer.seek(0,0)

        for message in consumer:
            try:
                if len(message.message.value) == m_len:
                    self.valid += 1
                else:
                    self.invalid += 1
            except:
                print "Reset Offset"
                consumer.seek(0,0)


def main():
    threads = [
        Producer(),
        Consumer()
    ]

    for t in threads:
        t.start()

    time.sleep(10)
    print 'Messages sent: %d' % threads[0].sent
    print 'Messages recvd: %d' % threads[1].valid
    print 'Messages invalid: %d' % threads[1].invalid

main()
