# Deploy a Resource Group with Azure resources.
#
# For suggested naming conventions, refer to:
#   https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/naming-and-tagging

# Resource Group

resource "azurerm_resource_group" "main" {
  name   = "rg-${var.appname}-${var.environment}-main"
  location = var.location
}

module "azureml" {
  source = "./azureml"
  appname = var.appname
  environment = var.environment
  location = var.location
  tenant_id = data.azurerm_client_config.current.tenant_id
  resource_group_name = azurerm_resource_group.main.name
}

module "training-data" {
  source = "./training-data"
  appname = var.appname
  environment = var.environment
  resource_group_name = azurerm_resource_group.main.name
  location = var.location
}

module "databricks" {
  source = "./databricks"
  appname = var.appname
  environment = var.environment
  resource_group_name = azurerm_resource_group.main.name
  location = var.location
}
