from flask import session
from app import API
from app import app


@app.route("/", methods=["GET"])
def render_main():
    if not session.get("user"):
        return API.main_page()
    else:
        return API.show_friend()


@app.route("/login", methods=["POST", "GET"])
def login_to_vk():
    return API.login_to_vk()


@app.route("/getCode", methods=["GET"])
def get_code():
    return API.get_code()


@app.route("/logout", methods=["POST"])
def logout():
    return API.logout()
