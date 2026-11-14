
from flask import Flask, render_template, abort
from app.cases import CASES


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "change-this-development-key"

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

    return app
