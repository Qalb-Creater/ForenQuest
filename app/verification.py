
import hashlib


def calculate_sha256(file_stream):
    """
    Calculate SHA-256 hash of an uploaded file.
    Reads the file in chunks to handle larger evidence files.
    """

    sha256_hash = hashlib.sha256()

    while True:
        chunk = file_stream.read(4096)

        if not chunk:
            break

        sha256_hash.update(chunk)

    return sha256_hash.hexdigest()


def verify_sha256(calculated_hash, reference_hash):
    """
    Compare calculated hash with the reference hash.
    """

    calculated_hash = calculated_hash.strip().lower()
    reference_hash = reference_hash.strip().lower()

    return calculated_hash == reference_hash
