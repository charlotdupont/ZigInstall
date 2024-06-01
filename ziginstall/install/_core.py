import platform

import requests

from ziginstall._logging import log

ZIG_JSON_INDEX_URL = "https://ziglang.org/download/index.json"


class ZigVersionComponents:
    """
    Represents the components of a Zig version for the purposes of installing it.
    """

    def __init__( self, url: str, shasum: str, version: str ):
        self.url = url

        self.shasum = shasum

        self.version = version

        self.filename = self._get_file_name(url)

        log.debug(f"Filename {self.filename}")

    @staticmethod
    def _get_file_name( url: str ):
        if "dev" in url:
            splits = url.split("-")
            a = len(splits) - 2
            return splits[a] + "-" + splits[-1]
        else:
            return url.split("-")[-1]


def _find_zig_version_components( target_version: str | None = None ) -> ZigVersionComponents | None:
    """
    Finds the components of a Zig version for the purposes of installing it.
    :param target_version: The version of Zig to find the components for.
    :type target_version: str | None
    :return: The components of the Zig version, or None if an error occurred.
    :rtype: ZigVersionComponents | None
    """
    version_id = f"{platform.machine()}-{platform.system().lower()}"

    try:
        response = requests.get(ZIG_JSON_INDEX_URL)
        response.raise_for_status()
        load = response.json()

        url = None
        shasum = None
        version = None

        if target_version is None:
            version = load["master"]["version"]
            url = load["master"][version_id]["tarball"]
            shasum = load["master"][version_id]["shasum"]
        elif target_version in load:
            version = target_version
            url = load[version][version_id]["tarball"]
            shasum = load[version][version_id]["shasum"]
        else:
            log.error(f"Version {target_version} not found.")
            return None

        return ZigVersionComponents(url, shasum, version)
    except requests.RequestException as e:
        log.error(f"Error fetching version components: {e}")
        return None
