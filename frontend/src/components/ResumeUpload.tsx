import { useState } from 'react';
import { Formik, Form } from 'formik';
import { resumeApi } from '../services/api';

interface ResumeUploadProps {
  onUploadSuccess: () => void;
}

export const ResumeUpload = ({ onUploadSuccess }: ResumeUploadProps) => {
  const [files, setFiles] = useState<FileList | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState<{ total: number; processed: number } | null>(null);

  const handleUpload = async () => {
    if (!files || files.length === 0) return;
    setIsLoading(true);
    setError(null);
    setProgress({ total: files.length, processed: 0 });

    try {
      const uploadPromises = Array.from(files).map(async (file, index) => {
        try {
          await resumeApi.uploadResume(file);
          setProgress(prev => prev ? { ...prev, processed: prev.processed + 1 } : null);
        } catch (error) {
          console.error(`Error uploading ${file.name}:`, error);
          return file.name; // Return filename if upload failed
        }
      });

      const results = await Promise.all(uploadPromises);
      const failedUploads = results.filter(Boolean);

      if (failedUploads.length > 0) {
        setError(`Failed to upload: ${failedUploads.join(', ')}`);
      } else {
        alert('All resumes uploaded successfully!');
      }

      setFiles(null);
      onUploadSuccess();
    } catch (error) {
      setError('Error uploading resumes. Please try again.');
      console.error('Error uploading resumes:', error);
    } finally {
      setIsLoading(false);
      setProgress(null);
    }
  };

  return (
    <section className="upload-section">
      <h2>Upload Resumes</h2>
      {error && <div className="error-message">{error}</div>}
      {progress && (
        <div className="progress-bar">
          Processing: {progress.processed} / {progress.total} resumes
        </div>
      )}
      <Formik
        initialValues={{ files: null }}
        onSubmit={() => handleUpload()}
      >
        {({ setFieldValue }) => (
          <Form>
            <input
              type="file"
              accept=".pdf,.doc,.docx"
              multiple
              onChange={(e) => {
                setFiles(e.target.files);
                setFieldValue('files', e.target.files);
              }}
            />
            <button 
              type="submit" 
              disabled={!files || files.length === 0 || isLoading}
            >
              {isLoading ? 'Uploading...' : 'Upload'}
            </button>
          </Form>
        )}
      </Formik>
    </section>
  );
}; 