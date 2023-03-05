# xcashu
X-Cashu – HTTP 402: Payment Required

# Install
- Install Python and Poetry environments as described here: https://github.com/cashubtc/cashu
- Run LNbits instance (Lightning backend)
- Edit `.env` file as needed

```sh
MINT_PRIVATE_KEY="This must be set"
LIGHTNING=FALSE
TOR=FALSE
DEBUG=TRUE
LNBITS_ENDPOINT=https://localhost:5001
LNBITS_KEY=<lnbits_admin_key>
```

Install all dependencies

```
git clone <this_repo>
poetry install
```

# Server
```sh
poetry run python -m uvicorn xcashu.server.app:app
```

# Client

Free endpoint:

```
poetry run python xcashu/client/client.py http://localhost:8000/api
```

Paid endpoint with no ecash:

```
poetry run python xcashu/client/client.py http://localhost:8000/paid/api
```

Mint ecash (LIGHTNING=FALSE means you can do this for free):

```
poetry run python xcashu/client/client.py mint
```


Paid endpoint with ecash:

```
poetry run python xcashu/client/client.py http://localhost:8000/paid/api ecash
```