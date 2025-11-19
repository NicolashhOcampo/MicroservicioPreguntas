import json
import pika, sys, os
from app.utils.security import removeTokenFromCache

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()

    # Declarar el exchange fanout
    channel.exchange_declare(exchange='auth', exchange_type='fanout')

    # Crear una queue temporal, exclusiva para este consumidor
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Bind sin routing key (fanout ignora la key)
    channel.queue_bind(
        exchange='auth',
        queue=queue_name
    )

    def callback(ch, method, properties, body):
        data = json.loads(body)
        message = data["message"]
        print("[fanout] Leido:", message)
        res = removeTokenFromCache(message)
        print("Token removed from cache:", res)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    print(" [*] Waiting for fanout messages. CTRL+C to exit.")

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=False
    )

    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
