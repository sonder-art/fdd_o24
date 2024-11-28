# backend/app/utils.py
ALLOWED_EXTENSIONS = {".xlsx"}

def allowed_file(filename):
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)
