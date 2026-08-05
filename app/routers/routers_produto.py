import base64

from flask import Blueprint, Response, jsonify, redirect, request
from marshmallow import ValidationError

from app.schemas.schemas_produto import produto_post_schema, produto_put_schema
from app.service.service_produto import ProdutoService

produto_bp = Blueprint("produto_bp", __name__, url_prefix="/produtos")


@produto_bp.route("", methods=["GET"])
def listar_produtos():
    try:
        produtos = ProdutoService.listar_todos()
        return jsonify(produtos), 200
    except RuntimeError as exc:
        return jsonify({"erro": str(exc)}), 503


@produto_bp.route("/<int:produto_id>", methods=["GET"])
def obter_produto(produto_id: int):
    try:
        produto = ProdutoService.buscar_por_id(produto_id)
    except RuntimeError as exc:
        return jsonify({"erro": str(exc)}), 503

    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify(produto), 200


@produto_bp.route("/<int:produto_id>/foto", methods=["GET"])
def obter_foto(produto_id: int):
    try:
        foto = ProdutoService.buscar_foto(produto_id)
    except RuntimeError as exc:
        return jsonify({"erro": str(exc)}), 503

    if foto is None:
        return jsonify({"erro": "Foto nao encontrada"}), 404
    if foto.startswith(("http://", "https://")):
        return redirect(foto)

    cabecalho, conteudo = foto.split(",", 1)
    tipo_mime = cabecalho.removeprefix("data:").removesuffix(";base64")
    return Response(base64.b64decode(conteudo), mimetype=tipo_mime)


@produto_bp.route("", methods=["POST"])
def criar_produto():
    payload = request.get_json(silent=True) or {}

    try:
        data = produto_post_schema.load(payload)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        produto = ProdutoService.criar(data)
    except RuntimeError as exc:
        return jsonify({"erro": str(exc)}), 503

    return jsonify(produto), 201


@produto_bp.route("/<int:produto_id>", methods=["PUT"])
def atualizar_produto(produto_id: int):
    payload = request.get_json(silent=True) or {}

    try:
        data = produto_put_schema.load(payload)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        produto = ProdutoService.atualizar(produto_id, data)
    except RuntimeError as exc:
        return jsonify({"erro": str(exc)}), 503

    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404

    return jsonify(produto), 200


@produto_bp.route("/<int:produto_id>", methods=["DELETE"])
def deletar_produto(produto_id: int):
    try:
        produto = ProdutoService.excluir(produto_id)
    except RuntimeError as exc:
        return jsonify({"erro": str(exc)}), 503

    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404

    return jsonify({"mensagem": "Produto removido com sucesso"}), 200
