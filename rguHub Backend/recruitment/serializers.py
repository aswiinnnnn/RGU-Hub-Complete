"""
RGU Hub Backend - Recruitment App Serializers

This module contains Django REST Framework serializers for converting
Recruitment model instances to JSON and handling API data validation.

Serializers Overview:
- RecruitmentSerializer: Serializes Recruitment model with program name

Author: RGU Hub Development Team
Last Updated: 2025
"""

from rest_framework import serializers
from .models import Recruitment

class RecruitmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Recruitment model with expanded program information.
    
    Includes program name for easier frontend consumption.
    Exposes all fields of the Recruitment model for API consumption.
    
    Fields:
    - id: Job posting primary key
    - program: Program's primary key
    - program_name: Full program name (e.g., "Bachelor of Science in Nursing")
    - company_name: Hiring company name
    - position: Job title/position
    - location: Job location
    - job_type: FT, PT, or IN
    - description: Detailed job description
    - requirements: Required qualifications
    - salary: Salary information (optional)
    - deadline: Application deadline
    - apply_link: Application URL
    - posted_on: When job was posted
    """
    # Include program name for easier frontend consumption
    program_name = serializers.CharField(source="program.name", read_only=True)

    class Meta:
        model = Recruitment
        fields = "__all__"
