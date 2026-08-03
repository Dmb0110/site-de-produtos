from sqlalchemy import Column, Integer, String, Numeric

from app.database.core import db


class Produto(db.Model):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f"<Produto id={self.id} nome={self.nome!r} preco={self.preco}>"
