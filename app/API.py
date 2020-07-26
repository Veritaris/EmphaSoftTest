from logging.handlers import RotatingFileHandler

from flask import render_template, request, jsonify
from app import app
import requests
import logging
import os

parent_dir = "/".join(os.path.realpath(__file__).split("/")[:-1])
log_dir = os.path.join(parent_dir, "logs")

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

handler = RotatingFileHandler(f"{log_dir}/app.log", maxBytes=1000000, backupCount=8)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter(
    '[%(asctime)s] -- %(message)s'
))

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

logging.basicConfig(
    filename=f"{log_dir}/app.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
oauth_url = "https://oauth.vk.com/authorize"
vk_api_url = "https://api.vk.com/method/"


def main_page():
    logger.info(f"\"{request.method} {request.url}\" {request.headers.get('User-Agent')} {request.cookies}")
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
    logger.info(f"\"{request.method} {request.url}\" {request.headers.get('User-Agent')} {request.cookies}")
    return r.content


def is_logged():
    logger.info(f"\"{request.method} {request.url}\" {request.headers.get('User-Agent')} {request.cookies}")
    return "ok"


def get_access():
    r = request
    logger.info(f"\"{request.method} {request.url}\" {request.headers.get('User-Agent')} {request.cookies}")
    return "r.path"
