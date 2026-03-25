from fastapi import FastAPI
from app.reconcile_service import run_reconciliation

app = FastAPI(title="Excel Recon Engine")


@app.post("/reconcile/{config_name}")
def reconcile(config_name: str):

    result = run_reconciliation(config_name)

    return result