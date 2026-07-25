import os
import sys
import tempfile
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend" / "src"))

from careermatch_ai.infrastructure.llm.gemini_client import GeminiClient
from careermatch_ai.infrastructure.llm.groq_client import GroqClient
from careermatch_ai.infrastructure.llm.llm_service import LLMService
from careermatch_ai.infrastructure.parsers.resume_parser import ResumeParser

st.set_page_config(page_title="CareerMatch AI", page_icon="📋", layout="wide")

st.title("📋 CareerMatch AI")
st.markdown("Upload a resume and analyze it against company profiles using AI.")

with st.sidebar:
    st.header("🔑 API Keys")
    groq_key = st.text_input("GROQ_API_KEY", type="password", value=os.getenv("GROQ_API_KEY", ""))
    gemini_key = st.text_input("GEMINI_API_KEY", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    groq_model = st.text_input("Groq Model", value=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"))
    gemini_model = st.text_input("Gemini Model", value=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"))

    st.divider()
    st.header("📁 Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf", "txt", "docx"])

    st.divider()
    st.header("⚙️ Analysis Mode")
    mode = st.radio("Match against:", ["Company Profiles (IT Companies)", "Job Description"])

    job_description = None
    if mode == "Job Description":
        job_description = st.text_area("Paste job description", height=300)

    analyze_btn = st.button("🚀 Analyze Resume", type="primary", use_container_width=True)


def get_llm_service() -> LLMService | None:
    primary = None
    fallbacks = []
    if groq_key:
        primary = GroqClient(api_key=groq_key, model=groq_model)
    if gemini_key:
        fallbacks.append(GeminiClient(api_key=gemini_key, model=gemini_model))
    openai_key = os.getenv("OPENAI_API_KEY", "")
    if openai_key:
        from careermatch_ai.infrastructure.llm.openai_client import OpenAIClient
        fallbacks.append(OpenAIClient(api_key=openai_key))
    if not primary:
        st.error("At least GROQ_API_KEY is required")
        return None
    return LLMService(primary_client=primary, fallback_clients=fallbacks)


def display_score_card(label: str, score: float, help_text: str = ""):
    color = "green" if score >= 80 else ("orange" if score >= 60 else "red")
    st.markdown(
        f"""<div style="padding:4px 0">
            <span style="font-size:14px">{label}</span>
            <span style="float:right;font-weight:bold;color:{color}">{score:.1f}%</span>
        </div>""",
        unsafe_allow_html=True,
    )


if analyze_btn and uploaded_file is not None:
    llm_service = get_llm_service()
    if llm_service is None:
        st.stop()

    with st.spinner("Parsing resume..."):
        suffix = Path(uploaded_file.name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        parser = ResumeParser(llm_service=llm_service)
        resume = parser.parse(Path(tmp_path))
        os.unlink(tmp_path)

    st.success("Resume parsed successfully!")
    st.header("📄 Resume Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Name", resume.candidate_name)
    col2.metric("Email", resume.email or "N/A")
    col3.metric("Skills", len(resume.skills))

    with st.expander("View full parsed resume"):
        st.json({
            "name": resume.candidate_name,
            "email": resume.email,
            "phone": resume.phone,
            "summary": resume.summary,
            "skills": resume.skills,
            "education": [{"degree": e.degree, "institution": e.institution} for e in resume.education],
            "experience": [{"title": e.title, "company": e.company, "years": e.years} for e in resume.experience],
            "projects": [{"name": p.name, "technologies": p.technologies} for p in resume.projects],
            "certifications": resume.certifications,
        })

    if mode == "Company Profiles (IT Companies)":
        from careermatch_ai.application.services.company_matching_service import CompanyMatchingService
        from careermatch_ai.domain.services.bullet_rewriter import BulletRewriter
        from careermatch_ai.domain.services.gap_analyzer import GapAnalyzer
        from careermatch_ai.infrastructure.config.company_loader import CompanyProfileLoader
        from careermatch_ai.infrastructure.scoring.ats_engine import ATSScoringEngine

        profiles_dir = Path(__file__).resolve().parents[1] / "company_profiles"

        with st.spinner("Analyzing against company profiles..."):
            loader = CompanyProfileLoader(profiles_dir)
            matcher = CompanyMatchingService(
                loader=loader,
                scoring_engine=ATSScoringEngine(llm_service=llm_service),
                gap_analyzer=GapAnalyzer(llm_service=llm_service),
                bullet_rewriter=BulletRewriter(llm_service=llm_service),
                llm_service=llm_service,
            )
            scores = matcher.match(resume)

        st.header("🏢 Company Match Scores")

        overall_ats = round(sum(s.overall_score for s in scores) / max(len(scores), 1), 2)
        st.metric("Overall ATS Score", f"{overall_ats:.1f}%")

        cols = st.columns(3)
        for i, score in enumerate(scores):
            with cols[i % 3]:
                color = "green" if score.overall_score >= 80 else ("orange" if score.overall_score >= 60 else "red")
                st.markdown(
                    f"""<div style="border:1px solid #ddd;border-radius:10px;padding:16px;margin:8px 0">
                        <h3 style="margin:0">{score.company_slug.upper()}</h3>
                        <div style="font-size:36px;font-weight:bold;color:{color}">{score.overall_score:.1f}%</div>
                        <div style="margin-top:8px">✅ {len(score.matched_skills)} matched</div>
                        <div style="color:red">❌ {len(score.missing_skills)} missing</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
                with st.expander(f"Details for {score.company_slug.upper()}"):
                    st.subheader("Score Breakdown")
                    display_score_card("Skill Match", score.score_breakdown.get("skill_match", 0))
                    display_score_card("Experience", score.score_breakdown.get("experience_relevance", 0))
                    display_score_card("Education", score.score_breakdown.get("education_fit", 0))
                    display_score_card("Projects", score.score_breakdown.get("project_relevance", 0))
                    display_score_card("Certifications", score.score_breakdown.get("certification_boost", 0))
                    display_score_card("Formatting", score.score_breakdown.get("formatting", 0))

                    if score.matched_skills:
                        st.subheader("✅ Matched Skills")
                        st.write(", ".join(score.matched_skills))
                    if score.missing_skills:
                        st.subheader("❌ Missing Skills")
                        st.write(", ".join(score.missing_skills))
                    if score.gaps:
                        st.subheader("🔍 Gaps")
                        for gap in score.gaps:
                            st.markdown(f"- {gap}")
                    if score.recommendations:
                        st.subheader("💡 Recommendations")
                        for rec in score.recommendations:
                            st.markdown(f"- {rec}")

        st.header("📝 Rewritten Bullets")
        if scores and scores[0].rewritten_bullets:
            for rb in scores[0].rewritten_bullets:
                st.markdown(f"- {rb}")

    elif job_description:
        with st.spinner("Analyzing against job description..."):
            result = llm_service.match_job_description(
                job_text=job_description,
                resume_skills=resume.skills,
                experience=[{"title": e.title, "company": e.company, "years": e.years, "bullets": e.bullets} for e in resume.experience],
                education=[{"degree": e.degree, "institution": e.institution, "year": e.year} for e in resume.education],
                projects=[{"name": p.name, "summary": p.summary, "technologies": p.technologies} for p in resume.projects],
                certifications=resume.certifications,
                sections_present=resume.sections_present,
                summary=resume.summary,
            )
            if isinstance(result, dict):
                st.metric("Match Score", f"{result.get('overall_score', 0):.1f}%")
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("✅ Matched Skills")
                    st.write(", ".join(result.get("matched_skills", [])) or "None")
                with col2:
                    st.subheader("❌ Missing Skills")
                    st.write(", ".join(result.get("missing_skills", [])) or "None")
                st.subheader("Score Breakdown")
                for key in ["skill_match", "experience_relevance", "education_fit", "project_relevance"]:
                    display_score_card(key.replace("_", " ").title(), result.get(key, 0))

elif analyze_btn:
    st.warning("Please upload a resume file first.")
