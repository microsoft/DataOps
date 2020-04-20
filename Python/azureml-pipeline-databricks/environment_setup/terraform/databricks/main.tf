data "azurerm_virtual_network" "main" {
  name                = var.vnet_name
  resource_group_name  = var.resource_group_name
}

data "azurerm_subnet" "databricks-private" {
  name                 = var.private_subnet_name
  virtual_network_name = var.vnet_name
  resource_group_name  = var.resource_group_name
}

data "azurerm_subnet" "databricks-public" {
  name                 = var.public_subnet_name
  virtual_network_name = var.vnet_name
  resource_group_name  = var.resource_group_name
}

resource "azurerm_network_security_group" "databricks" {
  name     = "nsg-${var.appname}-${var.environment}-databricks"
  location            = var.location
  resource_group_name = var.resource_group_name
}

resource "azurerm_subnet_network_security_group_association" "private" {
  subnet_id                 = data.azurerm_subnet.databricks-private.id
  network_security_group_id = azurerm_network_security_group.databricks.id
}

resource "azurerm_subnet_network_security_group_association" "public" {
  subnet_id                 = data.azurerm_subnet.databricks-public.id
  network_security_group_id = azurerm_network_security_group.databricks.id
}

resource "azurerm_databricks_workspace" "main" {
  name                = "dbricks-${var.appname}-${var.environment}"
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = "standard"

  custom_parameters {
    public_subnet_name = data.azurerm_subnet.databricks-public.name
    private_subnet_name = data.azurerm_subnet.databricks-private.name
    virtual_network_id = data.azurerm_virtual_network.main.id
  }

  depends_on = [
    azurerm_subnet_network_security_group_association.private,
    azurerm_subnet_network_security_group_association.public,
  ]
}
