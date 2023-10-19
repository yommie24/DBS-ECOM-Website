from fastapi import APIRouter, responses

router = APIRouter()


@router.get("/")
async def return_root():
    return responses.RedirectResponse("static/PrimeTime.html")

