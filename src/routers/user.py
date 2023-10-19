import uuid
from typing import Annotated

import aiosqlite
import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from ..models import datamodels
from ..util import utils

router = APIRouter(
    prefix=""  # note for testing: swagger only supports /token, not /users/token. Remove prefix
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pass_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/me")
async def get_self(token: Annotated[str, Depends(oauth2_scheme)]) -> datamodels.Customer:
    account = await utils.decode_token(token)
    return await get_customer_from_id(account)


@router.post("/token", response_model=datamodels.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # TODO: Flatten this to check for and handle various errors (wrong pass, user exists, etc)
    print("hi")
    if not validate_pass(form_data.password, await get_password(form_data.username)):
        raise HTTPException(
            status_code=401, detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = await utils.encode_token({"sub": form_data.username,
                                      "id": await get_id(form_data.username)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
async def register_user(user_info: datamodels.AccountNoId):
    return f"User {user_info.name_f} was created with id {await write_user(user_info)}"


async def user_exists(email: str) -> bool:
    async with aiosqlite.connect("./prime.db") as db:
        cur = await db.execute("SELECT * FROM account where email = ?", (email,))
        return bool(await cur.fetchone())


def validate_pass(entered: str, hashed: str):
    return pass_ctx.verify(entered, hashed)


async def get_password(email: str):
    async with aiosqlite.connect("./prime.db") as db:
        cur = await db.execute("SELECT password FROM account where email = ?", (email,))
        pass_w = await cur.fetchone()
        return pass_w[0]


async def get_id(email: str):
    async with aiosqlite.connect("./prime.db") as db:
        cur = await db.execute("SELECT acct_id FROM account where email = ?", (email,))
        act_id = await cur.fetchone()
        return act_id[0]


async def write_user(info: datamodels.AccountNoId):
    async with aiosqlite.connect("./prime.db") as db:
        user_id = uuid.uuid4()
        try:
            await db.execute("INSERT INTO account (acct_id, name_f, email, password) VALUES (?,?,?,?)",
                             (str(user_id), info.name_f, info.email,
                              pass_ctx.hash(info.password)))
            await db.commit()
            await write_customer(datamodels.Customer(user_id=str(user_id), name_f=info.name_f))
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="This email is already registered.")
        return user_id


async def write_customer(info: datamodels.Customer):
    async with aiosqlite.connect("./prime.db") as db:
        await db.execute("INSERT INTO customer VALUES (?,?,?,?,?)",
                         (info.user_id, info.name_f, info.name_l, info.cart, info.prefs))
        await db.commit()


async def get_customer_from_id(data: datamodels.TokenData) -> datamodels.Customer:
    async with aiosqlite.connect("./prime.db") as db:
        db.row_factory = utils.dict_factory
        cur = await db.execute("SELECT * FROM customer where user_id = ?", (data.user_id,))
        result = await cur.fetchone()
        return datamodels.Customer.model_validate(result)
