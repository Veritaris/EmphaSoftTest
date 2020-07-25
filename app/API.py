from flask import render_template

from app import app


def main_page():
    return render_template("index.html")


def login_to_vk():
    return "ok"
