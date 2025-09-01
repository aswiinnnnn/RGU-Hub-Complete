from django.contrib import admin
from .models import Program, Syllabus, Term, Subject, SubjectMaterial
import os
import cloudinary.uploader


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
    list_display = ("title", "subject", "file_type", "file_size", "cloudinary_url", "is_active", "created_at")
    list_filter = ("is_active", "subject__term__syllabus__program")
    search_fields = ("title", "subject__name", "subject__code")

    def save_model(self, request, obj, form, change):
        # If file uploaded
        if obj.file:
            file_name = obj.file.name
            obj.title = os.path.splitext(file_name)[0]  # default title = filename
            obj.file_type = os.path.splitext(file_name)[1].replace(".", "").upper()

            # Calculate size in KB
            obj.file_size = round(obj.file.size / 1024, 2)

            # Upload to cloudinary
            upload_result = cloudinary.uploader.upload(obj.file, resource_type="auto")

            # Save cloudinary URL
            obj.cloudinary_url = upload_result.get("secure_url")

        super().save_model(request, obj, form, change)

# Register your models here.
