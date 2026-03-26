import json
from datetime import datetime
from pathlib import Path

from app.core.settings import SESSION_DIR


def _session_path(session_id: str) -> Path:
    return SESSION_DIR / f"{session_id}.json"


def create_session(session_id: str):

    data = {

        "session_id": session_id,

        "files": [],

        "config": None,

        "job_id": None,

        "status": "created",

        "report_path": None,

        "created_at": datetime.utcnow().isoformat()
    }

    save_session(data)

    return data


def load_session(session_id: str):

    path = _session_path(session_id)

    if not path.exists():

        raise Exception(f"Session not found: {session_id}")

    with open(path) as f:

        return json.load(f)


def save_session(data: dict):

    path = _session_path(data["session_id"])

    with open(path, "w") as f:

        json.dump(data, f, indent=2)


def add_file_to_session(session_id: str, filename: str):

    session = load_session(session_id)

    session["files"].append(filename)

    save_session(session)


def update_session(session_id: str, **kwargs):

    session = load_session(session_id)

    session.update(kwargs)

    save_session(session)