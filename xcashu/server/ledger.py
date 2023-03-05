from typing import Union

from cashu.mint.ledger import Ledger
from cashu.core.migrations import migrate_databases
from cashu.mint import migrations
from cashu.core.settings import MINT_PRIVATE_KEY
from cashu.core.db import Database
from cashu.lightning.lnbits import LNbitsWallet  # type: ignore
from cashu.core.base import (
    GetMintResponse,
    KeysResponse,
    GetMintResponse,
    KeysResponse,
    PostMintRequest,
    PostMintResponse,
)
from cashu.core.errors import CashuError

ledger = Ledger(
    db=Database("mint", "data/mint"),
    seed=MINT_PRIVATE_KEY,
    derivation_path="0/0/0/0",
    lightning=LNbitsWallet(),
)


async def startup_cashu_mint():
    await migrate_databases(ledger.db, migrations)
    await ledger.load_used_proofs()
    await ledger.init_keysets(autosave=False)


from fastapi import APIRouter

csat_router: APIRouter = APIRouter(prefix="/cashu")


@csat_router.get(
    "/keys",
    name="Mint public keys",
    summary="Get the public keys of the newest mint keyset",
)
async def keys() -> KeysResponse:
    """This endpoint returns a dictionary of all supported token values of the mint and their associated public key."""
    keyset = ledger.get_keyset()
    keys = KeysResponse.parse_obj(keyset)
    return keys


@csat_router.get("/mint", name="Request mint", summary="Request minting of new tokens")
async def request_mint(amount: int = 0) -> GetMintResponse:
    """
    Request minting of new tokens. The mint responds with a Lightning invoice.
    This endpoint can be used for a Lightning invoice UX flow.

    Call `POST /mint` after paying the invoice.
    """
    payment_request, payment_hash = await ledger.request_mint(amount)
    print(f"Lightning invoice: {payment_request}")
    resp = GetMintResponse(pr=payment_request, hash=payment_hash)
    return resp


@csat_router.post(
    "/mint",
    name="Mint tokens",
    summary="Mint tokens in exchange for a Bitcoin paymemt that the user has made",
)
async def mint(
    payload: PostMintRequest,
    payment_hash: Union[str, None] = None,
) -> Union[PostMintResponse, CashuError]:
    """
    Requests the minting of tokens belonging to a paid payment request.

    Call this endpoint after `GET /mint`.
    """
    try:
        promises = await ledger.mint(payload.outputs, payment_hash=payment_hash)
        blinded_signatures = PostMintResponse(promises=promises)
        return blinded_signatures
    except Exception as exc:
        return CashuError(code=0, error=str(exc))
