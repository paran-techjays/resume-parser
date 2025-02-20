import { useState } from 'react';
import { Formik, Form } from 'formik';
import { resumeApi } from '../services/api';

interface ResumeUploadProps {
  onUploadSuccess: () => void;
}

export const ResumeUpload = ({ onUploadSuccess }: ResumeUploadProps) => {
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async () => {
    if (!file) return;
    setIsLoading(true);
    setError(null);

    try {
      await resumeApi.uploadResume(file);
      alert('Resume uploaded successfully!');
      setFile(null);
      onUploadSuccess();
    } catch (error) {
      setError('Error uploading resume. Please try again.');
      console.error('Error uploading resume:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="upload-section">
      <h2>Upload Resume</h2>
      {error && <div className="error-message">{error}</div>}
      <Formik
        initialValues={{ file: null }}
        onSubmit={() => handleUpload()}
      >
        {({ setFieldValue }) => (
          <Form>
            <input
              type="file"
              accept=".pdf,.doc,.docx"
              onChange={(e) => {
                setFile(e.target.files?.[0] || null);
                setFieldValue('file', e.target.files?.[0] || null);
              }}
            />
            <button type="submit" disabled={!file || isLoading}>
              {isLoading ? 'Uploading...' : 'Upload'}
            </button>
          </Form>
        )}
      </Formik>
    </section>
  );
}; 