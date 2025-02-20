from django.db import models

# Create your models here.
class Resume(models.Model):
    candidate_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    key_skills = models.TextField()  # Comma-separated skills
    job_title = models.CharField(max_length=255)
    experience_years = models.IntegerField()  # Years of experience
    education = models.TextField()
    companies = models.TextField()  # Comma-separated company names
    resume_file = models.FileField(upload_to='resumes/')
    resume_content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.candidate_name