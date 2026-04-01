import os
from azure.identity import ClientSecretCredential

SUBSCRIPTION_ID = "988db02a-e73a-40c8-9c76-744b8b58da45"
LOCATION = "eastus"
RG_NAME = "vm-python-lab"

credential = ClientSecretCredential(
    tenant_id=os.environ["AZURE_TENANT_ID"],
    client_id=os.environ["AZURE_CLIENT_ID"],
    client_secret=os.environ["AZURE_CLIENT_SECRET"]
)
