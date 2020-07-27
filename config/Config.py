from flask import json
import os


class Config(object):
    parent_dir = "/".join(os.path.realpath(__file__).split("/")[:-2])
    if not("super.config" in os.listdir(f"{parent_dir}/config")):
        os.symlink(f"{parent_dir}/config/secret.config", f"{parent_dir}/config/super.config")

    with open(f"{parent_dir}/config/super.config", "r") as f:
        config = json.loads(f.read())

    CLIENT_ID = config["client_id"]
    APP_SECRET_KEY = config["secretKey"]
    SECRET_KEY = config["secretKey"]
    ACCESS_TOKEN = config["access_token"]
    v = config["v"]
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{parent_dir}/database/database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

