import os

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def get_secret(secret_name: str) -> str:
    vault_url = os.environ["KEY_VAULT_URL"]
    client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
    return client.get_secret(secret_name).value
