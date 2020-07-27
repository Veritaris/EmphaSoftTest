from flask import render_template, request, jsonify, session, redirect
from database.DatabaseModels import database, Users
from logging.handlers import RotatingFileHandler
from werkzeug.urls import url_decode
from requests import post
from uuid import uuid4
from app import app
import logging
from faker import Faker
from faker.providers import internet
import os

dbsession = database.session
parent_dir = "/".join(os.path.realpath(__file__).split("/")[:-1])
log_dir = os.path.join(parent_dir, "logs")

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

fake = Faker()
fake.add_provider(internet)

fake_friend = []
for i in range(5):
    fake_friend.append(
        (fake.first_name(), fake.last_name(), fake.url())
    )

handler = RotatingFileHandler(f"{log_dir}/app.log", maxBytes=1000000, backupCount=8)
handler.setLevel(logging.INFO)
# handler.setFormatter(logging.Formatter(
#     '%(hostip)s [%(asctime)s] -- %(message)s'
# ))
handler.setFormatter(logging.Formatter(
    '[%(asctime)s] -- %(message)s'
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


def log(func):
    def wrap():
        logger.info(
            f"\"{request.method} "
            f"{request.url}\" "
            f"{request.headers.get('User-Agent')} "
            f"{stringify_cookie(request.cookies)}",
            extra={"hostip": request.url}
        )
        return func()
    return wrap


@log
def main_page():
    return render_template("login.html")


@log
def login_to_vk():
    session.permanent = True if request.form.get("keep_login") else False
    if not session.get("user"):
        user_session_uuid = str(uuid4().hex)
        dbsession.add(Users(user_uuid=user_session_uuid, user_token=str(uuid4().hex)))
        dbsession.commit()
        session["user"] = user_session_uuid
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
        return r.content
    return redirect("/est")


@log
def get_code():
    req = url_decode(request.url)
    print(req)
    if "code" in req.keys():
        code = req.get("code")
        r = post(
            url=token_url,
            data={
                "client_id": app.config["CLIENT_ID"],
                "client_secret": app.config["APP_SECRET_KEY"],
                "redirect_uri": "https://167.71.58.132/est/getCode",
                "code": code
            }
        )
        print(r)
        if r.json().get("access_token"):
            token = r.json().get("access_token")
            user = dbsession.query(Users).get(session.get("user"))
            user.user_token = str(token)
            dbsession.commit()
        return request.url, 200
    else:
        return "ok", 200


@log
def get_token():
    req = url_decode(request.url)

    if "error" in req:
        return jsonify({"error": req.get("error"), "error_description": req.get("error_description")}), 400

    return request.url, 200


@log
def show_friend():
    if not dbsession.query(Users).get(session.get("user")):
        session.pop("user", None)
        return redirect("/est")

    return render_template("home.html", user="testuser", friends=fake_friend), 200


def logout():
    if not session.get("user"):
        dbsession.delete(dbsession.quert(Users).get(session.get("user")))
        dbsession.commit()
        session.pop("user", None)
        session.modified = True
        return redirect("/est")
    return redirect("/est")
