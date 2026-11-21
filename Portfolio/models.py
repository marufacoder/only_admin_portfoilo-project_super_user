from django.conf import settings
from django.db import models
class Profile(models.Model):
 user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="portfolio_profile")
 name=models.CharField(max_length=120); designation=models.CharField(max_length=150,blank=True); bio=models.TextField(blank=True)
 email=models.EmailField(blank=True); phone=models.CharField(max_length=30,blank=True); photo=models.ImageField(upload_to="profile_photos/",blank=True,null=True); location=models.CharField(max_length=150,blank=True)
 def __str__(self): return self.name
class Skill(models.Model):
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="portfolio_skills")
 skill_name=models.CharField(max_length=100); proficiency_level=models.PositiveSmallIntegerField(default=70,help_text="1 to 100")
 class Meta: ordering=["skill_name"]; unique_together=("user","skill_name")
 def __str__(self): return self.skill_name
class Project(models.Model):
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="portfolio_projects")
 title=models.CharField(max_length=160); description=models.TextField(); technology_used=models.CharField(max_length=250)
 image=models.ImageField(upload_to="project_images/",blank=True,null=True); project_link=models.URLField(blank=True); is_published=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True)
 class Meta: ordering=["-created_at"]
 def __str__(self): return self.title
class PortfolioFile(models.Model):
 project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name="attachments")
 uploaded_file=models.FileField(upload_to="project_files/%Y/%m/"); display_name=models.CharField(max_length=180,blank=True); uploaded_at=models.DateTimeField(auto_now_add=True)
 def __str__(self): return self.display_name or self.uploaded_file.name
class Experience(models.Model):
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="portfolio_experiences")
 company_name=models.CharField(max_length=150); position=models.CharField(max_length=150); start_date=models.DateField(); end_date=models.DateField(blank=True,null=True); description=models.TextField(blank=True)
 class Meta: ordering=["-start_date"]
 def __str__(self): return f"{self.position} at {self.company_name}"
class Education(models.Model):
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="portfolio_education")
 institute_name=models.CharField(max_length=180); degree=models.CharField(max_length=150); passing_year=models.PositiveIntegerField(); result=models.CharField(max_length=80,blank=True)
 class Meta: ordering=["-passing_year"]
 def __str__(self): return f"{self.degree} - {self.institute_name}"
