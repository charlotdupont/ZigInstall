import platform
import re
import subprocess

import requests
from packaging import version as versioning

from ziginstall._logging import log

ZIG_JSON_INDEX_URL = "https://ziglang.org/download/index.json"


class ZigVersionComponents:
    def __init__( self, arch: str, os: str, url: str, shasum: str, size: int, version: str ):
        self.arch = arch
        self.os = os
        self.url = url
        self.shasum = shasum
        self.size = size
        self.version = version


def _get_os() -> str:
    """
    Fetches the operating system of the current system.
    :return: The operating system of the current system. Empty string if the OS is unknown.
    :rtype: str
    """
    return platform.system()


def get_installed_zig_version() -> str | None:
    """
    Fetches the installed version of Zig.
    :return: The installed version of Zig, or None if an error occurred.
    :rtype: str | None
    """
    try:
        result = subprocess.run(["zig", "version"], capture_output=True, text=True)
        return result.stdout.strip()
    except FileNotFoundError as e:
        log.debug(f"Error fetching installed version: Zig is not installed and in PATH.", extra={ "error": e })
        return None


def get_latest_zig_version() -> tuple[str, str] | None:
    """
    Fetches the latest version of Zig from the official website.
    :return: The latest version of Zig, or None if an error occurred.
    :rtype: str | None
    """
    try:
        response = requests.get(ZIG_JSON_INDEX_URL)
        response.raise_for_status()
        load = response.json()

        master_version = load["master"]["version"]

        versions = [v for v in load if re.match(r"\d+\.\d+\.\d+", v)]

        most_recent = max(versions, key=versioning.parse)

        return str(master_version), most_recent
    except requests.RequestException as e:
        log.error(f"Error fetching latest version: {e}")
        exit(1)


def _versions_by_os( versions: list[str] ) -> dict[str, list[str]]:
    """
    Seperates the versions by operating system.
    :param versions: The versions to seperate.
    :type versions: list[str]
    :return: The versions seperated by operating system.
    :rtype: dict[str, list[str]]
    """
    seperated = { "other": [] }
    for version in versions:
        arch = None
        os = None
        if '-' in version:
            (arch, os) = version.split('-')
        else:
            seperated["other"].append(version)
        if os and os not in seperated:
            seperated[os] = []
        if os and arch:
            seperated[os].append(arch)
    return seperated


def _is_valid_version( version: str ) -> bool:
    if version == "master":
        return True

    parts = version.split(".")
    if len(parts) != 3:
        return False

    try:
        [int(part) for part in parts]
    except ValueError:
        return False

    return True


def find_zig_version_components( target_version: str = "master" ) -> ZigVersionComponents | None:
    if target_version is None:  # Click assigns None, overriding the default value.
        target_version = "master"

    os = _get_os()
    arch = platform.machine()
    log.debug(f"Operating system: {os}, architecture: {arch}")

    # Check if the version is valid.
    if not _is_valid_version(target_version):
        log.error(f"Invalid version: {target_version}")
        exit(1)

    response = requests.get(ZIG_JSON_INDEX_URL)
    load = response.json()

    try:
        response.raise_for_status()
    except requests.RequestException as e:
        log.error(f"Error fetching latest version: {e}")
        exit(1)

    flavors = None

    try:
        flavors = [key for key, value in load[target_version].items() if isinstance(value, dict)]
    except KeyError:
        log.error(f"Unsupported version: {target_version}")
        exit(1)

    seperated_versions = _versions_by_os(flavors)

    if not os.lower() in seperated_versions:
        log.error(f"Unsupported operating system: {os}")
        return None
    if arch not in seperated_versions[os.lower()]:
        log.error(f"Unsupported architecture: {arch}")
        return None

    version_id = f"{arch}-{os.lower()}"

    output_version = target_version
    if target_version == "master":
        output_version = load["master"]["version"]

    return ZigVersionComponents(
            arch=arch,
            os=os,
            url=load[target_version][version_id]["tarball"],
            shasum=load[target_version][version_id]["shasum"],
            size=load[target_version][version_id]["size"],
            version=output_version,
            )
