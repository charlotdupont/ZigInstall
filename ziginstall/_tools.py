import platform
import subprocess

import requests

from ziginstall._linux import get_linux_zig_version_name
from ziginstall._logging import log

ZIG_VERSION_URL = "https://ziglang.org/download/index.json"


def get_latest_version() -> str | None:
    """
    Fetches the latest version of Zig from the official website.
    :return: The latest version of Zig, or None if an error occurred.
    :rtype: str | None
    """
    try:
        response = requests.get(ZIG_VERSION_URL)
        response.raise_for_status()
        return response.json()["master"]["version"]
    except requests.RequestException as e:
        log.error(f"Error fetching latest version: {e}")
        return None


def get_installed_version() -> str | None:
    """
    Fetches the installed version of Zig.
    :return: The installed version of Zig, or None if an error occurred.
    :rtype: str | None
    """
    try:
        result = subprocess.run(["zig", "version"], capture_output=True, text=True)
        return result.stdout.strip()
    except FileNotFoundError as e:
        log.error(f"Error fetching installed version: Zig is not installed and in PATH.", extra={ "error": e })
        return None


def get_os() -> str:
    """
    Fetches the operating system of the current system.
    :return: The operating system of the current system. Empty string if the OS is unknown.
    :rtype: str
    """
    return platform.system()


def find_correct_install() -> str:
    os = get_os()
    log.debug(f"Operating system: {os}")
    match os:
        case "Linux":
            get_linux_zig_version_name()
        case _:
            log.error(f"Unsupported operating system: {os}")
            return ""
