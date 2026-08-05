import base64
import re

from marshmallow import Schema, ValidationError, fields, validate

MAX_FOTO_BYTES = 2 * 1024 * 1024
FOTO_DATA_URL = re.compile(r"^data:(image/(?:jpeg|png|gif|webp));base64,([A-Za-z0-9+/]+={0,2})$")


def validar_foto(valor: str) -> None:
    correspondencia = FOTO_DATA_URL.fullmatch(valor)
    if not correspondencia:
        raise ValidationError("A foto deve ser uma imagem JPEG, PNG, GIF ou WebP em base64.")

    try:
        conteudo = base64.b64decode(correspondencia.group(2), validate=True)
    except ValueError as exc:
        raise ValidationError("A foto possui base64 invalido.") from exc

    if len(conteudo) > MAX_FOTO_BYTES:
        raise ValidationError("A foto deve ter no maximo 2 MB.")


class ProdutoPostSchema(Schema):
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    preco = fields.Float(required=True, validate=validate.Range(min=0))
    foto = fields.Str(required=False, validate=validar_foto)


class ProdutoPutSchema(Schema):
    nome = fields.Str(required=False, validate=validate.Length(min=1, max=100))
    preco = fields.Float(required=False, validate=validate.Range(min=0))
    foto = fields.Str(required=False, validate=validar_foto)


produto_post_schema = ProdutoPostSchema()
produto_put_schema = ProdutoPutSchema()
