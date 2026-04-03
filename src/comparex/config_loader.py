import yaml
from pathlib import Path


def load_config(config_name):

    path = Path(f"configs/{config_name}.yaml")

    if not path.exists():

        raise Exception(f"Config not found: {config_name}")

    with open(path) as f:

        return yaml.safe_load(f)