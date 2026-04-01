from azure.mgmt.network import NetworkManagementClient
from config import credential, SUBSCRIPTION_ID, LOCATION, RG_NAME

client = NetworkManagementClient(credential, SUBSCRIPTION_ID)

VNET_NAME = "vnet-lab"
SUBNET_NAME = "subnet-lab"

client.virtual_networks.begin_create_or_update(
    RG_NAME,
    VNET_NAME,
    {
        "location": LOCATION,
        "address_space": {"address_prefixes": ["10.0.0.0/16"]}
    }
).result()

client.subnets.begin_create_or_update(
    RG_NAME,
    VNET_NAME,
    SUBNET_NAME,
    {"address_prefix": "10.0.0.0/24"}
).result()

print("✅ Network Created")

