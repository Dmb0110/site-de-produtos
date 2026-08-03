import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()


def init_app(app: Flask):
    database_url = os.getenv("DATABASE_URL", "").strip()

    if not database_url:
        raise RuntimeError("A variável DATABASE_URL não foi configurada para PostgreSQL.")

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False

    if database_url.startswith("postgresql://") or database_url.startswith("postgresql+psycopg2://"):
        engine_options = app.config.setdefault("SQLALCHEMY_ENGINE_OPTIONS", {})
        connect_args = engine_options.setdefault("connect_args", {})
        connect_args["options"] = "-c client_encoding=UTF8"
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = engine_options

    db.init_app(app)
