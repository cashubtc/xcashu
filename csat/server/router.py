from fastapi import APIRouter

router: APIRouter = APIRouter()

@router.get(
    "/api",
    name="API endpoint",
    summary="Example API endpoint",
)
async def api_example():
    return {"return" : "This is your response"}
