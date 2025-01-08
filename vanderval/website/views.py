from rest_framework import viewsets # type: ignore
from rest_framework.decorators import action # type: ignore
from rest_framework.response import Response # type: ignore
from .models import JobType, CustomerType, Job, Site
from .serializers import JobTypeSerializer, CustomerTypeSerializer, TaskSerializer
from .tasks import process_job

class JobTypeViewSet(viewsets.ModelViewSet):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer

class CustomerTypeViewSet(viewsets.ModelViewSet):
    queryset = CustomerType.objects.all()
    serializer_class = CustomerTypeSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = TaskSerializer
    
    @action(detail=False, methods=['POST'])
    def create_job(self, request):
        site = Site.objects.get(id=request.data['site_id'])
        job_type = JobType.objects.get(id=request.data['job_type_id'])
        
        job = Job.objects.create(
            site=site,
            job_type=job_type
        )
        
        # Send to appropriate queue based on volume type
        queue_name = f"{site.volume_type.lower()}_queue"
        process_job.apply_async(args=[job.id], queue=queue_name)
        
        return Response({'job_id': job.id})
