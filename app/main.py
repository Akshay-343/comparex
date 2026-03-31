from fastapi import FastAPI
from app.reconcile_service import run_reconciliation
import uvicorn
import os
app = FastAPI(title="Excel Recon Engine")


@app.post("/reconcile/{config_name}")
def reconcile(config_name: str):

    result = run_reconciliation(config_name)

    return result
# entrypoint for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app.main:app",   # module path changed
        host="0.0.0.0",
        port=port
    )
