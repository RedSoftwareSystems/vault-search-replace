import sys

import hvac
import typer
from typing import Annotated, Optional, List
from dotenv import load_dotenv
from loguru import logger

from importlib.metadata import version

__version__ = version("vault-search-replace")


logger.remove()

app = typer.Typer(
    name="vault-search-replace",
    add_completion=False,
    help="An utility to search and replace Vault secrets.",
)


@app.callback()
def callback(
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Enable verbose logging")
    ] = False,
):
    """
    Vault Search Replace utility.
    """
    load_dotenv(verbose=True)
    level = "DEBUG" if verbose else "INFO"
    logger.add(sys.stderr, level=level)
    typer.echo(f"Vault Search Replace v{__version__}")


def list_keys(client: hvac.Client, path: str) -> []:
    logger.debug(f"Requested PATH is :{path}")
    if path is None:
        path = ""
    response = client.secrets.kv.v2.list_secrets(path=path)
    logger.debug(response)
    logger.debug(response["data"]["keys"])
    return response["data"]["keys"]


def recursive_list_keys(global_key_list: [], client: hvac.Client, path: str) -> []:
    entry: str

    for key in list_keys(client=client, path=path):
        if key.endswith("/"):
            logger.debug(f"Key {key} is a directory")
            recursive_list_keys(
                global_key_list=global_key_list, client=client, path=f"{path}{key}"
            )
        else:
            logger.debug(f"Key {key} is an entry")
            entry = f"{path}{key}"
            global_key_list.append(entry)

    return global_key_list


def find_string(client: hvac.Client, entry: str, string_to_match: str) -> bool:
    logger.debug(f"Requested KEY is :{entry}")
    data = client.secrets.kv.v2.read_secret(path=entry)["data"]
    logger.debug(f"Data --> {data}")

    elements_list = data["data"].values()

    for element in elements_list:
        if str(element).find(string_to_match) > -1:
            logger.debug(element)
            return True
    return False


def recursive_replace(data, search_string: str, replace_string: str):
    if isinstance(data, dict):
        return {
            k: recursive_replace(v, search_string, replace_string)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [recursive_replace(v, search_string, replace_string) for v in data]
    elif isinstance(data, str):
        return data.replace(search_string, replace_string)
    else:
        return data


def find_diff(old, new, path=""):
    diff = {}
    if isinstance(old, dict) and isinstance(new, dict):
        for k in old:
            if k in new:
                diff.update(find_diff(old[k], new[k], f"{path}.{k}" if path else k))
    elif isinstance(old, list) and isinstance(new, list):
        for i, (o, n) in enumerate(zip(old, new)):
            diff.update(find_diff(o, n, f"{path}[{i}]"))
    elif old != new:
        diff[path] = (old, new)
    return diff


def replace_in_list(
    client: hvac.Client,
    list_of_vaults: List[str],
    search_string: str,
    replace_string: str,
    dry_run: bool = True,
):
    for vault in list_of_vaults:
        try:
            read_response = client.secrets.kv.v2.read_secret(path=vault)
            secret_data = read_response["data"]["data"]

            new_secret_data = recursive_replace(
                secret_data, search_string, replace_string
            )

            if new_secret_data != secret_data:
                if dry_run:
                    typer.echo(f"[DRY-RUN] Secret '{vault}' would be modified:")
                    diff = find_diff(secret_data, new_secret_data)
                    for k, (old, new) in diff.items():
                        typer.echo(f"  - {k}: '{old}' -> '{new}'")
                else:
                    typer.echo(f"Updating secret '{vault}'...")
                    client.secrets.kv.v2.create_or_update_secret(
                        path=vault, secret=new_secret_data
                    )
        except hvac.exceptions.Forbidden:
            logger.error(f"Permission denied to read/write secret: {vault}")
        except Exception as e:
            logger.error(f"Error processing secret {vault}: {e}")


@app.command()
def search(
    string_to_search: Annotated[str, typer.Argument(help="String to Search")],
    vault_namespace: Annotated[str, typer.Argument(help="Vault Namespace")],
    vault_base_url: Annotated[str, typer.Argument(help="Vault Base url to Search")],
    vault_access_token: Annotated[str, typer.Argument(help="Vault Access Token")],
    ctx: typer.Context,
):
    """
    Search strings in Hashicorp Vault secrets.
    """
    typer.echo("Search command")

    global_function(
        string_to_search, vault_namespace, vault_base_url, vault_access_token, "", False
    )


@app.command()
def replace(
    string_to_search: Annotated[str, typer.Argument(help="String to Search")],
    vault_namespace: Annotated[str, typer.Argument(help="Vault Namespace")],
    vault_base_url: Annotated[str, typer.Argument(help="Vault Base url to Search")],
    vault_access_token: Annotated[str, typer.Argument(help="Vault Access Token")],
    replacement_string: Annotated[str, typer.Argument(help="String to Replace")] = None,
    execute: Annotated[
        bool,
        typer.Option(
            "--execute",
            help="Apply the changes (default is dry-run)",
            is_flag=True,
        ),
    ] = False,
):
    """
    Search and replace strings in Hashicorp Vault secrets.
    """
    typer.echo("replace command")
    global_function(
        string_to_search,
        vault_namespace,
        vault_base_url,
        vault_access_token,
        replacement_string,
        execute,
    )


def global_function(
    string_to_search,
    vault_namespace,
    vault_base_url,
    vault_access_token,
    replacement_string,
    execute: bool,
):
    global_key_list = []

    try:
        client = hvac.Client(
            url=vault_base_url, namespace=vault_namespace, token=vault_access_token
        )

        if not client.is_authenticated():
            typer.secho("Vault authentication failed", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        recursive_list = recursive_list_keys(global_key_list, client=client, path="")

        result_list = [
            entry
            for entry in recursive_list
            if find_string(client=client, entry=entry, string_to_match=string_to_search)
        ]

        if not result_list:
            typer.echo(f"String '{string_to_search}' not found in any secrets.")
            return

        typer.echo(f"Found '{string_to_search}' in {len(result_list)} secret(s):")
        for entry in result_list:
            typer.echo(f"  - {entry}")

        if replacement_string:
            replace_in_list(
                client,
                result_list,
                string_to_search,
                replacement_string,
                dry_run=not execute,
            )
            if not execute:
                typer.secho(
                    "\nDry-run complete. Use --execute to apply changes.",
                    fg=typer.colors.YELLOW,
                )
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        raise typer.Exit(code=1)
