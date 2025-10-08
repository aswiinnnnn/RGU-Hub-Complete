"""
RGU Hub Backend - Resources App URL Configuration

This module defines URL patterns for the resources app API endpoints.
It uses Django REST Framework routers to automatically generate
URL patterns for ViewSets.

URL Patterns:
- /materials/ - SubjectMaterialViewSet endpoints
- /subjects/ - SubjectViewSet endpoints  
- /material-types/ - MaterialTypeViewSet endpoints

Generated Endpoints:
- GET /materials/ - List all materials
- GET /materials/{id}/ - Get specific material
- POST /materials/ - Create new material
- PUT/PATCH /materials/{id}/ - Update material
- DELETE /materials/{id}/ - Delete material
- GET /subjects/ - List all subjects
- GET /subjects/{id}/ - Get specific subject
- GET /material-types/ - List all material types
- GET /material-types/{id}/ - Get specific material type

Author: RGU Hub Development Team
Last Updated: 2025
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectMaterialViewSet, SubjectViewSet, MaterialTypeViewSet

# Create router instance
router = DefaultRouter()

# Register ViewSets with router
router.register(r"materials", SubjectMaterialViewSet, basename="material")
router.register(r'subjects', SubjectViewSet)
router.register(r'material-types', MaterialTypeViewSet)

# URL patterns
urlpatterns = [
    path("", include(router.urls)),
]

