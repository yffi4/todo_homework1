from celery import Celery

celery = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

celery.conf.task_routes = {
    'tasks.*': {'queue': 'default'}
} 