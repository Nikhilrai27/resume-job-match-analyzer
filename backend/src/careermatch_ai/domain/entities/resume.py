from dataclasses import dataclass, field


@dataclass(frozen=True)
class ExperienceEntry:
    title: str
    company: str
    years: float
    bullets: list[str]


@dataclass(frozen=True)
class EducationEntry:
    degree: str
    institution: str
    year: str


@dataclass(frozen=True)
class ProjectEntry:
    name: str
    summary: str
    technologies: list[str]


@dataclass(frozen=True)
class ResumeAggregate:
    candidate_name: str
    email: str
    phone: str
    summary: str
    skills: list[str]
    education: list[EducationEntry]
    experience: list[ExperienceEntry]
    projects: list[ProjectEntry]
    certifications: list[str]
    raw_text: str
    sections_present: list[str] = field(default_factory=list)
