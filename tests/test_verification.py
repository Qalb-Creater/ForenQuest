
import io
import hashlib

from app.verification import calculate_sha256, verify_sha256


def test_sha256_calculation():

    evidence = b"ForenQuest evidence"

    file_stream = io.BytesIO(evidence)

    calculated_hash = calculate_sha256(file_stream)

    expected_hash = hashlib.sha256(evidence).hexdigest()

    assert calculated_hash == expected_hash


def test_sha256_verification():

    correct_hash = hashlib.sha256(
        b"ForenQuest evidence"
    ).hexdigest()

    # Matching hash
    assert verify_sha256(correct_hash, correct_hash) is True

    # Case-insensitive matching
    assert verify_sha256(correct_hash.upper(), correct_hash) is True

    # Mismatching hash
    assert verify_sha256(correct_hash, "incorrect_hash") is False
