import hashlib


def validate_shasum( filename: str, shasum: str ) -> bool:
    """
    Validate the SHA256 sum of a file.
    :param filename: The file to validate.
    :type filename: str
    :param shasum: The expected SHA256 sum.
    :type shasum: str
    :return: Whether the SHA256 sum is valid.
    """
    with open(filename, "rb") as f:
        sha = hashlib.sha256()
        while chunk := f.read(8192):
            sha.update(chunk)

    return sha.hexdigest() == shasum
