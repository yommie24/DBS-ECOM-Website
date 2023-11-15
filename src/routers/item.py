from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import aiosqlite
from ..models import datamodels
from ..util import utils
from typing import Annotated

router = APIRouter(
    prefix="/items",
)


@router.get("/item/{item_id}")
async def find(item_id: int):
    return await get_item(item_id)


@router.get("/all")
async def get_all_listings():
    """Returns all listings. NOT items."""
    return await fetch_all_listings()


@router.get("/all-filter")
async def get_all_listings_f(min_price: float = None, max_price: float = None, tags: str = None):
    """[Unfinished] Returns filtered listings, using optional parameters"""
    #NOTE: Should probably use "man" and "women" as tags, since the LIKE statement has leading and trailing wildcards
    return await fetch_listings_filter(min_price, max_price, tags)


@router.get("/allitems")
async def get_all_items(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]):
    """Returns all items. Requires auth, as this is an admin function."""
    return await fetch_all_items()


@router.post("/new", status_code=201)
async def create(item: datamodels.ItemNoId, token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]):
    sel_id = await utils.decode_token(token)
    item.seller_id = sel_id.user_id
    return f"Your item was successfully created with id: {await make_item(item)}"


@router.post("/list", status_code=201)
async def list_item(item: datamodels.Item):
    return f"Your item was successfully listed with id: {await make_listing(item)}"


@router.delete("/del/{item_id}")
async def del_item(item_id: int, token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]):
    """Delete an item. If the item does not exist, will still say it was deleted."""
    item = await get_item(item_id)
    seller = await utils.decode_token(token)
    if str(item.seller_id) == seller.user_id:
        try:
            await delete_item(item_id)
            return f"Item {item_id} was deleted."
        except Exception as e:  # goodness gracious
            raise HTTPException(status_code=500, detail=e)
    else:
        raise HTTPException(status_code=401, detail="You cannot edit or delete another seller's items.")


async def get_item(item_id: int) -> datamodels.Item:
    async with aiosqlite.connect("./prime.db") as db:
        db.row_factory = utils.dict_factory
        cursor = await db.execute("SELECT * FROM item WHERE item_id = ?", (item_id,))
        result = await cursor.fetchone()
        # except sqlite3.OperationalError:  # item table doesn't exist TODO: application-wide logging
        #     pass
        if not result:
            raise HTTPException(status_code=404, detail=f"An item with id {item_id} was not found.")
        return datamodels.Item.model_validate(result)


async def make_item(item) -> int:
    async with aiosqlite.connect("./prime.db") as db:
        cursor = await db.execute("INSERT INTO item (name, image, price, description, seller_id, tag, sku) "
                                  "VALUES (?, ?, ?, ?, ?, ?, ?)", (
                                      item.name, item.image, item.price, item.desc, item.seller_id, item.tag, item.sku,
                                    ))
        await db.commit()
        return cursor.lastrowid


async def make_listing(item):
    async with aiosqlite.connect("./prime.db") as db:
        cursor = await db.execute("INSERT INTO listing VALUES (?, ?, ?, ?, ?)",
                                  (item.item_id, item.name, item.image, item.price, item.tag))
        await db.commit()
        return cursor.lastrowid


async def fetch_all_listings():
    async with aiosqlite.connect("./prime.db") as db:
        db.row_factory = utils.dict_factory
        cursor = await db.execute("SELECT * FROM listing")
        return [datamodels.ListedItem.model_validate(listing) for listing in await cursor.fetchall()]


async def fetch_listings_filter(price_min, price_max, tags):
    async with aiosqlite.connect("./prime.db") as db:
        db.row_factory = utils.dict_factory
        statement = "SELECT * FROM listing WHERE item_id > 0"
        params = []
        if price_min:
            statement += " AND price > ?"
            params.append(price_min)
        if price_max:
            statement += " AND price < ?"
            params.append(price_max)
        if tags:
            for tag in tags:
                statement += " AND tag LIKE ?"
                params.append(f"%{tag}%")
        cursor = await db.execute(statement, tuple(params))
        return [datamodels.ListedItem.model_validate(listing) for listing in await cursor.fetchall()]


async def fetch_all_items():
    async with aiosqlite.connect("./prime.db") as db:
        db.row_factory = utils.dict_factory
        cursor = await db.execute("SELECT * FROM item")
        return [datamodels.Item.model_validate(item) for item in await cursor.fetchall()]


async def delete_item(item_id: int):
    async with aiosqlite.connect("./prime.db") as db:
        # Stop repeating code. Create connection/pool on module load,
        # if modules each having them doesn't cause conflicts. Else, maybe store in the FastAPI() if APIRouter
        # has access
        async with db.execute("DELETE FROM item WHERE item_id = ?", (item_id,)):
            await db.commit()
