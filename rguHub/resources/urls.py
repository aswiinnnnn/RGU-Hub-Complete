from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectMaterialViewSet, SubjectViewSet


router = DefaultRouter()
router.register(r"materials", SubjectMaterialViewSet, basename="material")
router.register(r"subject", SubjectViewSet, basename="subject")


urlpatterns = [
    path("", include(router.urls)),
]

