# databricks-client

## About

A REST client for the [Databricks REST API](https://docs.databricks.com/dev-tools/api/latest/index.html).

This module is a thin layer allowing to build HTTP [Requests](https://requests.readthedocs.io/en/master/).
It does not expose API operations as distinct methods, but rather exposes generic methods allowing
to build API calls.

The Databricks API sometimes returns 200 error codes and HTML content when the request is not
properly authenticated. The client intercepts such occurrences (detecting non-JSON returned content)
and wraps them into an exception.

_This open-source project is not developed by nor affiliated with Databricks._

## Installing

```
pip install databricks-client
```

## Usage

```python
import databricks_client

client = databricks_client.create("https://northeurope.azuredatabricks.net/api/2.0")
client.auth_pat_token(pat_token)
client.ensure_available()
clusters_list = client.get('clusters/list')
for cluster in clusters_list["clusters"]:
    print(cluster)
```

## Usage with a newly provisioned workspace

If using this module as part of a provisioning job, you need to call `client.ensure_available()`.

When the first user logs it to a new Databricks workspace, workspace provisioning is triggered,
and the API is not available until that job has completed (that usually takes under a minute,
but could take longer depending on the network configuration).

The method `client.ensure_available(url="instance-pools/list", retries=100, delay_seconds=6)`
attempts connecting to the provided URL and retries as long as the workspace is in provisioning
state, or until the given number of retries has elapsed.

## Usage with Azure Active Directory

Note: Azure AD authentication for Databricks is currently in preview.

The client generates short-lived Azure AD tokens. If you need to use your client for longer
than the lifetime (typically 30 minutes), rerun `client.auth_azuread` periodically.

### Azure AD authentication with Azure CLI

[Install the Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest).

```
pip install databricks-client[azurecli]
az login
```

```python
import databricks_client

client = databricks_client.create("https://northeurope.azuredatabricks.net/api/2.0")
client.auth_azuread("/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/my-rg/providers/Microsoft.Databricks/workspaces/my-workspace")
# or client.auth_azuread(resource_group="my-rg", workspace_name="my-workspace")
client.ensure_available()
clusters_list = client.get('clusters/list')
for cluster in clusters_list["clusters"]:
    print(cluster)
```

This is recommended with Azure DevOps Pipelines using the [Azure CLI task](https://docs.microsoft.com/en-us/azure/devops/pipelines/tasks/deploy/azure-cli?view=azure-devops).

### Azure AD authentication with ADAL

```
pip install databricks-client
pip install adal
```

```python
import databricks_client
import adal

authority_host_uri = 'https://login.microsoftonline.com'
authority_uri = authority_host_uri + '/' + tenant_id
context = adal.AuthenticationContext(authority_uri)

def token_callback(resource):
    return context.acquire_token_with_client_credentials(resource, client_id, client_secret)["accessToken"]

client = databricks_client.create("https://northeurope.azuredatabricks.net/api/2.0")
client.auth_azuread("/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/my-rg/providers/Microsoft.Databricks/workspaces/my-workspace", token_callback)
# or client.auth_azuread(resource_group="my-rg", workspace_name="my-workspace", token_callback=token_callback)
client.ensure_available()
clusters_list = client.get('clusters/list')
for cluster in clusters_list["clusters"]:
    print(cluster)
```

## Example usages

### Generating a PAT token

```python
response = client.post(
    'token/create',
    json={"lifetime_seconds": 60, "comment": "Unit Test Token"}
)
pat_token = response['token_value']
```

### Uploading a notebook

```python
import base64

with open(notebook_file, "rb") as f:
    file_content = f.read()

client.post(
    'workspace/import',
    json={
        "content": base64.b64encode(file_content).decode('ascii'),
        "path": notebook_path,
        "overwrite": False,
        "language": "PYTHON",
        "format": "SOURCE"
    }
)
```

