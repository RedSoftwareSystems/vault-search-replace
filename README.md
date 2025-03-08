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
### Command Line Parameters:

#### Required:
string_to_search
vault_namespace
vault_base_url
vault_access_token

#### Optional
string_to_replace

#### Options
--no-dry-run - confirm the execution

Without the (optional) replace_string argument, the command will execute a (string) search for _search_string_.
With the replace argument, the command will execute a **dry-run** of the replace operation (no change will be applied). To force the creation of new secrets
versions, the **--no-dry-run** option has to be passed.

As of this release, the search is very simple (python **str.find** function). 