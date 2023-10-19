import aiosqlite
import dotenv
from fastapi import FastAPI, staticfiles

from .routers import main, user, item


app = FastAPI()
app.mount("/static", staticfiles.StaticFiles(directory="src/Website"), name="page")


app.include_router(main.router)
app.include_router(user.router)
app.include_router(item.router)


@app.on_event("startup")
async def start():
    dotenv.load_dotenv(".env")
    await make_db("./prime.db")


async def make_db(path: str):
    async with aiosqlite.connect(path) as db:
        """Creates an SQLite database with the outlined tables if one, and each table, does not exist already.. """
        # TODO: Write the list parser. SQLite doesn't support TEXT[].
        # Just make a function to separate each address/tag with an uncommon symbol,
        # and parse it later
        # Alternatively, send them with the request body and store as an image table or other datatype entirely
        # Note SQLite doesn't support varchar or uuid types. Just use normal 128-length uuids and 72-length bcrypt.
        # TODO: consider removing the listing table if the performance is good enough to fetch everything
        # TODO: Consider the same for customer, or adding seller info to customer
        await db.execute("CREATE TABLE IF NOT EXISTS account ("
                         "acct_id TEXT PRIMARY KEY NOT NULL,"
                         "name_f TEXT NOT NULL,"
                         "name_l TEXT,"
                         "email TEXT NOT NULL UNIQUE,"
                         "password TEXT NOT NULL,"
                         "address TEXT,"
                         "contact TEXT"
                         ")")
        await db.execute("CREATE TABLE IF NOT EXISTS customer ("
                         "user_id TEXT NOT NULL,"
                         "name_f TEXT NOT NULL,"
                         "name_l TEXT,"
                         "cart TEXT[],"
                         "prefs TEXT[],"
                         "FOREIGN KEY(user_id) REFERENCES account(acct_id))")
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
