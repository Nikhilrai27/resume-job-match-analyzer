def read_resume(path):
    with open(path,"r") as file:
        content=file.read().lower()
        return content
