import tarfile
from enum import Enum, auto

import click
import requests
from platformdirs import *
from tqdm import tqdm

from ziginstall._global import log


class FileType(Enum):
    TAR_XZ = auto()
    ZIP = auto()


def get_file_type( filename: str ) -> FileType:
    if filename.endswith(".tar.xz"):
        return FileType.TAR_XZ
    elif filename.endswith(".zip"):
        return FileType.ZIP
    else:
        raise ValueError(f"Unsupported file type: {filename}")


def install_tar_xz( tarball_url: str, install_path: str, tmp_path: str, filename: str ) -> None:
    response = None
    try:
        response = requests.get(tarball_url)
        response.raise_for_status()
    except requests.RequestException as e:
        log.error(f"Error fetching tarball: {e}")
        return

    total_size = int(response.headers.get("content-length", 0))
    with open(tmp_path, "wb") as f, tqdm(desc=filename,
                                         total=total_size,
                                         unit="iB",
                                         unit_scale=True,
                                         unit_divisor=1024
                                         ) as bar:
        for data in response.iter_content(chunk_size=1024):
            f.write(data)
            bar.update(len(data))

    with tarfile.open(tmp_path, "r:xz") as tar:
        members = tar.getmembers()
        with click.progressbar(members, label="Extracting", show_eta=False) as bar:
            for member in bar:
                tar.extract(member, install_path)


"""
Check if click or tqdm works better, uninstall tdqm if not needed.
Add consent for install + other steps.
Finish setting everything up.
"""


def install_zig( url: str, install_path: str ) -> None:
    log.debug(f"Installing Zig from {url} in {install_path}")

    filename = url.split("/")[-1]
    tmp_path = user_downloads_path() / filename

    file_type = get_file_type(filename)

    if file_type == FileType.TAR_XZ:
        install_tar_xz(url, install_path, str(tmp_path), filename)
