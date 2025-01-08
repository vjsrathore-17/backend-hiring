from django.urls import path, include # type: ignore
from rest_framework.routers import DefaultRouter # type: ignore
from .views import JobTypeViewSet, CustomerTypeViewSet, JobViewSet
router = DefaultRouter()
router.register(r'job-types', JobTypeViewSet)
router.register(r'customer-types', CustomerTypeViewSet)
router.register(r'tasks', JobViewSet)

urlpatterns = [
    path('', include(router.urls)),
]