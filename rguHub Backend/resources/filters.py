import django_filters
from .models import Subject, SubjectMaterial


class SubjectFilter(django_filters.FilterSet):
    program_id = django_filters.UUIDFilter(field_name="term__syllabus__program_id")
    syllabus_id = django_filters.UUIDFilter(field_name="term__syllabus_id")
    term_id = django_filters.UUIDFilter(field_name="term_id")
    subject_type = django_filters.CharFilter(field_name="subject_type")

    class Meta:
        model = Subject
        fields = ["program_id", "syllabus_id", "term_id", "subject_type", "code", "name"]


class SubjectMaterialFilter(django_filters.FilterSet):
    program_id = django_filters.UUIDFilter(field_name="subject__term__syllabus__program_id")
    syllabus_id = django_filters.UUIDFilter(field_name="subject__term__syllabus_id")
    term_number = django_filters.NumberFilter(field_name="subject__term__term_number")
    term_type = django_filters.ChoiceFilter(
        field_name="subject__term__term_type",
        choices=(
            ("SEMESTER", "Semester"),
            ("YEAR", "Year"),
        ),
    )

    class Meta:
        model = SubjectMaterial
        fields = ["program_id", "syllabus_id", "term_number", "term_type"]


