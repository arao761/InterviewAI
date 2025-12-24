"""
Resume Data Schemas
Pydantic models for structured resume data
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import date


class Contact(BaseModel):
    """Contact information"""
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    location: Optional[str] = None

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v:
            # Basic phone validation - just ensure it has digits
            import re
            if not re.search(r'\d', v):
                return None
        return v


class Education(BaseModel):
    """Education entry"""
    institution: str
    degree: str
    field: Optional[str] = None
    graduation_date: Optional[str] = None
    gpa: Optional[str] = None
    honors: List[str] = Field(default_factory=list)
    relevant_coursework: List[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "institution": "Stanford University",
                "degree": "Bachelor of Science",
                "field": "Computer Science",
                "graduation_date": "May 2022",
                "gpa": "3.8/4.0",
                "honors": ["Dean's List", "Cum Laude"]
            }
        }


class Experience(BaseModel):
    """Work experience entry"""
    company: str
    title: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None  # "Present" for current role
    location: Optional[str] = None
    responsibilities: List[str] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v):
        # Convert various current date indicators to "Present"
        if v and v.lower() in ['current', 'now', 'ongoing']:
            return "Present"
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "company": "Google",
                "title": "Software Engineer",
                "start_date": "June 2022",
                "end_date": "Present",
                "location": "Mountain View, CA",
                "responsibilities": [
                    "Developed microservices using Python and Go",
                    "Led team of 3 engineers"
                ],
                "achievements": [
                    "Reduced API latency by 40%",
                    "Improved test coverage from 60% to 95%"
                ],
                "technologies": ["Python", "Go", "Kubernetes", "AWS"]
            }
        }


class Project(BaseModel):
    """Project entry"""
    name: str
    description: str
    technologies: List[str] = Field(default_factory=list)
    url: Optional[str] = None
    highlights: List[str] = Field(default_factory=list)
    duration: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "E-commerce Platform",
                "description": "Built full-stack e-commerce platform with React and Node.js",
                "technologies": ["React", "Node.js", "MongoDB", "Stripe"],
                "url": "https://github.com/user/ecommerce",
                "highlights": [
                    "Handled 10k+ daily active users",
                    "Integrated payment processing"
                ]
            }
        }


class Skills(BaseModel):
    """Skills categorization"""
    technical: List[str] = Field(default_factory=list)
    soft: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)  # Programming languages
    frameworks: List[str] = Field(default_factory=list)
    databases: List[str] = Field(default_factory=list)
    cloud: List[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "technical": ["Python", "JavaScript", "Java", "C++"],
                "soft": ["Leadership", "Communication", "Problem Solving"],
                "tools": ["Git", "Docker", "Jenkins"],
                "languages": ["Python", "JavaScript", "TypeScript"],
                "frameworks": ["React", "Django", "FastAPI"],
                "databases": ["PostgreSQL", "MongoDB", "Redis"],
                "cloud": ["AWS", "GCP", "Azure"]
            }
        }


class ParsedResume(BaseModel):
    """Complete parsed resume structure"""
    contact: Contact
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    skills: Skills = Field(default_factory=Skills)
    projects: List[Project] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    leadership: List[str] = Field(default_factory=list)
    awards: List[str] = Field(default_factory=list)
    publications: List[str] = Field(default_factory=list)
    volunteer: List[str] = Field(default_factory=list)

    # Metadata (auto-calculated)
    experience_level: Optional[str] = None  # "junior", "mid", "senior"
    total_years_experience: Optional[float] = None
    primary_domain: Optional[str] = None  # "software_engineering", "data_science", etc.

    @field_validator('experience_level')
    @classmethod
    def determine_experience_level(cls, v, info):
        """Auto-determine experience level from years of experience"""
        if v:  # If explicitly set, use that
            return v

        # Get total_years_experience from the data
        total_years = info.data.get('total_years_experience', 0) or 0

        if total_years < 2:
            return "junior"
        elif total_years < 5:
            return "mid"
        else:
            return "senior"

    def get_summary(self, max_length: int = 500) -> str:
        """Get concise resume summary"""
        summary_parts = []

        # Name and contact
        summary_parts.append(f"Name: {self.contact.name}")

        # Experience level
        if self.experience_level:
            summary_parts.append(f"Level: {self.experience_level.title()}")

        # Current/most recent role
        if self.experience:
            latest = self.experience[0]
            summary_parts.append(
                f"Current Role: {latest.title} at {latest.company}"
            )

        # Education
        if self.education:
            latest_edu = self.education[0]
            summary_parts.append(
                f"Education: {latest_edu.degree} in {latest_edu.field or 'N/A'}"
            )

        # Top skills
        if self.skills.technical:
            top_skills = ", ".join(self.skills.technical[:5])
            summary_parts.append(f"Skills: {top_skills}")

        summary = " | ".join(summary_parts)

        if len(summary) > max_length:
            summary = summary[:max_length-3] + "..."

        return summary

    def count_total_projects(self) -> int:
        """Count total number of projects"""
        return len(self.projects)

    def count_total_achievements(self) -> int:
        """Count total achievements across all experiences"""
        return sum(len(exp.achievements) for exp in self.experience)

    def has_leadership_experience(self) -> bool:
        """Check if candidate has leadership experience"""
        if self.leadership:
            return True

        # Check for leadership keywords in titles or responsibilities
        leadership_keywords = ['lead', 'manager', 'director', 'head', 'chief', 'vp']

        for exp in self.experience:
            title_lower = exp.title.lower()
            if any(keyword in title_lower for keyword in leadership_keywords):
                return True

            # Check responsibilities
            for resp in exp.responsibilities:
                resp_lower = resp.lower()
                if any(keyword in resp_lower for keyword in leadership_keywords):
                    return True

        return False

    class Config:
        json_schema_extra = {
            "example": {
                "contact": {
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "phone": "555-1234",
                    "linkedin": "linkedin.com/in/johndoe",
                    "github": "github.com/johndoe"
                },
                "education": [{
                    "institution": "MIT",
                    "degree": "BS",
                    "field": "Computer Science",
                    "graduation_date": "2020"
                }],
                "experience": [{
                    "company": "Google",
                    "title": "Software Engineer",
                    "start_date": "2020",
                    "end_date": "Present"
                }],
                "skills": {
                    "technical": ["Python", "Java", "React"],
                    "tools": ["Git", "Docker"]
                },
                "total_years_experience": 4.0,
                "experience_level": "mid"
            }
        }
