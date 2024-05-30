import os

import click
from colorama import Fore, Style
from platformdirs import *

from ziginstall._logging import init_logging, log
from ziginstall.tools.core import get_latest_zig_version, get_installed_zig_version, find_zig_version_components
from ziginstall.tools.install import install_zig
from ziginstall.tools.tracking import list_install_locations


@click.group(name="ziginstall")
@click.option("--debug",
              help="Whether to show debug and info log messages.",
              is_flag=True
              )
def zig_install( debug: bool ):
    """
    ZigInstall: A simple tool to install Zig.

    To see help about a specific commands run `ziginstall COMMAND --help`.
    """
    init_logging(debug)
    log.debug(f"Debug mode : {debug}")


@zig_install.command()
@click.option("--install-path", "-p",
              help="The path to install Zig to.",
              type=str,
              default=None
              )
@click.option("--target-version", "-v",
              help="The version of Zig to install. Default is master.",
              type=str,
              )
def install( target_version: str | None, install_path: str | None = None, ):
    """
    Installs Zig.

    > If no install path is provided, the default user data path is used.

    > If no target version is provided, the latest master version is used. Be aware that the master version may be unstable.
    """
    components = find_zig_version_components(target_version)

    log.debug("Preparing to install Zig...", extra={ "components": components })

    click.echo(f"\n{Style.BRIGHT}Installing Zig:{Style.RESET_ALL} {Fore.CYAN}{components.version}{Style.RESET_ALL} for {Fore.CYAN}{components.os}{Style.RESET_ALL} {Fore.CYAN}{components.arch}{Style.RESET_ALL}\n")

    if install_path is None:
        install_path = user_data_dir(appname='ZigInstall', appauthor='Charles Dupont')
        log.warn(f"No install path provided, using default: {install_path}")
    click.confirm("Confirm installation?", abort=True)
    install_zig(install_path, components)


@zig_install.command()
def list():
    """
    Lists all tracked Zig installations.

    Does not track installations that were not installed with ZigInstall.
    """

    install_directories = list_install_locations()
    click.echo()
    click.echo(f"{Fore.CYAN}{Style.BRIGHT}Tracked Installations:{Style.RESET_ALL}")
    for index, directory in enumerate(install_directories):
        click.echo(f"[{index}] {Fore.MAGENTA}{directory}{Style.RESET_ALL}")

        for entry in os.scandir(directory):
            if entry.is_dir():
                parts = entry.name.split("-")
                version_name = None
                if len(parts) == 5:
                    version_name = f"[dev] {parts[3]} - {parts[4]}"
                if len(parts) == 4:
                    version_name = f"[rel] {parts[3]}"
                click.echo(f"    {version_name}")


@zig_install.command()
def version():
    """
    Version information about installed and latest Zig versions.
    """
    click.echo(f"{Fore.CYAN}{Style.BRIGHT}Installed Zig Version: {Style.RESET_ALL}{Fore.MAGENTA}{get_installed_zig_version()}{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{Style.BRIGHT}Latest Zig Release Version: {Style.RESET_ALL}{Fore.MAGENTA}{get_latest_zig_version()[1]}{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{Style.BRIGHT}Latest Zig Master Version: {Style.RESET_ALL}{Fore.MAGENTA}{get_latest_zig_version()[0]}{Style.RESET_ALL}")
