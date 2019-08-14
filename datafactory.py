import os
import json
from datetime import datetime
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from dotenv import load_dotenv

project_folder = os.path.expanduser("/home/admin1/Desktop/TwitterLiveData") # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

#print(os.environ.get('AZURE_TENANT_ID'))
#print(os.environ.get('AZURE_CLIENT_ID'))
#print(os.environ.get('AZURE_CLIENT_SECRET'))
#print(os.environ.get('AZURE_SUBSCRIPTION_ID'))




EAST_US = "eastus2"
GROUP_NAME = "sukanyaresourcegrp1"

AZURE_TENANT_ID=os.environ.get('AZURE_TENANT_ID')
AZURE_CLIENT_ID=os.environ.get('AZURE_CLIENT_ID')
AZURE_CLIENT_SECRET=os.environ.get('AZURE_CLIENT_SECRET')
AZURE_SUBSCRIPTION_ID=os.environ.get('AZURE_SUBSCRIPTION_ID')


def run_example():
    """Resource Group management example."""
    #
    # Create the Resource Manager Client with an Application (service principal) token provider
    #
    subscription_id = os.environ.get(
        "AZURE_SUBSCRIPTION_ID", os.environ.get('AZURE_SUBSCRIPTION_ID')
    )  # your Azure Subscription Id

    credentials = ServicePrincipalCredentials(
        client_id=os.environ.get('AZURE_CLIENT_ID'),
        secret=os.environ.get('AZURE_CLIENT_SECRET'),
        tenant=os.environ.get('AZURE_TENANT_ID'),
    )

    client = ResourceManagementClient(credentials, subscription_id)
    resource_group_params = {"location": "eastus2"}

    # List Resource Groups
    print("List Resource Groups")
    for item in client.resource_groups.list():
        print_item(item)

        # Create Resource group
        print("Create Resource Group")
        print_item(
            client.resource_groups.create_or_update(
                GROUP_NAME, resource_group_params)
        )

    # Delete Resource group and everything in it
    print("Delete Resource Group")
    delete_async_operation = client.resource_groups.delete(GROUP_NAME)
    delete_async_operation.wait()
    print("\nDeleted: {}".format(GROUP_NAME))

def print_item(group):
    """Print a ResourceGroup instance."""
    print("\tName: {}".format(group.name))
    print("\tId: {}".format(group.id))
    print("\tLocation: {}".format(group.location))
    print("\tTags: {}".format(group.tags))
    print_properties(group.properties)

def print_properties(props):
    """Print a ResourceGroup properties instance."""
    if props and props.provisioning_state:
        print("\tProperties:")
        print("\t\tProvisioning State: {}".format(props.provisioning_state))
    print("\n\n")



if __name__ == "__main__":
    run_example()











