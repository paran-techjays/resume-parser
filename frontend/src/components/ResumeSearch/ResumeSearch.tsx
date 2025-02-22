import { Formik, Form, Field } from 'formik';
import { SearchFormValues } from '../../types';
import './ResumeSearch.css';

interface ResumeSearchProps {
  onSearch: (values: SearchFormValues) => Promise<void>;
  isLoading: boolean;
}

export const ResumeSearch = ({ onSearch, isLoading }: ResumeSearchProps) => {
  return (
    <section className="search-section">
      <h2>Search Resumes</h2>
      <Formik
        initialValues={{
          key_skills: '',
          job_title: '',
          experience_years: '',
          companies: ''
        }}
        onSubmit={onSearch}
      >
        <Form className="search-form">
          <div className="search-filters">
            <div className="form-group">
              <label htmlFor="key_skills">Skills</label>
              <Field
                type="text"
                id="key_skills"
                name="key_skills"
                className="form-control"
                placeholder="e.g., Python, React, AWS"
              />
            </div>
            <div className="form-group">
              <label htmlFor="job_title">Job Title</label>
              <Field
                type="text"
                id="job_title"
                name="job_title"
                className="form-control"
                placeholder="e.g., Software Engineer"
              />
            </div>
            <div className="form-group">
              <label htmlFor="companies">Company</label>
              <Field
                type="text"
                id="companies"
                name="companies"
                className="form-control"
                placeholder="e.g., Google, Microsoft"
              />
            </div>
            <div className="form-group">
              <label htmlFor="experience_years">Years of Experience</label>
              <Field
                type="number"
                id="experience_years"
                name="experience_years"
                className="form-control"
                placeholder="e.g., 5"
                min="0"
                max="50"
              />
            </div>
          </div>
          <button type="submit" className="search-button" disabled={isLoading}>
            {isLoading ? 'Searching...' : 'Search'}
          </button>
        </Form>
      </Formik>
    </section>
  );
}; 