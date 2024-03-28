import aiosqlite
import dotenv
from fastapi import FastAPI, staticfiles

from .routers import main, user, item, scrape


app = FastAPI()
app.mount("/static", staticfiles.StaticFiles(directory="src/Website"), name="page")


app.include_router(main.router)
app.include_router(user.router)
app.include_router(item.router)
app.include_router(scrape.router)


@app.on_event("startup")
async def start():
    dotenv.load_dotenv(".env")
    await make_db("./prime.db")


async def make_db(path: str):
    async with aiosqlite.connect(path) as db:
        """Creates an SQLite database with the outlined tables if one, and each table, does not exist already.. """
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
                         "seller_id TEXT NOT NULL,"
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
        await db.execute("CREATE TABLE IF NOT EXISTS news ("
                         "time TEXT NOT NULL,"
                         "title TEXT NOT NULL,"
                         "content TEXT,"
                         "thumbnail TEXT,"
                         "source TEXT NOT NULL"
                         ")")
        await db.execute("CREATE TABLE IF NOT EXISTS tracking ("
                         "url TEXT NOT NULL,"
                         "frequency INTEGER NOT NULL,"
                         "selector TEXT NOT NULL"
                         ")")
