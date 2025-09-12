from rest_framework import viewsets
from itertools import chain
from rest_framework.response import Response
from rest_framework.decorators import api_view
from resources.models import SubjectMaterial
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
    






class LatestUpdatesViewSet(viewsets.ViewSet):
    def list(self, request):
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