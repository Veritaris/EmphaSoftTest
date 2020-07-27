from flask import Flask, json, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.Config import Config
import datetime

app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.config.from_object(Config)
database = SQLAlchemy(app)
migrate = Migrate(app, database)

from database import DatabaseModels
from app import routes
