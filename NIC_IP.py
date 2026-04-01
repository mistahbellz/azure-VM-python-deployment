from azure.mgmt.network import NetworkManagementClient
from config import credential, SUBSCRIPTION_ID, LOCATION, RG_NAME

client = NetworkManagementClient(credential, SUBSCRIPTION_ID)

VNET_NAME = "vnet-lab"
SUBNET_NAME = "subnet-lab"
NSG_NAME = "nsg-lab"

def create_nic(nic_name, ip_name):
    public_ip = client.public_ip_addresses.begin_create_or_update(
        RG_NAME,
        ip_name,
        {
          "location": LOCATION,
           "sku": {
                    "name": "Standard"
                  },
          "public_ip_allocation_method": "Static"
        }
    ).result()

    subnet = client.subnets.get(RG_NAME, VNET_NAME, SUBNET_NAME)
    nsg = client.network_security_groups.get(RG_NAME, NSG_NAME)

    nic = client.network_interfaces.begin_create_or_update(
        RG_NAME,
        nic_name,
        {
            "location": LOCATION,
            "ip_configurations": [{
                "name": "ipconfig1",
                "subnet": {"id": subnet.id},
                "public_ip_address": {"id": public_ip.id}
            }],
            "network_security_group": {"id": nsg.id}
        }
    ).result()

    print(f"✅ NIC Created: {nic_name}")

create_nic("linux-nic", "linux-ip")
create_nic("windows-nic", "windows-ip")


