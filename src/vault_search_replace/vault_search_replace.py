import sys

import hvac
import typer
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

    return any(
        string_to_match in str(element)
        or string_to_match in (str(elements_list.get(element)))
        or string_to_match in entry
        for element in elements_list
    )


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


@app.command()
def replace(
    string_to_search: str,
    string_to_replace: str,
    vault_namespace: str = "",
    vault_base_url: str = "",
    vault_access_token: str = "",
):
    print(f"Hello {string_to_search} {string_to_replace}")


if __name__ == "__main__":
    app()
