
import json
import uuid
from app.verification import calculate_sha256, verify_sha256
from flask import send_file
from app.reports import create_investigation_pdf
from flask import (
    Flask,
    render_template,
    abort,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app.cases import CASES
from app.guides import GUIDES
from app.database import init_db, get_db


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "change-this-development-key"

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

        # Temporary browser-based student identity
        if "student_id" not in session:
            session["student_id"] = str(uuid.uuid4())

        student_id = session["student_id"]

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
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)

                ON CONFLICT(student_id, case_id)
                DO UPDATE SET
                    investigator_name = excluded.investigator_name,
                    findings = excluded.findings,
                    evidence_notes = excluded.evidence_notes,
                    answers = excluded.answers,
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

        if "student_id" not in session:
            flash("Please save an investigation before generating a report.")
            return redirect(
                url_for(
                    "investigation_workspace",
                    case_id=case_id
                )
            )

        db = get_db()

        saved_record = db.execute("""
            SELECT *
            FROM investigations
            WHERE student_id = ? AND case_id = ?
        """, (
            session["student_id"],
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

    return app
