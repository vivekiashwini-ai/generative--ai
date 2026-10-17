from typing import List, Dict, Optional
from pydantic import BaseModel

class ImageRemoveBackgroundRequest(BaseModel):
    file: bytes
    model: Optional[str] = "u2net"

class ImageResizeRequest(BaseModel):
    file: bytes
    width: int
    height: int
    maintain_aspect_ratio: bool = True

class ImageCompressRequest(BaseModel):
    file: bytes
    output_format: str = "png"
    quality: float = 0.8

class ResumeGenerateRequest(BaseModel):
    name: str
    email: str
    phone: str
    summary: str
    education: List[dict]
    experience: List[dict]
    skills: List[dict]
    projects: List[dict]
    certifications: List[dict]

class JobRecommendationRequest(BaseModel):
    desired_role: str
    location: str
    experience_level: str
    skills: List[str]

class SkillGapAnalysisRequest(BaseModel):
    desired_job: str
    current_skills: List[str]

class AssessmentStartRequest(BaseModel):
    skill: str
    difficulty: str

class AssessmentSubmitRequest(BaseModel):
    answers: dict
    assessment_id: str

class WritingGenerateRequest(BaseModel):
    task: str
    tone: str
    text: str