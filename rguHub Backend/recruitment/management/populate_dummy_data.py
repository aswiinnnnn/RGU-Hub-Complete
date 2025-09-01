from resources.models import Program

nursing = Program.objects.create(name="B.Sc Nursing", short_name="bsc-nursing", duration_years=4)
physio = Program.objects.create(name="B.Sc Physiotherapy", short_name="bsc-physio", duration_years=4)
