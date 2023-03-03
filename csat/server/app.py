from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware


from csat.server.ledger import startup_cashu_mint
from csat.server.router import router
from csat.server.ledger import csat_router

class EcashHeaderMiddleware(BaseHTTPMiddleware):
    """
    Middleware that checks the HTTP headers for ecash
    """

    async def dispatch(self, request, call_next):
        # all requests to /csat/* are not checked
        if not request.url.path.startswith("/csat/"):
            # check whether valid ecash was provided in header
            print("Cashu-csat header:", request.headers.get("Cashu-csat"))
            proofs = request.headers.get("Cashu-csat")
            await self._set_proofs_pending(proofs)
            try:
                await self._verify_proofs(proofs)
                await self._invalidate_proofs(proofs)
            except Exception as e:
                raise e
            finally:
                # delete proofs from pending list
                await self._unset_proofs_pending(proofs)

        response = await call_next(request)
        return response


def create_app() -> FastAPI:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"],
        ), 
        Middleware(EcashHeaderMiddleware),
    ]

    app = FastAPI(
        title="csat",
        description="API access with Cashu",
        license_info={
            "name": "MIT License",
            "url": "https://raw.githubusercontent.com/cashubtc/cashu/main/LICENSE",
        },
        middleware=middleware,
    )
    return app


app = create_app()

app.include_router(router=router)
app.include_router(router=csat_router)

@app.on_event("startup")
async def startup_mint():
    await startup_cashu_mint()

