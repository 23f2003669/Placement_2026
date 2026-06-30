from celery import Celery
from config import Config

# Create Celery app
celery_app = Celery('placement_portal')

# Configure Celery
celery_app.conf.update(
    broker_url='redis://localhost:6379/1',
    result_backend='redis://localhost:6379/2',
    timezone='UTC',
    enable_utc=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    imports=['tasks'],
    task_always_eager=False,  # Run async tasks
    task_eager_propagates=True,
)

# This function runs before task execution
def on_before_task_publish(sender=None, body=None, **kwargs):
    pass

# Connect signal
from celery.signals import before_task_publish
before_task_publish.connect(on_before_task_publish)