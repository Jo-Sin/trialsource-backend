from celery import shared_task

@shared_task()
def heartbeat():
    print("Celery: Heartbeat")