import pika
import time
import sys

RABBITMQ_PORT=5672

connection = pika.BlockingConnection(pika.ConnectionParameters(
               '192.168.1.169',RABBITMQ_PORT))

channel = connection.channel()

channel.queue_declare(queue='youtube')


while True:
    line=sys.stdin.readline()
    channel.basic_publish(exchange='',
                        routing_key='youtube',
                        body=line)
    print " [x] Sent ", line
    time.sleep(0.1)

connection.close()
