# vault-search-replace
Simple Python Script to Search (and replace) secrets content in hashicorp vault.

## Rationale
Recently, I have come across the fact that no API allows to simply search for **_values within secrets_**.
The specific use case I am working on is to change database connection strings for java based microservices.

## Running the script
Best option is to install [uv](https://docs.astral.sh/uv/). After that you can run the script with 

`uvx vault_search_replace`

or 

`uv tool install vault_search_replace`

The package is published on PyPI and all the dependencies are installed automatically.

## Usage

```shell
vault-search-replace --help   
                                                                                                                          
 Usage: vault-search-replace [OPTIONS] COMMAND [ARGS]...                                                                  
                                                                                                                          
 An utility to search and replace Vault secrets.                                                                          
                                                                                                                          
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --verbose  -v        Enable verbose logging                                                                            │
│ --help               Show this message and exit.                                                                       │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ search   Search strings in Hashicorp Vault secrets.                                                                    │
│ replace  Search and replace strings in Hashicorp Vault secrets.                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```shell
vault-search-replace search --help
Vault Search Replace v0.3.0
                                                                                                                          
 Usage: vault-search-replace search [OPTIONS] STRING_TO_SEARCH VAULT_NAMESPACE                                            
                                    VAULT_BASE_URL VAULT_ACCESS_TOKEN                                                     
                                                                                                                          
 Search strings in Hashicorp Vault secrets.                                                                               
                                                                                                                          
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    string_to_search        TEXT  String to Search [required]                                                         │
│ *    vault_namespace         TEXT  Vault Namespace [required]                                                          │
│ *    vault_base_url          TEXT  Vault Base url to Search [required]                                                 │
│ *    vault_access_token      TEXT  Vault Access Token [required]                                                       │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```shell
vault-search-replace replace --help
Vault Search Replace v0.3.0
                                                                                                                          
 Usage: vault-search-replace replace [OPTIONS] STRING_TO_SEARCH VAULT_NAMESPACE                                           
                                     VAULT_BASE_URL VAULT_ACCESS_TOKEN                                                    
                                     [REPLACEMENT_STRING]                                                                 
                                                                                                                          
 Search and replace strings in Hashicorp Vault secrets.                                                                   
                                                                                                                          
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    string_to_search          TEXT  String to Search [required]                                                       │
│ *    vault_namespace           TEXT  Vault Namespace [required]                                                        │
│ *    vault_base_url            TEXT  Vault Base url to Search [required]                                               │
│ *    vault_access_token        TEXT  Vault Access Token [required]                                                     │
│      [replacement_string]      TEXT  String to Replace                                                                 │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --execute          Apply the changes (default is dry-run)                                                              │
│ --help             Show this message and exit.                                                                         │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```
### Command Line Parameters:

#### Common to both commands:
string_to_search
vault_namespace
vault_base_url
vault_access_token

#### Only for replace
string_to_replace

#### Options - on replace command
--execute - confirm the execution

As of this release, the search is very simple (python **str.find** function). 