from flask import render_template, request, jsonify
from app import app
import requests
import logging
import os

parent_dir = "/".join(os.path.realpath(__file__).split("/")[:-1])
log_dir = os.path.join(parent_dir, "logs")

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(filename=f"{log_dir}/app.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s")
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
            "redirect_uri": "https://167.71.58.132/est/access",
            "scope": 2,
            "response_type": "code",
            "v": 5.120
        }
    )
    logging.info(str(r.content))
    logging.info(str(r.cookies))
    return "ok"


def is_logged():
    return "ok"


def get_access():
    r = request
    logging.info(r.path)
    return "r.path"
