from flask import render_template, request, jsonify
from logging.handlers import RotatingFileHandler
from werkzeug.urls import url_decode
from requests import post
from app import app
import logging
import os

parent_dir = "/".join(os.path.realpath(__file__).split("/")[:-1])
log_dir = os.path.join(parent_dir, "logs")

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

handler = RotatingFileHandler(f"{log_dir}/app.log", maxBytes=1000000, backupCount=8)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter(
    '%(hostip)s [%(asctime)s] -- %(message)s'
))

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

token_url = "https://oauth.vk.com/access_token"
oauth_url = "https://oauth.vk.com/authorize"
vk_api_url = "https://api.vk.com/method/"


def stringify_cookie(cookie: dict):
    out_cookie = ""
    for k, v in cookie.items():
        out_cookie += f"{k}={v};"
    return out_cookie


def log_action():
    logger.info(
        f"\"{request.method} "
        f"{request.url}\" "
        f"{request.headers.get('User-Agent')} "
        f"{stringify_cookie(request.cookies)}",
        extra={"hostip": request.host}
    )


def main_page():
    log_action()
    return render_template("index.html")


def login_to_vk():
    r = post(
        url=oauth_url,
        data={
            "client_id": app.config.get("CLIENT_ID"),
            "display": "page",
            "redirect_uri": "https://167.71.58.132/est/getCode",
            "scope": 2,
            "response_type": "code",
            "v": 5.120
        }
    )

    log_action()
    return r.content


def get_code():
    req = url_decode(request.url)

    # if "code" not in req.keys():
    #     return jsonify({"error": req.get("error"), "error_description": req.get("error_description")}), 400

    code = req.get("code")
    r = post(
        url=token_url,
        data={
            "client_id": app.config["CLIENT_ID"],
            "client_secret": app.config["APP_SECRET_KEY"],
            "redirect_url": "https://167.71.58.132/est/getToken",
            "code": code
        }
    )
    return request.url, 200


def get_token():
    req = url_decode(request.url)

    if "error" in req:
        return jsonify({"error": req.get("error"), "error_description": req.get("error_description")}), 400

    return request.url, 200
