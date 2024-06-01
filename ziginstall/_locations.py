import os

from platformdirs import PlatformDirs

_platforms = PlatformDirs(appname="ZigInstall", appauthor="Charles Dupont", ensure_exists=True)

install_directories_path = os.path.join(_platforms.user_data_dir, "installations")
bin_directory_path = os.path.join(_platforms.user_data_dir, "zig-bin")
used_file_path = os.path.join(_platforms.user_data_dir, "used")
tmp_directory_path = os.path.join(_platforms.user_data_dir, "tmp")
