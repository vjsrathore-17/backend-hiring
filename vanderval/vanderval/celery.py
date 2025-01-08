from __future__ import absolute_import, unicode_literals
import os
from kombu import Queue # type: ignore
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vanderval.settings')

app = Celery('vanderval')
app.config_from_object('django.conf:settings', namespace='CELERY')

def route_task(name, args, kwargs, options, task=None, **kw):
    if name == 'tasks.process_job':
        from website.models import Site
        site = Site.objects.get(id=args[0])
        return {'queue': f"{site.volume_type.lower()}_queue"}
    return None

app.conf.update(
    task_routes=(route_task,),
    task_queues=(
        Queue('small_queue', routing_key='small.#'),
        Queue('medium_queue', routing_key='medium.#'),
        Queue('large_queue', routing_key='large.#'),
    )
)
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')