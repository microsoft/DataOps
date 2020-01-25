from azureml.core import Workspace
from azureml.core.compute import DatabricksCompute
from azureml.core.compute import ComputeTarget
from env_variables import Env


def get_databricks_compute(
    workspace: Workspace,
    compute_name: str,
):
    if compute_name not in workspace.compute_targets:
        return None
    compute_target = workspace.compute_targets[compute_name]
    if compute_target and type(compute_target) is DatabricksCompute:
        return compute_target
    raise ValueError(
        "Compute target %s is of different type" % (compute_target))


def create_databricks_compute(
    workspace: Workspace,
    compute_name: str,
    access_token: str,
):
    e = Env()

    compute_config = DatabricksCompute.attach_configuration(
        resource_group=e.resource_group,
        workspace_name=e.databricks_workspace_name,
        access_token=access_token)

    compute_target = ComputeTarget.attach(
        workspace, compute_name, compute_config)

    compute_target.wait_for_completion(
        show_output=True)

    return compute_target
