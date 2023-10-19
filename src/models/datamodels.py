from pydantic import BaseModel
import uuid


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str
    user_id: str


class AccountNoId(BaseModel):
    """A user account but without the ID. Used for parsing input and registering users"""
    name_f: str
    name_l: str | None = None
    email: str
    password: str
    address: str | None = None
    contact: str | None = None


class Account(AccountNoId):
    """A full model of the user account in the database."""
    acct_id: uuid.UUID


class Customer(BaseModel):
    """User data for the frontend."""
    user_id: str
    name_f: str
    name_l: str | None = None
    cart: str | None = None
    prefs: str | None = None


class ItemNoId(BaseModel):
    """A representation of a full item for sale in the database."""
    # TODO: /items/new still has seller id in request body. Make a new model since seller id comes from token now.
    name: str
    image: str | None = None
    price: float | None = None
    desc: str | None = None
    tag: str | None = None
    seller: uuid.UUID | None = None
    sku: str | None = None


class Item(ItemNoId):
    """This class inherits all attributes of ItemNoId, but adds the item's id."""
    item_id: int


class ListedItem(BaseModel):
    """Listings differ from items.
    They are smaller and easier to process, and can exist multiple times per item.
    These only appear on the browse/search page. The full item is used for the item's own page."""
    item_id: int
    name: str
    thumbnail: str | None = None
    price: float
    tag: str | None = None
