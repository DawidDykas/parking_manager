from config.setting import celery_settings  
from celery import Celery


celery = Celery("worker", broker = celery_settings.URL_BROKER) # temp 


