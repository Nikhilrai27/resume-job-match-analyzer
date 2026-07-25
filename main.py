import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve() / "backend" / "src"))

import json

from careermatch_ai.infrastructure.llm.gemini_client import GeminiClient
from careermatch_ai.infrastructure.llm.groq_client import GroqClient
from careermatch_ai.infrastructure.llm.llm_service import LLMService
from careermatch_ai.infrastructure.parsers.resume_parser import ResumeParser


def build_parser():
    parser = argparse.ArgumentParser(
        description="Analyze how well a resume matches a job description using AI."
    )
    parser.add_argument("--resume", required=True, help="Path to the resume file (.pdf or .txt).")
    parser.add_argument("--job-description", help="Raw job description text.")
    parser.add_argument("--job-file", help="Path to the job description file (.pdf or .txt).")
    parser.add_argument("--json-output", help="Optional path to save the analysis report as JSON.")
    parser.add_argument("--groq-key", help="GROQ API key (default: GROQ_API_KEY env var).")
    parser.add_argument("--gemini-key", help="Gemini API key (default: GEMINI_API_KEY env var).")
    return parser


def get_llm_service(args) -> LLMService:
    groq_key = args.groq_key or os.getenv("GROQ_API_KEY", "")
    gemini_key = args.gemini_key or os.getenv("GEMINI_API_KEY", "")
    openai_key = os.getenv("OPENAI_API_KEY", "")
    primary = GroqClient(api_key=groq_key) if groq_key else None
    fallbacks = []
    if gemini_key:
        fallbacks.append(GeminiClient(api_key=gemini_key))
    if openai_key:
        from careermatch_ai.infrastructure.llm.openai_client import OpenAIClient
        fallbacks.append(OpenAIClient(api_key=openai_key))
    if not primary:
        raise ValueError("GROQ_API_KEY is required. Set it as an env var or pass --groq-key.")
    return LLMService(primary_client=primary, fallback_clients=fallbacks)


def load_text(file_path: str) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    return path.read_text(encoding="utf-8")


def main():
    args = build_parser().parse_args()
    llm = get_llm_service(args)

    parser = ResumeParser(llm_service=llm)
    resume = parser.parse(Path(args.resume))

    if args.job_file:
        job_text = load_text(args.job_file)
    elif args.job_description:
        job_text = args.job_description
    else:
        job_text = ""

    result = llm.match_job_description(
        job_text=job_text or "No job description provided.",
        resume_skills=resume.skills,
        experience=[{"title": e.title, "company": e.company, "years": e.years, "bullets": e.bullets} for e in resume.experience],
        education=[{"degree": e.degree, "institution": e.institution, "year": e.year} for e in resume.education],
        projects=[{"name": p.name, "summary": p.summary, "technologies": p.technologies} for p in resume.projects],
        certifications=resume.certifications,
        sections_present=resume.sections_present,
        summary=resume.summary,
    )

    if isinstance(result, dict):
        print(f"Overall Match Score: {result.get('overall_score', 'N/A')}%")
        print(f"Matched Skills: {', '.join(result.get('matched_skills', [])) or 'None'}")
        print(f"Missing Skills: {', '.join(result.get('missing_skills', [])) or 'None'}")
        if result.get("recommendations"):
            print("\nRecommendations:")
            for rec in result["recommendations"]:
                print(f"- {rec}")

    if args.json_output:
        with open(args.json_output, "w", encoding="utf-8") as f:
            json.dump(result if isinstance(result, dict) else {}, f, indent=2)
        print(f"\nSaved JSON report to {args.json_output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        raise SystemExit(1)
