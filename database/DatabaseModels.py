from flask import jsonify
from app import database


def dump_datetime(value):
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


class Users(database.Model):
    __tablename__ = "Users"
    user_uuid = database.Column(database.String(64), primary_key=True)
    user_code = database.Column(database.String(64), unique=True)
    user_token = database.Column(database.String(64), unique=True)

    def __repr__(self):
        return f"<User {self.user_uuid}>"

    @property
    def serialize(self):
        return {
            "uuid": self.user_uuid,
            "token": self.user_token
        }
