import json
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

from careermatch_ai.domain.entities.company_profile import ATSWeights, CompanyProfile


class CompanyProfileLoader:
    def __init__(self, profiles_dir: Path) -> None:
        self._profiles_dir = profiles_dir

    def load_all(self) -> list[CompanyProfile]:
        return [self.load(path) for path in sorted(self._profiles_dir.glob("*.yaml"))]

    def load(self, path: Path) -> CompanyProfile:
        content = path.read_text(encoding="utf-8")
        payload = self._parse(content)
        weights = ATSWeights(**payload["ats_weights"])
        return CompanyProfile(
            slug=payload["slug"],
            display_name=payload["display_name"],
            sector=payload["sector"],
            focus_skills=payload["focus_skills"],
            preferred_certifications=payload["preferred_certifications"],
            required_sections=payload["required_sections"],
            preferred_keywords=payload["preferred_keywords"],
            ats_weights=weights,
            minimum_experience_years=payload.get("minimum_experience_years", 0),
            keywords_by_weight=payload.get("keywords_by_weight", {}),
        )

    def _parse(self, content: str) -> dict:
        if yaml is not None:
            return yaml.safe_load(content)
        return json.loads(content)
