"""
RGU Hub Backend - Resources App Serializers

This module contains Django REST Framework serializers for converting
model instances to JSON and handling API data validation.

Serializers Overview:
- MaterialTypeSerializer: Serializes MaterialType model
- SubjectMaterialSerializer: Serializes SubjectMaterial with related data
- SubjectSerializer: Serializes Subject with material count

Each serializer defines which fields are exposed in the API and how
related models are represented.

Author: RGU Hub Development Team
Last Updated: 2025
"""

from rest_framework import serializers
from .models import Subject, SubjectMaterial, MaterialType

class MaterialTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for MaterialType model.
    
    Exposes all fields of MaterialType for API consumption.
    Used in material filtering and UI display.
    
    Fields:
    - id: Primary key
    - name: Material type name (e.g., "Notes", "PYQ")
    - slug: URL-friendly identifier
    - description: Detailed description
    - icon: Frontend icon identifier
    - color: UI color theme
    """
    class Meta:
        model = MaterialType
        fields = ["id", "name", "slug", "description", "icon", "color"]

class SubjectMaterialSerializer(serializers.ModelSerializer):
    """
    Serializer for SubjectMaterial model with expanded related data.
    
    Includes subject information and material type details for easier
    frontend consumption. Flattens related model data for better API design.
    
    Fields:
    - id: Material primary key
    - subject_id: Subject's primary key
    - subject_code: Subject code (e.g., "BN101")
    - subject_name: Full subject name
    - material_type: Complete MaterialType object
    - title: Material title/filename
    - url: Cloudinary download URL
    - description: Additional description
    - year: Year for PYQs
    - month: Month for PYQs
    - is_active: Availability status
    - created_at: Upload timestamp
    """
    # Flatten subject data for easier frontend consumption
    subject_id = serializers.IntegerField(source="subject.id", read_only=True)
    subject_code = serializers.CharField(source="subject.code", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    
    # Include complete material type object
    material_type = MaterialTypeSerializer(read_only=True)

    class Meta:
        model = SubjectMaterial
        fields = [
            "id",               # numeric material id
            "subject_id",       # subject's primary key
            "subject_code",     # subject code (BN101, etc.)
            "subject_name",     # full subject name
            "material_type",    # complete material type object
            "title",            # material title/filename
            "url",              # Cloudinary download URL
            "description",      # additional description
            "year",             # year for PYQs
            "month",            # month for PYQs
            "is_active",        # availability status
            "created_at",       # upload timestamp
        ]

class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Subject model with material count and term information.
    
    Includes computed material count and flattened term data for easier
    frontend consumption and better API design.
    
    Fields:
    - id: Subject primary key
    - code: Subject code (e.g., "BN101")
    - name: Full subject name
    - subject_type: THEORY, PRACTICAL, or CLINICAL
    - slug: URL-friendly identifier
    - term: Term's primary key
    - term_slug: Term's URL-friendly identifier
    - materials_count: Number of materials for this subject
    """
    # Computed field for material count
    materials_count = serializers.SerializerMethodField()
    
    # Flatten term data for easier frontend consumption
    term = serializers.IntegerField(source="term.id", read_only=True)
    term_slug = serializers.CharField(source="term.slug", read_only=True)

    class Meta:
        model = Subject
        fields = [
            "id",               # subject primary key
            "code",             # subject code (BN101, etc.)
            "name",             # full subject name
            "subject_type",     # THEORY, PRACTICAL, CLINICAL
            "slug",             # URL-friendly identifier
            "term",             # term's primary key
            "term_slug",        # term's URL-friendly identifier
            "materials_count",  # number of materials
        ]
    
    def get_materials_count(self, obj):
        """
        Compute the number of materials for this subject.
        
        Returns the count of active materials linked to this subject.
        Used for displaying material availability in the frontend.
        """
        return obj.materials.count()