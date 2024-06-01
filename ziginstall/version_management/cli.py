import os
import shutil

import click
from rich.console import Console
from rich.table import Table

from ziginstall._locations import used_file_path, bin_directory_path
from ziginstall._logging import log
from ziginstall.version_management.core import (get_installed_zig_versions, get_zig_version_in_use,
                                                install_directories_path)


@click.command()
def list():
    """List all installed versions of Zig."""
    installed = get_installed_zig_versions()
    in_use = get_zig_version_in_use()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Version")
    table.add_column("Status")

    for version in installed:
        status = f"[green]Used[/green]" if version == in_use else "[yellow]Installed[/yellow]"
        table.add_row(version, status)

    console = Console()
    console.print(table)


@click.command()
@click.argument("version")
def use( version: str ):
    """Use a specific version of Zig."""
    installed = get_installed_zig_versions()
    if version not in installed:
        click.echo(f"Version {version} is not installed.")
        return
    try:
        os.remove(os.path.join(bin_directory_path, "zig"))
    except FileNotFoundError:
        log.debug("No binary found.")

    os.symlink(os.path.join(install_directories_path, version, "zig"), os.path.join(bin_directory_path, "zig"))

    with open(used_file_path, "w") as f:
        f.write(version)

    click.echo(f"Version {version} is now in use.")


@click.command()
@click.argument("version")
def uninstall( version: str ):
    """Uninstall a specific version of Zig."""
    installed = get_installed_zig_versions()
    if version not in installed:
        click.echo(f"Version {version} is not installed.")
        return

    if version == get_zig_version_in_use():
        click.echo(f"Version {version} is currently in use. Please use another version before uninstalling.")
        return

    click.confirm(f"Are you sure you want to uninstall version {version}?", abort=True)
    shutil.rmtree(os.path.join(install_directories_path, version))

    click.echo(f"Version {version} has been uninstalled.")
