"""
RGU Hub Backend - Recruitment App Views

This module contains Django REST Framework ViewSets for handling API requests
related to job postings and recruitment opportunities.

ViewSets Overview:
- RecruitmentViewSet: Read-only access to job postings with program filtering
- LatestUpdatesViewSet: Custom viewset for combining recent materials and jobs

API Endpoints:
- GET /recruitments/ - List all job postings
- GET /recruitments/?program=BSCN - Filter by program
- GET /latest-updates/ - Get recent materials and job postings

Author: RGU Hub Development Team
Last Updated: 2025
"""

from rest_framework import viewsets
from itertools import chain
from rest_framework.response import Response
from rest_framework.decorators import api_view
from resources.models import SubjectMaterial
from .models import Recruitment
from .serializers import RecruitmentSerializer

class RecruitmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only ViewSet for Recruitment model with program filtering.
    
    Provides list and retrieve operations for job postings with optional
    filtering by academic program.
    
    Endpoints:
    - GET /recruitments/ - List all job postings
    - GET /recruitments/?program=BSCN - Filter by program short name
    - GET /recruitments/{id}/ - Get specific job posting
    
    Query Parameters:
    - program: Program short name (case-insensitive, e.g., "BSCN", "BPT")
    
    Response Format:
    {
        "id": 1,
        "program": 1,
        "program_name": "Bachelor of Science in Nursing",
        "company_name": "Apollo Hospitals",
        "position": "Staff Nurse",
        "location": "Bangalore, Karnataka",
        "job_type": "FT",
        "description": "Looking for experienced staff nurses...",
        "requirements": "B.Sc Nursing degree, 2+ years experience...",
        "salary": "₹25,000 - ₹35,000",
        "deadline": "2025-02-15",
        "apply_link": "https://apollo.com/careers/apply",
        "posted_on": "2025-01-15T10:30:00Z"
    }
    """
    queryset = Recruitment.objects.all().order_by("-posted_on")
    serializer_class = RecruitmentSerializer

    def get_queryset(self):
        """
        Override get_queryset to add program filtering.
        
        Filters job postings by program short name (case-insensitive).
        If no program filter is provided, returns all job postings.
        """
        queryset = super().get_queryset()
        program_filter = self.request.query_params.get("program", None)
        if program_filter:
            queryset = queryset.filter(program__short_name__iexact=program_filter)
        return queryset

class LatestUpdatesViewSet(viewsets.ViewSet):
    """
    Custom ViewSet for combining recent materials and job postings.
    
    Provides a unified endpoint that returns the most recent study materials
    and job postings, sorted by creation/posted date. Used for the homepage
    "Latest Updates" section.
    
    Endpoints:
    - GET /latest-updates/ - Get recent materials and job postings
    
    Response Format:
    [
        {
            "type": "Material",
            "title": "anatomy_notes.pdf",
            "created_at": "2025-01-15T10:30:00Z"
        },
        {
            "type": "Recruitment", 
            "title": "Staff Nurse at Apollo Hospitals",
            "created_at": "2025-01-14T15:20:00Z"
        }
    ]
    """
    def list(self, request):
        """
        Combine recent materials and job postings into a unified response.
        
        Fetches the 6 most recent materials and 6 most recent job postings,
        combines them, sorts by date, and returns the 6 most recent items.
        """
        # fetch last 5 subject materials
        materials = SubjectMaterial.objects.order_by("-created_at")[:6]
        recruitments = Recruitment.objects.order_by("-posted_on")[:6]

        # combine and sort by date
        combined = sorted(
            list(materials) + list(recruitments),
            key=lambda x: x.created_at if hasattr(x, "created_at") else x.posted_on,
            reverse=True,
        )[:6]

        data = []
        for obj in combined:
            if isinstance(obj, SubjectMaterial):
                data.append({
                    "type": "Material",
                    "title": obj.title,
                    "created_at": obj.created_at,
                })
            else:
                data.append({
                    "type": "Recruitment",
                    "title": f"{obj.position} at {obj.company_name}",
                    "created_at": obj.posted_on,
                })

        return Response(data)