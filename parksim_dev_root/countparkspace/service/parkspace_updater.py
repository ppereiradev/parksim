from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .get_image import updateMarkers

def scheduler_start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(updateMarkers, 'interval', minutes=30)
    scheduler.start()