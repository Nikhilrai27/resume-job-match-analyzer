def detect_skill(content,skills):
    found_skills=[]
    for skill in skills:
        if skill in content:
            found_skills.append(skill)

    return found_skills        