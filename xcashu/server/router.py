from fastapi import APIRouter

router: APIRouter = APIRouter()


@router.get(
    "/paid/api",
    name="Paid API endpoint",
)
async def api_paid_example():
    return {"return": "This is your paid response"}


@router.get(
    "/api",
    name="Free API endpoint",
)
async def api_free_example():
    return {"return": "This is your free response"}
