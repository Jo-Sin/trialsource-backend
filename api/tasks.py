from celery import shared_task


@shared_task()
def heartbeat() -> None:
    print("Celery: Heartbeat")