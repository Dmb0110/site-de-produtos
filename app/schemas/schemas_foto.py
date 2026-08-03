from marshmallow import Schema, fields, validate


class FotoGetSchema(Schema):
    id = fields.Str(dump_only=True)
    foto = fields.Str(required=True, validate=validate.Length(min=1))


class FotoPostSchema(Schema):
    foto = fields.Str(required=True, validate=validate.Length(min=1))


class FotoPutSchema(Schema):
    foto = fields.Str(required=False, validate=validate.Length(min=1))


class FotoDeleteSchema(Schema):
    id = fields.Str(required=True, validate=validate.Length(min=1))


foto_get_schema = FotoGetSchema()
fotos_get_schema = FotoGetSchema(many=True)
foto_post_schema = FotoPostSchema()
foto_put_schema = FotoPutSchema()
foto_delete_schema = FotoDeleteSchema()
