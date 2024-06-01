import click

from ziginstall._logging import init_logging, log
from ziginstall.install.cli import install
from ziginstall.version_management.cli import list, use, uninstall


@click.group(name="ziginstall")
@click.option("--debug",
              help="Whether to show debug and info log messages.",
              is_flag=True
              )
@click.pass_context
def zig_install( ctx, debug: bool ):
    """
    ZigInstall: A simple tool to install Zig.

    To see help about a specific commands run `ziginstall COMMAND --help`.
    """
    ctx.obj = { "DEBUG": debug }
    init_logging(debug)
    log.debug(f"Debug mode : {debug}")


zig_install.add_command(install)
zig_install.add_command(list)
zig_install.add_command(use)
zig_install.add_command(uninstall)
