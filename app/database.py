
import os
import sqlite3

from flask import current_app, g


def get_db():
    if "db" not in g:
        os.makedirs(current_app.instance_path, exist_ok=True)

        database_path = os.path.join(
            current_app.instance_path,
            "forenquest.db"
        )

        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(error=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db(app):
    app.teardown_appcontext(close_db)

    with app.app_context():
        db = get_db()

        # Investigations table
        db.execute("""
            CREATE TABLE IF NOT EXISTS investigations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                case_id TEXT NOT NULL,
                investigator_name TEXT,
                findings TEXT,
                evidence_notes TEXT,
                answers TEXT,
                status TEXT NOT NULL DEFAULT 'In Progress',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(student_id, case_id)
            )
        """)

        # Users table
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Activity history table
        db.execute("""
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                case_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Add status column to existing databases if needed
        columns = db.execute(
            "PRAGMA table_info(investigations)"
        ).fetchall()

        column_names = [
            column["name"] for column in columns
        ]

        if "status" not in column_names:
            db.execute("""
                ALTER TABLE investigations
                ADD COLUMN status TEXT NOT NULL DEFAULT 'In Progress'
            """)

        # Improve activity history lookup performance
        db.execute("""
            CREATE INDEX IF NOT EXISTS idx_activity_student
            ON activity_logs(student_id, created_at)
        """)

        # Evidence Chain of Custody table
        db.execute("""
            CREATE TABLE IF NOT EXISTS evidence_custody (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                evidence_id TEXT NOT NULL,
                case_id TEXT,
                action TEXT NOT NULL,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Improve custody history lookup performance
        db.execute("""
            CREATE INDEX IF NOT EXISTS idx_custody_student
            ON evidence_custody(student_id, created_at)
        """)

        # Add record_hash to existing custody databases
        custody_columns = db.execute(
            "PRAGMA table_info(evidence_custody)"
        ).fetchall()

        custody_column_names = [
            column["name"] for column in custody_columns
        ]

        if "record_hash" not in custody_column_names:
            db.execute("""
                ALTER TABLE evidence_custody
                ADD COLUMN record_hash TEXT
            """)

        db.commit()
