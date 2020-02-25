resource "azurerm_databricks_workspace" "aml" {
  name                = "dbricks${var.appname}${var.environment}"
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = "standard"
}

resource "azurerm_role_assignment" "databricks_mlpipeline" {
  scope                = azurerm_databricks_workspace.aml.id
  role_definition_name = "Contributor"
  principal_id         = var.devops_mlpipeline_sp_object_id
}
