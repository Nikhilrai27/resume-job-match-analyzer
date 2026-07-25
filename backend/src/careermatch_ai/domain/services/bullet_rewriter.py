from dataclasses import dataclass

from careermatch_ai.infrastructure.llm.llm_service import LLMService


@dataclass(frozen=True)
class BulletRewriteSuggestion:
    original: str
    rewritten: str
    rationale: str


class BulletRewriter:
    def __init__(self, llm_service: LLMService) -> None:
        self._llm = llm_service

    def rewrite(self, bullets: list[str]) -> list[BulletRewriteSuggestion]:
        cleaned = [b.strip(" -") for b in bullets if b.strip(" -")]
        if not cleaned:
            return []

        result = self._llm.rewrite_bullets(cleaned)
        suggestions: list[BulletRewriteSuggestion] = []
        for item in result:
            suggestions.append(
                BulletRewriteSuggestion(
                    original=item.get("original", ""),
                    rewritten=item.get("rewritten", ""),
                    rationale=item.get("rationale", "Improved with LLM optimization."),
                )
            )
        return suggestions
