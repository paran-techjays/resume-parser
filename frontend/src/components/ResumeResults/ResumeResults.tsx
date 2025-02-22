import { Resume } from '../../types';
import './ResumeResults.css';

interface ResumeResultsProps {
  resumes: Resume[];
}

export const ResumeResults = ({ resumes }: ResumeResultsProps) => {
  if (resumes.length === 0) {
    return (
      <div className="no-results">
        <p>No resumes found. Try uploading a resume or adjusting your search criteria.</p>
      </div>
    );
  }

  return (
    <div className="results-container">
      <h2>Search Results ({resumes.length})</h2>
      <div className="results-grid">
        {resumes.map((resume) => (
          <div key={resume.id} className="resume-card">
            <div className="resume-header">
              <h3>{resume.candidate_name}</h3>
              <span className="experience">{resume.experience_years} years</span>
            </div>
            <div className="resume-body">
              <div className="info-row">
                <span className="label">Email:</span>
                <span className="value">{resume.email}</span>
              </div>
              <div className="info-row">
                <span className="label">Phone:</span>
                <span className="value">{resume.phone_number}</span>
              </div>
              <div className="info-row">
                <span className="label">Job Title:</span>
                <span className="value">{resume.job_title}</span>
              </div>
              <div className="info-row">
                <span className="label">Companies:</span>
                <span className="value">{resume.companies}</span>
              </div>
              <div className="skills">
                <span className="label">Skills:</span>
                <div className="skills-list">
                  {resume.key_skills.split(',').map((skill, index) => (
                    <span key={index} className="skill-tag">
                      {skill.trim()}
                    </span>
                  ))}
                </div>
              </div>
            </div>
            <div className="resume-footer">
              <a 
                href={resume.resume_file} 
                className="download-button"
                target="_blank"
                rel="noopener noreferrer"
              >
                Download Resume
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}; 