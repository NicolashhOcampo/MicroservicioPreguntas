import json
import pika, sys, os
from app.services.questions import QuestionService
from app.config.db import get_session_sync
def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange='catalog',
        exchange_type='direct',
        durable=False
    )
    # Declaramos la cola durable
    channel.queue_declare(queue='article_deleted', durable=False)

    # Bind de la cola al exchange "catalog" usando "article_deleted" como routing_key
    channel.queue_bind(
        exchange='catalog',
        queue='article_deleted',
        routing_key='article_deleted'
    )

    def callback(ch, method, properties, body):
        wrapper = json.loads(body)
        data = wrapper["message"]
        print("Article deleted:", data['articleId'])
        QuestionService.delete_questions_by_article(session=get_session_sync(), article_id=data['articleId'])
        ch.basic_ack(delivery_tag=method.delivery_tag)

    print(" [*] Waiting for messages. To exit press CTRL+C")

    # Consumimos sin auto-ack
    channel.basic_consume(
        queue='article_deleted',
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