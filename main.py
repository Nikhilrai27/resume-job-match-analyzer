from app.utils.file_reader import read_resume
from app.services.skill_extractor import detect_skill

skills=["python","sql","machine-learning","fastapi","deep learning"]

content=read_resume("data/resume.txt")
detected_skills=detect_skill(content,skills)
print("detected skill ")
print(detected_skills )