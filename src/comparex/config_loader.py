import yaml
from importlib.resources import files
# import requests

def load_config(config_name: str):

    config_path = files("comparex.configs").joinpath(f"{config_name}.yaml")

    if not config_path.is_file():
        raise Exception(f"Config not found: {config_name}")

    with config_path.open("r") as f:
        return yaml.safe_load(f)
