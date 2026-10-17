import json
from typing import List, Dict, Any
from pathlib import Path

# Sample resume templates
RESUME_TEMPLATES = {
    "professional": {
        "header": {
            "name": True,
            "title": True,
            "contact": True
        },
        "sections": ["summary", "experience", "education", "skills", "projects"],
        "format": "clean-professional"
    },
    "modern": {
        "header": {
            "name": True,
            "title": True,
            "contact": True,
            "profile_image": False
        },
        "sections": ["summary", "experience", "education", "skills", "projects", "certifications"],
        "format": "contemporary"
    },
    "creative": {
        "header": {
            "name": True,
            "title": True,
            "contact": True,
            "portfolio": True
        },
        "sections": ["summary", "experience", "education", "skills", "projects", "awards"],
        "format": "artistic"
    }
}

def generate_resume_content(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate professional resume content from user data"""
    name = resume_data.get("name", "")
    email = resume_data.get("email", "")
    phone = resume_data.get("phone", "")
    summary = resume_data.get("summary", "")
    
    # Extract sections
    education = resume_data.get("education", [])
    experience = resume_data.get("experience", [])
    skills = resume_data.get("skills", [])
    projects = resume_data.get("projects", [])
    certifications = resume_data.get("certifications", [])
    
    # Validate required fields
    if not name:
        return {"error": "Name is required"}
    
    # Generate resume structure
    resume = {
        "personal_info": {
            "name": name,
            "email": email,
            "phone": phone
        },
        "summary": summary or "Professional with experience in various domains seeking to contribute skills and expertise to a dynamic organization.",
        "education": education or [
            {
                "degree": "Bachelor's Degree",
                "institution": "University Name",
                "graduation_year": "2020"
            }
        ],
        "experience": experience or [
            {
                "position": "Job Title",
                "company": "Company Name",
                "duration": "Month Year - Present",
                "description": "Key responsibilities and achievements"
            }
        ],
        "skills": skills or [
            {"name": "Python", "level": "Intermediate"},
            {"name": "SQL", "level": "Intermediate"}
        ],
        "projects": projects or [
            {
                "title": "Sample Project",
                "description": "Description of project",
                "technologies": ["Technology 1", "Technology 2"]
            }
        ],
        "certifications": certifications or []
    }
    
    return {
        "resume": resume,
        "template": "professional",
        "ats_friendly": True,
        "word_count": len(summary.split()) if summary else 0
    }

def export_resume_pdf(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """Export resume as PDF"""
    # In a real implementation, this would use a PDF generation library
    # like ReportLab, WeasyPrint, or FPDF
    return {
        "success": True,
        "message": "Resume exported as PDF",
        "download_url": "/download/resume.pdf",
        "file_size": "1.2 MB"
    }

def get_resume_template(template_name: str) -> Dict[str, Any]:
    """Get resume template configuration"""
    return RESUME_TEMPLATES.get(template_name, RESUME_TEMPLATES["professional"])