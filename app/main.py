import os
import sys
import traceback
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, send_from_directory
from werkzeug.exceptions import HTTPException

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.database.core import db, init_app
from app.routers.routers_produto import produto_bp

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
init_app(app)
app.register_blueprint(produto_bp)


@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.exception("Erro não tratado durante requisição")
    if isinstance(error, HTTPException):
        return jsonify({"erro": error.description}), error.code
    return jsonify({"erro": "Erro interno do servidor"}), 500

def inicializar_banco():
    with app.app_context():
        try:
            db.create_all()
            print("Banco inicializado com sucesso.")
        except Exception as exc:
            print(f"Não foi possível inicializar o banco: {exc}")
            traceback.print_exc()
            print("A aplicação continuará funcionando, mas o banco ainda não está disponível.")


inicializar_banco()

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)


'''
rodar para rodar o servidor:

python main.py
 
python app/main.py

'''
