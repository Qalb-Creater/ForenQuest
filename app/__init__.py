
from flask import Flask, render_template, abort
from app.cases import CASES
from app.guides import GUIDES


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

    return app
