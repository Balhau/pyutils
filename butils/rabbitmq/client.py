import pika
import os
import sys
import time

CD_SAMBA_FOLDER="cd /media/samba/hdc1/MediaLibrary/tmp"
RABBITMQ_PORT=5672

def on_message(channel, method_frame, header_frame, body):
    print method_frame.delivery_tag
    print body
    print
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

def downloadURL(channel, method_frame, header_frame, body):
    try:
        print "Downloading ", body
        os.system(CD_SAMBA_FOLDER + " &&  youtube-dl "+body)
        print "Retrieving data from ", CD_SAMBA_FOLDER, " &&  youtube-dl ", body
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    except:
        print "Error"

connection = pika.BlockingConnection(pika.ConnectionParameters(
               '192.168.1.169',RABBITMQ_PORT))
channel = connection.channel()
channel.basic_consume(downloadURL, 'youtube')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
