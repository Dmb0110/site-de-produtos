from marshmallow import Schema, fields, validate

class ProdutoGetSchema(Schema):
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    preco = fields.Float(required=True, validate=validate.Range(min=0))


class ProdutoPostSchema(Schema):
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    preco = fields.Float(required=True, validate=validate.Range(min=0))


class ProdutoPutSchema(Schema):
    nome = fields.Str(required=False, validate=validate.Length(min=1, max=100))
    preco = fields.Float(required=False, validate=validate.Range(min=0))


class ProdutoDeleteSchema(Schema):
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=100))


produto_get_schema = ProdutoGetSchema()
produtos_get_schema = ProdutoGetSchema(many=True)
produto_post_schema = ProdutoPostSchema()
produto_put_schema = ProdutoPutSchema()
produto_delete_schema = ProdutoDeleteSchema()
