from rest_framework import serializers
from .models import Subject, SubjectMaterial

class SubjectMaterialSerializer(serializers.ModelSerializer):
    subject_id = serializers.IntegerField(source="subject.id", read_only=True)
    subject_code = serializers.CharField(source="subject.code", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)

    class Meta:
        model = SubjectMaterial
        fields = [
            "id",               # numeric material id
            "subject_id",
            "subject_code",
            "subject_name",
            "title",
            "url",
            "description",
            "is_active",
            "created_at",
        ]
