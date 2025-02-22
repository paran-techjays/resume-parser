from pyresparser import ResumeParser
import spacy
import re

nlp = spacy.load("en_core_web_lg")  # Upgrade to larger model

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
   # Step 1: Extract organizations using NER
    doc = nlp(text)
    companies = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    print("companies", companies)
    # Step 2: Custom regex pattern to catch missed company names
    custom_pattern = r'\b[A-Z][a-zA-Z&,\s]+(?:Inc\.|LLC|Limited|Ltd\.|Corporation|Corp\.)\b'
    custom_matches = re.findall(custom_pattern, text)

    # Step 3: Combine and remove duplicates
    all_companies = list(set(companies + custom_matches))

    # Step 4: Optional filtering (remove universities or non-companies)
    exclude_keywords = ["Institute", "University", "College"]
    final_companies = [name for name in all_companies if not any(keyword in name for keyword in exclude_keywords)]

    return final_companies

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

def parse_resume(text, file_path=None):
    """
    Main function to parse resume using pyresparser and fall back to custom extraction
    if needed
    """
    parsed_data = {}
    
    if file_path:
        # PyResParser works better with actual files
        try:
            parser_data = ResumeParser(file_path).get_extracted_data()
            print("parser_data2", parser_data)
            parsed_data = {
                'name': parser_data.get('name'),
                'email': parser_data.get('email'),
                'phone': parser_data.get('mobile_number'),
                'skills': parser_data.get('skills'),
                'education': parser_data.get('degree'),
                'experience': parser_data.get('total_experience'),
                'companies': parser_data.get('company_names'),
                'job_title': parser_data.get('designation')
            }
        except Exception as e:
            print(f"Error parsing resume: {e}")
            return parsed_data
    

    # Fall back to custom extraction for missing fields
    if not parsed_data.get('name'):
        parsed_data['name'] = extract_candidate_name(text)
    if not parsed_data.get('email'):
        parsed_data['email'] = extract_email(text)
    if not parsed_data.get('phone'):
        parsed_data['phone'] = extract_phone(text)
    if not parsed_data.get('skills'):
        parsed_data['skills'] = extract_skills(text)
    if not parsed_data.get('job_title'):
        parsed_data['job_title'] = extract_job_title(text)
    if not parsed_data.get('companies'):
        parsed_data['companies'] = extract_companies(text)
    if not parsed_data.get('experience'):
        parsed_data['experience'] = extract_experience(text)
    
    return parsed_data

