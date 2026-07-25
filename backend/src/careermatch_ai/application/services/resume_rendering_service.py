from careermatch_ai.domain.entities.analysis import ResumeAnalysis
from careermatch_ai.domain.entities.resume import ResumeAggregate


class ResumeRenderingService:
    def render_markdown(self, resume: ResumeAggregate, analysis: ResumeAnalysis) -> str:
        top_company = analysis.company_scores[0] if analysis.company_scores else None
        top_skills = ", ".join(resume.skills[:10])
        lines = [
            f"# {resume.candidate_name}",
            "",
            f"- Email: {resume.email}",
            f"- Phone: {resume.phone}",
            "",
            "## Professional Summary",
            resume.summary or "Results-driven professional aligned to enterprise technology roles.",
            "",
            "## Skills",
            top_skills or "Add core technical skills here.",
            "",
            "## Experience",
        ]

        for experience in resume.experience:
            lines.append(f"### {experience.title} | {experience.company}")
            for bullet in experience.bullets:
                lines.append(f"- {bullet}")

        lines.extend(["", "## Education"])
        for education in resume.education:
            lines.append(f"- {education.degree}")

        lines.extend(["", "## Certifications"])
        for certification in resume.certifications or ["Add role-relevant certifications here"]:
            lines.append(f"- {certification}")

        if top_company:
            lines.extend([
                "",
                "## ATS Optimization Notes",
                f"- Best fit company: {top_company.company_slug.upper()}",
                f"- ATS score: {top_company.overall_score}",
            ])

        return "\n".join(lines)

    def render_plain_text(self, resume: ResumeAggregate, analysis: ResumeAnalysis) -> str:
        markdown = self.render_markdown(resume, analysis)
        return (
            markdown
            .replace("### ", "")
            .replace("## ", "")
            .replace("# ", "")
        )
