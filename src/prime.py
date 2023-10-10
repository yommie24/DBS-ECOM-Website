from fastapi import FastAPI
import aiosqlite
from .routers import main, user, item


app = FastAPI()

app.include_router(main.router)
app.include_router(user.router)
app.include_router(item.router)


@app.on_event("startup")
async def start():
    await make_db("./testing.db")


async def make_db(path: str):
    async with aiosqlite.connect(path) as db:
        """ Note SQLite doesn't support varchar or uuid types. 
        Just use normal 128-length uuids and 72-length bcrypt."""
        # TODO: Write the list parser. SQLite doesn't support TEXT[]. Maybe use CSV? It's hard to parse with the
        #  dict_factory though
        # Alternatively, send them with the request body and store as an image table or other datatype entirely
        await db.execute("CREATE TABLE IF NOT EXISTS account ("
                         "id TEXT PRIMARY KEY NOT NULL,"
                         "name_f TEXT NOT NULL,"
                         "name_l TEXT,"
                         "email TEXT NOT NULL,"
                         "password TEXT NOT NULL,"
                         "address TEXT[],"
                         "contact TEXT[]"
                         ")")
        await db.execute("CREATE TABLE IF NOT EXISTS customer ("
                         "id TEXT NOT NULL,"
                         "name_f TEXT NOT NULL,"
                         "name_l TEXT,"
                         "cart TEXT[],"
                         "prefs TEXT[],"
                         "FOREIGN KEY(id) REFERENCES account(id))")
        await db.execute("CREATE TABLE IF NOT EXISTS item ("
                         "item_id INTEGER PRIMARY KEY,"  # rowid, see https://www.sqlite.org/autoinc.html
                         "name TEXT NOT NULL,"
                         "image TEXT,"
                         "price REAL,"
                         "description TEXT,"
                         "seller_id TEXT,"
                         "tag TEXT,"
                         "sku TEXT"
                         ")")
        await db.execute("CREATE TABLE IF NOT EXISTS listing ("
                         "item_id INTEGER NOT NULL,"
                         "name TEXT NOT NULL,"
                         "thumbnail TEXT,"
                         "price REAL,"
                         "tag TEXT,"
                         "FOREIGN KEY(item_id) REFERENCES item(item_id)"
                         ")")
