
import pytest

from app import create_app
from app.custody import (
    record_custody_event,
    get_custody_history,
    verify_custody_record
)


@pytest.fixture
def app(tmp_path):
    database_file = tmp_path / "test_forenquest.db"

    test_app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret-key",
        "DATABASE": str(database_file)
    })

    yield test_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_custody_event_creation(app):
    with app.app_context():

        record_custody_event(
            student_id="student-1",
            evidence_id="evidence-001",
            case_id="deleted-files",
            action="Evidence Downloaded",
            details="Downloaded test dataset"
        )

        records = get_custody_history("student-1")

        assert len(records) == 1
        assert records[0]["evidence_id"] == "evidence-001"


def test_custody_hash_generation(app):
    with app.app_context():

        record_custody_event(
            student_id="student-1",
            evidence_id="evidence-001",
            action="Evidence Downloaded",
            details="Integrity test"
        )

        records = get_custody_history("student-1")

        assert records[0]["record_hash"]
        assert len(records[0]["record_hash"]) == 64


def test_custody_integrity_verification(app):
    with app.app_context():

        record_custody_event(
            student_id="student-1",
            evidence_id="evidence-001",
            action="Evidence Downloaded",
            details="Verification test"
        )

        records = get_custody_history("student-1")

        assert verify_custody_record(records[0]) is True


def test_modified_record_fails_verification(app):
    with app.app_context():

        record_custody_event(
            student_id="student-1",
            evidence_id="evidence-001",
            action="Evidence Downloaded",
            details="Original details"
        )

        records = get_custody_history("student-1")

        modified_record = dict(records[0])
        modified_record["details"] = "Modified details"

        assert verify_custody_record(modified_record) is False


def test_students_only_see_their_own_records(app):
    with app.app_context():

        record_custody_event(
            student_id="student-1",
            evidence_id="evidence-001",
            action="Evidence Downloaded"
        )

        record_custody_event(
            student_id="student-2",
            evidence_id="evidence-002",
            action="Evidence Downloaded"
        )

        student_one_records = get_custody_history("student-1")
        student_two_records = get_custody_history("student-2")

        assert len(student_one_records) == 1
        assert student_one_records[0]["student_id"] == "student-1"

        assert len(student_two_records) == 1
        assert student_two_records[0]["student_id"] == "student-2"
