from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Resume
from .serializers import ResumeSerializer
from .parser import extract_text
from .extractor import (
    extract_candidate_name, extract_email, extract_phone,
    extract_skills, extract_job_title, extract_companies,
    extract_experience, extract_education
)
from django.core.files.storage import default_storage
import tempfile
import os

# Create your views here.
class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     return Resume.objects.all()

    # def get_serializer_class(self):
    #     return ResumeSerializer

    @action(detail=False, methods=['POST'])
    def upload(self, request):
        try:
            # Get the uploaded file
            print(request.FILES)
            resume_file = request.FILES.get('resume')
            if not resume_file:
                return Response(
                    {'error': 'No file provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            print('resume_file', resume_file)

            # Get original file extension
            file_extension = os.path.splitext(resume_file.name)[1]
            
            # Create a temporary file with the correct extension
            with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as temp_file:
                for chunk in resume_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
                print('temp_file_path', temp_file_path)

            try:
                # Extract text from the resume
                resume_text = extract_text(temp_file_path)

                # Extract information from the text
                extracted_data = {
                    'candidate_name': extract_candidate_name(resume_text) or 'Unknown',
                    'email': extract_email(resume_text) or 'unknown@example.com',
                    'phone_number': extract_phone(resume_text) or 'N/A',
                    'key_skills': ', '.join(extract_skills(resume_text)) or 'Not specified',
                    'job_title': extract_job_title(resume_text) or 'Not specified',
                    'experience_years': extract_experience(resume_text) or 0,
                    'education': extract_education(resume_text) or 'Not specified',
                    'companies': ', '.join(extract_companies(resume_text)) or 'Not specified',
                    'resume_file': resume_file,
                    'resume_content': resume_text or ''
                }
                print('extracted_data', extracted_data)

                # Create and save the Resume instance
                serializer = self.get_serializer(data=extracted_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )

            finally:
                # Clean up the temporary file
                os.unlink(temp_file_path)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class ResumeSearchView(generics.ListAPIView):
    serializer_class = ResumeSerializer
    
    def get_queryset(self):
        queryset = Resume.objects.all()
        query_params = self.request.query_params
        print('query_params', query_params)

        key_skills = query_params.get('key_skills')
        job_title = query_params.get('job_title')
        experience_years = query_params.get('experience_years')
        companies = query_params.get('companies')
        
        filters = Q()
        if key_skills:
            filters |= Q(key_skills__icontains=key_skills)
        if job_title:
            filters |= Q(job_title__icontains=job_title)
        if experience_years:
            filters |= Q(experience_years__icontains=experience_years)
        if companies:
            filters |= Q(companies__icontains=companies)
            
        return queryset.filter(filters) if filters else queryset
