from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResumeViewSet, ResumeSearchView

router = DefaultRouter()
router.register(r'resumes', ResumeViewSet, basename='resume')

urlpatterns = [
    path('resumes/search/', ResumeSearchView.as_view(), name='resume-search'),
    path('', include(router.urls)),
    path('resumes/upload/', ResumeViewSet.as_view({'post': 'upload'}), name='resume-upload'),
]
