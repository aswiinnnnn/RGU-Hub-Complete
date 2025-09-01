from django.core.management.base import BaseCommand
from django.utils.text import slugify
from resources.models import Program, Syllabus, Term, Subject, SubjectMaterial, MaterialType
from datetime import date


class Command(BaseCommand):
    help = 'Populate database with dummy data for B.Sc Nursing and BPT programs'

    def handle(self, *args, **options):
        self.stdout.write('Creating dummy data...')
        
        # Create Material Types
        material_types_data = [
            {'name': 'Notes', 'slug': 'notes', 'description': 'Subject-wise organized handouts and study materials', 'icon': 'BookOpen', 'color': 'primary'},
            {'name': 'Previous Year Questions', 'slug': 'pyq', 'description': 'University question papers from past examinations', 'icon': 'FileText', 'color': 'accent'},
            {'name': 'Question Bank', 'slug': 'question-bank', 'description': 'Unit-wise and chapter-wise practice questions', 'icon': 'HelpCircle', 'color': 'success'},
            {'name': 'Syllabus', 'slug': 'syllabus', 'description': 'RGU/INC curriculum and course structure', 'icon': 'ClipboardList', 'color': 'secondary'},
            {'name': 'Practical Resources', 'slug': 'practical', 'description': 'Clinical logbook, skill checklists, lab guides', 'icon': 'Stethoscope', 'color': 'destructive'},
        ]
        
        material_types = {}
        for type_data in material_types_data:
            material_type, created = MaterialType.objects.get_or_create(
                slug=type_data['slug'],
                defaults=type_data
            )
            if created:
                self.stdout.write(f'Created material type: {material_type.name}')
            material_types[type_data['slug']] = material_type
        
        # Create Programs
        nursing_program, created = Program.objects.get_or_create(
            short_name='BN',
            defaults={
                'name': 'B.Sc Nursing',
                'duration_years': 4
            }
        )
        if created:
            self.stdout.write(f'Created program: {nursing_program.name}')
        
        bpt_program, created = Program.objects.get_or_create(
            short_name='BPT',
            defaults={
                'name': 'Bachelor of Physiotherapy',
                'duration_years': 4
            }
        )
        if created:
            self.stdout.write(f'Created program: {bpt_program.name}')
        
        # Create Syllabi
        nursing_syllabus, created = Syllabus.objects.get_or_create(
            program=nursing_program,
            name='CBCS 2022',
            defaults={
                'effective_from': date(2022, 6, 1),
                'effective_to': date(2026, 5, 31)
            }
        )
        if created:
            self.stdout.write(f'Created syllabus: {nursing_syllabus.name}')
        
        bpt_syllabus, created = Syllabus.objects.get_or_create(
            program=bpt_program,
            name='CBCS 2022',
            defaults={
                'effective_from': date(2022, 6, 1),
                'effective_to': date(2026, 5, 31)
            }
        )
        if created:
            self.stdout.write(f'Created syllabus: {bpt_syllabus.name}')
        
        # Create Terms (Semesters) for Nursing
        nursing_terms = []
        for i in range(1, 9):  # 8 semesters
            term, created = Term.objects.get_or_create(
                syllabus=nursing_syllabus,
                term_number=i,
                defaults={
                    'term_type': 'SEMESTER',
                    'name': f'Semester {i}',
                    'slug': f'bn-semester-{i}'
                }
            )
            if created:
                self.stdout.write(f'Created nursing term: {term.name}')
            nursing_terms.append(term)
        
        # Create Terms (Semesters) for BPT
        bpt_terms = []
        for i in range(1, 9):  # 8 semesters
            term, created = Term.objects.get_or_create(
                syllabus=bpt_syllabus,
                term_number=i,
                defaults={
                    'term_type': 'SEMESTER',
                    'name': f'Semester {i}',
                    'slug': f'bpt-semester-{i}'
                }
            )
            if created:
                self.stdout.write(f'Created BPT term: {term.name}')
            bpt_terms.append(term)
        
        # Create Subjects for Nursing (completely separate from BPT)
        nursing_subjects_data = [
            # Semester 1
            {'code': 'NSG101', 'name': 'Anatomy', 'subject_type': 'THEORY'},
            {'code': 'NSG102', 'name': 'Physiology', 'subject_type': 'THEORY'},
            {'code': 'NSG103', 'name': 'Biochemistry', 'subject_type': 'THEORY'},
            {'code': 'NSG104', 'name': 'Nutrition and Dietetics', 'subject_type': 'THEORY'},
            {'code': 'NSG105', 'name': 'Psychology', 'subject_type': 'THEORY'},
            
            # Semester 2
            {'code': 'NSG201', 'name': 'Sociology', 'subject_type': 'THEORY'},
            {'code': 'NSG202', 'name': 'Microbiology', 'subject_type': 'THEORY'},
            {'code': 'NSG203', 'name': 'Pathology', 'subject_type': 'THEORY'},
            {'code': 'NSG204', 'name': 'Genetics', 'subject_type': 'THEORY'},
            {'code': 'NSG205', 'name': 'English', 'subject_type': 'THEORY'},
            
            # Semester 3
            {'code': 'NSG301', 'name': 'Pharmacology', 'subject_type': 'THEORY'},
            {'code': 'NSG302', 'name': 'Nursing Foundation', 'subject_type': 'THEORY'},
            {'code': 'NSG303', 'name': 'Community Health Nursing I', 'subject_type': 'THEORY'},
            {'code': 'NSG304', 'name': 'Environmental Science', 'subject_type': 'THEORY'},
            {'code': 'NSG305', 'name': 'Nursing Informatics', 'subject_type': 'THEORY'},
            
            # Semester 4
            {'code': 'NSG401', 'name': 'Medical Surgical Nursing I', 'subject_type': 'THEORY'},
            {'code': 'NSG402', 'name': 'Mental Health Nursing', 'subject_type': 'THEORY'},
            {'code': 'NSG403', 'name': 'Child Health Nursing', 'subject_type': 'THEORY'},
            {'code': 'NSG404', 'name': 'Nursing Research', 'subject_type': 'THEORY'},
            {'code': 'NSG405', 'name': 'Clinical Practice I', 'subject_type': 'CLINICAL'},
            
            # Semester 5
            {'code': 'NSG501', 'name': 'Medical Surgical Nursing II', 'subject_type': 'THEORY'},
            {'code': 'NSG502', 'name': 'Obstetrics and Gynecological Nursing', 'subject_type': 'THEORY'},
            {'code': 'NSG503', 'name': 'Community Health Nursing II', 'subject_type': 'THEORY'},
            {'code': 'NSG504', 'name': 'Clinical Practice II', 'subject_type': 'CLINICAL'},
            
            # Semester 6
            {'code': 'NSG601', 'name': 'Critical Care Nursing', 'subject_type': 'THEORY'},
            {'code': 'NSG602', 'name': 'Nursing Education', 'subject_type': 'THEORY'},
            {'code': 'NSG603', 'name': 'Nursing Administration', 'subject_type': 'THEORY'},
            {'code': 'NSG604', 'name': 'Clinical Practice III', 'subject_type': 'CLINICAL'},
            
            # Semester 7
            {'code': 'NSG701', 'name': 'Emergency and Disaster Nursing', 'subject_type': 'THEORY'},
            {'code': 'NSG702', 'name': 'Geriatric Nursing', 'subject_type': 'THEORY'},
            {'code': 'NSG703', 'name': 'Professional Development', 'subject_type': 'THEORY'},
            {'code': 'NSG704', 'name': 'Internship I', 'subject_type': 'CLINICAL'},
            
            # Semester 8
            {'code': 'NSG801', 'name': 'Nursing Leadership', 'subject_type': 'THEORY'},
            {'code': 'NSG802', 'name': 'Evidence Based Practice', 'subject_type': 'THEORY'},
            {'code': 'NSG803', 'name': 'Project Work', 'subject_type': 'THEORY'},
            {'code': 'NSG804', 'name': 'Internship II', 'subject_type': 'CLINICAL'},
        ]
        
        # Create Subjects for BPT (completely separate from Nursing)
        bpt_subjects_data = [
            # Semester 1
            {'code': 'BPT101', 'name': 'Human Anatomy', 'subject_type': 'THEORY'},
            {'code': 'BPT102', 'name': 'Human Physiology', 'subject_type': 'THEORY'},
            {'code': 'BPT103', 'name': 'Biochemistry', 'subject_type': 'THEORY'},
            {'code': 'BPT104', 'name': 'Biomechanics', 'subject_type': 'THEORY'},
            {'code': 'BPT105', 'name': 'Psychology', 'subject_type': 'THEORY'},
            
            # Semester 2
            {'code': 'BPT201', 'name': 'Pathology', 'subject_type': 'THEORY'},
            {'code': 'BPT202', 'name': 'Microbiology', 'subject_type': 'THEORY'},
            {'code': 'BPT203', 'name': 'Pharmacology', 'subject_type': 'THEORY'},
            {'code': 'BPT204', 'name': 'Exercise Physiology', 'subject_type': 'THEORY'},
            {'code': 'BPT205', 'name': 'English', 'subject_type': 'THEORY'},
            
            # Semester 3
            {'code': 'BPT301', 'name': 'Orthopedics', 'subject_type': 'THEORY'},
            {'code': 'BPT302', 'name': 'Neurology', 'subject_type': 'THEORY'},
            {'code': 'BPT303', 'name': 'Cardiopulmonary', 'subject_type': 'THEORY'},
            {'code': 'BPT304', 'name': 'Sports Physiotherapy', 'subject_type': 'THEORY'},
            {'code': 'BPT305', 'name': 'Clinical Practice I', 'subject_type': 'CLINICAL'},
            
            # Semester 4
            {'code': 'BPT401', 'name': 'Pediatric Physiotherapy', 'subject_type': 'THEORY'},
            {'code': 'BPT402', 'name': 'Geriatric Physiotherapy', 'subject_type': 'THEORY'},
            {'code': 'BPT403', 'name': 'Women Health', 'subject_type': 'THEORY'},
            {'code': 'BPT404', 'name': 'Clinical Practice II', 'subject_type': 'CLINICAL'},
            
            # Semester 5
            {'code': 'BPT501', 'name': 'Community Physiotherapy', 'subject_type': 'THEORY'},
            {'code': 'BPT502', 'name': 'Research Methodology', 'subject_type': 'THEORY'},
            {'code': 'BPT503', 'name': 'Clinical Practice III', 'subject_type': 'CLINICAL'},
            
            # Semester 6
            {'code': 'BPT601', 'name': 'Advanced Physiotherapy', 'subject_type': 'THEORY'},
            {'code': 'BPT602', 'name': 'Clinical Practice IV', 'subject_type': 'CLINICAL'},
            
            # Semester 7
            {'code': 'BPT701', 'name': 'Internship I', 'subject_type': 'CLINICAL'},
            
            # Semester 8
            {'code': 'BPT801', 'name': 'Internship II', 'subject_type': 'CLINICAL'},
        ]
        
        # Create Nursing Subjects
        nursing_subjects = []
        for i, subject_data in enumerate(nursing_subjects_data):
            term_index = i // 5  # 5 subjects per semester (roughly)
            if term_index >= len(nursing_terms):
                term_index = len(nursing_terms) - 1
                
            subject, created = Subject.objects.get_or_create(
                term=nursing_terms[term_index],
                code=subject_data['code'],
                defaults={
                    'name': subject_data['name'],
                    'subject_type': subject_data['subject_type'],
                    'slug': f'bn-{subject_data["code"].lower()}'
                }
            )
            if created:
                self.stdout.write(f'Created nursing subject: {subject.name}')
            nursing_subjects.append(subject)
        
        # Create BPT Subjects
        bpt_subjects = []
        for i, subject_data in enumerate(bpt_subjects_data):
            term_index = i // 5  # 5 subjects per semester (roughly)
            if term_index >= len(bpt_terms):
                term_index = len(bpt_terms) - 1
                
            subject, created = Subject.objects.get_or_create(
                term=bpt_terms[term_index],
                code=subject_data['code'],
                defaults={
                    'name': subject_data['name'],
                    'subject_type': subject_data['subject_type'],
                    'slug': f'bpt-{subject_data["code"].lower()}'
                }
            )
            if created:
                self.stdout.write(f'Created BPT subject: {subject.name}')
            bpt_subjects.append(subject)
        
        # Create Sample Materials for Nursing Subjects with proper types
        nursing_materials = [
            {'title': 'Anatomy Notes - Unit 1', 'description': 'Introduction to Human Anatomy and Physiology', 'url': 'https://example.com/anatomy-notes-1.pdf', 'type': 'notes'},
            {'title': 'Physiology Lab Manual', 'description': 'Practical exercises for Physiology lab sessions', 'url': 'https://example.com/physiology-lab.pdf', 'type': 'practical'},
            {'title': 'Biochemistry Question Bank', 'description': 'Unit-wise practice questions for Biochemistry', 'url': 'https://example.com/biochem-questions.pdf', 'type': 'question-bank'},
            {'title': 'Nutrition PYQ July 2024', 'description': 'Previous year question paper for Nutrition', 'url': 'https://example.com/nutrition-pyq-july-2024.pdf', 'type': 'pyq', 'year': 2024, 'month': 'July'},
            {'title': 'Psychology Syllabus', 'description': 'Complete syllabus for Psychology subject', 'url': 'https://example.com/psychology-syllabus.pdf', 'type': 'syllabus'},
            {'title': 'Microbiology Practical Guide', 'description': 'Step-by-step practical procedures', 'url': 'https://example.com/micro-practical.pdf', 'type': 'practical'},
            {'title': 'Pathology Notes', 'description': 'Comprehensive notes for Pathology', 'url': 'https://example.com/pathology-notes.pdf', 'type': 'notes'},
            {'title': 'Pharmacology Question Bank', 'description': 'MCQs and descriptive questions', 'url': 'https://example.com/pharma-questions.pdf', 'type': 'question-bank'},
            {'title': 'Nursing Foundation PYQ December 2023', 'description': 'Previous year question paper for Nursing Foundation', 'url': 'https://example.com/nursing-foundation-pyq-dec-2023.pdf', 'type': 'pyq', 'year': 2023, 'month': 'December'},
        ]
        
        # Create Sample Materials for BPT Subjects with proper types
        bpt_materials = [
            {'title': 'Human Anatomy Atlas', 'description': 'Detailed anatomical diagrams and descriptions', 'url': 'https://example.com/bpt-anatomy-atlas.pdf', 'type': 'notes'},
            {'title': 'Biomechanics Lab Manual', 'description': 'Practical exercises for biomechanics', 'url': 'https://example.com/bpt-biomechanics-lab.pdf', 'type': 'practical'},
            {'title': 'Exercise Physiology Notes', 'description': 'Complete notes for exercise physiology', 'url': 'https://example.com/bpt-exercise-physio.pdf', 'type': 'notes'},
            {'title': 'Orthopedics PYQ June 2024', 'description': 'Previous year questions for orthopedics', 'url': 'https://example.com/bpt-ortho-pyq-june-2024.pdf', 'type': 'pyq', 'year': 2024, 'month': 'June'},
            {'title': 'Neurology Case Studies', 'description': 'Clinical case studies for neurology', 'url': 'https://example.com/bpt-neuro-cases.pdf', 'type': 'notes'},
            {'title': 'Sports Physio Guide', 'description': 'Sports injury assessment and treatment', 'url': 'https://example.com/bpt-sports-guide.pdf', 'type': 'practical'},
            {'title': 'Pathology PYQ March 2024', 'description': 'Previous year questions for pathology', 'url': 'https://example.com/bpt-pathology-pyq-march-2024.pdf', 'type': 'pyq', 'year': 2024, 'month': 'March'},
        ]
        
        # Assign materials to nursing subjects
        for i, material_data in enumerate(nursing_materials):
            subject_index = i % len(nursing_subjects)
            material, created = SubjectMaterial.objects.get_or_create(
                subject=nursing_subjects[subject_index],
                title=material_data['title'],
                material_type=material_types[material_data['type']],
                defaults={
                    'description': material_data['description'],
                    'url': material_data['url'],
                    'year': material_data.get('year'),
                    'month': material_data.get('month'),
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created nursing material: {material.title}')
        
        # Assign materials to BPT subjects
        for i, material_data in enumerate(bpt_materials):
            subject_index = i % len(bpt_subjects)
            material, created = SubjectMaterial.objects.get_or_create(
                subject=bpt_subjects[subject_index],
                title=material_data['title'],
                material_type=material_types[material_data['type']],
                defaults={
                    'description': material_data['description'],
                    'url': material_data['url'],
                    'year': material_data.get('year'),
                    'month': material_data.get('month'),
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created BPT material: {material.title}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created dummy data:\n'
                f'- Programs: {Program.objects.count()}\n'
                f'- Syllabi: {Syllabus.objects.count()}\n'
                f'- Terms: {Term.objects.count()}\n'
                f'- Subjects: {Subject.objects.count()}\n'
                f'- Material Types: {MaterialType.objects.count()}\n'
                f'- Materials: {SubjectMaterial.objects.count()}'
            )
        )
