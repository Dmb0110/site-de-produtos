from flask import current_app

from app.database.core import db
from app.models.models_produto import Produto


class ProdutoService:
    @staticmethod
    def _comando_db(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            current_app.logger.exception("Erro ao acessar o banco de dados")
            raise RuntimeError("Falha ao acessar o banco de dados") from exc
    @staticmethod
    def serializar(produto: Produto):
        return {
            "id": produto.id,
            "nome": produto.nome,
            "preco": float(produto.preco),
        }

    @staticmethod
    def criar(data: dict):
        return ProdutoService._comando_db(lambda: ProdutoService._criar_impl(data))

    @staticmethod
    def _criar_impl(data: dict):
        produto = Produto(nome=data["nome"], preco=data["preco"])
        db.session.add(produto)
        db.session.commit()
        db.session.refresh(produto)
        return ProdutoService.serializar(produto)

    @staticmethod
    def listar_todos():
        return ProdutoService._comando_db(lambda: [ProdutoService.serializar(produto) for produto in Produto.query.all()])

    @staticmethod
    def buscar_por_id(produto_id: int):
        return ProdutoService._comando_db(lambda: ProdutoService._buscar_impl(produto_id))

    @staticmethod
    def _buscar_impl(produto_id: int):
        produto = Produto.query.get(produto_id)
        if produto is None:
            return None
        return ProdutoService.serializar(produto)

    @staticmethod
    def atualizar(produto_id: int, data: dict):
        return ProdutoService._comando_db(lambda: ProdutoService._atualizar_impl(produto_id, data))

    @staticmethod
    def _atualizar_impl(produto_id: int, data: dict):
        produto = Produto.query.get(produto_id)
        if produto is None:
            return None

        for key, value in data.items():
            setattr(produto, key, value)

        db.session.commit()
        db.session.refresh(produto)
        return ProdutoService.serializar(produto)

    @staticmethod
    def excluir(produto_id: int):
        return ProdutoService._comando_db(lambda: ProdutoService._excluir_impl(produto_id))

    @staticmethod
    def _excluir_impl(produto_id: int):
        produto = Produto.query.get(produto_id)
        if produto is None:
            return None

        db.session.delete(produto)
        db.session.commit()
        return True
