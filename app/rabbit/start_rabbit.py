import threading
from app.rabbit.article_deleted_consumer import start_article_deleted_consumer
from app.rabbit.logout_consumer import start_logout_consumer


def start_rabbit_consumers():
    print("[*] Iniciando consumers RabbitMQ...")

    # Consumer 1
    t1 = threading.Thread(
        target=start_article_deleted_consumer,
        daemon=True
    )
    t1.start()

    # Consumer 2
    t2 = threading.Thread(
        target=start_logout_consumer,
        daemon=True
    )
    t2.start()

    print("[*] Consumers iniciados en paralelo")