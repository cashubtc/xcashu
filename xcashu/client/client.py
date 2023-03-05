import asyncio
import requests
import sys

import sys

from cashu.wallet.wallet import Wallet
from cashu.core.migrations import migrate_databases
from cashu.wallet import migrations
from cashu.core.helpers import sum_proofs

base_url = "http://127.0.0.1:8000"
s = requests.Session()
VERBOSE = True

import time


async def init_wallet():
    """Performs migrations and loads proofs from db."""
    wallet = Wallet(f"{base_url}/cashu", "data/wallet")
    await migrate_databases(wallet.db, migrations)
    await wallet.load_proofs()
    await wallet._load_mint_keys()
    return wallet


async def request_wrapped(wallet, *args, **kwargs):
    if VERBOSE:
        print(f"Wallet balance: {sum_proofs(wallet.proofs)} sats")
    proofs = wallet.proofs[:1]
    token = await wallet.serialize_proofs(
        proofs,
        include_mints=True,
    )

    s.headers.update({"X-Cashu": token})
    resp = s.request(*args, **kwargs)

    await wallet.invalidate(proofs, check_spendable=False)
    if VERBOSE:
        print(f"Wallet balance: {sum_proofs(wallet.proofs)} sats")
    try:
        resp.raise_for_status()
    except Exception as e:
        print(e)
    resp_dict = resp.json()
    print(resp_dict)
    return resp


async def main():
    # no argument: request /api without ecash
    if sys.argv[1] != "mint" and len(sys.argv[2:]) == 0:
        resp = s.request("GET", sys.argv[1])
        try:
            resp.raise_for_status()
        except Exception as e:
            print(e)
        resp_dict = resp.json()
        print(resp_dict)

        return

    wallet = await init_wallet()

    if sys.argv[1] == "mint":
        if VERBOSE:
            print("Minting 100 sats")
        r = await wallet.mint_amounts(100 * [1])
        if VERBOSE:
            print(f"Wallet balance: {sum_proofs(wallet.proofs)} sats")
        return

    if sys.argv[2] == "ecash":
        await request_wrapped(wallet, "GET", sys.argv[1])
        return


if __name__ == "__main__":
    asyncio.run(main())
