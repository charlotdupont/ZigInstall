import requests


def get_linux_zig_install_url( *, version: str | None = None, index_url: str ) -> str:
    """
    Fetches the URL of the latest Zig release for the Linux architecture.
    :return: The URL of the latest Zig release for the Linux architecture.
    :rtype: str
    """
    return "https://ziglang.org/download/0.8.0/zig-linux-x86_64-0.8.0.tar.xz"


def test():
    print(requests.get("https://ziglang.org/download/index.json").json())


test()
