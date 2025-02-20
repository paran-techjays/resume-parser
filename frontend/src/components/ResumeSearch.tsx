import { Formik, Form, Field } from 'formik';
import { SearchFormValues } from '../types';

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
        <Form>
          <div className="search-filters">
            <Field
              type="text"
              name="key_skills"
              placeholder="Skills"
            />
            <Field
              type="text"
              name="job_title"
              placeholder="Job Title"
            />
            <Field
              type="text"
              name="companies"
              placeholder="Company"
            />
            <Field
              type="number"
              name="experience_years"
              placeholder="Years of Experience"
            />
          </div>
          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Searching...' : 'Search'}
          </button>
        </Form>
      </Formik>
    </section>
  );
}; 