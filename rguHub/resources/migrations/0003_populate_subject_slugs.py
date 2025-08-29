"""Populate subject slugs for existing Subject records.

This data migration iterates over all Subject rows and calls save() to trigger
the model's slug generation logic added in models.py.
"""
from django.db import migrations


def populate_slugs(apps, schema_editor):
    Subject = apps.get_model('resources', 'Subject')
    for subj in Subject.objects.all():
        # If slug already present, skip
        if not subj.slug:
            subj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_term_slug'),
    ]

    operations = [
        migrations.RunPython(populate_slugs, reverse_code=migrations.RunPython.noop),
    ]
