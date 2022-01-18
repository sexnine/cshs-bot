from odmantic import Field, Model
from odmantic import AIOEngine
from os import getenv

db = AIOEngine(getenv("MONGO_URI"))


class User(Model):
    id: int = Field(primary_field=True)
    xp: int = 0
    level: int = 0
