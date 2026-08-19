from pathlib import Path
import uuid

from fastapi import FastAPI, File, Form, UploadFile, HTTPException

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_COURSES = [
    "Python Basic",
    "FastAPI",
    "Data Analysis",
]

ALLOWED_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
]

MAX_FILE_SIZE = 2 * 1024 * 1024 


@app.post("/students/register")
async def register_student(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    course: str = Form(...),
    avatar: UploadFile = File(...),
):
    full_name = full_name.strip()

    if not full_name:
        raise HTTPException(
            status_code=400,
            detail="Full name is required"
        )
    email = email.strip()

    if (
        "@" not in email
        or email.startswith("@")
        or email.endswith("@")
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid email"
        )

    phone = phone.strip()

    if not phone.isdigit() or len(phone) != 10:
        raise HTTPException(
            status_code=400,
            detail="Phone number must contain exactly 10 digits"
        )
    course = course.strip()

    if course not in ALLOWED_COURSES:
        raise HTTPException(
            status_code=400,
            detail="Course is not available"
        )

    if not avatar.filename:
        raise HTTPException(
            status_code=400,
            detail="Avatar is required"
        )

    extension = Path(avatar.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only JPG and PNG files are allowed"
        )

    content = await avatar.read()


    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Avatar file must not exceed 2 MB"
        )

    new_filename = f"{uuid.uuid4()}{extension}"

    file_path = UPLOAD_DIR / new_filename

    with open(file_path, "wb") as file:
        file.write(content)
    return {
        "success": True,
        "message": "Registration successful",
        "data": {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "course": course,
            "avatar": str(file_path),
        },
    }