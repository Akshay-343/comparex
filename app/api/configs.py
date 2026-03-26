from fastapi import APIRouter
from pathlib import Path

from app.core.settings import CONFIG_DIR
from app.config_loader import load_config


router = APIRouter()


@router.get("/api/configs")
def list_configs():

    configs = []

    for file in CONFIG_DIR.glob("*.yaml"):

        name = file.stem

        cfg = load_config(name)

        configs.append({

            "name": name,

            "label": cfg.get("label"),

            "left_dataset":
                cfg.get("datasets", {})
                   .get("left", {})
                   .get("name"),

            "right_dataset":
                cfg.get("datasets", {})
                   .get("right", {})
                   .get("name"),

            "join_keys":
                cfg.get("join", {})
                   .get("keys")
        })

    return configs


@router.get("/api/configs/{config_name}")
def get_config_details(config_name: str):

    cfg = load_config(config_name)

    columns = []

    for col, meta in cfg.get("columns", {}).items():

        columns.append({

            "name": col,

            "type": meta.get("type"),

            "tolerance": meta.get("tolerance"),

            "highlight": meta.get("highlight")

        })

    return {

        "config_name": config_name,

        "datasets": cfg.get("datasets"),

        "join_keys":
            cfg.get("join", {})
               .get("keys"),

        "columns": columns
    }