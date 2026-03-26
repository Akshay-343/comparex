from pydantic import BaseModel
from typing import List, Dict, Optional


class UploadResponse(BaseModel):
    status: str
    session_id: str
    uploaded_files: List[str]


class ConfigListItem(BaseModel):
    name: str
    label: Optional[str]
    left_dataset: Optional[str]
    right_dataset: Optional[str]
    join_keys: Optional[List[str]]


class ConfigDetail(BaseModel):

    config_name: str

    datasets: Dict

    join_keys: List[str]

    columns: List[Dict]


class RunReconcileRequest(BaseModel):

    session_id: str

    config_name: str


class RunReconcileResponse(BaseModel):

    status: str

    job_id: str

    rows_with_diff: int

    report_file: str


class ErrorResponse(BaseModel):

    status: str = "error"

    error_code: str

    message: str