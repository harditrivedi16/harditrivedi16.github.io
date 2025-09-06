from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class EducationItem(BaseModel):
    degree: str = ""
    field: str = ""
    institution: str = ""
    start_date: str = ""
    end_date: str = ""
    location: str = ""
    details: List[str] = Field(default_factory=list)
    courses: List[str] = Field(default_factory=list)

class ExperienceItem(BaseModel):
    title: str = ""
    company: str = ""
    date_range: str = ""
    location: str = ""
    bullets: List[str] = Field(default_factory=list)
    more_bullets: List[str] = Field(default_factory=list)

class ProjectItem(BaseModel):
    name: str
    bullets: List[str] = Field(default_factory=list)
    year: str = ""

class UserData(BaseModel):
    # identity
    firstName: str = ""
    lastName: str = ""
    headline: str = ""
    about: str = ""  # long paragraph for myDescription[0]

    # socials (handles only)
    github: str = ""
    facebook: str = ""
    instagram: str = ""
    linkedin: str = ""
    twitter: str = ""
    medium: str = ""

    # profile links/extras
    insta_link: str = ""         # if you want to keep a direct link
    email: str = ""
    phone: str = ""

    # content
    education: List[EducationItem] = Field(default_factory=list)
    experience: List[ExperienceItem] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)

    # github repos & maps 
    repo_names: List[str] = Field(default_factory=list)      # ["Repo1", "Repo2", ...]
    project_desc: Dict[str, List[str]] = Field(default_factory=dict)   # {repoName: [bullets]}
    project_dates: Dict[str, str] = Field(default_factory=dict)        # {repoName: "2025"}

    # raw text (helps regen)
    raw_resume_text: str = ""
