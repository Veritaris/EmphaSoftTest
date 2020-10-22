from flask import render_template, request, jsonify, session, redirect
from database.DatabaseModels import database, Users
from logging.handlers import RotatingFileHandler
from werkzeug.urls import url_decode, url_parse
from requests import post
from uuid import uuid4
from app import app
import logging
import os

dbsession = database.session
parent_dir = "/".join(os.path.realpath(__file__).split("/")[:-1])
log_dir = os.path.join(parent_dir, "logs")

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

token_url = "https://oauth.vk.com/access_token"
oauth_url = "https://oauth.vk.com/authorize"
vk_api_url = "https://api.vk.com/method/{}"

handler = RotatingFileHandler(f"{log_dir}/app.log", maxBytes=1000000, backupCount=8)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter(
    '%(userip)s -> %(hostip)s [%(asctime)s] -- %(message)s'
))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def log(func):
    def wrap():
        logger.info(
            f"\"{request.method} "
            f"{request.url}\" "
            f"{request.headers.get('User-Agent')} ",
            extra={"hostip": request.host, "userip": request.headers.get('X-Forwarded-For', request.remote_addr)}
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
        return redirect(
            oauth_url + f"?client_id={app.config.get('CLIENT_ID')}&"
                        f"display=page&"
                        f"redirect_uri=https://est.veritaris.me/getCode&"
                        f"scope=2&"
                        f"response_type=code&"
                        f"v=120"
        )
    return redirect("/")


@log
def get_code():
    req = url_decode(url_parse(request.url).query)
    if "code" in req.keys():
        code = req.get("code")
        r = post(
            url=token_url,
            data={
                "client_id": app.config["CLIENT_ID"],
                "client_secret": app.config["APP_SECRET_KEY"],
                "redirect_uri": "https://est.veritaris.me/getCode",
                "code": code
            }
        )
        if r.json().get("access_token"):
            token = r.json().get("access_token")
            user = dbsession.query(Users).get(session.get("user"))
            user.user_code = str(code)
            user.user_token = str(token)
            dbsession.commit()
        return redirect("/")
    else:
        return jsonify(req), 200


@log
def show_friend():
    if not dbsession.query(Users).get(session.get("user")):
        session.pop("user", None)
        return "You was logged out, please login again."
    user_token = dbsession.query(Users).get(session.get("user")).user_token
    me = post(
        url=vk_api_url.format("users.get"),
        data={
            "v": "5.120",
            "access_token": user_token
        }
    )
    username = " ".join([me.json().get("response")[0].get("first_name"), me.json().get("response")[0].get("last_name")])
    friends_ids = ",".join(map(str, post(
            url=vk_api_url.format("friends.get"),
            data={
                "v": "5.120",
                "access_token": user_token,
                "count": 5
            }).json().get("response").get("items")
        )
    )
    friends_data = post(
        url=vk_api_url.format("users.get"),
        data={
            "v": "5.120",
            "access_token": user_token,
            "user_ids": friends_ids
        }
    )
    friends = []
    for user in friends_data.json().get("response"):
        friends.append(
            (user.get("first_name"), user.get("last_name"), user.get("id"))
        )
    return render_template("home.html", user=username, friends=friends), 200


def logout():
    if session.get("user"):
        dbsession.delete(dbsession.query(Users).get(session.get("user")))
        dbsession.commit()
        session.pop("user", None)
    return redirect("/")
