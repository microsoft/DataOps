import databricks_client
import os
import pytest
import requests
import adal
from azure.common.credentials import get_azure_cli_credentials

credentials, subscription_id = get_azure_cli_credentials()
dbricks_api = os.environ["DATABRICKS_HOST"]
resource_group = os.environ["DATABRICKS_RG"]
workspace_name = os.environ["DATABRICKS_WORKSPACE"]
resource_id = (
    '/subscriptions/%s/resourceGroups/%s/providers/'
    'Microsoft.Databricks/workspaces/%s' %
    (subscription_id, resource_group, workspace_name)
)


client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
tenant_id = os.environ["TENANT_ID"]

authority_host_uri = 'https://login.microsoftonline.com'
authority_uri = authority_host_uri + '/' + tenant_id
context = adal.AuthenticationContext(authority_uri)


def get_clusters_list(client):
    response = client.get('clusters/list')
    assert "clusters" in response


def test_get_clusters_list():
    client = databricks_client.create(dbricks_api)
    client.auth_azuread(workspace_resource_id=resource_id)
    get_clusters_list(client)


def test_query_clusters_list():
    client = databricks_client.create(dbricks_api)
    client.auth_azuread(workspace_resource_id=resource_id)
    response = client.query(
        requests.get,
        'clusters/list',
    )
    assert "clusters" in response


def test_pat_token():
    client = databricks_client.create(dbricks_api)
    client.auth_azuread(workspace_resource_id=resource_id)
    response = client.post(
        'token/create',
        json={"lifetime_seconds": 60, "comment": "Unit Test Token"}
    )
    pat_client = databricks_client.create(client.host)
    pat_client.auth_pat_token(response['token_value'])
    get_clusters_list(pat_client)


def test_rethrows_http_error():
    client = databricks_client.create(dbricks_api)
    client.auth_pat_token("dapi0000000")
    with pytest.raises(requests.exceptions.HTTPError):
        get_clusters_list(client)


def test_throws_exception_on_non_json_response():
    client = databricks_client.create(dbricks_api)
    resource_id = (
        '/subscriptions/%s/resourceGroups/%s/providers/'
        'Microsoft.Databricks/workspaces/%s' %
        (subscription_id, resource_group, 'dummydummy')
    )
    client.auth_azuread(workspace_resource_id=resource_id)
    with pytest.raises(databricks_client.DatabricksPayloadException):
        get_clusters_list(client)


def test_workspace_name():
    client = databricks_client.create(dbricks_api)
    client.auth_azuread(
        resource_group=resource_group, workspace_name=workspace_name)
    get_clusters_list(client)


def test_credentials(mocker):
    get_cred = mocker.patch(
        "azure.common.credentials.get_azure_cli_credentials")
    client = databricks_client.create(dbricks_api)

    client.auth_azuread(resource_id, lambda r: credentials.get_token(r).token)
    get_clusters_list(client)
    get_cred.assert_not_called()


def test_credentials_msrest():
    client = databricks_client.create(dbricks_api)

    def token_callback(resource):
        return context.acquire_token_with_client_credentials(
            resource, client_id, client_secret)["accessToken"]
    client.auth_azuread(resource_id, token_callback)
    get_clusters_list(client)
