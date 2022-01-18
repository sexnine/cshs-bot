from bot.util.db import db


class Saveable:
    async def save(self):
        return await db.save(self)
