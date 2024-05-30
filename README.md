# Zig Install
<<<<<<< HEAD
[![PyPI](https://github.com/charlotdupont/ZigInstall/actions/workflows/python-publish.yml/badge.svg)](https://github.com/charlotdupont/ZigInstall/actions/workflows/python-publish.yml)
=======

[![PyPI](https://github.com/charlotdupont/ZigInstall/actions/workflows/python-publish.yml/badge.svg?branch=master&event=deployment)](https://github.com/charlotdupont/ZigInstall/actions/workflows/python-publish.yml)
>>>>>>> a3181a5 (Changed TODO)

Personal project to install Zig.

**Should work on all systems, but only tested on Ubuntu 20.04.**

**Note**: This project is not affiliated with the official Zig project.

## Usage

- run ```ziginstall``` to see available commands.
- run ```ziginstall install``` to install Zig.
    - You can specify the version to install by running ```ziginstall install -v <version>```.
    - You can specify the installation directory by running ```ziginstall install -d <directory>```.
      ull

## TODO

- Uninstall functionality.
- Add to path functionality.
- Check which versions are installed to avoid installing the same version in two different places.
- CLI tool to choose the version used and control which Zig exec it points to.
