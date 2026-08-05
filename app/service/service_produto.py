from flask import current_app

from app.database.core import db, mongo
from app.models.models_produto import Produto


class ProdutoService:
    @staticmethod
    def _comando_db(func):
        try:
            return func()
        except Exception as exc:
            db.session.rollback()
            current_app.logger.exception("Erro ao acessar os bancos")
            raise RuntimeError("Falha ao acessar os bancos") from exc

    @staticmethod
    def serializar(produto: Produto, possui_foto: bool = False) -> dict:
        return {
            "id": produto.id,
            "nome": produto.nome,
            "preco": float(produto.preco),
            "foto": f"/produtos/{produto.id}/foto" if possui_foto else None,
        }

    @staticmethod
    def criar(data: dict) -> dict:
        return ProdutoService._comando_db(lambda: ProdutoService._criar_impl(data))

    @staticmethod
    def _criar_impl(data: dict) -> dict:
        produto = Produto(nome=data["nome"], preco=data["preco"])
        db.session.add(produto)
        db.session.commit()
        db.session.refresh(produto)

        if data.get("foto"):
            try:
                mongo.db.fotos.insert_one({"product_id": produto.id, "foto": data["foto"]})
            except Exception:
                db.session.delete(produto)
                db.session.commit()
                raise

        return ProdutoService.serializar(produto, bool(data.get("foto")))

    @staticmethod
    def listar_todos() -> list[dict]:
        def listar():
            produtos = Produto.query.order_by(Produto.id).all()
            ids = [produto.id for produto in produtos]
            fotos = mongo.db.fotos.find({"product_id": {"$in": ids}}, {"product_id": 1}) if ids else []
            ids_com_foto = {foto["product_id"] for foto in fotos}
            return [ProdutoService.serializar(produto, produto.id in ids_com_foto) for produto in produtos]

        return ProdutoService._comando_db(listar)

    @staticmethod
    def buscar_por_id(produto_id: int) -> dict | None:
        def buscar():
            produto = db.session.get(Produto, produto_id)
            if produto is None:
                return None
            possui_foto = mongo.db.fotos.find_one({"product_id": produto.id}, {"_id": 1}) is not None
            return ProdutoService.serializar(produto, possui_foto)

        return ProdutoService._comando_db(buscar)

    @staticmethod
    def buscar_foto(produto_id: int) -> str | None:
        def buscar():
            if db.session.get(Produto, produto_id) is None:
                return None
            documento = mongo.db.fotos.find_one({"product_id": produto_id}, {"foto": 1})
            return documento.get("foto") if documento else None

        return ProdutoService._comando_db(buscar)

    @staticmethod
    def atualizar(produto_id: int, data: dict) -> dict | None:
        def atualizar():
            produto = db.session.get(Produto, produto_id)
            if produto is None:
                return None

            foto_anterior = mongo.db.fotos.find_one({"product_id": produto.id})
            if "foto" in data:
                mongo.db.fotos.update_one(
                    {"product_id": produto.id},
                    {"$set": {"foto": data["foto"]}},
                    upsert=True,
                )

            if "nome" in data:
                produto.nome = data["nome"]
            if "preco" in data:
                produto.preco = data["preco"]

            try:
                db.session.commit()
            except Exception:
                if "foto" in data:
                    if foto_anterior:
                        mongo.db.fotos.replace_one({"_id": foto_anterior["_id"]}, foto_anterior)
                    else:
                        mongo.db.fotos.delete_one({"product_id": produto.id})
                raise

            return ProdutoService.serializar(produto, "foto" in data or foto_anterior is not None)

        return ProdutoService._comando_db(atualizar)

    @staticmethod
    def excluir(produto_id: int) -> bool | None:
        def excluir():
            produto = db.session.get(Produto, produto_id)
            if produto is None:
                return None

            foto_anterior = mongo.db.fotos.find_one({"product_id": produto.id})
            db.session.delete(produto)
            db.session.flush()
            try:
                mongo.db.fotos.delete_one({"product_id": produto.id})
                db.session.commit()
            except Exception:
                db.session.rollback()
                if foto_anterior:
                    mongo.db.fotos.replace_one({"_id": foto_anterior["_id"]}, foto_anterior, upsert=True)
                raise
            return True

        return ProdutoService._comando_db(excluir)
