"""
RGU Hub Backend - Resources App Models

This module defines the core data models for the RGU Hub application.
It handles academic programs, syllabi, terms, subjects, material types, and study materials.

Models Overview:
- Program: Academic programs (B.Sc Nursing, BPT, etc.)
- Syllabus: Different curriculum versions (CBCS 2022, etc.)
- Term: Flexible terms (Semesters or Years)
- Subject: Individual subjects within terms
- MaterialType: Types of study materials (Notes, PYQ, etc.)
- SubjectMaterial: Actual study material files stored in Cloudinary

Database Relationships:
Program -> Syllabus -> Term -> Subject -> SubjectMaterial
                    -> MaterialType -> SubjectMaterial

Author: RGU Hub Development Team
Last Updated: 2025
"""

from django.db import models
from django.utils.text import slugify


class Program(models.Model):
    """
    Represents an academic program/course offered by the university.
    
    Examples:
    - B.Sc Nursing (4 years)
    - B.Sc Physiotherapy (4 years)
    - M.Sc Nursing (2 years)
    
    Fields:
    - id: Auto-generated primary key
    - name: Full program name (e.g., "Bachelor of Science in Nursing")
    - short_name: Abbreviated name for URLs/filtering (e.g., "BSCN")
    - duration_years: Program duration in years
    
    Usage in API:
    - GET /subjects/?course=BSCN - Filter subjects by program
    - GET /recruitments/?program=BSCN - Filter jobs by program
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, help_text="Full program name")
    short_name = models.CharField(max_length=50, unique=True, help_text="Short code for API filtering")
    duration_years = models.PositiveSmallIntegerField(help_text="Program duration in years")

    class Meta:
        ordering = ["name"]
        verbose_name = "Academic Program"
        verbose_name_plural = "Academic Programs"

    def __str__(self) -> str:
        return f"{self.name}"


class Syllabus(models.Model):
    """
    Represents a syllabus/curriculum version for a specific program.
    
    Different programs may have multiple syllabus versions over time.
    Examples:
    - CBCS 2022 (Choice Based Credit System)
    - RGUHS 2020 (Rajiv Gandhi University of Health Sciences)
    - INC 2018 (Indian Nursing Council)
    
    Fields:
    - id: Auto-generated primary key
    - program: Foreign key to Program model
    - name: Syllabus name/version
    - effective_from: When this syllabus became effective
    - effective_to: When this syllabus was replaced (optional)
    
    Usage:
    - Links programs to their curriculum versions
    - Helps organize subjects by academic year/regulation
    """
    id = models.AutoField(primary_key=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="syllabi")
    name = models.CharField(max_length=255, help_text="Syllabus name/version")
    effective_from = models.DateField(null=True, blank=True, help_text="Effective start date")
    effective_to = models.DateField(null=True, blank=True, help_text="Effective end date")

    class Meta:
        ordering = ["program__short_name", "name"]
        unique_together = ("program", "name")
        verbose_name = "Syllabus"
        verbose_name_plural = "Syllabi"

    def __str__(self) -> str:
        return f"{self.program.name} - {self.name}"


class Term(models.Model):
    """
    Flexible term structure that can represent either Semesters or Years.
    
    This model allows the system to handle different academic structures:
    - Semester-based: 1st Semester, 2nd Semester, etc.
    - Year-based: 1st Year, 2nd Year, etc.
    
    Fields:
    - id: Auto-generated primary key
    - syllabus: Foreign key to Syllabus model
    - term_number: Sequential number (1, 2, 3, etc.)
    - term_type: Either "SEMESTER" or "YEAR"
    - name: Optional display name (e.g., "First Year", "Semester I")
    - slug: URL-friendly identifier (auto-generated)
    
    Usage in API:
    - GET /subjects/?course=BSCN&sem=1 - Get 1st semester subjects
    - GET /subjects/?course=BSCN&year=1 - Get 1st year subjects
    """

    class TermType(models.TextChoices):
        SEMESTER = "SEMESTER", "Semester"
        YEAR = "YEAR", "Year"

    id = models.AutoField(primary_key=True)    
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE, related_name="terms")
    term_number = models.PositiveSmallIntegerField(help_text="1 for first term, 2 for second, etc.")
    term_type = models.CharField(max_length=16, choices=TermType.choices)
    name = models.CharField(max_length=100, blank=True, help_text="Optional display name")
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        ordering = ["syllabus__program__short_name", "syllabus__name", "term_number"]
        verbose_name = "Academic Term"
        verbose_name_plural = "Academic Terms"

    def __str__(self) -> str:
        label = self.name or f"{self.get_term_type_display()} {self.term_number}"
        return f"{self.syllabus} - {label}"


class Subject(models.Model):
    """
    Represents an individual subject/course within an academic term.
    
    Each subject belongs to a specific term and has a unique code.
    Examples:
    - BN101 - Anatomy and Physiology (Theory)
    - BN102 - Anatomy and Physiology (Practical)
    - BN201 - Medical Surgical Nursing (Clinical)
    
    Fields:
    - id: Auto-generated primary key
    - term: Foreign key to Term model
    - code: Subject code (e.g., "BN101", "BN102")
    - name: Full subject name
    - subject_type: THEORY, PRACTICAL, or CLINICAL
    - slug: URL-friendly identifier (auto-generated)
    
    Usage in API:
    - GET /materials/?subject=bn101-anatomy-physiology - Get materials for specific subject
    - GET /subjects/?course=BSCN&sem=1 - Get all 1st semester subjects
    """

    class SubjectType(models.TextChoices):
        THEORY = "THEORY", "Theory"
        PRACTICAL = "PRACTICAL", "Practical"
        CLINICAL = "CLINICAL", "Clinical"
        
    id = models.AutoField(primary_key=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="subjects")
    code = models.CharField(max_length=50, help_text="Subject code (e.g., BN101)")
    name = models.CharField(max_length=255, help_text="Full subject name")
    subject_type = models.CharField(max_length=16, choices=SubjectType.choices)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        ordering = [
        "term__syllabus__program__short_name",  # Program short name
        "term__syllabus__name",                 # Syllabus name
        "term__term_number",
        "code",]

        unique_together = ("term", "code")

    def _str_(self) -> str:
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        """
        Auto-generate a unique slug for the subject if not provided.

        The slug is built from the program short name, term number and subject code,
        falling back to code and name if needed. If a slug collision occurs,
        a numeric suffix is appended.
        """
        if not self.slug:
            # Try to build a meaningful base using related Term/Syllabus/Program
            base_parts = []
            try:
                if self.term and self.term.syllabus and self.term.syllabus.program:
                    prog = self.term.syllabus.program.short_name
                    base_parts.append(str(prog))
                if self.term and getattr(self.term, 'term_number', None) is not None:
                    base_parts.append(str(self.term.term_number))
            except Exception:
                # If relations are not available for some reason, ignore and continue
                pass

            # Prefer using code (short, likely unique per term) then name
            if self.code:
                base_parts.append(self.code)
            elif self.name:
                base_parts.append(self.name)

            base = slugify("-".join(base_parts)) or slugify(self.code or self.name) or "subject"

            slug_candidate = base
            counter = 1
            Model = self._class_
            while Model.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                counter += 1
                slug_candidate = f"{base}-{counter}"

            self.slug = slug_candidate

        super().save(*args, **kwargs)


class MaterialType(models.Model):
    """
    Represents different categories/types of study materials.
    
    This model categorizes study materials for better organization and filtering.
    Examples:
    - Notes: Lecture notes and handouts
    - PYQ: Previous Year Question papers
    - Question Bank: Unit-wise questions
    - Syllabus: Course outlines
    - Practical Resources: Lab guides, clinical logs
    
    Fields:
    - id: Auto-generated primary key
    - name: Material type name
    - slug: URL-friendly identifier (auto-generated)
    - description: Detailed description
    - icon: Frontend icon identifier
    - color: UI color theme
    
    Usage in API:
    - GET /material-types/ - List all material types
    - GET /materials/?type=notes - Filter materials by type
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, help_text="Material type name")
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, help_text="Detailed description")
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or identifier")
    color = models.CharField(max_length=20, blank=True, help_text="Color theme for UI")

    class Meta:
        ordering = ["name"]
        verbose_name = "Material Type"
        verbose_name_plural = "Material Types"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage
