import json
import pika


def send_question_created_message(question_id: int, user_id: int):
    # Conexión con RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()

    # Declarar exchange
    channel.exchange_declare(
        exchange='stats',
        exchange_type='direct',
        durable=False
    )

    body = json.dumps({
        "message": {
            "questionId": question_id,
            "userId": user_id
        }
    })

    # Enviar al exchange "stats" usando la routing_key "question_created"
    channel.basic_publish(
        exchange='stats',
        routing_key='question_created',
        body=body
    )

    connection.close()
    print(f"[stats] Sent question_created message for question ID {question_id}")