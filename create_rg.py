from azure.mgmt.resource import ResourceManagementClient
from config import credential, SUBSCRIPTION_ID, LOCATION, RG_NAME

client = ResourceManagementClient(credential, SUBSCRIPTION_ID)

client.resource_groups.create_or_update(
    RG_NAME,
    {"location": LOCATION}
)

print("✅ Resource Group Created")
