from flask import render_template, request, jsonify
from app import app
import requests

oauth_url = "https://oauth.vk.com/authorize"
vk_api_url = "https://api.vk.com/method/"


def main_page():
    return render_template("index.html")


def login_to_vk():
    r = requests.post(
        url=oauth_url,
        data={
            "client_id": app.config.get("CLIENT_ID"),
            "display": "page",
            # "redirect_uri": "167.71.58.132",
            "scope": 2,
            "response_type": "token",
            "v": 5.120
        }
    )
    print(r.content)
    print(r.cookies)
    return "ok"


def is_logged():
    return "ok"
