import { useState, useEffect } from 'react';
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

  useEffect(() => {
    const fetchInitialResumes = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await resumeApi.searchResumes({});
        setResumes(data);
      } catch (error) {
        setError('Error loading resumes. Please try again.');
        console.error('Error loading resumes:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchInitialResumes();
  }, []);

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
    <div className="app">
      <header className="app-header">
        <h1>Resume Parser & Search</h1>
      </header>
      
      <main className="app-main">
        <div className="sidebar">
          <div className="card">
            <ResumeUpload onUploadSuccess={() => handleSearch({})} />
          </div>
          <div className="card">
            <ResumeSearch onSearch={handleSearch} isLoading={isLoading} />
          </div>
        </div>
        
        <div className="content">
          {error && (
            <div className="error-banner">
              <p>{error}</p>
              <button onClick={() => setError(null)}>✕</button>
            </div>
          )}
          <ResumeResults resumes={resumes} />
        </div>
      </main>
    </div>
  );
}

export default App;