from flask import request
from app import app
from app import API


@app.route("/est", methods=["GET"])
def render_main():
    # if request.cookies.get("user_logged")
    return API.main_page()


@app.route("/est/login", methods=["POST"])
def login_to_vk():
    return API.login_to_vk()


@app.route("/est/getCode", methods=["GET"])
def get_code():
    return API.get_code()
