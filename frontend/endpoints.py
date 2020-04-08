from flask import Blueprint, render_template

frontend = Blueprint("frontend", __name__)


@frontend.route("/")
def start_page():
    return render_template("startpage.html")
