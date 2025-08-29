from rest_framework import viewsets
from .models import SubjectMaterial
from .serializers import SubjectMaterialSerializer


class SubjectMaterialViewSet(viewsets.ModelViewSet):
    queryset = SubjectMaterial.objects.all()
    serializer_class = SubjectMaterialSerializer

    def list(self, request, *args, **kwargs):
        subject_slug = request.query_params.get("subject")
        qs = self.queryset
        if subject_slug:
            qs = qs.filter(subject__slug=subject_slug)
        self.queryset = qs
        return super().list(request, *args, **kwargs)
