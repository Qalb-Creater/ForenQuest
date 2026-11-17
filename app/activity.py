
from .database import get_db


def log_activity(student_id, action, details="", case_id=None):
    """
    Save one student activity in the database.
    """

    if not student_id or not action:
        return

    db = get_db()

    db.execute(
        """
        INSERT INTO activity_logs (
            student_id,
            action,
            details,
            case_id
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            str(student_id),
            action,
            details,
            case_id
        )
    )

    db.commit()


def get_recent_activities(student_id, limit=20):
    """
    Retrieve the most recent activities for one student.
    """

    db = get_db()

    activities = db.execute(
        """
        SELECT
            id,
            action,
            details,
            case_id,
            created_at
        FROM activity_logs
        WHERE student_id = ?
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (str(student_id), limit)
    ).fetchall()

    return activities
