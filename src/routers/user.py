from fastapi import APIRouter
from ..models import datamodels
import aiosqlite

router = APIRouter(
    prefix="/user"
)


@router.get("/register")
async def register_user(user_info: datamodels.UserRegister):
    return "helpppp user"

async def write_user():
    async with aiosqlite.connect("./testing.db") as db:
        async with db.execute("INSERT INTO account (acct_id, ) VALUES (") as cur:
            pass

