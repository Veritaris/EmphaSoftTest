from config.Config import Config
from flask import Flask, json

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
