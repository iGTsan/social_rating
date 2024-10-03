import pika
import time
import sys

# Connect to RabbitMQ
while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        break
    except Exception:
        print("Failed to connect to RabbitMQ")
        sys.stdout.flush()
        time.sleep(2)
        continue

# Declare the queue
channel.queue_declare(queue='test') 

# Send message
message = 'Hello World'
channel.basic_publish(exchange='',
                      routing_key='test',
                      body=message)
print(f"Sent message: {message}")
sys.stdout.flush()

# Send multiple messages
for i in range(10):
    message = f"Message {i+1}"
    channel.basic_publish(exchange='',
                          routing_key='test',
                          body=message)
    print(f"Sent message: {message}")
    sys.stdout.flush()
    time.sleep(1)

# Close connection
connection.close()
