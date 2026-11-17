
import hashlib
import json

from .database import get_db


def calculate_custody_hash(
    student_id,
    evidence_id,
    case_id,
    action,
    details,
    created_at
):
    record_data = {
        "student_id": str(student_id),
        "evidence_id": evidence_id,
        "case_id": case_id,
        "action": action,
        "details": details or "",
        "created_at": created_at
    }

    serialized = json.dumps(
        record_data,
        sort_keys=True,
        separators=(",", ":")
    )

    return hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()


def record_custody_event(
    student_id,
    evidence_id,
    action,
    case_id=None,
    details=""
):
    if not student_id or not evidence_id or not action:
        return

    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO evidence_custody (
            student_id,
            evidence_id,
            case_id,
            action,
            details
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            str(student_id),
            evidence_id,
            case_id,
            action,
            details
        )
    )

    record = db.execute(
        """
        SELECT created_at
        FROM evidence_custody
        WHERE id = ?
        """,
        (cursor.lastrowid,)
    ).fetchone()

    record_hash = calculate_custody_hash(
        student_id,
        evidence_id,
        case_id,
        action,
        details,
        record["created_at"]
    )

    db.execute(
        """
        UPDATE evidence_custody
        SET record_hash = ?
        WHERE id = ?
        """,
        (record_hash, cursor.lastrowid)
    )

    db.commit()


def get_custody_history(student_id, limit=100):
    db = get_db()

    return db.execute(
        """
        SELECT
            id,
            student_id,
            evidence_id,
            case_id,
            action,
            details,
            created_at,
            record_hash
        FROM evidence_custody
        WHERE student_id = ?
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (str(student_id), limit)
    ).fetchall()


def verify_custody_record(record):
    expected_hash = calculate_custody_hash(
        record["student_id"],
        record["evidence_id"],
        record["case_id"],
        record["action"],
        record["details"],
        record["created_at"]
    )

    return expected_hash == record["record_hash"]
