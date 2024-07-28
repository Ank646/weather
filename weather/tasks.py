from celery import shared_task
from .utils import check_alerts


@shared_task
def my_periodic_task():
    check_alerts()
    print("This task runs every 5 minutes.")
