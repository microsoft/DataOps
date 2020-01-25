# Package maintainer documentation

## Testing and releasing


Create a Databricks workspace for integration testing, and provision a service principal with Contributor permissions on the workspace.

Use tox to run integration tests and release the package to PyPI.

To install tox:
`pip install tox`

To run tests and release:
```
export TENANT_ID=YOUR_AZURE_ACTIVE_DIRECTORY_TENANT_ID
export CLIENT_ID=YOUR_SERVICE_PRINCIPAL_CLIENT_ID
export CLIENT_SECRET=YOUR_SERVICE_PRINCIPAL_CLIENT_SECRET
export DATABRICKS_HOST=https://REGION.azuredatabricks.net/api/2.0
export DATABRICKS_RG=YOUR_DATABRICKS_WORKSPACE_RESOURCE_GROUP
export DATABRICKS_WORKSPACE=YOUR_DATABRICKS_WORKSPACE_NAME

tox
```
