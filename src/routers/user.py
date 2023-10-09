from fastapi import APIRouter

router = APIRouter(
    prefix="/user"
)


@router.get("/help")
async def help():
    return "helpppp user"

