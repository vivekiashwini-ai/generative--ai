import json
from typing import List, Dict, Any
from pathlib import Path

# Sample job profiles for demonstration
SAMPLE_JOB_PROFILES = [
    {
        "id": 1,
        "title": "Data Analyst",
        "company": "TechCorp Industries",
        "location": "Remote",
        "experience": "2-4 years",
        "description": "Analyze data to provide business insights and recommendations",
        "required_skills": ["Python", "SQL", "Excel", "Data Visualization", "Statistics"],
        "preferred_skills": ["Tableau", "Power BI", "AWS"],
        "salary_range": "$60,000 - $85,000",
        "application_link": "https://example.com/jobs/1"
    },
    {
        "id": 2,
        "title": "Software Developer",
        "company": "Innovatech Solutions",
        "location": "New York, NY",
        "experience": "3-5 years",
        "description": "Develop and maintain software applications using modern technologies",
        "required_skills": ["JavaScript", "Python", "Git", "SQL", "Data Structures"],
        "preferred_skills": ["React", "Node.js", "Docker"],
        "salary_range": "$80,000 - $120,000",
        "application_link": "https://example.com/jobs/2"
    },
    {
        "id": 3,
        "title": "Product Manager",
        "company": "Digital Products Inc.",
        "location": "San Francisco, CA",
        "experience": "5+ years",
        "description": "Manage product development and strategy from concept to launch",
        "required_skills": ["Product Strategy", "Data Analysis", "Communication", "Analytics"],
        "preferred_skills": ["Jira", "SQL", "A/B Testing"],
        "salary_range": "$100,000 - $150,000",
        "application_link": "https://example.com/jobs/3"
    }
]

# Skill taxonomy mapping job titles to required skills
SKILL_TAXONOMY = {
    "Data Analyst": ["Python", "SQL", "Excel", "Data Visualization", "Statistics", "Tableau"],
    "Software Developer": ["JavaScript", "Python", "Git", "SQL", "Data Structures", "React"],
    "Product Manager": ["Product Strategy", "Data Analysis", "Communication", "Analytics", "Jira"],
    "Marketing Specialist": ["SEO", "Content Creation", "Analytics", "Social Media", "Google Ads"],
    "Graphic Designer": ["Adobe Creative Suite", "Typography", "Color Theory", "Figma", "Illustrator"]
}

def get_job_recommendations(preferences: Dict[str, Any]) -> Dict[str, Any]:
    """Get job recommendations based on user preferences"""
    desired_role = preferences.get("desired_role", "").lower()
    location = preferences.get("location", "").lower()
    experience_level = preferences.get("experience_level", "").lower()
    skills = preferences.get("skills", [])
    
    recommendations = []
    
    for job in SAMPLE_JOB_PROFILES:
        match_score = 0
        match_reasons = []
        
        # Check role match
        if desired_role and desired_role in job["title"].lower():
            match_score += 35
            match_reasons.append("Role alignment")
        
        # Check location
        if location and location in job["location"].lower():
            match_score += 25
            match_reasons.append("Location match")
        
        # Check experience level
        if experience_level and experience_level in job["experience"].lower():
            match_score += 20
            match_reasons.append("Experience level match")
        
        # Check skills
        if skills:
            required = SKILL_TAXONOMY.get(job["title"], [])
            user_skills = set(s.lower() for s in skills)
            matching = user_skills.intersection(set(s.lower() for s in required))
            
            if matching:
                match_score += min(len(matching) * 5, 20)
                match_reasons.append(f"{len(matching)} skill(s) match")
        
        if match_score > 0:
            recommendations.append({
                "id": job["id"],
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "experience": job["experience"],
                "matchPercentage": min(match_score, 100),
                "matchReasons": match_reasons,
                "applicationLink": job["application_link"]
            })
    
    # Sort by match percentage (highest first)
    recommendations.sort(key=lambda x: x["matchPercentage"], reverse=True)
    
    return {
        "recommendations": recommendations,
        "total": len(recommendations)
    }

def analyze_skill_gaps(desired_job: str, current_skills: List[str]) -> Dict[str, Any]:
    """Analyze skill gaps for a target role"""
    required_skills = SKILL_TAXONOMY.get(desired_job, [])
    
    user_skill_set = set(current_skills)
    missing_skills = [skill for skill in required_skills if skill not in user_skill_set]
    
    # Create learning roadmap
    roadmap = []
    for skill in missing_skills:
        roadmap.append({
            "skill": skill,
            "beginner_resources": [
                {"title": f"Introduction to {skill}", "type": "course", "url": f"https://example.com/learn/{skill.lower()}"},
                {"title": f"Practice {skill} exercises", "type": "project", "url": f"https://example.com/projects/{skill.lower()}"}
            ],
            "intermediate_resources": [
                {"title": f"Advanced {skill}", "type": "course", "url": f"https://example.com/advanced/{skill.lower()}"}
            ]
        })
    
    progress = len(user_skill_set.intersection(set(required_skills))) / len(required_skills) * 100 if required_skills else 0
    
    return {
        "desired_job": desired_job,
        "required_skills": required_skills,
        "current_skills": current_skills,
        "missing_skills": missing_skills,
        "roadmap": roadmap,
        "progress": round(progress, 2)
    }