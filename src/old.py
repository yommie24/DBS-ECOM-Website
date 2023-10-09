from typing import Annotated

import aiosqlite
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# connection = sqlite3.connect("testing.db")
# db = connection.cursor()
# db.execute("CREATE TABLE IF NOT EXISTS users(username TEXT UNIQUE, password VARCHAR(72), disabled BOOLEAN)")
# db.execute("INSERT INTO users (username, password, disabled) VALUES(?, ?, ?)", ("johndoe", "secret", "False"))
# db.execute("INSERT INTO users (username, password, disabled) VALUES(?, ?, ?)", ("alice", "secret2", "True"))
# print(db.execute("SELECT * FROM users").fetchall())




app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None
#
#
# class UserInDB(User):
#     password: str

class User:
    def __init__(self, db_user: tuple):
        self.username = db_user[0]
        self.disabled = db_user[2]


async def get_user(username: str, pass_w: str):
    result = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if result:
        if result[2]:
            print("disabled")
        if secrets.compare_digest(result[1], pass_w):
            print("good")
            return User(result)
        else:
            print("bad")


@app.get("/getuser")
async def grab(user, passw):
    return await get_user(user, passw)

#
#
# def fake_decode_token(token):
#     # This doesn't provide any security at all
#     # Check the next version
#     user = get_user(fake_users_db, token)
#     return user
#
#
# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user
#
#
# async def get_current_active_user(
#         current_user: Annotated[User, Depends(get_current_user)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#
#


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await get_user(form_data.username, form_data.password)
    # if not user_dict:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    # user = UserInDB(**user_dict)
    # hashed_password = fake_hash_password(form_data.password)
    # if not hashed_password == user.hashed_password:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


# @app.get("/users/me")
# async def read_users_me(
#         current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return current_user
