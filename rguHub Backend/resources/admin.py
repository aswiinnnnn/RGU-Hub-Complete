from django.contrib import admin
from .models import Program, Syllabus, Term, Subject, SubjectMaterial, MaterialType
from django.utils.html import format_html
import os

# ----------------- Program Admin -----------------
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("short_name", "name", "duration_years")
    search_fields = ("name", "short_name")


# ----------------- Syllabus Admin -----------------
@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ("name", "program", "effective_from", "effective_to")
    list_filter = ("program",)
    search_fields = ("name", "program__name")


# ----------------- Term Admin -----------------
@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ("name", "syllabus", "term_number", "term_type")
    list_filter = ("term_type", "syllabus__program")
    search_fields = ("name", "syllabus__name", "syllabus__program__name")
    ordering = ["syllabus__program__short_name", "syllabus__name", "term_number"]


# ----------------- Subject Admin -----------------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "subject_type", "term")
    list_filter = ("subject_type", "term__syllabus__program")
    search_fields = ("code", "name")
    ordering = ["term__syllabus__program__short_name", "term__syllabus__name", "term__term_number", "code"]


# ----------------- SubjectMaterial Admin -----------------
@admin.register(SubjectMaterial)
class SubjectMaterialAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "subject",
        "material_type",
        "year",
        "file_type",
        "file_size",
        "uploaded_link",
        "created_at",
        "is_active",
    )
    list_filter = ("is_active", "subject__term__syllabus__program", "material_type", "year")
    search_fields = ("title", "subject__name", "subject__code")
    readonly_fields = ("file_url", "file_type", "file_size", "created_at")

    def uploaded_link(self, obj):
        url = self.file_url(obj)
        if url:
            return format_html(f"<a href='{url}' target='_blank'>Open File</a>")
        return "-"
    def file_url(self, obj):
        try:
            if obj.file and hasattr(obj.file, 'url') and obj.file.url:
                return obj.file.url
        except Exception:
            pass
        return getattr(obj, 'url', None)
    file_url.short_description = "Cloudinary URL"
    uploaded_link.short_description = "Cloudinary URL"

    def file_type(self, obj):
        if obj.file and obj.file.name:
            return os.path.splitext(obj.file.name)[1].lstrip(".").upper()
        return "-"
    file_type.short_description = "File Type"

    def file_size(self, obj):
        if obj.file and hasattr(obj.file, "size"):
            size = obj.file.size
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.2f} KB"
            elif size < 1024 * 1024 * 1024:
                return f"{size / (1024 * 1024):.2f} MB"
            else:
                return f"{size / (1024 * 1024 * 1024):.2f} GB"
        return "Unknown"
    file_size.short_description = "File Size"


# ----------------- MaterialType Admin -----------------
@admin.register(MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "slug")
    search_fields = ("name", "slug")
