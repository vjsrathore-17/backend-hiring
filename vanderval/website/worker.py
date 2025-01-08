from celery.worker.strategy import default_strategy # type: ignore
from .models import Job, Site

class PriorityWorker:
    def __init__(self, volume_type):
        self.volume_type = volume_type
    
    def get_next_job(self):
        return Job.objects.filter(
            status='PENDING',
            site__volume_type=self.volume_type
        ).order_by('created_at').first()