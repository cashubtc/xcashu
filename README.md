# xcashu
X-Cashu – HTTP 402: Payment Required

<p align="center">
<img width="500" alt="Screenshot 2023-03-05 at 04 05 36" src="https://user-images.githubusercontent.com/93376500/222955642-5c442c71-a031-45d1-80a9-8e3f1400bd62.png">
</p>

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
