from rest_framework import serializers
from .models import Recruitment

class RecruitmentSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source="program.name", read_only=True)

    class Meta:
        model = Recruitment
        fields = "__all__"
