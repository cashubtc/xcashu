import asyncio

from cashu.wallet.wallet import Wallet
from cashu.core.migrations import migrate_databases
from cashu.wallet import migrations
from cashu.core.settings import CASHU_DIR, LIGHTNING, MINT_PRIVATE_KEY

async def init_wallet(wallet: Wallet):
    """Performs migrations and loads proofs from db."""
    await migrate_databases(wallet.db, migrations)
    await wallet.load_proofs()
    await wallet.load_mint()

async def main():
    wallet = Wallet("http://127.0.0.1:8000/csat", "data/wallet")
    await init_wallet(wallet)
    print(wallet.proofs)
    r = await wallet.mint(100)
    print(wallet.proofs)
if __name__ == "__main__":
    asyncio.run(main())
