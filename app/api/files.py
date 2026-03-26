from fastapi import APIRouter, UploadFile, File, Form
from typing import List
from pathlib import Path

from app.core.settings import (
    INPUT_DIR,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB,
    ensure_directories
)

from app.services.session_store import (
    create_session,
    add_file_to_session
)

router = APIRouter()


def validate_file(file: UploadFile):

    ext = Path(file.filename).suffix.lower()

    if ext not in ALLOWED_EXTENSIONS:

        raise Exception(
            f"INVALID_FILE_TYPE: {file.filename}"
        )


async def save_file(
    file: UploadFile,
    session_id: str
):

    session_dir = INPUT_DIR / session_id

    session_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    path = session_dir / file.filename

    size = 0

    with open(path, "wb") as f:

        while chunk := await file.read(1024 * 1024):

            size += len(chunk)

            if size > MAX_FILE_SIZE_MB * 1024 * 1024:

                raise Exception(
                    f"FILE_TOO_LARGE: {file.filename}"
                )

            f.write(chunk)

    return file.filename


@router.post("/api/files/upload")

async def upload_files(

    files: List[UploadFile] = File(...),

    session_id: str = Form(...)
):

    ensure_directories()

    create_session(session_id)

    uploaded = []

    for file in files:

        validate_file(file)

        name = await save_file(file, session_id)

        add_file_to_session(session_id, name)

        uploaded.append(name)

    return {

        "status": "success",

        "session_id": session_id,

        "uploaded_files": uploaded
    }