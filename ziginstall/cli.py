import click
from colorama import Fore, Style

from ziginstall._logging import init_logging, log
from ziginstall._tools import get_installed_version
from ziginstall.tools._core import get_latest_zig_version


@click.group(name="ziginstall")
@click.option("--debug",
              help="Whether to show debug and info log messages.",
              is_flag=True
              )
def zig_install( debug: bool ):
    """
    ZigInstall: A simple tool to install Zig.
    """
    init_logging(debug)
    log.debug(f"Debug mode : {debug}")


@zig_install.command()
@click.option("--install-path",
              help="The path to install Zig to.",
              type=str
              )
def install():
    """
    Installs Zig.
    """
    log.info("Installing Zig...")


@zig_install.command()
def version():
    """
    Prints the installed version of Zig.
    """
    click.echo(f"{Fore.CYAN}{Style.BRIGHT}Installed Zig Version: {Style.RESET_ALL}{Fore.MAGENTA}{get_installed_version()}{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{Style.BRIGHT}Latest Zig Release Version: {Style.RESET_ALL}{Fore.MAGENTA}{get_latest_zig_version()[1]}{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{Style.BRIGHT}Latest Zig Master Version: {Style.RESET_ALL}{Fore.MAGENTA}{get_latest_zig_version()[0]}{Style.RESET_ALL}")
