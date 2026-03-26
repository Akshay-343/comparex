from fastapi import APIRouter
from uuid import uuid4
from pathlib import Path
import shutil

from app.models.schemas import RunReconcileRequest
from app.services.session_store import (
    load_session,
    update_session
)

from app.core.settings import INPUT_DIR
from app.reconcile_service import run_reconciliation


router = APIRouter()


def prepare_input_dir(session_id: str):

    session_input_dir = INPUT_DIR / session_id

    if not session_input_dir.exists():

        raise Exception(
            f"NO_FILE_FOUND: {session_id}"
        )

    # copy files to base input dir
    for f in session_input_dir.glob("*"):

        shutil.copy(
            f,
            INPUT_DIR / f.name
        )


@router.post("/api/reconcile/run")
def run_reconcile(
    payload: RunReconcileRequest
):

    session = load_session(
        payload.session_id
    )

    prepare_input_dir(
        payload.session_id
    )

    result = run_reconciliation(
        payload.config_name
    )

    job_id = f"job_{uuid4().hex[:8]}"

    update_session(

        payload.session_id,

        config=payload.config_name,

        job_id=job_id,

        status="completed",

        report_path=result["output"]
    )

    return {

        "status": "success",

        "job_id": job_id,

        "rows_with_diff":
            result["rows"],

        "report_file":
            Path(result["output"]).name
    }