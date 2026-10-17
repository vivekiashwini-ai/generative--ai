import json
import os
from pathlib import Path
from typing import List, Dict, Any

# Sample data for demonstration
SAMPLE_JOBS = [
    {
        "id": 1,
        "title": "Data Analyst",
        "company": "TechCorp Industries",
        "location": "Remote",
        "experience": "2-4 years",
        "description": "Analyze data to provide business insights"
    },
    {
        "id": 2,
        "title": "Software Developer",
        "company": "Innovatech Solutions",
        "location": "New York, NY",
        "experience": "3-5 years",
        "description": "Develop and maintain software applications"
    },
    {
        "id": 3,
        "title": "Product Manager",
        "company": "Digital Products Inc.",
        "location": "San Francisco, CA",
        "experience": "5+ years",
        "description": "Manage product development and strategy"
    }
]

SAMPLE_SKILL_TAXONOMY = {
    "Data Analyst": ["Python", "SQL", "Excel", "Data Visualization", "Statistics"],
    "Software Developer": ["JavaScript", "Python", "Git", "SQL", "Data Structures"],
    "Product Manager": ["Product Strategy", "Data Analysis", "Communication", "Analytics"],
    "Marketing Specialist": ["SEO", "Content Creation", "Analytics", "Social Media"],
    "Graphic Designer": ["Adobe Creative Suite", "Typography", "Color Theory", "Figma"]
}

def get_job_recommendations(preferences: Dict[str, Any]) -> List[Dict]:
    """Get job recommendations based on user preferences"""
    desired_role = preferences.get("desired_role", "")
    location = preferences.get("location", "")
    experience_level = preferences.get("experience_level", "")
    skills = preferences.get("skills", [])
    
    # Filter sample jobs based on basic criteria
    recommendations = []
    for job in SAMPLE_JOBS:
        match_score = 0
        match_reasons = []
        
        # Check if desired role matches job title
        if desired_role.lower() in job["title"].lower():
            match_score += 30
            match_reasons.append("Role alignment")
        
        # Check location
        if location and location.lower() in job["location"].lower():
            match_score += 25
            match_reasons.append("Location match")
        
        # Check experience level
        if experience_level and experience_level.lower() in job["experience"].lower():
            match_score += 20
            match_reasons.append("Experience level match")
        
        # Check skills
        if skills:
            job_skills = set()
            for skill_key, required_skills in SAMPLE_SKILL_TAXONOMY.items():
                if desired_role.lower() in skill_key.lower():
                    job_skills = set(required_skills)
                    break
            
            user_skills = set(skills.lower() for skills in skills)
            matching_skills = user_skills.intersection(job_skills)
            
            if matching_skills:
                match_score += min(len(matching_skills) * 5, 25)
                match_reasons.append(f"{len(matching_skills)} skill(s) match")
        
        if match_score > 0:
            recommendations.append({
                "id": job["id"],
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "experience": job["experience"],
                "matchPercentage": min(match_score, 100),
                "matchReasons": match_reasons,
                "applyLink": f"https://example.com/jobs/{job['id']}"
            })
    
    return sorted(recommendations, key=lambda x: x["matchPercentage"], reverse=True)

def analyze_skill_gaps(desired_job: str, current_skills: List[str]) -> Dict[str, Any]:
    """Analyze skill gaps for a target role"""
    required_skills = SAMPLE_SKILL_TAXONOMY.get(desired_job, [])
    
    user_skill_set = set(current_skills)
    missing_skills = [skill for skill in required_skills if skill not in user_skill_set]
    
    # Create a learning roadmap
    roadmap = []
    for skill in missing_skills:
        roadmap.append({
            "skill": skill,
            "resources": [
                {"title": f"Learn {skill}", "type": "course", "url": f"https://example.com/learn/{skill.lower().replace(' ', '-')}"},
                {"title": f"Practice {skill}", "type": "project", "url": f"https://example.com/projects/{skill.lower().replace(' ', '-')}"}
            ]
        })
    
    return {
        "desired_job": desired_job,
        "required_skills": required_skills,
        "current_skills": current_skills,
        "missing_skills": missing_skills,
        "roadmap": roadmap,
        "progress": len(current_skills) / len(required_skills) * 100 if required_skills else 0
    }

def start_skill_assessment(skill: str, difficulty: str) -> Dict[str, Any]:
    """Start a skill assessment"""
    question_banks = {
        "Python": {
            "beginner": [
                {"id": 1, "question": "What is the correct way to define a function in Python?", 
                 "options": ["def my_function():", "function my_function():", "def my_function(x):", "function my_function(x)"],
                 "answer": 0},
                {"id": 2, "question": "Which of the following is used to iterate over a range of numbers?",
                 "options": ["for i in range(5):", "for i from 0 to 5:", "for i in 5:", "for i = 0; i < 5; i++"],
                 "answer": 0}
            ]
        },
        "SQL": {
            "beginner": [
                {"id": 1, "question": "Which SQL clause is used to filter results?",
                 "options": ["SELECT", "FROM", "WHERE", "GROUP BY"],
                 "answer": 2}
            ]
        }
    }
    
    bank = question_banks.get(skill, {}).get(difficulty, [])
    
    return {
        "assessment_id": f"{skill.lower()}-{difficulty}-123",
        "skill": skill,
        "difficulty": difficulty,
        "questions": bank,
        "current_question": 0,
        "score": 0
    }

def submit_skill_assessment(assessment_id: str, answers: dict) -> Dict[str, Any]:
    """Submit skill assessment answers"""
    # In a real implementation, this would calculate the score
    # For now, return mock results
    skill = assessment_id.split("-")[0]
    total_questions = 5  # Mock value
    correct_answers = 3  # Mock value
    score_percentage = round((correct_answers / total_questions) * 100)
    
    # Topic analysis
    topic_analysis = {}
    if skill == "Python":
        topic_analysis = {"syntax": 90, "functions": 80, "libraries": 70}
    elif skill == "SQL":
        topic_analysis = {"queries": 85, "joins": 75, "aggregation": 65}
    
    return {
        "assessment_id": assessment_id,
        "score": score_percentage,
        "correctAnswers": correct_answers,
        "totalQuestions": total_questions,
        "topicAnalysis": topic_analysis,
        "feedback": f"Great job! You scored {score_percentage}%. Keep practicing to improve."
    }

def generate_writing_content(writing_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate written content using LLM"""
    task = writing_data.get("task", "improve")
    tone = writing_data.get("tone", "professional")
    text = writing_data.get("text", "")
    
    # Mock content generation based on task and tone
    if task == "improve":
        # Basic grammar improvement
        sentences = text.split('.')
        improved = '. '.join(s.strip().capitalize() for s in sentences if s.strip())
        return {"content": improved}
    
    elif task == "rewrite":
        return {"content": f"[Rewritten in {tone} tone]: {text}"}
    
    elif task == "summarize":
        sentences = text.split('.')
        summary = '. '.join(s.strip() for s in sentences[:3] if s.strip())
        return {"content": summary}
    
    elif task == "email":
        return {"content": f"Subject: Follow-up\n\nDear recipient,\n\n{text}\n\nBest regards"}
    
    elif task == "resume":
        return {"content": f"Professional Summary: {text}"}
    
    else:
        return {"content": text}