def match_skills(resume_skills,job_skills):
    resume_set=set(resume_skills)
    job_set=set(job_skills)

    matched_skills=list(resume_set&job_set)

    missing_skills=list(job_set-resume_set)

    match_score=(len(matched_skills)/len(job_set))*100

    return{
        "matched_skills":matched_skills,
        "missing_skills":missing_skills,
        "matched_score":round(match_score,2)}
