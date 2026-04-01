from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from config import credential, SUBSCRIPTION_ID, LOCATION, RG_NAME

compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)
network_client = NetworkManagementClient(credential, SUBSCRIPTION_ID)

nic = network_client.network_interfaces.get(RG_NAME, "windows-nic")

compute_client.virtual_machines.begin_create_or_update(
    RG_NAME,
    "windows-vm",
    {
        "location": LOCATION,
        "hardware_profile": {"vm_size": "Standard_B1s"},
        "storage_profile": {
            "image_reference": {
                "publisher": "MicrosoftWindowsServer",
                "offer": "WindowsServer",
                "sku": "2019-Datacenter",
                "version": "latest"
            }
        },
        "os_profile": {
            "computer_name": "winvm",
            "admin_username": "azureuser",
            "admin_password": "YourPassword123!"
        },
        "network_profile": {
            "network_interfaces": [{"id": nic.id}]
        }
    }
).result()

print("✅ Windows VM Created")

compute_client.virtual_machine_extensions.begin_create_or_update(
    RG_NAME,
    "windows-vm",
    "CustomScriptExtension",
    {
        "location": LOCATION,
        "publisher": "Microsoft.Compute",
        "virtual_machine_extension_type": "CustomScriptExtension",
        "type_handler_version": "1.10",
        "settings": {
            "fileUris": ["https://github.com/mistahbellz/IIS_php_VMLab/blob/main/IIS_php.ps1"],
            "commandToExecute": "powershell -ExecutionPolicy Unrestricted -File IIS_php.ps1"
        }
    }
).result()

print("✅ Windows IIS + PHP setup complete")




