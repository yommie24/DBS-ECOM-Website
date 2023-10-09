from fastapi import APIRouter, HTTPException
import aiosqlite
import sqlite3
import uuid
from ..models import datamodels

router = APIRouter(
    prefix="/item"
)


@router.get("/{item_id}")
async def find(item_id: int):
    return await get_item(item_id)


@router.post("/new")
async def create(item: datamodels.Item):
    return await make_item(item)


async def get_item(item_id: int):
    async with aiosqlite.connect("./testing.db") as db:
        try:
            cursor = await db.execute("SELECT * FROM item WHERE id = ?", (item_id,))
            result = await cursor.fetchone()
        except sqlite3.OperationalError:  # item table doesn't exist
            pass
        if not result:
            return HTTPException(status_code=404, detail=f"An item with id {item_id} was not found.")
        print(result)


async def make_item(item):
    async with aiosqlite.connect("./testing.db") as db:
        cursor = await db.execute("INSERT INTO item (name, images, price, description, seller_id, tags, sku) "
                                  "VALUES (?, NULL, ?, ?, ?, NULL, ?)", (
                                      item.name, item.price, item.desc, str(item.seller), item.sku))
        # return cursor.lastrowid
        async with db.execute("SELECT * FROM item") as cur:
            strang = ""
            async for x in cur:
                strang += str(x)
            return strang
