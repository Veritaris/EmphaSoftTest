from flask import json
import os


class Config(object):
    config_dir = os.path.dirname(os.path.realpath(__file__))
    if not("super.config" in os.listdir(config_dir)):
        os.symlink(f"{config_dir}/secret.config", f"{config_dir}/super.config")

    with open(f"{config_dir}/super.config", "r") as f:
        config = json.loads(f.read())

    CLIENT_ID = config["client_id"]
    APP_SECRET_KEY = config["secretKey"]
    ACCESS_TOKEN = config["access_token"]
    v = config["v"]
