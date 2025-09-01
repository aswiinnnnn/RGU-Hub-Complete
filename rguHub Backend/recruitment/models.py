from django.db import models
from resources.models import Program

# Create your models here.
class Recruitment(models.Model):
    JOB_TYPES = [('FT','Full-Time'),
                 ('PT','Part-Time'),
                 ('IN','Internship')]
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="recruitments")
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=2, choices=JOB_TYPES,default= 'FT')
    description = models.TextField()
    requirements = models.TextField()
    salary = models.CharField(max_length=100, blank=True, null=True)
    deadline = models.DateField()
    apply_link = models.URLField(max_length=500)   
    posted_on = models.DateTimeField(auto_now_add=True)


    
    def __str__(self):
        return f"{self.position} at {self.company_name}"