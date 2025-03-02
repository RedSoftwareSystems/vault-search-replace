import sys

import hvac
import typer
from typing import Annotated, Optional, List
from dotenv import load_dotenv
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")

app = typer.Typer()

load_dotenv(verbose=True)


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

    elements_list = data["data"]

    for element in elements_list:
        if (
            str(element).find(string_to_match) > -1
            or (str(elements_list.get(element))).find(string_to_match) > -1
            or entry.find(string_to_match) > -1
        ):
            return True
    return False


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


def verify_key(client: hvac.Client, entry: str, string_to_match: str) -> bool:
    return False


@app.command()
def search(
    string_to_search: str,
    vault_namespace: str = "",
    vault_base_url: str = "",
    vault_access_token: str = "",
):
    global_key_list = []

    client = hvac.Client(
        url=vault_base_url, namespace=vault_namespace, token=vault_access_token
    )

    list_response = client.secrets.kv.v2.list_secrets(
        path="",
    )
    global_path_list = list_response["data"]["keys"]

    recursive_list = recursive_list_keys(global_key_list, client=client, path="")

    for entry in recursive_list:
        if find_string(client=client, entry=entry, string_to_match=string_to_search):
            print(f"Found {entry}")


def main(
    string_to_search: Annotated[str, typer.Argument(help="String to Search")],
    vault_namespace: Annotated[str, typer.Argument(help="Vault Namespace")],
    vault_base_url: Annotated[str, typer.Argument(help="Vault Base url to Search")],
    vault_access_token: Annotated[str, typer.Argument(help="Vault Access Token")],
    replacement_string: Annotated[
        Optional[str], typer.Argument(help="String to Replace")
    ] = None,
    no_dry_run: Annotated[
        bool, typer.Option(help="No Dry Run - Execute the Change")
    ] = False,
):
    """
    This command allows for a search (and eventual replace) of strings within an hashicorp vault namespace.

    :param string_to_search: The string you are looking for
    :param replacement_string: Replacement String
    :param vault_namespace: Vault namespace (if empty, VAULT_NAMESPACE env variable will be used)
    :param vault_base_url:
    :param vault_access_token:
    :param no_dry_run:
    :return:
    """


if __name__ == "__main__":
    typer.run(main)
    app()
