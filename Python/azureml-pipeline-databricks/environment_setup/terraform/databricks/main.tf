resource "azurerm_databricks_workspace" "aml" {
  name                = "dbricks${var.appname}${var.environment}"
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = "standard"
}
