from pydantic import BaseModel
import uuid

# We're not using Pydantic's models here.
# Why? Our rdbms likely will output results as tuples.
# Pydantic expects dicts, and we'd need to write a rowparser for the rdbms


class User:
    def __init__(self, db_user: tuple):
        self.username = db_user[0]


class Item(BaseModel):
    name: str
    price: float = None
    desc: str = None
    seller: uuid.UUID = None
    sku: str = None
