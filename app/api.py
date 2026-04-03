from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import os
import datetime
import shutil
from app.reconcile_service import run_reconciliation

router = APIRouter()

INPUT_DIR = Path("data/input")
OUTPUT_DIR = Path("data/output")
CONFIGS_DIR = Path("configs")

@router.get("/configs")
async def get_configs():
    if not CONFIGS_DIR.exists():
        return {"configs": []}
    
    # Return filenames without extensions
    configs = [p.stem for p in CONFIGS_DIR.glob("*.y*ml")]
    return {"configs": configs}

@router.post("/reconcile")
async def reconcile_api(
    file_a: UploadFile = File(...),
    file_b: UploadFile = File(...),
    config_name: str = Form(...)
):
    try:
        run_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        left_dir = INPUT_DIR / run_id / "left"
        right_dir = INPUT_DIR / run_id / "right"
        
        left_dir.mkdir(parents=True, exist_ok=True)
        right_dir.mkdir(parents=True, exist_ok=True)
        
        left_path = left_dir / file_a.filename
        right_path = right_dir / file_b.filename

        content_a = await file_a.read()
        with open(left_path, "wb") as f:
            f.write(content_a)

        content_b = await file_b.read()
        with open(right_path, "wb") as f:
            f.write(content_b)

        result = run_reconciliation(
            config_name=config_name,
            left_file_path=str(left_path),
            right_file_path=str(right_path),
            run_id=run_id
        )

        return {
            "status": "success",
            "run_id": run_id,
            "rows": result.get("rows"),
            "download_url": f"/api/download/{run_id}"
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@router.get("/download/{run_id}")
async def download_report(run_id: str):
    output_dir = OUTPUT_DIR / run_id
    if not output_dir.exists():
        return JSONResponse(status_code=404, content={"status": "error", "message": "Report not found"})
    
    files = list(output_dir.glob("*.xlsx"))
    if not files:
        return JSONResponse(status_code=404, content={"status": "error", "message": "Report file not found"})
    
    return FileResponse(
        path=str(files[0]), 
        filename=files[0].name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@router.delete("/clear")
async def clear_files():
    try:
        if INPUT_DIR.exists():
            for item in INPUT_DIR.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                    
        if OUTPUT_DIR.exists():
            for item in OUTPUT_DIR.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                    
        return {"status": "success", "message": "Input and output files cleared"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
