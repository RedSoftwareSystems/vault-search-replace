# vault-search-replace
Simple Python Script to Search (and replace) secrets content in hashicorp vault.

## Rationale
Recently, I have come across the fact that no API allows to simply search for **_values within secrets_**.
The specific use case I am working on is to change database connection strings for java based microservices.

## Running the script
Best option is to install [uv](https://docs.astral.sh/uv/) and run the script with:

`uv run vault_search_replace.py`

The script has [inline metadata](https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies) and will run without installation.

## Usage

```shell
vault_search_replace.py [OPTIONS] 
                      STRING_TO_SEARCH 
                      VAULT_NAMESPACE
                      VAULT_BASE_URL 
                      VAULT_ACCESS_TOKEN
                      [REPLACEMENT_STRING]
```
Where
 * STRING_TO_SEARCH is the string to be searched
 * VAULT_NAMESPACE is the vault namespace to be searched
 * VAULT_BASE_URL is the vault address
 * VAULT_ACCESS_TOKEN is the vault token 
 * REPLACEMENT_STRING (optional) is the string to replace the searched string
 * the only OPTION is --no-dry-run to confirm the replacement of the string (default is that the string is not replaced)
