from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecruitmentViewSet, LatestUpdatesViewSet  

router = DefaultRouter()
router.register(r"recruitments", RecruitmentViewSet, basename="recruitments")
router.register(r"latest-updates", LatestUpdatesViewSet, basename="latest-updates")  

urlpatterns = [
    path("", include(router.urls)),
]
