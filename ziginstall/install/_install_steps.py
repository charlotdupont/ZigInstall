import atexit
import os
import shutil
import tarfile
from zipfile import ZipFile

import click
import requests

from ziginstall._locations import tmp_directory_path, install_directories_path, used_file_path, bin_directory_path
from ziginstall._logging import log
from ziginstall.install._core import ZigVersionComponents, _find_zig_version_components
from ziginstall.install._verification import validate_shasum


def __do_cleanup():
    if os.path.exists(tmp_directory_path):
        shutil.rmtree(tmp_directory_path)


def _one_pre_install( version: str | None ) -> ZigVersionComponents | None:
    atexit.register(__do_cleanup)

    os.makedirs(tmp_directory_path, exist_ok=True)
    os.makedirs(install_directories_path, exist_ok=True)
    os.makedirs(bin_directory_path, exist_ok=True)

    components = _find_zig_version_components(version)

    if components.version in os.listdir(install_directories_path):
        log.debug(f"Version {components.version} already installed.")
        click.confirm(f"Version {components.version} is already installed. Do you want to reinstall it?", abort=True)

    if components is None:
        return None

    return components


def _two_download_zig( components: ZigVersionComponents ) -> bool:
    with requests.get(components.url, stream=True) as response:
        if response.status_code != 200:
            log.error(f"Failed to download from {components.url}: {response.status_code}")
            return False

        with open(os.path.join(tmp_directory_path, components.filename), "wb") as f:
            for data in response.iter_content(chunk_size=8192):
                f.write(data)

    return True


def _three_validate_shasum( components: ZigVersionComponents ) -> bool:
    log.debug(f"Validating SHA-256 checksum for {components.filename} in {tmp_directory_path}")
    log.debug(os.listdir(tmp_directory_path))
    path = os.path.join(tmp_directory_path, components.filename)
    return validate_shasum(path, components.shasum)


def _four_extract_zig( components: ZigVersionComponents ) -> bool:
    filepath = str(os.path.join(tmp_directory_path, components.filename))

    if not components.filename.endswith((".zip", ".tar.xz")):
        log.error(f"Unsupported file type: {components.filename}")
        return False

    if components.version in os.listdir(install_directories_path):
        shutil.rmtree(os.path.join(install_directories_path, components.version))

    if components.filename.endswith(".zip"):
        with ZipFile(filepath, "r") as zip_ref:
            zip_ref.extractall(install_directories_path)
    else:
        with tarfile.open(filepath, "r:xz") as tar_ref:
            tar_ref.extractall(install_directories_path)

    return True


def _five_post_install( components: ZigVersionComponents ) -> bool:
    # Rename all directories to only be the version number
    for directory in os.listdir(install_directories_path):
        if directory.startswith("zig-"):
            path = os.path.join(install_directories_path, directory)
            version = None
            if "dev" in directory:
                splits = directory.split("-")
                a = len(splits) - 2
                version = splits[a] + "-" + splits[-1]
            else:
                version = directory.split("-")[-1]
            shutil.move(path, os.path.join(install_directories_path, version))

    if not os.path.exists(used_file_path):
        log.debug(f"Creating {used_file_path}")
        with open(used_file_path, "w") as f:
            f.write(components.version)
            try:
                os.remove(os.path.join(install_directories_path, "zig"))
            except FileNotFoundError:
                pass
            os.symlink(os.path.join(install_directories_path, components.version, "zig"), bin_directory_path)

    __do_cleanup()

    return True
