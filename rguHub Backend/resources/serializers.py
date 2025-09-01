from rest_framework import serializers
from .models import Subject, SubjectMaterial, MaterialType

class MaterialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialType
        fields = ["id", "name", "slug", "description", "icon", "color"]

class SubjectMaterialSerializer(serializers.ModelSerializer):
    subject_id = serializers.IntegerField(source="subject.id", read_only=True)
    subject_code = serializers.CharField(source="subject.code", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    material_type = MaterialTypeSerializer(read_only=True)

    class Meta:
        model = SubjectMaterial
        fields = [
            "id",               # numeric material id
            "subject_id",
            "subject_code",
            "subject_name",
            "material_type",
            "title",
            "url",
            "description",
            "year",
            "month",
            "is_active",
            "created_at",
        ]


class SubjectSerializer(serializers.ModelSerializer):
    materials_count = serializers.SerializerMethodField()
    term = serializers.IntegerField(source="term.id", read_only=True)
    term_slug = serializers.CharField(source="term.slug", read_only=True)

    class Meta:
        model = Subject
        fields = [
            "id",
            "code",
            "name",
            "subject_type",
            "slug",
            "term",
            "term_slug",
            "materials_count",
        ]
    
    def get_materials_count(self, obj):
        return obj.materials.count()
