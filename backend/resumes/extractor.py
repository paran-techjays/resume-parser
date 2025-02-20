import spacy
import re
nlp = spacy.load("en_core_web_sm")

def extract_candidate_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":  # Looking for a person name
            return ent.text
    return None

def extract_email(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else None

def extract_phone(text):
    phone_pattern = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    matches = re.findall(phone_pattern, text)
    return matches[0] if matches else None

def extract_skills(text):
    doc = nlp(text)
    key_skills = []
    for token in doc:
        if token.pos_ in ["ADJ", "NOUN"]:
            key_skills.append(token.text)
    return key_skills

def extract_job_title(text):
    doc = nlp(text)
    for token in doc:
        if token.pos_ == "NOUN" and token.text.lower() in ["developer", "engineer", "designer", "analyst"]:
            return token.text
    return None

def extract_companies(text):
    doc = nlp(text)
    companies = []
    for token in doc:
        if token.pos_ == "PROPN":
            companies.append(token.text)
    return companies

def extract_experience(text):
    doc = nlp(text)
    for token in doc:
        if token.pos_ == "NUM":
            return token.text
    return None

def extract_education(text):
    doc = nlp(text)
    for token in doc:
        if token.pos_ == "PROPN":
            return token.text
    return None

