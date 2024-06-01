import os

from ziginstall._locations import used_file_path, install_directories_path


def get_zig_version_in_use():
    with open(used_file_path, "r") as f:
        return f.read().strip()


def get_installed_zig_versions():
    return os.listdir(install_directories_path)
