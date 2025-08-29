from rest_framework import viewsets
from .models import SubjectMaterial, Subject
from .serializers import SubjectMaterialSerializer, SubjectSerializer


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


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.select_related("term", "term__syllabus", "term__syllabus__program").all()
    serializer_class = SubjectSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        term_slug = self.request.query_params.get("term")  # ?term=<term-slug>
        if term_slug:
            qs = qs.filter(term__slug=term_slug)
        return qs
