from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectMaterialViewSet, SubjectViewSet, MaterialTypeViewSet


router = DefaultRouter()
router.register(r"materials", SubjectMaterialViewSet, basename="material")
router.register(r'subjects', SubjectViewSet)
router.register(r'material-types', MaterialTypeViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

