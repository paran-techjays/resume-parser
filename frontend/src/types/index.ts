export interface Resume {
  id: number;
  name: string;
  job_title: string;
  companies: string;
  experience_years: number;
  key_skills: string;
  file_url: string;
}

export interface SearchFormValues {
  key_skills: string;
  job_title: string;
  experience_years: string;
  companies: string;
} 