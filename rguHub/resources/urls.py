from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectMaterialViewSet


router = DefaultRouter()
router.register(r"materials", SubjectMaterialViewSet, basename="material")


urlpatterns = [
    path("", include(router.urls)),
]

