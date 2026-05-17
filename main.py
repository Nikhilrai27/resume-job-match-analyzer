from app.utils.file_reader import read_resume
from app.services.skill_extractor import detect_skill
from app.services.pdf_praser import extract_text_from_pdf
from app.services.job_matcher import match_skills

resume_path="data/resume.pdf"
try:
    if resume_path.endswith(".txt"):
        content=read_resume("data/resume.txt")
    elif resume_path.endswith(".pdf"):
        content=extract_text_from_pdf(resume_path) 
    else:
        print("unsupported file format")  
        raise ValueError 
    skills=["python",
            "sql",
            "machine-learning",
            "fastapi",
            "deep learning"]

    detected_skills=detect_skill(content,skills)
    result=match_skills(detected_skills,skills)
    print("detected skill ")
    print(detected_skills )
    print(result)
except FileNotFoundError:
    print("resume file not found")

except Exception as error:
    print("something went wrong")
    print(error)
