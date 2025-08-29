from django.db import models
from django.utils.text import slugify


class Program(models.Model):
    """Represents a program/course (e.g., B.Sc Nursing, BPT)."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=50, unique=True)
    duration_years = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}"


class Syllabus(models.Model):
    """Represents a syllabus/regulation version for a Program (e.g., CBCS 2022)."""
    id = models.AutoField(primary_key=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="syllabi")
    name = models.CharField(max_length=255)
    effective_from = models.DateField(null=True, blank=True)
    effective_to = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["program__short_name", "name"]
        unique_together = ("program", "name")

    def __str__(self) -> str:
        return f"{self.program.name} - {self.name}"


class Term(models.Model):
    """Flexible term which can be a Semester or a Year under a Syllabus."""

    class TermType(models.TextChoices):
        SEMESTER = "SEMESTER", "Semester"
        YEAR = "YEAR", "Year"

    id = models.AutoField(primary_key=True)    
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE, related_name="terms")
    term_number = models.PositiveSmallIntegerField(help_text="1 for first term, 2 for second, etc.")
    term_type = models.CharField(max_length=16, choices=TermType.choices)
    name = models.CharField(max_length=100, blank=True, help_text="Optional display name")
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        ordering = ["syllabus__program__short_name", "syllabus__name", "term_number"]
        unique_together = ("syllabus", "term_number")

    def __str__(self) -> str:
        label = self.name or f"{self.get_term_type_display()} {self.term_number}"
        return f"{self.syllabus} - {label}"


class Subject(models.Model):
    """Represents a subject under a Term."""

    class SubjectType(models.TextChoices):
        THEORY = "THEORY", "Theory"
        PRACTICAL = "PRACTICAL", "Practical"
        CLINICAL = "CLINICAL", "Clinical"
    id = models.AutoField(primary_key=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="subjects")
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    subject_type = models.CharField(max_length=16, choices=SubjectType.choices)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        ordering = [
            "term__syllabus__program__short_name",
            "term__syllabus__name",
            "term__term_number",
            "code",
        ]
        unique_together = ("term", "code")

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        """
        Auto-generate a unique slug for the subject if not provided.

        The slug is built from the program short name, term number and subject code,
        falling back to code and name if needed. If a slug collision occurs,
        a numeric suffix is appended.
        """
        if not self.slug:
            # Try to build a meaningful base using related Term/Syllabus/Program
            base_parts = []
            try:
                if self.term and self.term.syllabus and self.term.syllabus.program:
                    prog = self.term.syllabus.program.short_name
                    base_parts.append(str(prog))
                if self.term and getattr(self.term, 'term_number', None) is not None:
                    base_parts.append(str(self.term.term_number))
            except Exception:
                # If relations are not available for some reason, ignore and continue
                pass

            # Prefer using code (short, likely unique per term) then name
            if self.code:
                base_parts.append(self.code)
            elif self.name:
                base_parts.append(self.name)

            base = slugify("-".join(base_parts)) or slugify(self.code or self.name) or "subject"

            slug_candidate = base
            counter = 1
            Model = self.__class__
            while Model.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                counter += 1
                slug_candidate = f"{base}-{counter}"

            self.slug = slug_candidate

        super().save(*args, **kwargs)


class SubjectMaterial(models.Model):

    """Stores URLs for study materials related to a Subject."""
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="materials")
    title = models.CharField(max_length=255)
    url = models.URLField(help_text="Direct URL to the study material")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.subject.code} - {self.title}"
