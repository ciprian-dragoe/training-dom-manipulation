from flask import Blueprint, request, redirect, session, render_template, url_for
import bcrypt
from services import docker
from data.configuration import CONFIGURATION


admin_route = Blueprint('admin', __name__)


@admin_route.route("/login", methods=["GET", "POST"])
def display_admin_login():
    if request.method == "GET":
        return render_template("admin-login.html")
    else:
        if verify_password(request.form['pass'], CONFIGURATION['ADMIN-HASHED-PASSWORD']):
            session["is-admin-logged"] = 1
            return redirect(url_for("admin.display_admin_dashboard"))
        return redirect(url_for("admin.display_admin_login"))


@admin_route.route("/dashboard", methods=["GET"])
def display_admin_dashboard():
    if "is-admin-logged" in session.keys():
        docker.initialize()
        return render_template("admin-dashboard.html")
    else:
        return redirect(url_for("admin.display_admin_login"))


@admin_route.route("/logout", methods=["POST"])
def logout_admin():
    docker.kill_existing_containers()
    session.pop('is-admin-logged', None)
    return redirect(url_for("admin.display_admin_login"))


def verify_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)


