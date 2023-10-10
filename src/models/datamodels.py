from pydantic import BaseModel
import uuid


class User:
    pass


class ItemNoId(BaseModel):
    # TODO: Come back and implement images/tags. SQLite doesn't support lists/arrays
    name: str
    image: str = None
    price: float = None
    desc: str = None
    tag: str = None
    seller: uuid.UUID = None
    sku: str = None


class Item(ItemNoId):
    item_id: int

