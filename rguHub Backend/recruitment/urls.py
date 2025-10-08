"""
RGU Hub Backend - Recruitment App URL Configuration

This module defines URL patterns for the recruitment app API endpoints.
It uses Django REST Framework routers to automatically generate
URL patterns for ViewSets.

URL Patterns:
- /recruitments/ - RecruitmentViewSet endpoints
- /latest-updates/ - LatestUpdatesViewSet endpoints

Generated Endpoints:
- GET /recruitments/ - List all job postings
- GET /recruitments/{id}/ - Get specific job posting
- GET /latest-updates/ - Get recent materials and job postings

Query Parameters:
- GET /recruitments/?program=BSCN - Filter by program
- GET /latest-updates/ - No parameters needed

Author: RGU Hub Development Team
Last Updated: 2025
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecruitmentViewSet, LatestUpdatesViewSet  

# Create router instance
router = DefaultRouter()

# Register ViewSets with router
router.register(r"recruitments", RecruitmentViewSet, basename="recruitments")
router.register(r"latest-updates", LatestUpdatesViewSet, basename="latest-updates")  

# URL patterns
urlpatterns = [
    path("", include(router.urls)),
]
