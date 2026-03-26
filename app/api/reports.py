from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pathlib import Path
import json

from app.services.session_store import load_session
from app.reconcile_service import build_summary
import pandas as pd


router = APIRouter()


def _get_session_by_job(job_id: str):

    from app.core.settings import SESSION_DIR

    for f in SESSION_DIR.glob("*.json"):

        with open(f) as fp:

            data = json.load(fp)

            if data.get("job_id") == job_id:

                return data

    raise Exception(f"JOB_NOT_FOUND: {job_id}")


@router.get("/api/reports/{job_id}")
def download_report(job_id: str):

    session = _get_session_by_job(job_id)

    path = Path(session["report_path"])

    if not path.exists():

        raise Exception(
            f"REPORT_NOT_FOUND: {job_id}"
        )

    return StreamingResponse(

        open(path, "rb"),

        media_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

        headers={
            "Content-Disposition":
            f"attachment; filename={path.name}"
        }
    )


@router.get("/api/reports/{job_id}/summary")
def get_summary(job_id: str):

    session = _get_session_by_job(job_id)

    path = Path(session["report_path"])

    if not path.exists():

        raise Exception(
            f"REPORT_NOT_FOUND: {job_id}"
        )

    df_detail = pd.read_excel(

        path,

        sheet_name="DETAIL"
    )

    df_summary = pd.read_excel(

        path,

        sheet_name="SUMMARY"
    )

    matched = df_summary[
        df_summary["Metric"] == "Matched"
    ]["Value"].values[0]

    missing = df_summary[
        df_summary["Section"]
        .str.contains("Missing")
    ].shape[0]

    extra = df_summary[
        df_summary["Section"]
        .str.contains("Extra")
    ].shape[0]

    diff_distribution = {}

    for _, row in df_summary.iterrows():

        if "distribution" in row["Section"]:

            col = row["Section"].replace(
                " distribution",
                ""
            )

            diff_distribution.setdefault(
                col,
                {}
            )

            diff_distribution[col][
                str(row["Metric"])
            ] = int(row["Value"])


    return {

        "matched": int(matched),

        "missing_in_right": int(missing),

        "extra_in_right": int(extra),

        "diff_distribution": diff_distribution
    }