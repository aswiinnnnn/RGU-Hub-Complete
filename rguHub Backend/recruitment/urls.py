from django.urls import path,include
from .views import RecruitmentViewSet
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r"recruitments", RecruitmentViewSet, basename="recruitments")

urlpatterns = [
    path("", include(router.urls)),
]

