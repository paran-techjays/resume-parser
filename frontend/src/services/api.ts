import axios from 'axios';
import { Resume, SearchFormValues } from '../types';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
});

export const resumeApi = {
  searchResumes: async (params: SearchFormValues): Promise<Resume[]> => {
    const response = await api.get('/resumes/search/', { params });
    return response.data;
  },

  uploadResume: async (file: File): Promise<void> => {
    const formData = new FormData();
    formData.append('resume', file);
    
    await api.post('/resumes/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
}; 