import os
import PyPDF2
import docx
import mimetypes

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        raise Exception(f"Error reading PDF file: {str(e)}")
    return text

def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        raise Exception(f"Error reading DOCX file: {str(e)}")

def extract_text(file_path):
    # Get the mime type of the file
    mime_type, _ = mimetypes.guess_type(file_path)
    
    if mime_type == 'application/pdf':
        return extract_text_from_pdf(file_path)
    elif mime_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']:
        return extract_text_from_docx(file_path)
    else:
        # Fallback to checking file extension
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return extract_text_from_pdf(file_path)
        elif ext == ".docx" or ext == ".doc":
            return extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Please upload PDF or DOCX files only.")

# Example usage:
# resume_text = extract_text("sample_resume.pdf")
# print(resume_text)  # Check extracted text
