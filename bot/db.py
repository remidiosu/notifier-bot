from tortoise import Tortoise, fields
from tortoise.models import Model
from dotenv import load_dotenv
import os

class UserURL(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField()
    url = fields.CharField(max_length=300)

    class Meta:
        table = "user_urls"

async def init_db():
    load_dotenv()

    db_url = (
        f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
        f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DB')}"
    )

    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["bot.db"]}
    )
    await Tortoise.generate_schemas()
