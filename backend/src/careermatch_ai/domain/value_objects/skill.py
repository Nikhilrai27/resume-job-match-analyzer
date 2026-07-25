from dataclasses import dataclass


@dataclass(frozen=True)
class Skill:
    name: str
    category: str = "general"
