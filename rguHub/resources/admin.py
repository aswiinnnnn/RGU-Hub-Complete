from django.contrib import admin
from .models import Program, Syllabus, Term, Subject, SubjectMaterial


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("short_name", "name", "duration_years")
    search_fields = ("name", "short_name")


@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ("name", "program", "effective_from", "effective_to")
    list_filter = ("program",)
    search_fields = ("name",)


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ("syllabus", "term_number", "term_type", "name")
    list_filter = ("term_type", "syllabus__program")
    search_fields = ("name",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "subject_type", "term")
    list_filter = ("subject_type", "term__syllabus__program")
    search_fields = ("code", "name")


@admin.register(SubjectMaterial)
class SubjectMaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "is_active", "created_at")
    list_filter = ("is_active", "subject__term__syllabus__program")
    search_fields = ("title", "subject__name", "subject__code")

# Register your models here.
