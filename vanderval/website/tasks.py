import logging
from time import sleep
from celery import Celery # type: ignore
from django.conf import settings # type: ignore
from .models import Site, UserRecords, JobType, Job

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = Celery('tasks', broker=settings.CELERY_BROKER_URL)

@app.task
def process_job(job_id):
    job = Job.objects.get(id=job_id)
    try:
        job.status = 'RUNNING'
        job.save()
        
        # Simulate job execution
        sleep(job.job_type.execution_time)
        
        job.status = 'COMPLETED'
        job.save()
    except Exception as e:
        job.status = 'FAILED'
        job.save()
        raise e
