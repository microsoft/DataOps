import sys
import requests
import json
from requests.exceptions import HTTPError


class DatabricksPayloadException(IOError):
    """Databricks returned an unexpected payload.
    """

    def __init__(self, *args, **kwargs):
        response = kwargs.pop('response', None)
        self.response = response
        self.request = kwargs.pop('request', None)
        if (response is not None and not self.request and
                hasattr(response, 'request')):
            self.request = self.response.request
        super(DatabricksPayloadException, self).__init__(*args, **kwargs)


class DatabricksClient(object):
    def __init__(self, host):
        self.host = host.strip('/')

    def auth_pat_token(self, pat_token):
        self.dbricks_auth = {
            'Authorization': 'Bearer %s' % pat_token
        }

    def auth_azuread(
        self,
        workspace_resource_id=None,
        token_callback=None,
        subscription_id=None,
        resource_group=None,
        workspace_name=None
    ):
        if token_callback is None:
            from azure.common.credentials import get_azure_cli_credentials
            credentials, subscription_id = get_azure_cli_credentials()

            def token_callback(resource):
                return credentials.get_token(resource).token
        if workspace_resource_id is None:
            if resource_group is None or workspace_name is None:
                raise ValueError(
                    "Either workspace_resource_id or both of "
                    "resource_group and workspace_name must be provided")
            if subscription_id is None:
                raise ValueError("subscription_id must be provided")
            workspace_resource_id = (
                '/subscriptions/%s/resourceGroups/%s/providers/'
                'Microsoft.Databricks/workspaces/%s'
                % (subscription_id, resource_group, workspace_name)
            )

        adb_token = token_callback('2ff814a6-3304-4ab8-85cb-cd0e6f879c1d')
        arm_token = token_callback('https://management.core.windows.net/')

        self.dbricks_auth = {
            'Authorization': 'Bearer %s' % adb_token,
            'X-Databricks-Azure-SP-Management-Token': arm_token,
            'X-Databricks-Azure-Workspace-Resource-Id': workspace_resource_id,
        }

    def get(self, url, **kwargs):
        return self.query(requests.get, url, **kwargs)

    def post(self, url, **kwargs):
        return self.query(requests.post, url, **kwargs)

    def query(self, method, url, **kwargs):
        response = self.query_raw(method, url, **kwargs)
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            sys.stderr.write(response.text)
            raise DatabricksPayloadException(response=response) from None

    def query_raw(self, method, url, **kwargs):
        """
        Run a REST query against the Databricks API.
        Raises an exception on any non-success response.
        """

        full_url = self.host + '/' + url.lstrip('/')
        response = method(full_url, headers=self.dbricks_auth, **kwargs)
        try:
            response.raise_for_status()
        except HTTPError:
            sys.stderr.write(response.text)
            raise
        return response


def create(*args, **kwargs):
    return DatabricksClient(*args, **kwargs)
