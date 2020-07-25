from flask import jsonify

from app import app
from app import API


@app.route("/", methods=["GET"])
def render_main():
    return API.main_page()

@app.route("/login", methods=["POST"])
def login_to_vk():
    return API.login_to_vk()
