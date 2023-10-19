from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def return_root():
    return "See the docs at /docs or /redoc"

