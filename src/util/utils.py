from fastapi.security import OAuth2PasswordBearer
from ..models import datamodels
import os
import jose.jwt
from datetime import timedelta, datetime


def dict_factory(cursor, row):
    """Use this as the row factory to replace tuples with dicts for Pydantic validation"""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


async def encode_token(data: dict):
    pre_token = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes=float(os.getenv("TOKEN_EXPIRE_MINUTES")))
    pre_token.update({"exp": expiration})
    return jose.jwt.encode(pre_token, os.getenv("OPENSSL_SECRET"), algorithm=os.getenv("OPENSSL_ALGO"))


async def decode_token(token: OAuth2PasswordBearer("token")) -> datamodels.TokenData:
    inf = jose.jwt.decode(token, os.getenv("OPENSSL_SECRET"), algorithms=[os.getenv("OPENSSL_ALGO")])
    return datamodels.TokenData(email=inf.get("sub"), user_id=inf.get("id"))
