"""
RGU Hub Backend - Main URL Configuration

This is the main URL configuration for the RGU Hub Django project.
It includes URL patterns from all Django apps and the admin interface.

URL Patterns:
- /admin/ - Django admin interface
- / - Resources app URLs (materials, subjects, material-types)
- / - Recruitment app URLs (recruitments, latest-updates)

Complete API Endpoints:
- GET /materials/ - List all study materials
- GET /materials/?subject=slug - Filter materials by subject
- GET /materials/?type=slug - Filter materials by type
- GET /subjects/ - List all subjects
- GET /subjects/?course=BSCN - Filter subjects by program
- GET /subjects/?course=BSCN&sem=1 - Filter by program and semester
- GET /material-types/ - List all material types
- GET /recruitments/ - List all job postings
- GET /recruitments/?program=BSCN - Filter jobs by program
- GET /latest-updates/ - Get recent materials and jobs

Admin Interface:
- /admin/ - Django admin for managing data

Author: RGU Hub Development Team
Last Updated: 2025
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),
    
    # Resources app URLs (materials, subjects, material-types)
    path('', include('resources.urls')),      
    
    # Recruitment app URLs (recruitments, latest-updates)
    path('', include('recruitment.urls')),     
]