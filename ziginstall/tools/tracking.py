import json
import os

from platformdirs import *

from ziginstall._logging import log


def data_dir() -> str:
    ddir = user_data_dir(appname='ZigInstall', appauthor='Charles Dupont', ensure_exists=True)
    if not os.path.exists(os.path.join(ddir, "install_locations.json")):
        with open(os.path.join(ddir, "install_locations.json"), "w") as f:
            json.dump({ "paths": [] }, f)
    return ddir


def add_install_location( install_path: str ):
    with open(os.path.join(data_dir(), "install_locations.json"), "r+") as f:
        data = json.load(f)
        if data["paths"] is None:
            data["paths"] = []
        if install_path not in data["paths"]:
            log.debug(f"Adding install location {install_path} to tracking...")
            data["paths"].append(install_path)

            f.seek(0)
            json.dump(data, f)
            f.truncate()
        else:
            log.debug(f"Install location {install_path} already tracked.")


def remove_install_location( install_path: str ):
    with open(os.path.join(data_dir(), "install_locations.json"), "r+") as f:
        data = json.load(f)
        if data["paths"] is None:
            data["paths"] = []
        if install_path in data["paths"]:
            log.debug(f"Removing install location {install_path} from tracking...")
            data["paths"].remove(install_path)

            f.seek(0)
            json.dump(data, f)
            f.truncate()
        else:
            log.debug(f"Install location {install_path} not found in tracking.")


def list_install_locations() -> list[str]:
    with open(os.path.join(data_dir(), "install_locations.json"), "r") as f:
        data = json.load(f)
        return data["paths"]
