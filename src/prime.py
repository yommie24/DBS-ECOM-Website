from fastapi import FastAPI, APIRouter
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
        # TODO: Write the list parser. SQLite doesn't support TEXT[], but we can do CSV with it
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
                         "id ROWID,"  # rowid, see https://www.sqlite.org/autoinc.html
                         "name TEXT NOT NULL,"
                         "images TEXT[],"
                         "price REAL,"
                         "description TEXT,"
                         "seller_id TEXT,"
                         "tags TEXT[],"
                         "sku TEXT"
                         ")")
        await db.execute("CREATE TABLE IF NOT EXISTS listing ("
                         "id INTEGER NOT NULL,"
                         "name TEXT NOT NULL,"
                         "thumbnail TEXT,"
                         "price REAL,"
                         "tags TEXT[],"
                         "FOREIGN KEY(id) REFERENCES item(id)"
                         ")")

        await db.execute("INSERT INTO customer VALUES ('123', 'john', 'doe', NULL, NULL)")
        await db.execute("INSERT INTO account VALUES ('123', 'john', 'doe', 'jd@jd.com', '1234', 'addr', 'phone')")

        async with db.execute("SELECT * FROM account") as cur:
            async for x in cur:
                print(x)

        async with db.execute("SELECT * FROM customer") as cur:
            async for x in cur:
                print(x)
