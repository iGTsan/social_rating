import pika, time, sys

while True:
    # Connect to RabbitMQ
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        break
    except:
        print("Failed to connect to RabbitMQ")
        sys.stdout.flush()
        time.sleep(2)
        continue



# Declare the queue
channel.queue_declare(queue='test')

# Define callback function to handle messages
def callback(ch, method, properties, body):
    print(f"Received: {body}")
    sys.stdout.flush()

# Set up subscription on the queue
channel.basic_consume(queue='test',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
sys.stdout.flush()

# Start consuming messages
channel.start_consuming()

