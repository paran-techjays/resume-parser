export interface Resume {
  id: number;
  candidate_name: string;
  email: string;
  phone_number: string;
  key_skills: string;
  job_title: string;
  experience_years: number;
  education: string;
  companies: string;
  resume_file: string;
  resume_content: string;
  uploaded_at: string;
}

export interface SearchFormValues {
  key_skills?: string;
  job_title?: string;
  experience_years?: string;
  companies?: string;
} 