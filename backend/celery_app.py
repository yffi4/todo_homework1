from celery import Celery

celery = Celery(
    'backend',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

celery.conf.task_routes = {
    'backend.tasks.*': {'queue': 'default'}
} 