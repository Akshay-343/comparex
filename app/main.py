from fastapi import FastAPI
from app.reconcile_service import run_reconciliation
from app.api import files, configs, reconcile, reports

app = FastAPI(title="Excel Recon Engine")
app.include_router(configs.router)

app.include_router(files.router)

app.include_router(reconcile.router)

app.include_router(reports.router)

@app.post("/reconcile/{config_name}")
def reconcile(config_name: str):

    result = run_reconciliation(config_name)

    return result