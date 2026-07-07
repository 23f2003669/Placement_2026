import os
import sys
from celery import Celery
from celery.schedules import crontab

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

celery_app = Celery('placement_portal')

celery_app.conf.update(
    broker_url='redis://localhost:6379/1',
    result_backend='redis://localhost:6379/2',
    timezone='UTC',
    enable_utc=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    imports=['tasks'],
    task_always_eager=False,
    task_eager_propagates=True,
)

# ---- Beat schedule ----
celery_app.conf.beat_schedule = {
    'daily-deadline-reminders': {
        'task': 'send_daily_reminders',
        'schedule': crontab(hour=9, minute=0),
    },
    'monthly-placement-report': {
        'task': 'generate_monthly_report',
        'schedule': crontab(day_of_month=1, hour=8, minute=0),
    },
}

# ---- Flask app-context wrapper (lazy, avoids circular import) ----
_flask_app = None


class ContextTask(celery_app.Task):
    def __call__(self, *args, **kwargs):
        global _flask_app
        if _flask_app is None:
            from app import create_app
            _flask_app = create_app()
        with _flask_app.app_context():
            return self.run(*args, **kwargs)


celery_app.Task = ContextTask
