"""
RGU Hub Backend - Recruitment App Models

This module defines models for handling recruitment and job opportunities
for students in various academic programs.

Models Overview:
- Recruitment: Job postings and opportunities for students

Database Relationships:
Program -> Recruitment (One-to-Many)

Author: RGU Hub Development Team
Last Updated: 2025
"""

from django.db import models
from resources.models import Program

class Recruitment(models.Model):
    """
    Represents job postings and recruitment opportunities for students.
    
    Links job opportunities to specific academic programs and provides
    comprehensive job details including requirements, deadlines, and application links.
    
    Fields:
    - id: Auto-generated primary key
    - program: Foreign key to Program model (BSCN, BPT, etc.)
    - company_name: Name of the hiring company/organization
    - position: Job title/position name
    - location: Job location (city, state, etc.)
    - job_type: FT (Full-Time), PT (Part-Time), or IN (Internship)
    - description: Detailed job description
    - requirements: Required qualifications and skills
    - salary: Salary information (optional)
    - deadline: Application deadline date
    - apply_link: URL to apply for the position
    - posted_on: When the job was posted (auto-generated)
    
    Usage in API:
    - GET /recruitments/ - List all job postings
    - GET /recruitments/?program=BSCN - Filter by program
    - GET /recruitments/?program=BPT - Filter by program
    
    Job Types:
    - FT: Full-Time positions
    - PT: Part-Time positions  
    - IN: Internship opportunities
    """
    JOB_TYPES = [
        ('FT', 'Full-Time'),
        ('PT', 'Part-Time'),
        ('IN', 'Internship')
    ]
    
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="recruitments")
    company_name = models.CharField(max_length=255, help_text="Name of the hiring company")
    position = models.CharField(max_length=255, help_text="Job title/position")
    location = models.CharField(max_length=255, help_text="Job location")
    job_type = models.CharField(max_length=2, choices=JOB_TYPES, default='FT', help_text="Type of employment")
    description = models.TextField(help_text="Detailed job description")
    requirements = models.TextField(help_text="Required qualifications and skills")
    salary = models.CharField(max_length=100, blank=True, null=True, help_text="Salary information")
    deadline = models.DateField(help_text="Application deadline")
    apply_link = models.URLField(max_length=500, help_text="URL to apply for the position")   
    posted_on = models.DateTimeField(auto_now_add=True, help_text="When the job was posted")

    class Meta:
        ordering = ["-posted_on"]
        verbose_name = "Job Posting"
        verbose_name_plural = "Job Postings"

    def __str__(self):
        return f"{self.position} at {self.company_name}"