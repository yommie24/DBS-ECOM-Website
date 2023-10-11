from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
import aiosqlite
from ..models import datamodels
from passlib.context import CryptContext
import secrets
import uuid

router = APIRouter(
    prefix="/user"
)
oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pass_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # TODO: Flatten this to check for and handle various errors (wrong pass, user exists, etc)
    if validate_pass(form_data.password, await get_password(form_data.username)):
        print("hi")
    else:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/register")
async def register_user(user_info: datamodels.AccountNoId):
    return f"User {user_info.name_f} was created with id {await write_user(user_info)}"


async def user_exists(email: str) -> bool:
    async with aiosqlite.connect("./testing.db") as db:
        cur = await db.execute("SELECT * FROM account where email = ?", (email,))
        return bool(await cur.fetchone())


def validate_pass(entered: str, hashed: str):
    # return secrets.compare_digest(entered, hashed)
    return pass_ctx.verify(entered, hashed)


async def get_password(email: str):
    async with aiosqlite.connect("./testing.db") as db:
        cur = await db.execute("SELECT password FROM account where email = ?", (email,))
        passw = await cur.fetchone()
        return passw[0]


async def write_user(info: datamodels.AccountNoId):
    async with aiosqlite.connect("./testing.db") as db:
        user_id = uuid.uuid4()
        await db.execute("INSERT INTO account (acct_id, name_f, email, password) VALUES (?,?,?,?)",
                         (str(user_id), info.name_f, info.email,
                          pass_ctx.hash(info.password)))
        await db.commit()
        return user_id
