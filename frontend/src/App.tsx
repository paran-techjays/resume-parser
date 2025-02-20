import { useState } from 'react';
import { ResumeUpload } from './components/ResumeUpload';
import { ResumeSearch } from './components/ResumeSearch';
import { ResumeResults } from './components/ResumeResults';
import { resumeApi } from './services/api';
import { Resume, SearchFormValues } from './types';
import './App.css';

function App() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (values: SearchFormValues) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await resumeApi.searchResumes(values);
      setResumes(data);
    } catch (error) {
      setError('Error searching resumes. Please try again.');
      console.error('Error searching resumes:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      {error && <div className="error-message">{error}</div>}
      <ResumeUpload onUploadSuccess={() => handleSearch({})} />
      <ResumeSearch onSearch={handleSearch} isLoading={isLoading} />
      <ResumeResults resumes={resumes} />
    </div>
  );
}

export default App;