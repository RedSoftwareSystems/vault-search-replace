import sys

import hvac
import typer
from typing import Annotated, Optional, List
from dotenv import load_dotenv
from loguru import logger
import requests
import json

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

    return any(
        string_to_match in str(element)
        or string_to_match in (str(elements_list.get(element)))
        or string_to_match in entry
        for element in elements_list
    )


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


def replace_in_list(
    list_of_vaults: List,
    search_string: str,
    replace_string: str,
    vault_base_url,
    vault_access_token,
):
    headers = {"X-Vault-Token": vault_access_token}

    for vault in list_of_vaults:
        vault_url = f"{vault_base_url}/v1/adeo/cdp/oreo/secret/data/{vault}"
        response = requests.get(vault_url, headers=headers)

        response_text = response.text

        if response_text.find(search_string) > 0:
            print(f"Vault {vault} will be modified")
            newdata = response_text.replace(search_string, replace_string)
            response_dict = json.loads(newdata)
            data = response_dict["data"]
            post_response = requests.post(vault_url, headers=headers, json=data)


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


    """
    global_key_list = []

    client = hvac.Client(
        url=vault_base_url, namespace=vault_namespace, token=vault_access_token
    )

    logger.info(client.is_authenticated())
    list_response = client.secrets.kv.v2.list_secrets(
        path="",
    )

    global_path_list = list_response["data"]["keys"]

    logger.info(global_path_list)

    recursive_list = recursive_list_keys(global_key_list, client=client, path="")

    result_list = [
        entry
        for entry in recursive_list
        if find_string(client=client, entry=entry, string_to_match=string_to_search)
    ]

    if result_list:
        print(
            f"Search Key {string_to_search} has been found in:\n{'\n'.join(result_list)}"
        )
    else:
        print(f"Search Key {string_to_search} not found")

    if replacement_string != "" and no_dry_run:
        replace_in_list(
            result_list,
            string_to_search,
            replacement_string,
            vault_base_url,
            vault_access_token,
        )


if __name__ == "__main__":
    typer.run(main)
    app()
