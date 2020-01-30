import sys
import requests
import json
import time
from requests.exceptions import HTTPError


class DatabricksNotAvailableException(Exception):
    """Databricks was not available.
    """


class DatabricksPayloadException(IOError):
    """Databricks returned an unexpected payload.
    """

    def __init__(self, *args, **kwargs):
        response = kwargs.pop('response', None)
        self.response = response
        self.request = kwargs.pop('request', None)
        if (response is not None
                and not self.request
                and hasattr(response, 'request')):
            self.request = self.response.request
        super(DatabricksPayloadException, self).__init__(*args, **kwargs)


class DatabricksClient(object):
    def __init__(self, host):
        self.host = host.strip('/')
        self.dbricks_auth = {}

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

    def query_exec(self, method, url, **kwargs):
        """
        Run a REST query against the Databricks API.
        Raises an exception on any non-success response.
        """

        full_url = self.host + '/' + url.lstrip('/')
        response = method(full_url, headers=self.dbricks_auth, **kwargs)
        return response

    def query_raw(self, method, url, **kwargs):
        """
        Run a REST query against the Databricks API.
        Raises an exception on any non-success response.
        """

        response = self.query_exec(method, url, **kwargs)
        try:
            response.raise_for_status()
        except HTTPError:
            sys.stderr.write(response.text)
            raise
        return response

    def ensure_available(
            self,
            url="instance-pools/list",
            retries=100,
            delay_seconds=6,
            **kwargs):
        """
        When the first user logs it to a new Databricks workspace, workspace
        provisioning is triggered, which results in 400 errors until
        provisioning is complete. Retrying for some time allows provisioning
        to complete (that usually takes under a minute).

        This method attempts connecting to the provided URL and retries
        as long an error 400 with INVALID_PARAMETER_VALUE in the message
        is returned, or until the given number of retries has elapsed.

        This is the response returned by Databricks until provisioning
        has completed:
        400 Client Error: Bad Request
        {"error_code":"INVALID_PARAMETER_VALUE",
         "message":
          "Unknown worker environment WorkerEnvId(workerenv-6183622352140885)"}

        throws DatabricksNotAvailableException if the number of retries
               have been exhausted.
        throws HTTPError if Databricks returns an unexpected error response.
        """
        for try_num in range(retries):
            try:
                response = self.query_exec(requests.get, url, **kwargs)
                response.raise_for_status()
                return
            except HTTPError:
                if ("INVALID_PARAMETER_VALUE" not in response.text):
                    raise
            time.sleep(delay_seconds)
        raise DatabricksNotAvailableException()


def create(*args, **kwargs):
    return DatabricksClient(*args, **kwargs)
