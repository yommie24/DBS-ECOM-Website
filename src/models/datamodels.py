from pydantic import BaseModel
import uuid


class AccountNoId(BaseModel):
    name_f: str
    name_l: str = None
    email: str
    password: str
    address: str = None
    contact: str = None


class Account(AccountNoId):
    acct_id: uuid.UUID






class ItemNoId(BaseModel):
    """A representation of a full item for sale in the database."""
    # TODO: Come back and implement images/tags. SQLite doesn't support lists/arrays
    name: str
    image: str = None
    price: float = None
    desc: str = None
    tag: str = None
    seller: uuid.UUID = None
    sku: str = None


class Item(ItemNoId):
    """This class inherits all attributes of ItemNoId, but adds the item's id."""
    item_id: int


class ListedItem(BaseModel):
    """Listings differ from items.
    They are smaller and easier to process, and can exist multiple times per item.
    These only appear on the browse/search page. The full item is used for the item's own page."""
    item_id: int
    name: str
    thumbnail: str = None
    price: float
    tag: str = None
