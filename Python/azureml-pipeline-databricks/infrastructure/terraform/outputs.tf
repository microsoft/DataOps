output "subscription_id" {
  value = data.azurerm_client_config.current.subscription_id
}

output "resource_group_name" {
  value = azurerm_resource_group.main.name
}

output "aml_workspace_id" {
    value = module.azureml.id
}

output "aml_workspace_name" {
    value = module.azureml.name
}

output "databricks_workspace_name" {
    value = module.databricks.name
}

output "databricks_location" {
    value = module.databricks.location
}
