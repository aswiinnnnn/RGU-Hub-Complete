from django.core.management.base import BaseCommand
from resources.models import SubjectMaterial, MaterialType


class Command(BaseCommand):
    help = 'Update existing materials with proper material types based on their titles'

    def handle(self, *args, **options):
        self.stdout.write('Updating material types for existing materials...')
        
        # Get all material types
        material_types = {}
        for mt in MaterialType.objects.all():
            material_types[mt.slug] = mt
        
        self.stdout.write(f'Found {len(material_types)} material types: {list(material_types.keys())}')
        
        # Get all materials without material types
        materials_without_types = SubjectMaterial.objects.filter(material_type__isnull=True)
        self.stdout.write(f'Found {materials_without_types.count()} materials without types')
        
        updated_count = 0
        
        for material in materials_without_types:
            # Determine material type based on title and description
            title_lower = material.title.lower()
            description_lower = material.description.lower() if material.description else ""
            
            # Check for PYQ indicators
            if any(keyword in title_lower for keyword in ['pyq', 'question paper', 'exam', 'previous year']):
                material.material_type = material_types.get('pyq')
                if material.material_type:
                    # Try to extract year and month from title
                    import re
                    year_match = re.search(r'(\d{4})', title_lower)
                    if year_match:
                        material.year = int(year_match.group(1))
                    
                    month_match = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december)', title_lower)
                    if month_match:
                        material.month = month_match.group(1).title()
                    
                    self.stdout.write(f'Updated {material.title} -> PYQ')
                    updated_count += 1
                    continue
            
            # Check for Notes
            if any(keyword in title_lower for keyword in ['notes', 'unit', 'chapter', 'handout']):
                material.material_type = material_types.get('notes')
                if material.material_type:
                    self.stdout.write(f'Updated {material.title} -> Notes')
                    updated_count += 1
                    continue
            
            # Check for Question Bank
            if any(keyword in title_lower for keyword in ['question bank', 'mcq', 'practice questions']):
                material.material_type = material_types.get('question-bank')
                if material.material_type:
                    self.stdout.write(f'Updated {material.title} -> Question Bank')
                    updated_count += 1
                    continue
            
            # Check for Syllabus
            if any(keyword in title_lower for keyword in ['syllabus', 'curriculum']):
                material.material_type = material_types.get('syllabus')
                if material.material_type:
                    self.stdout.write(f'Updated {material.title} -> Syllabus')
                    updated_count += 1
                    continue
            
            # Check for Practical
            if any(keyword in title_lower for keyword in ['practical', 'lab', 'clinical', 'manual', 'guide']):
                material.material_type = material_types.get('practical')
                if material.material_type:
                    self.stdout.write(f'Updated {material.title} -> Practical')
                    updated_count += 1
                    continue
            
            # Default to Notes if no match found
            material.material_type = material_types.get('notes')
            if material.material_type:
                self.stdout.write(f'Updated {material.title} -> Notes (default)')
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated_count} materials with material types!'
            )
        )


