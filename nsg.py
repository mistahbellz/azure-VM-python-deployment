from azure.mgmt.network import NetworkManagementClient
from config import credential, SUBSCRIPTION_ID, LOCATION, RG_NAME

client = NetworkManagementClient(credential, SUBSCRIPTION_ID)

NSG_NAME = "nsg-lab"

client.network_security_groups.begin_create_or_update(
    RG_NAME,
    NSG_NAME,
    {
        "location": LOCATION,
        "security_rules": [
            {
                "name": "Allow-HTTP",
                "protocol": "Tcp",
                "source_port_range": "*",
                "destination_port_range": "80",
                "source_address_prefix": "*",
                "destination_address_prefix": "*",
                "access": "Allow",
                "priority": 1000,
                "direction": "Inbound"
            }
        ]
    }
).result()

print("✅ NSG Created")


