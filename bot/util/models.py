from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    xp = fields.IntField()
    level = fields.IntField()
