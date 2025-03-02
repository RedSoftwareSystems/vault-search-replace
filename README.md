# vault-search-replace
Simple Python Script to Search (and replace) secrets content in hashicorp vault.

## Rationale
Recently, I have come across the fact that no API allows to simply search for **_values within secrets_**.
The specific use case I am working on is to change database connection strings for java based microservices.

## Running the script
Best option is to install [uv](https://docs.astral.sh/uv/) and run the script with:

`uv run vault_search_replace.py`

The script has [inline metadata](https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies) and will run without installation.


