import click

from ziginstall._global import init_logging, log


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
def install():
    """
    Installs Zig.
    """
    click.echo("Installing Zig...")
