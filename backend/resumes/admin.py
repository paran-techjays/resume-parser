from django.contrib import admin

# Register your models here.
from .models import Resume

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'email', 'phone_number', 'job_title', 'experience_years', 'uploaded_at')
    search_fields = ('candidate_name', 'email', 'phone_number', 'job_title')
    list_filter = ('uploaded_at',)
    ordering = ('-uploaded_at',)
    list_per_page = 20
    list_max_show_all = 100
