import pika

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Declare queue
channel.queue_declare(queue='test')

# Publish message
channel.basic_publish(exchange='', routing_key='test', body='Hello World!')
print("Sent message")

# Define callback for receiving messages
def callback(ch, method, properties, body):
    print("Received: %r" % body)

# Set up subscription on queue
channel.basic_consume(queue='test',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

