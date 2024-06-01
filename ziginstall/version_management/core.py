import os
import shutil
import subprocess

from ziginstall._locations import bin_directory_path
from ziginstall._logging import log


def get_zig_install_location() -> str | None:
    path = shutil.which("zig")

    if path and os.access(path, os.X_OK):
        return path
    else:
        log.debug(f"Error fetching install location.")
        return None


def get_zig_install_directory() -> str | None:
    path = get_zig_install_location()

    if path:
        return os.path.dirname(path)
    else:
        log.debug(f"Error fetching install directory.")
        return None


def get_installed_zig_version() -> str | None:
    try:
        result = subprocess.run(["zig", "version"], capture_output=True, text=True)
        return result.stdout.strip()
    except FileNotFoundError:
        log.debug(f"Error fetching installed version: Zig is not installed and in PATH.")
        return None


def verify_zig_path() -> bool:
    zig_path = get_zig_install_directory()

    bin_path = bin_directory_path()

    return zig_path == bin_path
