import atexit
import os
import shutil
import tarfile
from zipfile import ZipFile

import click
import requests
from colorama import Fore, Style

from ziginstall._logging import log
from ziginstall.tools.core import ZigVersionComponents
from ziginstall.tools.tracking import add_install_location


def _cleanup( tmp_dir: str ):
    log.debug("Cleaning up temporary files...")
    if os.path.exists(os.path.join(tmp_dir)):
        shutil.rmtree(os.path.join(tmp_dir))


def install_zig( install_path: str, components: ZigVersionComponents ):
    # TODO: Verify signature

    complete_install_path = os.path.join(install_path,
                                         f"zig-{components.os.lower()}-{components.arch.lower()}-{components.version}"
                                         )

    if os.path.exists(complete_install_path):
        log.debug(f"Found existing installation at {complete_install_path}")
        click.confirm(f"An existing installation of Zig was found at {complete_install_path}. Do you want to remove it?",
                      abort=True
                      )
        log.debug("Cleaning up existing installation...")
        shutil.rmtree(complete_install_path)

    tmp_dir = os.path.join(install_path, "tmp")
    os.makedirs(tmp_dir, exist_ok=True)

    atexit.register(lambda: _cleanup(tmp_dir))

    filename = components.url.split("/")[-1]
    if not filename.endswith((".zip", ".tar.xz")):
        log.error(f"Unsupported file type: {filename}")
        exit(1)

    filepath = os.path.join(tmp_dir, filename)

    log.debug(f"Downloading {filename}...")
    with requests.get(components.url, stream=True) as response:
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            log.error(f"Failed to download {filename}: {e}")
            exit(1)

        total_size = int(response.headers.get("content-length", 0))

        with open(filepath, "wb") as f, click.progressbar(length=total_size, label=f"Downloading {filename}") as bar:
            for data in response.iter_content(chunk_size=8192):
                f.write(data)
                bar.update(len(data))

    log.debug(f"Extracting {filename}...")

    if filename.endswith(".zip"):
        with ZipFile(filepath, "r") as zip_ref:
            members = zip_ref.infolist()
            with click.progressbar(label=f"Extracting {filename}", length=len(members)) as bar:
                for i, member in enumerate(members):
                    zip_ref.extract(member, install_path)
                    bar.update(i)
    elif filename.endswith(".tar.xz"):
        with tarfile.open(filepath, "r:xz") as tar_ref:
            members = tar_ref.getmembers()
            with click.progressbar(label=f"Extracting {filename}", length=len(members)) as bar:
                for i, member in enumerate(members):
                    tar_ref.extract(member, install_path)
                    bar.update(i)
    else:
        log.error(f"Unsupported file type: {filename}")
        exit(1)

    log.debug(f"Cleaning up temporary files...")

    add_install_location(install_path)

    click.echo(f"\nInstalled Zig: {Fore.CYAN}{components.version}{Fore.RESET} for {Fore.CYAN}{components.arch}-{components.os}{Style.RESET_ALL} at {Fore.MAGENTA}{complete_install_path}{Style.RESET_ALL}")
    click.echo(f"\n{Fore.CYAN}{Style.BRIGHT}Installation complete! Don't forget to add Zig to your path!{Style.RESET_ALL}\n")
