import os

from dotenv import load_dotenv
from flask import Flask
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()
mongo = PyMongo()


def init_app(app: Flask) -> None:
    database_url = os.getenv("DATABASE_URL", "").strip()
    mongodb_uri = os.getenv("MONGODB_URI", "").strip()

    if not database_url:
        raise RuntimeError("A variavel DATABASE_URL nao foi configurada.")
    if not mongodb_uri:
        raise RuntimeError("A variavel MONGODB_URI nao foi configurada.")

    app.config.update(
        MONGO_URI=mongodb_uri,
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False,
        MAX_CONTENT_LENGTH=3 * 1024 * 1024,
    )

    if database_url.startswith(("postgresql://", "postgresql+psycopg2://")):
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "connect_args": {"options": "-c client_encoding=UTF8"},
        }

    db.init_app(app)
    mongo.init_app(app)
