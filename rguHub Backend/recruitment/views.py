from rest_framework import viewsets
from .models import Recruitment
from .serializers import RecruitmentSerializer

class RecruitmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recruitment.objects.all().order_by("-posted_on")
    serializer_class = RecruitmentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        program_filter = self.request.query_params.get("program", None)
        if program_filter:
            queryset = queryset.filter(program__short_name__iexact=program_filter)
        return queryset
