from .celery_app import celery

@celery.task
def sample_task(x: int, y: int) -> int:
    return x + y 