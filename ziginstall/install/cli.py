import sys

import click
from colorama import Style, Fore

import ziginstall.install._install_steps as steps
from ziginstall._locations import bin_directory_path


def _delete_last_line( debug: bool ):
    if debug:
        return
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')


@click.command()
@click.option("--version", "-v", help="The version of Zig to install.", type=str, default=None)
@click.pass_context
def install( ctx, version: str | None ):
    """
    Install Zig.

    Use -v or --version to specify a version.
    """

    debug = ctx.obj["DEBUG"]

    click.echo("[ ] Pre-install checks")
    components = steps._one_pre_install(version)
    if components:
        _delete_last_line(debug)
        click.confirm(f"Pre-install checks are complete. Install version {components.version}?", abort=True)
        _delete_last_line(debug)

    click.echo("[x] Pre-install checks")

    click.echo("[ ] Downloading Zig")
    step2 = steps._two_download_zig(components)
    if step2:
        _delete_last_line(debug)
        click.echo("[x] Downloading Zig")
    else:
        _delete_last_line(debug)
        click.echo("Failed to download Zig.")
        return

    click.echo("[ ] Validating SHA-256 checksum")
    step3 = steps._three_validate_shasum(components)
    if step3:
        _delete_last_line(debug)
        click.echo("[x] Validating SHA-256 checksum")
    else:
        _delete_last_line(debug)
        click.echo("Failed to validate SHA-256 checksum.")
        return

    click.echo("[ ] Extracting Zig")
    step4 = steps._four_extract_zig(components)
    if step4:
        _delete_last_line(debug)
        click.echo("[x] Extracting Zig")
    else:
        _delete_last_line(debug)
        click.echo("Failed to extract Zig.")
        return

    click.echo("[ ] Post-install checks")
    step5 = steps._five_post_install(components)
    if step5:
        _delete_last_line(debug)
        click.echo("[x] Post-install checks")
    else:
        _delete_last_line(debug)
        click.echo("Failed post-install checks.")
        return

    click.echo(f"Installation complete. If you have not done so, add {Fore.CYAN}{Style.BRIGHT}{bin_directory_path}{Fore.RESET} to your PATH to let ZigInstall control your Zig version.")
