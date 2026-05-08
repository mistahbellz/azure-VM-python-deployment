from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from config import credential, SUBSCRIPTION_ID, LOCATION, RG_NAME

import base64

cloud_init = """#cloud-config
package_update: true
packages:
  - apache2
  - php

runcmd:
  - systemctl enable apache2
  - systemctl start apache2
  - echo "<?php echo 'Hello from Linux VM via Azure Automation'; ?>" > /var/www/html/index.php
  - rm /var/www/html/index.html
"""

custom_data = base64.b64encode(cloud_init.encode()).decode()


compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)
network_client = NetworkManagementClient(credential, SUBSCRIPTION_ID)

nic = network_client.network_interfaces.get(RG_NAME, "linux-nic")

compute_client.virtual_machines.begin_create_or_update(
    RG_NAME,
    "linux-vm",
    {
        "location": LOCATION,
        "hardware_profile": {"vm_size": "Standard_FX2ms_v2"},
        "storage_profile": {
            "image_reference": {
                "publisher": "Canonical",
                "offer": "0001-com-ubuntu-server-jammy",
                "sku": "22_04-lts-gen2",
                "version": "latest"
            }
        },
       "os_profile": {
                        "computer_name": "linuxvm",
                        "admin_username": "miztahbellz",
                        "admin_password": "password123!",
                        "custom_data": custom_data,
                        "linux_configuration": {
                            "disable_password_authentication": False
                            }
                    },

        "network_profile": {
            "network_interfaces": [{"id": nic.id}]
        }
    }
).result()

print("✅ Linux VM Created")
