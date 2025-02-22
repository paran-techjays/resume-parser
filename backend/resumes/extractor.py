import spacy
import re
nlp = spacy.load("en_core_web_sm")

def extract_candidate_name(text):
    # Process the first few lines of text to find the name
    first_section = '\n'.join(text.split('\n')[:5])  # Look at first 5 lines
    doc = nlp(first_section)
    
    # Look for PERSON entities
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # Verify it's not part of an email address or common header
            if not any(keyword in ent.text.lower() for keyword in ['resume', 'cv', '@']):
                return ent.text.strip()
    
    # Fallback to the original method if no person entity is found
    lines = text.split('\n')
    for line in lines[:5]:
        if line.strip() and not any(keyword in line.lower() for keyword in ['resume', 'cv', 'email', 'phone', '@']):
            return line.strip()
    
    return None

def extract_email(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else None

def extract_phone(text):
    # Look for various phone number formats
    phone_patterns = [
        r'\+?\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # International format
        r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
        r'\+?\d{10,12}'  # Simple consecutive digits
    ]
    
    for pattern in phone_patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]
    return None

def extract_skills(text):
    # Common technical skills to look for
    common_skills = {
        'python', 'javascript', 'react', 'angular', 'vue', 'node', 'django', 'fastapi',
        'aws', 'docker', 'kubernetes', 'sql', 'nosql', 'mongodb', 'postgresql',
        'java', 'c++', 'ruby', 'php', 'html', 'css', 'git', 'redux', 'typescript',
        'rest api', 'graphql', 'machine learning', 'ai', 'cloud computing',
        'devops', 'ci/cd', 'agile', 'scrum'
    }
    
    # Find skills section
    skills_section = ""
    lines = text.lower().split('\n')
    for i, line in enumerate(lines):
        if 'skills' in line or 'technical skills' in line:
            skills_section = '\n'.join(lines[i:i+15])  # Take next 15 lines after skills heading
            break
    
    found_skills = set()
    for skill in common_skills:
        if skill in text.lower() or skill in skills_section:
            found_skills.add(skill)
    
    return list(found_skills)

def extract_job_title(text):
    common_titles = [
        'software engineer', 'senior software engineer', 'software developer',
        'full stack developer', 'frontend developer', 'backend developer',
        'data scientist', 'product manager', 'project manager',
        'solutions architect', 'technical lead', 'team lead'
    ]
    
    lines = text.lower().split('\n')
    for line in lines[:10]:  # Check first 10 lines
        for title in common_titles:
            if title in line.lower():
                return title.title()
    return None

def extract_companies(text):
    companies = []
    experience_keywords = ['experience', 'employment', 'work history']
    lines = text.lower().split('\n')
    
    # Find the experience section
    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in experience_keywords):
            # Look at the next 10 lines for company names
            potential_companies = lines[i+1:i+11]
            for company_line in potential_companies:
                # Skip empty lines and lines with common words
                if (company_line.strip() and 
                    not any(word in company_line.lower() for word in 
                        ['experience', 'responsibilities', 'skills', 'education'])):
                    companies.append(company_line.strip())
    
    return list(set(companies))[:3]  # Return up to 3 unique companies

def extract_experience(text):
    # Look for years of experience patterns
    experience_patterns = [
        r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
        r'experience\s*(?:of\s*)?(\d+)\+?\s*years?',
        r'worked\s+(?:for\s+)?(\d+)\+?\s*years?'
    ]
    
    for pattern in experience_patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            try:
                years = int(matches[0])
                return min(years, 50)  # Cap at 50 years
            except ValueError:
                continue
    
    # If no explicit mention, try to calculate from work history
    try:
        # Look for year patterns (e.g., 2018-2023, 2018 - present)
        year_pattern = r'20\d{2}(?:\s*-\s*(?:20\d{2}|present))?'
        years = re.findall(year_pattern, text)
        if years:
            return min(len(years), 50)
    except:
        pass
    
    return 0

def extract_education(text):
    education_keywords = ['education', 'university', 'college', 'institute', 'b.tech', 'b.e', 'b.s', 'm.s', 'ph.d']
    lines = text.lower().split('\n')
    
    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in education_keywords):
            # Return next non-empty line
            for edu_line in lines[i:i+3]:
                if edu_line.strip() and not any(keyword in edu_line.lower() for keyword in ['education']):
                    return edu_line.strip()
    return None