import os

class SubjectMaterial(models.Model):
    """
    Stores study material files with metadata and Cloudinary integration.
    
    This is the core model that stores actual study materials (PDFs, documents, etc.)
    uploaded to Cloudinary cloud storage. Each material is linked to a subject and
    optionally categorized by material type.
    
    Fields:
    - id: Auto-generated primary key
    - subject: Foreign key to Subject model
    - material_type: Foreign key to MaterialType (optional)
    - title: Display title (auto-filled from filename)
    - file: Cloudinary file field
    - url: Cloudinary URL (auto-filled)
    - description: Additional description
    - year: Year for PYQs and time-sensitive materials
    - month: Month for PYQs (July, December, etc.)
    - is_active: Whether material is available for download
    - created_at: Upload timestamp
    
    Usage in API:
    - GET /materials/ - List all materials
    - GET /materials/?subject=bn101-anatomy-physiology - Filter by subject
    - GET /materials/?type=pyq - Filter by material type
    - GET /materials/?subject=bn101&type=notes - Combined filtering
    
    Cloudinary Integration:
    - Files are automatically uploaded to Cloudinary
    - URLs are auto-generated for direct download
    - Supports PDF, DOC, images, and other formats
    """
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE, related_name="materials")
    material_type = models.ForeignKey("MaterialType", on_delete=models.CASCADE, related_name="materials", null=True, blank=True)
    title = models.CharField(max_length=255, help_text="Display title (auto-filled from filename)")
    file = models.FileField(storage=MediaCloudinaryStorage(), upload_to="materials/")
    url = models.URLField(blank=True, help_text="Auto-filled Cloudinary URL")
    description = models.TextField(blank=True, help_text="Additional description")
    year = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Year for PYQs and time-sensitive materials")
    month = models.CharField(max_length=20, blank=True, null=True, help_text="Month for PYQs (e.g., 'July', 'December')")
    is_active = models.BooleanField(default=True, help_text="Whether material is available")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Upload timestamp")

    class Meta:
        ordering = ["-year", "-created_at"]

    def save(self, *args, **kwargs):
        """
        Auto-fill title from filename and URL from Cloudinary.
        
        When a file is uploaded:
        1. Extract filename as title
        2. Get Cloudinary URL for direct access
        3. Save the material record
        """
        if self.file:
            self.title = os.path.basename(self.file.name)
            self.url = self.file.url
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """String representation with year/month info for PYQs."""
        if self.year and self.month:
            return f"{self.subject.code} - {self.title} ({self.month} {self.year})"
        return f"{self.subject.code} - {self.title}"