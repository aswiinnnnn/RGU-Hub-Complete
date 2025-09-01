from rest_framework import viewsets
from .models import SubjectMaterial, Subject, MaterialType
from .serializers import SubjectMaterialSerializer, SubjectSerializer, MaterialTypeSerializer
import logging

logger = logging.getLogger(__name__)

class MaterialTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MaterialType.objects.all()
    serializer_class = MaterialTypeSerializer

class SubjectMaterialViewSet(viewsets.ModelViewSet):
    queryset = SubjectMaterial.objects.all()
    serializer_class = SubjectMaterialSerializer

    def list(self, request, *args, **kwargs):
        subject_slug = request.query_params.get("subject")
        material_type = request.query_params.get("type")
        
        logger.info(f"[SubjectMaterialViewSet] Request received with subject slug: {subject_slug}, material type: {material_type}")
        
        qs = self.queryset
        if subject_slug:
            qs = qs.filter(subject__slug=subject_slug)
            logger.info(f"[SubjectMaterialViewSet] After subject filter: {qs.count()} materials")
            
        if material_type:
            qs = qs.filter(material_type__slug=material_type)
            logger.info(f"[SubjectMaterialViewSet] After material type filter: {qs.count()} materials")
            
        logger.info(f"[SubjectMaterialViewSet] Final queryset count: {qs.count()}")
        self.queryset = qs
        return super().list(request, *args, **kwargs)

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.select_related(
        "term", "term__syllabus", "term__syllabus__program"
    )
    serializer_class = SubjectSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        course = self.request.query_params.get("course")
        year = self.request.query_params.get("year")
        sem = self.request.query_params.get("sem")

        if not course:
            return qs  # no course provided, return all

        # make course case-insensitive
        qs = qs.filter(term__syllabus__program__short_name__iexact=course)

        if sem:
            try:
                sem = int(sem)
                qs = qs.filter(term__term_type="SEMESTER", term__term_number=sem)
            except (TypeError, ValueError):
                return qs.none()  # invalid sem
        elif year:
            try:
                year = int(year)
                qs = qs.filter(term__term_type="YEAR", term__term_number=year)
            except (TypeError, ValueError):
                return qs.none()  # invalid year
        print(qs.query)

        return qs

