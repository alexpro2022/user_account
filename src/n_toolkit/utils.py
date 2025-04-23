import hashlib


def sha256_hash(input_string: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(input_string.encode("utf-8"))
    return sha256.hexdigest()
