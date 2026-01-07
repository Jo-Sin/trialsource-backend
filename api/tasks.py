from celery import shared_task

from .collector.anzctr import scrape_anzctr


@shared_task()
def heartbeat() -> None:
    print("Celery: Heartbeat")

@shared_task
def scrape() -> None:
    print("Celery: Start scraping")
    scrape_anzctr()
    print("Celery: End scraping")