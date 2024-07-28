from django.core.management.base import BaseCommand
from weather.utils import fetch_weather_data, check_alerts
from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import time


def my_periodic_task():
    check_alerts()
    print("This task runs every 1 minutes.")
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

class Command(BaseCommand):
    help = 'Run APScheduler'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=pytz.utc)
        scheduler.add_job(my_periodic_task, IntervalTrigger(minutes=1))
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass
