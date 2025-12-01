from celery import shared_task

from .scraper import do_the_scrape


@shared_task()
def heartbeat() -> None:
    print("Celery: Heartbeat")

@shared_task
def scrape() -> None:
    print("Celery: Start scraping")
    do_the_scrape()
    print("Celery: End scraping")