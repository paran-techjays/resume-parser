import { Resume } from '../types';

interface ResumeResultsProps {
  resumes: Resume[];
}

export const ResumeResults = ({ resumes }: ResumeResultsProps) => {
  return (
    <section className="results-section">
      <h2>Search Results</h2>
      <div className="results-grid">
        {resumes.map((resume) => (
          <div key={resume.id} className="resume-card">
            <h3>{resume.candidate_name}</h3>
            <p><strong>Email:</strong> {resume.email}</p>
            <p><strong>Phone:</strong> {resume.phone_number}</p>
            <p><strong>Job Title:</strong> {resume.job_title}</p>
            <p><strong>Companies:</strong> {resume.companies}</p>
            <p><strong>Experience:</strong> {resume.experience_years} years</p>
            <p><strong>Skills:</strong> {resume.key_skills}</p>
            <p><strong>Education:</strong> {resume.education}</p>
            <a href={resume.resume_file} className="download-button">
              Download Resume
            </a>
          </div>
        ))}
      </div>
    </section>
  );
}; 