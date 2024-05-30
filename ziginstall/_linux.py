import platform

from ziginstall._logging import log


def get_linux_zig_version_name():
    match platform.machine():
        case "x86_64":
            return "x86_64-linux"
        case _:
            e = ValueError(f"Unsupported machine: {platform.machine()}")
            log.error(e)
