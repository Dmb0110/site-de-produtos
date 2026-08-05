import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, send_from_directory
from werkzeug.exceptions import HTTPException

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.database.core import db, init_app, mongo
from app.routers.routers_produto import produto_bp

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
init_app(app)
app.register_blueprint(produto_bp)


@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.exception("Erro nao tratado durante requisicao")
    if isinstance(error, HTTPException):
        return jsonify({"erro": error.description}), error.code
    return jsonify({"erro": "Erro interno do servidor"}), 500


def inicializar_bancos() -> None:
    with app.app_context():
        db.create_all()
        mongo.db.command("ping")
        mongo.db.fotos.create_index("product_id", unique=True, sparse=True)


inicializar_bancos()


@app.route("/", methods=["GET"])
def ola():
    return send_from_directory(ROOT_DIR / "front", "index.html")


@app.route("/front", methods=["GET"])
@app.route("/front/", methods=["GET"])
def abrir_front():
    return send_from_directory(ROOT_DIR / "front", "index.html")


@app.route("/front/<path:filename>", methods=["GET"])
def servir_front(filename):
    return send_from_directory(ROOT_DIR / "front", filename)


@app.route("/<filename>.html", methods=["GET"])
def servir_pagina_html(filename):
    return send_from_directory(ROOT_DIR / "front", f"{filename}.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)

