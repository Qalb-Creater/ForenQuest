from flask import Flask, render_template


def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "change-this-development-key"

    @app.route("/")
    def home():
        return render_template("index.html")

    return app