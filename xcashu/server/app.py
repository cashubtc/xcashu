from fastapi import FastAPI, HTTPException
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


from xcashu.server.ledger import startup_cashu_mint
from xcashu.server.router import router
from xcashu.server.ledger import csat_router, ledger

from cashu.core.base import TokenV2
import json
import base64


class EcashHeaderMiddleware(BaseHTTPMiddleware):
    """
    Middleware that checks the HTTP headers for ecash
    """

    async def dispatch(self, request, call_next):
        # all requests to /cashu/* are not checked for ecash
        if request.url.path.startswith("/paid/"):
            # check whether valid ecash was provided in header
            token = request.headers.get("X-Cashu")
            if not token:
                payment_request, payment_hash = await ledger.request_mint(1000)
                return JSONResponse(
                    {
                        "detail": "This endpoint requires a X-Cashu ecash header",
                        "pr": payment_request,
                        "hash": payment_hash,
                        "mint": "http://localhost:8000/cashu",
                    },
                    status_code=402,
                )
            tokenv2 = TokenV2.parse_obj(json.loads(base64.urlsafe_b64decode(token)))
            proofs = tokenv2.proofs
            await ledger._set_proofs_pending(proofs)
            try:
                await ledger._verify_proofs(proofs)
                await ledger._invalidate_proofs(proofs)
            except Exception as e:
                return JSONResponse({"detail": str(e)}, status_code=402)
            finally:
                # delete proofs from pending list
                await ledger._unset_proofs_pending(proofs)

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
        title="Cashu csat",
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
