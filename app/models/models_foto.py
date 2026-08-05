from sqlalchemy import Column, Integer, String

from app.database.core import db


class Foto(db.Model):
    __tablename__ = "fotos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    foto = Column(String(500), nullable=False)

    def __repr__(self):
        return f"<Foto id={self.id} foto={self.foto!r}>"
