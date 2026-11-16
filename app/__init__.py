import os
import json
import uuid
from app.verification import calculate_sha256, verify_sha256
from app.reports import create_investigation_pdf
from app.auth import hash_password, verify_password
from app.evidence import EVIDENCE
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_file,
    send_from_directory,
    current_app,
    abort
)

from app.cases import CASES
from app.guides import GUIDES
from app.database import init_db, get_db


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        "dev-only-change-this-key-before-deployment"
    )

    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = False
    app.config["PERMANENT_SESSION_LIFETIME"] = 1800

    # Initialize SQLite database
    init_db(app)

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/cases")
    def case_library():
        return render_template("cases.html", cases=CASES)
    

    @app.route("/cases/<case_id>")
    def case_detail(case_id):
        selected_case = next(
            (case for case in CASES if case["id"] == case_id),
            None
        )

        if selected_case is None:
            abort(404)

        return render_template(
            "case_detail.html",
            case=selected_case
        )

    @app.route("/guides")
    def guide_library():
        return render_template("guides.html", guides=GUIDES)

    @app.route("/guides/<case_id>")
    def guide_detail(case_id):
        selected_guide = next(
            (guide for guide in GUIDES
             if guide["case_id"] == case_id),
            None
        )

        if selected_guide is None:
            abort(404)

        return render_template(
            "guide_detail.html",
            guide=selected_guide
        )
    @app.route("/evidence")
    def evidence_library():
        evidence_items = []

        for item in EVIDENCE:
            matching_case = next(
                (
                    case for case in CASES
                    if case["id"] == item["case_id"]
                ),
                None
            )

            if matching_case:
                evidence_items.append({
                    **item,
                    "case_title": matching_case["title"]
                })

        return render_template(
            "evidence_library.html",
            evidence_items=evidence_items
        )
        
    @app.route("/evidence/download/<evidence_id>")
    def download_evidence(evidence_id):

        evidence_item = next(
            (
                item for item in EVIDENCE
                if item["id"] == evidence_id
            ),
            None
        )

        if evidence_item is None:
            flash("Evidence dataset not found.")
            return redirect(url_for("evidence_library"))

        return send_from_directory(
            current_app.static_folder + "/evidence",
            evidence_item["filename"],
            as_attachment=True
        )
    # Investigation Workspace
    @app.route("/workspace/<case_id>", methods=["GET", "POST"])
    def investigation_workspace(case_id):

        selected_case = next(
            (case for case in CASES if case["id"] == case_id),
            None
        )

        selected_guide = next(
            (guide for guide in GUIDES
             if guide["case_id"] == case_id),
            None
        )

        if selected_case is None or selected_guide is None:
            abort(404)

               # Require student login
        if "user_id" not in session:
            flash("Please log in to access the investigation workspace.")
            return redirect(url_for("login"))

        # Use the logged-in student's account ID
        student_id = str(session["user_id"])

        db = get_db()

        if request.method == "POST":

            investigator_name = request.form.get(
                "investigator_name", ""
            )

            findings = request.form.get("findings", "")

            evidence_notes = request.form.get(
                "evidence_notes", ""
            )

            answers = {}

            for index, question in enumerate(
                selected_guide["questions"]
            ):
                answers[str(index)] = request.form.get(
                    f"answer_{index}", ""
                )

            db.execute("""
                INSERT INTO investigations (
                    student_id,
                    case_id,
                    investigator_name,
                    findings,
                    evidence_notes,
                    answers,
                    status,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, 'In Progress', CURRENT_TIMESTAMP)

                ON CONFLICT(student_id, case_id)
                DO UPDATE SET
                    investigator_name = excluded.investigator_name,
                    findings = excluded.findings,
                    evidence_notes = excluded.evidence_notes,
                    answers = excluded.answers,
                    status = 'In Progress',
                    updated_at = CURRENT_TIMESTAMP
            """, (
                student_id,
                case_id,
                investigator_name,
                findings,
                evidence_notes,
                json.dumps(answers)
            ))

            db.commit()

            flash("Investigation progress saved successfully!")

            return redirect(
                url_for(
                    "investigation_workspace",
                    case_id=case_id
                )
            )

        saved_record = db.execute("""
            SELECT *
            FROM investigations
            WHERE student_id = ? AND case_id = ?
        """, (student_id, case_id)).fetchone()

        saved_answers = {}

        if saved_record:
            saved_answers = json.loads(
                saved_record["answers"] or "{}"
            )

        return render_template(
            "workspace.html",
            case=selected_case,
            guide=selected_guide,
            record=saved_record,
            saved_answers=saved_answers
        )

    # Mark an investigation as completed
    @app.route("/workspace/<case_id>/complete", methods=["POST"])
    def complete_investigation(case_id):

        selected_case = next(
            (case for case in CASES if case["id"] == case_id),
            None
        )

        if selected_case is None:
            abort(404)

        if "user_id" not in session:
            flash("Please log in to update investigation status.")
            return redirect(url_for("login"))

        student_id = str(session["user_id"])

        db = get_db()

        result = db.execute("""
            UPDATE investigations
            SET status = 'Completed',
                updated_at = CURRENT_TIMESTAMP
            WHERE student_id = ? AND case_id = ?
        """, (student_id, case_id))

        db.commit()

        if result.rowcount == 0:
            flash("Save your investigation before marking it completed.")
        else:
            flash("Investigation marked as completed!")

        return redirect(
            url_for("investigation_workspace", case_id=case_id)
        )
        
    # Evidence Verification
    @app.route("/verification", methods=["GET", "POST"])
    def evidence_verification():

        calculated_hash = None
        reference_hash = ""
        verification_result = None
        filename = None
        error = None

        if request.method == "POST":

            uploaded_file = request.files.get("evidence_file")
            reference_hash = request.form.get(
                "reference_hash", ""
            ).strip()

            if not uploaded_file or not uploaded_file.filename:
                error = "Please select an evidence file."

            else:
                filename = uploaded_file.filename

                calculated_hash = calculate_sha256(
                    uploaded_file.stream
                )

                if reference_hash:
                    verification_result = verify_sha256(
                        calculated_hash,
                        reference_hash
                    )

        return render_template(
            "verification.html",
            calculated_hash=calculated_hash,
            reference_hash=reference_hash,
            verification_result=verification_result,
            filename=filename,
            error=error
        )

    # Investigation PDF Report
    @app.route("/report/<case_id>")
    def download_investigation_report(case_id):

        selected_case = next(
            (case for case in CASES if case["id"] == case_id),
            None
        )

        selected_guide = next(
            (guide for guide in GUIDES
             if guide["case_id"] == case_id),
            None
        )

        if selected_case is None or selected_guide is None:
            abort(404)

               # Require student login
        if "user_id" not in session:
            flash("Please log in to download your investigation report.")
            return redirect(url_for("login"))

        db = get_db()

        saved_record = db.execute("""
            SELECT *
            FROM investigations
            WHERE student_id = ? AND case_id = ?
                """, (
            str(session["user_id"]),
            case_id
        )).fetchone()

        if saved_record is None:
            flash("No saved investigation found. Please save your work first.")
            return redirect(
                url_for(
                    "investigation_workspace",
                    case_id=case_id
                )
            )

        pdf_buffer = create_investigation_pdf(
            selected_case,
            saved_record,
            selected_guide
        )

        filename = f"ForenQuest_Report_{case_id}.pdf"

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype="application/pdf"
        )
   
    # Student Dashboard
    @app.route("/dashboard")
    def student_dashboard():

        # Require student login
        if "user_id" not in session:
            flash("Please log in to access your dashboard.")
            return redirect(url_for("login"))

        # Get the logged-in student's account ID
        student_id = str(session["user_id"])

        db = get_db()

        # Retrieve all saved investigations and their statuses
        saved_records = db.execute("""
            SELECT case_id, status, updated_at
            FROM investigations
            WHERE student_id = ?
            ORDER BY updated_at DESC
        """, (student_id,)).fetchall()

        # Get IDs of cases with saved investigations
        saved_case_ids = [
            record["case_id"] for record in saved_records
        ]

        # Map each case to its current investigation status
        case_statuses = {
            record["case_id"]: record["status"]
            for record in saved_records
        }

        # Calculate dashboard statistics
        total_cases = len(CASES)

        saved_count = len(saved_records)

        completed_count = sum(
            1 for record in saved_records
            if record["status"] == "Completed"
        )

        in_progress_count = sum(
            1 for record in saved_records
            if record["status"] == "In Progress"
        )

        not_started_count = total_cases - saved_count

        # Display dashboard
        return render_template(
            "dashboard.html",
            cases=CASES,
            total_cases=total_cases,
            saved_count=saved_count,
            saved_case_ids=saved_case_ids,
            saved_records=saved_records,
            case_statuses=case_statuses,
            completed_count=completed_count,
            in_progress_count=in_progress_count,
            not_started_count=not_started_count
        )

        
    # Student Registration
    @app.route("/register", methods=["GET", "POST"])
    def register():

        if request.method == "POST":

            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")

            
            if not username or not email or not password:
                flash("All fields are required.")
                return redirect(url_for("register"))

            if len(username) < 3 or len(username) > 30:
                flash("Username must be between 3 and 30 characters.")
                return redirect(url_for("register"))

            if not username.replace("_", "").isalnum():
                flash("Username can contain only letters, numbers and underscores.")
                return redirect(url_for("register"))

            if len(email) > 254 or "@" not in email:
                flash("Please enter a valid email address.")
                return redirect(url_for("register"))

            if len(password) < 8:
                flash("Password must contain at least 8 characters.")
                return redirect(url_for("register"))

            if len(password) > 128:
                flash("Password cannot exceed 128 characters.")
                return redirect(url_for("register"))


            db = get_db()

            existing_user = db.execute("""
                SELECT id FROM users
                WHERE username = ? OR email = ?
            """, (username, email)).fetchone()

            if existing_user:
                flash("Username or email already exists.")
                return redirect(url_for("register"))

            password_hash = hash_password(password)

            db.execute("""
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            """, (username, email, password_hash))

            db.commit()

            flash("Registration successful! Please log in.")
            return redirect(url_for("login"))

        return render_template("register.html")


    # Student Login
    @app.route("/login", methods=["GET", "POST"])
    def login():

        if request.method == "POST":

            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            db = get_db()

            user = db.execute("""
                SELECT * FROM users
                WHERE username = ?
            """, (username,)).fetchone()

            if user is None or not verify_password(
                user["password_hash"], password
            ):
                flash("Invalid username or password.")
                return redirect(url_for("login"))

            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session.permanent = True
            flash("Login successful!")
            return redirect(url_for("student_dashboard"))

        return render_template("login.html")


    # Student Logout
    @app.route("/logout")
    def logout():

        session.clear()

        flash("You have been logged out.")
        return redirect(url_for("login"))

    return app
