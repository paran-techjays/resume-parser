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
from concurrent.futures import ThreadPoolExecutor
from django.conf import settings
from .extractor import parse_resume
from .config import create_config_file

# Add this at the start of your views.py
create_config_file()

# Create your views here.
class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     return Resume.objects.all()

    # def get_serializer_class(self):
    #     return ResumeSerializer

    def process_resume(self, resume_file):
        """Process a single resume file and return extracted data"""
        try:
            # Get original file extension
            file_extension = os.path.splitext(resume_file.name)[1]
            
            # Create a temporary file with the correct extension
            with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as temp_file:
                for chunk in resume_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

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
            return None, str(e)

    @action(detail=False, methods=['POST'])
    def upload(self, request):
        files = request.FILES.getlist('resume')
        if not files:
            return Response(
                {'error': 'No files provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = []
        max_workers = getattr(settings, 'MAX_RESUME_PROCESSING_WORKERS', 4)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Process resumes in parallel
            future_to_file = {
                executor.submit(self.process_resume, resume_file): resume_file
                for resume_file in files
            }

            for future in future_to_file:
                resume_file = future_to_file[future]
                try:
                    extracted_data, error = future.result()
                    if error:
                        results.append({
                            'filename': resume_file.name,
                            'status': 'error',
                            'error': error
                        })
                    else:
                        # Create and save the Resume instance
                        serializer = self.get_serializer(data=extracted_data)
                        if serializer.is_valid():
                            serializer.save()
                            results.append({
                                'filename': resume_file.name,
                                'status': 'success',
                                'data': serializer.data
                            })
                        else:
                            results.append({
                                'filename': resume_file.name,
                                'status': 'error',
                                'error': serializer.errors
                            })
                except Exception as e:
                    results.append({
                        'filename': resume_file.name,
                        'status': 'error',
                        'error': str(e)
                    })

        # Return summary of all operations
        success_count = sum(1 for r in results if r['status'] == 'success')
        return Response({
            'total': len(files),
            'successful': success_count,
            'failed': len(files) - success_count,
            'results': results
        }, status=status.HTTP_200_OK)

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
