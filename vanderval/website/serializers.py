from rest_framework import serializers # type: ignore
from .models import JobType, CustomerType, Job

class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = '__all__'

class CustomerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerType
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
